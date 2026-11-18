"""Corre todos los escenarios con EPANET 2.0.12 (y 2.2 como control) y calcula las tablas del informe.

Todos los numeros del informe salen de aqui; nada se copia a mano.
"""
import math
import os
import shutil
import subprocess

import numpy as np
import pandas as pd

import modelo as M
import motor

J = list(M.JUNCTIONS)
G = 9.81
A_T = math.pi * M.TANK["diam"] ** 2 / 4
Z_T = M.TANK["base"]
H_MAX = Z_T + M.TANK["max"]
H_INI = Z_T + M.TANK["init"]

# Curva de la bomba H = A - B Q^C (ajuste de 3 puntos, Q en L/s)
(_, A_P), (Q1, H1), (Q2, H2) = M.PUMP_CURVE
C_P = math.log((A_P - H2) / (A_P - H1)) / math.log(Q2 / Q1)
B_P = (A_P - H1) / Q1 ** C_P
# Hazen-Williams: constante SI equivalente a la de EPANET (4.727 en unidades inglesas)
K_EPANET = 4.727 * 0.0283168 ** -1.852 * 0.3048 ** 4.871

NOMBRE = {"PMP-1-S": "PMP-1", "PMP-1-D": "PMP-1"}
for _v in M.PRVS:
    NOMBRE[f"{_v}-A"] = _v
    NOMBRE[f"{_v}-B"] = _v


def nom(n):
    return NOMBRE.get(n, n)


def h_bomba(q):
    return A_P - B_P * q ** C_P


# ---------------------------------------------------------------- escenarios estaticos
def estatico(r):
    t = 0
    H, P, D, Q, V, S = (r.head.loc[t], r.pressure.loc[t], r.demand.loc[t],
                        r.flow.loc[t], r.velocity.loc[t], r.status.loc[t])
    nudos = pd.DataFrame({"z": [r.elev[j] for j in J], "q": D[J].values, "H": H[J].values, "p": P[J].values}, index=J)
    tub = []
    for p, (n1, n2, L, d) in M.PIPES.items():
        q = Q[p]
        cerrada = S[p] == 0
        if abs(q) < 0.005:
            sentido = "—"
        else:
            a, b = (n1, n2) if q > 0 else (n2, n1)
            sentido = f"{nom(a)} → {nom(b)}"
        hf = 0.0 if cerrada else abs(H[n1] - H[n2])
        tub.append(dict(tubo=p, sentido=sentido, L=L, D=d, Q=abs(q), V=V[p], hf=hf, S=hf / L * 1000,
                        estado="Cerrada" if cerrada else "Abierta"))
    tub = pd.DataFrame(tub).set_index("tubo")
    bomba = bomba_en(r, t)
    prv = prv_en(r, t)
    otros = dict(R_Q=-D["R-1"], T_Q=D["T-1"], T_H=H["T-1"], T_nivel=H["T-1"] - Z_T,
                 P16_estado="Cerrada" if S["P-16"] == 0 else "Abierta")
    return dict(nudos=nudos, tub=tub, bomba=bomba, prv=prv, **otros)


def bomba_en(r, t):
    hs, hd = r.head.loc[t, "PMP-1-S"], r.head.loc[t, "PMP-1-D"]
    q = r.flow.loc[t, "PMP-1"]
    return dict(Q=q, H=hd - hs, Hs=hs, Hd=hd, ps=hs - M.PUMP_Z, pd=hd - M.PUMP_Z, Pot=G * q / 1000 * (hd - hs))


def prv_en(r, t):
    """Estado de cada PRV. La consigna se lee del motor (setting en m de presion) + cota de la valvula."""
    out = []
    for v, (a, b, z, d, _hgl) in M.PRVS.items():
        hgl = round(float(r.setting.loc[t, v]) + z, 3)
        q = r.flow.loc[t, v]
        hi, ho = r.head.loc[t, a], r.head.loc[t, b]
        if r.status.loc[t, v] == 0 or abs(q) < 1e-4:
            est = "Cerrada"
        elif abs(ho - hgl) < 0.01:
            est = "Activa"
        else:
            est = "Abierta"
        out.append(dict(prv=v, hgl=hgl, pset=hgl - z, estado=est, Q=q, Hi=hi, Ho=ho, pi=hi - z, po=ho - z, dH=hi - ho))
    return pd.DataFrame(out).set_index("prv")


# ---------------------------------------------------------------- periodo extendido
def eps(r):
    t = np.array(r.times, dtype=float)
    dt = np.diff(t, append=t[-1])                       # duracion de cada paso (el ultimo = 0)
    P = r.pressure[J]
    rows = []
    for k, tt in enumerate(r.times):
        b = bomba_en(r, tt)
        p = P.loc[tt]
        rows.append(dict(t=tt, hora=motor.hhmm(tt), dem=r.demand.loc[tt, J].sum(), Qb=b["Q"], Hb=b["H"],
                         Q16=r.flow.loc[tt, "P-16"], HT=r.head.loc[tt, "T-1"],
                         P16="Cerrada" if r.status.loc[tt, "P-16"] == 0 else "Abierta",
                         Q1=r.flow.loc[tt, "PRV-1"], Q2=r.flow.loc[tt, "PRV-2"], Q3=r.flow.loc[tt, "PRV-3"],
                         pmin=p.min(), nmin=p.idxmin(), pmax=p.max(), nmax=p.idxmax(),
                         estados={v: e for v, e in prv_en(r, tt)["estado"].items()}))
    serie = pd.DataFrame(rows).set_index("t")
    llen = [tt for tt in r.times if r.status.loc[tt, "P-16"] == 0]
    t_lleno = llen[0] if llen else None
    vol = lambda s: float((s.values * dt).sum() / 1000)                            # m3
    pm = pd.Series({j: float((P[j].values * dt).sum() / dt.sum()) for j in J})     # media ponderada en el tiempo
    ext = pd.DataFrame({"pmin": P.min(), "tmin": P.idxmin(), "pmax": P.max(), "tmax": P.idxmax(), "pmed": pm})
    vel = r.velocity[list(M.PIPES)]
    vmax_tubo = vel.max().idxmax()
    energia = float((G * serie["Qb"].values / 1000 * serie["Hb"].values * dt).sum() / 3600)   # kWh
    despues = [tt for tt in r.times if t_lleno is not None and tt >= t_lleno]
    hj7 = r.head.loc[despues, "J-7"] if despues else pd.Series(dtype=float)
    zona_baja = P[["J-3", "J-4"]]
    q23 = serie["Q2"] + serie["Q3"]
    return dict(serie=serie, t_lleno=t_lleno, ext=ext, P=P, dt=dt,
                V_dem=vol(serie["dem"]), V_bomba=vol(serie["Qb"]), V_tanque=vol(serie["Q16"]),
                Q_med=vol(serie["dem"]) * 1000 / 86400, energia=energia,
                vmax=float(vel.max().max()), vmax_tubo=vmax_tubo, vmax_t=vel[vmax_tubo].idxmax(),
                hj7_min=float(hj7.min()) if len(hj7) else None, hj7_max=float(hj7.max()) if len(hj7) else None,
                zb_min=float(zona_baja.min().min()), zb_max=float(zona_baja.max().max()),
                q23_min=float(q23.min()), q23_max=float(q23.max()),
                prv1_siempre_cerrada=bool((serie["Q1"].abs() < 1e-4).all()),
                prv23_siempre_activas=all(e["PRV-2"] == "Activa" and e["PRV-3"] == "Activa" for e in serie["estados"]),
                Qb_min=float(serie["Qb"].min()), Qb_max=float(serie["Qb"].max()),
                Hb_min=float(serie["Hb"].min()), Hb_max=float(serie["Hb"].max()),
                dem_min=float(serie["dem"].min()), dem_max=float(serie["dem"].max()))


# ---------------------------------------------------------------- recomendaciones
def recomendaciones():
    tmp = os.path.join(M.MODELOS, "recomendaciones")
    os.makedirs(tmp, exist_ok=True)
    out = {}
    casos = {
        "R1": ("R1_PRV1_consigna_286.5.inp", "Recomendacion 1: consigna de PRV-1 = 286.5 m (Escenario 2)",
               True, False, {"PRV-1": 286.5}, ()),
        "R2": ("R2_PRV_consigna_285.0.inp", "Recomendacion 2: consigna de las tres PRV = 285.0 m (Escenario 2)",
               True, False, {"PRV-1": 285.0, "PRV-2": 285.0, "PRV-3": 285.0}, ()),
        "R1b": ("R1b_PRV1_consigna_287.0.inp", "Prueba: consigna de PRV-1 = 287.0 m, mayor que la de PRV-2 y PRV-3 (Escenario 2)",
                True, False, {"PRV-1": 287.0}, ()),
        "R3": ("R3_Control_bomba_EPS.inp", "Recomendacion 3: control de PMP-1 por nivel de T-1 (Escenario 3)",
               True, True, None, ("LINK PMP-1 CLOSED IF NODE T-1 ABOVE 17.99", "LINK PMP-1 OPEN IF NODE T-1 BELOW 12")),
    }
    for k, (fn, title, tank, eps_, prv, ctr) in casos.items():
        f = os.path.join(tmp, fn)
        M.write_inp(f, title, tank, eps_, prv_hgl=prv, controls=ctr)
        r = motor.run(f)
        d = dict(archivo=fn, r=r)
        if not eps_:
            d["prv"] = prv_en(r, 0)
            d["p"] = r.pressure.loc[0, J]
        else:
            d["eps"] = eps(r)
            st = r.status["PMP-1"]
            d["cambios"] = [(tt, int(s)) for tt, s, s0 in zip(r.times[1:], st.values[1:], st.values[:-1]) if s != s0]
            t = np.array(r.times, dtype=float)
            d["horas_bomba"] = float((np.diff(t, append=t[-1]) * (st.values > 0)).sum() / 3600)
            lvl = r.head["T-1"] - Z_T
            d["nivel_min"], d["nivel_fin"] = float(lvl.min()), float(lvl.iloc[-1])
        out[k] = d
    return out


# ---------------------------------------------------------------- salidas: .rpt y Excel
def reportes():
    """Reportes .rpt de EPANET 2.0.12 (programa de linea de comandos) y de EPANET 2.2 (WNTR)."""
    os.makedirs(M.RESULTADOS, exist_ok=True)
    exe = os.path.join(M.MOTOR, "epanet20")
    hechos = []
    for esc, (fn, *_r) in M.ESCENARIOS.items():
        base = os.path.splitext(fn)[0]
        rpt = os.path.join(M.RESULTADOS, base + "_EPANET2.0.12.rpt")
        subprocess.run([exe, M.ruta(esc), rpt], capture_output=True, timeout=60, check=False)
        hechos.append(rpt)
        try:
            import wntr
            wn = wntr.network.WaterNetworkModel(M.ruta(esc))
            pref = os.path.join("/tmp", base + "_22")
            wntr.sim.EpanetSimulator(wn).run_sim(file_prefix=pref)
            shutil.copy(pref + ".rpt", os.path.join(M.RESULTADOS, base + "_EPANET2.2.rpt"))
        except Exception as e:  # pragma: no cover
            print("aviso 2.2:", e)
    return hechos


def excel(R):
    path = os.path.join(M.RESULTADOS, "Resultados_Taller1.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        for esc in ("E1", "E2"):
            s = R[esc]
            s["nudos"].rename(columns={"z": "Elevacion (m)", "q": "Demanda (L/s)", "H": "HGL (m)", "p": "Presion (m)"}) \
                .round(3).to_excel(xw, sheet_name=f"{esc} nudos")
            s["tub"].rename(columns={"sentido": "Sentido del flujo", "L": "L (m)", "D": "D (mm)", "Q": "Q (L/s)",
                                     "V": "V (m/s)", "hf": "hf (m)", "S": "S (m/km)", "estado": "Estado"}) \
                .round(4).to_excel(xw, sheet_name=f"{esc} tuberias")
            s["prv"].rename(columns={"hgl": "Consigna HGL (m)", "pset": "Consigna p (m)", "estado": "Estado",
                                     "Q": "Q (L/s)", "Hi": "HGL entrada (m)", "Ho": "HGL salida (m)",
                                     "pi": "p entrada (m)", "po": "p salida (m)", "dH": "dH (m)"}) \
                .round(3).to_excel(xw, sheet_name=f"{esc} PRV")
        for esc in ("E3", "E3b"):
            e = R[esc]
            r = R["run"][esc]
            se = e["serie"].drop(columns=["estados"]).copy()
            se.index = se["hora"]
            se = se.drop(columns=["hora"]).rename(columns={
                "dem": "Demanda total (L/s)", "Qb": "Q bomba (L/s)", "Hb": "H bomba (m)", "Q16": "Q P-16 a T-1 (L/s)",
                "HT": "HGL T-1 (m)", "P16": "Estado P-16", "Q1": "Q PRV-1", "Q2": "Q PRV-2", "Q3": "Q PRV-3",
                "pmin": "p min (m)", "nmin": "nudo p min", "pmax": "p max (m)", "nmax": "nudo p max"})
            se.round(3).to_excel(xw, sheet_name=f"{esc} resumen horario")
            for key, nombre in (("pressure", "presiones"), ("head", "HGL")):
                df = getattr(r, key)[J + (["T-1"] if key == "head" else [])].copy()
                df.index = [motor.hhmm(t) for t in df.index]
                df.index.name = "Hora"
                df.round(3).to_excel(xw, sheet_name=f"{esc} {nombre}")
            df = r.flow[list(M.PIPES) + ["PMP-1"] + list(M.PRVS)].copy()
            df.index = [motor.hhmm(t) for t in df.index]
            df.index.name = "Hora"
            df.round(3).to_excel(xw, sheet_name=f"{esc} caudales")
    return path


# ---------------------------------------------------------------- datos derivados para el texto
def extras(R):
    import verificacion as V
    X = {}
    # Verificacion de datos y ecuaciones
    ver = {}
    for esc, (fn, title, tank, eps_, j6) in M.ESCENARIOS.items():
        errs, wn = V.datos(M.ruta(esc), eps_, j6_residencial=(j6 == "RES"), p16_abierta=tank)
        peor, fallas = V.ecuaciones(R["run"][esc], wn)
        ver[esc] = dict(datos=errs, fallas=fallas, **peor)
        if eps_:
            ver[esc]["tanque"] = V.tanque(R["run"][esc], A_T)
    X["ver"] = ver
    X["graf_dif"] = V.lectura_grafica()[2]
    # Demandas: horas de demanda maxima y minima en el Escenario 3
    s = R["E3"]["serie"]
    horas = s[s.index < 86400]
    horas = horas[horas.index % 3600 == 0]
    X["h_dem_max"] = [int(t // 3600) for t, d in horas["dem"].items() if abs(d - horas["dem"].max()) < 1e-3]
    X["h_dem_min"] = [int(t // 3600) for t, d in horas["dem"].items() if abs(d - horas["dem"].min()) < 1e-3]
    X["q_res"] = sum(q for j, (z, q, u) in M.JUNCTIONS.items() if u == "RES")
    X["q_com"] = sum(q for j, (z, q, u) in M.JUNCTIONS.items() if u == "COM")
    X["q_base"] = sum(q for z, q, u in M.JUNCTIONS.values())
    X["m_res"], X["m_com"] = sum(M.RES) / 24, sum(M.COM) / 24
    # Velocidades en el Escenario 3: tuberias que superan 0.5 m/s y cuando
    r3 = R["run"]["E3"]
    vel = r3.velocity[list(M.PIPES)]
    t = np.array(r3.times, dtype=float)
    dt = np.diff(t, append=t[-1])
    sobre = {}
    for p in M.PIPES:
        m = vel[p].values > 0.5
        if m.any():
            sobre[p] = dict(vmax=float(vel[p].max()), horas=float((dt * m).sum() / 3600),
                            fin=motor.hhmm(max(tt for tt, mm in zip(r3.times, m) if mm)))
    X["v_sobre_05"] = sobre
    X["v_max_e1"] = float(R["run"]["E1"].velocity.loc[0, list(M.PIPES)].max())
    X["v_max_e2"] = float(R["run"]["E2"].velocity.loc[0, list(M.PIPES)].max())
    X["v_tubo_e1"] = R["run"]["E1"].velocity.loc[0, list(M.PIPES)].idxmax()
    X["v_tubo_e2"] = R["run"]["E2"].velocity.loc[0, list(M.PIPES)].idxmax()
    # Sensibilidad J-6: diferencias hora a hora (solo horas enteras, comunes a ambos)
    a, b = R["run"]["E3"].pressure[J], R["run"]["E3b"].pressure[J]
    comunes = [tt for tt in a.index if tt in b.index and tt % 3600 == 0]
    X["sens_dif_horaria"] = float((a.loc[comunes] - b.loc[comunes]).abs().max().max())
    X["sens_nudo_horaria"] = (a.loc[comunes] - b.loc[comunes]).abs().max().idxmax()
    e3, e3b = R["E3"]["ext"], R["E3b"]["ext"]
    d_ext = pd.concat([(e3["pmin"] - e3b["pmin"]).abs(), (e3["pmax"] - e3b["pmax"]).abs()], axis=1).max(axis=1)
    X["sens_dif_ext"], X["sens_nudo_ext"] = float(d_ext.max()), d_ext.idxmax()
    # Presion estatica (sin consumo): zona alta con la bomba a caudal cero, zona baja con la consigna de las PRV
    h_alta = M.RESERVOIR[1] + A_P
    h_baja = max(hgl for *_r, hgl in M.PRVS.values())
    X["h_estatica_alta"], X["h_estatica_baja"] = h_alta, h_baja
    X["h_estatica_tanque"] = H_MAX
    X["p_estatica"] = {j: (h_baja if j in ("J-3", "J-4") else h_alta) - z for j, (z, q, u) in M.JUNCTIONS.items()}
    X["p_estatica_tanque"] = {j: (h_baja if j in ("J-3", "J-4") else H_MAX) - z for j, (z, q, u) in M.JUNCTIONS.items()}
    return X


# ---------------------------------------------------------------- todo
def calcular(salidas=True):
    M.generar()
    run = {esc: motor.run(M.ruta(esc), "2.0.12") for esc in M.ESCENARIOS}
    run22 = {esc: motor.run(M.ruta(esc), "2.2") for esc in M.ESCENARIOS}
    R = dict(run=run, run22=run22)
    R["E1"], R["E2"] = estatico(run["E1"]), estatico(run["E2"])
    R["E3"], R["E3b"] = eps(run["E3"]), eps(run["E3b"])
    R["rec"] = recomendaciones()
    R["dif_versiones"] = {esc: dict(H=float((run[esc].head - run22[esc].head).abs().max().max()),
                                    Q=float((run[esc].flow - run22[esc].flow).abs().max().max()),
                                    pasos=run[esc].times == run22[esc].times)
                          for esc in M.ESCENARIOS}
    R["avisos"] = {esc: run[esc].warnings for esc in M.ESCENARIOS}
    R["X"] = extras(R)
    if salidas:
        R["rpt"] = reportes()
        R["xlsx"] = excel(R)
    return R


if __name__ == "__main__":
    R = calcular()
    for esc in ("E1", "E2"):
        print(esc, R[esc]["bomba"], "\n", R[esc]["nudos"].round(2).to_string(), "\n", R[esc]["prv"].round(2).to_string())
    for esc in ("E3", "E3b"):
        e = R[esc]
        print(esc, "lleno:", motor.hhmmss(e["t_lleno"]), "V_dem", round(e["V_dem"], 1), "V_bomba", round(e["V_bomba"], 1),
              "V_tanque", round(e["V_tanque"], 2), "Qmed", round(e["Q_med"], 2), "E", round(e["energia"], 1),
              "vmax", round(e["vmax"], 3), e["vmax_tubo"], motor.hhmm(e["vmax_t"]))
        print(e["ext"].round(2).to_string())
    print("dif versiones:", R["dif_versiones"])
    print("avisos:", R["avisos"])
    for k, d in R["rec"].items():
        print(k, d.get("prv", pd.DataFrame()).round(2).to_dict() if "prv" in d else
              (d["cambios"], d["horas_bomba"], d["nivel_min"], d["nivel_fin"], round(d["eps"]["ext"]["pmax"].max(), 2),
               round(d["eps"]["ext"]["pmin"].min(), 2)))
    print(R["xlsx"])

"""Verificacion independiente de los datos y de los resultados (seccion 11 del informe).

1. Compara cada .inp con una SEGUNDA transcripcion de las tablas del taller (no usa modelo.py).
2. Comprueba que la solucion de EPANET cumple todas las ecuaciones en cada paso de calculo:
   continuidad, Hazen-Williams, curva de la bomba, logica de las PRV y balance del tanque.
"""
import math

import numpy as np
import wntr

# ---------------------------------------------------------------- segunda transcripcion del enunciado
NUDOS = {"J-1": (250, 3.2), "J-2": (265, 3.2), "J-3": (235, 4.7), "J-4": (235, 3.2),
         "J-5": (270, 4.7), "J-6": (270, 5.0), "J-7": (277, 0.0), "J-8": (276, 3.2)}
USO = {"J-1": "RESIDENCIAL", "J-2": "RESIDENCIAL", "J-3": "RESIDENCIAL", "J-7": "RESIDENCIAL",
       "J-4": "COMERCIAL", "J-5": "COMERCIAL", "J-8": "COMERCIAL"}
TUBOS = {"P-1": (3, 300), "P-2": (1525, 300), "P-3": (300, 200), "P-4": (30, 200),
         "P-5": (460, 200), "P-6": (460, 200), "P-7": (300, 200), "P-8": (30, 200),
         "P-9": (460, 200), "P-10": (460, 200), "P-11": (550, 200), "P-12": (460, 250),
         "P-13": (300, 250), "P-14": (30, 200), "P-15": (300, 200), "P-16": (460, 300)}
# Extremos segun la figura (bomba y PRV como elementos, igual que en WaterGEMS)
EXTREMOS = {"P-1": ("R-1", "PMP-1"), "P-2": ("PMP-1", "J-1"), "P-3": ("J-1", "J-2"),
            "P-4": ("J-2", "PRV-1"), "P-5": ("PRV-1", "J-3"), "P-6": ("J-3", "J-4"),
            "P-7": ("PRV-2", "J-4"), "P-8": ("J-5", "PRV-2"), "P-9": ("J-6", "J-5"),
            "P-10": ("J-1", "J-6"), "P-11": ("J-1", "J-7"), "P-12": ("J-7", "J-8"),
            "P-13": ("J-8", "J-5"), "P-14": ("J-6", "PRV-3"), "P-15": ("PRV-3", "J-3"),
            "P-16": ("J-7", "T-1")}
# PRV: elevacion, diametro, HGL de consigna, tuberia de entrada, tuberia de salida
PRV = {"PRV-1": (250, 200, 285.0, "P-4", "P-5"), "PRV-2": (253, 200, 286.5, "P-8", "P-7"),
       "PRV-3": (253, 200, 286.5, "P-14", "P-15")}
BOMBA = [(0.0, 48.8), (63.2, 39.6), (88.4, 33.8)]
Z_BOMBA = 288
TANQUE = dict(base=308, minimo=314, inicial=320, maximo=326, diametro=15)
R1_NIVEL = 290
# Lectura de los marcadores de la grafica de consumo (antes de redondear a 0.1)
GRAF_RES = [0.12, 0.12, 0.12, 0.12, 0.29, 0.79, 1.79, 1.99, 1.40, 0.99, 0.89, 0.79,
            0.70, 1.23, 1.39, 0.80, 0.69, 0.89, 0.96, 1.19, 1.39, 1.09, 0.69, 0.48]
GRAF_COM = [-0.01, -0.01, -0.01, -0.01, -0.01, 0.09, 0.39, 0.59, 1.19, 1.39, 1.49, 1.19,
            1.49, 1.09, 1.19, 0.99, 0.89, 1.19, 1.09, 0.69, 0.49, 0.19, 0.19, 0.09]

K_HW = 4.727 * 0.0283168 ** -1.852 * 0.3048 ** 4.871        # 10.667 en SI (Q m3/s, D m)
_A = BOMBA[0][1]
_C = math.log((_A - BOMBA[2][1]) / (_A - BOMBA[1][1])) / math.log(BOMBA[2][0] / BOMBA[1][0])
_B = (_A - BOMBA[1][1]) / BOMBA[1][0] ** _C


def elemento(n):
    """Nudo auxiliar de EPANET -> elemento del esquema (PMP-1-S -> PMP-1)."""
    for k in ("PMP-1", "PRV-1", "PRV-2", "PRV-3"):
        if n.startswith(k + "-"):
            return k
    return n


def lectura_grafica():
    """Maxima diferencia entre la lectura de la grafica y el valor redondeado usado."""
    res = [round(x, 1) for x in GRAF_RES]
    com = [max(0.0, round(x, 1)) for x in GRAF_COM]
    dif = max(max(abs(a - b) for a, b in zip(GRAF_RES, res)), max(abs(a - b) for a, b in zip(GRAF_COM, com)))
    return res, com, dif


def datos(inp, eps, j6_residencial=False, p16_abierta=True):
    """Lista de diferencias entre el .inp y la segunda transcripcion."""
    wn = wntr.network.WaterNetworkModel(inp)
    e = []

    def chk(c, m):
        if not c:
            e.append(m)

    for j, (z, q) in NUDOS.items():
        n = wn.get_node(j)
        chk(abs(n.elevation - z) < 1e-6, f"{j} elevacion")
        d = n.demand_timeseries_list[0]
        chk(abs(d.base_value * 1000 - q) < 1e-6, f"{j} demanda")
        esperado = USO.get(j) if eps else None
        if j == "J-6" and eps and j6_residencial:
            esperado = "RESIDENCIAL"
        chk((d.pattern_name or None) == esperado, f"{j} patron {d.pattern_name} (esperado {esperado})")
    for p, (L, D) in TUBOS.items():
        lk = wn.get_link(p)
        chk(abs(lk.length - L) < 1e-6 and abs(lk.diameter * 1000 - D) < 1e-6, f"{p} L o D")
        chk(abs(lk.roughness - 100) < 1e-6 and abs(lk.minor_loss) < 1e-9, f"{p} C o perdidas menores")
        chk((elemento(lk.start_node_name), elemento(lk.end_node_name)) == EXTREMOS[p], f"{p} conexion")
    chk(str(wn.get_link("P-16").initial_status) == ("Open" if p16_abierta else "Closed"), "P-16 estado inicial")
    for v, (z, D, hgl, ent, sal) in PRV.items():
        lk = wn.get_link(v)
        chk(lk.valve_type == "PRV", f"{v} tipo")
        chk(wn.get_link(ent).end_node_name == lk.start_node_name, f"{v} entra por {ent}")
        chk(wn.get_link(sal).start_node_name == lk.end_node_name, f"{v} sale por {sal}")
        chk(abs(lk.diameter * 1000 - D) < 1e-6, f"{v} diametro")
        for n in (lk.start_node_name, lk.end_node_name):
            chk(abs(wn.get_node(n).elevation - z) < 1e-6, f"{v} elevacion")
        chk(abs(z + lk.initial_setting - hgl) < 1e-6, f"{v} consigna")
    pm = wn.get_link("PMP-1")
    chk(wn.get_link("P-1").end_node_name == pm.start_node_name and
        wn.get_link("P-2").start_node_name == pm.end_node_name, "PMP-1 sentido")
    for n in (pm.start_node_name, pm.end_node_name):
        chk(abs(wn.get_node(n).elevation - Z_BOMBA) < 1e-6, "PMP-1 elevacion")
    pts = [(round(q * 1000, 6), round(h, 6)) for q, h in pm.get_pump_curve().points]
    chk(pts == BOMBA, "curva de la bomba")
    chk(abs(wn.get_node("R-1").base_head - R1_NIVEL) < 1e-6, "R-1")
    t = wn.get_node("T-1")
    chk((t.elevation, t.elevation + t.min_level, t.elevation + t.init_level, t.elevation + t.max_level,
         t.diameter) == (TANQUE["base"], TANQUE["minimo"], TANQUE["inicial"], TANQUE["maximo"],
                         TANQUE["diametro"]), "T-1")
    if eps:
        res, com, _ = lectura_grafica()
        chk(np.allclose(wn.get_pattern("RESIDENCIAL").multipliers, res), "curva residencial")
        chk(np.allclose(wn.get_pattern("COMERCIAL").multipliers, com), "curva comercial")
        chk(wn.options.time.duration == 24 * 3600 and wn.options.time.hydraulic_timestep == 3600
            and wn.options.time.pattern_timestep == 3600, "tiempos EPS")
    else:
        chk(wn.options.time.duration == 0, "duracion estatica")
    chk(wn.options.hydraulic.inpfile_units == "LPS" and wn.options.hydraulic.headloss == "H-W", "opciones")
    return e, wn


def ecuaciones(r, wn):
    """Errores maximos de la solucion (r = motor.Resultado) en todos los pasos de calculo."""
    juncs = [n for n, t in r.node_type.items() if t == "Junction"]
    inc = {n: [(l, 1 if r.link_nodes[l][1] == n else -1) for l in r.links if n in r.link_nodes[l]] for n in juncs}
    tubos = [l for l in r.links if r.link_type[l] in ("Pipe", "CVPipe")]
    peor = dict(continuidad=0.0, hw=0.0, bomba=0.0, prv=0.0)
    fallas = []
    for t in r.times:
        H, Q, S, D = r.head.loc[t], r.flow.loc[t], r.status.loc[t], r.demand.loc[t]
        for n in juncs:
            s = sum(sg * Q[l] for l, sg in inc[n])
            peor["continuidad"] = max(peor["continuidad"], abs(s - D[n]))
        for p in tubos:
            a, b = r.link_nodes[p]
            if S[p] == 0:
                if abs(Q[p]) > 1e-4:
                    fallas.append(f"t={t} {p} cerrada con caudal")
                continue
            lk = wn.get_link(p)
            hf = K_HW * lk.length * (abs(Q[p]) / 1000) ** 1.852 / (lk.roughness ** 1.852 * lk.diameter ** 4.871)
            peor["hw"] = max(peor["hw"], abs(math.copysign(hf, Q[p]) - (H[a] - H[b])))
        a, b = r.link_nodes["PMP-1"]
        if S["PMP-1"] > 0:
            peor["bomba"] = max(peor["bomba"], abs((_A - _B * Q["PMP-1"] ** _C) - (H[b] - H[a])))
        for v in PRV:
            a, b = r.link_nodes[v]
            hset = r.elev[b] + r.setting.loc[t, v]
            hu, hd, q = H[a], H[b], Q[v]
            if S[v] == 0:                                  # cerrada
                ok = abs(q) < 1e-4 and (hd >= hset - 0.01 or hu <= hd)
            elif abs(hd - hset) < 0.01:                    # activa
                ok = hu >= hd - 1e-4 and q >= -1e-4
                peor["prv"] = max(peor["prv"], abs(hd - hset))
            else:                                          # abierta
                ok = hu <= hset + 0.01 and q >= -1e-4
            if not ok:
                fallas.append(f"t={t} {v} estado incoherente")
    return peor, fallas


def tanque(r, area):
    """Balance de volumen del tanque: integracion de Euler paso a paso y volumen total."""
    t = np.array(r.times, dtype=float)
    H = r.head["T-1"].values
    q = r.flow["P-16"].values / 1000                      # P-16 va de J-7 a T-1: q > 0 entra
    euler = max(abs(H[k] + q[k] * (t[k + 1] - t[k]) / area - H[k + 1]) for k in range(len(t) - 1))
    v_int = float(np.sum(q[:-1] * np.diff(t)))
    v_niv = float((H[-1] - H[0]) * area)
    return dict(euler=euler, v_int=v_int, v_niv=v_niv)

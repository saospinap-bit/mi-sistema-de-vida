# -*- coding: utf-8 -*-
"""
================================================================================
MODELO TECNICO-FINANCIERO - PROYECTO PEPI
Optimizacion y ampliacion del sistema de acueducto del municipio de TADO (Choco)
================================================================================
Caso REAL. Cifras monetarias en millones de pesos colombianos (COP MM)
salvo indicacion contraria.

El script calcula, en este orden:
  A. DISENO DE CAUDAL segun Resolucion 0330 de 2017 (RAS): poblacion de diseno,
     dotacion neta/bruta, caudales medio diario (Qmd), maximo diario (QMD) y
     maximo horario (QMH), y la capacidad de la PTAP.
  B. PRESUPUESTO / CAPEX por capitulos (anclado a la inversion real del
     proyecto MinVivienda + cooperacion espaniola: COP 19.971 MM).
  C. ESTRUCTURA DE FINANCIACION (aporte publico + deuda + equity) y WACC.
  D. FLUJOS DE CAJA y tres evaluaciones:
        1) Financiera del PROYECTO (a costo total)         -> VPN, TIR
        2) Del INVERSIONISTA privado (con aporte publico)  -> VPN, TIR
        3) SOCIOECONOMICA (tasa social DNP 9%)             -> VPN economico, B/C
  E. ANALISIS DE SENSIBILIDAD del aporte publico.
  F. Exporta 'resultados_modelo.csv'.

FUENTES de los parametros reales: ver seccion "FUENTES" del INFORME_PEPI.md.
================================================================================
"""
import csv

# ======================================================================
# A. DISENO DE CAUDAL  (Resolucion 0330 de 2017 - RAS)
# ======================================================================
# --- Poblacion (DANE) ---
POB_MUNICIPIO_2018 = 17000     # CNPV 2018 (DANE), poblacion total del municipio
FRAC_URBANA = 0.60             # fraccion en cabecera urbana (estimacion)
POB_URBANA_2018 = POB_MUNICIPIO_2018 * FRAC_URBANA
ANIO_BASE = 2024
TASA_CREC_POB = 0.012          # crecimiento geometrico anual (~1,2%) - Choco bajo
PERIODO_DISENO = 25            # anios (horizonte de diseno y de evaluacion)

# Poblacion en el anio base y al final del periodo de diseno (metodo geometrico)
POB_URBANA_BASE = POB_URBANA_2018 * (1 + TASA_CREC_POB) ** (ANIO_BASE - 2018)
POB_DISENO = POB_URBANA_BASE * (1 + TASA_CREC_POB) ** PERIODO_DISENO

# --- Dotacion (Res 0330/2017, clima calido < 1000 m s.n.m.) ---
DOTACION_NETA = 140.0          # L/hab.dia  (Art. 43, altitud < 1000 m)
PERDIDAS = 0.25                # 25% perdidas tecnicas maximas admisibles (Art. 44)
DOTACION_BRUTA = DOTACION_NETA / (1 - PERDIDAS)   # L/hab.dia

# --- Coeficientes de consumo (Res 0330/2017, Art. 47) ---
K1 = 1.30                      # coef. consumo maximo diario
K2 = 1.60                      # coef. consumo maximo horario (red menor de distribucion)

# --- Caudales (L/s) ---
Qmd = POB_DISENO * DOTACION_BRUTA / 86400.0   # caudal medio diario
QMD = Qmd * K1                                # caudal maximo diario
QMH = QMD * K2                                # caudal maximo horario
CAP_PTAP = 45.0                # capacidad nominal seleccionada de la PTAP (L/s)

# ======================================================================
# B. PRESUPUESTO / CAPEX  (COP MM)  -> anclado a inversion real 19.971 MM
# ======================================================================
capex_detalle = {
    "Captacion (bocatoma) y linea de aduccion": 2400.0,
    "PTAP 45 L/s (obra civil + equipos)": 6300.0,
    "Almacenamiento (tanques) y estaciones de bombeo": 2800.0,
    "Redes de distribucion, conexiones y micromedicion": 4200.0,
    "Optimizacion del alcantarillado (componente asociado)": 2471.0,
    "Estudios, disenios, interventoria y gestion ambiental": 1800.0,
}
CAPEX = sum(capex_detalle.values())            # = 19.971 MM (cifra real)

# ======================================================================
# C. FINANCIACION Y WACC
# ======================================================================
HORIZONTE = PERIODO_DISENO     # 25 anios de operacion
TASA_IMPUESTOS = 0.35          # impuesto de renta Colombia
TASA_SOCIAL = 0.09             # tasa social de descuento (DNP)

# Estructura de financiacion (tipica de acueductos municipales: gran aporte publico)
PCT_PUBLICO = 0.80             # aporte no reembolsable (SGR / PDA / MinVivienda / cooperacion)
PCT_DEUDA = 0.10               # credito de banca de desarrollo (FINDETER)
PCT_EQUITY = 0.10              # aporte del operador / municipio

APORTE_PUBLICO = CAPEX * PCT_PUBLICO
DEUDA = CAPEX * PCT_DEUDA
EQUITY = CAPEX * PCT_EQUITY

KD = 0.11                      # costo de la deuda (banca de desarrollo)
KE = 0.14                      # costo del equity (operador)
PLAZO_DEUDA = 10               # anios

# WACC: el costo de oportunidad del aporte publico se toma como la tasa social
WACC = (PCT_PUBLICO * TASA_SOCIAL
        + PCT_EQUITY * KE
        + PCT_DEUDA * KD * (1 - TASA_IMPUESTOS))

# Depreciacion lineal del CAPEX a 25 anios
DEP_ANUAL = CAPEX / HORIZONTE

# Tabla de amortizacion de la deuda (sistema frances)
def cuota_fija(principal, tasa, n):
    return principal * tasa / (1 - (1 + tasa) ** (-n))

CUOTA = cuota_fija(DEUDA, KD, PLAZO_DEUDA)
saldo = DEUDA
intereses, amortizacion, servicio, saldos = [], [], [], []
for t in range(1, HORIZONTE + 1):
    if t <= PLAZO_DEUDA:
        interes_t = saldo * KD
        amort_t = CUOTA - interes_t
        saldo -= amort_t
    else:
        interes_t = amort_t = 0.0
    intereses.append(interes_t)
    amortizacion.append(amort_t)
    servicio.append(interes_t + amort_t)
    saldos.append(max(saldo, 0.0))

# ======================================================================
# D. PROYECCION OPERATIVA (Ingresos y OPEX)  - tarifa regulada CRA
# ======================================================================
# Ingresos por tarifa de acueducto (cargo fijo + consumo). Poblacion mayoritaria
# estrato 1-2 con subsidios; el recaudo cubre OPEX y deja un margen pequenio.
INGRESO_ANIO1 = 1500.0         # COP MM (~2.700 suscriptores estrato 1-2 subsidiados)
CREC_INGRESO = 0.035           # 3,5% anual (cobertura + IPC real moderado)
OPEX_ANIO1 = 1150.0            # COP MM (energia bombeo, quimicos, personal, mant.)
CREC_OPEX = 0.035              # 3,5% anual

ingresos = [INGRESO_ANIO1 * (1 + CREC_INGRESO) ** (t - 1) for t in range(1, HORIZONTE + 1)]
opex = [OPEX_ANIO1 * (1 + CREC_OPEX) ** (t - 1) for t in range(1, HORIZONTE + 1)]

# ======================================================================
# Estado de resultados y flujos
# ======================================================================
ebitda, ebit = [], []
fclp = []        # Flujo de Caja Libre del Proyecto (a costo total)
fcla = []        # Flujo de Caja del Inversionista (con aporte publico)
util_neta = []
for t in range(HORIZONTE):
    e = ingresos[t] - opex[t]
    ebitda.append(e)
    ebit_t = e - DEP_ANUAL
    ebit.append(ebit_t)

    # --- Flujo del PROYECTO (sin financiacion, a costo total) ---
    fclp_t = ebit_t * (1 - TASA_IMPUESTOS) + DEP_ANUAL if ebit_t > 0 else e
    # si EBIT<=0 no hay impuesto; el flujo operativo es el EBITDA (Dep es no-caja)
    fclp.append(fclp_t)

    # --- Flujo del INVERSIONISTA (solo arriesga deuda+equity; resto es aporte) ---
    uai = ebit_t - intereses[t]
    imp_inv = max(uai, 0) * TASA_IMPUESTOS
    un = uai - imp_inv
    util_neta.append(un)
    fcla_t = un + DEP_ANUAL - amortizacion[t]
    fcla.append(fcla_t)

flujo_proyecto = [-CAPEX] + fclp
flujo_inversionista = [-EQUITY] + fcla
flujo_banco = [DEUDA] + [-(servicio[t]) for t in range(HORIZONTE)]

# ======================================================================
# E. EVALUACION SOCIOECONOMICA (precios economicos, tasa social 9%)
# ======================================================================
# Beneficios sociales anuales (COP MM), ano 1, crecen con la cobertura:
#  - Ahorro en compra de agua alterna (carrotanques / agua embotellada / hervir)
#  - Reduccion de costos en salud por enfermedad diarreica aguda (EDA) evitada
#  - Valor del tiempo liberado por acarreo de agua
BEN_AGUA_ALTERNA = 2800.0      # COP MM/anio (agua embotellada/hervida que hoy compran)
BEN_SALUD = 900.0              # COP MM/anio (EDA evitada: atencion + productividad)
BEN_TIEMPO = 450.0             # COP MM/anio (tiempo liberado de acarreo)
BENEFICIO_SOCIAL_1 = BEN_AGUA_ALTERNA + BEN_SALUD + BEN_TIEMPO
CREC_BENEFICIO = 0.035

# Costos economicos = OPEX (sin impuestos, que son transferencias)
beneficios_soc = [BENEFICIO_SOCIAL_1 * (1 + CREC_BENEFICIO) ** (t - 1) for t in range(1, HORIZONTE + 1)]
flujo_social = [-CAPEX] + [beneficios_soc[t] - opex[t] for t in range(HORIZONTE)]

# ======================================================================
# Funciones VPN / TIR
# ======================================================================
def vpn(tasa, flujos):
    return sum(f / (1 + tasa) ** i for i, f in enumerate(flujos))

def tir(flujos):
    lo, hi = -0.9, 5.0
    f_lo = vpn(lo, flujos)
    if f_lo * vpn(hi, flujos) > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = vpn(mid, flujos)
        if abs(f_mid) < 1e-7:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo = mid
            f_lo = f_mid
    return (lo + hi) / 2

VPN_PROYECTO = vpn(WACC, flujo_proyecto)
TIR_PROYECTO = tir(flujo_proyecto)
VPN_INVERSIONISTA = vpn(KE, flujo_inversionista)
TIR_INVERSIONISTA = tir(flujo_inversionista)

# VPN social y relacion Beneficio/Costo (a tasa social)
VPN_BENEFICIOS = sum(beneficios_soc[t] / (1 + TASA_SOCIAL) ** (t + 1) for t in range(HORIZONTE))
VPN_COSTOS = CAPEX + sum(opex[t] / (1 + TASA_SOCIAL) ** (t + 1) for t in range(HORIZONTE))
VPN_SOCIAL = vpn(TASA_SOCIAL, flujo_social)
RBC = VPN_BENEFICIOS / VPN_COSTOS

# ======================================================================
# E2. SENSIBILIDAD: TIR del inversionista segun % de aporte publico
# ======================================================================
def tir_inv_segun_aporte(pct_publico):
    pct_priv = 1 - pct_publico
    deuda = CAPEX * pct_priv * 0.5
    equity = CAPEX * pct_priv * 0.5
    cuota = cuota_fija(deuda, KD, PLAZO_DEUDA)
    s = deuda
    inter, amort = [], []
    for t in range(1, HORIZONTE + 1):
        if t <= PLAZO_DEUDA:
            it = s * KD
            at = cuota - it
            s -= at
        else:
            it = at = 0.0
        inter.append(it)
        amort.append(at)
    fcla_s = []
    for t in range(HORIZONTE):
        uai = ebit[t] - inter[t]
        un = uai - max(uai, 0) * TASA_IMPUESTOS
        fcla_s.append(un + DEP_ANUAL - amort[t])
    return tir([-equity] + fcla_s)

sensibilidad = [(p, tir_inv_segun_aporte(p)) for p in (0.0, 0.40, 0.60, 0.70, 0.80, 0.90)]

# ======================================================================
# SALIDA EN CONSOLA
# ======================================================================
def pct(x): return "n/d" if x is None else f"{x:.2%}"

print("=" * 74)
print("PROYECTO PEPI - ACUEDUCTO DE TADO (CHOCO)   |   cifras en COP millones")
print("=" * 74)
print("\n[A] DISENO DE CAUDAL (Res. 0330/2017 - RAS)")
print(f"  Poblacion municipio (CNPV 2018, DANE)..: {POB_MUNICIPIO_2018:,.0f} hab")
print(f"  Poblacion urbana base ({ANIO_BASE}).........: {POB_URBANA_BASE:,.0f} hab")
print(f"  Poblacion de diseno (+{PERIODO_DISENO} anios)......: {POB_DISENO:,.0f} hab")
print(f"  Dotacion neta..........................: {DOTACION_NETA:.0f} L/hab.dia")
print(f"  Dotacion bruta (perdidas {PERDIDAS:.0%})........: {DOTACION_BRUTA:.1f} L/hab.dia")
print(f"  Caudal medio diario  Qmd...............: {Qmd:.2f} L/s")
print(f"  Caudal maximo diario QMD (k1={K1})......: {QMD:.2f} L/s")
print(f"  Caudal maximo horario QMH (k2={K2}).....: {QMH:.2f} L/s")
print(f"  Capacidad PTAP seleccionada............: {CAP_PTAP:.0f} L/s")

print("\n[B] CAPEX POR CAPITULOS")
for k, v in capex_detalle.items():
    print(f"  {k:.<55}: {v:>8,.0f}")
print(f"  {'TOTAL CAPEX':.<55}: {CAPEX:>8,.0f}")

print("\n[C] FINANCIACION Y WACC")
print(f"  Aporte publico (80%)...: {APORTE_PUBLICO:>9,.1f}")
print(f"  Deuda (10%)............: {DEUDA:>9,.1f}  (Kd={KD:.1%}, {PLAZO_DEUDA} anios)")
print(f"  Equity (10%)...........: {EQUITY:>9,.1f}  (Ke={KE:.1%})")
print(f"  WACC...................: {WACC:.4f}  ({WACC:.2%})")

print("\n[D] EVALUACIONES")
print(f"  1) FINANCIERA PROYECTO  VPN(@WACC)={VPN_PROYECTO:>10,.0f}   TIR={pct(TIR_PROYECTO)}")
print(f"  2) INVERSIONISTA        VPN(@Ke)  ={VPN_INVERSIONISTA:>10,.0f}   TIR={pct(TIR_INVERSIONISTA)}")
print(f"  3) SOCIOECONOMICA       VPN(@9%)  ={VPN_SOCIAL:>10,.0f}   B/C={RBC:.2f}")

print("\n[E] SENSIBILIDAD - TIR inversionista segun aporte publico")
for p, ti in sensibilidad:
    print(f"     Aporte publico {p:>4.0%}  ->  TIR inversionista = {pct(ti)}")
print("=" * 74)

# ======================================================================
# F. EXPORTAR CSV
# ======================================================================
with open("resultados_modelo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["PROYECTO PEPI - ACUEDUCTO DE TADO (CHOCO) - cifras COP MM"])
    w.writerow([])
    w.writerow(["DISENO DE CAUDAL (Res 0330/2017)"])
    w.writerow(["Poblacion municipio CNPV 2018", POB_MUNICIPIO_2018])
    w.writerow(["Poblacion urbana base", round(POB_URBANA_BASE)])
    w.writerow(["Poblacion de diseno (+25 anios)", round(POB_DISENO)])
    w.writerow(["Dotacion neta (L/hab.dia)", DOTACION_NETA])
    w.writerow(["Dotacion bruta (L/hab.dia)", round(DOTACION_BRUTA, 1)])
    w.writerow(["Qmd (L/s)", round(Qmd, 2)])
    w.writerow(["QMD (L/s)", round(QMD, 2)])
    w.writerow(["QMH (L/s)", round(QMH, 2)])
    w.writerow(["Capacidad PTAP (L/s)", CAP_PTAP])
    w.writerow([])
    w.writerow(["CAPEX por capitulos (COP MM)"])
    for k, v in capex_detalle.items():
        w.writerow([k, v])
    w.writerow(["TOTAL CAPEX", CAPEX])
    w.writerow([])
    w.writerow(["FLUJOS DE CAJA (COP MM)"])
    w.writerow(["Anio", "Ingresos", "OPEX", "EBITDA", "Depreciacion", "Intereses",
                "Amortizacion", "Saldo_deuda", "FC_Proyecto", "FC_Inversionista",
                "FC_Banco", "Beneficio_social", "FC_Social"])
    w.writerow([0, "", "", "", "", "", "", round(DEUDA, 1), round(-CAPEX, 1),
                round(-EQUITY, 1), round(DEUDA, 1), "", round(-CAPEX, 1)])
    for t in range(HORIZONTE):
        w.writerow([t + 1, round(ingresos[t], 1), round(opex[t], 1), round(ebitda[t], 1),
                    round(DEP_ANUAL, 1), round(intereses[t], 1), round(amortizacion[t], 1),
                    round(saldos[t], 1), round(fclp[t], 1), round(fcla[t], 1),
                    round(-servicio[t], 1), round(beneficios_soc[t], 1),
                    round(beneficios_soc[t] - opex[t], 1)])
    w.writerow([])
    w.writerow(["INDICADORES"])
    w.writerow(["WACC", round(WACC, 4)])
    w.writerow(["VPN_Proyecto", round(VPN_PROYECTO, 1)])
    w.writerow(["TIR_Proyecto", None if TIR_PROYECTO is None else round(TIR_PROYECTO, 4)])
    w.writerow(["VPN_Inversionista", round(VPN_INVERSIONISTA, 1)])
    w.writerow(["TIR_Inversionista", None if TIR_INVERSIONISTA is None else round(TIR_INVERSIONISTA, 4)])
    w.writerow(["VPN_Social_@9%", round(VPN_SOCIAL, 1)])
    w.writerow(["Relacion_Beneficio_Costo", round(RBC, 3)])
    w.writerow([])
    w.writerow(["SENSIBILIDAD aporte publico -> TIR inversionista"])
    for p, ti in sensibilidad:
        w.writerow([f"{p:.0%}", None if ti is None else round(ti, 4)])

print("\nArchivo 'resultados_modelo.csv' generado.")

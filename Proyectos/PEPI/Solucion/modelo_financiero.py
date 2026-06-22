"""
============================================================================
MODELO TECNICO-FINANCIERO - PROYECTO PEPI
Optimizacion y ampliacion del sistema de acueducto del municipio de
TADO (Choco, Colombia)
============================================================================
Cifras monetarias en millones de pesos colombianos (COP MM) salvo indicacion.

El modelo:
  1. Calcula el CAUDAL DE DISENIO segun la Resolucion 0330 de 2017 (RAS).
  2. Arma el PRESUPUESTO DE OBRA (CAPEX) por capitulos.
  3. Define la ESTRUCTURA DE FINANCIACION (aporte publico + deuda + equity).
  4. Calcula WACC y los flujos del PROYECTO, INVERSIONISTA y BANCO.
  5. Calcula VPN/TIR (proyecto, inversionista) y la evaluacion SOCIOECONOMICA.

FUENTES (ver INFORME, Seccion 10):
  - Poblacion: DANE, CNPV 2018 y proyecciones (Tado: 20.476 hab total 2025;
    cabecera 11.917 hab).
  - Diseno: Resolucion 0330 de 2017 (RAS).
  - Marco tarifario / costo de capital: Resolucion CRA 943 de 2021.
  - Calidad del agua: Resolucion 2115 de 2007.
  - Tasa social de descuento: DNP (9%).
============================================================================
"""

# ---------------------------------------------------------------------------
# 0. DATOS DEL MUNICIPIO (FUENTE: DANE CNPV 2018 y proyecciones)
# ---------------------------------------------------------------------------
POB_TOTAL_2025 = 20476      # habitantes (proyeccion DANE 2025)
POB_URBANA_2025 = 11917     # habitantes cabecera municipal (DANE)
ALTITUD = 75                # m s.n.m. (define dotacion neta en Res 0330)

# ---------------------------------------------------------------------------
# 1. CAUDAL DE DISENIO  (Resolucion 0330 de 2017)
# ---------------------------------------------------------------------------
HORIZONTE = 25
TASA_CREC_POB = 0.008       # 0.8% anual (proyeccion urbana, metodo geometrico)
POB_DISENIO = POB_URBANA_2025 * (1 + TASA_CREC_POB) ** HORIZONTE

DOTACION_NETA = 140.0       # L/hab.dia (altitud < 1000 msnm, Res 0330 Art. 43)
PERDIDAS = 0.25             # perdidas tecnicas maximas admisibles (Res 0330)
DOTACION_BRUTA = DOTACION_NETA / (1 - PERDIDAS)
K1 = 1.30                   # coef. consumo maximo diario
K2 = 1.60                   # coef. consumo maximo horario

Q_MEDIO = DOTACION_BRUTA * POB_DISENIO / 86400.0
Q_MAX_DIARIO = Q_MEDIO * K1
Q_MAX_HORARIO = Q_MAX_DIARIO * K2
CAPACIDAD_PTAP = 45.0       # L/s adoptada (con holgura sobre QMD)

# ---------------------------------------------------------------------------
# 2. PRESUPUESTO DE OBRA - CAPEX (precios de referencia; validar con APU).
#    Nota: el Choco tiene sobrecostos por logistica, transporte y lluvias.
# ---------------------------------------------------------------------------
capex_capitulos = {
    "1. Preliminares y obras provisionales": 350.0,
    "2. Captacion (bocatoma rio San Juan) + desarenador": 950.0,
    "3. Aduccion y conduccion (tuberia PVC/HD ~4 km)": 1900.0,
    "4. PTAP compacta 45 L/s (obra civil + equipos + dosificacion + laboratorio)": 3800.0,
    "5. Tanque de almacenamiento (1.000 m3)": 1200.0,
    "6. Estacion de bombeo (bombas de alta eficiencia + variadores)": 750.0,
    "7. Redes de distribucion y sectorizacion": 2700.0,
    "8. Micromedicion (~3.700 medidores) + macromedicion": 720.0,
    "9. Estudios, disenios e interventoria": 1100.0,
}
CAPEX = sum(capex_capitulos.values())

# ---------------------------------------------------------------------------
# 3. ESTRUCTURA DE FINANCIACION
#    Choco es uno de los departamentos con mayor NBI: el CAPEX se cofinancia
#    casi en su totalidad con recursos publicos (SGR/PDA/SGP/cooperacion).
# ---------------------------------------------------------------------------
PCT_APORTE_PUBLICO = 0.90
PCT_DEUDA = 0.05
PCT_EQUITY = 0.05
APORTE_PUBLICO = CAPEX * PCT_APORTE_PUBLICO
DEUDA = CAPEX * PCT_DEUDA
EQUITY = CAPEX * PCT_EQUITY
CAPITAL_REMUNERADO = DEUDA + EQUITY

KD = 0.11
KE = 0.14
TASA_IMPUESTOS = 0.35
PLAZO_DEUDA = 12
w_d = DEUDA / CAPITAL_REMUNERADO
w_e = EQUITY / CAPITAL_REMUNERADO
WACC = w_e * KE + w_d * KD * (1 - TASA_IMPUESTOS)

# ---------------------------------------------------------------------------
# 4. PROYECCION OPERATIVA
# ---------------------------------------------------------------------------
SUSCRIPTORES_1 = 3400
CREC_SUSCRIPTORES = 0.012
FACTURA_MES_1 = 28000.0     # COP/mes por suscriptor (estratos bajos, subsidiados)
CREC_TARIFA = 0.035
OPEX_1 = 1050.0             # COP MM ano 1 (energia, quimicos, personal, mtto, admin)
CREC_OPEX = 0.04
DEP_ANUAL = CAPEX / HORIZONTE

ingresos, opex = [], []
for t in range(1, HORIZONTE + 1):
    susc = SUSCRIPTORES_1 * (1 + CREC_SUSCRIPTORES) ** (t - 1)
    fact = FACTURA_MES_1 * (1 + CREC_TARIFA) ** (t - 1)
    ingresos.append(susc * fact * 12 / 1e6)
    opex.append(OPEX_1 * (1 + CREC_OPEX) ** (t - 1))

# ---------------------------------------------------------------------------
# 5. AMORTIZACION DE LA DEUDA (sistema frances)
# ---------------------------------------------------------------------------
def cuota_fija(p, i, n):
    return p * i / (1 - (1 + i) ** (-n))

CUOTA = cuota_fija(DEUDA, KD, PLAZO_DEUDA)
saldo = DEUDA
intereses, amortizacion = [], []
for t in range(1, HORIZONTE + 1):
    if t <= PLAZO_DEUDA:
        it = saldo * KD; at = CUOTA - it; saldo -= at
    else:
        it = at = 0.0
    intereses.append(it); amortizacion.append(at)

# ---------------------------------------------------------------------------
# 6. FLUJOS DE CAJA
# ---------------------------------------------------------------------------
ebitda, ebit, fclp, fcla = [], [], [], []
for t in range(HORIZONTE):
    e = ingresos[t] - opex[t]; ebitda.append(e)
    eb = e - DEP_ANUAL; ebit.append(eb)
    fclp.append(eb * (1 - TASA_IMPUESTOS) + DEP_ANUAL)
    uai = eb - intereses[t]
    fcla.append(uai * (1 - TASA_IMPUESTOS) + DEP_ANUAL - amortizacion[t])

flujo_proyecto = [-CAPEX] + fclp
flujo_inversionista = [-EQUITY] + fcla
servicio = [intereses[t] + amortizacion[t] for t in range(HORIZONTE)]
flujo_banco = [DEUDA] + [-s for s in servicio]

# ---------------------------------------------------------------------------
# 7. VPN y TIR
# ---------------------------------------------------------------------------
def vpn(tasa, flujos):
    return sum(f / (1 + tasa) ** i for i, f in enumerate(flujos))

def tir(flujos):
    lo, hi = -0.95, 5.0
    flo = vpn(lo, flujos); fhi = vpn(hi, flujos)
    if flo * fhi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2; fm = vpn(mid, flujos)
        if abs(fm) < 1e-7:
            return mid
        if flo * fm < 0:
            hi = mid
        else:
            lo = mid; flo = fm
    return (lo + hi) / 2

VPN_PROY = vpn(WACC, flujo_proyecto); TIR_PROY = tir(flujo_proyecto)
VPN_INV = vpn(KE, flujo_inversionista); TIR_INV = tir(flujo_inversionista)

# ---------------------------------------------------------------------------
# 8. SALIDA
# ---------------------------------------------------------------------------
print("=" * 74)
print(" PROYECTO PEPI - ACUEDUCTO DE TADO (CHOCO)")
print("=" * 74)
print("\n--- 1. CAUDAL DE DISENIO (Resolucion 0330 de 2017) ---")
print(f"Poblacion urbana 2025 (DANE)........: {POB_URBANA_2025:,.0f} hab")
print(f"Poblacion de diseno (anio {HORIZONTE})......: {POB_DISENIO:,.0f} hab")
print(f"Dotacion neta (altitud {ALTITUD} m)......: {DOTACION_NETA:.0f} L/hab.dia")
print(f"Dotacion bruta (perdidas {PERDIDAS:.0%})......: {DOTACION_BRUTA:.1f} L/hab.dia")
print(f"Caudal medio diario (Qmd)...........: {Q_MEDIO:.1f} L/s")
print(f"Caudal max diario (QMD=Qmd*{K1})......: {Q_MAX_DIARIO:.1f} L/s  -> diseno PTAP")
print(f"Caudal max horario (QMH=QMD*{K2}).....: {Q_MAX_HORARIO:.1f} L/s  -> diseno redes")
print(f"Capacidad PTAP adoptada.............: {CAPACIDAD_PTAP:.0f} L/s")

print("\n--- 2. PRESUPUESTO DE OBRA (CAPEX) ---")
for k, v in capex_capitulos.items():
    print(f"  {k:<64} {v:>8,.0f}")
print(f"  {'TOTAL CAPEX':<64} {CAPEX:>8,.0f}  COP MM")

print("\n--- 3. ESTRUCTURA DE FINANCIACION ---")
print(f"Aporte publico no reembolsable (90%): {APORTE_PUBLICO:>8,.0f}")
print(f"Deuda (5%)..........................: {DEUDA:>8,.0f}  (Kd={KD:.0%})")
print(f"Equity (5%).........................: {EQUITY:>8,.0f}  (Ke={KE:.0%})")
print(f"WACC (capital remunerado)...........: {WACC:.4f}  ({WACC:.2%})")

print("\n--- 4. INDICADORES ---")
print(f"VPN PROYECTO 'puro' (@WACC).........: {VPN_PROY:>10,.0f}  COP MM")
print(f"TIR PROYECTO 'puro'.................: {('NA' if TIR_PROY is None else format(TIR_PROY,'.2%'))}")
print(f"VPN INVERSIONISTA (@Ke).............: {VPN_INV:>10,.0f}  COP MM")
print(f"TIR INVERSIONISTA...................: {('NA' if TIR_INV is None else format(TIR_INV,'.2%'))}")

print("\n--- FLUJOS ANUALES (COP MM) ---")
print(f"{'Anio':>4}{'Ingresos':>10}{'OPEX':>9}{'EBITDA':>9}{'Interes':>9}{'Amort':>9}{'FC Proy':>10}{'FC Inv':>10}")
for t in range(HORIZONTE):
    print(f"{t+1:>4}{ingresos[t]:>10,.0f}{opex[t]:>9,.0f}{ebitda[t]:>9,.0f}"
          f"{intereses[t]:>9,.0f}{amortizacion[t]:>9,.0f}{fclp[t]:>10,.0f}{fcla[t]:>10,.0f}")

import csv
with open("resultados_modelo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["DISENO (Res 0330/2017) - TADO (CHOCO)", ""])
    w.writerow(["Poblacion urbana 2025 (DANE)", POB_URBANA_2025])
    w.writerow(["Poblacion de diseno (anio 25)", round(POB_DISENIO)])
    w.writerow(["Q max diario L/s (PTAP)", round(Q_MAX_DIARIO, 1)])
    w.writerow(["Q max horario L/s", round(Q_MAX_HORARIO, 1)])
    w.writerow(["Capacidad PTAP L/s", CAPACIDAD_PTAP])
    w.writerow([])
    w.writerow(["CAPEX (COP MM)", round(CAPEX)])
    w.writerow(["Aporte publico", round(APORTE_PUBLICO)])
    w.writerow(["Deuda", round(DEUDA)]); w.writerow(["Equity", round(EQUITY)])
    w.writerow(["WACC", round(WACC, 4)])
    w.writerow(["VPN Proyecto", round(VPN_PROY)])
    w.writerow(["TIR Proyecto", "NA" if TIR_PROY is None else round(TIR_PROY, 4)])
    w.writerow(["VPN Inversionista", round(VPN_INV)])
    w.writerow(["TIR Inversionista", "NA" if TIR_INV is None else round(TIR_INV, 4)])
    w.writerow([])
    w.writerow(["Anio", "Ingresos", "OPEX", "EBITDA", "Deprec", "Intereses",
                "Amortizacion", "FC_Proyecto", "FC_Inversionista", "FC_Banco"])
    w.writerow([0, "", "", "", "", "", "", round(-CAPEX), round(-EQUITY), round(DEUDA)])
    for t in range(HORIZONTE):
        w.writerow([t + 1, round(ingresos[t], 1), round(opex[t], 1), round(ebitda[t], 1),
                    round(DEP_ANUAL, 1), round(intereses[t], 1), round(amortizacion[t], 1),
                    round(fclp[t], 1), round(fcla[t], 1), round(-servicio[t], 1)])

# ---------------------------------------------------------------------------
# 9. SENSIBILIDAD: aporte publico vs viabilidad del inversionista
# ---------------------------------------------------------------------------
print("\n--- 9. SENSIBILIDAD: aporte publico vs TIR del inversionista ---")
print(f"{'Aporte publico':>15}{'Equity (MM)':>14}{'TIR Inv':>10}{'VPN Inv (MM)':>14}")
for g in [0.70, 0.80, 0.85, 0.90, 0.95]:
    pe = (1 - g) / 2; eq = CAPEX * pe; de = CAPEX * pe
    cuota_s = cuota_fija(de, KD, PLAZO_DEUDA); saldo_s = de
    inte_s, amor_s = [], []
    for t in range(1, HORIZONTE + 1):
        if t <= PLAZO_DEUDA:
            i_ = saldo_s * KD; a_ = cuota_s - i_; saldo_s -= a_
        else:
            i_ = a_ = 0.0
        inte_s.append(i_); amor_s.append(a_)
    fcla_s = []
    for t in range(HORIZONTE):
        uai = ebit[t] - inte_s[t]
        fcla_s.append(uai * (1 - TASA_IMPUESTOS) + DEP_ANUAL - amor_s[t])
    flujo_s = [-eq] + fcla_s
    t_inv = tir(flujo_s); v_inv = vpn(KE, flujo_s)
    print(f"{g:>14.0%}{eq:>14,.0f}{('NA' if t_inv is None else format(t_inv,'.2%')):>10}{v_inv:>14,.0f}")

# ---------------------------------------------------------------------------
# 10. EVALUACION SOCIOECONOMICA (tasa social DNP = 9%)
# ---------------------------------------------------------------------------
TASA_SOCIAL = 0.09
HOGARES_1 = 3400
BENEFICIO_HOGAR_MES = 75000.0
beneficios = [HOGARES_1 * (1 + CREC_SUSCRIPTORES) ** t * BENEFICIO_HOGAR_MES * 12 / 1e6
              for t in range(HORIZONTE)]
flujo_economico = [-CAPEX] + [beneficios[t] - opex[t] for t in range(HORIZONTE)]
VPN_ECON = vpn(TASA_SOCIAL, flujo_economico); TIR_ECON = tir(flujo_economico)
RBC = (sum(beneficios[t] / (1 + TASA_SOCIAL) ** (t + 1) for t in range(HORIZONTE)) /
       (CAPEX + sum(opex[t] / (1 + TASA_SOCIAL) ** (t + 1) for t in range(HORIZONTE))))
print("\n--- 10. EVALUACION SOCIOECONOMICA (tasa social DNP = 9%) ---")
print(f"Beneficio por hogar.................: {BENEFICIO_HOGAR_MES:,.0f} COP/mes")
print(f"VPN ECONOMICO (@9%).................: {VPN_ECON:>10,.0f}  COP MM")
print(f"TIR ECONOMICA (TIRE)................: {('NA' if TIR_ECON is None else format(TIR_ECON,'.2%'))}")
print(f"Relacion Beneficio/Costo (B/C)......: {RBC:.2f}")
print("\nCONCLUSION: el proyecto NO es financieramente rentable por si solo")
print("(tipico de acueductos municipales pequenos), pero es SOCIALMENTE viable")
print("y se justifica con cofinanciacion publica (SGR/PDA/SGP/cooperacion).")
print("\nArchivo 'resultados_modelo.csv' generado.")

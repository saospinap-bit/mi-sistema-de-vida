"""
Modelo financiero - Proyecto PEPI
Construccion de PTAP y ampliacion del sistema de acueducto - Municipio de El Progreso
Todas las cifras en millones de pesos colombianos (COP MM) salvo indicacion contraria.

Genera:
  - WACC
  - Flujo de Caja del Proyecto (FCLP)  -> VPN y TIR del proyecto
  - Flujo de Caja del Inversionista (FCLA / equity)  -> VPN y TIR del inversionista
  - Flujo de Caja del Banco (deuda)
  - Archivo resultados_modelo.csv y resumen impreso en consola
"""

import numpy as np
import csv

# ----------------------------------------------------------------------
# 1. PARAMETROS GENERALES
# ----------------------------------------------------------------------
HORIZONTE = 20            # anios de operacion
ANIO_CONSTRUCCION = 0     # CAPEX se desembolsa en el anio 0
TASA_IMPUESTOS = 0.35     # impuesto de renta Colombia (proxy)

# ----------------------------------------------------------------------
# 2. INVERSION (CAPEX)
# ----------------------------------------------------------------------
CAPEX = 14000.0           # COP MM (PTAP + redes + bombeo + tanques + interventoria)
# Distribucion del CAPEX (solo informativa)
capex_detalle = {
    "PTAP (obra civil + equipos)": 6300.0,
    "Ampliacion red de aduccion y conduccion": 2800.0,
    "Estaciones de bombeo y tanques de almacenamiento": 2100.0,
    "Redes de distribucion y micromedicion": 1900.0,
    "Estudios, disenios e interventoria": 900.0,
}
assert abs(sum(capex_detalle.values()) - CAPEX) < 1e-6

# Depreciacion lineal de la inversion depreciable a 20 anios
DEP_ANUAL = CAPEX / HORIZONTE

# ----------------------------------------------------------------------
# 3. ESTRUCTURA DE FINANCIACION (Deuda + Equity)
# ----------------------------------------------------------------------
PCT_DEUDA = 0.60
PCT_EQUITY = 0.40
DEUDA = CAPEX * PCT_DEUDA       # 8400
EQUITY = CAPEX * PCT_EQUITY     # 5600

KD = 0.125          # costo de la deuda (antes de impuestos)
PLAZO_DEUDA = 10    # anios
KE = 0.155          # costo del equity (CAPM del inversionista)

# Cuota fija (sistema frances) para la deuda
def cuota_fija(principal, tasa, n):
    return principal * tasa / (1 - (1 + tasa) ** (-n))

CUOTA = cuota_fija(DEUDA, KD, PLAZO_DEUDA)

# Tabla de amortizacion de la deuda
saldo = DEUDA
amortizacion = []   # principal pagado cada anio
intereses = []      # interes pagado cada anio
servicio = []       # cuota total
saldos = []
for t in range(1, HORIZONTE + 1):
    if t <= PLAZO_DEUDA:
        interes_t = saldo * KD
        amort_t = CUOTA - interes_t
        saldo = saldo - amort_t
    else:
        interes_t = 0.0
        amort_t = 0.0
    intereses.append(interes_t)
    amortizacion.append(amort_t)
    servicio.append(interes_t + amort_t)
    saldos.append(max(saldo, 0.0))

# ----------------------------------------------------------------------
# 4. WACC
# ----------------------------------------------------------------------
WACC = PCT_EQUITY * KE + PCT_DEUDA * KD * (1 - TASA_IMPUESTOS)

# ----------------------------------------------------------------------
# 5. PROYECCION OPERATIVA (Ingresos y OPEX)
# ----------------------------------------------------------------------
# Ingresos: tarifa de acueducto. Crecen por aumento de cobertura/poblacion.
INGRESO_ANIO1 = 5200.0     # COP MM
CREC_INGRESO = 0.045       # 4.5% anual (poblacion + recuperacion de cartera)

# OPEX: energia (bombeo), quimicos, personal, mantenimiento.
OPEX_ANIO1 = 2350.0        # COP MM
CREC_OPEX = 0.04           # 4% anual

ingresos = [INGRESO_ANIO1 * (1 + CREC_INGRESO) ** (t - 1) for t in range(1, HORIZONTE + 1)]
opex = [OPEX_ANIO1 * (1 + CREC_OPEX) ** (t - 1) for t in range(1, HORIZONTE + 1)]

# ----------------------------------------------------------------------
# 6. ESTADO DE RESULTADOS Y FLUJOS
# ----------------------------------------------------------------------
ebitda = []
ebit = []
impuestos_proy = []   # impuestos del flujo de proyecto (sin escudo de deuda)
fclp = []             # Flujo de Caja Libre del Proyecto
util_neta = []
impuestos_inv = []    # impuestos del inversionista (con escudo fiscal de intereses)
fcla = []             # Flujo de Caja Libre del Accionista / inversionista

for t in range(HORIZONTE):
    e = ingresos[t] - opex[t]
    ebitda.append(e)
    ebit_t = e - DEP_ANUAL
    ebit.append(ebit_t)

    # --- Flujo del PROYECTO (sin deuda) ---
    imp_proy = max(ebit_t, 0) * TASA_IMPUESTOS
    impuestos_proy.append(imp_proy)
    # FCLP = EBIT*(1-t) + Depreciacion  (sin variacion de capital de trabajo)
    fclp_t = ebit_t * (1 - TASA_IMPUESTOS) + DEP_ANUAL
    fclp.append(fclp_t)

    # --- Flujo del INVERSIONISTA (con deuda) ---
    uai = ebit_t - intereses[t]          # utilidad antes de impuestos
    imp_inv = max(uai, 0) * TASA_IMPUESTOS
    impuestos_inv.append(imp_inv)
    un = uai - imp_inv
    util_neta.append(un)
    # FCLA = Utilidad neta + Depreciacion - Amortizacion de deuda
    fcla_t = un + DEP_ANUAL - amortizacion[t]
    fcla.append(fcla_t)

# Vectores con el anio 0 (desembolsos)
flujo_proyecto = [-CAPEX] + fclp
flujo_inversionista = [-EQUITY] + fcla
flujo_banco = [DEUDA] + [-(servicio[t]) for t in range(HORIZONTE)]  # desde la optica del banco: presta y recibe

# ----------------------------------------------------------------------
# 7. INDICADORES: VPN y TIR
# ----------------------------------------------------------------------
def vpn(tasa, flujos):
    return sum(f / (1 + tasa) ** i for i, f in enumerate(flujos))

def tir(flujos):
    # metodo de biseccion robusto
    lo, hi = -0.9, 5.0
    f_lo = vpn(lo, flujos)
    f_hi = vpn(hi, flujos)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = vpn(mid, flujos)
        if abs(f_mid) < 1e-6:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return (lo + hi) / 2

VPN_PROYECTO = vpn(WACC, flujo_proyecto)
TIR_PROYECTO = tir(flujo_proyecto)
VPN_INVERSIONISTA = vpn(KE, flujo_inversionista)
TIR_INVERSIONISTA = tir(flujo_inversionista)

# ----------------------------------------------------------------------
# 8. SALIDA EN CONSOLA
# ----------------------------------------------------------------------
print("=" * 70)
print("MODELO FINANCIERO - PROYECTO PEPI (PTAP + ACUEDUCTO EL PROGRESO)")
print("Cifras en COP millones")
print("=" * 70)
print(f"CAPEX total................: {CAPEX:,.0f}")
print(f"Deuda (60%)................: {DEUDA:,.0f}")
print(f"Equity (40%)...............: {EQUITY:,.0f}")
print(f"Kd (costo deuda)...........: {KD:.2%}")
print(f"Ke (costo equity)..........: {KE:.2%}")
print(f"Tasa de impuestos..........: {TASA_IMPUESTOS:.0%}")
print(f"Cuota anual de la deuda....: {CUOTA:,.1f} (plazo {PLAZO_DEUDA} anios)")
print("-" * 70)
print(f"WACC.......................: {WACC:.4f}  ({WACC:.2%})")
print("-" * 70)
print(f"VPN del PROYECTO (@WACC)...: {VPN_PROYECTO:,.1f}")
print(f"TIR del PROYECTO...........: {TIR_PROYECTO:.2%}")
print(f"VPN INVERSIONISTA (@Ke)....: {VPN_INVERSIONISTA:,.1f}")
print(f"TIR del INVERSIONISTA......: {TIR_INVERSIONISTA:.2%}")
print("=" * 70)

# Tabla anual resumida
print("\nFLUJOS ANUALES (COP MM)")
hdr = f"{'Anio':>4} {'Ingresos':>10} {'OPEX':>9} {'EBITDA':>9} {'Interes':>9} {'Amort':>9} {'FC Proy':>10} {'FC Inv':>10}"
print(hdr)
for t in range(HORIZONTE):
    print(f"{t+1:>4} {ingresos[t]:>10,.0f} {opex[t]:>9,.0f} {ebitda[t]:>9,.0f} "
          f"{intereses[t]:>9,.0f} {amortizacion[t]:>9,.0f} {fclp[t]:>10,.0f} {fcla[t]:>10,.0f}")

# ----------------------------------------------------------------------
# 9. EXPORTAR A CSV
# ----------------------------------------------------------------------
with open("resultados_modelo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Anio", "Ingresos", "OPEX", "EBITDA", "Depreciacion", "Intereses",
                "Amortizacion", "Saldo_deuda", "FC_Proyecto", "FC_Inversionista", "FC_Banco"])
    w.writerow([0, "", "", "", "", "", "", DEUDA, -CAPEX, -EQUITY, DEUDA])
    for t in range(HORIZONTE):
        w.writerow([t + 1, round(ingresos[t], 1), round(opex[t], 1), round(ebitda[t], 1),
                    round(DEP_ANUAL, 1), round(intereses[t], 1), round(amortizacion[t], 1),
                    round(saldos[t], 1), round(fclp[t], 1), round(fcla[t], 1),
                    round(-servicio[t], 1)])
    w.writerow([])
    w.writerow(["WACC", round(WACC, 4)])
    w.writerow(["VPN_Proyecto", round(VPN_PROYECTO, 1)])
    w.writerow(["TIR_Proyecto", round(TIR_PROYECTO, 4)])
    w.writerow(["VPN_Inversionista", round(VPN_INVERSIONISTA, 1)])
    w.writerow(["TIR_Inversionista", round(TIR_INVERSIONISTA, 4)])

print("\nArchivo 'resultados_modelo.csv' generado.")

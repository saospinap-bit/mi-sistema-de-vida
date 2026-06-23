# -*- coding: utf-8 -*-
"""
Genera 'MODELO FINANCIERO PEPI.xlsx' LEYENDO los resultados de
'resultados_modelo.csv' (que produce modelo_financiero.py).
Asi el Excel y el modelo NUNCA difieren, y todas las celdas llevan VALORES
calculados (no formulas) -> ningun visor mostrara celdas vacias.

Uso:
    python3 modelo_financiero.py   # genera resultados_modelo.csv
    python3 generar_excel.py       # lee el CSV y arma el Excel
"""
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

CSV = "resultados_modelo.csv"

# ---------------------------------------------------------------
# 1) LEER Y PARSEAR EL CSV DEL MODELO
# ---------------------------------------------------------------
with open(CSV, encoding="utf-8") as f:
    rows = list(csv.reader(f))

def to_num(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return s

diseno, capex, indic, sens = [], [], [], []
flujos_header, flujos = [], []
seccion = None
for row in rows:
    if not row or all(c.strip() == "" for c in row):
        continue
    head = row[0].strip()
    if head.startswith("DISENO DE CAUDAL"):
        seccion = "diseno"; continue
    if head.startswith("CAPEX por capitulos"):
        seccion = "capex"; continue
    if head.startswith("FLUJOS DE CAJA"):
        seccion = "flujos"; continue
    if head == "INDICADORES":
        seccion = "indic"; continue
    if head.startswith("SENSIBILIDAD"):
        seccion = "sens"; continue
    if head.startswith("PROYECTO PEPI"):
        continue
    if seccion == "diseno" and len(row) >= 2:
        diseno.append((row[0], to_num(row[1])))
    elif seccion == "capex" and len(row) >= 2:
        capex.append((row[0], to_num(row[1])))
    elif seccion == "flujos":
        if head == "Anio":
            flujos_header = row
        else:
            flujos.append([to_num(c) if c.strip() != "" else "" for c in row])
    elif seccion == "indic" and len(row) >= 2:
        indic.append((row[0], to_num(row[1])))
    elif seccion == "sens" and len(row) >= 2:
        sens.append((row[0], to_num(row[1])))

ind = {k: v for k, v in indic}
CAPEX_TOTAL = next((v for k, v in capex if k.startswith("TOTAL")), 0.0)

# ---------------------------------------------------------------
# 2) ESTILOS
# ---------------------------------------------------------------
AZUL = "1F4E79"; CLARO = "D6E4F0"; GRIS = "F2F2F2"
f_tit = Font(bold=True, color="FFFFFF", size=12)
f_hdr = Font(bold=True, color="FFFFFF", size=10)
f_b = Font(bold=True)
fa = PatternFill("solid", fgColor=AZUL); fc = PatternFill("solid", fgColor=CLARO)
fg = PatternFill("solid", fgColor=GRIS)
ctr = Alignment(horizontal="center", vertical="center", wrap_text=True)
lft = Alignment(horizontal="left", vertical="center", wrap_text=True)
rgt = Alignment(horizontal="right", vertical="center")
thin = Side(style="thin", color="BFBFBF")
bd = Border(left=thin, right=thin, top=thin, bottom=thin)

def title(ws, rng, text):
    ws.merge_cells(rng)
    c = ws[rng.split(":")[0]]
    c.value = text; c.font = f_tit; c.fill = fa; c.alignment = ctr
    ws.row_dimensions[1].height = 26

def header(ws, row, headers):
    for j, h in enumerate(headers, 1):
        c = ws.cell(row, j, h); c.font = f_hdr; c.fill = fa; c.alignment = ctr; c.border = bd

def is_pct(label):
    l = label.lower()
    return any(w in l for w in ["wacc", "tir", "%"])

wb = Workbook()

# ---------------------------------------------------------------
# HOJA 1: DISENO DE CAUDAL
# ---------------------------------------------------------------
ws = wb.active; ws.title = "Diseno Caudal"; ws.sheet_view.showGridLines = False
title(ws, "A1:B1", "DISENO DE CAUDAL (Resolucion 0330 de 2017 - RAS)")
header(ws, 2, ["Concepto", "Valor"])
r = 3
for k, v in diseno:
    ws.cell(r, 1, k).font = f_b; ws.cell(r, 1).fill = fc
    c = ws.cell(r, 2, v)
    if isinstance(v, float):
        c.number_format = "#,##0.00"
    c.alignment = rgt
    for j in (1, 2):
        ws.cell(r, j).border = bd
    if r % 2 == 0:
        for j in (1, 2):
            ws.cell(r, j).fill = fg if j == 2 else fc
    r += 1
ws.column_dimensions["A"].width = 40; ws.column_dimensions["B"].width = 16

# ---------------------------------------------------------------
# HOJA 2: PRESUPUESTO / CAPEX
# ---------------------------------------------------------------
wp = wb.create_sheet("Presupuesto"); wp.sheet_view.showGridLines = False
title(wp, "A1:C1", "PRESUPUESTO DE OBRA - CAPEX (COP MM; precios de referencia, validar con APU)")
header(wp, 2, ["Capitulo", "COP MM", "% del total"])
r = 3
for k, v in capex:
    es_total = k.startswith("TOTAL")
    wp.cell(r, 1, k).alignment = lft
    if es_total:
        wp.cell(r, 1).font = f_b; wp.cell(r, 1).fill = fc
    cc = wp.cell(r, 2, v); cc.number_format = "#,##0"; cc.alignment = rgt
    if es_total:
        cc.font = f_b
    pcv = (v / CAPEX_TOTAL) if CAPEX_TOTAL else 0
    pc = wp.cell(r, 3, pcv); pc.number_format = "0.0%"; pc.alignment = rgt
    if es_total:
        pc.font = f_b
    for j in (1, 2, 3):
        wp.cell(r, j).border = bd
    if r % 2 == 0 and not es_total:
        for j in (1, 2, 3):
            wp.cell(r, j).fill = fg
    r += 1
wp.column_dimensions["A"].width = 56; wp.column_dimensions["B"].width = 12; wp.column_dimensions["C"].width = 12

# ---------------------------------------------------------------
# HOJA 3: FINANCIACION (derivada del CAPEX y porcentajes del modelo)
# ---------------------------------------------------------------
wfin = wb.create_sheet("Financiacion"); wfin.sheet_view.showGridLines = False
title(wfin, "A1:D1", "ESTRUCTURA DE FINANCIACION Y WACC")
header(wfin, 2, ["Fuente", "Participacion", "Monto (COP MM)", "Costo"])
fin = [
    ("Aporte publico no reembolsable (SGR/PDA/MinVivienda/cooperacion)", 0.80, "no exige retorno"),
    ("Deuda (banca de desarrollo / FINDETER)", 0.10, "Kd = 11%"),
    ("Equity (operador + municipio)", 0.10, "Ke = 14%"),
]
r = 3
for nombre, pct, costo in fin:
    wfin.cell(r, 1, nombre).alignment = lft
    wfin.cell(r, 2, pct).number_format = "0%"; wfin.cell(r, 2).alignment = ctr
    wfin.cell(r, 3, round(CAPEX_TOTAL * pct, 1)).number_format = "#,##0.0"; wfin.cell(r, 3).alignment = rgt
    wfin.cell(r, 4, costo).alignment = ctr
    for j in range(1, 5):
        wfin.cell(r, j).border = bd
    r += 1
wfin.cell(r, 1, "TOTAL").font = f_b; wfin.cell(r, 1).fill = fc
wfin.cell(r, 2, 1.0).number_format = "0%"; wfin.cell(r, 2).alignment = ctr; wfin.cell(r, 2).font = f_b
wfin.cell(r, 3, round(CAPEX_TOTAL, 1)).number_format = "#,##0.0"; wfin.cell(r, 3).alignment = rgt; wfin.cell(r, 3).font = f_b
for j in range(1, 5):
    wfin.cell(r, j).border = bd
r += 2
wfin.cell(r, 1, "WACC").font = f_b; wfin.cell(r, 1).fill = fc
wfin.cell(r, 2, ind.get("WACC", "")).number_format = "0.00%"; wfin.cell(r, 2).alignment = ctr; wfin.cell(r, 2).font = f_b
wfin.cell(r, 3, "Tasa de descuento del proyecto").alignment = lft
for j in range(1, 4):
    wfin.cell(r, j).border = bd
wfin.column_dimensions["A"].width = 56; wfin.column_dimensions["B"].width = 14
wfin.column_dimensions["C"].width = 16; wfin.column_dimensions["D"].width = 18

# ---------------------------------------------------------------
# HOJA 3b: AMORTIZACION DE LA DEUDA (reconstruida desde los flujos)
# ---------------------------------------------------------------
wa = wb.create_sheet("Amortizacion Deuda"); wa.sheet_view.showGridLines = False
title(wa, "A1:F1", "TABLA DE AMORTIZACION DE LA DEUDA (Sistema Frances - cuota fija)")
header(wa, 2, ["Anio", "Saldo inicial", "Interes", "Abono capital", "Cuota", "Saldo final"])
# columnas en flujos: Anio=0, Intereses=5, Amortizacion=6, Saldo_deuda(final)=7
col = {h: i for i, h in enumerate(flujos_header)}
ci_int = col.get("Intereses", 5); ci_amo = col.get("Amortizacion", 6); ci_sal = col.get("Saldo_deuda", 7)
saldo_ini = None
r = 3
for fila in flujos:
    anio = fila[0]
    if anio == 0:
        saldo_ini = fila[ci_sal] if isinstance(fila[ci_sal], (int, float)) else 0.0
        continue
    interes = fila[ci_int] if isinstance(fila[ci_int], (int, float)) else 0.0
    abono = fila[ci_amo] if isinstance(fila[ci_amo], (int, float)) else 0.0
    saldo_fin = fila[ci_sal] if isinstance(fila[ci_sal], (int, float)) else 0.0
    cuota = interes + abono
    vals = [anio, round(saldo_ini, 1), round(interes, 1), round(abono, 1), round(cuota, 1), round(saldo_fin, 1)]
    for j, val in enumerate(vals, 1):
        c = wa.cell(r, j, val)
        c.alignment = ctr if j == 1 else rgt
        if j > 1:
            c.number_format = "#,##0.0"
        c.border = bd
    if anio % 2 == 0:
        for j in range(1, 7):
            wa.cell(r, j).fill = fg
    saldo_ini = saldo_fin
    r += 1
for col_l, w in zip("ABCDEF", [8, 15, 13, 15, 13, 15]):
    wa.column_dimensions[col_l].width = w

# ---------------------------------------------------------------
# HOJA 4: FLUJOS DE CAJA
# ---------------------------------------------------------------
wf = wb.create_sheet("Flujos de Caja"); wf.sheet_view.showGridLines = False
ncol = len(flujos_header)
last = chr(ord("A") + ncol - 1)
title(wf, f"A1:{last}1", "FLUJOS DE CAJA (COP MM) - PROYECTO, INVERSIONISTA, BANCO Y SOCIAL")
header(wf, 2, flujos_header)
r = 3
for fila in flujos:
    for j, val in enumerate(fila, 1):
        c = wf.cell(r, j, val)
        if j == 1:
            c.alignment = ctr
        else:
            c.alignment = rgt
            if isinstance(val, float):
                c.number_format = "#,##0.0"
        c.border = bd
    if (r - 3) % 2 == 1:
        for j in range(1, ncol + 1):
            wf.cell(r, j).fill = fg
    r += 1
wf.column_dimensions["A"].width = 6
for j in range(2, ncol + 1):
    wf.column_dimensions[chr(ord("A") + j - 1)].width = 12

# ---------------------------------------------------------------
# HOJA 5: INDICADORES + SENSIBILIDAD
# ---------------------------------------------------------------
wi = wb.create_sheet("Indicadores"); wi.sheet_view.showGridLines = False
title(wi, "A1:C1", "INDICADORES DE RENTABILIDAD Y EVALUACION")
header(wi, 2, ["Indicador", "Valor", "Interpretacion"])
interp = {
    "WACC": "Costo de capital (tasa de descuento)",
    "VPN_Proyecto": "<0: no rentable solo con tarifas (tipico)",
    "TIR_Proyecto": "< WACC -> no rentable por si solo",
    "VPN_Inversionista": "Valor para el inversionista (con cofinanciacion)",
    "TIR_Inversionista": "Comparar con Ke = 14%",
    "VPN_Social_@9%": ">0: socialmente viable (tasa social DNP)",
    "Relacion_Beneficio_Costo": ">1: socialmente viable (B/C)",
}
r = 3
for k, v in indic:
    wi.cell(r, 1, k.replace("_", " ")).font = f_b; wi.cell(r, 1).fill = fc
    c = wi.cell(r, 2, v)
    c.number_format = "0.00%" if is_pct(k) else "#,##0.00"
    c.alignment = rgt; c.font = f_b
    wi.cell(r, 3, interp.get(k, "")).alignment = lft
    for j in (1, 2, 3):
        wi.cell(r, j).border = bd
    r += 1
r += 1
wi.merge_cells(f"A{r}:C{r}")
wi.cell(r, 1, "SENSIBILIDAD: % de aporte publico -> TIR del inversionista")
wi.cell(r, 1).font = f_tit; wi.cell(r, 1).fill = fa; wi.cell(r, 1).alignment = ctr
r += 1
header(wi, r, ["Aporte publico", "TIR inversionista", "Criterio (Ke=14%)"])
r += 1
for k, v in sens:
    pct = float(k.replace("%", "")) / 100
    wi.cell(r, 1, pct).number_format = "0%"; wi.cell(r, 1).alignment = ctr
    cc = wi.cell(r, 2, v); cc.number_format = "0.00%"; cc.alignment = rgt
    crit = "Viable" if isinstance(v, float) and v >= 0.14 else "No viable"
    wi.cell(r, 3, crit).alignment = ctr
    for j in (1, 2, 3):
        wi.cell(r, j).border = bd
    r += 1
wi.column_dimensions["A"].width = 30; wi.column_dimensions["B"].width = 18; wi.column_dimensions["C"].width = 40

# ---------------------------------------------------------------
# HOJA 6: RIESGOS (matriz de 20 + intervencion de 10)
# ---------------------------------------------------------------
wr = wb.create_sheet("Riesgos"); wr.sheet_view.showGridLines = False
title(wr, "A1:G1", "MATRIZ DE RIESGOS (20) - Nivel=PxI [Bajo 1-6 / Medio 8-12 / Alto 15-25]")
header(wr, 2, ["#", "Riesgo", "Tipo", "P", "I", "PxI", "Nivel"])
riesgos = [
    [1, "Sobrecostos en la construccion", "Financiero", 4, 4],
    [2, "Retrasos en el cronograma de obra", "Operativo", 4, 3],
    [3, "Demoras en gestion predial y servidumbres", "Legal", 3, 4],
    [4, "Insuficiencia/retraso del aporte publico (SGR/PDA)", "Financiero", 3, 5],
    [5, "Incremento de tasas de interes", "Financiero", 3, 4],
    [6, "Recaudo tarifario inferior al proyectado", "Comercial", 4, 4],
    [7, "Cambios regulatorios marco tarifario (CRA)", "Regulatorio", 2, 4],
    [8, "Alta turbiedad/contaminacion (mercurio) rio San Juan", "Ambiental", 4, 5],
    [9, "Inundaciones por lluvias extremas (Choco)", "Ambiental", 4, 4],
    [10, "Inadecuada disposicion de lodos PTAP", "Ambiental", 3, 4],
    [11, "Vertimiento de aguas de lavado sin tratar", "Ambiental", 3, 4],
    [12, "Afectacion de fauna/flora en obras", "Ambiental", 2, 3],
    [13, "Fallas o paradas de equipos de bombeo", "Operativo", 3, 3],
    [14, "Interrupcion del suministro electrico", "Operativo", 3, 4],
    [15, "Accidentes laborales en obra", "SST", 3, 4],
    [16, "Dificultad logistica y de acceso (transporte)", "Operativo", 4, 3],
    [17, "Orden publico en la region", "Social", 3, 4],
    [18, "Errores en estudios y disenios tecnicos", "Tecnico", 2, 4],
    [19, "Incumplimiento del contratista", "Contractual", 2, 4],
    [20, "Inflacion de costos operativos", "Financiero", 3, 3],
]
def nivel(pi):
    return "Alto" if pi >= 15 else ("Medio" if pi >= 8 else "Bajo")
r = 3
for ri in riesgos:
    pi = ri[3] * ri[4]
    vals = [ri[0], ri[1], ri[2], ri[3], ri[4], pi, nivel(pi)]
    for j, val in enumerate(vals, 1):
        c = wr.cell(r, j, val)
        c.alignment = lft if j == 2 else ctr
        c.border = bd
    r += 1
for col, w in zip("ABCDEFG", [5, 44, 14, 5, 5, 7, 9]):
    wr.column_dimensions[col].width = w
base = r + 2
wr.merge_cells(f"A{base}:H{base}")
wr.cell(base, 1, "INTERVENCION DE 10 RIESGOS (5 ambientales) Y RECALIFICACION")
wr.cell(base, 1).font = f_tit; wr.cell(base, 1).fill = fa; wr.cell(base, 1).alignment = ctr
header(wr, base + 1, ["#", "Riesgo", "Tipo", "Intervencion", "P res", "I res", "PxI res", "Nivel res"])
inter = [
    [1, "Sobrecostos de construccion", "Financiero", "Contrato EPC precio fijo + contingencia 10% + control de cambios", 2, 3],
    [6, "Bajo recaudo tarifario", "Comercial", "Cultura de pago, subsidios Ley 142, corte por mora, micromedicion", 2, 3],
    [4, "Insuficiencia del aporte publico", "Financiero", "Cierre financiero previo; convenios SGR/PDA y cooperacion", 2, 3],
    [8, "Turbiedad/mercurio rio San Juan", "Ambiental", "Bocatoma con desarenador, pretratamiento y monitoreo de mercurio", 2, 4],
    [9, "Inundaciones por lluvias extremas", "Ambiental", "Obras elevadas, drenaje, diseno hidrologico y plan de contingencia", 2, 3],
    [10, "Disposicion de lodos", "Ambiental", "Lechos de secado y disposicion final autorizada (CODECHOCO)", 1, 3],
    [11, "Vertimiento aguas de lavado", "Ambiental", "Recirculacion y tratamiento previo, permiso de vertimientos", 1, 3],
    [12, "Afectacion fauna/flora", "Ambiental", "Plan de Manejo Ambiental y compensacion forestal", 1, 2],
    [16, "Dificultad logistica/acceso", "Operativo", "Plan logistico, acopio de materiales y cronograma con holguras", 2, 2],
    [15, "Accidentes laborales", "SST", "SG-SST (Dec 1072/2015), capacitacion, EPP, permisos", 1, 4],
]
r = base + 2
for it in inter:
    pir = it[4] * it[5]
    vals = [it[0], it[1], it[2], it[3], it[4], it[5], pir, nivel(pir)]
    for j, val in enumerate(vals, 1):
        c = wr.cell(r, j, val)
        c.alignment = lft if j in (2, 4) else ctr
        c.border = bd
    r += 1
wr.column_dimensions["D"].width = 54; wr.column_dimensions["H"].width = 10

wb.calculation.fullCalcOnLoad = True
wb.save("MODELO FINANCIERO PEPI.xlsx")
print("OK -> MODELO FINANCIERO PEPI.xlsx  (valores leidos del modelo; sin celdas vacias)")
print(f"   Hojas: {wb.sheetnames}")
print(f"   CAPEX={CAPEX_TOTAL:,.0f}  WACC={ind.get('WACC')}  VPN_proy={ind.get('VPN_Proyecto')}  "
      f"VPN_inv={ind.get('VPN_Inversionista')}  B/C={ind.get('Relacion_Beneficio_Costo')}")

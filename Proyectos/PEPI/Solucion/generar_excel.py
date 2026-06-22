# -*- coding: utf-8 -*-
"""
Modelo financiero del Proyecto PEPI - Acueducto de Tesalia (Huila) en Excel,
CON FORMULAS VIVAS. Hojas:
  1. Supuestos          -> parametros (poblacion DANE, diseno Res 0330, financiacion)
  2. Diseno Caudal      -> caudal de diseno (Res 0330/2017) con formulas
  3. Presupuesto        -> CAPEX por capitulos
  4. Amortizacion Deuda -> sistema frances
  5. Flujos de Caja     -> proyecto, inversionista y banco
  6. Indicadores        -> WACC, VPN/TIR (proyecto, inversionista, socioeconomico)
  7. Riesgos            -> matriz de 20 + intervencion/recalificacion de 10
Al abrir en Excel/LibreOffice/Sheets, todo se recalcula al cambiar Supuestos.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

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

wb = Workbook()

# =============== HOJA 1: SUPUESTOS ===============
ws = wb.active; ws.title = "Supuestos"; ws.sheet_view.showGridLines = False
ws.merge_cells("A1:C1")
ws["A1"] = "SUPUESTOS - PROYECTO PEPI ACUEDUCTO DE TADO (CHOCO)"
ws["A1"].font = f_tit; ws["A1"].fill = fa; ws["A1"].alignment = ctr
ws.row_dimensions[1].height = 26
ws["A2"] = "Cifras en COP millones (salvo % y unidades indicadas). Fuente poblacion: DANE CNPV 2018."
ws["A2"].font = Font(italic=True, size=8)

filas = [
    ("Parametro", "Valor", "Unidad / fuente"),
    ("Poblacion urbana 2025 (cabecera)", 11917, "hab (DANE)"),
    ("Tasa de crecimiento", 0.008, "% anual"),
    ("Horizonte de diseno/evaluacion", 25, "anios (Res 0330)"),
    ("Poblacion de diseno", "=B4*(1+B5)^B6", "hab"),
    ("Dotacion neta (alt<1000 m)", 140, "L/hab.dia (Res 0330)"),
    ("Perdidas maximas admisibles", 0.25, "% (Res 0330)"),
    ("Dotacion bruta", "=B8/(1-B9)", "L/hab.dia"),
    ("Coef. maximo diario k1", 1.30, "Res 0330"),
    ("Coef. maximo horario k2", 1.60, "Res 0330"),
    ("Caudal medio diario", "=B10*B7/86400", "L/s"),
    ("Caudal maximo diario (PTAP)", "=B13*B11", "L/s"),
    ("Caudal maximo horario", "=B14*B12", "L/s"),
    ("Capacidad PTAP adoptada", 45, "L/s"),
    ("CAPEX total", "=Presupuesto!B12", "COP MM"),
    ("% Aporte publico (SGR/PDA/SGP)", 0.90, "%"),
    ("% Deuda", 0.05, "%"),
    ("% Equity", 0.05, "%"),
    ("Aporte publico", "=B17*B18", "COP MM"),
    ("Deuda", "=B17*B19", "COP MM"),
    ("Equity", "=B17*B20", "COP MM"),
    ("Kd (costo deuda)", 0.11, "%"),
    ("Ke (costo equity)", 0.14, "%"),
    ("Tasa de impuestos", 0.35, "%"),
    ("Plazo de la deuda", 12, "anios"),
    ("Depreciacion anual", "=B17/B6", "COP MM"),
    ("Cuota anual deuda (frances)", "=B22*B24/(1-(1+B24)^(-B27))", "COP MM"),
    ("WACC (capital remunerado 50/50)", "=0.5*B25+0.5*B24*(1-B26)", "%"),
    ("Suscriptores anio 1", 3400, "suscriptores"),
    ("Crecimiento suscriptores", 0.012, "% anual"),
    ("Factura media acueducto anio 1", 28000, "COP/mes"),
    ("Crecimiento tarifa", 0.035, "% anual"),
    ("OPEX anio 1", 1050, "COP MM"),
    ("Crecimiento OPEX", 0.04, "% anual"),
    ("Tasa social de descuento (DNP)", 0.09, "%"),
    ("Beneficio social por hogar", 75000, "COP/mes"),
]
r = 3
pct_rows = set()
for row in filas:
    ws.cell(r, 1, row[0]); ws.cell(r, 2, row[1]); ws.cell(r, 3, row[2])
    if r == 3:
        for c in range(1, 4):
            ws.cell(r, c).font = f_hdr; ws.cell(r, c).fill = fa; ws.cell(r, c).alignment = ctr
    else:
        ws.cell(r, 1).font = f_b; ws.cell(r, 1).fill = fc
        unit = str(row[2])
        if unit.startswith("%"):
            ws.cell(r, 2).number_format = "0.00%"
        elif "hab" in unit or "suscript" in unit:
            ws.cell(r, 2).number_format = "#,##0"
        elif "COP/mes" in unit:
            ws.cell(r, 2).number_format = "#,##0"
        elif "anios" in unit or "Res" in unit:
            ws.cell(r, 2).number_format = "#,##0.00"
        else:
            ws.cell(r, 2).number_format = "#,##0.0"
        ws.cell(r, 2).alignment = rgt; ws.cell(r, 3).alignment = lft
    for c in range(1, 4):
        ws.cell(r, c).border = bd
    r += 1
ws.column_dimensions["A"].width = 32
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 20

S = "Supuestos!"
POBd = f"{S}$B$7"; DOTb = f"{S}$B$10"; QMD = f"{S}$B$14"
CAPEX = f"{S}$B$17"; APORTE = f"{S}$B$21"; DEUDA = f"{S}$B$22"; EQUITY = f"{S}$B$23"
KD = f"{S}$B$24"; KE = f"{S}$B$25"; IMP = f"{S}$B$26"; PLAZO = f"{S}$B$27"
DEP = f"{S}$B$28"; CUOTA = f"{S}$B$29"; WACC = f"{S}$B$30"
SUS1 = f"{S}$B$31"; CSUS = f"{S}$B$32"; FAC1 = f"{S}$B$33"; CFAC = f"{S}$B$34"
OPEX1 = f"{S}$B$35"; COPEX = f"{S}$B$36"; TSOC = f"{S}$B$37"; BENH = f"{S}$B$38"
HOR = 25

# =============== HOJA 2: DISENO CAUDAL ===============
wd = wb.create_sheet("Diseno Caudal"); wd.sheet_view.showGridLines = False
wd.merge_cells("A1:C1")
wd["A1"] = "CAUDAL DE DISENIO (Resolucion 0330 de 2017)"
wd["A1"].font = f_tit; wd["A1"].fill = fa; wd["A1"].alignment = ctr
wd.row_dimensions[1].height = 24
dis = [
    ("Concepto", "Valor", "Unidad"),
    ("Poblacion de diseno (anio 25)", f"={POBd}", "hab"),
    ("Dotacion bruta", f"={DOTb}", "L/hab.dia"),
    ("Caudal medio diario (Qmd)", f"={S}$B$13", "L/s"),
    ("Caudal maximo diario (QMD)", f"={QMD}", "L/s -> PTAP"),
    ("Caudal maximo horario (QMH)", f"={S}$B$15", "L/s -> redes"),
    ("Capacidad PTAP adoptada", f"={S}$B$16", "L/s"),
]
r = 2
for row in dis:
    wd.cell(r, 1, row[0]); wd.cell(r, 2, row[1]); wd.cell(r, 3, row[2])
    if r == 2:
        for c in range(1, 4):
            wd.cell(r, c).font = f_hdr; wd.cell(r, c).fill = fa; wd.cell(r, c).alignment = ctr
    else:
        wd.cell(r, 1).font = f_b; wd.cell(r, 1).fill = fc
        wd.cell(r, 2).number_format = "#,##0.0"; wd.cell(r, 2).alignment = rgt
        wd.cell(r, 3).alignment = lft
    for c in range(1, 4):
        wd.cell(r, c).border = bd
    r += 1
wd.column_dimensions["A"].width = 30; wd.column_dimensions["B"].width = 14; wd.column_dimensions["C"].width = 16

# =============== HOJA 3: PRESUPUESTO ===============
wp = wb.create_sheet("Presupuesto"); wp.sheet_view.showGridLines = False
wp.merge_cells("A1:C1")
wp["A1"] = "PRESUPUESTO DE OBRA - CAPEX (precios de referencia; validar con APU)"
wp["A1"].font = f_tit; wp["A1"].fill = fa; wp["A1"].alignment = ctr
wp.row_dimensions[1].height = 24
cap = [
    ("Preliminares y obras provisionales", 350),
    ("Captacion (bocatoma rio San Juan) + desarenador", 950),
    ("Aduccion y conduccion (PVC/HD ~4 km)", 1900),
    ("PTAP compacta 45 L/s (civil+equipos+dosif.+lab)", 3800),
    ("Tanque de almacenamiento (1.000 m3)", 1200),
    ("Estacion de bombeo (bombas + variadores)", 750),
    ("Redes de distribucion y sectorizacion", 2700),
    ("Micromedicion (~3.700 medidores) + macromedicion", 720),
    ("Estudios, disenios e interventoria", 1100),
]
wp.cell(2, 1, "Capitulo"); wp.cell(2, 2, "COP MM")
for c in range(1, 3):
    wp.cell(2, c).font = f_hdr; wp.cell(2, c).fill = fa; wp.cell(2, c).alignment = ctr; wp.cell(2, c).border = bd
r = 3
for nombre, val in cap:
    wp.cell(r, 1, nombre); wp.cell(r, 2, val)
    wp.cell(r, 2).number_format = "#,##0"; wp.cell(r, 2).alignment = rgt
    wp.cell(r, 1).alignment = lft
    for c in range(1, 3):
        wp.cell(r, c).border = bd
    if r % 2 == 0:
        for c in range(1, 3):
            wp.cell(r, c).fill = fg
    r += 1
wp.cell(r, 1, "TOTAL CAPEX"); wp.cell(r, 1).font = f_b; wp.cell(r, 1).fill = fc
wp.cell(r, 2, f"=SUM(B3:B{r-1})"); wp.cell(r, 2).number_format = "#,##0"
wp.cell(r, 2).font = f_b; wp.cell(r, 2).alignment = rgt
for c in range(1, 3):
    wp.cell(r, c).border = bd
# total en B13 (9 capitulos: filas 3..11, total fila 12). Ajustar referencia en Supuestos.
TOTAL_ROW = r
wp.column_dimensions["A"].width = 52; wp.column_dimensions["B"].width = 12

# =============== HOJA 4: AMORTIZACION ===============
wa = wb.create_sheet("Amortizacion Deuda"); wa.sheet_view.showGridLines = False
wa.merge_cells("A1:F1")
wa["A1"] = "AMORTIZACION DE LA DEUDA (sistema frances)"
wa["A1"].font = f_tit; wa["A1"].fill = fa; wa["A1"].alignment = ctr
wa.row_dimensions[1].height = 24
for j, h in enumerate(["Anio", "Saldo inicial", "Interes", "Abono capital", "Cuota", "Saldo final"], 1):
    c = wa.cell(2, j, h); c.font = f_hdr; c.fill = fa; c.alignment = ctr; c.border = bd
for t in range(1, HOR + 1):
    row = t + 2
    wa.cell(row, 1, t)
    wa.cell(row, 2, f"={DEUDA}" if t == 1 else f"=F{row-1}")
    wa.cell(row, 3, f"=IF(A{row}<={PLAZO},B{row}*{KD},0)")
    wa.cell(row, 5, f"=IF(A{row}<={PLAZO},{CUOTA},0)")
    wa.cell(row, 4, f"=E{row}-C{row}")
    wa.cell(row, 6, f"=B{row}-D{row}")
    for j in range(1, 7):
        cell = wa.cell(row, j); cell.border = bd
        cell.alignment = ctr if j == 1 else rgt
        if j > 1:
            cell.number_format = "#,##0.0"
    if t % 2 == 0:
        for j in range(1, 7):
            wa.cell(row, j).fill = fg
for col, w in zip("ABCDEF", [8, 15, 13, 15, 13, 15]):
    wa.column_dimensions[col].width = w
AM = "'Amortizacion Deuda'!"

# =============== HOJA 5: FLUJOS ===============
wf = wb.create_sheet("Flujos de Caja"); wf.sheet_view.showGridLines = False
wf.merge_cells("A1:K1")
wf["A1"] = "FLUJOS DE CAJA - PROYECTO, INVERSIONISTA Y BANCO (COP MM)"
wf["A1"].font = f_tit; wf["A1"].fill = fa; wf["A1"].alignment = ctr
wf.row_dimensions[1].height = 24
hdr = ["Anio", "Ingresos", "OPEX", "EBITDA", "Deprec.", "EBIT", "Intereses",
       "FC Proyecto", "Util.neta", "FC Inversionista", "FC Banco"]
for j, h in enumerate(hdr, 1):
    c = wf.cell(2, j, h); c.font = f_hdr; c.fill = fa; c.alignment = ctr; c.border = bd
# anio 0 (fila 3)
wf.cell(3, 1, 0)
wf.cell(3, 8, f"=-{CAPEX}"); wf.cell(3, 10, f"=-{EQUITY}"); wf.cell(3, 11, f"={DEUDA}")
for j in range(1, 12):
    wf.cell(3, j).border = bd
    wf.cell(3, j).alignment = ctr if j == 1 else rgt
    if j > 1:
        wf.cell(3, j).number_format = "#,##0.0"
for t in range(1, HOR + 1):
    row = t + 3; am = t + 2
    wf.cell(row, 1, t)
    wf.cell(row, 2, f"={SUS1}*(1+{CSUS})^(A{row}-1)*{FAC1}*(1+{CFAC})^(A{row}-1)*12/1000000")
    wf.cell(row, 3, f"={OPEX1}*(1+{COPEX})^(A{row}-1)")
    wf.cell(row, 4, f"=B{row}-C{row}")
    wf.cell(row, 5, f"={DEP}")
    wf.cell(row, 6, f"=D{row}-E{row}")
    wf.cell(row, 7, f"={AM}C{am}")
    wf.cell(row, 8, f"=F{row}*(1-{IMP})+E{row}")
    wf.cell(row, 9, f"=(F{row}-G{row})*(1-{IMP})")
    wf.cell(row, 10, f"=I{row}+E{row}-{AM}D{am}")
    wf.cell(row, 11, f"=-{AM}E{am}")
    for j in range(1, 12):
        cell = wf.cell(row, j); cell.border = bd
        cell.alignment = ctr if j == 1 else rgt
        if j > 1:
            cell.number_format = "#,##0.0"
    if t % 2 == 0:
        for j in range(1, 12):
            wf.cell(row, j).fill = fg
for col, w in zip("ABCDEFGHIJK", [6, 10, 9, 9, 9, 9, 10, 12, 9, 14, 11]):
    wf.column_dimensions[col].width = w

# =============== HOJA 6: INDICADORES ===============
wi = wb.create_sheet("Indicadores"); wi.sheet_view.showGridLines = False
wi.merge_cells("A1:C1")
wi["A1"] = "INDICADORES DE RENTABILIDAD"
wi["A1"].font = f_tit; wi["A1"].fill = fa; wi["A1"].alignment = ctr
wi.row_dimensions[1].height = 24
FCp = "'Flujos de Caja'!$H$3:$H$28"; FCp1 = "'Flujos de Caja'!$H$4:$H$28"; FCp0 = "'Flujos de Caja'!$H$3"
FCi = "'Flujos de Caja'!$J$3:$J$28"; FCi1 = "'Flujos de Caja'!$J$4:$J$28"; FCi0 = "'Flujos de Caja'!$J$3"
# Flujo economico: -CAPEX (B3 col?) lo construimos aparte con beneficios sociales.
ind = [
    ("Indicador", "Valor", "Criterio"),
    ("WACC", f"={WACC}", "Costo de capital remunerado"),
    ("VPN Proyecto 'puro' (@WACC)", f"={FCp0}+NPV({WACC},{FCp1})", "No rentable si <0"),
    ("TIR Proyecto 'puro'", f"=IRR({FCp})", "Viable si > WACC"),
    ("VPN Inversionista (@Ke)", f"={FCi0}+NPV({KE},{FCi1})", "Viable si >0"),
    ("TIR Inversionista", f"=IRR({FCi})", "Viable si > Ke"),
]
r = 2
for row in ind:
    wi.cell(r, 1, row[0]); wi.cell(r, 2, row[1]); wi.cell(r, 3, row[2])
    if r == 2:
        for c in range(1, 4):
            wi.cell(r, c).font = f_hdr; wi.cell(r, c).fill = fa; wi.cell(r, c).alignment = ctr
    else:
        wi.cell(r, 1).font = f_b; wi.cell(r, 1).fill = fc; wi.cell(r, 3).alignment = lft
        lab = row[0]
        wi.cell(r, 2).number_format = "0.00%" if ("WACC" in lab or "TIR" in lab) else "#,##0.0"
        wi.cell(r, 2).alignment = rgt; wi.cell(r, 2).font = f_b
    for c in range(1, 4):
        wi.cell(r, c).border = bd
    r += 1
# Evaluacion socioeconomica
r += 1
wi.cell(r, 1, "EVALUACION SOCIOECONOMICA (tasa social DNP)"); wi.cell(r, 1).font = f_b
r += 1
# beneficios col E, costos col F (años 1..25) - tabla auxiliar
wi.cell(r, 5, "Anio"); wi.cell(r, 6, "Beneficio"); wi.cell(r, 7, "OPEX"); wi.cell(r, 8, "Flujo econ.")
for c in range(5, 9):
    wi.cell(r, c).font = f_hdr; wi.cell(r, c).fill = fa; wi.cell(r, c).alignment = ctr; wi.cell(r, c).border = bd
econ_start = r + 1
wi.cell(econ_start, 5, 0); wi.cell(econ_start, 8, f"=-{CAPEX}")
for c in (5, 6, 7, 8):
    wi.cell(econ_start, c).border = bd; wi.cell(econ_start, c).number_format = "#,##0.0"
for t in range(1, HOR + 1):
    row = econ_start + t
    wi.cell(row, 5, t)
    wi.cell(row, 6, f"={SUS1}*(1+{CSUS})^(E{row}-1)*{BENH}*12/1000000")
    wi.cell(row, 7, f"={OPEX1}*(1+{COPEX})^(E{row}-1)")
    wi.cell(row, 8, f"=F{row}-G{row}")
    for c in (5, 6, 7, 8):
        wi.cell(row, c).border = bd; wi.cell(row, c).number_format = "#,##0.0"
econ_end = econ_start + HOR
FCe = f"$H${econ_start}:$H${econ_end}"; FCe1 = f"$H${econ_start+1}:$H${econ_end}"; FCe0 = f"$H${econ_start}"
# resultados socioeconomicos en A/B debajo
rr = r + 1
wi.cell(rr, 1, "VPN Economico (@tasa social)"); wi.cell(rr, 1).font = f_b; wi.cell(rr, 1).fill = fc
wi.cell(rr, 2, f"={FCe0}+NPV({TSOC},{FCe1})"); wi.cell(rr, 2).number_format = "#,##0.0"; wi.cell(rr, 2).alignment = rgt
wi.cell(rr + 1, 1, "TIR Economica"); wi.cell(rr + 1, 1).font = f_b; wi.cell(rr + 1, 1).fill = fc
wi.cell(rr + 1, 2, f"=IRR({FCe})"); wi.cell(rr + 1, 2).number_format = "0.00%"; wi.cell(rr + 1, 2).alignment = rgt
for rx in (rr, rr + 1):
    for c in (1, 2):
        wi.cell(rx, c).border = bd
wi.column_dimensions["A"].width = 30; wi.column_dimensions["B"].width = 15; wi.column_dimensions["C"].width = 26
for col in "EFGH":
    wi.column_dimensions[col].width = 11

# =============== HOJA 7: RIESGOS ===============
wr = wb.create_sheet("Riesgos"); wr.sheet_view.showGridLines = False
wr.merge_cells("A1:G1")
wr["A1"] = "MATRIZ DE RIESGOS (20) - Nivel=PxI [Bajo 1-6 / Medio 8-12 / Alto 15-25]"
wr["A1"].font = f_tit; wr["A1"].fill = fa; wr["A1"].alignment = ctr
wr.row_dimensions[1].height = 24
for j, h in enumerate(["#", "Riesgo", "Tipo", "P", "I", "PxI", "Nivel"], 1):
    c = wr.cell(2, j, h); c.font = f_hdr; c.fill = fa; c.alignment = ctr; c.border = bd
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
r = 3
for ri in riesgos:
    wr.cell(r, 1, ri[0]); wr.cell(r, 2, ri[1]); wr.cell(r, 3, ri[2])
    wr.cell(r, 4, ri[3]); wr.cell(r, 5, ri[4])
    wr.cell(r, 6, f"=D{r}*E{r}")
    wr.cell(r, 7, f'=IF(F{r}>=15,"Alto",IF(F{r}>=8,"Medio","Bajo"))')
    for j in range(1, 8):
        cell = wr.cell(r, j); cell.border = bd
        cell.alignment = ctr if j != 2 else lft
    r += 1
for col, w in zip("ABCDEFG", [5, 42, 14, 5, 5, 7, 9]):
    wr.column_dimensions[col].width = w

base = r + 2
wr.merge_cells(f"A{base}:H{base}")
wr.cell(base, 1, "INTERVENCION DE 10 RIESGOS (5 ambientales) Y RECALIFICACION")
wr.cell(base, 1).font = f_tit; wr.cell(base, 1).fill = fa; wr.cell(base, 1).alignment = ctr
wr.row_dimensions[base].height = 24
for j, h in enumerate(["#", "Riesgo", "Tipo", "Intervencion", "P res", "I res", "PxI res", "Nivel res"], 1):
    c = wr.cell(base + 1, j, h); c.font = f_hdr; c.fill = fa; c.alignment = ctr; c.border = bd
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
    wr.cell(r, 1, it[0]); wr.cell(r, 2, it[1]); wr.cell(r, 3, it[2]); wr.cell(r, 4, it[3])
    wr.cell(r, 5, it[4]); wr.cell(r, 6, it[5])
    wr.cell(r, 7, f"=E{r}*F{r}")
    wr.cell(r, 8, f'=IF(G{r}>=15,"Alto",IF(G{r}>=8,"Medio","Bajo"))')
    for j in range(1, 9):
        cell = wr.cell(r, j); cell.border = bd
        cell.alignment = ctr if j not in (2, 4) else lft
    r += 1
wr.column_dimensions["D"].width = 54; wr.column_dimensions["H"].width = 10

wb.save("MODELO FINANCIERO PEPI.xlsx")
print("OK -> MODELO FINANCIERO PEPI.xlsx  (TOTAL CAPEX en Presupuesto!B%d)" % TOTAL_ROW)

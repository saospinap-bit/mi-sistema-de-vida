# -*- coding: utf-8 -*-
"""
Genera el modelo tecnico-financiero del Proyecto PEPI (Acueducto de Tado, Choco)
en Excel (.xlsx) CON FORMULAS VIVAS.

Hojas:
  1. Diseno de Caudal   -> Resolucion 0330/2017 (RAS): poblacion, dotacion, k1/k2, QMD/QMH
  2. Supuestos          -> parametros de entrada (editables)
  3. Amortizacion Deuda -> tabla de amortizacion (sistema frances)
  4. Flujos de Caja     -> ingresos, OPEX, EBITDA, EBIT, FC Proyecto/Inversionista/Banco y FC Social
  5. Indicadores        -> WACC, VPN/TIR (proyecto e inversionista) y evaluacion social (VPN, B/C)
  6. Riesgos            -> matriz de 20 riesgos + intervencion/recalificacion de 10

Al abrir el archivo, todas las celdas con formula se recalculan si cambias los Supuestos.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

AZUL = "1F4E79"
AZUL_CLARO = "D6E4F0"
GRIS = "F2F2F2"

f_titulo = Font(bold=True, color="FFFFFF", size=12)
f_hdr = Font(bold=True, color="FFFFFF", size=10)
f_bold = Font(bold=True)
fill_azul = PatternFill("solid", fgColor=AZUL)
fill_clar = PatternFill("solid", fgColor=AZUL_CLARO)
fill_gris = PatternFill("solid", fgColor=GRIS)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)
right = Alignment(horizontal="right", vertical="center")
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

HOR_N = 25  # anios

wb = Workbook()

# ===============================================================
# HOJA 1: DISENO DE CAUDAL (Resolucion 0330 de 2017 - RAS)
# ===============================================================
wd = wb.active
wd.title = "Diseno de Caudal"
wd.sheet_view.showGridLines = False
wd.merge_cells("A1:C1")
wd["A1"] = "DISENO DE CAUDAL - ACUEDUCTO DE TADO (Resolucion 0330 de 2017 - RAS)"
wd["A1"].font = f_titulo; wd["A1"].fill = fill_azul; wd["A1"].alignment = center
wd.row_dimensions[1].height = 28

dis = [
    ("Parametro", "Valor", "Unidad / Fuente"),
    ("Poblacion municipio (CNPV 2018, DANE)", 17000, "hab"),
    ("Fraccion urbana (estimada)", 0.60, "%"),
    ("Poblacion urbana 2018", "=B4*B5", "hab"),
    ("Anio base", 2024, "anio"),
    ("Tasa de crecimiento anual", 0.012, "%"),
    ("Periodo de diseno", 25, "anios"),
    ("Poblacion urbana base", "=B6*(1+B8)^(B7-2018)", "hab"),
    ("Poblacion de diseno", "=B10*(1+B8)^B9", "hab (+25 anios)"),
    ("Dotacion neta (Art. 43, clima calido)", 140, "L/hab.dia"),
    ("Perdidas tecnicas max. (Art. 44)", 0.25, "%"),
    ("Dotacion bruta", "=B12/(1-B13)", "L/hab.dia"),
    ("k1 (coef. max. diario)", 1.30, "Art. 47"),
    ("k2 (coef. max. horario)", 1.60, "Art. 47"),
    ("Caudal medio diario (Qmd)", "=B11*B14/86400", "L/s"),
    ("Caudal maximo diario (QMD)", "=B17*B15", "L/s"),
    ("Caudal maximo horario (QMH)", "=B18*B16", "L/s"),
    ("Capacidad PTAP seleccionada", 45, "L/s"),
]
r = 3
for row in dis:
    wd.cell(r, 1, row[0]); wd.cell(r, 2, row[1]); wd.cell(r, 3, row[2])
    if r == 3:
        for c in range(1, 4):
            wd.cell(r, c).font = f_hdr; wd.cell(r, c).fill = fill_azul; wd.cell(r, c).alignment = center
    else:
        wd.cell(r, 1).font = f_bold; wd.cell(r, 1).fill = fill_clar
        if row[2] == "%":
            wd.cell(r, 2).number_format = "0.0%"
        else:
            wd.cell(r, 2).number_format = "#,##0.00"
        wd.cell(r, 2).alignment = right
        wd.cell(r, 3).alignment = left
    for c in range(1, 4):
        wd.cell(r, c).border = border
    r += 1
wd.column_dimensions["A"].width = 38
wd.column_dimensions["B"].width = 14
wd.column_dimensions["C"].width = 20

# ===============================================================
# HOJA 2: SUPUESTOS
# ===============================================================
ws = wb.create_sheet("Supuestos")
ws.sheet_view.showGridLines = False
ws.merge_cells("A1:C1")
ws["A1"] = "SUPUESTOS DEL MODELO - PROYECTO PEPI (ACUEDUCTO DE TADO, CHOCO)"
ws["A1"].font = f_titulo; ws["A1"].fill = fill_azul; ws["A1"].alignment = center
ws.row_dimensions[1].height = 28
ws["A2"] = "Cifras en COP millones (salvo %). CAPEX anclado a inversion real (19.971 MM)."
ws["A2"].font = Font(italic=True, size=9)

sup = [
    ("Parametro", "Valor", "Unidad"),
    ("CAPEX total", 19971, "COP MM"),
    ("% Aporte publico (SGR/PDA/cooperacion)", 0.80, "%"),
    ("% Deuda (banca de desarrollo)", 0.10, "%"),
    ("% Equity (operador/municipio)", 0.10, "%"),
    ("Aporte publico", "=B4*B5", "COP MM"),
    ("Deuda", "=B4*B6", "COP MM"),
    ("Equity", "=B4*B7", "COP MM"),
    ("Kd (costo deuda)", 0.11, "%"),
    ("Ke (costo equity)", 0.14, "%"),
    ("Tasa social de descuento (DNP)", 0.09, "%"),
    ("Tasa de impuestos", 0.35, "%"),
    ("Plazo de la deuda", 10, "anios"),
    ("Horizonte de evaluacion", 25, "anios"),
    ("Ingreso tarifa anio 1", 1500, "COP MM"),
    ("Crecimiento ingresos", 0.035, "%"),
    ("OPEX anio 1", 1150, "COP MM"),
    ("Crecimiento OPEX", 0.035, "%"),
    ("Beneficio social anio 1", 4150, "COP MM"),
    ("Crecimiento beneficio social", 0.035, "%"),
    ("Depreciacion anual", "=B4/B16", "COP MM"),
    ("Cuota anual deuda (frances)", "=B9*B11/(1-(1+B11)^(-B15))", "COP MM"),
    ("WACC", "=B5*B13+B7*B12+B6*B11*(1-B14)", "%"),
]
r = 3
for row in sup:
    ws.cell(r, 1, row[0]); ws.cell(r, 2, row[1]); ws.cell(r, 3, row[2])
    if r == 3:
        for c in range(1, 4):
            ws.cell(r, c).font = f_hdr; ws.cell(r, c).fill = fill_azul; ws.cell(r, c).alignment = center
    else:
        ws.cell(r, 1).font = f_bold; ws.cell(r, 1).fill = fill_clar
        if row[2] == "%":
            ws.cell(r, 2).number_format = "0.00%"
        else:
            ws.cell(r, 2).number_format = "#,##0.0"
        ws.cell(r, 2).alignment = right
        ws.cell(r, 3).alignment = center
    for c in range(1, 4):
        ws.cell(r, c).border = border
    r += 1
ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 12

S = "Supuestos!"
CAPEX = f"{S}$B$4"
DEUDA = f"{S}$B$9"
EQUITY = f"{S}$B$10"
KD = f"{S}$B$11"
KE = f"{S}$B$12"
TSOC = f"{S}$B$13"
IMP = f"{S}$B$14"
PLAZO = f"{S}$B$15"
ING1 = f"{S}$B$17"
CRECI = f"{S}$B$18"
OPEX1 = f"{S}$B$19"
CRECO = f"{S}$B$20"
BEN1 = f"{S}$B$21"
CRECB = f"{S}$B$22"
DEP = f"{S}$B$23"
CUOTA = f"{S}$B$24"
WACC = f"{S}$B$25"

# ===============================================================
# HOJA 3: AMORTIZACION DEUDA
# ===============================================================
wa = wb.create_sheet("Amortizacion Deuda")
wa.sheet_view.showGridLines = False
wa.merge_cells("A1:F1")
wa["A1"] = "TABLA DE AMORTIZACION DE LA DEUDA (Sistema Frances - cuota fija)"
wa["A1"].font = f_titulo; wa["A1"].fill = fill_azul; wa["A1"].alignment = center
wa.row_dimensions[1].height = 26
hdr = ["Anio", "Saldo inicial", "Interes", "Abono capital", "Cuota", "Saldo final"]
for j, h in enumerate(hdr, start=1):
    c = wa.cell(2, j, h); c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border
for t in range(1, HOR_N + 1):
    row = t + 2
    wa.cell(row, 1, t)
    wa.cell(row, 2, f"={DEUDA}" if t == 1 else f"=F{row-1}")
    wa.cell(row, 3, f"=IF(A{row}<={PLAZO},B{row}*{KD},0)")
    wa.cell(row, 5, f"=IF(A{row}<={PLAZO},{CUOTA},0)")
    wa.cell(row, 4, f"=E{row}-C{row}")
    wa.cell(row, 6, f"=B{row}-D{row}")
    for j in range(1, 7):
        cell = wa.cell(row, j); cell.border = border
        cell.alignment = center if j == 1 else right
        if j != 1:
            cell.number_format = "#,##0.0"
    if t % 2 == 0:
        for j in range(1, 7):
            wa.cell(row, j).fill = fill_gris
for col, w in zip("ABCDEF", [8, 16, 14, 16, 14, 16]):
    wa.column_dimensions[col].width = w

# ===============================================================
# HOJA 4: FLUJOS DE CAJA
# ===============================================================
wf = wb.create_sheet("Flujos de Caja")
wf.sheet_view.showGridLines = False
wf.merge_cells("A1:M1")
wf["A1"] = "FLUJOS DE CAJA - PROYECTO, INVERSIONISTA, BANCO Y SOCIAL (COP MM)"
wf["A1"].font = f_titulo; wf["A1"].fill = fill_azul; wf["A1"].alignment = center
wf.row_dimensions[1].height = 26
hdr = ["Anio", "Ingresos", "OPEX", "EBITDA", "Deprec.", "EBIT", "Intereses",
       "FC Proyecto", "Util. neta", "FC Inversionista", "FC Banco", "Benef. social", "FC Social"]
for j, h in enumerate(hdr, start=1):
    c = wf.cell(2, j, h); c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border

# Anio 0 (fila 3)
wf.cell(3, 1, 0)
wf.cell(3, 8, f"=-{CAPEX}")     # FC Proyecto
wf.cell(3, 10, f"=-{EQUITY}")   # FC Inversionista
wf.cell(3, 11, f"={DEUDA}")     # FC Banco
wf.cell(3, 13, f"=-{CAPEX}")    # FC Social
for j in range(1, 14):
    wf.cell(3, j).border = border
    wf.cell(3, j).alignment = center if j == 1 else right
    if j != 1:
        wf.cell(3, j).number_format = "#,##0.0"

AM = "'Amortizacion Deuda'!"
for t in range(1, HOR_N + 1):
    row = t + 3
    am_row = t + 2
    wf.cell(row, 1, t)
    wf.cell(row, 2, f"={ING1}*(1+{CRECI})^(A{row}-1)")
    wf.cell(row, 3, f"={OPEX1}*(1+{CRECO})^(A{row}-1)")
    wf.cell(row, 4, f"=B{row}-C{row}")
    wf.cell(row, 5, f"={DEP}")
    wf.cell(row, 6, f"=D{row}-E{row}")
    wf.cell(row, 7, f"={AM}C{am_row}")
    # FC Proyecto = EBITDA - MAX(EBIT,0)*imp
    wf.cell(row, 8, f"=D{row}-MAX(F{row},0)*{IMP}")
    # Util neta = (EBIT-Int) - MAX(EBIT-Int,0)*imp
    wf.cell(row, 9, f"=(F{row}-G{row})-MAX(F{row}-G{row},0)*{IMP}")
    # FC Inversionista = Util neta + Deprec - Abono capital
    wf.cell(row, 10, f"=I{row}+E{row}-{AM}D{am_row}")
    # FC Banco = -(cuota)
    wf.cell(row, 11, f"=-{AM}E{am_row}")
    # Beneficio social
    wf.cell(row, 12, f"={BEN1}*(1+{CRECB})^(A{row}-1)")
    # FC Social = Beneficio social - OPEX
    wf.cell(row, 13, f"=L{row}-C{row}")
    for j in range(1, 14):
        cell = wf.cell(row, j); cell.border = border
        cell.alignment = center if j == 1 else right
        if j != 1:
            cell.number_format = "#,##0.0"
    if t % 2 == 0:
        for j in range(1, 14):
            wf.cell(row, j).fill = fill_gris
for col, w in zip("ABCDEFGHIJKLM", [6, 10, 9, 10, 9, 10, 10, 12, 10, 14, 10, 12, 11]):
    wf.column_dimensions[col].width = w

LAST = HOR_N + 3  # ultima fila de datos (anio 25 -> fila 28)

# ===============================================================
# HOJA 5: INDICADORES
# ===============================================================
wi = wb.create_sheet("Indicadores")
wi.sheet_view.showGridLines = False
wi.merge_cells("A1:C1")
wi["A1"] = "INDICADORES DE RENTABILIDAD Y EVALUACION SOCIAL"
wi["A1"].font = f_titulo; wi["A1"].fill = fill_azul; wi["A1"].alignment = center
wi.row_dimensions[1].height = 26

FCp = f"'Flujos de Caja'!$H$3:$H${LAST}"
FCp0 = "'Flujos de Caja'!$H$3"
FCp1 = f"'Flujos de Caja'!$H$4:$H${LAST}"
FCi = f"'Flujos de Caja'!$J$3:$J${LAST}"
FCi0 = "'Flujos de Caja'!$J$3"
FCi1 = f"'Flujos de Caja'!$J$4:$J${LAST}"
FCs0 = "'Flujos de Caja'!$M$3"
FCs1 = f"'Flujos de Caja'!$M$4:$M${LAST}"
BEN1_25 = f"'Flujos de Caja'!$L$4:$L${LAST}"
OPEX1_25 = f"'Flujos de Caja'!$C$4:$C${LAST}"

ind = [
    ("Indicador", "Valor", "Criterio"),
    ("WACC", f"={WACC}", "Costo promedio de capital"),
    ("VPN Proyecto (@WACC)", f"={FCp0}+NPV({WACC},{FCp1})", "Si >0 crea valor (solo tarifas)"),
    ("TIR Proyecto", f"=IRR({FCp})", "Viable si > WACC"),
    ("VPN Inversionista (@Ke)", f"={FCi0}+NPV({KE},{FCi1})", "Si >0 atractivo"),
    ("TIR Inversionista", f"=IRR({FCi})", "Viable si > Ke"),
    ("VPN Social (@tasa social 9%)", f"={FCs0}+NPV({TSOC},{FCs1})", "Si >0 socialmente rentable"),
    ("Relacion Beneficio/Costo", f"=NPV({TSOC},{BEN1_25})/({CAPEX}+NPV({TSOC},{OPEX1_25}))", "Viable si > 1"),
]
r = 2
for row in ind:
    wi.cell(r, 1, row[0]); wi.cell(r, 2, row[1]); wi.cell(r, 3, row[2])
    if r == 2:
        for c in range(1, 4):
            wi.cell(r, c).font = f_hdr; wi.cell(r, c).fill = fill_azul; wi.cell(r, c).alignment = center
    else:
        wi.cell(r, 1).font = f_bold; wi.cell(r, 1).fill = fill_clar
        wi.cell(r, 3).alignment = left
        label = row[0]
        if "WACC" in label or "TIR" in label:
            wi.cell(r, 2).number_format = "0.00%"
        elif "Beneficio/Costo" in label:
            wi.cell(r, 2).number_format = "0.00"
        else:
            wi.cell(r, 2).number_format = "#,##0.0"
        wi.cell(r, 2).alignment = right
        wi.cell(r, 2).font = f_bold
    for c in range(1, 4):
        wi.cell(r, c).border = border
    r += 1
wi.column_dimensions["A"].width = 30
wi.column_dimensions["B"].width = 16
wi.column_dimensions["C"].width = 32

# ===============================================================
# HOJA 6: RIESGOS
# ===============================================================
wr = wb.create_sheet("Riesgos")
wr.sheet_view.showGridLines = False
wr.merge_cells("A1:G1")
wr["A1"] = "MATRIZ DE RIESGOS (20) - Nivel = P x I  [Bajo 1-6 / Medio 8-12 / Alto 15-25]"
wr["A1"].font = f_titulo; wr["A1"].fill = fill_azul; wr["A1"].alignment = center
wr.row_dimensions[1].height = 26
hdr = ["#", "Riesgo", "Tipo", "P", "I", "PxI", "Nivel"]
for j, h in enumerate(hdr, start=1):
    c = wr.cell(2, j, h); c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border
riesgos = [
    [1, "Crecientes/turbiedad extrema del rio San Juan", "Ambiental", 4, 5],
    [2, "Contaminacion por mineria ilegal (mercurio)", "Ambiental", 4, 5],
    [3, "Inundaciones que danan captacion/redes", "Ambiental", 4, 4],
    [4, "Deforestacion de la cuenca", "Ambiental", 3, 3],
    [5, "Vertimientos de aguas residuales a la fuente", "Ambiental", 3, 4],
    [6, "Resistencia comunitaria a micromedicion/tarifa", "Social", 3, 3],
    [7, "Baja cultura de pago y cartera morosa", "Social", 4, 3],
    [8, "Presencia de grupos armados (extorsion/retrasos)", "Seguridad", 4, 4],
    [9, "Demora en desembolsos de cofinanciacion", "Institucional", 4, 4],
    [10, "Debilidad del operador municipal", "Institucional", 3, 4],
    [11, "Sobrecostos por inflacion de insumos/transporte", "Financiero", 3, 3],
    [12, "Tarifa insuficiente para cubrir OPEX", "Financiero", 4, 3],
    [13, "Diseno hidraulico subdimensionado", "Tecnico", 2, 4],
    [14, "Fallas de equipos de bombeo", "Tecnico", 3, 3],
    [15, "Suministro electrico inestable", "Tecnico", 3, 4],
    [16, "Alto IANC por fugas no detectadas", "Operativo", 3, 3],
    [17, "Dificultad de acceso por mal estado de vias", "Logistico", 4, 3],
    [18, "Escasez de insumos quimicos (coagulantes)", "Ambiental", 2, 3],
    [19, "Demoras en predios/servidumbres", "Legal", 3, 3],
    [20, "Brote de EDA durante la transicion de obra", "Salud publica", 2, 4],
]
r = 3
for ri in riesgos:
    wr.cell(r, 1, ri[0]); wr.cell(r, 2, ri[1]); wr.cell(r, 3, ri[2])
    wr.cell(r, 4, ri[3]); wr.cell(r, 5, ri[4])
    wr.cell(r, 6, f"=D{r}*E{r}")
    wr.cell(r, 7, f'=IF(F{r}>=15,"Alto",IF(F{r}>=8,"Medio","Bajo"))')
    for j in range(1, 8):
        cell = wr.cell(r, j); cell.border = border
        cell.alignment = center if j != 2 else left
    r += 1
for col, w in zip("ABCDEFG", [5, 44, 14, 5, 5, 7, 9]):
    wr.column_dimensions[col].width = w

base = r + 2
wr.merge_cells(f"A{base}:H{base}")
wr.cell(base, 1, "INTERVENCION DE 10 RIESGOS (5 ambientales) Y RECALIFICACION RESIDUAL")
wr.cell(base, 1).font = f_titulo; wr.cell(base, 1).fill = fill_azul; wr.cell(base, 1).alignment = center
wr.row_dimensions[base].height = 26
hdr2 = ["#", "Riesgo", "Tipo", "Intervencion", "P res", "I res", "PxI res", "Nivel res"]
for j, h in enumerate(hdr2, start=1):
    c = wr.cell(base + 1, j, h); c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border
inter = [
    [1, "Turbiedad extrema del rio San Juan", "Ambiental", "Pretratamiento robusto + sedimentadores alta tasa + dosificacion automatica + tanque de regulacion", 2, 4],
    [2, "Contaminacion por mineria ilegal", "Ambiental", "Monitoreo de fuente + carbon activado + articulacion con CODECHOCO y control de mineria", 3, 3],
    [3, "Inundaciones que danan infraestructura", "Ambiental", "Captacion elevada/protegida + obras de proteccion de orillas + redes en cotas seguras", 2, 4],
    [5, "Vertimientos a la fuente", "Ambiental", "Optimizacion de alcantarillado + campanas + coordinacion municipal", 2, 3],
    [4, "Deforestacion de la cuenca", "Ambiental", "Pago por servicios ambientales + reforestacion de microcuenca con la comunidad", 2, 2],
    [8, "Grupos armados / inseguridad", "Seguridad", "Plan de seguridad de obra + articulacion con autoridades + contratacion local", 2, 4],
    [9, "Demora en desembolsos", "Institucional", "Convenio con desembolsos por hitos + anticipo + fiducia", 2, 4],
    [7, "Baja cultura de pago", "Social", "Subsidios focalizados + educacion + tarifa social + facturacion clara", 2, 3],
    [12, "Tarifa insuficiente", "Financiero", "Estudio tarifario CRA + subsidios cruzados + aporte SGP", 2, 3],
    [15, "Suministro electrico inestable", "Tecnico", "Planta electrica de respaldo + almacenamiento con autonomia", 2, 3],
]
r = base + 2
for it in inter:
    wr.cell(r, 1, it[0]); wr.cell(r, 2, it[1]); wr.cell(r, 3, it[2]); wr.cell(r, 4, it[3])
    wr.cell(r, 5, it[4]); wr.cell(r, 6, it[5])
    wr.cell(r, 7, f"=E{r}*F{r}")
    wr.cell(r, 8, f'=IF(G{r}>=15,"Alto",IF(G{r}>=8,"Medio","Bajo"))')
    for j in range(1, 9):
        cell = wr.cell(r, j); cell.border = border
        cell.alignment = center if j not in (2, 4) else left
    r += 1
wr.column_dimensions["D"].width = 55
wr.column_dimensions["H"].width = 10

wb.save("MODELO FINANCIERO PEPI.xlsx")
print("OK -> MODELO FINANCIERO PEPI.xlsx")

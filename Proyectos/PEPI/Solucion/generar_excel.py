# -*- coding: utf-8 -*-
"""
Genera el modelo financiero completo del Proyecto PEPI en Excel (.xlsx) CON FORMULAS VIVAS.
Hojas:
  1. Supuestos          -> parametros de entrada (editables)
  2. Amortizacion Deuda -> tabla de amortizacion (sistema frances)
  3. Flujos de Caja     -> ingresos, OPEX, EBITDA, EBIT, impuestos, FCLP, FCLA, FC Banco
  4. Indicadores        -> WACC, VPN y TIR (proyecto e inversionista) con funciones NPV/IRR
  5. Riesgos            -> matriz de 20 riesgos + intervencion/recalificacion de 10

Al abrir el archivo en Excel/LibreOffice/Google Sheets, todas las celdas con formula
se recalculan automaticamente si cambias los Supuestos.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

AZUL = "1F4E79"
AZUL_CLARO = "D6E4F0"
GRIS = "F2F2F2"
VERDE = "E2EFDA"
ROJO = "F8CBAD"
AMAR = "FFE699"

f_titulo = Font(bold=True, color="FFFFFF", size=12)
f_hdr = Font(bold=True, color="FFFFFF", size=10)
f_bold = Font(bold=True)
fill_azul = PatternFill("solid", fgColor=AZUL)
fill_clar = PatternFill("solid", fgColor=AZUL_CLARO)
fill_gris = PatternFill("solid", fgColor=GRIS)
fill_verde = PatternFill("solid", fgColor=VERDE)
fill_rojo = PatternFill("solid", fgColor=ROJO)
fill_amar = PatternFill("solid", fgColor=AMAR)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)
right = Alignment(horizontal="right", vertical="center")
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

# ===============================================================
# HOJA 1: SUPUESTOS
# ===============================================================
ws = wb.active
ws.title = "Supuestos"
ws.sheet_view.showGridLines = False
ws.merge_cells("A1:C1")
ws["A1"] = "SUPUESTOS DEL MODELO - PROYECTO PEPI (PTAP + ACUEDUCTO EL PROGRESO)"
ws["A1"].font = f_titulo
ws["A1"].fill = fill_azul
ws["A1"].alignment = center
ws.row_dimensions[1].height = 28

ws["A2"] = "Cifras en COP millones (salvo %)"
ws["A2"].font = Font(italic=True, size=9)

# (etiqueta, valor, nombre_celda_referencia, formato)
sup = [
    ("Parametro", "Valor", "Unidad"),
    ("CAPEX total", 14000, "COP MM"),
    ("% Deuda", 0.60, "%"),
    ("% Equity", 0.40, "%"),
    ("Deuda", "=B4*B5", "COP MM"),
    ("Equity", "=B4*B6", "COP MM"),
    ("Kd (costo deuda)", 0.125, "%"),
    ("Ke (costo equity)", 0.155, "%"),
    ("Tasa de impuestos", 0.35, "%"),
    ("Plazo de la deuda", 10, "anios"),
    ("Horizonte de evaluacion", 20, "anios"),
    ("Ingreso anio 1", 5200, "COP MM"),
    ("Crecimiento ingresos", 0.045, "%"),
    ("OPEX anio 1", 2350, "COP MM"),
    ("Crecimiento OPEX", 0.04, "%"),
    ("Depreciacion anual", "=B4/B13", "COP MM"),
    ("Cuota anual deuda (frances)", "=B7*B9/(1-(1+B9)^(-B12))", "COP MM"),
    ("WACC", "=B6*B10+B5*B9*(1-B11)", "%"),
]
r = 3
for row in sup:
    ws.cell(r, 1, row[0])
    ws.cell(r, 2, row[1])
    ws.cell(r, 3, row[2])
    if r == 3:
        for c in range(1, 4):
            ws.cell(r, c).font = f_hdr
            ws.cell(r, c).fill = fill_azul
            ws.cell(r, c).alignment = center
    else:
        ws.cell(r, 1).font = f_bold
        ws.cell(r, 1).fill = fill_clar
        # formato porcentaje o numero
        if row[2] == "%":
            ws.cell(r, 2).number_format = "0.00%"
        else:
            ws.cell(r, 2).number_format = "#,##0.0"
        ws.cell(r, 2).alignment = right
        ws.cell(r, 3).alignment = center
    for c in range(1, 4):
        ws.cell(r, c).border = border
    r += 1
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 12

# Referencias utiles (nombres de celda en hoja Supuestos)
S = "Supuestos!"
CAPEX = f"{S}$B$4"
DEUDA = f"{S}$B$7"
EQUITY = f"{S}$B$8"
KD = f"{S}$B$9"
KE = f"{S}$B$10"
IMP = f"{S}$B$11"
PLAZO = f"{S}$B$12"
HOR = f"{S}$B$13"
ING1 = f"{S}$B$14"
CRECI = f"{S}$B$15"
OPEX1 = f"{S}$B$16"
CRECO = f"{S}$B$17"
DEP = f"{S}$B$18"
CUOTA = f"{S}$B$19"
WACC = f"{S}$B$20"

# ===============================================================
# HOJA 2: AMORTIZACION DEUDA
# ===============================================================
wa = wb.create_sheet("Amortizacion Deuda")
wa.sheet_view.showGridLines = False
wa.merge_cells("A1:F1")
wa["A1"] = "TABLA DE AMORTIZACION DE LA DEUDA (Sistema Frances - cuota fija)"
wa["A1"].font = f_titulo
wa["A1"].fill = fill_azul
wa["A1"].alignment = center
wa.row_dimensions[1].height = 26
hdr = ["Anio", "Saldo inicial", "Interes", "Abono capital", "Cuota", "Saldo final"]
for j, h in enumerate(hdr, start=1):
    c = wa.cell(2, j, h)
    c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border
# fila 1 -> fila 3
HOR_N = 20
for t in range(1, HOR_N + 1):
    row = t + 2  # anio t en fila t+2
    wa.cell(row, 1, t)
    # saldo inicial: si t==1 -> Deuda; si no -> saldo final fila anterior
    if t == 1:
        wa.cell(row, 2, f"={DEUDA}")
    else:
        wa.cell(row, 2, f"=F{row-1}")
    # interes = saldo_ini * Kd  (solo si t<=plazo)
    wa.cell(row, 3, f"=IF(A{row}<={PLAZO},B{row}*{KD},0)")
    # cuota fija (solo si t<=plazo)
    wa.cell(row, 5, f"=IF(A{row}<={PLAZO},{CUOTA},0)")
    # abono = cuota - interes
    wa.cell(row, 4, f"=E{row}-C{row}")
    # saldo final = saldo ini - abono
    wa.cell(row, 6, f"=B{row}-D{row}")
    for j in range(1, 7):
        cell = wa.cell(row, j)
        cell.border = border
        if j == 1:
            cell.alignment = center
        else:
            cell.number_format = "#,##0.0"
            cell.alignment = right
    if t % 2 == 0:
        for j in range(1, 7):
            wa.cell(row, j).fill = fill_gris
for col, w in zip("ABCDEF", [8, 16, 14, 16, 14, 16]):
    wa.column_dimensions[col].width = w

# ===============================================================
# HOJA 3: FLUJOS DE CAJA
# ===============================================================
wf = wb.create_sheet("Flujos de Caja")
wf.sheet_view.showGridLines = False
wf.merge_cells("A1:K1")
wf["A1"] = "FLUJOS DE CAJA - PROYECTO, INVERSIONISTA Y BANCO (COP MM)"
wf["A1"].font = f_titulo
wf["A1"].fill = fill_azul
wf["A1"].alignment = center
wf.row_dimensions[1].height = 26
hdr = ["Anio", "Ingresos", "OPEX", "EBITDA", "Deprec.", "EBIT",
       "Intereses", "FC Proyecto", "Util. neta", "FC Inversionista", "FC Banco"]
for j, h in enumerate(hdr, start=1):
    c = wf.cell(2, j, h)
    c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border

# Fila anio 0 (fila 3)
wf.cell(3, 1, 0)
wf.cell(3, 8, f"=-{CAPEX}")          # FC Proyecto
wf.cell(3, 10, f"=-{EQUITY}")        # FC Inversionista
wf.cell(3, 11, f"={DEUDA}")          # FC Banco (desembolso)
for j in range(1, 12):
    wf.cell(3, j).border = border
    if j == 1:
        wf.cell(3, j).alignment = center
    else:
        wf.cell(3, j).number_format = "#,##0.0"
        wf.cell(3, j).alignment = right

# Anios 1..20 (filas 4..23). anio t en fila t+3.
AM = "'Amortizacion Deuda'!"
for t in range(1, HOR_N + 1):
    row = t + 3
    am_row = t + 2  # fila correspondiente en hoja amortizacion
    wf.cell(row, 1, t)
    # Ingresos = ING1 * (1+crec)^(t-1)
    wf.cell(row, 2, f"={ING1}*(1+{CRECI})^(A{row}-1)")
    # OPEX
    wf.cell(row, 3, f"={OPEX1}*(1+{CRECO})^(A{row}-1)")
    # EBITDA = ing - opex
    wf.cell(row, 4, f"=B{row}-C{row}")
    # Depreciacion
    wf.cell(row, 5, f"={DEP}")
    # EBIT = EBITDA - Deprec
    wf.cell(row, 6, f"=D{row}-E{row}")
    # Intereses (de hoja amortizacion)
    wf.cell(row, 7, f"={AM}C{am_row}")
    # FC Proyecto = EBIT*(1-imp) + Deprec
    wf.cell(row, 8, f"=F{row}*(1-{IMP})+E{row}")
    # Utilidad neta = (EBIT - intereses)*(1-imp)  [escudo fiscal]
    wf.cell(row, 9, f"=(F{row}-G{row})*(1-{IMP})")
    # FC Inversionista = Util neta + Deprec - Abono capital
    wf.cell(row, 10, f"=I{row}+E{row}-{AM}D{am_row}")
    # FC Banco = -(cuota) = -(interes+abono)
    wf.cell(row, 11, f"=-{AM}E{am_row}")
    for j in range(1, 12):
        cell = wf.cell(row, j)
        cell.border = border
        if j == 1:
            cell.alignment = center
        else:
            cell.number_format = "#,##0.0"
            cell.alignment = right
    if t % 2 == 0:
        for j in range(1, 12):
            wf.cell(row, j).fill = fill_gris
for col, w in zip("ABCDEFGHIJK", [7, 11, 10, 11, 10, 11, 11, 13, 11, 15, 12]):
    wf.column_dimensions[col].width = w

# ===============================================================
# HOJA 4: INDICADORES
# ===============================================================
wi = wb.create_sheet("Indicadores")
wi.sheet_view.showGridLines = False
wi.merge_cells("A1:C1")
wi["A1"] = "INDICADORES DE RENTABILIDAD"
wi["A1"].font = f_titulo
wi["A1"].fill = fill_azul
wi["A1"].alignment = center
wi.row_dimensions[1].height = 26

FCp = "'Flujos de Caja'!$H$3:$H$23"   # FC Proyecto anios 0..20
FCi = "'Flujos de Caja'!$J$3:$J$23"   # FC Inversionista anios 0..20
FCp0 = "'Flujos de Caja'!$H$3"
FCp1_20 = "'Flujos de Caja'!$H$4:$H$23"
FCi0 = "'Flujos de Caja'!$J$3"
FCi1_20 = "'Flujos de Caja'!$J$4:$J$23"

ind = [
    ("Indicador", "Valor", "Criterio"),
    ("WACC", f"={WACC}", "Costo promedio de capital"),
    ("VPN Proyecto (@WACC)", f"={FCp0}+NPV({WACC},{FCp1_20})", "Si >0 crea valor"),
    ("TIR Proyecto", f"=IRR({FCp})", "Viable si > WACC"),
    ("VPN Inversionista (@Ke)", f"={FCi0}+NPV({KE},{FCi1_20})", "Si >0 atractivo"),
    ("TIR Inversionista", f"=IRR({FCi})", "Viable si > Ke"),
]
r = 2
for row in ind:
    wi.cell(r, 1, row[0]); wi.cell(r, 2, row[1]); wi.cell(r, 3, row[2])
    if r == 2:
        for c in range(1, 4):
            wi.cell(r, c).font = f_hdr; wi.cell(r, c).fill = fill_azul
            wi.cell(r, c).alignment = center
    else:
        wi.cell(r, 1).font = f_bold; wi.cell(r, 1).fill = fill_clar
        wi.cell(r, 3).alignment = left
        label = row[0]
        if "WACC" in label or "TIR" in label:
            wi.cell(r, 2).number_format = "0.00%"
        else:
            wi.cell(r, 2).number_format = "#,##0.0"
        wi.cell(r, 2).alignment = right
        wi.cell(r, 2).font = f_bold
    for c in range(1, 4):
        wi.cell(r, c).border = border
    r += 1
wi.column_dimensions["A"].width = 26
wi.column_dimensions["B"].width = 16
wi.column_dimensions["C"].width = 28

# ===============================================================
# HOJA 5: RIESGOS
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
    [1, "Sobrecostos en la construccion", "Financiero", 4, 4],
    [2, "Retrasos en el cronograma de obra", "Operativo", 4, 3],
    [3, "Demoras en gestion predial y servidumbres", "Legal", 3, 4],
    [4, "Variacion en la tasa de cambio", "Financiero", 3, 3],
    [5, "Incremento de tasas de interes", "Financiero", 3, 4],
    [6, "Recaudo tarifario inferior al proyectado", "Comercial", 4, 4],
    [7, "Cambios regulatorios en marco tarifario", "Regulatorio", 2, 4],
    [8, "Contaminacion de la fuente de captacion", "Ambiental", 3, 5],
    [9, "Reduccion del caudal (sequia/clima)", "Ambiental", 3, 5],
    [10, "Inadecuada disposicion de lodos PTAP", "Ambiental", 3, 4],
    [11, "Vertimiento de aguas de lavado sin tratar", "Ambiental", 3, 4],
    [12, "Afectacion de fauna/flora en obras", "Ambiental", 2, 3],
    [13, "Fallas o paradas de equipos de bombeo", "Operativo", 3, 3],
    [14, "Interrupcion del suministro electrico", "Operativo", 3, 4],
    [15, "Accidentes laborales en obra", "SST", 3, 4],
    [16, "Oposicion o conflicto con la comunidad", "Social", 3, 3],
    [17, "Vandalismo o robo de infraestructura", "Seguridad", 3, 2],
    [18, "Errores en estudios y disenios tecnicos", "Tecnico", 2, 4],
    [19, "Incumplimiento del contratista", "Contractual", 2, 4],
    [20, "Inflacion de costos operativos", "Financiero", 3, 3],
]
r = 3
for ri in riesgos:
    wr.cell(r, 1, ri[0]); wr.cell(r, 2, ri[1]); wr.cell(r, 3, ri[2])
    wr.cell(r, 4, ri[3]); wr.cell(r, 5, ri[4])
    wr.cell(r, 6, f"=D{r}*E{r}")  # PxI
    # Nivel segun PxI
    wr.cell(r, 7, f'=IF(F{r}>=15,"Alto",IF(F{r}>=8,"Medio","Bajo"))')
    for j in range(1, 8):
        cell = wr.cell(r, j); cell.border = border
        cell.alignment = center if j != 2 else left
    r += 1
for col, w in zip("ABCDEFG", [5, 40, 13, 5, 5, 7, 9]):
    wr.column_dimensions[col].width = w

# Bloque intervencion / recalificacion
base = r + 2
wr.merge_cells(f"A{base}:H{base}")
wr.cell(base, 1, "INTERVENCION DE 10 RIESGOS (5 ambientales) Y RECALIFICACION RESIDUAL")
wr.cell(base, 1).font = f_titulo; wr.cell(base, 1).fill = fill_azul; wr.cell(base, 1).alignment = center
wr.row_dimensions[base].height = 26
hdr2 = ["#", "Riesgo", "Tipo", "Intervencion", "P res", "I res", "PxI res", "Nivel res"]
for j, h in enumerate(hdr2, start=1):
    c = wr.cell(base + 1, j, h); c.font = f_hdr; c.fill = fill_azul; c.alignment = center; c.border = border
inter = [
    [1, "Sobrecostos de construccion", "Financiero", "Contrato EPC precio fijo + contingencia 10% + control de cambios", 2, 3],
    [6, "Bajo recaudo tarifario", "Comercial", "Cultura de pago, financiacion de cartera, corte por mora, micromedicion", 2, 3],
    [5, "Alza de tasas de interes", "Financiero", "Cobertura con tasa fija / SWAP en cierre financiero", 1, 3],
    [8, "Contaminacion de la fuente", "Ambiental", "Reforestacion ronda hidrica, monitoreo de calidad, barreras de captacion", 2, 4],
    [9, "Reduccion de caudal (sequia)", "Ambiental", "Fuente alterna, tanques de regulacion, PUEAA y reuso", 2, 4],
    [10, "Disposicion de lodos", "Ambiental", "Lechos de secado, disposicion autorizada, aprovechamiento agricola", 1, 3],
    [11, "Vertimiento aguas de lavado", "Ambiental", "Recirculacion y tratamiento previo, permiso ambiental (CAR)", 1, 3],
    [12, "Afectacion fauna/flora", "Ambiental", "Plan de Manejo Ambiental, compensacion forestal", 1, 2],
    [14, "Interrupcion electrica", "Operativo", "Grupo electrogeno de respaldo y energia dual", 1, 4],
    [15, "Accidentes laborales", "SST", "SG-SST (Dec 1072), capacitacion, EPP, permisos trabajo de alto riesgo", 1, 4],
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
wr.column_dimensions["D"].width = 52
wr.column_dimensions["H"].width = 10

wb.save("MODELO FINANCIERO PEPI.xlsx")
print("OK -> MODELO FINANCIERO PEPI.xlsx")

# -*- coding: utf-8 -*-
"""Genera PROPUESTA_ECONOMICA.xlsx (oferta, APU, mano de obra, programa y cronograma)
y SIMULADOR_CALIFICACION.xlsx."""
import sys
from decimal import Decimal
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.page import PageMargins
import datos as D

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

thin = Side(style="thin", color="000000")
B = Border(left=thin, right=thin, top=thin, bottom=thin)
BOLD = Font(bold=True)
H_FILL = PatternFill("solid", fgColor="1F4E78")
H_FONT = Font(bold=True, color="FFFFFF")
CAP_FILL = PatternFill("solid", fgColor="D9E1F2")
TOT_FILL = PatternFill("solid", fgColor="FFF2CC")
BAR_FILL = PatternFill("solid", fgColor="2E75B6")
IN_FILL = PatternFill("solid", fgColor="E2EFDA")
NUM = '#,##0'
NUM2 = '#,##0.00'
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
WRAP = Alignment(vertical="center", wrap_text=True)


def hdr(ws, row, values, widths=None):
    for j, v in enumerate(values, 1):
        c = ws.cell(row, j, v)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, B
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[L(j)].width = w


def encabezado(ws, titulo, ncols):
    lines = [D.ENTIDAD, D.LICITACION, "OBJETO: " + D.OBJETO, "PROPONENTE: " + D.PROPONENTE, titulo]
    for i, t in enumerate(lines, 1):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=ncols)
        c = ws.cell(i, 1, t)
        c.alignment = CENTER
        c.font = Font(bold=True, size=12 if i in (1, 5) else 10)
    ws.row_dimensions[3].height = 30


def imprimir(ws, landscape=False, fit_height=0):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = fit_height
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.5, bottom=0.5)
    ws.print_options.horizontalCentered = True


def firma(ws, row, ncols):
    ws.cell(row + 2, 2, "_______________________________________")
    ws.cell(row + 3, 2, D.REPRESENTANTE).font = BOLD
    ws.cell(row + 4, 2, "Representante legal – " + D.PROPONENTE)
    ws.cell(row + 5, 2, D.CEDULA_REP)


wb = Workbook()

# ===================================================================== MANO DE OBRA
mo = wb.active
mo.title = "MANO DE OBRA"
encabezado(mo, f"CÁLCULO DEL COSTO HORA DE MANO DE OBRA – {D.ANIO}", 4)
r = 7
mo.cell(r, 1, f"Salario mínimo {D.ANIO} (SMMLV)"); mo.cell(r, 3, D.SMMLV).number_format = NUM
mo.cell(r, 4, D.DEC_SMMLV)
mo.cell(r + 1, 1, f"Auxilio de transporte {D.ANIO}"); mo.cell(r + 1, 3, D.AUX_TRANSPORTE).number_format = NUM
mo.cell(r + 1, 4, D.DEC_AUX)
mo.cell(r + 2, 1, f"Horas laborables por mes ({D.HORAS_SEMANA} h/sem × 52 / 12)")
mo.cell(r + 2, 3, f"={D.HORAS_SEMANA}*52/12").number_format = NUM2
mo.cell(r + 2, 4, "Ley 2101 de 2021")
R_SMMLV, R_AUX, R_HMES = r, r + 1, r + 2
r += 4
hdr(mo, r, ["PRESTACIONES Y APORTES DEL EMPLEADOR", "", "% sobre salario", ""], [44, 4, 18, 30])
p0 = r + 1
for k, (n, p) in enumerate(D.PRESTACIONES):
    mo.cell(p0 + k, 1, n).border = B
    c = mo.cell(p0 + k, 3, float(p)); c.number_format = '0.00%'; c.border = B
pf = p0 + len(D.PRESTACIONES)
mo.cell(pf, 1, "FACTOR PRESTACIONAL TOTAL").font = BOLD
c = mo.cell(pf, 3, f"=SUM(C{p0}:C{pf-1})"); c.number_format = '0.00%'; c.font = BOLD; c.fill = TOT_FILL
mo.cell(pf + 1, 1, "Factor sobre auxilio de transporte (cesantías + intereses + prima)")
c = mo.cell(pf + 1, 3, float(D.AUX_FACTOR)); c.number_format = '0.0000'
R_PF, R_AF = pf, pf + 1
r = pf + 3
hdr(mo, r, ["CARGO", "× SMMLV", "COSTO MENSUAL", "COSTO HORA"])
filas_cargo = {}
for k, (n, m) in enumerate(D.CARGOS):
    rr = r + 1 + k
    mo.cell(rr, 1, n).border = B
    mo.cell(rr, 2, float(m)).border = B
    c = mo.cell(rr, 3, f"=$C${R_SMMLV}*B{rr}*(1+$C${R_PF})+$C${R_AUX}*$C${R_AF}")
    c.number_format = NUM; c.border = B
    c = mo.cell(rr, 4, f"=C{rr}/$C${R_HMES}"); c.number_format = NUM; c.border = B
    filas_cargo[n] = rr
ra, rof = filas_cargo["Ayudante (obrero)"], filas_cargo["Oficial"]
r = rr + 2
hdr(mo, r, ["CUADRILLA", "", "", "COSTO HORA-CUADRILLA (hc)"])
CUAD_REF = {}
for k, (key, (n, _)) in enumerate(D.CUADRILLAS.items()):
    rr = r + 1 + k
    nay = {"C11": 1, "C12": 2, "C13": 3}[key]
    mo.cell(rr, 1, n).border = B
    c = mo.cell(rr, 4, f"=D{rof}+{nay}*D{ra}"); c.number_format = NUM; c.border = B; c.font = BOLD
    CUAD_REF[key] = f"'MANO DE OBRA'!$D${rr}"
imprimir(mo)

# ===================================================================== APU
APU_REF = {}
for cod, a in D.APUS.items():
    ws = wb.create_sheet(f"APU {cod}")
    encabezado(ws, "ANÁLISIS DE PRECIO UNITARIO (APU)", 6)
    hdr(ws, 7, ["ÍTEM", "DESCRIPCIÓN", "", "", "UNIDAD", ""], [30, 16, 11, 12, 15, 16])
    ws.merge_cells("B7:D7")
    ws.cell(8, 1, cod).alignment = CENTER
    ws.merge_cells("B8:D8")
    ws.cell(8, 2, a["titulo"]).alignment = WRAP
    ws.cell(8, 5, a["und"]).alignment = CENTER
    for j in range(1, 7):
        ws.cell(8, j).border = B
    ws.row_dimensions[8].height = 30
    r = 10
    filas, total, precio = D.calc_apu(cod)
    sub_rows = {}
    mo_sub_ref = None
    pending_h = []
    for g, gname in D.GRUPOS:
        recs = [x for x in a["rec"] if x[0] == g or (g == "E" and x[0] == "H")]
        if not recs:
            continue
        ws.cell(r, 1, gname).font = BOLD
        ws.cell(r, 1).fill = CAP_FILL
        for j in range(1, 7):
            ws.cell(r, j).fill = CAP_FILL
        r += 1
        hdr(ws, r, ["Descripción", "Unidad", "Cantidad", "Desperdicio", "V. Unitario", "V. Parcial"])
        r += 1
        r0 = r
        for gg, d, u, q, w, vu in recs:
            ws.cell(r, 1, d).alignment = WRAP
            ws.cell(r, 2, u).alignment = CENTER
            ws.cell(r, 3, q).number_format = '0.000'
            c = ws.cell(r, 4, w); c.number_format = '0%'
            if gg == "O":
                ws.cell(r, 5, "=" + CUAD_REF[vu])
            elif gg == "H":
                pending_h.append(r)
            else:
                ws.cell(r, 5, vu)
            ws.cell(r, 5).number_format = NUM
            c = ws.cell(r, 6, f"=C{r}*(1+D{r})*E{r}"); c.number_format = NUM
            for j in range(1, 7):
                ws.cell(r, j).border = B
            ws.row_dimensions[r].height = 28
            r += 1
        ws.cell(r, 5, "Subtotal").font = BOLD
        c = ws.cell(r, 6, f"=SUM(F{r0}:F{r-1})"); c.number_format = NUM; c.font = BOLD
        sub_rows[g] = r
        if g == "O":
            mo_sub_ref = f"F{r}"
        r += 2
    for hr in pending_h:
        ws.cell(hr, 5, "=" + mo_sub_ref).number_format = NUM
    ws.cell(r, 1, "COSTO DIRECTO TOTAL DEL APU").font = BOLD
    c = ws.cell(r, 6, "=" + "+".join(f"F{x}" for x in sub_rows.values()))
    c.number_format = NUM2; c.font = BOLD; c.fill = TOT_FILL
    r += 1
    ws.cell(r, 1, "PRECIO UNITARIO ADOPTADO (ajustado al peso)").font = BOLD
    c = ws.cell(r, 6, f"=ROUND(F{r-1},0)"); c.number_format = NUM; c.font = Font(bold=True, size=12)
    c.fill = TOT_FILL; c.border = B
    APU_REF[cod] = f"'APU {cod}'!$F${r}"
    r += 2
    ws.cell(r, 1, "Notas: " + a["nota"] + " El precio no incluye AIU; la Administración, los Imprevistos "
            "y la Utilidad se aplican sobre el costo directo total de la oferta.").alignment = WRAP
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    ws.row_dimensions[r].height = 58
    firma(ws, r + 1, 6)
    imprimir(ws, fit_height=1)

# ===================================================================== AJUSTE (hoja de trabajo)
aj = wb.create_sheet("AJUSTE", 0)
aj["A1"] = "HOJA DE TRABAJO – NO SE IMPRIME NI SE ENTREGA"
aj["A1"].font = Font(bold=True, size=13, color="C00000")
aj["A3"] = "Presupuesto oficial"; aj["C3"] = D.PRESUPUESTO_OFICIAL; aj["C3"].number_format = NUM
aj["A4"] = "FACTOR sobre precios del formato (cambie esta celda)"
aj["C4"] = float(D.FACTOR); aj["C4"].fill = IN_FILL; aj["C4"].font = Font(bold=True, size=12)
aj["C4"].number_format = '0.0000'
aj["A5"] = "Valor total de la oferta"; aj["C5"] = "=OFERTA!F_TOTAL"
aj["A6"] = "% del presupuesto oficial"; aj["C6"] = "=C5/C3"; aj["C6"].number_format = '0.000%'
aj["A7"] = "¿Dentro del rango 90 %–100 %?"; aj["C7"] = '=IF(AND(C6>=0.9,C6<=1),"SÍ","NO – SE RECHAZA")'
aj["A8"] = "Mínimo (90 %)"; aj["C8"] = "=ROUND(C3*0.9,0)"; aj["C8"].number_format = NUM
aj["A9"] = ("Los ítems 3.06, 4.05, 7.01 y 12.02 toman el precio de su APU y no cambian con el factor. "
            "Los demás = ROUND(precio del formato × factor; 0).")
aj.column_dimensions["A"].width = 52
aj.column_dimensions["B"].width = 12
aj.column_dimensions["C"].width = 18
hdr(aj, 11, ["Ítem", "Código", "Precio formato"])
BASE_REF = {}
for k, (_, cod, desc, und, q, vu) in enumerate(D.ITEMS):
    rr = 12 + k
    aj.cell(rr, 1, desc[:60]); aj.cell(rr, 2, cod)
    aj.cell(rr, 3, vu).number_format = NUM
    BASE_REF[cod] = f"AJUSTE!$C${rr}"

# ===================================================================== OFERTA
of = wb.create_sheet("OFERTA", 1)
encabezado(of, "ANEXO 4 – FORMATO DE CANTIDADES Y PRESUPUESTO – OFERTA ECONÓMICA (SOBRE No. 2)", 6)
hdr(of, 7, ["COD.", "ITEM", "UNIDAD", "CANTIDAD", "VR. UNITARIO", "VR. TOTAL"], [8, 58, 9, 11, 15, 17])
r = 8
ROW_OF = {}
first = r
for f in D.FORMATO:
    if f[0] == "cap":
        of.cell(r, 1, f[1] + ".").font = BOLD
        of.cell(r, 2, f[2]).font = BOLD
        for j in range(1, 7):
            of.cell(r, j).fill = CAP_FILL; of.cell(r, j).border = B
    else:
        _, cod, desc, und, q, vu = f
        of.cell(r, 1, cod)
        of.cell(r, 2, desc).alignment = WRAP
        of.cell(r, 3, und).alignment = CENTER
        of.cell(r, 4, q).number_format = '#,##0.00'
        if cod in APU_REF:
            of.cell(r, 5, "=" + APU_REF[cod])
        else:
            of.cell(r, 5, f"=ROUND({BASE_REF[cod]}*AJUSTE!$C$4,0)")
        of.cell(r, 5).number_format = NUM
        of.cell(r, 6, f"=ROUND(D{r}*E{r},0)").number_format = NUM
        for j in range(1, 7):
            of.cell(r, j).border = B
        ROW_OF[cod] = r
        if len(desc) > 60:
            of.row_dimensions[r].height = 15 * (len(desc) // 58 + 1)
    r += 1
last = r - 1
r += 1
of.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
of.cell(r, 2, "VALOR TOTAL COSTO DIRECTO").font = BOLD
of.cell(r, 2).alignment = Alignment(horizontal="right")
c = of.cell(r, 6, f"=SUM(F{first}:F{last})"); c.number_format = NUM; c.font = BOLD; c.fill = TOT_FILL
R_CD = r
r += 2
hdr(of, r, ["", "COSTOS INDIRECTOS – DESCRIPCIÓN", "", "", "PORCENTAJE", "VR. TOTAL"])
aiu = [("A", "Administración", D.A_PCT), ("I", "Imprevistos", D.I_PCT), ("U", "Utilidad", D.U_PCT)]
for k, (s, n, p) in enumerate(aiu):
    rr = r + 1 + k
    of.cell(rr, 1, s).alignment = CENTER
    of.cell(rr, 2, n)
    c = of.cell(rr, 5, float(p)); c.number_format = '0.00%'
    c = of.cell(rr, 6, f"=ROUND($F${R_CD}*E{rr},0)"); c.number_format = NUM
    for j in range(1, 7):
        of.cell(rr, j).border = B
r = rr + 1
of.cell(r, 2, "VALOR TOTAL COSTO INDIRECTO").font = BOLD
c = of.cell(r, 5, f"=SUM(E{r-3}:E{r-1})"); c.number_format = '0.00%'
c = of.cell(r, 6, f"=SUM(F{r-3}:F{r-1})"); c.number_format = NUM; c.font = BOLD
R_CI = r
r += 2
of.cell(r, 2, "VALOR TOTAL DE LA PROPUESTA").font = Font(bold=True, size=12)
c = of.cell(r, 6, f"=F{R_CD}+F{R_CI}"); c.number_format = NUM
c.font = Font(bold=True, size=12); c.fill = TOT_FILL; c.border = B
R_TOT = r
r += 1
of.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
of.cell(r, 1, "SON: " + D.letras(D.TOTAL) + " PESOS M/CTE.").alignment = WRAP
of.cell(r, 1).font = BOLD
of.row_dimensions[r].height = 30
r += 1
of.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
of.cell(r, 1, "Precios ajustados al peso. Cantidades y unidades del formato oficial sin modificación. "
        "Los precios unitarios cubren materiales, mano de obra, prestaciones, herramienta, equipo y "
        "transporte. Los impuestos, contribuciones, personal directivo, señalización, seguridad y "
        "limpieza están incluidos en el AIU (numerales 3.2.1, 3.2.1.1, 6.1, 6.10, 6.12 y 6.13 de los TR). "
        "Precios fijos sin ajuste durante el plazo.").alignment = WRAP
of.cell(r, 1).font = Font(size=8, italic=True)
of.row_dimensions[r].height = 45
firma(of, r, 6)
of.print_title_rows = "7:7"
imprimir(of)
aj["C5"] = f"=OFERTA!F{R_TOT}"

# ===================================================================== PROGRAMA (ANEXO 6)
pg = wb.create_sheet("ANEXO 6 PROGRAMA")
encabezado(pg, "ANEXO 6 – FORMATO PROGRAMACIÓN DE OBRA", 9)
hdr(pg, 7, ["Ítem", "Actividad", "Unidad", "Cantidad", "Duración (días)", "Costo actividad",
            "Inicio (día)", "Fin (día)", "Personal y equipo"], [7, 44, 7, 10, 10, 15, 9, 9, 46])
r = 8
ROW_PG = {}
for f in D.FORMATO:
    if f[0] == "cap":
        pg.cell(r, 1, f[1] + ".").font = BOLD
        pg.cell(r, 2, f[2]).font = BOLD
        for j in range(1, 10):
            pg.cell(r, j).fill = CAP_FILL; pg.cell(r, j).border = B
    else:
        _, cod, desc, und, q, vu = f
        ini, dur, pers = D.PROG[cod]
        vals = [cod, desc, und, q, dur, f"=OFERTA!F{ROW_OF[cod]}", ini, f"=G{r}+E{r}-1", pers]
        for j, v in enumerate(vals, 1):
            c = pg.cell(r, j, v); c.border = B
            c.alignment = WRAP if j in (2, 9) else CENTER
        pg.cell(r, 4).number_format = '#,##0.00'
        pg.cell(r, 6).number_format = NUM
        ROW_PG[cod] = r
        pg.row_dimensions[r].height = 26 if max(len(desc), len(pers)) > 45 else 15
    r += 1
r += 1
pg.cell(r, 2, "COSTO DIRECTO TOTAL").font = BOLD
c = pg.cell(r, 6, f"=SUM(F8:F{r-2})"); c.number_format = NUM; c.font = BOLD
r += 2
textos = [
    f"a. Secuencia y duración: ver columnas Inicio, Duración y Fin de cada actividad del presupuesto oficial.",
    f"b. Inicio y fin: expresados en días calendario contados desde el día 1 = fecha del acta de inicio.",
    f"c. Duración total del proyecto: 5 MESES. Cronograma de 21 semanas = 147 días calendario; "
    f"los 3 días restantes del plazo (150 días) se destinan a la entrega de la obra al Municipio (Anexo 7).",
    "d. Jornada de trabajo: " + D.JORNADA,
]
for t in textos:
    pg.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
    pg.cell(r, 1, t).alignment = WRAP
    pg.row_dimensions[r].height = 30
    r += 1
firma(pg, r, 9)
pg.print_title_rows = "7:7"
imprimir(pg, landscape=True)

# ===================================================================== CRONOGRAMA (ANEXO 7)
cr = wb.create_sheet("ANEXO 7 CRONOGRAMA")
nc = 4 + D.SEMANAS
encabezado(cr, "ANEXO 7 – CRONOGRAMA DE ACTIVIDADES E INVERSIÓN (21 SEMANAS – 147 DÍAS)", nc)
heads = ["Ítem", "Actividad", "Inicio", "Fin"] + [f"S{w}" for w in range(1, D.SEMANAS + 1)]
hdr(cr, 7, heads, [7, 40, 6, 6] + [9.5] * D.SEMANAS)
r = 8
first = r
for f in D.FORMATO:
    if f[0] == "cap":
        cr.cell(r, 1, f[1] + ".").font = BOLD
        cr.cell(r, 2, f[2]).font = BOLD
        for j in range(1, nc + 1):
            cr.cell(r, j).fill = CAP_FILL; cr.cell(r, j).border = B
    else:
        _, cod, desc, und, q, vu = f
        ini, dur, _ = D.PROG[cod]
        fin = ini + dur - 1
        cr.cell(r, 1, cod); cr.cell(r, 2, desc[:55])
        cr.cell(r, 3, ini).alignment = CENTER; cr.cell(r, 4, fin).alignment = CENTER
        for w in range(1, D.SEMANAS + 1):
            d0, d1 = 7 * (w - 1) + 1, 7 * w
            n = max(0, min(fin, d1) - max(ini, d0) + 1)
            c = cr.cell(r, 4 + w)
            c.border = B
            if n:
                c.value = f"=ROUND('ANEXO 6 PROGRAMA'!F{ROW_PG[cod]}*{n}/{dur},0)"
                c.fill = BAR_FILL
                c.font = Font(color="FFFFFF", size=7)
                c.number_format = NUM
        for j in range(1, 5):
            cr.cell(r, j).border = B
    r += 1
last = r - 1
r += 1
cr.cell(r, 2, "INVERSIÓN SEMANAL (costo directo)").font = BOLD
cr.cell(r + 1, 2, "INVERSIÓN ACUMULADA").font = BOLD
cr.cell(r + 2, 2, "% ACUMULADO").font = BOLD
for w in range(1, D.SEMANAS + 1):
    col = L(4 + w)
    c = cr.cell(r, 4 + w, f"=SUM({col}{first}:{col}{last})"); c.number_format = NUM
    c.font = Font(size=8, bold=True)
    prev = f"+{L(3 + w)}{r+1}" if w > 1 else ""
    c = cr.cell(r + 1, 4 + w, f"={col}{r}{prev}"); c.number_format = NUM; c.font = Font(size=8)
    c = cr.cell(r + 2, 4 + w, f"={col}{r+1}/{L(4 + D.SEMANAS)}{r+1}"); c.number_format = '0.0%'
    c.font = Font(size=8, bold=True)
r += 4
for t in ["Semanas de 7 días calendario. S1 = días 1 a 7 desde el acta de inicio; S21 = días 141 a 147.",
          "Los 3 días restantes del plazo (días 148 a 150) son para la entrega de la obra y no hacen parte "
          "del cronograma evaluado (Anexo 7 de los TR).",
          "Jornada: " + D.JORNADA]:
    cr.merge_cells(start_row=r, start_column=1, end_row=r, end_column=nc)
    cr.cell(r, 1, t).alignment = WRAP
    cr.row_dimensions[r].height = 28
    r += 1
firma(cr, r, nc)
cr.print_title_rows = "7:7"
cr.freeze_panes = "E8"
imprimir(cr, landscape=True)

wb.save(f"{OUT}/PROPUESTA_ECONOMICA.xlsx")

# ===================================================================== SIMULADOR
sm = Workbook()
ws = sm.active
ws.title = "SIMULADOR"
ws["A1"] = "SIMULADOR DE CALIFICACIÓN ECONÓMICA – TR numeral 4.1.1.1"
ws["A1"].font = Font(bold=True, size=13)
ws["A3"] = "Presupuesto oficial"; ws["C3"] = D.PRESUPUESTO_OFICIAL
ws["A4"] = "Balota sorteada (1 a 6)"; ws["C4"] = 4; ws["C4"].fill = IN_FILL
ws["A5"] = "Mínimo válido (90 %)"; ws["C5"] = "=C3*0.9"
ws["A6"] = "Máximo válido (100 %)"; ws["C6"] = "=C3"
for c in ("C3", "C5", "C6"):
    ws[c].number_format = NUM
ws.column_dimensions["A"].width = 30
for col, w in zip("BCDEFGHI", [10, 20, 14, 18, 14, 14, 14, 14]):
    ws.column_dimensions[col].width = w
hdr(ws, 8, ["Proponente", "", "Valor oferta", "¿Hábil? (90–100 %)", "% de la media",
            "Puntaje A", "Puntaje B", "", ""])
ws.merge_cells("A8:B8")
N = 15
for k in range(N):
    rr = 9 + k
    ws.cell(rr, 1, f"Proponente {k+1}")
    c = ws.cell(rr, 3); c.fill = IN_FILL; c.number_format = NUM
    ws.cell(rr, 4, f'=IF(C{rr}="","",IF(AND(C{rr}>=$C$5,C{rr}<=$C$6),1,0))')
    ws.cell(rr, 5, f'=IF(D{rr}=1,C{rr}/$C${9+N+10},"")').number_format = '0.00%'
    ws.cell(rr, 6, f'=IF(D{rr}=1,IF(OR(E{rr}<0.95,E{rr}>1.02),0,ROUND(800*(1-ABS(1-E{rr})),3)),"")')
    ws.cell(rr, 7, f'=IF(D{rr}=1,IF(OR(E{rr}<0.95,E{rr}>1.02),0,ROUND(IF(E{rr}<=1,800*(E{rr}-0.95)/0.05,'
                   f'800*(1.02-E{rr})/0.02),3)),"")')
    for j in range(1, 8):
        ws.cell(rr, j).border = B
ws.cell(9, 3, D.TOTAL)
rr = 9 + N + 1
habil = f"$D$9:$D${8+N}"
vals = f"$C$9:$C${8+N}"
ws.cell(rr, 1, "n (ofertas hábiles)"); ws.cell(rr, 3, f"=SUM({habil})")
ws.cell(rr + 1, 1, "Media geométrica MG")
ws.cell(rr + 1, 3, f"=EXP(SUMPRODUCT(({habil}=1)*LN({vals}+({vals}=\"\")))/C{rr})")
ws.cell(rr + 2, 1, "Media aritmética MA"); ws.cell(rr + 2, 3, f"=SUMPRODUCT(({habil}=1)*{vals})/C{rr}")
names = ["1. MG", "2. MG × 0,99", "3. MG × 1,01", "4. MA", "5. MA × 0,99", "6. MA × 1,01"]
forms = [f"=C{rr+1}", f"=0.99*C{rr+1}", f"=1.01*C{rr+1}", f"=C{rr+2}", f"=0.99*C{rr+2}", f"=1.01*C{rr+2}"]
for k in range(6):
    ws.cell(rr + 3 + k, 1, names[k]); ws.cell(rr + 3 + k, 3, forms[k])
for k in range(rr + 1, rr + 9):
    ws.cell(k, 3).number_format = NUM
ws.cell(rr + 9, 1, "MEDIA SORTEADA").font = BOLD
ws.cell(rr + 9, 3, f"=INDEX(C{rr+3}:C{rr+8},$C$4)").number_format = NUM
ws.cell(rr + 9, 3).fill = TOT_FILL
assert rr + 9 == 9 + N + 10
ws.cell(rr + 11, 1, "Puntaje A: 800 × (1 − |P − M| / M). Puntaje B: lineal, 800 en la media y 0 en "
        "95 % y 102 % de la media. Ambos dan 0 por fuera de 95 %–102 %. El TR solo dice "
        "\"proporcional\": confirmar en clase cuál se usa.").alignment = WRAP
ws.merge_cells(start_row=rr + 11, start_column=1, end_row=rr + 11, end_column=7)
ws.row_dimensions[rr + 11].height = 45
ws.cell(rr + 12, 1, "Escriba los valores de las ofertas en las celdas verdes; la fila 1 trae nuestra oferta.")
sm.save(f"{OUT}/SIMULADOR_CALIFICACION.xlsx")

# ===================================================================== EXPERIENCIA
ex = Workbook()
ws = ex.active
ws.title = "EXPERIENCIA"
ws["A1"] = "CÁLCULO DE LA EXPERIENCIA ESPECÍFICA (TR 3.1.7 y Anexo 3) – cierre " + D.CIERRE
ws["A1"].font = Font(bold=True, size=13)
info = [("Presupuesto oficial (formulario Excel)", D.PRESUPUESTO_OFICIAL, NUM),
        ("Experiencia mínima = 50 % del presupuesto", "=ROUND(C3*0.5,0)", NUM),
        (f"SMMLV {D.ANIO}", D.SMMLV, NUM),
        ("Experiencia mínima en SMMLV (C4 ÷ C5)", "=C4/C5", NUM2),
        ("Contratos terminados desde", D.EXP_DESDE, None),
        ("Máximo de contratos", 5, None)]
for k, (a, v, f) in enumerate(info):
    ws.cell(3 + k, 1, a); c = ws.cell(3 + k, 3, v)
    if f: c.number_format = f
for col, w in zip("ABCDEFGHI", [34, 30, 18, 14, 12, 16, 16, 18, 14]):
    ws.column_dimensions[col].width = w
hdr(ws, 10, ["Contratante", "Objeto", "Valor total contrato ($)", "% participación (100 si individual)",
             "Año de terminación", "Valor que cuenta ($)", "SMMLV del año", "Valor en SMMLV", ""])
for k in range(5):
    rr = 11 + k
    for j in (1, 2, 3, 4, 5):
        ws.cell(rr, j).fill = IN_FILL; ws.cell(rr, j).border = B
    ws.cell(rr, 3).number_format = NUM; ws.cell(rr, 4, 100)
    ws.cell(rr, 6, f'=IF(C{rr}="","",ROUND(C{rr}*D{rr}/100,0))').number_format = NUM
    ws.cell(rr, 7, f'=IF(E{rr}="","",VLOOKUP(E{rr},$K$11:$L$21,2,FALSE))').number_format = NUM
    ws.cell(rr, 8, f'=IF(OR(F{rr}="",G{rr}=""),"",F{rr}/G{rr})').number_format = NUM2
ws.cell(16, 5, "TOTAL").font = BOLD
ws.cell(16, 8, "=SUM(H11:H15)").number_format = NUM2
ws.cell(16, 8).font = BOLD
ws.cell(17, 5, "¿CUMPLE?").font = BOLD
ws.cell(17, 8, '=IF(H16>=C6,"SÍ CUMPLE","NO CUMPLE")').font = BOLD
ws.cell(18, 1, "Llene las celdas verdes. El valor de cada contrato se convierte con el SMMLV del año en que "
        "terminó; la suma debe ser igual o mayor al 50 % del presupuesto expresado en SMMLV 2025.")
ws.merge_cells("A18:H18"); ws["A18"].alignment = WRAP; ws.row_dimensions[18].height = 30
hdr(ws, 10, ["Contratante", "Objeto", "Valor total contrato ($)", "% participación (100 si individual)",
             "Año de terminación", "Valor que cuenta ($)", "SMMLV del año", "Valor en SMMLV", ""])
ws.cell(10, 11, "Año").font = BOLD; ws.cell(10, 12, "SMMLV").font = BOLD
for k, (a, v) in enumerate(D.SMMLV_ANIOS):
    ws.cell(11 + k, 11, a); ws.cell(11 + k, 12, v).number_format = NUM
ex.save(f"{OUT}/EXPERIENCIA_CALCULO.xlsx")
print("ok", R_TOT)

# -*- coding: utf-8 -*-
"""Un solo Excel: PRESUPUESTO (formato original EJERCICIO.xls) + MANO DE OBRA + 4 APU.
Los precios de 3.06, 4.05, 7.01 y 12.02 salen por fórmula de su APU, y el costo de la mano
de obra de cada APU sale de la hoja MANO DE OBRA. Cada fórmula lleva su valor calculado,
para que el archivo se vea completo incluso en visores que no recalculan (celular)."""
import sys
from decimal import Decimal
import xlrd
import xlsxwriter
import datos as D

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
F = lambda x: float(x)

wb = xlsxwriter.Workbook(f"{OUT}/PRESUPUESTO_CON_APU.xlsx")
_fmt_cache = {}


def fmt(**k):
    key = tuple(sorted(k.items()))
    if key not in _fmt_cache:
        base = {"font_name": "Calibri", "font_size": 9, "valign": "vcenter"}
        base.update(k)
        _fmt_cache[key] = wb.add_format(base)
    return _fmt_cache[key]


NUM = '#,##0'
NUM2 = '#,##0.00'
AZUL, CAP, AMA = "#1F4E78", "#D9E1F2", "#FFF2CC"
H = dict(bold=True, font_color="#FFFFFF", bg_color=AZUL, border=1, align="center", text_wrap=True)
CELL = dict(border=1)

# ======================================================================= PRESUPUESTO
rb = xlrd.open_workbook(D.XLS, formatting_info=True)
rs = rb.sheet_by_index(0)
ps = wb.add_worksheet("PRESUPUESTO")
APU_PRECIO_CELL = {}  # se llena después; se usan nombres fijos de celda
CMAP = rb.colour_map


def color(idx):
    c = CMAP.get(idx)
    return "#%02X%02X%02X" % c if c else None


def xf_format(r, c):
    xf = rb.xf_list[rs.cell_xf_index(r, c)]
    f = rb.font_list[xf.font_index]
    k = {"font_name": f.name, "font_size": f.height / 20, "bold": bool(f.bold), "italic": bool(f.italic),
         "num_format": rb.format_map[xf.format_key].format_str,
         "left": xf.border.left_line_style, "right": xf.border.right_line_style,
         "top": xf.border.top_line_style, "bottom": xf.border.bottom_line_style,
         "text_wrap": bool(xf.alignment.text_wrapped)}
    fc = color(f.colour_index)
    if fc and fc != "#000000":
        k["font_color"] = fc
    ha = {1: "left", 2: "center", 3: "right", 5: "justify", 6: "center_across"}.get(xf.alignment.hor_align)
    if ha:
        k["align"] = ha
    k["valign"] = {0: "top", 1: "vcenter", 2: "bottom"}.get(xf.alignment.vert_align, "bottom")
    if xf.background.fill_pattern == 1:
        bg = color(xf.background.pattern_colour_index)
        if bg:
            k["bg_color"] = bg
    return fmt(**k)


for c in range(rs.ncols):
    ci = rs.colinfo_map.get(c)
    if ci:
        ps.set_column(c, c, ci.width / 256)
for r, ri in rs.rowinfo_map.items():
    if not ri.height_mismatch or True:
        ps.set_row(r, ri.height / 20)
merged = {(a, c1): (b, c2) for a, b, c1, c2 in rs.merged_cells}
skip = {(r, c) for a, b, c1, c2 in rs.merged_cells for r in range(a, b) for c in range(c1, c2)
        if (r, c) != (a, c1)}

ROWS = {}
for r in range(rs.nrows):
    for c in range(rs.ncols):
        if (r, c) in skip:
            continue
        v = rs.cell_value(r, c)
        fm = xf_format(r, c)
        if (r, c) in merged:
            b, c2 = merged[(r, c)]
            ps.merge_range(r, c, b - 1, c2 - 1, v, fm)
        elif v != "":
            ps.write(r, c, v, fm)
        else:
            ps.write_blank(r, c, None, fm)
    cod = rs.cell_value(r, 0)
    if isinstance(cod, str) and cod.strip().rstrip(".") in D.PRECIOS and isinstance(rs.cell_value(r, 3), float):
        ROWS[cod.strip().rstrip(".")] = r
    for lab, key in [("VALOR TOTAL COSTO DIRECTO", "CD"), ("VALOR TOTAL COSTO INDIRECTO", "CI")]:
        if rs.cell_value(r, 3) == lab:
            ROWS[key] = r
    for lab in ("A", "I", "U"):
        if rs.cell_value(r, 1) == lab:
            ROWS[lab] = r
    if rs.cell_value(r, 1) == "VALOR TOTAL DEL PROYECTO":
        ROWS["TOT"] = r
assert len([k for k in ROWS if k in D.PRECIOS]) == 85

# ======================================================================= MANO DE OBRA
mo = wb.add_worksheet("MANO DE OBRA")
mo.set_column(0, 0, 50); mo.set_column(1, 1, 11); mo.set_column(2, 2, 18); mo.set_column(3, 3, 22)


def titulo(ws, txt, ncols):
    lines = [(D.ENTIDAD, 12), (D.LICITACION, 10), ("OBJETO: " + D.OBJETO, 9),
             ("PROPONENTE: " + D.PROPONENTE, 9), (txt, 12)]
    for i, (t, s) in enumerate(lines):
        ws.merge_range(i, 0, i, ncols - 1, t, fmt(bold=True, font_size=s, align="center", text_wrap=True))
    ws.set_row(2, 26)


titulo(mo, f"CÁLCULO DEL COSTO DE MANO DE OBRA – {D.ANIO}", 4)
r = 6
mo.write(r, 0, f"Salario mínimo {D.ANIO} (SMMLV)", fmt(**CELL)); mo.write(r, 2, D.SMMLV, fmt(num_format=NUM, **CELL))
mo.write(r, 3, D.DEC_SMMLV, fmt(**CELL))
mo.write(r + 1, 0, f"Auxilio de transporte {D.ANIO}", fmt(**CELL))
mo.write(r + 1, 2, D.AUX_TRANSPORTE, fmt(num_format=NUM, **CELL)); mo.write(r + 1, 3, D.DEC_AUX, fmt(**CELL))
mo.write(r + 2, 0, f"Horas laborables por mes ({D.HORAS_SEMANA} h/semana × 52 / 12)", fmt(**CELL))
mo.write_formula(r + 2, 2, f"={D.HORAS_SEMANA}*52/12", fmt(num_format=NUM2, **CELL), F(D.HORAS_MES))
mo.write(r + 2, 3, "Ley 2101 de 2021", fmt(**CELL))
R_SM, R_AUX, R_HM = r + 1, r + 2, r + 3  # filas Excel (1-based)
r += 4
mo.write_row(r, 0, ["PRESTACIONES SOCIALES Y APORTES DEL EMPLEADOR", "", "% sobre salario", "Soporte"], fmt(**H))
soporte = ["C.S.T. art. 249", "Ley 52 de 1975", "C.S.T. art. 306", "C.S.T. art. 186", "Ley 100 de 1993",
           "Ley 100 de 1993", "Decreto 1772 de 1994 (clase V)", "Ley 21 de 1982", "Ley 89 de 1988",
           "Ley 21 de 1982", "C.S.T. art. 230 y EPP"]
p0 = r + 1
for k, (n, p) in enumerate(D.PRESTACIONES):
    mo.write(p0 + k, 0, n, fmt(**CELL)); mo.write_blank(p0 + k, 1, None, fmt(**CELL))
    mo.write(p0 + k, 2, F(p), fmt(num_format='0.00%', **CELL)); mo.write(p0 + k, 3, soporte[k], fmt(**CELL))
pf = p0 + len(D.PRESTACIONES)
mo.write(pf, 0, "FACTOR PRESTACIONAL TOTAL", fmt(bold=True, **CELL)); mo.write_blank(pf, 1, None, fmt(**CELL))
mo.write_formula(pf, 2, f"=SUM(C{p0+1}:C{pf})", fmt(bold=True, num_format='0.00%', bg_color=AMA, **CELL),
                 F(D.PREST_TOTAL))
mo.write(pf + 1, 0, "Factor sobre auxilio de transporte (cesantías + intereses + prima)", fmt(**CELL))
mo.write_formula(pf + 1, 2, f"=1+C{p0+1}+C{p0+2}+C{p0+3}", fmt(num_format='0.0000', **CELL), F(D.AUX_FACTOR))
R_PF, R_AF = pf + 1, pf + 2
r = pf + 3
mo.write_row(r, 0, ["CARGO", "× SMMLV", "COSTO MENSUAL", "COSTO HORA"], fmt(**H))
CARGO_ROW = {}
for k, (n, m) in enumerate(D.CARGOS):
    rr = r + 1 + k
    h = D.costo_hora(m)
    mo.write(rr, 0, n, fmt(**CELL)); mo.write(rr, 1, F(m), fmt(num_format='0.0', **CELL))
    mo.write_formula(rr, 2, f"=$C${R_SM}*B{rr+1}*(1+$C${R_PF})+$C${R_AUX}*$C${R_AF}",
                     fmt(num_format=NUM, **CELL), F(h * D.HORAS_MES))
    mo.write_formula(rr, 3, f"=C{rr+1}/$C${R_HM}", fmt(num_format=NUM, **CELL), F(h))
    CARGO_ROW[n] = rr + 1
ra, rof = CARGO_ROW["Ayudante (obrero)"], CARGO_ROW["Oficial"]
r = rr + 2
mo.write_row(r, 0, ["CUADRILLA", "", "", "COSTO HORA-CUADRILLA (hc)"], fmt(**H))
CUAD = {}
for k, (key, (n, v)) in enumerate(D.CUADRILLAS.items()):
    rr = r + 1 + k
    nay = {"C11": 1, "C12": 2, "C13": 3}[key]
    mo.write(rr, 0, n, fmt(**CELL)); mo.write_blank(rr, 1, None, fmt(**CELL)); mo.write_blank(rr, 2, None, fmt(**CELL))
    mo.write_formula(rr, 3, f"=D{rof}+{nay}*D{ra}", fmt(bold=True, num_format=NUM, **CELL), F(v))
    CUAD[key] = (f"'MANO DE OBRA'!$D${rr+1}", v)
mo.write(rr + 2, 0, "Costo mensual = salario × (1 + factor prestacional) + auxilio de transporte × factor. "
         "Costo hora = costo mensual ÷ horas del mes.", fmt(italic=True, text_wrap=True))
mo.set_row(rr + 2, 26)
mo.fit_to_pages(1, 1); mo.set_paper(1); mo.center_horizontally()

# ======================================================================= APU
APU_CELL = {}
for cod, a in D.APUS.items():
    ws = wb.add_worksheet(f"APU {cod}")
    for c, w in enumerate([46, 9, 10, 11, 14, 15]):
        ws.set_column(c, c, w)
    titulo(ws, "ANÁLISIS DE PRECIO UNITARIO (APU)", 6)
    ws.write(6, 0, "ÍTEM", fmt(**H)); ws.merge_range(6, 1, 6, 4, "DESCRIPCIÓN", fmt(**H))
    ws.write(6, 5, "UNIDAD", fmt(**H))
    ws.write(7, 0, cod, fmt(bold=True, align="center", font_size=11, **CELL))
    ws.merge_range(7, 1, 7, 4, a["titulo"], fmt(bold=True, font_size=11, text_wrap=True, **CELL))
    ws.write(7, 5, a["und"], fmt(bold=True, align="center", font_size=11, **CELL))
    ws.set_row(7, 30)
    filas, total, precio = D.calc_apu(cod)
    mo_val = sum(f[6] for f in filas if f[0] == "O")
    r = 9
    subs = []
    mo_sub = None
    pend_h = []
    for g, gname in D.GRUPOS:
        sel = [(i, f) for i, f in enumerate(filas) if f[0] == g or (g == "E" and f[0] == "H")]
        if not sel:
            continue
        ws.merge_range(r, 0, r, 5, gname, fmt(bold=True, bg_color=CAP, **CELL))
        r += 1
        ws.write_row(r, 0, ["Descripción", "Unidad", "Cantidad", "Desperdicio", "V. Unitario", "V. Parcial"],
                     fmt(**H))
        r += 1
        r0 = r
        for i, (gg, d, u, q, w, v, parc) in sel:
            ws.write(r, 0, d, fmt(text_wrap=True, **CELL))
            ws.write(r, 1, u, fmt(align="center", **CELL))
            ws.write(r, 2, q, fmt(num_format='0.000', **CELL))
            ws.write(r, 3, w, fmt(num_format='0%', **CELL))
            if gg == "O":
                ws.write_formula(r, 4, "=" + CUAD[a["rec"][i][5]][0], fmt(num_format=NUM2, **CELL), F(v))
            elif gg == "H":
                pend_h.append((r, F(v)))
            else:
                ws.write(r, 4, F(v), fmt(num_format=NUM2, **CELL))
            ws.write_formula(r, 5, f"=C{r+1}*(1+D{r+1})*E{r+1}", fmt(num_format=NUM2, **CELL), F(parc))
            ws.set_row(r, 26 if len(d) > 44 else 15)
            r += 1
        sub = sum(f[6] for _, f in sel)
        ws.write(r, 4, "Subtotal", fmt(bold=True, align="right"))
        ws.write_formula(r, 5, f"=SUM(F{r0+1}:F{r})", fmt(bold=True, num_format=NUM2, top=1), F(sub))
        subs.append((f"F{r+1}", sub))
        if g == "O":
            mo_sub = f"F{r+1}"
        r += 2
    for hr, hv in pend_h:
        ws.write_formula(hr, 4, "=" + mo_sub, fmt(num_format=NUM2, **CELL), hv)
    ws.merge_range(r, 0, r, 4, "COSTO DIRECTO TOTAL DEL APU", fmt(bold=True, bg_color=AMA, **CELL))
    ws.write_formula(r, 5, "=" + "+".join(x for x, _ in subs), fmt(bold=True, num_format=NUM2, bg_color=AMA, **CELL),
                     F(total))
    r += 1
    ws.merge_range(r, 0, r, 4, "PRECIO UNITARIO ADOPTADO (ajustado al peso) → va al presupuesto",
                   fmt(bold=True, bg_color=AMA, font_size=11, **CELL))
    ws.write_formula(r, 5, f"=ROUND(F{r},0)", fmt(bold=True, num_format=NUM, bg_color=AMA, font_size=11, **CELL),
                     precio)
    APU_CELL[cod] = (f"'APU {cod}'!$F${r+1}", precio)
    r += 2
    ws.merge_range(r, 0, r, 5, "Notas: " + a["nota"] + " Herramienta menor = 5 % de la mano de obra. El costo de "
                   "la cuadrilla viene de la hoja MANO DE OBRA. El precio no incluye AIU (15 % + 7 % + 2 %), que se "
                   "aplica sobre el costo directo total del presupuesto.", fmt(italic=True, text_wrap=True, valign="top"))
    ws.set_row(r, 54)
    ws.write(r + 3, 0, "______________________________________")
    ws.write(r + 4, 0, D.REPRESENTANTE + " – Representante legal", fmt(bold=True))
    ws.fit_to_pages(1, 1); ws.set_paper(1); ws.center_horizontally()

# ======================================================================= fórmulas del presupuesto
bold_num = xf_format(ROWS["TOT"], 5)
for cod, r in ROWS.items():
    if cod not in D.PRECIOS:
        continue
    fe, ff = xf_format(r, 4), xf_format(r, 5)
    if cod in APU_CELL:
        ref, val = APU_CELL[cod]
        ps.write_formula(r, 4, "=" + ref, fmt(num_format=NUM, bold=True, font_color="#C00000", border=1), val)
    else:
        ps.write(r, 4, D.PRECIOS[cod], fe)
    ps.write_formula(r, 5, f"=ROUND(D{r+1}*E{r+1},0)", ff, D.total_item(cod))
first, last = min(ROWS[c] for c in D.PRECIOS) + 1, max(ROWS[c] for c in D.PRECIOS) + 1
ps.write_formula(ROWS["CD"], 5, f"=SUM(F{first}:F{last})", xf_format(ROWS["CD"], 5), D.CD)
for k, v in (("A", D.VA), ("I", D.VI), ("U", D.VU_)):
    ps.write_formula(ROWS[k], 5, f"=ROUND($F${ROWS['CD']+1}*E{ROWS[k]+1},0)", xf_format(ROWS[k], 5), v)
ps.write_formula(ROWS["CI"], 5, f"=SUM(F{ROWS['A']+1}:F{ROWS['U']+1})", xf_format(ROWS["CI"], 5),
                 D.VA + D.VI + D.VU_)
ps.write_formula(ROWS["TOT"], 5, f"=F{ROWS['CD']+1}+F{ROWS['CI']+1}", bold_num, D.TOTAL)
ps.write(1, 1, "PROPONENTE: " + D.PROPONENTE, fmt(bold=True, font_size=11))
n = rs.nrows
ps.write(n + 1, 1, "SON: " + D.letras(D.TOTAL) + " PESOS M/CTE.", fmt(bold=True, font_size=10))
ps.write(n + 2, 1, "Los valores unitarios en rojo (3.06, 4.05, 7.01 y 12.02) salen de su APU (hojas APU). "
         "Los demás precios incluyen materiales, mano de obra, equipo y transporte.", fmt(italic=True, font_size=8))
ps.write(n + 5, 1, "______________________________________")
ps.write(n + 6, 1, D.REPRESENTANTE + " – Representante legal", fmt(bold=True))
ps.fit_to_pages(1, 0); ps.set_paper(1); ps.center_horizontally(); ps.repeat_rows(5)
wb.close()
print("ok")

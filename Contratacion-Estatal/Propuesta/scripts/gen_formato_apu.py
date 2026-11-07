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
AZUL, CAP, AMA = "#1F4E78", "#D9E1F2", "#BDD7EE"
H = dict(bold=True, font_color="#FFFFFF", bg_color=AZUL, border=1, align="center", text_wrap=True)
CELL = dict(border=1)

# ======================================================================= hojas (orden)
ps = wb.add_worksheet("PRESUPUESTO")
rsm = wb.add_worksheet("RESUMEN")

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

# ======================================================================= PRESUPUESTO organizado
ACC = '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)'
B9 = dict(font_size=9, border=1)
ps.set_column(0, 0, 8); ps.set_column(1, 1, 52); ps.set_column(2, 3, 11); ps.set_column(4, 4, 15)
ps.set_column(5, 5, 18)
hdr_lines = [(D.ENTIDAD, 12), (D.LICITACION, 10), ("OBJETO: " + D.OBJETO, 9),
             ("PROPONENTE: " + D.PROPONENTE, 10),
             ("FORMATO DE CANTIDADES Y PRESUPUESTO – OFERTA ECONÓMICA", 12)]
for i, (t, sz) in enumerate(hdr_lines):
    ps.merge_range(i, 0, i, 5, t, fmt(bold=True, font_size=sz, align="center", text_wrap=True))
ps.set_row(2, 26)
r = 6
ps.merge_range(r, 0, r, 5, "COSTOS DIRECTOS", fmt(bold=True, font_size=11, align="center"))
r += 1
ps.write_row(r, 0, ["COD.", "ITEM", "UNIDAD", "CANTIDAD", "VR. UNITARIO", "VR. TOTAL"], fmt(**H))
HEAD_ROW = r
r += 1
sub_cells = []
cap_ref = {}
for cc, nombre, its in D.CAPITULOS:
    ps.write(r, 0, cc + ".", fmt(bold=True, bg_color=CAP, **B9))
    ps.merge_range(r, 1, r, 5, nombre, fmt(bold=True, bg_color=CAP, **B9))
    r += 1
    r0 = r
    for cod in its:
        _, _, desc, und, q, vu = next(x for x in D.ITEMS if x[1] == cod)
        ps.write(r, 0, cod, fmt(align="left", **B9))
        ps.write(r, 1, desc, fmt(text_wrap=True, **B9))
        ps.write(r, 2, und, fmt(align="center", **B9))
        ps.write(r, 3, q, fmt(num_format='#,##0.00', **B9))
        if cod in APU_CELL:
            ref, val = APU_CELL[cod]
            ps.write_formula(r, 4, "=" + ref, fmt(num_format=ACC, bold=True, font_color="#1F4E78", **B9), val)
        else:
            ps.write(r, 4, D.PRECIOS[cod], fmt(num_format=ACC, **B9))
        ps.write_formula(r, 5, f"=ROUND(D{r+1}*E{r+1},0)", fmt(num_format=ACC, **B9), D.total_item(cod))
        if len(desc) > 55:
            ps.set_row(r, 12.5 * (len(desc) // 52 + 1))
        r += 1
    ps.merge_range(r, 0, r, 4, f"SUBTOTAL {cc}. {nombre}", fmt(bold=True, align="right", bg_color="#DEEAF6", **B9))
    ps.write_formula(r, 5, f"=SUM(F{r0+1}:F{r})", fmt(bold=True, num_format=ACC, bg_color="#DEEAF6", **B9),
                     D.SUBTOTAL[cc])
    sub_cells.append(f"F{r+1}")
    cap_ref[cc] = f"PRESUPUESTO!$F${r+1}"
    r += 2
ps.merge_range(r, 0, r, 4, "VALOR TOTAL COSTO DIRECTO", fmt(bold=True, font_size=10, bg_color=AMA, border=1))
ps.write_formula(r, 5, "=" + "+".join(sub_cells), fmt(bold=True, font_size=10, num_format=ACC, bg_color=AMA, border=1),
                 D.CD)
R_CD = r + 1
r += 2
ps.merge_range(r, 0, r, 5, "COSTOS INDIRECTOS", fmt(bold=True, font_size=11, align="center"))
r += 1
ps.write(r, 0, "", fmt(**H)); ps.merge_range(r, 1, r, 3, "DESCRIPCIÓN", fmt(**H))
ps.write(r, 4, "PORCENTAJE", fmt(**H)); ps.write(r, 5, "VR. TOTAL", fmt(**H))
r += 1
ra = r
for sig, nom, pct, val in (("A", "Administración", D.A_PCT, D.VA), ("I", "Imprevistos", D.I_PCT, D.VI),
                           ("U", "Utilidad", D.U_PCT, D.VU_)):
    ps.write(r, 0, sig, fmt(bold=True, align="center", **B9))
    ps.merge_range(r, 1, r, 3, nom, fmt(**B9))
    ps.write(r, 4, F(pct), fmt(num_format='0.00%', align="center", **B9))
    ps.write_formula(r, 5, f"=ROUND($F${R_CD}*E{r+1},0)", fmt(num_format=ACC, **B9), val)
    r += 1
ps.merge_range(r, 0, r, 3, "VALOR TOTAL COSTO INDIRECTO (AIU)", fmt(bold=True, **B9))
ps.write_formula(r, 4, f"=SUM(E{ra+1}:E{r})", fmt(bold=True, num_format='0.00%', align="center", **B9), F(D.AIU))
ps.write_formula(r, 5, f"=SUM(F{ra+1}:F{r})", fmt(bold=True, num_format=ACC, **B9), D.VA + D.VI + D.VU_)
R_CI = r + 1
r += 2
ps.merge_range(r, 0, r, 4, "VALOR TOTAL DEL PROYECTO (costo directo + AIU)",
               fmt(bold=True, font_size=12, bg_color=AMA, border=2))
ps.write_formula(r, 5, f"=F{R_CD}+F{R_CI}", fmt(bold=True, font_size=12, num_format=ACC, bg_color=AMA, border=2),
                 D.TOTAL)
R_TOT = r + 1
r += 1
ps.merge_range(r, 0, r, 5, "SON: " + D.letras(D.TOTAL) + " PESOS M/CTE.",
               fmt(bold=True, font_size=10, text_wrap=True))
ps.set_row(r, 28)
r += 2
notas = [
    "Cantidades y unidades del formato oficial sin modificación. Precios ajustados al peso y fijos, sin reajuste "
    "durante el plazo (numeral 3.2.1 de los TR).",
    "Los valores unitarios en azul y negrilla (3.06, 4.05, 7.01 y 12.02) salen por fórmula de su APU (hojas APU), y la mano "
    "de obra de cada APU sale de la hoja MANO DE OBRA (salario mínimo 2025).",
    "Los precios unitarios cubren materiales, mano de obra con prestaciones, herramienta, equipo y transporte. "
    "Personal directivo, señalización, seguridad, limpieza, impuestos y contribuciones van en el AIU "
    "(numerales 3.2.1.1, 6.1, 6.10, 6.12 y 6.13).",
]
for t in notas:
    ps.merge_range(r, 0, r, 5, "• " + t, fmt(italic=True, font_size=8, text_wrap=True, valign="top"))
    ps.set_row(r, 24)
    r += 1
ps.write(r + 2, 1, "______________________________________")
ps.write(r + 3, 1, D.REPRESENTANTE + " – Representante legal", fmt(bold=True))
ps.write(r + 4, 1, D.CEDULA_REP)
ps.fit_to_pages(1, 0); ps.set_paper(1); ps.center_horizontally(); ps.repeat_rows(HEAD_ROW)
ps.set_margins(left=0.4, right=0.4, top=0.5, bottom=0.5)

# ======================================================================= RESUMEN
for c, w in enumerate([8, 44, 18, 12]):
    rsm.set_column(c, c, w)
titulo(rsm, "RESUMEN DEL PRESUPUESTO POR CAPÍTULOS", 4)
r = 6
rsm.write_row(r, 0, ["CAP.", "CAPÍTULO", "VALOR", "% DEL C.D."], fmt(**H))
r += 1
r0 = r
for cc, nombre, its in D.CAPITULOS:
    rsm.write(r, 0, cc, fmt(align="center", **CELL)); rsm.write(r, 1, nombre, fmt(**CELL))
    rsm.write_formula(r, 2, "=" + cap_ref[cc], fmt(num_format=ACC, **CELL), D.SUBTOTAL[cc])
    rsm.write_formula(r, 3, f"=C{r+1}/$C${r0+len(D.CAPITULOS)+1}", fmt(num_format='0.0%', **CELL),
                      D.SUBTOTAL[cc] / D.CD)
    r += 1
rsm.merge_range(r, 0, r, 1, "COSTO DIRECTO", fmt(bold=True, bg_color=AMA, **CELL))
rsm.write_formula(r, 2, f"=SUM(C{r0+1}:C{r})", fmt(bold=True, num_format=ACC, bg_color=AMA, **CELL), D.CD)
rsm.write_formula(r, 3, f"=SUM(D{r0+1}:D{r})", fmt(bold=True, num_format='0.0%', bg_color=AMA, **CELL), 1.0)
r += 1
for lab, ref, val in (("A – Administración (15 %)", ra + 1, D.VA), ("I – Imprevistos (7 %)", ra + 2, D.VI),
                      ("U – Utilidad (2 %)", ra + 3, D.VU_)):
    rsm.merge_range(r, 0, r, 1, lab, fmt(**CELL))
    rsm.write_formula(r, 2, f"=PRESUPUESTO!F{ref}", fmt(num_format=ACC, **CELL), val)
    rsm.write_blank(r, 3, None, fmt(**CELL))
    r += 1
rsm.merge_range(r, 0, r, 1, "VALOR TOTAL DE LA PROPUESTA", fmt(bold=True, font_size=11, bg_color=AMA, **CELL))
rsm.write_formula(r, 2, f"=PRESUPUESTO!F{R_TOT}", fmt(bold=True, font_size=11, num_format=ACC, bg_color=AMA, **CELL),
                  D.TOTAL)
rsm.write_blank(r, 3, None, fmt(bg_color=AMA, **CELL))
r += 2
rsm.merge_range(r, 0, r, 1, "Presupuesto oficial", fmt(**CELL))
rsm.write(r, 2, D.PRESUPUESTO_OFICIAL, fmt(num_format=ACC, **CELL)); rsm.write_blank(r, 3, None, fmt(**CELL))
rsm.merge_range(r + 1, 0, r + 1, 1, "Oferta / presupuesto oficial (debe estar entre 90 % y 100 %)", fmt(**CELL))
rsm.write_formula(r + 1, 2, f"=C{r-1}/C{r+1}", fmt(num_format="0.00%", bold=True, **CELL),
                  D.TOTAL / D.PRESUPUESTO_OFICIAL)
rsm.write_blank(r + 1, 3, None, fmt(**CELL))
rsm.fit_to_pages(1, 1); rsm.set_paper(1); rsm.center_horizontally()

wb.close()
print("ok")

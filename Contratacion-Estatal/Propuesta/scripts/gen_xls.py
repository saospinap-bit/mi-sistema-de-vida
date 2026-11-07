# -*- coding: utf-8 -*-
"""Llena el formato original EJERCICIO.xls con los precios de la oferta, conservando su diseño."""
import sys
import xlrd
from xlutils.copy import copy
import xlwt
import datos as D
CAL = xlwt.easyxf('font: name Calibri, height 220, bold on')
CALN = xlwt.easyxf('font: name Calibri, height 220')

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
rb = xlrd.open_workbook(D.XLS, formatting_info=True)
rs = rb.sheet_by_index(0)
wb = copy(rb)
ws = wb.get_sheet(0)


def put(r, c, v):
    """Escribe conservando el estilo (formato de número, bordes, fuente) de la celda original."""
    row = ws._Worksheet__rows.get(r)
    xf = row._Row__cells[c].xf_idx if row and c in row._Row__cells else None
    ws.write(r, c, v)
    if xf is not None:
        ws._Worksheet__rows[r]._Row__cells[c].xf_idx = xf


n = 0
for r in range(rs.nrows):
    cod = rs.cell_value(r, 0)
    q = rs.cell_value(r, 3)
    if isinstance(cod, str) and cod.strip().rstrip(".") in D.PRECIOS and isinstance(q, float):
        c = cod.strip().rstrip(".")
        put(r, 4, D.PRECIOS[c])
        put(r, 5, D.total_item(c))
        n += 1
    elif rs.cell_value(r, 3) == "VALOR TOTAL COSTO DIRECTO":
        put(r, 5, D.CD)
    elif rs.cell_value(r, 1) == "A":
        put(r, 5, D.VA)
    elif rs.cell_value(r, 1) == "I":
        put(r, 5, D.VI)
    elif rs.cell_value(r, 1) == "U":
        put(r, 5, D.VU_)
    elif rs.cell_value(r, 3) == "VALOR TOTAL COSTO INDIRECTO":
        put(r, 5, D.VA + D.VI + D.VU_)
    elif rs.cell_value(r, 1) == "VALOR TOTAL DEL PROYECTO":
        put(r, 5, D.TOTAL)
assert n == 85, n
ws.write(1, 1, "PROPONENTE: " + D.PROPONENTE, CAL)
ws.write(rs.nrows + 1, 1, "SON: " + D.letras(D.TOTAL) + " PESOS M/CTE.", CAL)
ws.write(rs.nrows + 4, 1, "______________________________", CALN)
ws.write(rs.nrows + 5, 1, D.REPRESENTANTE + " – Representante legal", CALN)
wb.save(f"{OUT}/EJERCICIO_OFERTA.xls")
print("xls ok", n)

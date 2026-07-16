# -*- coding: utf-8 -*-
import fitz, os
def crop(pdf, out, fx0, fy0, fx1, fy1, zoom=5.0):
    doc = fitz.open(pdf); pg = doc[0]; r = pg.rect
    clip = fitz.Rect(r.width*fx0, r.height*fy0, r.width*fx1, r.height*fy1)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(os.path.join("_img", out)); print("OK", out, pix.width, pix.height)

crop("ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE COLUMNAS.pdf", "crop_col_det1.png",
     0.06, 0.60, 0.24, 0.82)
crop("ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE COLUMNAS.pdf", "crop_col_det2.png",
     0.24, 0.60, 0.42, 0.82)

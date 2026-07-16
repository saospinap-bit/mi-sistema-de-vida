# -*- coding: utf-8 -*-
import fitz, os
def crop(pdf, out, fx0, fy0, fx1, fy1, zoom=4.0):
    doc = fitz.open(pdf); pg = doc[0]; r = pg.rect
    clip = fitz.Rect(r.width*fx0, r.height*fy0, r.width*fx1, r.height*fy1)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(os.path.join("_img", out)); print("OK", out, pix.width, pix.height)

A = "ARQUITECTONICOS - MODULO 1 - FC3-PLANTA 1-1.pdf"
# Cuadrantes del arquitectonico para leer cotas perimetrales
crop(A, "arq_full_hi.png", 0.0, 0.0, 1.0, 1.0, zoom=3.2)

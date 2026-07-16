# -*- coding: utf-8 -*-
import fitz, os
def crop(pdf, out, fx0, fy0, fx1, fy1, zoom=4.5):
    doc = fitz.open(pdf); pg = doc[0]; r = pg.rect
    clip = fitz.Rect(r.width*fx0, r.height*fy0, r.width*fx1, r.height*fy1)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(os.path.join("_img", out)); print("OK", out, pix.width, pix.height)

D = "ESTRUCTURAL - MODULO 1 - FC3-DETALLES MAMPOSTERIA.pdf"
# cuadrantes del plano de detalles para leer todas las secciones
crop(D, "det_q1.png", 0.02, 0.05, 0.52, 0.52)   # arriba izq
crop(D, "det_q2.png", 0.50, 0.05, 0.99, 0.52)   # arriba der
crop(D, "det_q3.png", 0.02, 0.50, 0.52, 0.98)   # abajo izq
crop(D, "det_q4.png", 0.50, 0.50, 0.99, 0.98)   # abajo der

# -*- coding: utf-8 -*-
import fitz, os
def crop_pts(pdf, out, x0, y0, x1, y1, zoom=4):
    d=fitz.open(pdf); pg=d[0]
    pix=pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=fitz.Rect(x0,y0,x1,y1))
    pix.save(os.path.join("_img",out)); print("OK",out,pix.width,pix.height)

C="ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE CIMENTACION.pdf"
# region alrededor/debajo del detalle de zapata para hallar el detalle de losa
crop_pts(C,"find_losa1.png", 1450, 850, 2350, 1350)
crop_pts(C,"find_losa2.png", 1950, 1300, 2835, 1750)

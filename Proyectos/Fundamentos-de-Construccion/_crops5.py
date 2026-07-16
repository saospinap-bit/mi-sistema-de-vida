# -*- coding: utf-8 -*-
import fitz, os
def crop_pts(pdf, out, x0, y0, x1, y1, zoom=6):
    doc = fitz.open(pdf); pg = doc[0]
    clip = fitz.Rect(x0, y0, x1, y1)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(os.path.join("_img", out)); print("OK", out, pix.width, pix.height)

C = "ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE CIMENTACION.pdf"
# nota NE ... 0.10 (placa) en la zona central del plano
crop_pts(C, "cim_placa_010.png", 300, 1180, 950, 1300)
# detalle solado / piso (arriba centro-der)
crop_pts(C, "cim_solado.png", 1560, 640, 1980, 800)
# convenciones placa 0.05
crop_pts(C, "cim_conv.png", 2020, 1400, 2600, 1480)

# -*- coding: utf-8 -*-
import fitz, os
def crop_pts(pdf, out, x0, y0, x1, y1, zoom=6):
    d=fitz.open(pdf); pg=d[0]
    pix=pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=fitz.Rect(x0,y0,x1,y1))
    pix.save(os.path.join("_img",out)); print("OK",out,pix.width,pix.height)

C="ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE CIMENTACION.pdf"
# Detalle tipo zapata (seccion con 'nivel de desplante minimo 1.5m')
crop_pts(C,"ref_2_1_3_desplante.png", 1540, 600, 2000, 840)
# Cuadro de zapatas (Z-1 2.30, Z-2 2.15)
crop_pts(C,"ref_2_1_3_cuadro.png", 1850, 250, 2560, 520)

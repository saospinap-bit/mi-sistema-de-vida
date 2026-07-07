# -*- coding: utf-8 -*-
import fitz, os
os.makedirs("_img", exist_ok=True)

def crop(pdf, out, fx0, fy0, fx1, fy1, zoom=4.0):
    doc = fitz.open(pdf); pg = doc[0]; r = pg.rect
    clip = fitz.Rect(r.width*fx0, r.height*fy0, r.width*fx1, r.height*fy1)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(os.path.join("_img", out))
    print("OK", out, pix.width, "x", pix.height)

# Detalle de columnas (parte inferior izquierda del plano)
crop("ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE COLUMNAS.pdf", "crop_col_detalle.png",
     0.08, 0.46, 0.30, 0.66, zoom=5)

# Detalle seccion vigueta / losa aligerada de cubierta (arriba a la derecha)
crop("ESTRUCTURAL - MODULO 1 - FC3-PLACA DE CUBIERTA.pdf", "crop_cub_seccion.png",
     0.60, 0.10, 0.88, 0.28, zoom=5)

# Detalle viguetas de cubierta (abajo centro)
crop("ESTRUCTURAL - MODULO 1 - FC3-PLACA DE CUBIERTA.pdf", "crop_cub_viguetas.png",
     0.28, 0.44, 0.52, 0.62, zoom=5)

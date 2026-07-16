# -*- coding: utf-8 -*-
import fitz, os
def crop(pdf, out, fx0, fy0, fx1, fy1, zoom=3.5):
    doc = fitz.open(pdf); pg=doc[0]; r=pg.rect
    clip=fitz.Rect(r.width*fx0, r.height*fy0, r.width*fx1, r.height*fy1)
    pix=pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
    pix.save(os.path.join("_img",out)); print("OK",out,pix.width,pix.height)

C="ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE CIMENTACION.pdf"
crop(C,"cim_izq.png",0.0,0.0,0.40,0.95)
crop(C,"cim_cen.png",0.30,0.0,0.70,0.95)

# contar etiquetas Z-1 / Z-2 por texto
import fitz as f2
d=f2.open(C); pg=d[0]
zs=[w for w in pg.get_text('words') if w[4].strip() in ('Z-1','Z-2','Z1','Z2','Z-1,','Z-2,')]
print("Etiquetas Z encontradas:", len(zs))
for w in zs: print("  ", w[4], "en x=",round(w[0]), "y=",round(w[1]))

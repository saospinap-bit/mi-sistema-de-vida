# -*- coding: utf-8 -*-
import fitz, os
def crop(pdf, out, x0,y0,x1,y1, zoom=5):
    d=fitz.open(pdf); pg=d[0]
    pix=pg.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=fitz.Rect(x0,y0,x1,y1))
    pix.save(os.path.join("_img",out)); print("OK",out,pix.width,pix.height)

CIM="ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE CIMENTACION.pdf"
CUB="ESTRUCTURAL - MODULO 1 - FC3-PLACA DE CUBIERTA.pdf"
DET="ESTRUCTURAL - MODULO 1 - FC3-DETALLES MAMPOSTERIA.pdf"

# Vigas de cimentacion (secciones VC-1..VC-4, VC-A/VC-B) -> 2.2.1 / 2.3.1
crop(CIM,"ref_vigas_cim.png", 60,1170, 900,1800, zoom=4.5)
# Despiece de cubierta (VG-6, viguetas, VG-7, VG-1/2/3) -> 4.2.1 / 4.3.3 / 4.8.1
crop(CUB,"ref_vigas_cubierta.png", 100,1150, 1720,1660, zoom=3.2)
# Detalle de columneta (0.20x0.15, estribo No.3 c/0.20) -> 5.1.2 / 5.2.1
crop(DET,"ref_columneta.png", 760,560, 1180,1030, zoom=5)
# Detalle viga cinta -> 5.2.1
crop(DET,"ref_cinta.png", 1300,820, 1830,1320, zoom=5)

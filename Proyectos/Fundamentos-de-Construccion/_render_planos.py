import fitz, os

OUT = "_img"
os.makedirs(OUT, exist_ok=True)

# (pdf, salida, zoom)
planos = [
    ("ARQUITECTONICOS - MODULO 1 - FC3-PLANTA 1-1.pdf", "plano_arquitectonico.png", 2.2),
    ("ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE CIMENTACION.pdf", "plano_cimentacion.png", 1.1),
    ("ESTRUCTURAL - MODULO 1 - FC3-PLANTA DE COLUMNAS.pdf", "plano_columnas.png", 1.1),
    ("ESTRUCTURAL - MODULO 1 - FC3-PLACA DE CUBIERTA.pdf", "plano_cubierta.png", 1.1),
    ("ESTRUCTURAL - MODULO 1 - FC3-DETALLES MAMPOSTERIA.pdf", "plano_detalles_mamp.png", 1.1),
    ("MAMPOSTERIA - FACHADA - DIVISORI.pdf", "plano_mamposteria.png", 1.6),
    ("PLANTA - ADOQUIN - ARQUITECTONICA FC3-MEDIDAS - ADOQUIN.pdf", "plano_adoquin.png", 1.6),
]

for pdf, out, zoom in planos:
    if not os.path.exists(pdf):
        print("NO EXISTE:", pdf); continue
    doc = fitz.open(pdf)
    page = doc[0]
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    path = os.path.join(OUT, out)
    pix.save(path)
    print(f"OK {out}  {pix.width}x{pix.height}  ({os.path.getsize(path)//1024} KB)")

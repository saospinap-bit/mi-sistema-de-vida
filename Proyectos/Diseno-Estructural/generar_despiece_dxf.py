#!/usr/bin/env python3
"""
Generador de DESPIECE en DXF (abre en AutoCAD) para viguetas/vigas/riostras.
Dibuja: elevacion longitudinal con refuerzo y estribos + seccion transversal + notas.
Parametrico: cuando tengamos el diseno real (de la herramienta), se regenera con tus barras.
Requiere: ezdxf
"""
import ezdxf

def despiece(nombre, archivo, L, b, h, rec, n_inf, db_inf, n_sup, db_sup,
             s_conf, s_centro, Lconf, est_label):
    doc = ezdxf.new("R2018", setup=True)
    msp = doc.modelspace()

    # ---------- ELEVACION (unidades = mm, escala 1:1) ----------
    msp.add_lwpolyline([(0,0),(L,0),(L,h),(0,h)], close=True)  # contorno viga
    # barras inferiores (corren toda la luz)
    msp.add_line((rec, rec), (L-rec, rec))
    # barras superiores (bastones en apoyos, largo Lconf+desde cara)
    msp.add_line((0, h-rec), (Lconf, h-rec))
    msp.add_line((L-Lconf, h-rec), (L, h-rec))
    # estribos: mas juntos en zona de confinamiento, mas separados al centro
    x = rec; xs=[]
    while x <= L-rec:
        xs.append(x)
        x += s_conf if (x < Lconf or x > L-Lconf) else s_centro
    for xi in xs:
        msp.add_line((xi, rec), (xi, h-rec))
    # cotas basicas
    msp.add_aligned_dim(p1=(0,-150), p2=(L,-150), distance=-120,
                        override={"dimtxt":120}).render()
    # ---------- SECCION TRANSVERSAL (a la derecha) ----------
    ox = L + 800
    msp.add_lwpolyline([(ox,0),(ox+b,0),(ox+b,h),(ox,h)], close=True)
    # estribo (rectangulo interior)
    msp.add_lwpolyline([(ox+rec,rec),(ox+b-rec,rec),(ox+b-rec,h-rec),(ox+rec,h-rec)], close=True)
    # barras inferiores
    if n_inf>1:
        sep=(b-2*rec)/(n_inf-1)
    else:
        sep=0
    for i in range(n_inf):
        cx = ox+rec + (i*sep if n_inf>1 else (b-2*rec)/2)
        msp.add_circle((cx, rec+db_inf/2), db_inf/2)
    # barras superiores
    if n_sup>1:
        seps=(b-2*rec)/(n_sup-1)
    else:
        seps=0
    for i in range(n_sup):
        cx = ox+rec + (i*seps if n_sup>1 else (b-2*rec)/2)
        msp.add_circle((cx, h-rec-db_sup/2), db_sup/2)

    # ---------- NOTAS ----------
    ty = h + 250
    msp.add_text(nombre, height=120).set_placement((0, ty))
    notas = [
        f"Seccion: {b} x {h} mm",
        f"Inferior: {n_inf} barras No.{round(db_inf/3.175)}  (db={db_inf} mm)",
        f"Superior (bastones): {n_sup} barras No.{round(db_sup/3.175)}",
        f"Estribos: {est_label}  -> @ {s_conf} mm en {Lconf} mm de cada extremo (confinamiento), resto @ {s_centro} mm",
        f"Longitud: {L} mm",
    ]
    for i, t in enumerate(notas):
        msp.add_text(t, height=90).set_placement((0, ty - 200 - i*160))

    doc.saveas(archivo)
    print(f"OK -> {archivo}  (estribos dibujados: {len(xs)})")

if __name__ == "__main__":
    # EJEMPLOS con valores del diseno verificado
    despiece("DESPIECE VIGA V-1 (EJEMPLO)", "Despiece-Viga-EJEMPLO.dxf",
             L=5000, b=300, h=500, rec=40,
             n_inf=2, db_inf=15.9, n_sup=3, db_sup=15.9,
             s_conf=100, s_centro=200, Lconf=1000, est_label="Estribo No.3")
    despiece("DESPIECE VIGUETA VG-1 (EJEMPLO)", "Despiece-Vigueta-EJEMPLO.dxf",
             L=5000, b=100, h=400, rec=25,
             n_inf=1, db_inf=15.9, n_sup=2, db_sup=12.7,
             s_conf=90, s_centro=180, Lconf=800, est_label="Estribo No.2")

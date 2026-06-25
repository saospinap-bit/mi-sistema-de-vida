#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de planos de despiece (DXF, editable en AutoCAD) para el proyecto
de Diseno Estructural - Grupo 6 Santa Marta.

Produce 3 archivos en /Solucion:
  - Despiece-Vigas-VC.dxf      (vigas de carga 40x30, grupos VC-1..3)
  - Despiece-Riostras-VR.dxf   (vigas de rigidez/riostras 40x35, grupos VR-1..4)
  - Despiece-Viguetas.dxf      (viguetas T 15x34, grupos de luz VT-1..4)

Valores tomados del Excel de calculos verificado (NSR-10, DMO, R=5,
f'c=28 MPa, fy=420 MPa). Unidades de dibujo: milimetros (1:1).
"""
import ezdxf

# ---------------------------------------------------------------- utilidades
def setup_doc():
    doc = ezdxf.new("R2010", setup=True)
    doc.units = 6  # metros? -> usamos mm; dejamos 4 = mm
    doc.header["$INSUNITS"] = 4  # 4 = milimetros
    layers = [
        ("CONCRETO", 8),
        ("ACERO_SUP", 1),   # rojo  - acero negativo (superior)
        ("ACERO_INF", 5),   # azul  - acero positivo (inferior)
        ("ESTRIBOS", 3),    # verde
        ("COTAS", 4),       # cian
        ("TEXTO", 7),       # blanco/negro
        ("ROTULO", 2),      # amarillo
        ("EJES", 6),        # magenta
    ]
    for name, color in layers:
        doc.layers.add(name, color=color)
    # estilos de texto
    return doc


def add_text(msp, txt, x, y, h, layer="TEXTO", align="LEFT", rot=0):
    t = msp.add_text(txt, dxfattribs={"height": h, "layer": layer, "rotation": rot})
    # ezdxf: set placement
    if align == "CENTER":
        t.set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    elif align == "RIGHT":
        t.set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_RIGHT)
    else:
        t.set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_LEFT)
    return t


def dim_horizontal(msp, x1, x2, y, text, off=140, h=70):
    """Cota horizontal sencilla con lineas de extension y texto."""
    msp.add_line((x1, y), (x1, y - off - 40), dxfattribs={"layer": "COTAS"})
    msp.add_line((x2, y), (x2, y - off - 40), dxfattribs={"layer": "COTAS"})
    yl = y - off
    msp.add_line((x1, yl), (x2, yl), dxfattribs={"layer": "COTAS"})
    # marcas en extremos
    for xx in (x1, x2):
        msp.add_line((xx - 25, yl - 25), (xx + 25, yl + 25), dxfattribs={"layer": "COTAS"})
    add_text(msp, text, (x1 + x2) / 2, yl + 55, h, layer="COTAS", align="CENTER")


def scale_bar(msp, x, y, total_m=2.0, seg=0.5):
    """Barra de escala grafica (en mm, 1:1). Segmentos de 'seg' metros."""
    n = int(round(total_m / seg))
    seg_mm = seg * 1000.0
    h = 60
    for i in range(n):
        x0 = x + i * seg_mm
        layer = "ROTULO" if i % 2 == 0 else "TEXTO"
        msp.add_lwpolyline([(x0, y), (x0 + seg_mm, y), (x0 + seg_mm, y - h),
                            (x0, y - h), (x0, y)],
                           dxfattribs={"layer": "COTAS", "closed": True})
        if i % 2 == 0:
            # relleno simbolico con hatch alternado: dibujamos diagonal
            msp.add_line((x0, y - h), (x0 + seg_mm, y), dxfattribs={"layer": "COTAS"})
        add_text(msp, f"{i*seg:.1f}", x0, y - h - 70, 55, layer="COTAS", align="CENTER")
    add_text(msp, f"{total_m:.1f} m", x + n * seg_mm, y - h - 70, 55, layer="COTAS", align="CENTER")
    add_text(msp, "ESCALA GRAFICA (m)", x, y + 70, 60, layer="TEXTO", align="LEFT")


def title_block(msp, x, y, w, lines):
    """Cuadro de notas/rotulo."""
    hrow = 220
    htot = hrow * len(lines)
    msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y - htot), (x, y - htot), (x, y)],
                       dxfattribs={"layer": "ROTULO", "closed": True})
    for i, (txt, bold) in enumerate(lines):
        yy = y - hrow * i - hrow / 2
        if i > 0:
            msp.add_line((x, y - hrow * i), (x + w, y - hrow * i), dxfattribs={"layer": "ROTULO"})
        add_text(msp, txt, x + 80, yy, 95 if bold else 80,
                 layer="ROTULO" if bold else "TEXTO", align="LEFT")


# ---------------------------------------------------------------- viga/riostra
def draw_beam(msp, ox, oy, *, tag, bxh, Ln_m, n_sup, n_inf, db_sup, db_inf,
              Lsup_m, Linf_m, s_conf, s_centro, zona2h, est_tag, Mneg, Mpos, Vu,
              tors, Ats, d_mm, dbar_sup_mm, dbar_inf_mm):
    """Dibuja elevacion + 2 secciones de una viga. ox,oy esquina sup-izq de la elevacion."""
    b, h = bxh
    Ln = Ln_m * 1000.0
    esc_v = 1.0  # vertical real
    # ---- elevacion (la altura se exagera? no, 1:1) ----
    top = oy
    bot = oy - h
    # contorno de concreto
    msp.add_lwpolyline([(ox, top), (ox + Ln, top), (ox + Ln, bot), (ox, bot), (ox, top)],
                       dxfattribs={"layer": "CONCRETO", "closed": True})
    rec = 40
    # acero inferior (positivo) - corrida toda la luz + ldh a cada lado
    yinf = bot + rec
    msp.add_line((ox - 0, yinf), (ox + Ln, yinf), dxfattribs={"layer": "ACERO_INF"})
    # ganchos extremos inferiores (hacia arriba)
    msp.add_line((ox, yinf), (ox, yinf + 120), dxfattribs={"layer": "ACERO_INF"})
    msp.add_line((ox + Ln, yinf), (ox + Ln, yinf + 120), dxfattribs={"layer": "ACERO_INF"})
    add_text(msp, f"{n_inf} {db_inf} L={Linf_m:.2f} m  (inferior, corrida)",
             ox + Ln / 2, yinf - 90, 70, layer="ACERO_INF", align="CENTER")
    # acero superior (negativo) - baston en cada apoyo, largo Lsup
    ysup = top - rec
    Lsup = Lsup_m * 1000.0
    Lsup = min(Lsup, Ln * 0.45)  # para que se vea dentro de la luz
    msp.add_line((ox, ysup), (ox + Lsup, ysup), dxfattribs={"layer": "ACERO_SUP"})
    msp.add_line((ox + Ln - Lsup, ysup), (ox + Ln, ysup), dxfattribs={"layer": "ACERO_SUP"})
    # ganchos hacia abajo en apoyos
    for xx in (ox, ox + Ln):
        msp.add_line((xx, ysup), (xx, ysup - 120), dxfattribs={"layer": "ACERO_SUP"})
    add_text(msp, f"{n_sup} {db_sup} L={Lsup_m:.2f} m (superior, apoyos)",
             ox + Lsup / 2, ysup + 80, 65, layer="ACERO_SUP", align="CENTER")
    add_text(msp, f"{n_sup} {db_sup} L={Lsup_m:.2f} m",
             ox + Ln - Lsup / 2, ysup + 80, 65, layer="ACERO_SUP", align="CENTER")
    # estribos: lineas verticales. confinamiento en 2h desde cada apoyo
    z = min(zona2h, Ln / 2)
    x = ox
    # zona confinada izquierda
    xx = ox
    while xx <= ox + z:
        msp.add_line((xx, bot + 25), (xx, top - 25), dxfattribs={"layer": "ESTRIBOS"})
        xx += s_conf
    # zona central
    xc = ox + z
    while xc <= ox + Ln - z:
        msp.add_line((xc, bot + 25), (xc, top - 25), dxfattribs={"layer": "ESTRIBOS"})
        xc += s_centro
    # zona confinada derecha
    xx = ox + Ln - z
    while xx <= ox + Ln + 1:
        msp.add_line((min(xx, ox + Ln), bot + 25), (min(xx, ox + Ln), top - 25),
                     dxfattribs={"layer": "ESTRIBOS"})
        xx += s_conf
    # marcas de zona de confinamiento
    add_text(msp, f"Conf. 2h={zona2h:.0f}", ox + z / 2, bot - 70, 55, layer="ESTRIBOS", align="CENTER")
    add_text(msp, f"Est {est_tag} c/{s_conf:.0f} mm",
             ox + z / 2, bot - 130, 55, layer="ESTRIBOS", align="CENTER")
    add_text(msp, f"Est {est_tag} c/{s_centro:.0f} mm (centro)",
             ox + Ln / 2, bot - 70, 55, layer="ESTRIBOS", align="CENTER")
    # cota de longitud
    dim_horizontal(msp, ox, ox + Ln, bot - 180, f"Ln = {Ln_m:.2f} m")
    # titulo del grupo
    add_text(msp, f"{tag}  (seccion {b:.0f}x{h:.0f} mm)", ox, top + 230, 110, layer="ROTULO")
    # solicitaciones
    tor_txt = "torsion: si (At/s=%.2f)" % Ats if tors.startswith("SI") else "torsion: despreciable"
    add_text(msp,
             f"Mu(-)={Mneg:.0f}  Mu(+)={Mpos:.0f} kN.m   Vu={Vu:.0f} kN   {tor_txt}",
             ox, top + 120, 65, layer="TEXTO")

    # ---- secciones transversales (a la derecha) ----
    sx = ox + Ln + 700
    # seccion en apoyo (acero superior)
    draw_section(msp, sx, top, b, h, n_sup, n_inf, dbar_sup_mm, dbar_inf_mm,
                 est_tag, "SECCION EN APOYO")
    # seccion en centro
    draw_section(msp, sx + b + 900, top, b, h, 0, n_inf, dbar_sup_mm, dbar_inf_mm,
                 est_tag, "SECCION EN CENTRO", show_top_min=2, dbtop=dbar_sup_mm)


def draw_section(msp, sx, sy, b, h, n_top, n_bot, db_top, db_bot, est_tag, titulo,
                 show_top_min=0, dbtop=15.9):
    """Seccion transversal con barras y estribo."""
    bot = sy - h
    msp.add_lwpolyline([(sx, sy), (sx + b, sy), (sx + b, bot), (sx, bot), (sx, sy)],
                       dxfattribs={"layer": "CONCRETO", "closed": True})
    rec = 40
    # estribo (rectangulo interior)
    msp.add_lwpolyline([(sx + rec, sy - rec), (sx + b - rec, sy - rec),
                        (sx + b - rec, bot + rec), (sx + rec, bot + rec),
                        (sx + rec, sy - rec)],
                       dxfattribs={"layer": "ESTRIBOS", "closed": True})
    r = max(db_top, db_bot) / 2 + 3
    # barras superiores
    ntop = n_top if n_top > 0 else show_top_min
    if ntop > 0:
        xs = _spread(sx + rec + r + 5, sx + b - rec - r - 5, ntop)
        for xx in xs:
            msp.add_circle((xx, sy - rec - r - 3), r, dxfattribs={"layer": "ACERO_SUP"})
    # barras inferiores
    xs = _spread(sx + rec + r + 5, sx + b - rec - r - 5, n_bot)
    for xx in xs:
        msp.add_circle((xx, bot + rec + r + 3), r, dxfattribs={"layer": "ACERO_INF"})
    add_text(msp, titulo, sx + b / 2, sy + 110, 60, layer="TEXTO", align="CENTER")
    add_text(msp, f"{b:.0f}x{h:.0f}", sx + b / 2, bot - 90, 55, layer="COTAS", align="CENTER")
    if ntop > 0:
        lab = f"{n_top} sup" if n_top > 0 else f"{show_top_min} sup (montaje)"
        add_text(msp, lab, sx + b + 80, sy - rec - r, 50, layer="ACERO_SUP", align="LEFT")
    add_text(msp, f"{n_bot} inf", sx + b + 80, bot + rec + r, 50, layer="ACERO_INF", align="LEFT")


def _spread(x1, x2, n):
    if n <= 1:
        return [(x1 + x2) / 2]
    step = (x2 - x1) / (n - 1)
    return [x1 + step * i for i in range(n)]


# ---------------------------------------------------------------- viguetas T
def draw_vigueta(msp, ox, oy, *, tag, bw, h, hf, bf, Ln_m, n_sup, n_inf, db,
                 Mneg, Mpos, Vu, sin_estribos):
    Ln = Ln_m * 1000.0
    top = oy
    bot = oy - h
    # nervio + loseta (T) en elevacion: dibujamos el contorno del nervio
    msp.add_lwpolyline([(ox, top), (ox + Ln, top), (ox + Ln, bot), (ox, bot), (ox, top)],
                       dxfattribs={"layer": "CONCRETO", "closed": True})
    # loseta (linea de la parte superior, espesor hf)
    msp.add_line((ox, top - hf), (ox + Ln, top - hf), dxfattribs={"layer": "CONCRETO"})
    rec = 30
    # inferior corrido
    yinf = bot + rec
    msp.add_line((ox, yinf), (ox + Ln, yinf), dxfattribs={"layer": "ACERO_INF"})
    add_text(msp, f"{n_inf} {db} (inferior, corrida)", ox + Ln / 2, yinf - 70, 55,
             layer="ACERO_INF", align="CENTER")
    # superior en apoyos
    ysup = top - rec
    Lsup = min(Ln * 0.30, Ln / 4 + 200)
    msp.add_line((ox, ysup), (ox + Lsup, ysup), dxfattribs={"layer": "ACERO_SUP"})
    msp.add_line((ox + Ln - Lsup, ysup), (ox + Ln, ysup), dxfattribs={"layer": "ACERO_SUP"})
    add_text(msp, f"{n_sup} {db} (superior, apoyos)", ox + Ln / 2, ysup + 60, 50,
             layer="ACERO_SUP", align="CENTER")
    dim_horizontal(msp, ox, ox + Ln, bot - 150, f"Ln = {Ln_m:.2f} m")
    add_text(msp, f"{tag}  (T: bw={bw:.0f}, h={h:.0f}, loseta hf={hf:.0f}, bf={bf:.0f} mm)",
             ox, top + 180, 90, layer="ROTULO")
    est = "Sin estribos (Vu < phi 1.1 Vc)" if sin_estribos else "Con estribos"
    add_text(msp, f"Mu(-)={Mneg:.1f}  Mu(+)={Mpos:.1f} kN.m   Vu={Vu:.1f} kN   {est}",
             ox, top + 90, 55, layer="TEXTO")
    # seccion T a la derecha
    sx = ox + Ln + 700
    sy = top
    botS = sy - h
    # nervio
    msp.add_lwpolyline([(sx, sy - hf), (sx + bw, sy - hf), (sx + bw, botS),
                        (sx, botS), (sx, sy - hf)], dxfattribs={"layer": "CONCRETO", "closed": True})
    # loseta (ala)
    half = (bf - bw) / 2
    msp.add_lwpolyline([(sx - half, sy), (sx + bw + half, sy), (sx + bw + half, sy - hf),
                        (sx - half, sy - hf), (sx - half, sy)],
                       dxfattribs={"layer": "CONCRETO", "closed": True})
    r = db_area_to_r(db)
    xs = _spread(sx + 20, sx + bw - 20, n_inf)
    for xx in xs:
        msp.add_circle((xx, botS + 30 + r), r, dxfattribs={"layer": "ACERO_INF"})
    xs = _spread(sx + 20, sx + bw - 20, n_sup)
    for xx in xs:
        msp.add_circle((xx, sy - 25 - r), r, dxfattribs={"layer": "ACERO_SUP"})
    add_text(msp, "SECCION T", sx + bw / 2, sy + 120, 55, layer="TEXTO", align="CENTER")


def db_area_to_r(db):
    return {"Nº 3": 9.5, "Nº 4": 12.7, "Nº 5": 15.9}.get(db, 12.7) / 2 + 2


# ---------------------------------------------------------------- main
def build_vigas():
    doc = setup_doc(); msp = doc.modelspace()
    add_text(msp, "DESPIECE - VIGAS DE CARGA  VC 40x30 cm   (NSR-10 / DMO / R=5)",
             0, 1400, 160, layer="ROTULO")
    add_text(msp, "f'c=28 MPa  fy=420 MPa   Acero long. Nº 5 (db=15.9)   Estribos Nº 3 (db=9.5) 2 ramas, gancho 135",
             0, 1180, 80, layer="TEXTO")
    add_text(msp, "DIBUJO EN MILIMETROS (1:1).  ESCALA DE IMPRESION SUGERIDA 1:25",
             0, 1050, 75, layer="ROTULO")
    groups = [
        dict(tag="VC-1", n_sup=4, n_inf=3, Mneg=77, Mpos=58, Vu=70, tors="SI", Ats=0.0),
        dict(tag="VC-2", n_sup=6, n_inf=5, Mneg=118, Mpos=101, Vu=86, tors="SI", Ats=0.0),
        dict(tag="VC-3", n_sup=7, n_inf=4, Mneg=142, Mpos=79, Vu=108, tors="SI", Ats=0.0),
    ]
    dy = 0
    for g in groups:
        draw_beam(msp, 0, dy, tag=g["tag"], bxh=(300, 400), Ln_m=4.9,
                  n_sup=g["n_sup"], n_inf=g["n_inf"], db_sup="Nº5", db_inf="Nº5",
                  Lsup_m=1.52, Linf_m=5.71, s_conf=86, s_centro=171, zona2h=800,
                  est_tag="Nº3", Mneg=g["Mneg"], Mpos=g["Mpos"], Vu=g["Vu"],
                  tors=g["tors"], Ats=g["Ats"], d_mm=342.6, dbar_sup_mm=15.9, dbar_inf_mm=15.9)
        dy -= 1600
    title_block(msp, 0, dy - 100, 6000, [
        ("NOTAS GENERALES", True),
        ("1. Recubrimiento libre 40 mm. d = 342.6 mm.", False),
        ("2. Barras superiores (negativo) en apoyos: L = Ln/4 + ldh = 1.52 m (Nº5, ldh=303 mm).", False),
        ("3. Barras inferiores (positivo) corridas: L = Ln + 2 ldh = 5.71 m (Nº5).", False),
        ("4. Estribos Nº3: zona de confinamiento 2h=800 mm desde cada apoyo c/86 mm; resto c/171 mm.", False),
        ("5. Gancho sismico de estribo a 135 grados, extension 6db>=75 mm. Gancho de barra 90: 12db.", False),
        ("6. Disenado por capacidad (DMO): V de diseno = max(Vu, Ve).", False),
    ])
    scale_bar(msp, 0, dy - 1900)
    out = "Proyectos/Diseno-Estructural/Solucion/Despiece-Vigas-VC.dxf"
    doc.saveas(out); print("OK", out)


def build_riostras():
    doc = setup_doc(); msp = doc.modelspace()
    add_text(msp, "DESPIECE - VIGAS DE RIGIDEZ / RIOSTRAS  VR 40x35 cm   (NSR-10 / DMO / R=5)",
             0, 1400, 160, layer="ROTULO")
    add_text(msp, "f'c=28 MPa  fy=420 MPa   Acero long. Nº 5 (db=15.9)   Estribos Nº 3 (db=9.5) 2 ramas, gancho 135",
             0, 1180, 80, layer="TEXTO")
    add_text(msp, "DIBUJO EN MILIMETROS (1:1).  ESCALA DE IMPRESION SUGERIDA 1:25",
             0, 1050, 75, layer="ROTULO")
    groups = [
        dict(tag="VR-1", n_sup=5, n_inf=4, Mneg=100, Mpos=74, Vu=104, tors="SI", Ats=0.56),
        dict(tag="VR-2", n_sup=6, n_inf=5, Mneg=135, Mpos=98, Vu=133, tors="SI", Ats=0.27),
        dict(tag="VR-3", n_sup=9, n_inf=6, Mneg=186, Mpos=138, Vu=189, tors="No", Ats=0.0),
        dict(tag="VR-4", n_sup=12, n_inf=6, Mneg=243, Mpos=134, Vu=202, tors="SI", Ats=0.13),
    ]
    dy = 0
    for g in groups:
        draw_beam(msp, 0, dy, tag=g["tag"], bxh=(350, 400), Ln_m=5.1,
                  n_sup=g["n_sup"], n_inf=g["n_inf"], db_sup="Nº5", db_inf="Nº5",
                  Lsup_m=1.58, Linf_m=5.71, s_conf=86, s_centro=171, zona2h=800,
                  est_tag="Nº3", Mneg=g["Mneg"], Mpos=g["Mpos"], Vu=g["Vu"],
                  tors=g["tors"], Ats=g["Ats"], d_mm=342.6, dbar_sup_mm=15.9, dbar_inf_mm=15.9)
        dy -= 1600
    title_block(msp, 0, dy - 100, 6000, [
        ("NOTAS GENERALES", True),
        ("1. Recubrimiento libre 40 mm. d = 342.6 mm.", False),
        ("2. Barras superiores (negativo) en apoyos: L = Ln/4 + ldh = 1.58 m (Nº5).", False),
        ("3. Barras inferiores (positivo) corridas: L = Ln + 2 ldh = 5.71 m (Nº5).", False),
        ("4. Estribos Nº3: zona de confinamiento 2h=800 mm c/86 mm; resto c/171 mm.", False),
        ("5. VR-1, VR-2 y VR-4 requieren refuerzo por torsion (estribo cerrado + acero longitudinal adicional).", False),
        ("6. Disenado por capacidad (DMO): V de diseno = max(Vu, Ve).", False),
    ])
    scale_bar(msp, 0, dy - 1900)
    out = "Proyectos/Diseno-Estructural/Solucion/Despiece-Riostras-VR.dxf"
    doc.saveas(out); print("OK", out)


def build_viguetas():
    doc = setup_doc(); msp = doc.modelspace()
    add_text(msp, "DESPIECE - VIGUETAS  T 15x34 (loseta 6 cm)   (NSR-10, gravedad)",
             0, 1100, 150, layer="ROTULO")
    add_text(msp, "f'c=28 MPa  fy=420 MPa   Acero Nº 4 (db=12.7)   Sin estribos (Vu < phi 1.1 Vc)",
             0, 920, 75, layer="TEXTO")
    add_text(msp, "DIBUJO EN MILIMETROS (1:1).  ESCALA DE IMPRESION SUGERIDA 1:25",
             0, 800, 70, layer="ROTULO")
    # grupos de luz (se muestran los de entrepiso; cubierta mismo refuerzo 2Nº4)
    groups = [
        dict(tag="VT-1  L=1.85 m", Ln=1.85, Mneg=3.1, Mpos=2.2, Vu=9.6, bf=462),
        dict(tag="VT-2  L=3.25 m", Ln=3.25, Mneg=9.6, Mpos=6.8, Vu=16.9, bf=800),
        dict(tag="VT-3  L=4.45 m", Ln=4.45, Mneg=18.0, Mpos=12.8, Vu=23.2, bf=800),
        dict(tag="VT-4  L=4.80 m", Ln=4.80, Mneg=20.9, Mpos=14.9, Vu=25.0, bf=800),
    ]
    dy = 0
    for g in groups:
        draw_vigueta(msp, 0, dy, tag=g["tag"], bw=150, h=340, hf=60, bf=g["bf"],
                     Ln_m=g["Ln"], n_sup=2, n_inf=2, db="Nº 4",
                     Mneg=g["Mneg"], Mpos=g["Mpos"], Vu=g["Vu"], sin_estribos=True)
        dy -= 1100
    title_block(msp, 0, dy - 100, 6000, [
        ("NOTAS GENERALES - VIGUETAS", True),
        ("1. Seccion T: nervio 15 cm, altura total 34 cm, loseta 6 cm, separacion 80 cm.", False),
        ("2. Refuerzo: 2 Nº4 inferiores (corridas) y 2 Nº4 superiores en apoyos (continuidad).", False),
        ("3. No requieren estribos: el cortante actuante es menor que phi 1.1 Vc (=33.8 kN).", False),
        ("4. Longitud barra inferior = Ln + 2 ldh; superior en apoyos = Ln/4 + ldh (ldh Nº4=242 mm).", False),
        ("5. Las viguetas de cubierta llevan el mismo refuerzo (2 Nº4); las solicitaciones de", False),
        ("   gravedad son similares (wu cubierta=10.6 vs entrepiso=9.06 kN/m).", False),
    ])
    scale_bar(msp, 0, dy - 1900)
    out = "Proyectos/Diseno-Estructural/Solucion/Despiece-Viguetas.dxf"
    doc.saveas(out); print("OK", out)


if __name__ == "__main__":
    build_vigas()
    build_riostras()
    build_viguetas()

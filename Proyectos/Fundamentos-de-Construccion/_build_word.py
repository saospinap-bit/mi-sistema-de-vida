# -*- coding: utf-8 -*-
"""Genera el documento Word: explicacion detallada de la memoria de calculo."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

IMG = "_img"
AZUL = RGBColor(0x1F, 0x3B, 0x73)
GRIS = RGBColor(0x40, 0x40, 0x40)

doc = Document()

# --- estilos base ---
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)

def set_cell_bg(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)

def h(text, level=1):
    p = doc.add_heading(text, level=level)
    for r in p.runs:
        r.font.color.rgb = AZUL
    return p

def par(text, size=11, bold=False, italic=False, color=None, align=None, space_after=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold; r.italic = italic
    r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    if align is not None: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p

def add_img(name, width_cm=15, caption=None):
    path = os.path.join(IMG, name)
    if os.path.exists(path):
        doc.add_picture(path, width=Cm(width_cm))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            c = par(caption, size=9, italic=True, color=GRIS, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    else:
        par(f"[Falta imagen: {name}]", italic=True, color=RGBColor(0xC0,0,0))

# =====================================================================
# PORTADA
# =====================================================================
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("MEMORIA DE CÁLCULO DE CANTIDADES DE OBRA")
r.bold = True; r.font.size = Pt(22); r.font.color.rgb = AZUL
par("Explicación detallada del cálculo, origen de cada valor y planos de soporte",
    size=13, italic=True, color=GRIS, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

par("PROYECTO: Módulo 1 – Colegio", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
par("Asignatura: Fundamentos de Construcción – Universidad Nacional de Colombia", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
par("Etapa: Obra gris  |  Grupo 3", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
par("Norma de diseño: NSR-10  |  Sistema: Pórticos de concreto reforzado", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

# Nota destacada
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = p.add_run("Este documento explica CÓMO se obtuvo cada cantidad del archivo\n«MEMORIAS DE CALCULO.xlsx» y CUÁL plano usar como foto de referencia.")
rr.italic = True; rr.font.size = Pt(10.5); rr.font.color.rgb = GRIS

doc.add_page_break()

# =====================================================================
# 1. INTRODUCCION
# =====================================================================
h("1. Objetivo y alcance de este documento", 1)
par("El objetivo de este documento es explicar, de forma clara y trazable, cómo se calcularon "
    "las cantidades de obra consignadas en el formato de memoria de cálculo del proyecto "
    "(archivo MEMORIAS DE CALCULO.xlsx). Para cada actividad se indica:")
bullet("qué se está midiendo y en qué unidad;", "Actividad e ítem: ")
bullet("de qué plano y de qué cota sale cada dimensión (el soporte gráfico);", "Origen del valor: ")
bullet("la fórmula geométrica aplicada y el resultado;", "Cálculo: ")
bullet("cuál imagen/plano debe pegarse en la celda «IMAGEN/REFERENCIA» del formato.", "Foto de referencia: ")
par("El proyecto corresponde a la etapa de obra gris del Módulo 1 de un colegio, estructurado "
    "en pórticos de concreto reforzado con cimentación superficial (zapatas aisladas y vigas de "
    "cimentación), placa de contrapiso, columnas, vigas y placa de cubierta aligerada, muros de "
    "mampostería confinada y piso en adoquín.")

# =====================================================================
# 2. METODOLOGIA
# =====================================================================
h("2. Metodología general de cálculo de cantidades", 1)
par("Las cantidades de obra son la medición de cada actividad expresada en su unidad de pago. "
    "Toda la memoria se apoya en una tabla común con cuatro datos por renglón: Ancho, Alto (o "
    "espesor), Largo y Cantidad (número de elementos iguales). El total de cada renglón se obtiene "
    "multiplicando esos cuatro campos:")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = p.add_run("TOTAL = Ancho × Alto × Largo × Cantidad")
rr.bold = True; rr.font.size = Pt(13); rr.font.color.rgb = AZUL

par("Según la unidad de la actividad, algunos campos se dejan en 1 para que la fórmula entregue "
    "la unidad correcta:", space_after=4)
# tabla unidades
tb = doc.add_table(rows=1, cols=3); tb.style = "Light Grid Accent 1"; tb.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tb.rows[0].cells
hdr[0].text = "Unidad"; hdr[1].text = "Qué representa"; hdr[2].text = "Cómo se arma la fórmula"
for a,b,c in [
    ("M3 (volumen)", "Concreto, excavaciones, rellenos", "Ancho × Alto × Largo × Cantidad"),
    ("M2 (área)", "Placas, muros, geotextil, pañete, adoquín", "un campo = 1 (se usa Área × Cantidad o Ancho × Largo)"),
    ("ML (longitud)", "Columnetas de confinamiento", "Alto/Largo × Cantidad (Ancho = 1)"),
    ("KG (peso)", "Acero de refuerzo", "Longitud de varillas × peso lineal (kg/m)"),
]:
    row = tb.add_row().cells
    row[0].text = a; row[1].text = b; row[2].text = c
    for cc in row: cc.paragraphs[0].runs[0].font.size = Pt(10)
par("")
par("Las dimensiones NO se inventan: se leen directamente de los planos arquitectónicos y "
    "estructurales. Por eso el formato pide una «IMAGEN/REFERENCIA»: es el pantallazo del plano "
    "donde se ve la cota que se usó. A continuación se listan los planos base.", space_after=4)

# =====================================================================
# 3. PLANOS DE REFERENCIA
# =====================================================================
h("3. Planos de soporte (de aquí salen las dimensiones)", 1)
par("Estas son las imágenes de los planos entregados. Cada actividad de la memoria indica más "
    "adelante cuál de ellos usar como foto de referencia.")

add_img("plano_cimentacion.png", 16, "Figura 3.1. Planta de cimentación: ejes, vigas VC-A/VC-B (0.40×0.45), zapatas Z-1 (2.30×2.30) y Z-2 (2.15×2.15), y placa de piso e=0.10.")
add_img("plano_columnas.png", 16, "Figura 3.2. Planta y detalle de columnas: sección 0.40×0.40 m, altura libre 4.70–4.90 m, refuerzo 3#6 + estribos.")
add_img("plano_cubierta.png", 16, "Figura 3.3. Placa de cubierta: losa aligerada e=0.08 m en N+4.90, vigas de cubierta VG (0.40×0.50).")
add_img("plano_detalles_mamp.png", 16, "Figura 3.4. Detalles de mampostería confinada (muros, columnetas y confinamiento).")
add_img("plano_arquitectonico.png", 15, "Figura 3.5. Planta arquitectónica con las áreas de cada espacio (base para el área de adoquín y de acabados).")

doc.add_page_break()

# =====================================================================
# 4. CALCULO DETALLADO POR ITEM
# =====================================================================
h("4. Cálculo detallado por actividad", 1)
par("Para cada ítem se muestra la actividad, el origen de las dimensiones, la fórmula y el "
    "resultado tal como está en la memoria de cálculo (MEMORIAS DE CALCULO.xlsx).")

def item_block(cap, code, title, unit, plano_caption, dims, formula, resultado, obs=None, scheme=None, scheme_cap=None):
    h(f"Ítem {code} — {title}  ({unit})", 2)
    par(f"Capítulo: {cap}", size=10, italic=True, color=GRIS, space_after=4)
    # tabla origen de dimensiones
    par("Origen de cada valor (de dónde sale):", bold=True, space_after=2)
    tb = doc.add_table(rows=1, cols=2); tb.style = "Light List Accent 1"
    tb.rows[0].cells[0].text = "Dimensión / dato"
    tb.rows[0].cells[1].text = "De dónde se obtiene"
    for d, s in dims:
        row = tb.add_row().cells
        row[0].text = d; row[1].text = s
        for cc in row:
            for rn in cc.paragraphs[0].runs: rn.font.size = Pt(10)
    par("")
    par("Cálculo:", bold=True, space_after=2)
    p = doc.add_paragraph()
    rr = p.add_run(formula); rr.font.size = Pt(11.5); rr.bold = True; rr.font.color.rgb = AZUL
    p = doc.add_paragraph()
    rr = p.add_run(f"➜ Resultado: {resultado}")
    rr.bold = True; rr.font.size = Pt(11.5); rr.font.color.rgb = RGBColor(0x00,0x66,0x00)
    if obs:
        par(f"Observación: {obs}", size=10, italic=True, color=RGBColor(0xB0,0x60,0x00))
    if scheme:
        add_img(scheme, 15, scheme_cap)
    par(f"Foto de referencia para el formato: {plano_caption}", size=10, italic=True, color=GRIS, space_after=12)

# ---- CAPITULO 2: CIMENTACION ----
h("Capítulo 2 – Cimentación", 2)

item_block(
    "2. Cimentación", "2.1.1", "Excavación a máquina conglomerado 0–2 m (incl. retiro)", "M3",
    "Figura 3.1 (planta de cimentación) — se acota la huella del módulo y la profundidad de excavación.",
    [("Ancho = 9.85 m", "Ancho total de la huella del módulo (plano de cimentación / arquitectónico)."),
     ("Largo = 21.95 m", "Longitud total de la huella del módulo (mismo plano)."),
     ("Alto = 0.55 m", "Profundidad de la excavación masiva de la plataforma bajo la placa (perfil de rellenos: 0.20 recebo + 0.15 subbase + 0.10 placa + solado ≈ 0.55 m).")],
    "V = 9.85 × 0.55 × 21.95 × 1", "118.92 m³",
    scheme="esq_capas_placa.png",
    scheme_cap="Esquema 1. Corte del sistema de piso: la excavación (0.55 m) aloja recebo, sub-base y placa.")

item_block(
    "2. Cimentación", "2.1.2", "Relleno granular sub-base B-400", "M3",
    "Figura 3.1 + Esquema 1 (capa de sub-base).",
    [("Ancho = 9.85 m / Largo = 21.95 m", "Huella del módulo (igual que la excavación)."),
     ("Alto = 0.15 m", "Espesor de la capa de sub-base granular indicada en el perfil de piso.")],
    "V = 9.85 × 0.15 × 21.95 × 1", "32.44 m³")

item_block(
    "2. Cimentación", "2.1.3", "Excavación manual material común 0–2 m", "M3",
    "Figura 3.1 — anchos y luces de las zanjas de las vigas VC (0.40 m) y ejes.",
    [("Zanjas longitudinales: 0.40 × 0.40 × 19.80, cantidad 2", "Ancho de zanja 0.40 m; profundidad 0.40 m; longitud entre ejes 1 y 4 = 6.00+6.60+5.80+1.40 = 19.80 m; son 2 zanjas (ejes A y B)."),
     ("Zanjas transversales: 0.40 × 0.40 × 7.30, cantidad 5", "Luz libre transversal 7.30 m; 5 ejes (1, 2, 3, 3', 4).")],
    "V = (0.40×0.40×19.80×2) + (0.40×0.40×7.30×5) = 6.34 + 5.84", "12.18 m³")

item_block(
    "2. Cimentación", "2.1.4", "Relleno material común (recebo)", "M3",
    "Figura 3.1 + Esquema 1 (capa de recebo de nivelación).",
    [("Ancho = 9.85 m / Largo = 21.95 m", "Huella del módulo."),
     ("Alto = 0.20 m", "Espesor de la capa de recebo de nivelación bajo la placa.")],
    "V = 9.85 × 0.20 × 21.95 × 1", "43.24 m³")

item_block(
    "2. Cimentación", "2.1.6", "Geotextil NT 1600", "M2",
    "Figura 3.1 + Esquema 1 (línea verde del geotextil).",
    [("Ancho = 9.85 m / Largo = 21.95 m", "Huella del módulo (se coloca bajo toda la placa)."),
     ("Alto = 1", "Se deja en 1 porque el geotextil se mide por área, no por volumen.")],
    "A = 9.85 × 1 × 21.95 × 1", "216.21 m²")

item_block(
    "2. Cimentación", "2.2.1", "Vigas de cimentación concreto 3000 psi", "M3",
    "Figura 3.1 — sección de vigas VC-A/VC-B rotulada B=0.40 H=0.45.",
    [("Sección 0.40 × 0.45", "Dimensiones de la viga de cimentación (rótulo del plano: B=0.40, H=0.45)."),
     ("Long. = 19.80 m × 2", "Vigas longitudinales VC-A y VC-B (entre ejes 1 y 4)."),
     ("Transv. = 7.30 m × 5", "Vigas transversales VC-1..4 en los 5 ejes (luz libre 7.30 m).")],
    "V = (0.40×0.45×19.80×2) + (0.40×0.45×7.30×5) = 7.13 + 6.57", "13.70 m³",
    scheme="esq_viga_cim.png", scheme_cap="Esquema 3. Sección típica de viga de cimentación 0.40×0.45 sobre solado.")

item_block(
    "2. Cimentación", "2.2.2", "Concreto 1500 psi solado e=0.05", "M2",
    "Figura 3.1 + Esquema 3 (solado bajo vigas).",
    [("Ancho = 0.50 m", "Ancho del solado (10 cm más ancho que la viga a cada lado)."),
     ("Long. = 19.80 (×2) y 7.30 (×5)", "Mismo desarrollo de las vigas de cimentación."),
     ("Alto = 1", "El solado se mide por área (el espesor 0.05 va en el APU).")],
    "A = (0.50×1×19.80×2) + (0.50×1×7.30×5) = 19.80 + 18.25", "38.05 m²")

item_block(
    "2. Refuerzos / Acero", "2.3.1", "Acero figurado vigas de cimentación", "KG",
    "Figura 3.1 — despiece: refuerzo longitudinal 3#6 + 3#5 y estribos #3 c/0.20.",
    [("Refuerzo longitudinal 3#6 + 3#5", "Barras indicadas en el despiece de las vigas de cimentación (cuadro de hierros del plano)."),
     ("Estribos #3 c/0.20 m", "Separación de estribos indicada en el plano."),
     ("Peso por metro", "#6 = 2.235 kg/m ; #5 = 1.552 kg/m ; #3 = 0.559 kg/m (tabla estándar de aceros)."),
     ("+10 %", "Desperdicio y traslapos.")],
    "Long. 3#6+3#5 = 864.6 kg  +  Estribos #3 = 319.6 kg  =  1 184.2 kg  ×1.10",
    "1 302.6 kg",
    obs="El acero se obtiene sumando la longitud de cada tipo de varilla del despiece × su peso lineal (kg/m), y se añade 10 % por desperdicio y traslapos.")

# ---- CAPITULO 4: ESTRUCTURA ----
doc.add_page_break()
h("Capítulo 4 – Estructura en concreto", 2)

item_block(
    "4. Estructura", "4.1.1", "Columnas concreto 3000 psi", "M3",
    "Figura 3.2 (planta y detalle de columnas): sección 0.40×0.40, altura 4.90.",
    [("Sección 0.40 × 0.40", "Dimensión de la columna tipo (rótulo del plano: B=0.40 H=0.40)."),
     ("Alto = 4.90 m", "Altura libre de la columna (del nivel de cimentación a la viga de cubierta N+4.90)."),
     ("Cantidad = 10", "Número de columnas del módulo (5 ejes × 2 líneas A y B).")],
    "V = 0.40 × 0.40 × 4.90 × 10", "7.84 m³",
    scheme="esq_columna.png", scheme_cap="Esquema 4. Columna tipo 0.40×0.40, h=4.90 m (10 unidades).")

item_block(
    "4. Estructura", "4.2.1", "Concreto 3000 psi viga cubierta / cinta", "M3",
    "Figura 3.3 (placa de cubierta): vigas VG rotuladas B=0.40 H=0.50.",
    [("Sección 0.40 × 0.50", "Dimensión de la viga de cubierta (rótulo del plano de cubierta)."),
     ("Long. = 19.80 m × 2", "Vigas longitudinales sobre ejes A y B."),
     ("Transv. = 7.30 m × 5", "Vigas transversales en los 5 ejes.")],
    "V = (0.40×0.50×19.80×2) + (0.40×0.50×7.30×5) = 7.92 + 7.30", "15.22 m³")

item_block(
    "4. Estructura", "4.3.1", "Placa de concreto contrapiso", "M3",
    "Figura 3.1 (placa de piso e=0.10) + Esquema 1.",
    [("Ancho = 9.85 m / Largo = 21.95 m", "Huella del módulo."),
     ("Alto = 0.10 m", "Espesor de la placa de contrapiso (rótulo del plano de cimentación).")],
    "V = 9.85 × 0.10 × 21.95 × 1", "21.62 m³")

item_block(
    "4. Estructura", "4.3.3.1", "Placas de cubierta en concreto", "M2",
    "Figura 3.3 (placa aligerada e=0.08) + Esquema 5.",
    [("Ancho = 7.30 m", "Ancho de la placa (luz transversal)."),
     ("Largo = 5.55 + 6.10 + 6.87 = 18.52 m", "Suma de los tramos de la cubierta a lo largo del módulo."),
     ("Espesor = 0.08 m", "Espesor de la losa aligerada (rótulo del plano de cubierta)."),
     ("Viguetas 0.20 × 0.32, largo 18.52, cantidad 6", "Nervios/viguetas de la losa aligerada.")],
    "Placa = 7.30×0.08×18.52  +  Viguetas = 0.20×0.32×18.52×6",
    "Placa 10.82 + viguetas 7.11  (según memoria)",
    obs="En el formato la unidad aparece como M2 pero la fórmula incluye el espesor (queda en volumen). Verifica con tu profesor si la placa aligerada se paga por área (7.30×18.52 ≈ 135.2 m²) o por volumen de concreto; ajusta según el APU 4.3.3.",
    scheme="esq_cubierta.png", scheme_cap="Esquema 5. Placa de cubierta aligerada 7.30×18.52, e=0.08, con 6 viguetas.")

item_block(
    "4. Refuerzos / Acero", "4.7.1", "Acero figurado columnas", "KG",
    "Figura 3.2 (despiece de columnas): 2#6 + 2#7, L≈5.95 m, estribos.",
    [("Long. 10 col × (2#6 + 2#7), L=5.95 m", "Refuerzo longitudinal de las 10 columnas (despiece del plano)."),
     ("Estribos #2 c/0.20 m", "Confinamiento indicado en el detalle."),
     ("+10 %", "Desperdicio y traslapos.")],
    "Long. = 628 kg  +  Estribos = 91.9 kg  =  719.8 kg  ×1.10", "791.8 kg")

item_block(
    "4. Refuerzos / Acero", "4.8.1", "Acero figurado vigas de cubierta", "KG",
    "Figura 3.3 (despiece de vigas de cubierta): 2#6 + 2#7 + 2#6, estribos #3 c/0.15.",
    [("Long. 2#6 + 2#7 + 2#6", "Refuerzo longitudinal de las vigas de cubierta."),
     ("Estribos #3 c/0.15 m", "Separación de estribos del plano."),
     ("+10 %", "Desperdicio y traslapos.")],
    "Long. = 1 143.3 kg  +  Estribos = 454.6 kg  =  1 597.9 kg  ×1.10", "1 757.7 kg")

# ---- CAPITULO 5: MAMPOSTERIA ----
doc.add_page_break()
h("Capítulo 5 – Mampostería", 2)

item_block(
    "5. Mampostería", "5.1.1", "Muros bloque hueco No. 4", "M2",
    "Figura 3.4 / plano de mampostería — se miden las longitudes de todos los muros y su altura.",
    [("Longitud total = 173.60 m", "Suma de la longitud de todos los muros del módulo (medida sobre el plano de mampostería)."),
     ("Alto = 2.90 m", "Altura libre del muro (piso a viga de cubierta)."),
     ("Descuento de vanos = 20 %", "Se resta el área de puertas y ventanas (aprox. 20 % del área bruta).")],
    "A = (173.60×1×2.90×1) − (173.60×1×2.90×0.20) = 503.44 − 100.69", "402.75 m²",
    scheme="esq_muro.png", scheme_cap="Esquema 6. Elevación de muro: área bruta menos 20 % de vanos.")

item_block(
    "5. Mampostería", "5.1.2", "Columneta de confinamiento No. 5", "ML",
    "Figura 3.4 (detalles de confinamiento) — columnetas cada 3 m.",
    [("Cantidad = 58", "Número de columnetas de confinamiento (una cada ≈3 m a lo largo de los muros)."),
     ("Alto = 2.90 m", "Altura de cada columneta (igual a la del muro)."),
     ("Ancho = 1", "Se mide por longitud (metro lineal).")],
    "L = 1 × 1 × 2.90 × 58", "168.20 ml")

item_block(
    "5. Mampostería", "5.1.4", "Pañete liso impermeabilizado 1:4", "M2",
    "Figura 3.4 — se pañeta un porcentaje del área de muro.",
    [("Área de muro = 402.75 m²", "Tomada del ítem 5.1.1 (muros)."),
     ("Factor = 65 %", "Porcentaje del área de muro que lleva pañete (según alcance).")],
    "A = 402.75 × 1 × 0.65 × 1", "261.79 m²")

item_block(
    "5. Refuerzos / Acero", "5.2.1", "Acero mampostería confinada", "KG",
    "Figura 3.4 (despiece de confinamiento): 4#3 longitudinal, estribos #2 c/0.20.",
    [("Long. 4#3", "Refuerzo longitudinal de columnetas y vigas de confinamiento."),
     ("Estribos #2 c/0.20 m", "Confinamiento del plano de detalles."),
     ("+10 %", "Desperdicio y traslapos.")],
    "Long. = 376.8 kg  +  Estribos = 105.1 kg  =  481.9 kg  ×1.10", "530.1 kg")

# ---- CAPITULO 8: PISOS ----
doc.add_page_break()
h("Capítulo 8 – Pisos", 2)

item_block(
    "8. Pisos", "8.1.1", "Adoquín en concreto 0.20×0.10×0.06 m (suministro e instalación)", "M2",
    "Figura 3.5 (planta arquitectónica) — se suman las áreas de las zonas que van en adoquín.",
    [("9 áreas parciales (m²)", "Se toma el área de cada zona/espacio del plano arquitectónico o de adoquín: 18.62 + 17.49 + 22.25 + 7.76 + 14.60 + 15.00 + 1.91 + 1.91 + 15.76."),
     ("Cantidad = 1 c/u", "Cada área se cuenta una vez.")],
    "A = 18.62+17.49+22.25+7.76+14.60+15.00+1.91+1.91+15.76", "115.30 m²",
    obs="Cada área se lee/mide directamente sobre el plano de adoquín o arquitectónico; conviene pegar el pantallazo con esas zonas resaltadas.")

# =====================================================================
# 5. RESUMEN
# =====================================================================
doc.add_page_break()
h("5. Resumen de cantidades de obra", 1)
par("Tabla consolidada de las cantidades calculadas (tal como quedan en la memoria):")
resumen = [
    ("2.1.1","Excavación a máquina 0–2 m","M3","118.92"),
    ("2.1.2","Relleno sub-base B-400","M3","32.44"),
    ("2.1.3","Excavación manual","M3","12.18"),
    ("2.1.4","Relleno común (recebo)","M3","43.24"),
    ("2.1.6","Geotextil NT 1600","M2","216.21"),
    ("2.2.1","Vigas de cimentación 3000 psi","M3","13.70"),
    ("2.2.2","Solado 1500 psi e=0.05","M2","38.05"),
    ("2.3.1","Acero vigas de cimentación","KG","1 302.6"),
    ("4.1.1","Columnas 3000 psi","M3","7.84"),
    ("4.2.1","Vigas de cubierta 3000 psi","M3","15.22"),
    ("4.3.1","Placa de contrapiso","M3","21.62"),
    ("4.3.3.1","Placa de cubierta aligerada","M2","ver ítem"),
    ("4.7.1","Acero columnas","KG","791.8"),
    ("4.8.1","Acero vigas de cubierta","KG","1 757.7"),
    ("5.1.1","Muros bloque No.4","M2","402.75"),
    ("5.1.2","Columneta de confinamiento","ML","168.20"),
    ("5.1.4","Pañete liso impermeabilizado","M2","261.79"),
    ("5.2.1","Acero mampostería confinada","KG","530.1"),
    ("8.1.1","Adoquín en concreto","M2","115.30"),
]
tb = doc.add_table(rows=1, cols=4); tb.style = "Medium Shading 1 Accent 1"
hc = tb.rows[0].cells
for i,tx in enumerate(["Ítem","Actividad","Und","Cantidad"]):
    hc[i].text = tx
for it,de,un,ca in resumen:
    row = tb.add_row().cells
    row[0].text=it; row[1].text=de; row[2].text=un; row[3].text=ca
    for cc in row:
        for rn in cc.paragraphs[0].runs: rn.font.size = Pt(9.5)

# =====================================================================
# 6. COMO LLENAR LA COLUMNA IMAGEN/REFERENCIA
# =====================================================================
doc.add_page_break()
h("6. Cómo llenar la columna «IMAGEN/REFERENCIA» del formato", 1)
par("El formato de memoria de cálculo tiene, a la izquierda de cada renglón, una casilla llamada "
    "«IMAGEN/REFERENCIA». Ahí es donde el profesor pide la «foto de dónde saliste el dato». "
    "El procedimiento es:")
bullet("Abre el plano PDF correspondiente al ítem (ver la figura indicada en cada bloque de este documento).")
bullet("Haz un recorte/pantallazo de la zona donde se ve la cota o la dimensión usada (ej.: el rótulo B=0.40 H=0.45 de la viga, la altura 4.90 de la columna, la longitud entre ejes, etc.).")
bullet("Pega ese recorte en la casilla IMAGEN/REFERENCIA de ese ítem en el Excel.")
par("Correspondencia rápida ítem → plano:", bold=True, space_after=2)
tb = doc.add_table(rows=1, cols=2); tb.style = "Light Grid Accent 1"
tb.rows[0].cells[0].text = "Ítems"; tb.rows[0].cells[1].text = "Plano a recortar"
for a,b in [
    ("2.1.1 / 2.1.2 / 2.1.4 / 2.1.6 / 4.3.1", "Planta de cimentación + corte de piso (Figura 3.1 / Esquema 1)"),
    ("2.1.3 / 2.2.1 / 2.2.2 / 2.3.1", "Planta de cimentación – vigas VC y despiece (Figura 3.1)"),
    ("4.1.1 / 4.7.1", "Planta y detalle de columnas (Figura 3.2)"),
    ("4.2.1 / 4.3.3.1 / 4.8.1", "Placa de cubierta y vigas VG (Figura 3.3)"),
    ("5.1.1 / 5.1.2 / 5.1.4 / 5.2.1", "Detalles de mampostería / fachada (Figura 3.4)"),
    ("8.1.1", "Planta arquitectónica / adoquín con áreas (Figura 3.5)"),
]:
    row = tb.add_row().cells
    row[0].text=a; row[1].text=b
    for cc in row:
        for rn in cc.paragraphs[0].runs: rn.font.size = Pt(10)

par("")
par("Nota final: todas las dimensiones de este documento provienen de los planos entregados y "
    "coinciden con las fórmulas del archivo MEMORIAS DE CALCULO.xlsx. Si el profesor pide ajustar "
    "un porcentaje (vanos, pañete) o un espesor, basta con cambiar ese dato en el renglón y la "
    "cantidad se recalcula sola.", size=10, italic=True, color=GRIS)

out = "EXPLICACION - Memoria de Calculo - Cantidades de Obra.docx"
doc.save(out)
print("DOCUMENTO GUARDADO:", out, "| tamano:", os.path.getsize(out)//1024, "KB")

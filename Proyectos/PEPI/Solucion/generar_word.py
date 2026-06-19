# -*- coding: utf-8 -*-
"""
Genera el informe PEPI en formato Word (.docx) a partir de los datos del proyecto.
Requiere: python-docx
Ejecutar:  python3 generar_word.py  -> crea INFORME_PEPI.docx
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AZUL = RGBColor(0x1F, 0x4E, 0x79)
GRIS = RGBColor(0x59, 0x59, 0x59)

doc = Document()

base = doc.styles["Normal"]
base.font.name = "Calibri"
base.font.size = Pt(11)

def shade_cell(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)

def set_cell_text(cell, text, bold=False, white=False, size=10, align="left"):
    cell.text = ""
    p = cell.paragraphs[0]
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(str(text))
    run.bold = bold
    run.font.size = Pt(size)
    if white:
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

def add_table(headers, rows, col_align=None, header_fill="1F4E79"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for j, h in enumerate(headers):
        shade_cell(hdr[j], header_fill)
        set_cell_text(hdr[j], h, bold=True, white=True, size=9, align="center")
    for r in rows:
        cells = t.add_row().cells
        for j, val in enumerate(r):
            al = col_align[j] if col_align else "left"
            set_cell_text(cells[j], val, size=9, align=al)
    doc.add_paragraph()
    return t

def h1(text):
    p = doc.add_heading(level=1)
    run = p.add_run(text)
    run.font.color.rgb = AZUL
    run.font.size = Pt(15)

def h2(text):
    p = doc.add_heading(level=2)
    run = p.add_run(text)
    run.font.color.rgb = AZUL
    run.font.size = Pt(12)

def para(text, italic=False, size=11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.italic = italic
    run.font.size = Pt(size)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

# PORTADA
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("INFORME DE PREPARACIÓN Y EVALUACIÓN\nDE PROYECTOS DE INGENIERÍA (PEPI)")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = AZUL

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
rs = sub.add_run("Construcción de PTAP y ampliación del sistema de acueducto\ndel municipio de El Progreso")
rs.font.size = Pt(13)
rs.font.color.rgb = GRIS
doc.add_paragraph()
note = doc.add_paragraph()
note.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn = note.add_run("Cifras monetarias en millones de pesos colombianos (COP MM) salvo indicación contraria.")
rn.italic = True
rn.font.size = Pt(9)
doc.add_paragraph()

# 1. RESUMEN EJECUTIVO
h1("1. Resumen Ejecutivo")
para("El municipio de El Progreso (≈18.000 habitantes, con proyección a 25.000 en 20 años) presenta un déficit "
     "crónico en la prestación del servicio de acueducto: cobertura del 78 %, índice de agua no contabilizada "
     "(IANC) del 48 % y una planta de tratamiento obsoleta que opera por encima de su capacidad de diseño, lo "
     "que genera intermitencia en el suministro y riesgo sanitario.")
para("El proyecto consiste en la construcción de una nueva Planta de Tratamiento de Agua Potable (PTAP) de "
     "120 L/s, la ampliación y rehabilitación de las redes de aducción, conducción y distribución, y la "
     "incorporación de estaciones de bombeo, tanques de almacenamiento y micromedición. El objetivo central es "
     "garantizar agua potable continua (24 h) y de calidad al 98 % de la población, reduciendo el IANC al 25 % "
     "y eliminando los racionamientos.")
para("La inversión total (CAPEX) asciende a COP 14.000 MM, financiada en un 60 % con deuda (banca de desarrollo / "
     "FINDETER) y 40 % con equity (operador especializado + municipio). Con un WACC de 11,07 %, el proyecto "
     "presenta un VPN de COP 8.376 MM y una TIR del 18,13 % a nivel de proyecto; desde la óptica del inversionista "
     "la TIR es 24,78 % con un VPN de COP 4.698 MM. Los indicadores confirman que el proyecto es financiera y "
     "económicamente viable, además de socialmente prioritario.")
add_table(
    ["Indicador", "Valor"],
    [["Horizonte de evaluación", "20 años"],
     ["CAPEX", "COP 14.000 MM"],
     ["Estructura Deuda / Equity", "60 % / 40 %"],
     ["WACC", "11,07 %"],
     ["VPN del proyecto (@WACC)", "COP 8.376 MM"],
     ["TIR del proyecto", "18,13 %"],
     ["VPN del inversionista (@Ke)", "COP 4.698 MM"],
     ["TIR del inversionista", "24,78 %"]],
    col_align=["left", "right"])

def add_image_centered(path, width_inches=6.3):
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(path, width=Inches(width_inches))
    else:
        para("[No se encontro la imagen: " + path + ". Ejecuta generar_arboles.py]", italic=True, size=9)

# 2. ARBOL DE PROBLEMAS
h1("2. Árbol de Problemas")
para("Problema central: Deficiente prestación del servicio de acueducto en el municipio de El Progreso. "
     "Los efectos (consecuencias) se ubican en la parte superior y las causas en la parte inferior.")
add_image_centered("arbol_problemas.png")

# 3. ARBOL DE OBJETIVOS
h1("3. Árbol de Objetivos")
para("Objetivo central: Mejorar la prestación del servicio de acueducto en el municipio de El Progreso. "
     "Es el espejo en positivo del árbol de problemas: cada causa se convierte en un medio y cada efecto en un fin.")
add_image_centered("arbol_objetivos.png")

# 4. MML
h1("4. Matriz de Marco Lógico (MML)")
add_table(
    ["Nivel", "Resumen narrativo", "Indicadores", "Medios de verificación", "Supuestos"],
    [["FIN", "Contribuir al desarrollo social y económico mejorando la salud pública.",
      "Reducción 40 % en EDA a 3 años; aumento del IDM.",
      "Reportes Secretaría de Salud; DANE/SIVIGILA.",
      "Estabilidad política y continuidad de la inversión social."],
     ["PROPÓSITO", "Garantizar servicio continuo (24 h), con calidad y cobertura 98 %.",
      "Cobertura ≥ 98 %; continuidad 24 h; IRCA < 5 %; IANC ≤ 25 %.",
      "Informes SUI–SSPD; reportes IRCA; auditorías.",
      "La población se conecta y paga la tarifa."],
     ["COMPONENTES", "1) PTAP 120 L/s. 2) Redes ampliadas. 3) Micromedición. 4) Bombeo y tanques.",
      "PTAP operando; km de red renovada; N° de medidores.",
      "Actas de recibo; pruebas; inventario de activos.",
      "Disponibilidad de predios, permisos y energía."],
     ["ACTIVIDADES", "Estudios; gestión predial/ambiental; construcción; equipos; puesta en marcha.",
      "Avance físico vs. cronograma; ejecución CAPEX 14.000 MM.",
      "Informes de interventoría; cortes de obra.",
      "Cierre financiero; clima y orden público normales."]],
    col_align=["center", "left", "left", "left", "left"])

# 5. SOLUCION DE INGENIERIA
h1("5. Solución de Ingeniería Propuesta")
para("1. Planta de Tratamiento de Agua Potable (PTAP) – 120 L/s. Planta convencional compacta-modular con "
     "coagulación, floculación, sedimentación de alta tasa, filtración rápida y desinfección por cloración, "
     "dimensionada para el caudal máximo diario a 20 años. Incluye dosificación automatizada y laboratorio de "
     "control de calidad para garantizar IRCA < 5 % (Resolución 2115 de 2007).")
para("2. Aducción y conducción. Renovación de la línea de aducción desde la bocatoma y conducción a presión hasta "
     "los tanques, con tubería PVC/HD de diámetros calculados hidráulicamente (Hazen-Williams) para minimizar "
     "pérdidas y garantizar presiones de servicio.")
para("3. Almacenamiento, bombeo y distribución. Tanques con capacidad equivalente al 30 % del volumen diario, "
     "estaciones de bombeo con bombas de alta eficiencia y variadores de frecuencia, y sectorización de la red en "
     "distritos hidráulicos para control de presiones y pérdidas.")
para("4. Reducción de pérdidas y micromedición. Instalación masiva de micromedidores, macromedición por sector y "
     "un programa permanente de detección de fugas y control de conexiones fraudulentas, para bajar el IANC del "
     "48 % al 25 %.")

# 6. ANALISIS FINANCIERO
h1("6. Análisis de Viabilidad Financiera y Económica")
h2("6.1 Estructura de Inversión y Costos (CAPEX / OPEX)")
para("CAPEX — Inversión inicial: COP 14.000 MM (año 0).")
add_table(
    ["Componente", "COP MM", "%"],
    [["PTAP (obra civil + equipos)", "6.300", "45,0 %"],
     ["Ampliación red de aducción y conducción", "2.800", "20,0 %"],
     ["Estaciones de bombeo y tanques", "2.100", "15,0 %"],
     ["Redes de distribución y micromedición", "1.900", "13,6 %"],
     ["Estudios, diseños e interventoría", "900", "6,4 %"],
     ["Total CAPEX", "14.000", "100 %"]],
    col_align=["left", "right", "right"])
para("OPEX — Costos de operación (año 1): COP 2.350 MM, con crecimiento del 4 % anual (energía de bombeo, químicos, "
     "personal, mantenimiento y costos administrativos/comerciales). Ingresos por tarifa de acueducto: COP 5.200 MM "
     "en el año 1, con crecimiento del 4,5 % anual.")

h2("6.2 Estructura de Deuda + Equity")
add_table(
    ["Fuente", "Monto (COP MM)", "Participación", "Costo"],
    [["Deuda (banca de desarrollo / FINDETER)", "8.400", "60 %", "Kd = 12,5 %"],
     ["Equity (operador + municipio)", "5.600", "40 %", "Ke = 15,5 %"],
     ["Total", "14.000", "100 %", "—"]],
    col_align=["left", "right", "center", "center"])
para("La deuda se amortiza por el sistema francés (cuota fija) a 10 años, con una cuota anual de COP 1.517,2 MM. "
     "La tasa de impuesto de renta aplicada es del 35 %.")

h2("6.3 Cálculo del WACC")
para("WACC = (E/V)·Ke + (D/V)·Kd·(1 − t)")
para("WACC = (0,40 × 0,155) + (0,60 × 0,125 × (1 − 0,35)) = 0,0620 + 0,04875 = 0,1108 ≈ 11,07 %")

h2("6.4 Indicadores de Rentabilidad — VPN y TIR")
add_table(
    ["Óptica", "Tasa de descuento", "VPN (COP MM)", "TIR", "Criterio"],
    [["Proyecto (FCLP)", "WACC = 11,07 %", "8.376", "18,13 %", "TIR > WACC → viable"],
     ["Inversionista (FCLA)", "Ke = 15,5 %", "4.698", "24,78 %", "TIR > Ke → viable"]],
    col_align=["left", "center", "right", "right", "left"])
para("Ambos VPN son positivos y ambas TIR superan su respectiva tasa de descuento, por lo que el proyecto crea "
     "valor. El apalancamiento mejora la rentabilidad del inversionista (24,78 % vs. 18,13 %) por el escudo fiscal "
     "de los intereses y el menor costo relativo de la deuda.")

h2("6.5 Flujos de Caja (Proyecto, Inversionistas y Banco)")
flujos = [
    ["0", "—", "—", "—", "—", "—", "-14.000", "-5.600", "+8.400"],
    ["1", "5.200", "2.350", "2.850", "1.050", "467", "2.098", "948", "-1.517"],
    ["2", "5.434", "2.444", "2.990", "992", "526", "2.188", "1.018", "-1.517"],
    ["3", "5.679", "2.542", "3.137", "926", "591", "2.284", "1.091", "-1.517"],
    ["4", "5.934", "2.643", "3.291", "852", "665", "2.384", "1.165", "-1.517"],
    ["5", "6.201", "2.749", "3.452", "769", "748", "2.489", "1.241", "-1.517"],
    ["6", "6.480", "2.859", "3.621", "675", "842", "2.599", "1.318", "-1.517"],
    ["7", "6.772", "2.973", "3.798", "570", "947", "2.714", "1.396", "-1.517"],
    ["8", "7.076", "3.092", "3.984", "452", "1.066", "2.835", "1.475", "-1.517"],
    ["9", "7.395", "3.216", "4.179", "318", "1.199", "2.961", "1.555", "-1.517"],
    ["10", "7.728", "3.345", "4.383", "169", "1.349", "3.094", "1.636", "-1.517"],
    ["11", "8.075", "3.479", "4.597", "0", "0", "3.233", "3.233", "0"],
    ["12", "8.439", "3.618", "4.821", "0", "0", "3.379", "3.379", "0"],
    ["13", "8.819", "3.762", "5.056", "0", "0", "3.532", "3.532", "0"],
    ["14", "9.215", "3.913", "5.302", "0", "0", "3.692", "3.692", "0"],
    ["15", "9.630", "4.069", "5.561", "0", "0", "3.859", "3.859", "0"],
    ["16", "10.063", "4.232", "5.831", "0", "0", "4.035", "4.035", "0"],
    ["17", "10.516", "4.402", "6.115", "0", "0", "4.220", "4.220", "0"],
    ["18", "10.990", "4.578", "6.412", "0", "0", "4.413", "4.413", "0"],
    ["19", "11.484", "4.761", "6.723", "0", "0", "4.615", "4.615", "0"],
    ["20", "12.001", "4.951", "7.050", "0", "0", "4.827", "4.827", "0"],
]
add_table(
    ["Año", "Ingresos", "OPEX", "EBITDA", "Interés", "Amort.", "FC Proyecto", "FC Inv.", "FC Banco"],
    flujos,
    col_align=["center"] + ["right"] * 8)
para("Flujo del Proyecto (FCLP): rentabilidad de la inversión total, descontado al WACC. Flujo del Inversionista "
     "(FCLA): lo que queda al accionista tras pagar intereses y amortizar deuda, descontado al Ke. Flujo del Banco: "
     "desembolsa COP 8.400 MM en el año 0 y recibe la cuota fija durante 10 años (TIR = Kd = 12,5 %).", italic=True, size=9)

# 7. MATRIZ DE RIESGOS
h1("7. Matriz de Riesgos (20 riesgos)")
para("Escala: Probabilidad (P) e Impacto (I) de 1 a 5. Nivel de riesgo = P × I. "
     "Clasificación: Bajo (1–6), Medio (8–12), Alto (15–25).", italic=True, size=9)
riesgos = [
    ["1", "Sobrecostos en la construcción", "Financiero", "4", "4", "16", "Alto"],
    ["2", "Retrasos en el cronograma de obra", "Operativo", "4", "3", "12", "Medio"],
    ["3", "Demoras en gestión predial y servidumbres", "Legal", "3", "4", "12", "Medio"],
    ["4", "Variación en la tasa de cambio", "Financiero", "3", "3", "9", "Medio"],
    ["5", "Incremento de tasas de interés", "Financiero", "3", "4", "12", "Medio"],
    ["6", "Recaudo tarifario inferior al proyectado", "Comercial", "4", "4", "16", "Alto"],
    ["7", "Cambios regulatorios en el marco tarifario", "Regulatorio", "2", "4", "8", "Medio"],
    ["8", "Contaminación de la fuente de captación", "Ambiental", "3", "5", "15", "Alto"],
    ["9", "Reducción del caudal (sequía/cambio climático)", "Ambiental", "3", "5", "15", "Alto"],
    ["10", "Inadecuada disposición de lodos de la PTAP", "Ambiental", "3", "4", "12", "Medio"],
    ["11", "Vertimiento de aguas de lavado sin tratar", "Ambiental", "3", "4", "12", "Medio"],
    ["12", "Afectación de fauna/flora en zona de obras", "Ambiental", "2", "3", "6", "Bajo"],
    ["13", "Fallas o paradas de equipos de bombeo", "Operativo", "3", "3", "9", "Medio"],
    ["14", "Interrupción del suministro eléctrico", "Operativo", "3", "4", "12", "Medio"],
    ["15", "Accidentes laborales en obra", "SST", "3", "4", "12", "Medio"],
    ["16", "Oposición o conflicto con la comunidad", "Social", "3", "3", "9", "Medio"],
    ["17", "Vandalismo o robo de infraestructura", "Seguridad", "3", "2", "6", "Bajo"],
    ["18", "Errores en estudios y diseños técnicos", "Técnico", "2", "4", "8", "Medio"],
    ["19", "Incumplimiento del contratista", "Contractual", "2", "4", "8", "Medio"],
    ["20", "Inflación de costos operativos", "Financiero", "3", "3", "9", "Medio"],
]
add_table(
    ["#", "Riesgo", "Tipo", "P", "I", "P×I", "Nivel"],
    riesgos,
    col_align=["center", "left", "left", "center", "center", "center", "center"])
para("Resumen: 4 riesgos Altos, 14 Medios y 2 Bajos. Los Altos se concentran en sobrecostos, recaudo y los "
     "factores ambientales de la fuente.")

# 8. INTERVENCION DE 10 RIESGOS
h1("8. Intervención de 10 Riesgos (5 ambientales) y Recalificación")
para("Se intervienen los 10 riesgos prioritarios; los riesgos 8, 9, 10, 11 y 12 son de tipo ambiental "
     "(5 ambientales, según lo exigido).")
h2("8.1 Descripción de las intervenciones")
inter = [
    ["1", "Sobrecostos de construcción", "Financiero", "Contrato a precio global fijo (EPC), contingencia del 10 % y control de cambios por interventoría."],
    ["6", "Bajo recaudo tarifario", "Comercial", "Cultura de pago, financiación de cartera, corte por mora y micromedición masiva."],
    ["5", "Alza de tasas de interés", "Financiero", "Cobertura con tasa fija / SWAP en el cierre financiero."],
    ["8", "Contaminación de la fuente", "Ambiental", "Protección y reforestación de ronda hídrica, monitoreo de calidad y barreras de captación."],
    ["9", "Reducción de caudal (sequía)", "Ambiental", "Fuente alterna de respaldo, tanques de regulación, PUEAA y reuso."],
    ["10", "Disposición de lodos", "Ambiental", "Lechos de secado y deshidratación, disposición final autorizada y aprovechamiento agrícola."],
    ["11", "Vertimiento de aguas de lavado", "Ambiental", "Recirculación y tratamiento previo, con permiso ambiental (CAR)."],
    ["12", "Afectación de fauna/flora", "Ambiental", "Plan de Manejo Ambiental (PMA), compensación forestal y obras en franjas intervenidas."],
    ["14", "Interrupción eléctrica", "Operativo", "Grupo electrógeno de respaldo y energía con respaldo dual."],
    ["15", "Accidentes laborales", "SST", "SG-SST (Decreto 1072), capacitación, EPP y permisos de trabajo de alto riesgo."],
]
add_table(
    ["#", "Riesgo", "Tipo", "Intervención propuesta"],
    inter,
    col_align=["center", "left", "left", "left"])

h2("8.2 Matriz de recalificación (riesgo residual)")
recal = [
    ["1", "Sobrecostos de construcción", "Financiero", "16", "Alto", "6", "Bajo"],
    ["6", "Bajo recaudo tarifario", "Comercial", "16", "Alto", "6", "Bajo"],
    ["5", "Alza de tasas de interés", "Financiero", "12", "Medio", "3", "Bajo"],
    ["8", "Contaminación de la fuente", "Ambiental", "15", "Alto", "8", "Medio"],
    ["9", "Reducción de caudal (sequía)", "Ambiental", "15", "Alto", "8", "Medio"],
    ["10", "Disposición de lodos", "Ambiental", "12", "Medio", "3", "Bajo"],
    ["11", "Vertimiento aguas de lavado", "Ambiental", "12", "Medio", "3", "Bajo"],
    ["12", "Afectación fauna/flora", "Ambiental", "6", "Bajo", "2", "Bajo"],
    ["14", "Interrupción eléctrica", "Operativo", "12", "Medio", "4", "Bajo"],
    ["15", "Accidentes laborales", "SST", "12", "Medio", "4", "Bajo"],
]
add_table(
    ["#", "Riesgo", "Tipo", "P×I inicial", "Nivel inicial", "P×I residual", "Nivel residual"],
    recal,
    col_align=["center", "left", "left", "center", "center", "center", "center"])
para("Efecto de las intervenciones: los riesgos Altos descienden a Medio o Bajo, y la mayoría de los Medios pasan "
     "a Bajo. Los riesgos asociados a la fuente (8 y 9) permanecen en nivel Medio por depender de factores "
     "climáticos externos, por lo que requieren monitoreo y planes de contingencia permanentes.")

# 9. CONCLUSIONES
h1("9. Conclusiones")
for x in ["El proyecto resuelve una necesidad básica insatisfecha de alto impacto en salud pública y desarrollo local.",
          "Es financieramente viable: VPN positivo y TIR superior al costo de capital a nivel de proyecto (18,13 % vs. WACC 11,07 %) y de inversionista (24,78 % vs. Ke 15,5 %).",
          "El apalancamiento 60/40 es adecuado y mejora la rentabilidad del accionista sin comprometer el servicio de la deuda.",
          "La gestión de riesgos —en especial los ambientales— es determinante; con las intervenciones el perfil de riesgo se reduce a niveles mayoritariamente bajos."]:
    doc.add_paragraph(x, style="List Number")

doc.save("INFORME_PEPI.docx")
print("OK -> INFORME_PEPI.docx generado")

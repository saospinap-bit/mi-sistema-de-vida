# -*- coding: utf-8 -*-
"""Hojas de vida del personal (numeral 4.3 de los TR) y Anexo 2, en Word editable."""
import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm
import datos as D

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

OBRAS = ("módulos educativos, centros comunitarios, polideportivos, baterías sanitarias, parques modulares, "
         "edificaciones sencillas hasta 500 m2 y alturas menores de 15 m, edificaciones mayores de 500 m2 y "
         "alturas mayores de 15 m, o unidades básicas de atención en salud")
CARGOS = [
    ("DIRECTOR DE OBRA", "Ingeniero civil, arquitecto o constructor en ingeniería o arquitectura",
     "5 años, contados desde la expedición de la matrícula profesional",
     "Mínimo 2 contratos como contratista, director de obra o director de interventoría; o mínimo 4 "
     "contratos como residente de obra o de interventoría; o mínimo 2 años en cargos públicos de "
     "supervisión de contratos de obra o interventoría. Obras: " + OBRAS + ".",
     "Puede ser el mismo contratista. Dedicación según necesidades de la obra."),
    ("RESIDENTE DE OBRA", "Ingeniero civil, arquitecto o constructor en ingeniería o arquitectura "
     "(el numeral 6.1 pide ingeniero civil o arquitecto matriculado: preferir uno de los dos)",
     "3 años, contados desde la expedición de la matrícula profesional",
     "Mínimo 1 contrato como contratista, director de obra o director de interventoría; o mínimo 2 "
     "contratos como residente de obra o de interventoría; o mínimo 1 año en cargos públicos de "
     "supervisión de contratos de obra o interventoría. Obras: " + OBRAS + ".",
     "TIEMPO COMPLETO. NO puede ser el contratista, el director ni el representante legal (numeral 6.1)."),
    ("MAESTRO DE OBRA", "Maestro de obra – técnico en construcción (diploma o certificado)",
     "3 años, contados desde la fecha del título o certificado",
     "Mínimo 2 contratos como inspector de obra en: " + OBRAS.replace(", o unidades básicas de atención en salud", "") + ".",
     "Permanente en obra."),
]


def tabla(doc, filas, anchos, bold_first=True, header=False):
    t = doc.add_table(rows=len(filas), cols=len(filas[0]))
    t.style = "Table Grid"
    for i, f in enumerate(filas):
        for j, v in enumerate(f):
            c = t.cell(i, j)
            c.text = v
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(8.5)
                    if (header and i == 0) or (bold_first and j == 0 and not header):
                        r.bold = True
            c.width = Cm(anchos[j])
    return t


def encabezado(doc, titulo):
    for t, s in [(D.ENTIDAD, 10), (D.LICITACION, 9), ("OBJETO: " + D.OBJETO, 8)]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(t); r.font.size = Pt(s); r.bold = s > 8
    h = doc.add_paragraph()
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run(titulo); r.bold = True; r.font.size = Pt(13)


def hoja_vida(doc, cargo, formacion, gen, esp, cond):
    encabezado(doc, f"HOJA DE VIDA – {cargo}")
    doc.add_paragraph().add_run("Requisitos del pliego (numeral 4.3 de los TR)").bold = True
    tabla(doc, [["Cargo / cantidad", f"{cargo.title()} – 1"], ["Formación académica", formacion],
                ["Experiencia general", gen], ["Experiencia específica", esp], ["Condiciones", cond],
                ["Plazo para acreditar", "5 días hábiles después de la notificación al proponente en primer "
                                         "orden de elegibilidad. Si no se cumple, se contrata con el segundo y "
                                         "se hace efectiva la garantía de seriedad."]], [4.5, 12.5])
    doc.add_paragraph()
    doc.add_paragraph().add_run("1. Datos personales").bold = True
    tabla(doc, [["Nombre completo", "[ ]"], ["Cédula de ciudadanía", "[ ]"], ["Fecha de nacimiento", "[ ]"],
                ["Dirección / ciudad", "[ ]"], ["Teléfono", "[ ]"], ["Correo electrónico", "[ ]"]], [4.5, 12.5])
    doc.add_paragraph()
    doc.add_paragraph().add_run("2. Formación académica").bold = True
    tabla(doc, [["Título", "Institución", "Fecha de grado"], ["[ ]", "[ ]", "[ ]"], ["[ ]", "[ ]", "[ ]"]],
          [7, 6, 4], header=True)
    doc.add_paragraph()
    doc.add_paragraph().add_run("3. Matrícula profesional").bold = True
    tabla(doc, [["Número de matrícula / tarjeta", "[ ]"], ["Entidad que la expide", "[COPNIA / CPNAA / CPNT]"],
                ["Fecha de expedición (desde aquí cuenta la experiencia)", "[ ]"],
                ["Certificado de vigencia y antecedentes", "[No. y fecha]"],
                ["Experiencia general acumulada a la fecha de cierre", "[ años y meses ]"]], [8, 9])
    doc.add_paragraph()
    doc.add_paragraph().add_run("4. Experiencia específica (debe coincidir exactamente con las certificaciones)").bold = True
    head = ["No.", "Contratante / empleador", "Objeto del contrato (tipo de obra)", "Cargo desempeñado",
            "Fecha inicio", "Fecha fin", "Duración"]
    filas = [head] + [[str(k), "", "", "", "", "", ""] for k in range(1, 6)]
    tabla(doc, filas, [0.8, 3.2, 5, 2.8, 1.8, 1.8, 1.6], header=True)
    doc.add_paragraph()
    doc.add_paragraph().add_run("5. Soportes que se adjuntan").bold = True
    for t in ["Copia de la cédula", "Copia de diplomas y actas de grado", "Copia de la matrícula profesional",
              "Certificado de vigencia de la matrícula", "Certificaciones laborales o de contratos (cargo, objeto, "
              "fechas y entidad)", "Carta de compromiso y disponibilidad firmada"]:
        doc.add_paragraph("☐ " + t)
    doc.add_paragraph()
    doc.add_paragraph().add_run("6. Carta de compromiso y disponibilidad").bold = True
    doc.add_paragraph(
        f"Yo, [NOMBRE], identificado con C.C. [ ], me comprometo a desempeñar el cargo de {cargo.lower()} "
        f"en la obra “{D.OBJETO}”, en caso de que el contrato se adjudique a {D.PROPONENTE}, durante todo el "
        "plazo de ejecución (5 meses) y con la dedicación exigida en el pliego de condiciones. Declaro que la "
        "información de esta hoja de vida es verídica y autorizo su verificación.")
    doc.add_paragraph("\n\n______________________________\nFirma del profesional\nC.C. [ ]\n\n"
                      "______________________________\nVo. Bo. Representante legal del proponente")


doc = Document()
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2)
    s.top_margin = s.bottom_margin = Cm(1.8)
doc.styles["Normal"].font.size = Pt(9.5)
for k, c in enumerate(CARGOS):
    if k:
        doc.add_page_break()
    hoja_vida(doc, *c)
doc.save(f"{OUT}/HOJAS_DE_VIDA_Director_Residente_Maestro.docx")

# Anexo 2
doc = Document()
doc.styles["Normal"].font.size = Pt(10)
encabezado(doc, "ANEXO 2 – CARTA DE CONFORMACIÓN DE CONSORCIO O UNIÓN TEMPORAL")
doc.add_paragraph("(Solo si el proponente es plural. Su falta o sus errores NO son subsanables, numeral 3.1.3.)").runs[0].italic = True
doc.add_paragraph(D.CIUDAD_FECHA)
doc.add_paragraph("Señores\nALCALDÍA DE SANDONÁ\nSandoná – Nariño")
doc.add_paragraph(f"REFERENCIA: {D.LICITACION}")
doc.add_paragraph(
    "Los suscritos, ______________ identificado con C.C. No. ________ de ________, en nombre propio / en "
    "representación de ______________, y ______________ identificado con C.C. No. ________ de ________, en "
    "nombre propio / en representación de ______________, manifestamos por este documento que hemos "
    f"convenido asociarnos en (CONSORCIO / UNIÓN TEMPORAL) para participar en la licitación de la referencia, "
    f"cuyo objeto es “{D.OBJETO}”, y por lo tanto expresamos lo siguiente:")
for t in [
    "1. La duración del (CONSORCIO / UNIÓN TEMPORAL) será igual al plazo de ejecución del contrato (5 meses) y "
    f"dos (2) años más, es decir, como mínimo hasta el {D.DURACION_CONSORCIO} (numeral 3.1.3).",
    "2. El (CONSORCIO / UNIÓN TEMPORAL) está integrado por:",
]:
    doc.add_paragraph(t)
tabla(doc, [["Nombre del integrante", "NIT / C.C.", "Participación (%)", "Actividades a cargo (solo UT)"],
            ["", "", "", ""], ["", "", "", ""], ["TOTAL", "", "100 %", ""]], [5, 3, 3, 6], header=True)
for t in [
    "3. El (CONSORCIO / UNIÓN TEMPORAL) se denomina: ________________________.",
    "4. La responsabilidad de los integrantes es solidaria (artículo 7 de la Ley 80 de 1993). En la unión "
    "temporal, las sanciones por incumplimiento se impondrán según la participación de cada integrante en la "
    "ejecución; los términos y la extensión de la participación no podrán modificarse sin consentimiento "
    "previo de la entidad.",
    "5. El representante es ______________, identificado con C.C. No. ________ de ________, expresamente "
    "facultado para firmar y presentar la oferta y, en caso de adjudicación, firmar el contrato y tomar todas "
    "las determinaciones necesarias para su ejecución y liquidación, con amplias y suficientes facultades.",
    "6. Sede: dirección ______________, correo ______________, teléfono ______________.",
    "En constancia se firma en ________, a los ___ días del mes de ________ de 2025.",
    "\n\n__________________________          __________________________\nFirma integrante 1"
    "                                  Firma integrante 2\n\n__________________________\nFirma representante",
]:
    doc.add_paragraph(t)
doc.save(f"{OUT}/ANEXO_2_Consorcio_o_UT_(si_aplica).docx")
print("docx ok")

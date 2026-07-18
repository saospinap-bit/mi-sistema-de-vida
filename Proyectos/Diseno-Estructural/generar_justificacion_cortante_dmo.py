#!/usr/bin/env python3
"""Genera la justificación y actualiza la memoria con el diseño final de vigas."""
from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = Path(__file__).resolve().parent
DESIGN_SCRIPT = BASE / "generar_diseno_vigas_envolventes.py"
SOURCE_MEMORY = BASE / "GRUPO_6_SANTA_MARTA_MEMORIA_ACTUALIZADA (6).docx"
OUTPUT = BASE / "JUSTIFICACION-DISENO-CORTANTE-DMO.docx"
MEMORY_OUTPUT = BASE / "GRUPO_6_SANTA_MARTA_MEMORIA_FINAL_VIGAS.docx"


def load_design_module():
    spec = importlib.util.spec_from_file_location("beam_design", DESIGN_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell(cell, text, bold=False, color=None, size=7):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(str(text))
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_heading(doc, text, level=1):
    paragraph = doc.add_heading(text, level=level)
    paragraph.paragraph_format.space_before = Pt(8)
    paragraph.paragraph_format.space_after = Pt(4)
    return paragraph


def add_equation(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(text)
    run.bold = True
    run.font.name = "Cambria Math"
    run.font.size = Pt(11)


def configure(doc):
    section = doc.sections[-1]
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10)


def set_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:color"), "808080")
        borders.append(element)
    tbl_pr.append(borders)


def result_table(doc, design, groups, all_results):
    headers = ["Grupo", "N", "Sección", "Frame gob.", "Mu−", "Mu+", "Vu diseño", "Tu bruto", "Tu diseño", "Estado"]
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    for i, header in enumerate(headers):
        set_cell(table.rows[0].cells[i], header, bold=True, color="FFFFFF", size=6)
        shade(table.rows[0].cells[i], "17365D")
    for result in groups:
        cells = table.add_row().cells
        ok = result["group_all_ok"]
        failed_count = sum(1 for x in all_results
                           if x["group"] == result["group"] and not x["overall"])
        values = [
            result["group"], result["count"], f"{int(result['b'])}×{int(result['h'])}", result["frame"],
            f"{result['Mu_neg']:.1f}", f"{result['Mu_pos']:.1f}", f"{result['Vdesign']:.1f}",
            f"{result['max_Tu_raw']:.1f}", f"{result['Tu']:.1f}", "CUMPLE" if ok else f"{failed_count} NO CUMPLEN",
        ]
        for i, value in enumerate(values):
            set_cell(cells[i], value, size=6)
        shade(cells[0], design.COLORS[result["group"]])
        shade(cells[-1], "C6E0B4" if ok else "F4CCCC")
    return table


def append_viga_chapter(doc, design, records, results, groups):
    doc.add_page_break()
    add_heading(doc, "VERIFICACIÓN Y DESPIECE DE VIGAS — NO EMITIR PARA CONSTRUCCIÓN", 1)
    doc.add_paragraph(
        "Este capítulo verifica las 592 vigas con el export resultados sap.xlsx del modelo reanalizado en "
        "SAP2000 v26. Se conservaron los 12 grupos y sus secciones efectivamente asignadas: 450×550 mm "
        "para VC1–VC7 y VRAUX, y 500×550 mm para VR1, VR N1, VR2 y VR3. La verificación es conservadora "
        "y mantiene visibles todos los incumplimientos; no constituye liberación para construcción."
    )

    add_heading(doc, "Solicitaciones y criterios", 2)
    criteria = [
        "Mu− y Mu+ se obtienen de los extremos mínimo y máximo de M3 en ENVFLEX.",
        "Vu de diseño es el mayor entre ENVCORT directo y Ve por capacidad DMO.",
        "Ve = Vu,ENVFLEX + (Mpr− + Mpr+)/Ln, con Ln = máx(L estación − 0.60 m; 0.50L).",
        "R = R0·φa·φp·φr = 5·1·1·1 = 5; las fuerzas exportadas no se vuelven a dividir por R.",
        "Tu de diseño es el mayor |T| de ENVFLEX y ENVCORT. No se limita automáticamente a φTcr porque no se dispone de clasificación frame a frame ni de reanálisis de redistribución.",
        "El refuerzo transversal satisface máx(Av/s por resistencia; Av/s mínimo) + 2At/s, interacción V–T y límites de separación.",
        "Al se cubre con barras Nº5 dedicadas y distribuidas alrededor del perímetro, adicionales al acero requerido por flexión; no se acredita doblemente As superior/inferior.",
        "La zona extrema de estribos tiene longitud 2h desde cada cara y el primer estribo se coloca a máximo 50 mm.",
    ]
    for text in criteria:
        doc.add_paragraph("• " + text)

    add_equation(doc, "Vu,diseño = máx[Vu,ENVCORT ; Vu,ENVFLEX + (Mpr− + Mpr+)/Ln]")
    add_equation(doc, "Tu,diseño = máx(|TENVFLEX|, |TENVCORT|)  [sin reducción automática a φTcr]")

    add_heading(doc, "Resultados por grupo", 2)
    result_table(doc, design, groups, results)
    doc.add_paragraph(
        f"Resultado individual conservador: {sum(x['overall'] for x in results)} de {len(results)} vigas cumplen "
        f"todos los controles con torsión bruta. {sum(not x['overall'] for x in results)} vigas quedan NO CUMPLE. "
        f"En {sum(x['requires_compatibility_assessment'] for x in results)} vigas Tu bruto excede la referencia φTcr; "
        "cualquier reducción futura exige demostrar compatibilidad y reanalizar los elementos receptores."
    )

    failures = [x for x in results if not x["overall"]]
    add_heading(doc, "Observaciones obligatorias", 2)
    if failures:
        failure_counts = Counter(x["group"] for x in failures)
        summary = ", ".join(f"{group}: {failure_counts[group]}" for group in design.GROUP_ORDER if failure_counts[group])
        doc.add_paragraph(
            f"Quedan {len(failures)} frames no conformes ({summary}). Las causas son exceso de interacción V–T, "
            "límite seccional o ausencia de un estribo práctico con la sección actual. Deben aumentarse secciones, "
            "actualizarse las propiedades en SAP, reanalizarse las envolventes y regenerarse el expediente. No se "
            "reduce ENVCORT ni Tu para forzar cumplimiento."
        )
        for group in design.GROUP_ORDER:
            group_frames = [x["frame"] for x in failures if x["group"] == group]
            if group_frames:
                doc.add_paragraph(f"• {group}: frames {', '.join(group_frames)}")
    doc.add_paragraph(
        "Los planos son detalles académicos de coordinación y todos se rotulan NO EMITIR PARA CONSTRUCCIÓN. "
        "Incluyen tabla frame–nudos–longitud–nivel y esquema por centroides disponibles, pero el export no contiene "
        "Joint Coordinates ni una planta estructural completa; por tanto, no sustituyen planos de localización o fabricación."
    )

    add_heading(doc, "Archivos de entrega", 2)
    for text in [
        "DISENO-VIGAS-ENTREGA-FINAL-DMO.xlsx: diseño individual, grupos, fórmulas y auditoría.",
        "PLANOS-DESPIECE-VIGAS-POR-GRUPO.pdf: doce láminas, una por grupo.",
        "Planos-Despiece-Vigas/*.dxf: archivos editables para AutoCAD.",
    ]:
        doc.add_paragraph("• " + text)


def build_justification(design, records, results, groups):
    doc = Document()
    configure(doc)
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("JUSTIFICACIÓN DEL DISEÑO DE VIGAS\nSISTEMA DMO — R = 5")
    run.bold = True
    run.font.size = Pt(18)
    subtitle = doc.add_paragraph("Proyecto edificio residencial — Santa Marta\nAnexo técnico para memoria y sustentación")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True
    append_viga_chapter(doc, design, records, results, groups)
    doc.save(OUTPUT)


def reconcile_group_use(doc):
    """Corrige la contradicción heredada y fija residencial = Grupo I, I=1.0."""
    replacements = {
        163: ("Grupo de Uso: por tratarse de un edificio residencial de ocupación normal, el proyecto se "
              "clasifica en el Grupo de Uso I según NSR-10 A.2.5.1, con coeficiente de importancia I = 1.0."),
        530: ("Grupo I – Estructuras de ocupación normal: incluye edificaciones residenciales y demás usos "
              "que no pertenecen a los Grupos II, III o IV."),
        532: ("Grupo II – Estructuras de ocupación especial: reúne usos con condiciones especiales de "
              "ocupación o concentración según NSR-10 A.2.5.1.3."),
        538: ("Para el presente proyecto residencial, la estructura se clasifica en el Grupo de Uso I "
              "(ocupación normal)."),
        540: ("Para el Grupo de Uso I adoptado en este proyecto, el coeficiente de importancia es:"),
        541: "I = 1.0",
    }
    for index, text in replacements.items():
        if index >= len(doc.paragraphs):
            raise ValueError(f"No existe el párrafo {index} requerido para reconciliar el grupo de uso")
        doc.paragraphs[index].text = text


def build_memory(design, records, results, groups):
    doc = Document(SOURCE_MEMORY) if SOURCE_MEMORY.exists() else Document()
    configure(doc)
    if SOURCE_MEMORY.exists():
        reconcile_group_use(doc)
    append_viga_chapter(doc, design, records, results, groups)
    doc.save(MEMORY_OUTPUT)


def main():
    design = load_design_module()
    records, _ = design.extract_inputs()
    results = [design.design_record(record) for record in records]
    groups = design.build_group_records(records, results)
    build_justification(design, records, results, groups)
    build_memory(design, records, results, groups)
    print(f"OK: {OUTPUT}")
    print(f"OK: {MEMORY_OUTPUT}")
    print(f"Vigas: {len(results)}; cumplen: {sum(x['overall'] for x in results)}; no cumplen: {sum(not x['overall'] for x in results)}")


if __name__ == "__main__":
    main()

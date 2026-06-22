# -*- coding: utf-8 -*-
"""
Convierte INFORME_PEPI.md a INFORME_PEPI.docx (Word), preservando titulos,
parrafos, tablas e imagenes (arboles). Asi el Word siempre coincide con el
informe en Markdown.  Requiere: python-docx.
"""
import os
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

MD = "INFORME_PEPI.md"
OUT = "INFORME_PEPI.docx"
AZUL = RGBColor(0x1F, 0x4E, 0x79)

doc = Document()
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(11)


def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def add_runs(paragraph, text):
    """Procesa **negrita** dentro de un texto."""
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part == "":
            continue
        run = paragraph.add_run(part)
        if i % 2 == 1:
            run.bold = True


def heading(text, level):
    text = text.strip()
    p = doc.add_heading(level=min(level, 4))
    run = p.add_run(re.sub(r"\*\*(.+?)\*\*", r"\1", text))
    run.font.color.rgb = AZUL
    run.font.size = Pt({1: 15, 2: 12, 3: 11, 4: 11}.get(level, 11))


def paragraph(text):
    text = text.strip()
    if not text:
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_runs(p, text)


def add_image(path):
    if os.path.exists(path):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Inches(6.3))


def add_table(rows):
    # rows: lista de listas de celdas (texto). rows[0] = encabezado.
    ncol = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=ncol)
    t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for ci in range(ncol):
            val = row[ci] if ci < len(row) else ""
            val = re.sub(r"\*\*(.+?)\*\*", r"\1", val).strip()
            cell = cells[ci]
            cell.text = ""
            par = cell.paragraphs[0]
            run = par.add_run(val)
            run.font.size = Pt(8.5)
            if ri == 0:
                run.bold = True; run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                shade(cell, "1F4E79"); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


# ---- Parser principal ----
with open(MD, encoding="utf-8") as f:
    lines = f.readlines()

i = 0
n = len(lines)
while i < n:
    line = lines[i].rstrip("\n")
    s = line.strip()

    # Imagen
    m = re.match(r"!\[.*?\]\((.+?)\)", s)
    if m:
        add_image(m.group(1)); i += 1; continue

    # Encabezados
    if s.startswith("#"):
        lvl = len(s) - len(s.lstrip("#"))
        heading(s.lstrip("#"), lvl); i += 1; continue

    # Tabla (linea con | y siguiente de separacion ---)
    if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]):
        rows = [split_row(s)]
        i += 2  # saltar encabezado + separador
        while i < n and lines[i].strip().startswith("|"):
            rows.append(split_row(lines[i].strip())); i += 1
        add_table(rows); continue

    # Regla horizontal
    if s == "---":
        i += 1; continue

    # Cita / nota
    if s.startswith(">"):
        paragraph(s.lstrip(">").strip()); i += 1; continue

    # Formula en bloque $$
    if s.startswith("$$"):
        paragraph(s.replace("$$", "").replace("\\", "").strip()); i += 1; continue

    # Linea en blanco
    if s == "":
        i += 1; continue

    # Parrafo normal (acumula lineas hasta blanco/estructura)
    buff = [s]
    i += 1
    while i < n:
        nxt = lines[i].strip()
        if (nxt == "" or nxt.startswith("#") or nxt.startswith("|")
                or nxt.startswith(">") or nxt.startswith("![") or nxt == "---"):
            break
        buff.append(nxt); i += 1
    paragraph(" ".join(buff))

doc.save(OUT)
n_img = len(doc.inline_shapes)
print(f"OK -> {OUT}  (imagenes incrustadas: {n_img})")

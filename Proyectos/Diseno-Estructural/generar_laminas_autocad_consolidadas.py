"""Genera dos láminas AutoCAD A0 consolidadas con el estilo de la referencia.

Lámina 1: siete grupos de vigas de carga (VC1–VC7).
Lámina 2: cinco grupos de vigas de rigidez (VR1, VR N1, VR2, VR3 y VRAUX).

El export SAP suministrado no contiene viguetas. Cada DXF se dibuja en
milímetros sobre Modelspace y trae una presentación A0 horizontal 1:1.
Las cotas distinguen expresamente L SAP I-J de Ln adoptada para cálculo.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment

BASE = Path(__file__).resolve().parent
DESIGN_SCRIPT = BASE / "generar_diseno_vigas_envolventes.py"
GROUP_SCRIPT = BASE / "generar_planos_despiece_grupos.py"
OUTPUT_DIR = BASE / "Planos-Autocad-Consolidados"

SHEET_W = 1189.0
SHEET_H = 841.0
MARGIN = 10.0
TITLEBLOCK_W = 170.0
MAIN_RIGHT = SHEET_W - MARGIN - TITLEBLOCK_W
DATE_TEXT = "17-07-2026"

WHITE = 7
RED = 1
YELLOW = 2
GREEN = 3
CYAN = 4
BLUE = 5
MAGENTA = 6
GRAY = 8
LIGHT_GRAY = 9
BROWN = 30


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_text(msp, text, point, height=3.0, layer="TEXTO", color=None,
             align=TextEntityAlignment.LEFT):
    attribs = {"height": height, "layer": layer}
    if color is not None:
        attribs["color"] = color
    entity = msp.add_text(str(text), dxfattribs=attribs)
    entity.set_placement(point, align=align)
    return entity


def line(msp, start, end, layer="MARCO", color=None, lineweight=18):
    attribs = {"layer": layer, "lineweight": lineweight}
    if color is not None:
        attribs["color"] = color
    return msp.add_line(start, end, dxfattribs=attribs)


def rect(msp, x, y, width, height, layer="MARCO", color=None, lineweight=18):
    attribs = {"layer": layer, "lineweight": lineweight}
    if color is not None:
        attribs["color"] = color
    return msp.add_lwpolyline(
        [(x, y), (x + width, y), (x + width, y + height), (x, y + height)],
        close=True,
        dxfattribs=attribs,
    )


def circle_text(msp, center, radius, text):
    msp.add_circle(center, radius, dxfattribs={"layer": "EJES", "color": GRAY})
    add_text(msp, text, (center[0], center[1] - 1.15), 2.6, "EJES", GRAY,
             TextEntityAlignment.MIDDLE_CENTER)


def format_range(vmin_mm, vmax_mm):
    if math.isclose(vmin_mm, vmax_mm, abs_tol=1.0):
        return f"{vmin_mm / 1000:.3f} m"
    return f"{vmin_mm / 1000:.3f} a {vmax_mm / 1000:.3f} m"


def split_lines(text, max_chars):
    words = str(text).split()
    output, current = [], ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) > max_chars and current:
            output.append(current)
            current = word
        else:
            current = candidate
    if current:
        output.append(current)
    return output


def create_doc():
    doc = ezdxf.new("R2018", setup=True)
    layers = {
        "MARCO": WHITE, "GUIA": LIGHT_GRAY, "ROTULO": WHITE, "TITULO": MAGENTA,
        "TEXTO": WHITE, "CONTORNO": WHITE, "APOYOS": CYAN, "EJES": GRAY,
        "ACERO_SUP": BLUE, "ACERO_ADIC": YELLOW, "ACERO_INF": RED,
        "ACERO_TOR": BROWN, "ESTRIBOS": WHITE, "CORTE": WHITE,
        "COTAS": GREEN, "ALERTA": RED,
    }
    for name, color in layers.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    doc.units = 4  # milímetros
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 3
    doc.header["$MEASUREMENT"] = 1
    return doc


def draw_logo(msp, x, y, width, height):
    """Emblema vectorial esquemático; no requiere una referencia raster externa."""
    cx = x + width / 2
    top = y + height - 10
    sw, sh = 43.0, 48.0
    left, right, bottom = cx - sw / 2, cx + sw / 2, top - sh
    msp.add_lwpolyline(
        [(left, top), (right, top), (right - 4, bottom + 12),
         (cx, bottom), (left + 4, bottom + 12)],
        close=True, dxfattribs={"layer": "ROTULO", "color": WHITE, "lineweight": 30},
    )
    line(msp, (left + 4, top - 11), (right - 4, top - 11), "ROTULO", WHITE, 25)
    line(msp, (cx, top - 3), (cx, bottom + 5), "ROTULO", WHITE, 25)
    add_text(msp, "UN", (cx, bottom + 15), 8.0, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "UNIVERSIDAD NACIONAL", (cx, y + 18), 4.1, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "DE COLOMBIA", (cx, y + 10), 4.1, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)


def draw_titleblock(msp, title, sheet_number):
    x, y = MAIN_RIGHT, MARGIN
    w, h = TITLEBLOCK_W, SHEET_H - 2 * MARGIN
    rect(msp, x, y, w, h, "MARCO", WHITE, 35)

    logo_h = 145.0
    logo_y = y + h - logo_h
    rect(msp, x, logo_y, w, logo_h, "ROTULO", WHITE, 25)
    draw_logo(msp, x, logo_y, w, logo_h)

    univ_h = 105.0
    univ_y = logo_y - univ_h
    rect(msp, x, univ_y, w, univ_h, "ROTULO", WHITE, 25)
    for index, text in enumerate([
        "SEDE BOGOTA", "FACULTAD DE INGENIERIA",
        "DEPARTAMENTO DE INGENIERIA CIVIL", "Y AGRICOLA", "DISEÑO ESTRUCTURAL",
    ]):
        add_text(msp, text, (x + w / 2, univ_y + 88 - index * 17), 4.0,
                 "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)

    project_h = 130.0
    project_y = univ_y - project_h
    rect(msp, x, project_y, w, project_h, "ROTULO", WHITE, 25)
    add_text(msp, "Localizacion:", (x + 7, project_y + 110), 4.1, "ROTULO", WHITE)
    add_text(msp, "Santa Marta", (x + w / 2, project_y + 87), 5.0, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)
    line(msp, (x, project_y + 66), (x + w, project_y + 66), "ROTULO", WHITE, 18)
    add_text(msp, "Tipo de proyecto:", (x + 7, project_y + 50), 4.1, "ROTULO", WHITE)
    add_text(msp, "RESIDENCIAL", (x + w / 2, project_y + 25), 5.0, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)

    content_h = 230.0
    content_y = project_y - content_h
    rect(msp, x, content_y, w, content_h, "ROTULO", WHITE, 25)
    add_text(msp, "Contiene:", (x + 7, content_y + 208), 4.2, "ROTULO", WHITE)
    for index, text in enumerate(split_lines(title, 19)):
        add_text(msp, text, (x + w / 2, content_y + 171 - index * 15), 5.6,
                 "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "ELEVACIONES Y CORTES", (x + w / 2, content_y + 96), 4.4,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "NO EMITIR PARA CONSTRUCCION", (x + w / 2, content_y + 46), 4.6,
             "ALERTA", RED, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "DETALLE ACADEMICO", (x + w / 2, content_y + 29), 4.2,
             "ALERTA", RED, TextEntityAlignment.MIDDLE_CENTER)

    bottom_h = content_y - y
    rect(msp, x, y, w, bottom_h, "ROTULO", WHITE, 25)
    line(msp, (x, y + bottom_h / 2), (x + w, y + bottom_h / 2), "ROTULO", WHITE, 18)
    add_text(msp, "Formato: A0 horizontal", (x + 7, y + bottom_h - 17), 3.8, "ROTULO", WHITE)
    add_text(msp, "Unidades: mm", (x + 7, y + bottom_h - 33), 3.8, "ROTULO", WHITE)
    add_text(msp, f"Fecha: {DATE_TEXT}", (x + 7, y + 23), 3.8, "ROTULO", WHITE)
    add_text(msp, f"Lamina: {sheet_number}", (x + 7, y + 9), 4.5, "ROTULO", WHITE)


def draw_section(msp, cx, cy, d, label, width=32.0, height=40.0):
    left, bottom = cx - width / 2, cy - height / 2
    rect(msp, left, bottom, width, height, "CORTE", WHITE, 20)
    inset = 3.0
    rect(msp, left + inset, bottom + inset, width - 2 * inset, height - 2 * inset,
         "ESTRIBOS", WHITE, 18)
    if d["legs"] == 4:
        line(msp, (left + width / 3, bottom + inset),
             (left + width / 3, bottom + height - inset), "ESTRIBOS", WHITE, 18)
        line(msp, (left + 2 * width / 3, bottom + inset),
             (left + 2 * width / 3, bottom + height - inset), "ESTRIBOS", WHITE, 18)

    top_n, bot_n = min(d["n_sup"], 7), min(d["n_inf"], 7)
    for index in range(top_n):
        px = left + inset + 2.3 + index * (width - 2 * inset - 4.6) / max(top_n - 1, 1)
        msp.add_circle((px, bottom + height - inset - 2.3), 1.0,
                       dxfattribs={"layer": "ACERO_SUP", "color": BLUE})
    for index in range(bot_n):
        px = left + inset + 2.3 + index * (width - 2 * inset - 4.6) / max(bot_n - 1, 1)
        msp.add_circle((px, bottom + inset + 2.3), 1.0,
                       dxfattribs={"layer": "ACERO_INF", "color": RED})
    if d["n_lat"]:
        msp.add_circle((left + inset + 2.2, cy), 0.9,
                       dxfattribs={"layer": "ACERO_TOR", "color": BROWN})
        msp.add_circle((left + width - inset - 2.2, cy), 0.9,
                       dxfattribs={"layer": "ACERO_TOR", "color": BROWN})

    add_text(msp, label, (cx, bottom - 5.5), 2.8, "TEXTO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, f"{int(d['b'])}x{int(d['h'])}", (cx, bottom - 10), 2.7,
             "TEXTO", WHITE, TextEntityAlignment.MIDDLE_CENTER)


def draw_beam_detail(msp, design, d, x, y, width, height):
    rect(msp, x, y, width, height, "GUIA", LIGHT_GRAY, 9)
    add_text(msp, f"DESPIECE VIGA {d['group']}", (x + width / 2, y + height - 10),
             4.8, "TITULO", MAGENTA, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "PISO TIPO", (x + 7, y + height - 23), 3.6, "TITULO", MAGENTA)
    add_text(msp, f"{int(d['b']/10)}x{int(d['h']/10)} cm", (x + 7, y + height - 31),
             3.6, "TITULO", MAGENTA)

    beam_x0, beam_x1 = x + 61, x + width - 19
    beam_y, beam_h = y + height - 67, 21.0
    draw_l = beam_x1 - beam_x0

    for support_x, label in ((beam_x0, "I"), (beam_x1, "J")):
        line(msp, (support_x - 4, beam_y - 15), (support_x - 4, beam_y + beam_h + 15),
             "APOYOS", CYAN, 18)
        line(msp, (support_x + 4, beam_y - 15), (support_x + 4, beam_y + beam_h + 15),
             "APOYOS", CYAN, 18)
        line(msp, (support_x, beam_y - 19), (support_x, beam_y + beam_h + 20),
             "EJES", GRAY, 9)
        circle_text(msp, (support_x, beam_y + beam_h + 14), 4.5, label)

    for fraction, label in ((1 / 3, "1"), (2 / 3, "2")):
        px = beam_x0 + draw_l * fraction
        line(msp, (px, beam_y - 13), (px, beam_y + beam_h + 17), "EJES", GRAY, 9)
        circle_text(msp, (px, beam_y + beam_h + 14), 4.2, label)

    rect(msp, beam_x0, beam_y, draw_l, beam_h, "CONTORNO", WHITE, 18)

    for index in range(min(d["n_sup"], 3)):
        py = beam_y + beam_h - 3.5 - index * 2.1
        line(msp, (beam_x0, py), (beam_x1, py), "ACERO_SUP", BLUE, 30)
    extra = max(d["n_sup"] - 2, 0)
    extension = min(draw_l * 0.36, draw_l / 2)
    for index in range(min(extra, 4)):
        py = beam_y + beam_h - 10 - index * 1.5
        line(msp, (beam_x0, py), (beam_x0 + extension, py), "ACERO_ADIC", YELLOW, 30)
        line(msp, (beam_x1 - extension, py), (beam_x1, py), "ACERO_ADIC", YELLOW, 30)
    for index in range(min(d["n_inf"], 4)):
        py = beam_y + 3.5 + index * 1.8
        line(msp, (beam_x0, py), (beam_x1, py), "ACERO_INF", RED, 30)

    # Estribos esquemáticos: densidad diferenciada en extremos y centro.
    zone = draw_l * min(d["zone"] / max(d["Lmax"], 1), 0.28)
    for start, end, spacing in (
        (beam_x0 + 3, beam_x0 + zone, d["s_end"]),
        (beam_x0 + zone, beam_x1 - zone, d["s_center"]),
        (beam_x1 - zone, beam_x1 - 3, d["s_end"]),
    ):
        if end <= start:
            continue
        step = max(3.0, draw_l * spacing / max(d["Lmax"], 1))
        px = start
        while px <= end:
            line(msp, (px, beam_y + 1), (px, beam_y + beam_h - 1), "ESTRIBOS", WHITE, 9)
            px += step

    lmin, lmax = d["Lmin"], d["Lmax"]
    ln_min = design.clear_span(lmin / 1000) * 1000
    ln_max = design.clear_span(lmax / 1000) * 1000
    dim_y = beam_y - 11
    line(msp, (beam_x0, dim_y), (beam_x1, dim_y), "COTAS", GREEN, 18)
    line(msp, (beam_x0, dim_y - 2), (beam_x0, dim_y + 2), "COTAS", GREEN, 18)
    line(msp, (beam_x1, dim_y - 2), (beam_x1, dim_y + 2), "COTAS", GREEN, 18)
    add_text(msp, f"L SAP I-J = {format_range(lmin, lmax)}", ((beam_x0 + beam_x1) / 2, dim_y + 2.5),
             3.0, "COTAS", GREEN, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, f"Ln calculo = {format_range(ln_min, ln_max)}", ((beam_x0 + beam_x1) / 2, dim_y - 5),
             2.7, "TEXTO", WHITE, TextEntityAlignment.MIDDLE_CENTER)

    add_text(msp, f"SUP: {d['n_sup']}#5 | INF: {d['n_inf']}#5 | TOR: {d['n_lat']}#5 adicionales",
             (beam_x0, beam_y - 20), 2.8, "TEXTO", WHITE)
    add_text(msp, f"EST {d['st_label']} {d['legs']}R: 1ro <=50; @{int(d['s_end'])} en 2h; @{int(d['s_center'])} centro",
             (beam_x0, beam_y - 26), 2.8, "TEXTO", WHITE)

    cut_y = y + 43
    for fraction, label in ((0.28, "CORTE A-A"), (0.52, "CORTE B-B"), (0.76, "CORTE C-C")):
        draw_section(msp, x + width * fraction, cut_y, d, label)

    add_text(msp, f"{d['count']} frames | variantes de longitud: {d['variant_count']}",
             (x + 7, y + 10), 2.8, "TEXTO", WHITE)
    if d["failures"]:
        add_text(msp, f"NO CUMPLEN {len(d['failures'])} frames - ver Excel",
                 (x + width - 7, y + 10), 2.8, "ALERTA", RED,
                 TextEntityAlignment.RIGHT)
    else:
        add_text(msp, "Verificacion seccional: CUMPLE", (x + width - 7, y + 10),
                 2.8, "TEXTO", GREEN, TextEntityAlignment.RIGHT)


def draw_general_notes(msp, title, groups):
    x, y = MARGIN + 4, MARGIN + 3
    add_text(msp, title, (x, y + 8), 4.0, "TITULO", MAGENTA)
    add_text(msp, "L SAP I-J corresponde a Connectivity - Frame. Ln calculo es una hipotesis de diseño y no una cota geometrica.",
             (x + 225, y + 8), 3.0, "TEXTO", WHITE)
    add_text(msp, "Detalle por grupo; las longitudes exactas de cada frame se conservan en el Excel y en los DXF individuales.",
             (x + 225, y + 3), 3.0, "TEXTO", WHITE)
    add_text(msp, "Grupos incluidos: " + ", ".join(groups), (x, y + 3), 3.0, "TEXTO", WHITE)


def add_a0_layout(doc):
    layout = doc.layouts.new("A0_HORIZONTAL")
    if "Layout1" in doc.layout_names():
        doc.layouts.delete("Layout1")
    layout.page_setup(
        size=(SHEET_W, SHEET_H), margins=(0, 0, 0, 0), units="mm",
        rotation=0, scale=(1, 1), name="A0 horizontal 1:1", device="DWG To PDF.pc3",
    )
    layout.add_viewport(
        center=(SHEET_W / 2, SHEET_H / 2), size=(SHEET_W, SHEET_H),
        view_center_point=(SHEET_W / 2, SHEET_H / 2), view_height=SHEET_H,
        status=2,
    )
    layout.dxf.plot_layout_flags = 0


def make_sheet(path, title, sheet_number, details, design, columns, rows):
    doc = create_doc()
    msp = doc.modelspace()
    rect(msp, MARGIN, MARGIN, SHEET_W - 2 * MARGIN, SHEET_H - 2 * MARGIN,
         "MARCO", WHITE, 35)
    line(msp, (MAIN_RIGHT, MARGIN), (MAIN_RIGHT, SHEET_H - MARGIN), "MARCO", WHITE, 35)
    draw_titleblock(msp, title, sheet_number)

    content_left = MARGIN + 5
    content_bottom = MARGIN + 24
    content_top = SHEET_H - MARGIN - 5
    content_right = MAIN_RIGHT - 5
    gap_x, gap_y = 6.0, 6.0
    cell_w = (content_right - content_left - gap_x * (columns - 1)) / columns
    cell_h = (content_top - content_bottom - gap_y * (rows - 1)) / rows

    for index, detail in enumerate(details):
        row_from_top = index // columns
        col = index % columns
        x = content_left + col * (cell_w + gap_x)
        y = content_top - (row_from_top + 1) * cell_h - row_from_top * gap_y
        draw_beam_detail(msp, design, detail, x, y, cell_w, cell_h)

    draw_general_notes(msp, title, [d["group"] for d in details])
    add_a0_layout(doc)
    doc.saveas(path)


def main():
    design = load_module(DESIGN_SCRIPT, "beam_design_a0")
    group_module = load_module(GROUP_SCRIPT, "beam_group_a0")
    records, _ = design.extract_inputs()
    results = [design.design_record(record) for record in records]
    details = {group: group_module.group_detail(design, group, records, results)
               for group in design.GROUP_ORDER}

    vc_groups = ["VC1", "VC2", "VC3", "VC4", "VC5", "VC6", "VC7"]
    vr_groups = ["VR1", "VR N1", "VR2", "VR3", "VRAUX"]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    vc_path = OUTPUT_DIR / "LAMINA-A0-VIGAS-DE-CARGA-VC.dxf"
    vr_path = OUTPUT_DIR / "LAMINA-A0-VIGAS-DE-RIGIDEZ-VR.dxf"
    make_sheet(vc_path, "DESPIECE VIGAS DE CARGA", "V-01", [details[g] for g in vc_groups], design, 2, 4)
    make_sheet(vr_path, "DESPIECE VIGAS DE RIGIDEZ", "V-02", [details[g] for g in vr_groups], design, 2, 3)

    print(f"OK: {vc_path}")
    print(f"OK: {vr_path}")
    print("VC: 7 grupos / 240 frames")
    print("VR: 5 grupos / 352 frames")
    print("Nota: el export SAP no contiene viguetas")


if __name__ == "__main__":
    main()

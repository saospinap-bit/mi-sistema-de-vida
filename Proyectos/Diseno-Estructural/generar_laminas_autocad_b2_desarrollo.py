#!/usr/bin/env python3
"""Genera dos láminas CAD B2 de despiece de vigas, sin barras superpuestas.

La lámina V-01 reúne VC1–VC7 y la V-02 reúne VR1, VR N1, VR2, VR3 y
VRAUX. Cada panel representa una tipología mediante marcas de barra (no una
línea por cada barra en elevación), tres cortes y un cuadro de longitudes.

Las longitudes de desarrollo y gancho se calculan con los parámetros del
proyecto y se redondean hacia arriba para detallado:
- ld recto inferior Nº5 = 370 mm
- ld recto superior Nº5 = 480 mm
- ldh Nº5 = 305 mm
- cola de gancho estándar de 90° = 195 mm
- diámetro interior mínimo de doblado Nº5 = 100 mm

Los DXF se dibujan en milímetros de papel y contienen un layout B2 horizontal
707 x 500 mm, escala 1:1. El detalle sigue marcado como académico/no emitible.
"""
from __future__ import annotations

import importlib.util
import math
import zipfile
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment

BASE = Path(__file__).resolve().parent
DESIGN_SCRIPT = BASE / "generar_diseno_vigas_envolventes.py"
GROUP_SCRIPT = BASE / "generar_planos_despiece_grupos.py"
OUTPUT_DIR = BASE / "Planos-Autocad-B2-Final"
ZIP_PATH = OUTPUT_DIR / "DESCARGA-AUTOCAD-LAMINAS-B2-CORREGIDAS.zip"

# ISO B2 apaisado, en milímetros de papel.
SHEET_W = 707.0
SHEET_H = 500.0
MARGIN = 7.0
TITLEBLOCK_W = 103.0
MAIN_RIGHT = SHEET_W - MARGIN - TITLEBLOCK_W
DATE_TEXT = "18-07-2026"

# Materiales/detallado del proyecto.
FC = 28.0
FY = 420.0
DB_LONG = 15.9
PSI_E = 1.0
PSI_S = 0.8
LAMBDA = 1.0
TOP_FACTOR = 1.3
BOTTOM_FACTOR = 1.0
CB_FACTOR_LIMIT = 2.5
CLEAR_BAR = 25.0


def round_up(value: float, step: float = 5.0) -> float:
    return math.ceil(value / step - 1e-12) * step


LD_INF_RAW = FY * BOTTOM_FACTOR * PSI_E * PSI_S / (
    1.1 * LAMBDA * math.sqrt(FC) * CB_FACTOR_LIMIT
) * DB_LONG
LD_SUP_RAW = FY * TOP_FACTOR * PSI_E * PSI_S / (
    1.1 * LAMBDA * math.sqrt(FC) * CB_FACTOR_LIMIT
) * DB_LONG
LDH_RAW = max(0.24 * PSI_E * FY / (LAMBDA * math.sqrt(FC)) * DB_LONG,
              8 * DB_LONG, 150.0)
TAIL_90_RAW = 12 * DB_LONG
BEND_90_RAW = 6 * DB_LONG
LD_INF = round_up(LD_INF_RAW)
LD_SUP = round_up(LD_SUP_RAW)
LDH = round_up(LDH_RAW)
TAIL_90 = round_up(TAIL_90_RAW)
BEND_90 = round_up(BEND_90_RAW)

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


def add_text(msp, text, point, height=2.0, layer="TEXTO", color=None,
             align=TextEntityAlignment.LEFT, rotation=0.0):
    attribs = {"height": height, "layer": layer, "rotation": rotation}
    if color is not None:
        attribs["color"] = color
    entity = msp.add_text(str(text), dxfattribs=attribs)
    entity.set_placement(point, align=align)
    return entity


def line(msp, start, end, layer="MARCO", color=None, lineweight=18,
         linetype=None):
    attribs = {"layer": layer, "lineweight": lineweight}
    if color is not None:
        attribs["color"] = color
    if linetype:
        attribs["linetype"] = linetype
    return msp.add_line(start, end, dxfattribs=attribs)


def polyline(msp, points, layer, color=None, lineweight=30, close=False):
    attribs = {"layer": layer, "lineweight": lineweight}
    if color is not None:
        attribs["color"] = color
    return msp.add_lwpolyline(points, close=close, dxfattribs=attribs)


def rect(msp, x, y, width, height, layer="MARCO", color=None, lineweight=18):
    return polyline(
        msp,
        [(x, y), (x + width, y), (x + width, y + height), (x, y + height)],
        layer, color, lineweight, True,
    )


def fmt_range(vmin: float, vmax: float, decimals=0, suffix=""):
    if math.isclose(vmin, vmax, abs_tol=0.51):
        return f"{vmin:.{decimals}f}{suffix}"
    return f"{vmin:.{decimals}f}-{vmax:.{decimals}f}{suffix}"


def cut_length_ranges(design, detail):
    ln_min = design.clear_span(detail["Lmin"] / 1000.0) * 1000.0
    ln_max = design.clear_span(detail["Lmax"] / 1000.0) * 1000.0
    return {
        "ln_min": ln_min,
        "ln_max": ln_max,
        "continuous_min": round_up(ln_min + 2 * LDH, 5),
        "continuous_max": round_up(ln_max + 2 * LDH, 5),
        "support_min": round_up(ln_min / 4 + LDH, 5),
        "support_max": round_up(ln_max / 4 + LDH, 5),
    }


def create_doc():
    doc = ezdxf.new("R2018", setup=True)
    layers = {
        "MARCO": WHITE,
        "GUIA": LIGHT_GRAY,
        "ROTULO": WHITE,
        "TITULO": MAGENTA,
        "TEXTO": WHITE,
        "CONTORNO": WHITE,
        "APOYOS": CYAN,
        "EJES": GRAY,
        "M1_SUP_CONT": BLUE,
        "M2_SUP_IZQ": YELLOW,
        "M3_SUP_DER": YELLOW,
        "M4_INF_CONT": RED,
        "M5_TORSION": BROWN,
        "ESTRIBOS": WHITE,
        "CORTE": WHITE,
        "COTAS": GREEN,
        "ALERTA": RED,
    }
    for name, color in layers.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    doc.units = 4
    doc.header["$INSUNITS"] = 4
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 3
    doc.header["$MEASUREMENT"] = 1
    return doc


def draw_logo(msp, x, y, width, height):
    cx = x + width / 2
    top = y + height - 5.0
    sw, sh = 27.0, 28.0
    left, right, bottom = cx - sw / 2, cx + sw / 2, top - sh
    polyline(msp, [(left, top), (right, top), (right - 3, bottom + 7),
                   (cx, bottom), (left + 3, bottom + 7)], "ROTULO", WHITE, 25, True)
    line(msp, (left + 3, top - 7), (right - 3, top - 7), "ROTULO", WHITE, 18)
    line(msp, (cx, top - 2), (cx, bottom + 3), "ROTULO", WHITE, 18)
    add_text(msp, "UN", (cx, bottom + 9), 4.5, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)


def draw_titleblock(msp, title, sheet_number):
    x, y = MAIN_RIGHT, MARGIN
    w, h = TITLEBLOCK_W, SHEET_H - 2 * MARGIN
    rect(msp, x, y, w, h, "MARCO", WHITE, 35)

    # Bloques verticales compactos inspirados en la lámina de referencia.
    levels = [h, h - 60, h - 112, h - 184, h - 300, 78, 0]
    for level in levels[1:-1]:
        line(msp, (x, y + level), (x + w, y + level), "ROTULO", WHITE, 18)
    draw_logo(msp, x, y + h - 60, w, 60)
    add_text(msp, "UNIVERSIDAD NACIONAL DE COLOMBIA", (x + w / 2, y + h - 48),
             2.5, "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "FACULTAD DE INGENIERIA", (x + w / 2, y + h - 74), 2.7,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "DISEÑO ESTRUCTURAL - GRUPO 6", (x + w / 2, y + h - 88), 2.7,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "EDIFICIO RESIDENCIAL", (x + w / 2, y + h - 128), 3.2,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "SANTA MARTA", (x + w / 2, y + h - 143), 3.0,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, title, (x + w / 2, y + h - 215), 4.0, "ROTULO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "ELEVACIONES, CORTES Y", (x + w / 2, y + h - 242), 2.7,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "LONGITUDES DE ANCLAJE", (x + w / 2, y + h - 254), 2.7,
             "ROTULO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "NO EMITIR PARA CONSTRUCCION", (x + w / 2, y + 116), 2.8,
             "ALERTA", RED, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "DETALLE ACADEMICO", (x + w / 2, y + 102), 2.6,
             "ALERTA", RED, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "Formato: ISO B2 horizontal", (x + 5, y + 61), 2.4, "ROTULO", WHITE)
    add_text(msp, "Tamaño: 707 x 500 mm", (x + 5, y + 49), 2.4, "ROTULO", WHITE)
    add_text(msp, "Unidades de lámina: mm", (x + 5, y + 37), 2.4, "ROTULO", WHITE)
    add_text(msp, f"Fecha: {DATE_TEXT}", (x + 5, y + 22), 2.4, "ROTULO", WHITE)
    add_text(msp, f"Lamina: {sheet_number}", (x + 5, y + 9), 3.0, "ROTULO", WHITE)


def bar_positions(n: int, width: float, y: float):
    """Posiciones físicas de flexión con separación libre mínima de 25 mm."""
    if n <= 0:
        return []
    db = DB_LONG
    required = (n - 1) * (db + CLEAR_BAR)
    available = width - 2 * (40 + 12.7 + db / 2)
    if required > available + 1e-6:
        raise ValueError(f"No caben {n} barras Nº5 en una fila de {width} mm")
    start = (width - required) / 2
    return [(start + i * (db + CLEAR_BAR), y) for i in range(n)]


def torsion_positions(n: int, width: float, height: float):
    """Distribución dedicada que no invade las filas de acero de flexión."""
    if n <= 0:
        return []
    x_edge = 40 + 12.7 + DB_LONG / 2
    y_inner = 112.0
    left, right = x_edge, width - x_edge
    bottom, top = y_inner, height - y_inner
    if n % 4 != 0 or n < 4:
        raise ValueError(f"Se esperaba un múltiplo de 4 barras torsionales, recibido {n}")
    per_side = n // 4
    points = []
    # Barras cercanas a caras superior e inferior.
    for i in range(per_side):
        fraction = i / max(per_side - 1, 1)
        x = left + fraction * (right - left) if per_side > 1 else width / 2
        points.append((x, bottom))
        points.append((x, top))
    # Barras de caras laterales, sin repetir las esquinas de la franja interior.
    for i in range(per_side):
        fraction = (i + 1) / (per_side + 1)
        y = bottom + fraction * (top - bottom)
        points.append((left, y))
        points.append((right, y))
    return points[:n]


def assert_section_clearance(n_top: int, n_bottom: int, n_tor: int,
                             b: float, h: float):
    y_flex = 40 + 12.7 + DB_LONG / 2
    flex = bar_positions(n_bottom, b, y_flex) + bar_positions(n_top, b, h - y_flex)
    torsion = torsion_positions(n_tor, b, h)
    labelled = [("F", p) for p in flex] + [("T", p) for p in torsion]
    minimum = DB_LONG + CLEAR_BAR
    for i, (kind_i, p_i) in enumerate(labelled):
        for kind_j, p_j in labelled[i + 1:]:
            distance = math.dist(p_i, p_j)
            if distance + 1e-6 < minimum:
                raise ValueError(
                    f"Superposición {kind_i}/{kind_j}: {distance:.1f} < {minimum:.1f} mm"
                )


def map_section_point(px, py, b, h, left, bottom, width, height):
    return left + px / b * width, bottom + py / h * height


def draw_section(msp, cx, cy, detail, label, center=False, scale=1.0):
    sec_h = 25.0 * scale
    sec_w = sec_h * detail["b"] / detail["h"]
    left, bottom = cx - sec_w / 2, cy - sec_h / 2
    rect(msp, left, bottom, sec_w, sec_h, "CORTE", WHITE, 20)
    inset = 2.2 * scale
    rect(msp, left + inset, bottom + inset, sec_w - 2 * inset, sec_h - 2 * inset,
         "ESTRIBOS", WHITE, 18)
    if detail["legs"] == 4:
        line(msp, (left + sec_w / 3, bottom + inset),
             (left + sec_w / 3, bottom + sec_h - inset), "ESTRIBOS", WHITE, 15)
        line(msp, (left + 2 * sec_w / 3, bottom + inset),
             (left + 2 * sec_w / 3, bottom + sec_h - inset), "ESTRIBOS", WHITE, 15)

    n_top = 2 if center else detail["n_sup"]
    n_bottom = detail["n_inf"]
    y_flex = 40 + 12.7 + DB_LONG / 2
    assert_section_clearance(n_top, n_bottom, detail["n_lat"], detail["b"], detail["h"])
    for px, py in bar_positions(n_top, detail["b"], detail["h"] - y_flex):
        x, y = map_section_point(px, py, detail["b"], detail["h"], left, bottom, sec_w, sec_h)
        msp.add_circle((x, y), 0.72 * scale,
                       dxfattribs={"layer": "M1_SUP_CONT", "color": BLUE})
    for px, py in bar_positions(n_bottom, detail["b"], y_flex):
        x, y = map_section_point(px, py, detail["b"], detail["h"], left, bottom, sec_w, sec_h)
        msp.add_circle((x, y), 0.72 * scale,
                       dxfattribs={"layer": "M4_INF_CONT", "color": RED})
    for px, py in torsion_positions(detail["n_lat"], detail["b"], detail["h"]):
        x, y = map_section_point(px, py, detail["b"], detail["h"], left, bottom, sec_w, sec_h)
        msp.add_circle((x, y), 0.64 * scale,
                       dxfattribs={"layer": "M5_TORSION", "color": BROWN})

    add_text(msp, label, (cx, bottom - 3.3 * scale), 1.65 * scale,
             "TEXTO", WHITE, TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, f"{int(detail['b'])}x{int(detail['h'])}",
             (cx, bottom - 6.0 * scale), 1.45 * scale,
             "TEXTO", WHITE, TextEntityAlignment.MIDDLE_CENTER)


def draw_hooked_bar(msp, x0, x1, y, hook_depth, layer, color, left=True, right=True,
                    lineweight=35):
    points = []
    if left:
        points.extend([(x0, y - hook_depth), (x0, y)])
    else:
        points.append((x0, y))
    points.append((x1, y))
    if right:
        points.append((x1, y - hook_depth))
    return polyline(msp, points, layer, color, lineweight)


def draw_simple_dimension(msp, x0, x1, y, text, color=GREEN, text_height=1.6):
    line(msp, (x0, y), (x1, y), "COTAS", color, 15)
    line(msp, (x0, y - 1.2), (x0, y + 1.2), "COTAS", color, 15)
    line(msp, (x1, y - 1.2), (x1, y + 1.2), "COTAS", color, 15)
    add_text(msp, text, ((x0 + x1) / 2, y + 1.3), text_height,
             "COTAS", color, TextEntityAlignment.MIDDLE_CENTER)


def draw_beam_panel(msp, design, detail, x, y, width, height):
    cuts = cut_length_ranges(design, detail)
    rect(msp, x, y, width, height, "GUIA", LIGHT_GRAY, 9)
    add_text(msp, f"VIGA {detail['group']} - {int(detail['b'])}x{int(detail['h'])} mm",
             (x + width / 2, y + height - 4.0), 2.45, "TITULO", MAGENTA,
             TextEntityAlignment.MIDDLE_CENTER)

    axis_l, axis_r = x + 31.0, x + width - 11.0
    support_half = 4.6
    face_l, face_r = axis_l + support_half, axis_r - support_half
    beam_y = y + height - 30.0
    beam_h = 13.0
    clear_draw = face_r - face_l

    # Apoyos, ejes y contorno geométrico.
    rect(msp, axis_l - support_half, beam_y - 4.2, 2 * support_half, beam_h + 8.4,
         "APOYOS", CYAN, 18)
    rect(msp, axis_r - support_half, beam_y - 4.2, 2 * support_half, beam_h + 8.4,
         "APOYOS", CYAN, 18)
    line(msp, (axis_l, beam_y - 6), (axis_l, beam_y + beam_h + 8), "EJES", GRAY, 9)
    line(msp, (axis_r, beam_y - 6), (axis_r, beam_y + beam_h + 8), "EJES", GRAY, 9)
    rect(msp, face_l, beam_y, clear_draw, beam_h, "CONTORNO", WHITE, 18)
    add_text(msp, "I", (axis_l, beam_y + beam_h + 5.2), 1.6, "EJES", GRAY,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(msp, "J", (axis_r, beam_y + beam_h + 5.2), 1.6, "EJES", GRAY,
             TextEntityAlignment.MIDDLE_CENTER)

    # Una polilínea por marca: no se dibuja una línea coincidente por cada barra.
    anchor_m1_l, anchor_m1_r = axis_l - 1.2, axis_r + 1.2
    anchor_m2_l, anchor_m3_r = axis_l - 3.2, axis_r + 3.2
    anchor_m4_l, anchor_m4_r = axis_l + 1.2, axis_r - 1.2
    anchor_m5_l, anchor_m5_r = axis_l + 3.0, axis_r - 3.0
    hook = 4.4
    y_m1 = beam_y + beam_h - 2.0
    y_m2 = beam_y + beam_h - 5.0
    y_m3 = beam_y + beam_h - 7.8
    y_m4 = beam_y + 2.1
    y_m5 = beam_y + beam_h / 2

    draw_hooked_bar(msp, anchor_m1_l, anchor_m1_r, y_m1, hook, "M1_SUP_CONT", BLUE)
    extra = max(detail["n_sup"] - 2, 0)
    ext = max(clear_draw / 4, 23.0)
    if extra:
        draw_hooked_bar(msp, anchor_m2_l, min(face_l + ext, (face_l + face_r) / 2),
                        y_m2, hook, "M2_SUP_IZQ", YELLOW, left=True, right=False)
        draw_hooked_bar(msp, max(face_r - ext, (face_l + face_r) / 2), anchor_m3_r,
                        y_m3, hook, "M3_SUP_DER", YELLOW, left=False, right=True)
    # Gancho inferior orientado hacia arriba en los extremos.
    polyline(msp, [(anchor_m4_l, y_m4 + hook), (anchor_m4_l, y_m4),
                   (anchor_m4_r, y_m4), (anchor_m4_r, y_m4 + hook)],
             "M4_INF_CONT", RED, 35)
    if detail["n_lat"]:
        draw_hooked_bar(msp, anchor_m5_l, anchor_m5_r, y_m5, 3.4,
                        "M5_TORSION", BROWN, True, True, 30)

    # Cortes A/B/C claramente separados.
    for fraction, label in ((0.10, "A"), (0.50, "B"), (0.90, "C")):
        px = face_l + fraction * clear_draw
        line(msp, (px, beam_y - 2), (px, beam_y + beam_h + 2), "CORTE", WHITE, 9)
        add_text(msp, label, (px, beam_y + beam_h + 2.6), 1.35, "CORTE", WHITE,
                 TextEntityAlignment.MIDDLE_CENTER)

    draw_simple_dimension(
        msp, axis_l, axis_r, beam_y - 7.0,
        f"L SAP I-J = {fmt_range(detail['Lmin']/1000, detail['Lmax']/1000, 3, ' m')}",
    )
    add_text(msp,
             f"Ln = {fmt_range(cuts['ln_min']/1000, cuts['ln_max']/1000, 3, ' m')}",
             ((axis_l + axis_r) / 2, beam_y - 10.0), 1.45, "TEXTO", WHITE,
             TextEntityAlignment.MIDDLE_CENTER)

    # Lista de barras y longitudes de corte; cada línea corresponde a una marca gráfica.
    list_y = beam_y - 14.0
    rows = [
        ("M1", f"2#5 SUP CONT | Lc={fmt_range(cuts['continuous_min'], cuts['continuous_max'], 0, ' mm')}", BLUE),
        ("M2/M3", f"{extra}#5 SUP/APOYO | Lc={fmt_range(cuts['support_min'], cuts['support_max'], 0, ' mm')}", YELLOW),
        ("M4", f"{detail['n_inf']}#5 INF CONT | Lc={fmt_range(cuts['continuous_min'], cuts['continuous_max'], 0, ' mm')}", RED),
        ("M5", f"{detail['n_lat']}#5 TOR DEDIC. | Lc={fmt_range(cuts['continuous_min'], cuts['continuous_max'], 0, ' mm')}", BROWN),
    ]
    for idx, (mark, text, color) in enumerate(rows):
        yy = list_y - idx * 3.2
        add_text(msp, mark, (x + 6, yy), 1.45, "TEXTO", color)
        add_text(msp, text, (x + 22, yy), 1.42, "TEXTO", color)

    # Anclajes y estribos, explícitos dentro de cada panel.
    st_tail_raw = max(6 * detail["st_db"], 75.0)
    st_tail = round_up(st_tail_raw)
    st_bend = round_up(6 * detail["st_db"])
    note_y = list_y - 13.6
    add_text(msp,
             f"#5: ld sup={LD_SUP:.0f}; ld inf={LD_INF:.0f}; ldh={LDH:.0f}; 90°: cola={TAIL_90:.0f}, Dint>={BEND_90:.0f} mm",
             (x + 6, note_y), 1.35, "TEXTO", WHITE)
    add_text(msp,
             f"E1 {detail['st_label']} {detail['legs']}R: 1ro<=50; @{int(detail['s_end'])} en 2h; @{int(detail['s_center'])} centro; 135° cola={st_tail:.0f}, Dint>={st_bend:.0f}",
             (x + 6, note_y - 3.0), 1.35, "TEXTO", WHITE)

    # Tres cortes sin barras coincidentes.
    cut_y = y + 15.5
    scale = 0.82 if height < 120 else 1.0
    draw_section(msp, x + width * 0.29, cut_y, detail, "A-A APOYO I", False, scale)
    draw_section(msp, x + width * 0.52, cut_y, detail, "B-B CENTRO", True, scale)
    draw_section(msp, x + width * 0.75, cut_y, detail, "C-C APOYO J", False, scale)

    add_text(msp, f"{detail['count']} frames | {detail['variant_count']} longitudes",
             (x + 5, y + 3.0), 1.35, "TEXTO", WHITE)
    add_text(msp, "Marcas separadas; cantidades reales en cortes",
             (x + width - 5, y + 3.0), 1.35, "TEXTO", GREEN,
             TextEntityAlignment.RIGHT)


def draw_general_notes(msp, groups):
    x = MARGIN + 3
    y = MARGIN + 3
    add_text(msp, "DETALLE DE ANCLAJE Nº5", (x, y + 16), 2.0, "TITULO", MAGENTA)
    # Minidetalle de gancho 90°.
    hx = x + 50
    hy = y + 15
    polyline(msp, [(hx, hy - 9), (hx, hy), (hx + 27, hy)], "M1_SUP_CONT", BLUE, 35)
    draw_simple_dimension(msp, hx, hx + 27, hy + 4.2, f"ldh adopt. {LDH:.0f} mm", BLUE, 1.35)
    draw_simple_dimension(msp, hx - 4.0, hx - 4.0, hy - 9, "", BLUE, 1.0)
    add_text(msp, f"cola 12db = {TAIL_90:.0f} mm", (hx - 1, hy - 11.8), 1.35,
             "TEXTO", BLUE)
    add_text(msp, f"Dint >= {BEND_90:.0f} mm", (hx + 31, hy - 1), 1.35,
             "TEXTO", BLUE)
    add_text(msp,
             "ld recto: superior 480 mm; inferior 370 mm. Si no cabe recto, usar gancho estándar y verificar confinamiento.",
             (x + 135, y + 15), 1.55, "TEXTO", WHITE)
    add_text(msp,
             "Lc: barras continuas = Ln+2ldh; barras negativas de apoyo = Ln/4+ldh. Longitudes redondeadas hacia arriba.",
             (x + 135, y + 9), 1.55, "TEXTO", WHITE)
    add_text(msp, "Grupos: " + ", ".join(groups), (x + 135, y + 3), 1.55,
             "TEXTO", WHITE)


def add_b2_layout(doc):
    layout = doc.layouts.new("B2_HORIZONTAL")
    if "Layout1" in doc.layout_names():
        doc.layouts.delete("Layout1")
    layout.page_setup(
        size=(SHEET_W, SHEET_H), margins=(0, 0, 0, 0), units="mm",
        rotation=0, scale=(1, 1), name="ISO B2 horizontal 707x500 mm 1:1",
        device="DWG To PDF.pc3",
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

    content_left = MARGIN + 3
    content_right = MAIN_RIGHT - 3
    content_bottom = MARGIN + 29
    content_top = SHEET_H - MARGIN - 3
    gap_x, gap_y = 4.0, 4.0
    cell_w = (content_right - content_left - gap_x * (columns - 1)) / columns
    cell_h = (content_top - content_bottom - gap_y * (rows - 1)) / rows
    for index, detail in enumerate(details):
        row_from_top = index // columns
        col = index % columns
        x = content_left + col * (cell_w + gap_x)
        y = content_top - (row_from_top + 1) * cell_h - row_from_top * gap_y
        draw_beam_panel(msp, design, detail, x, y, cell_w, cell_h)

    draw_general_notes(msp, [d["group"] for d in details])
    add_b2_layout(doc)
    doc.saveas(path)


def audit_detail_layout(details):
    for detail in details:
        assert_section_clearance(detail["n_sup"], detail["n_inf"], detail["n_lat"],
                                 detail["b"], detail["h"])
        assert_section_clearance(2, detail["n_inf"], detail["n_lat"],
                                 detail["b"], detail["h"])
    assert math.isclose(LD_INF, 370.0)
    assert math.isclose(LD_SUP, 480.0)
    assert math.isclose(LDH, 305.0)
    assert math.isclose(TAIL_90, 195.0)
    assert math.isclose(BEND_90, 100.0)


def main():
    design = load_module(DESIGN_SCRIPT, "beam_design_b2")
    group_module = load_module(GROUP_SCRIPT, "beam_group_b2")
    records, _ = design.extract_inputs()
    results = [design.design_record(record) for record in records]
    details_by_group = {
        group: group_module.group_detail(design, group, records, results)
        for group in design.GROUP_ORDER
    }
    all_details = [details_by_group[g] for g in design.GROUP_ORDER]
    audit_detail_layout(all_details)

    vc_groups = ["VC1", "VC2", "VC3", "VC4", "VC5", "VC6", "VC7"]
    vr_groups = ["VR1", "VR N1", "VR2", "VR3", "VRAUX"]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    vc_path = OUTPUT_DIR / "LAMINA-B2-VIGAS-DE-CARGA-VC-CORREGIDA.dxf"
    vr_path = OUTPUT_DIR / "LAMINA-B2-VIGAS-DE-RIGIDEZ-VR-CORREGIDA.dxf"
    make_sheet(vc_path, "VIGAS DE CARGA", "V-01", [details_by_group[g] for g in vc_groups],
               design, 2, 4)
    make_sheet(vr_path, "VIGAS DE RIGIDEZ", "V-02", [details_by_group[g] for g in vr_groups],
               design, 2, 3)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(vc_path, vc_path.name)
        archive.write(vr_path, vr_path.name)

    print(f"OK: {vc_path}")
    print(f"OK: {vr_path}")
    print(f"OK: {ZIP_PATH}")
    print(f"Desarrollo Nº5: ld inf={LD_INF:.0f}, ld sup={LD_SUP:.0f}, "
          f"ldh={LDH:.0f}, cola90={TAIL_90:.0f}, Dint={BEND_90:.0f} mm")
    print("Auditoría geométrica previa: 24 cortes sin barras superpuestas")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Genera dos archivos CAD B2 con las vigas completas por ejes y tramos.

La geometría y continuidad se reconstruyen desde resultados sap.xlsx y
geomatria sap.xlsx. Los armados por grupo se leen del Excel final del proyecto.
Cada familia se entrega en un único DXF con una presentación B2 por grupo:
VC1–VC7 en V-01 y VR1, VR N1, VR2, VR3 y VRAUX en V-02.
"""
from __future__ import annotations

import math
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment
from openpyxl import load_workbook

BASE = Path(__file__).resolve().parent
SAP = BASE / "resultados sap.xlsx"
GEOMETRY = BASE / "geomatria sap.xlsx"
DESIGN = BASE / "Diseño de vigas proyecto diseño DEF.xlsx"
OUT = BASE / "Planos-Autocad-B2-Vigas-Continuas"
ZIP = OUT / "PLANOS-AUTOCAD-B2-VIGAS-CONTINUAS.zip"

SHEET_W, SHEET_H = 707.0, 500.0
MARGIN = 7.0
FC, FY = 28.0, 420.0
DB_LONG = 15.9
COVER = 40.0
LD_INF, LD_SUP, LDH = 370.0, 480.0, 305.0
TAIL_90, BEND_90 = 195.0, 100.0
DATE = "18-07-2026"

VC_GROUPS = ["VC1", "VC2", "VC3", "VC4", "VC5", "VC6", "VC7"]
VR_GROUPS = ["VR1", "VR N1", "VR2", "VR3", "VRAUX"]
GROUPS = VC_GROUPS + VR_GROUPS
ALIASES = {"VR1 N1": "VR N1", "VR AUX": "VRAUX"}

# AutoCAD ACI colors.
BLACK = 7
RED = 1
YELLOW = 2
GREEN = 3
CYAN = 4
BLUE = 5
MAGENTA = 6
GRAY = 8
BROWN = 30
LIGHT = 9


def normalize_group(value) -> str:
    text = str(value).strip()
    return ALIASES.get(text, text)


def read_sap_table(workbook, sheet: str):
    ws = workbook[sheet]
    headers = [cell.value for cell in ws[2]]
    return [dict(zip(headers, row)) for row in ws.iter_rows(min_row=4, values_only=True)
            if row and row[0] is not None]


def load_sources():
    sap = load_workbook(SAP, read_only=True, data_only=True)
    geometry = load_workbook(GEOMETRY, read_only=True, data_only=True)

    grids = [row for row in read_sap_table(sap, "Grid Lines")
             if row.get("CoordSys") == "GLOBAL"]
    # SAP no exportó la línea 15 en la tabla, pero aparece en las plantas y en
    # la geometría a Y=37.70 m.
    grids.append({"CoordSys": "GLOBAL", "AxisDir": "Y", "GridID": "15", "XRYZCoord": 37.70})

    joints = {
        str(row["Joint"]): (
            float(row["GlobalX"]), float(row["GlobalY"]), float(row["GlobalZ"])
        )
        for row in read_sap_table(geometry, "Joint Coordinates")
    }
    frames = {str(row["Frame"]): row for row in read_sap_table(geometry, "Connectivity - Frame")}
    assignments = defaultdict(set)
    for row in read_sap_table(sap, "Groups 2 - Assignments"):
        if str(row.get("ObjectType")) != "Frame":
            continue
        group = normalize_group(row.get("GroupName"))
        if group in GROUPS:
            assignments[group].add(str(row["ObjectLabel"]))
    sap.close()
    geometry.close()

    if sum(len(assignments[group]) for group in GROUPS) != 592:
        raise ValueError("La asignación de grupos no contiene las 592 vigas esperadas")
    if any(not assignments[group] for group in GROUPS):
        raise ValueError("Falta al menos un grupo de vigas en el export SAP")

    design = load_workbook(DESIGN, read_only=True, data_only=True)
    details = {}
    for sheet in ("Vigas de Carga (7)", "Vigas de Rigidez (5)"):
        ws = design[sheet]
        headers = [cell.value for cell in ws[3]]
        for values in ws.iter_rows(min_row=4, values_only=True):
            if values[0] is None:
                continue
            row = dict(zip(headers, values))
            group = normalize_group(row["Grupo"])
            details[group] = {
                "group": group,
                "b": float(row["b adopt. (mm)"]),
                "h": float(row["h adopt. (mm)"]),
                "n_sup": int(row["Nº5 sup"]),
                "n_inf": int(row["Nº5 inf"]),
                "n_tor": int(row["Nº5 torsión dedicadas"]),
                "stirrup": str(row["Estribo"]).replace(" (referencia)", ""),
                "legs": int(row["Ramas"]),
                "s_end": int(round(float(row["s extremo DMO (mm; zona 2h)"]))),
                "s_center": int(round(float(row["s centro (mm)"]))),
                "db_st": float(row["db estribo (mm)"]),
                "count": int(row["N vigas"]),
            }
    design.close()
    if set(details) != set(GROUPS):
        raise ValueError(f"Los grupos del Excel final no coinciden: {sorted(details)}")
    return grids, joints, frames, assignments, details


def nearest_axis(grids, direction: str, coordinate: float, tolerance=0.22) -> str:
    candidates = [
        (abs(float(row["XRYZCoord"]) - coordinate), str(row["GridID"]))
        for row in grids if row.get("AxisDir") == direction
    ]
    if not candidates:
        return f"{coordinate:.2f}"
    distance, label = min(candidates)
    return label if distance <= tolerance else f"{coordinate:.2f}"


def frame_components(group, assignments, frames, joints, grids):
    ids = [frame for frame in assignments[group] if frame in frames]
    z_values = sorted({round(float(frames[frame]["CentroidZ"]), 3) for frame in ids})
    z = z_values[0]
    level = [frame for frame in ids if abs(float(frames[frame]["CentroidZ"]) - z) < 0.02]
    by_joint = defaultdict(list)
    for frame in level:
        by_joint[str(frames[frame]["JointI"])].append(frame)
        by_joint[str(frames[frame]["JointJ"])].append(frame)

    seen, components = set(), []
    for initial in sorted(level, key=lambda value: int(value)):
        if initial in seen:
            continue
        stack, found = [initial], []
        seen.add(initial)
        while stack:
            frame = stack.pop()
            found.append(frame)
            for joint in (str(frames[frame]["JointI"]), str(frames[frame]["JointJ"])):
                for neighbor in by_joint[joint]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
        components.append(found)

    chains = []
    for component in components:
        local = defaultdict(list)
        degree = Counter()
        for frame in component:
            i, j = str(frames[frame]["JointI"]), str(frames[frame]["JointJ"])
            local[i].append(frame); local[j].append(frame)
            degree[i] += 1; degree[j] += 1
        if max(degree.values()) > 2:
            raise ValueError(f"El grupo {group} forma una red ramificada en el nivel {z}")
        ends = [joint for joint, value in degree.items() if value == 1]
        start = min(ends or degree, key=lambda joint: (joints[joint][0], joints[joint][1]))
        used, ordered, current = set(), [], start
        while len(used) < len(component):
            options = [frame for frame in local[current] if frame not in used]
            if not options:
                break
            frame = options[0]
            used.add(frame)
            i, j = str(frames[frame]["JointI"]), str(frames[frame]["JointJ"])
            following = j if i == current else i
            ordered.append({
                "frame": frame,
                "joint_i": current,
                "joint_j": following,
                "length": float(frames[frame]["Length"]) * 1000.0,
            })
            current = following
        coordinates = [joints[ordered[0]["joint_i"]]] + [joints[item["joint_j"]] for item in ordered]
        dx = max(point[0] for point in coordinates) - min(point[0] for point in coordinates)
        dy = max(point[1] for point in coordinates) - min(point[1] for point in coordinates)
        direction = "X" if dx >= dy else "Y"
        axis_labels = [nearest_axis(grids, direction, point[0] if direction == "X" else point[1])
                       for point in coordinates]
        constant_direction = "Y" if direction == "X" else "X"
        constant_coordinate = sum(point[1] if direction == "X" else point[0] for point in coordinates) / len(coordinates)
        constant_axis = nearest_axis(grids, constant_direction, constant_coordinate)
        chains.append({
            "group": group,
            "z": z,
            "all_levels": z_values,
            "segments": ordered,
            "axes": axis_labels,
            "line_axis": constant_axis,
            "direction": direction,
            "coordinates": coordinates,
        })

    # Las vigas repetidas en ejes paralelos se muestran juntas cuando tienen
    # exactamente los mismos tramos. VRAUX se reduce a cuatro variantes de tramo.
    if group == "VRAUX":
        unique = {}
        for chain in chains:
            key = (tuple(round(item["length"]) for item in chain["segments"]), tuple(chain["axes"]))
            if key not in unique:
                unique[key] = chain
            else:
                unique[key]["line_axis"] += f"/{chain['line_axis']}"
        chains = list(unique.values())
    elif group in ("VR1", "VR N1"):
        unique = {}
        for chain in chains:
            key = (tuple(round(item["length"]) for item in chain["segments"]), tuple(chain["axes"]))
            if key not in unique:
                unique[key] = chain
            else:
                unique[key]["line_axis"] += f"/{chain['line_axis']}"
        chains = list(unique.values())
    return sorted(chains, key=lambda chain: (chain["axes"][0], chain["line_axis"]))


def add_layers(doc):
    colors = {
        "MARCO": BLACK, "CONTORNO": BLACK, "TEXTO": BLACK, "EJES": RED,
        "APOYOS": LIGHT, "ACERO_SUP_CONT": CYAN, "ACERO_SUP_APOYO": BLUE,
        "ACERO_INF": RED, "ACERO_TORSION": BROWN, "ESTRIBOS": GRAY,
        "COTAS": GREEN, "CORTE": MAGENTA, "NOTAS": BLACK,
    }
    for name, color in colors.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    if "DASHED" not in doc.linetypes:
        doc.linetypes.add("DASHED", pattern=[0.6, 0.3, -0.3], description="Dashed")


def add_text(space, text, point, height=2.0, layer="TEXTO", color=None,
             align=TextEntityAlignment.LEFT, rotation=0.0):
    attribs = {"height": height, "layer": layer, "rotation": rotation}
    if color is not None:
        attribs["color"] = color
    entity = space.add_text(str(text), dxfattribs=attribs)
    entity.set_placement(point, align=align)
    return entity


def line(space, start, end, layer="CONTORNO", color=None, weight=18, linetype=None):
    attribs = {"layer": layer, "lineweight": weight}
    if color is not None:
        attribs["color"] = color
    if linetype:
        attribs["linetype"] = linetype
    return space.add_line(start, end, dxfattribs=attribs)


def polyline(space, points, layer="CONTORNO", color=None, weight=25, close=False):
    attribs = {"layer": layer, "lineweight": weight}
    if color is not None:
        attribs["color"] = color
    return space.add_lwpolyline(points, close=close, dxfattribs=attribs)


def rectangle(space, x, y, width, height, layer="CONTORNO", color=None, weight=18):
    return polyline(space, [(x, y), (x + width, y), (x + width, y + height), (x, y + height)],
                    layer, color, weight, True)


def dimension(space, x0, x1, y, text, height=1.8):
    line(space, (x0, y), (x1, y), "COTAS", GREEN, 13)
    line(space, (x0, y - 1.2), (x0, y + 1.2), "COTAS", GREEN, 13)
    line(space, (x1, y - 1.2), (x1, y + 1.2), "COTAS", GREEN, 13)
    add_text(space, text, ((x0 + x1) / 2, y + 1.0), height, "COTAS", GREEN,
             TextEntityAlignment.MIDDLE_CENTER)


def choose_scale(total_length: float, max_width=600.0):
    for scale in (10, 20, 25, 30, 40, 50, 60, 75, 100):
        if total_length / scale <= max_width:
            return scale
    return math.ceil(total_length / max_width / 25) * 25


def draw_info_box(space, chain, detail, x, y, width=43.0, height=44.0):
    rectangle(space, x, y, width, height, "MARCO", BLACK, 20)
    add_text(space, f"VIGA {detail['group']}", (x + width / 2, y + height - 5), 2.6,
             "TEXTO", BLACK, TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, f"EJE {chain['line_axis']}", (x + width / 2, y + height - 11), 2.2,
             "TEXTO", BLACK, TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, f"{int(detail['b'])}x{int(detail['h'])} mm", (x + width / 2, y + height - 17), 1.9,
             "TEXTO", BLACK, TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, f"SUP {detail['n_sup']}#5", (x + 3, y + height - 24), 1.7)
    add_text(space, f"INF {detail['n_inf']}#5", (x + 3, y + height - 29), 1.7)
    add_text(space, f"TOR {detail['n_tor']}#5", (x + 3, y + height - 34), 1.7)
    add_text(space, f"NIVEL TIPO z={chain['z']:.1f} m", (x + 3, y + 4), 1.45)


def draw_axis(space, x, beam_y, beam_h, label):
    line(space, (x, beam_y - 11), (x, beam_y + beam_h + 17), "EJES", RED, 9, "DASHED")
    space.add_circle((x, beam_y + beam_h + 12), 3.5,
                     dxfattribs={"layer": "EJES", "color": RED, "lineweight": 18})
    add_text(space, label, (x, beam_y + beam_h + 12), 2.0, "EJES", RED,
             TextEntityAlignment.MIDDLE_CENTER)


def stirrup_positions(span_start, span_end, scale, s_end, s_center, zone_mm):
    length_mm = (span_end - span_start) * scale
    zone = min(zone_mm, length_mm / 2)
    values = []
    # Primer estribo a 50 mm desde cada cara; zonas 2h en ambos extremos.
    left = 50.0
    while left < zone - 1e-6:
        values.append(span_start + left / scale)
        left += s_end
    center = zone + s_center
    while center < length_mm - zone - 1e-6:
        values.append(span_start + center / scale)
        center += s_center
    right = length_mm - 50.0
    while right > length_mm - zone + 1e-6:
        values.append(span_start + right / scale)
        right -= s_end
    return sorted(set(round(value, 4) for value in values))


def clear_span(length_mm):
    return max(length_mm - 600.0, 0.5 * length_mm)


def draw_chain(space, chain, detail, row_y, row_height=78.0):
    info_x = 8.5
    x0 = 57.0
    total = sum(item["length"] for item in chain["segments"])
    scale = choose_scale(total, 635.0)
    drawn = total / scale
    x1 = x0 + drawn
    beam_h = max(8.0, detail["h"] / 25.0)
    beam_y = row_y + 27.0
    draw_info_box(space, chain, detail, info_x, beam_y - 8.0, 43.0, 44.0)

    nodes = [x0]
    for segment in chain["segments"]:
        nodes.append(nodes[-1] + segment["length"] / scale)

    # Contorno y apoyos en cada eje.
    rectangle(space, x0, beam_y, drawn, beam_h, "CONTORNO", BLACK, 22)
    for x, label in zip(nodes, chain["axes"]):
        support_width = max(4.0, 500.0 / scale)
        rectangle(space, x - support_width / 2, beam_y - 4.0, support_width,
                  beam_h + 8.0, "APOYOS", LIGHT, 15)
        draw_axis(space, x, beam_y, beam_h, label)

    # Estribos reales por cada tramo.
    for idx, segment in enumerate(chain["segments"]):
        start, end = nodes[idx], nodes[idx + 1]
        for x in stirrup_positions(start, end, scale, detail["s_end"], detail["s_center"],
                                   2 * detail["h"]):
            line(space, (x, beam_y + 1.0), (x, beam_y + beam_h - 1.0),
                 "ESTRIBOS", GRAY, 9)
        add_text(space,
                 f"{detail['stirrup'].replace(' cerrado','')} {detail['legs']}R @{detail['s_end']} (2h) / @{detail['s_center']} ctr",
                 ((start + end) / 2, beam_y + beam_h / 2 - 0.8), 1.25,
                 "ESTRIBOS", GRAY, TextEntityAlignment.MIDDLE_CENTER)

    # M1: dos barras superiores continuas con ganchos en extremos.
    y_top = beam_y + beam_h - 2.0
    polyline(space, [(x0, y_top - 6.0), (x0, y_top), (x1, y_top), (x1, y_top - 6.0)],
             "ACERO_SUP_CONT", CYAN, 35)
    continuous_cut = clear_span(total) + 2 * LDH
    add_text(space, f"M1  2#5 CONT.  Lc={continuous_cut:.0f} mm", ((x0 + x1) / 2, y_top + 3.0),
             1.55, "ACERO_SUP_CONT", CYAN, TextEntityAlignment.MIDDLE_CENTER)

    # M2: barras negativas sobre cada apoyo, alternadas verticalmente para evitar superposición.
    extra = max(detail["n_sup"] - 2, 0)
    if extra:
        for index, x in enumerate(nodes):
            if index == 0:
                right = nodes[1]
                extent_r = (right - x) / 4
                start, end = x - LDH / scale, x + extent_r
                cut = clear_span(chain["segments"][0]["length"]) / 4 + LDH
            elif index == len(nodes) - 1:
                left = nodes[-2]
                extent_l = (x - left) / 4
                start, end = x - extent_l, x + LDH / scale
                cut = clear_span(chain["segments"][-1]["length"]) / 4 + LDH
            else:
                extent_l = (x - nodes[index - 1]) / 4
                extent_r = (nodes[index + 1] - x) / 4
                start, end = x - extent_l, x + extent_r
                cut = (chain["segments"][index - 1]["length"] / 4
                       + chain["segments"][index]["length"] / 4 + 500.0)
            y = beam_y + beam_h - 4.5 - (index % 2) * 2.2
            points = [(start, y)]
            if index == 0:
                points = [(start, y - 5.0), (start, y)]
            points.append((end, y))
            if index == len(nodes) - 1:
                points.append((end, y - 5.0))
            polyline(space, points, "ACERO_SUP_APOYO", BLUE, 30)
            add_text(space, f"M2 {extra}#5 L={cut:.0f}", (x, y + 1.2), 1.15,
                     "ACERO_SUP_APOYO", BLUE, TextEntityAlignment.MIDDLE_CENTER)

    # M3: barras inferiores independientes por tramo, con ganchos en ambas caras.
    for idx, segment in enumerate(chain["segments"]):
        start, end = nodes[idx], nodes[idx + 1]
        y = beam_y + 2.0 + (idx % 2) * 1.8
        support_shift = min(2.0, 150.0 / scale)
        polyline(space, [(start + support_shift, y + 5.0), (start + support_shift, y),
                         (end - support_shift, y), (end - support_shift, y + 5.0)],
                 "ACERO_INF", RED, 35)
        cut = clear_span(segment["length"]) + 2 * LDH
        add_text(space, f"M3 {detail['n_inf']}#5 L={cut:.0f}", ((start + end) / 2, y - 2.1),
                 1.2, "ACERO_INF", RED, TextEntityAlignment.MIDDLE_CENTER)

    # M4: acero torsional dedicado continuo, separado de flexión.
    if detail["n_tor"]:
        y_tor = beam_y + beam_h / 2 + 2.4
        polyline(space, [(x0 + 1.0, y_tor), (x1 - 1.0, y_tor)],
                 "ACERO_TORSION", BROWN, 26)
        add_text(space, f"M4 {detail['n_tor']}#5 TORSIÓN DEDICADA", ((x0 + x1) / 2, y_tor + 1.6),
                 1.15, "ACERO_TORSION", BROWN, TextEntityAlignment.MIDDLE_CENTER)

    # Cortes y cotas de cada tramo.
    cut_locations = []
    if len(nodes) >= 3:
        cut_locations = [(nodes[1], "A"), ((nodes[1] + nodes[2]) / 2, "B"), (nodes[-2], "C")]
    else:
        cut_locations = [(x0 + drawn * 0.15, "A"), (x0 + drawn * 0.50, "B"), (x0 + drawn * 0.85, "C")]
    for x, label in cut_locations:
        line(space, (x, beam_y - 2.5), (x, beam_y + beam_h + 2.5), "CORTE", MAGENTA, 13)
        add_text(space, label, (x, beam_y + beam_h + 5.2), 1.5, "CORTE", MAGENTA,
                 TextEntityAlignment.MIDDLE_CENTER)

    dim_y = beam_y - 10.0
    for idx, segment in enumerate(chain["segments"]):
        dimension(space, nodes[idx], nodes[idx + 1], dim_y, f"{segment['length'] / 1000:.3f} m", 1.3)
        add_text(space, f"F{segment['frame']}", ((nodes[idx] + nodes[idx + 1]) / 2, dim_y - 2.7),
                 1.1, "TEXTO", BLACK, TextEntityAlignment.MIDDLE_CENTER)
    dimension(space, x0, x1, dim_y - 6.0, f"TOTAL SAP I-J = {total / 1000:.3f} m", 1.5)
    add_text(space, f"ESC. H 1:{scale} | V 1:25 | Ejes/tramos obtenidos de SAP",
             (x1, row_y + 1.0), 1.35, "TEXTO", BLACK, TextEntityAlignment.RIGHT)
    return {"scale": scale, "total": total, "nodes": nodes, "beam_y": beam_y, "beam_h": beam_h}


def flex_positions(count, width, y, margin=65.0):
    if count <= 0:
        return []
    if count == 1:
        return [(width / 2, y)]
    usable = width - 2 * margin
    return [(margin + index * usable / (count - 1), y) for index in range(count)]


def torsion_positions(count, width, height):
    if count <= 0:
        return []
    # Franja independiente de las filas superior/inferior para evitar colisiones.
    per_side = max(1, count // 4)
    left, right = 90.0, width - 90.0
    bottom, top = 110.0, height - 110.0
    points = []
    for index in range(per_side):
        fraction = (index + 1) / (per_side + 1)
        points.append((left + fraction * (right - left), bottom))
        points.append((left + fraction * (right - left), top))
    remaining = count - len(points)
    per_vertical = max(0, remaining // 2)
    for index in range(per_vertical):
        fraction = (index + 1) / (per_vertical + 1)
        points.append((left, bottom + fraction * (top - bottom)))
        points.append((right, bottom + fraction * (top - bottom)))
    return points[:count]


def check_section_clearance(detail):
    b, h = detail["b"], detail["h"]
    y_bottom, y_top = 60.65, h - 60.65
    points = [("SUP", point) for point in flex_positions(detail["n_sup"], b, y_top)]
    points += [("INF", point) for point in flex_positions(detail["n_inf"], b, y_bottom)]
    points += [("TOR", point) for point in torsion_positions(detail["n_tor"], b, h)]
    minimum = DB_LONG + 25.0
    for idx, (kind_a, a) in enumerate(points):
        for kind_b, bpoint in points[idx + 1:]:
            if math.dist(a, bpoint) < minimum - 1e-6:
                raise ValueError(f"Colisión {detail['group']} {kind_a}/{kind_b}: {a} {bpoint}")


def draw_section(space, cx, cy, detail, label, center=False):
    scale = 20.0
    width, height = detail["b"] / scale, detail["h"] / scale
    left, bottom = cx - width / 2, cy - height / 2
    rectangle(space, left, bottom, width, height, "CONTORNO", BLACK, 20)
    inset = COVER / scale
    rectangle(space, left + inset, bottom + inset, width - 2 * inset, height - 2 * inset,
              "ESTRIBOS", GRAY, 18)
    if detail["legs"] == 4:
        line(space, (left + width / 3, bottom + inset), (left + width / 3, bottom + height - inset),
             "ESTRIBOS", GRAY, 13)
        line(space, (left + 2 * width / 3, bottom + inset), (left + 2 * width / 3, bottom + height - inset),
             "ESTRIBOS", GRAY, 13)

    n_top = 2 if center else detail["n_sup"]
    for x, y in flex_positions(n_top, detail["b"], detail["h"] - 60.65):
        space.add_circle((left + x / scale, bottom + y / scale), 0.55,
                         dxfattribs={"layer": "ACERO_SUP_CONT", "color": CYAN})
    for x, y in flex_positions(detail["n_inf"], detail["b"], 60.65):
        space.add_circle((left + x / scale, bottom + y / scale), 0.55,
                         dxfattribs={"layer": "ACERO_INF", "color": RED})
    for x, y in torsion_positions(detail["n_tor"], detail["b"], detail["h"]):
        space.add_circle((left + x / scale, bottom + y / scale), 0.48,
                         dxfattribs={"layer": "ACERO_TORSION", "color": BROWN})
    add_text(space, label, (cx, bottom - 3.1), 1.55, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, f"{int(detail['b'])}x{int(detail['h'])} | 1:20", (cx, bottom - 5.6), 1.25,
             "TEXTO", BLACK, TextEntityAlignment.MIDDLE_CENTER)


def draw_bottom_details(space, detail, sheet_id):
    y = 48.0
    draw_section(space, 205, y + 15, detail, "A-A APOYO", False)
    draw_section(space, 280, y + 15, detail, "B-B CENTRO", True)
    draw_section(space, 355, y + 15, detail, "C-C APOYO", False)

    # Detalle de gancho 90° a escala 1:10.
    hx, hy = 430.0, 65.0
    polyline(space, [(hx, hy - TAIL_90 / 10), (hx, hy), (hx + LDH / 10, hy)],
             "ACERO_SUP_APOYO", BLUE, 35)
    dimension(space, hx, hx + LDH / 10, hy + 5.0, f"ldh={LDH:.0f} mm", 1.25)
    add_text(space, f"cola 90°={TAIL_90:.0f} mm", (hx - 3, hy - TAIL_90 / 10 - 3), 1.3,
             "ACERO_SUP_APOYO", BLUE)
    add_text(space, f"Dint>={BEND_90:.0f} mm | ESC. 1:10", (hx + 36, hy - 2), 1.3)
    add_text(space, f"ld recto #5: superior={LD_SUP:.0f} mm | inferior={LD_INF:.0f} mm",
             (430, 44), 1.45)
    add_text(space, "Si no cabe ld recto en apoyo, usar gancho estándar 90° con ldh indicado.",
             (430, 40), 1.25)

    # Rótulo inferior semejante al formato de referencia.
    rectangle(space, 7, 7, 690, 30, "MARCO", BLACK, 25)
    divisions = [118, 250, 390, 520, 610]
    for x in divisions:
        line(space, (x, 7), (x, 37), "MARCO", BLACK, 18)
    add_text(space, "UNIVERSIDAD NACIONAL DE COLOMBIA", (62.5, 28), 2.0, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "DISEÑO ESTRUCTURAL - GRUPO 6", (62.5, 20), 1.7, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "EDIFICIO RESIDENCIAL SANTA MARTA", (184, 25), 2.0, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, f"DESPIECE VIGA {detail['group']}", (320, 25), 2.5, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "ELEVACIÓN, CORTES Y ANCLAJES", (320, 16), 1.7, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "FORMATO ISO B2 707x500 mm", (455, 26), 1.8, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "COTAS EN mm | ESCALAS INDICADAS", (455, 17), 1.55, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "DETALLE ACADÉMICO", (565, 26), 1.8, "TEXTO", RED,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, "NO EMITIR PARA CONSTRUCCIÓN", (565, 17), 1.55, "TEXTO", RED,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, f"LÁMINA {sheet_id}", (653.5, 26), 2.1, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)
    add_text(space, DATE, (653.5, 17), 1.7, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)


def configure_layout(layout):
    layout.page_setup(size=(SHEET_W, SHEET_H), margins=(0, 0, 0, 0), units="mm",
                      rotation=0, scale=(1, 1), name="ISO B2 707x500 mm 1:1",
                      device="DWG To PDF.pc3")
    layout.dxf.plot_layout_flags = 0


def draw_group_layout(layout, group, chains, detail, sheet_id):
    configure_layout(layout)
    rectangle(layout, MARGIN, MARGIN, SHEET_W - 2 * MARGIN, SHEET_H - 2 * MARGIN,
              "MARCO", BLACK, 30)
    add_text(layout, f"DESPIECE DE VIGA COMPLETA {group}", (SHEET_W / 2, SHEET_H - 13),
             4.0, "TEXTO", BLACK, TextEntityAlignment.MIDDLE_CENTER)
    levels = ", ".join(f"{value:.1f}" for value in chains[0]["all_levels"])
    add_text(layout, f"Continuidad reconstruida de SAP | Niveles z={levels} m | {detail['count']} frames",
             (SHEET_W / 2, SHEET_H - 20), 1.8, "TEXTO", BLACK,
             TextEntityAlignment.MIDDLE_CENTER)

    count = len(chains)
    top, bottom = SHEET_H - 29.0, 103.0
    usable = top - bottom
    row_height = usable / max(count, 1)
    if row_height < 54:
        raise ValueError(f"No cabe el grupo {group}: {count} cadenas en B2")
    for index, chain in enumerate(chains):
        row_y = top - (index + 1) * row_height
        draw_chain(layout, chain, detail, row_y, row_height)
    draw_bottom_details(layout, detail, sheet_id)


def create_family(path: Path, family_groups, chains_by_group, details, prefix):
    doc = ezdxf.new("R2018", setup=True)
    add_layers(doc)
    for index, group in enumerate(family_groups, 1):
        layout_name = group.replace(" ", "_")
        if index == 1:
            doc.layouts.rename("Layout1", layout_name)
            layout = doc.layouts.get(layout_name)
        else:
            layout = doc.layouts.new(layout_name)
        draw_group_layout(layout, group, chains_by_group[group], details[group], f"{prefix}-{index:02d}")
    doc.units = 4
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    doc.saveas(path)
    audit = doc.audit()
    if audit.has_errors:
        raise ValueError(f"Auditoría DXF con errores en {path.name}: {len(audit.errors)}")


def audit_inputs(chains_by_group, details):
    if set(chains_by_group) != set(GROUPS):
        raise ValueError("No se reconstruyeron los doce grupos")
    for group in GROUPS:
        if not chains_by_group[group]:
            raise ValueError(f"El grupo {group} no tiene cadenas")
        check_section_clearance(details[group])
        for chain in chains_by_group[group]:
            if len(chain["axes"]) != len(chain["segments"]) + 1:
                raise ValueError(f"Ejes/tramos inconsistentes en {group}")
            if len({item["frame"] for item in chain["segments"]}) != len(chain["segments"]):
                raise ValueError(f"Frames duplicados en la cadena {group}")
            if any(item["length"] <= 0 for item in chain["segments"]):
                raise ValueError(f"Longitud no positiva en {group}")
    if (LD_INF, LD_SUP, LDH, TAIL_90, BEND_90) != (370.0, 480.0, 305.0, 195.0, 100.0):
        raise ValueError("Las longitudes de desarrollo/ganchos no son las aprobadas")


def main():
    grids, joints, frames, assignments, details = load_sources()
    chains_by_group = {
        group: frame_components(group, assignments, frames, joints, grids)
        for group in GROUPS
    }
    audit_inputs(chains_by_group, details)
    OUT.mkdir(parents=True, exist_ok=True)
    vc_path = OUT / "V-01-VIGAS-DE-CARGA-CONTINUAS-B2.dxf"
    vr_path = OUT / "V-02-VIGAS-DE-RIGIDEZ-CONTINUAS-B2.dxf"
    create_family(vc_path, VC_GROUPS, chains_by_group, details, "V-01")
    create_family(vr_path, VR_GROUPS, chains_by_group, details, "V-02")
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(vc_path, vc_path.name)
        archive.write(vr_path, vr_path.name)
    print(f"OK {vc_path}")
    print(f"OK {vr_path}")
    print(f"OK {ZIP}")
    for group in GROUPS:
        signatures = ["-".join(chain["axes"]) for chain in chains_by_group[group]]
        print(f"{group}: {len(chains_by_group[group])} vigas completas tipo | {signatures}")


if __name__ == "__main__":
    main()

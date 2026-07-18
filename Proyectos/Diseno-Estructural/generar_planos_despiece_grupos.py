#!/usr/bin/env python3
"""Genera planos PDF y DXF de despiece para los 12 grupos de vigas."""
from __future__ import annotations

import importlib.util
import math
import re
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment
from reportlab.lib.colors import Color, HexColor, black, blue, red, white
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parent
DESIGN_SCRIPT = BASE / "generar_diseno_vigas_envolventes.py"
OUTPUT_DIR = BASE / "Planos-Despiece-Vigas"
COMBINED_PDF = BASE / "PLANOS-DESPIECE-VIGAS-POR-GRUPO.pdf"
DATE_TEXT = "17-07-2026"


def load_design():
    spec = importlib.util.spec_from_file_location("beam_design", DESIGN_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def safe_name(group):
    return re.sub(r"[^A-Za-z0-9_-]+", "-", group).strip("-")


def compress_frames(frames):
    numbers = sorted(int(x) for x in frames)
    ranges = []
    start = previous = numbers[0]
    for value in numbers[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append(str(start) if start == previous else f"{start}–{previous}")
        start = previous = value
    ranges.append(str(start) if start == previous else f"{start}–{previous}")
    return ", ".join(ranges)


def wrap_frame_text(text, max_chars=105):
    lines, current = [], ""
    for token in text.split(", "):
        candidate = token if not current else f"{current}, {token}"
        if len(candidate) > max_chars and current:
            lines.append(current)
            current = token
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def floor10(value):
    return max(10.0, math.floor(value / 10.0) * 10.0)


def group_detail(design, group, records, results):
    raw = [x for x in records if x["group"] == group]
    rows = [x for x in results if x["group"] == group]
    b = rows[0]["b"]
    h = rows[0]["h"]
    n_sup = max(x["neg"]["n"] for x in rows)
    n_inf = max(x["pos"]["n"] for x in rows)
    n_lat = max(x["n_torsion"] for x in rows)
    min_d = min(x["d"] for x in rows)
    max_at = max(x["at_s"] for x in rows)
    max_req = max(x["combined_s_required"] for x in rows)
    intense = any(x["Vs_req"] > 0.33 * math.sqrt(design.FC) * b * x["d"] / 1000 for x in rows)
    centerline = design.COVER + design.DB_ST / 2
    ph = 2 * ((b - 2 * centerline) + (h - 2 * centerline))
    candidates = []
    for label, db, area in (("Nº3", 9.5, 71.0), ("Nº4", 12.7, 129.0)):
        for legs in (2, 4):
            s_res = legs * area / max_req
            torsion_limit = ph / 8 if max_at > 0 else math.inf
            s_end = floor10(min(s_res, min_d / 4, 8 * design.DB_LONG, 24 * db, 300, torsion_limit))
            s_center = floor10(min(s_res, min_d / 4 if intense else min_d / 2, 600, torsion_limit))
            if s_end < 80 or (max_at > 0 and area / s_end < max_at - 1e-9):
                continue
            valid = True
            for result in rows:
                av = legs * area / s_end
                phi_vn = design.PHI_V * (result["Vc"] + max(av - 2 * result["at_s"], 0) * design.FYT * result["d"] / 1000)
                if phi_vn + 1e-8 < result["Vdesign"]:
                    valid = False
                    break
            if valid:
                candidates.append((legs * area / s_end, legs * area, -s_end, label, db, area, legs, s_end, s_center))
    if not candidates:
        label, db, area, legs, s_end, s_center = "Nº4", 12.7, 129.0, 4, 80.0, 80.0
    else:
        _, _, _, label, db, area, legs, s_end, s_center = min(candidates)
    failures = [x["frame"] for x in rows if not x["overall"]]
    sorted_rows = sorted(rows, key=lambda x: design.sort_frame(x["frame"]))
    lengths = sorted({round(x["L"] * 1000) for x in sorted_rows})
    variants = {length: f"V{index + 1}" for index, length in enumerate(lengths)}
    schedule = []
    for result in sorted_rows:
        length_mm = round(result["L"] * 1000)
        reasons = []
        if not result["interaction_ok"]:
            reasons.append("V-T")
        if not result["shear_section_ok"]:
            reasons.append("V")
        if not result["practical_stirrup_found"]:
            reasons.append("EST")
        schedule.append({
            "frame": result["frame"], "joint_i": result["joint_i"], "joint_j": result["joint_j"],
            "length": length_mm, "variant": variants[length_mm],
            "x": result["centroid_x"], "y": result["centroid_y"], "z": result["centroid_z"],
            "n_sup": result["neg"]["n"], "n_inf": result["pos"]["n"],
            "n_tor": result["n_torsion"], "stirrup": result["stirrup_label"],
            "legs": result["legs"], "s_end": result["s_end"], "s_center": result["s_center"],
            "status": "CUMPLE" if result["overall"] else "NO CUMPLE",
            "reason": "+".join(reasons) if reasons else "—",
        })
    return {
        "group": group,
        "frames": [x["frame"] for x in raw],
        "frame_text": compress_frames(x["frame"] for x in raw),
        "count": len(raw),
        "b": b, "h": h,
        "Lmin": min(x["L"] for x in raw) * 1000,
        "Lmax": max(x["L"] for x in raw) * 1000,
        "n_sup": n_sup, "n_inf": n_inf, "n_lat": n_lat,
        "bar_db": design.DB_LONG,
        "st_label": label, "st_db": db, "st_area": area, "legs": legs,
        "s_end": s_end, "s_center": s_center,
        "zone": 2 * h,
        "failures": failures,
        "design_ok": not failures,
        "ok": False,
        "schedule": schedule,
        "variant_count": len(variants),
        "color": design.COLORS[group],
        "mu_neg": max(x["Mu_neg"] for x in raw),
        "mu_pos": max(x["Mu_pos"] for x in raw),
        "vu": max(x["Vu_elastic"] for x in raw),
        "tu_raw": max(x["Tu_raw"] for x in raw),
        "tu_design": max(x["Tu"] for x in raw),
    }


def bar_positions(n, width, cover, max_per_layer=10):
    if n <= 0:
        return []
    first = min(n, max_per_layer)
    second = n - first
    points = []
    for layer, count in enumerate((first, second)):
        if count <= 0:
            continue
        if count == 1:
            xs = [width / 2]
        else:
            xs = [cover + i * (width - 2 * cover) / (count - 1) for i in range(count)]
        points.extend((x, layer) for x in xs)
    return points


def perimeter_bar_positions(n, width, height, cover):
    """Distribuye barras torsionales dedicadas en esquinas y caras del perímetro."""
    if n <= 0:
        return []
    left, right = cover, width - cover
    bottom, top = cover, height - cover
    points = [(left, bottom), (right, bottom), (right, top), (left, top)]
    remaining = max(0, n - 4)
    sides = [
        ((left, bottom), (right, bottom)),
        ((right, bottom), (right, top)),
        ((right, top), (left, top)),
        ((left, top), (left, bottom)),
    ]
    counts = [remaining // 4 + (1 if i < remaining % 4 else 0) for i in range(4)]
    for ((x1, y1), (x2, y2)), count in zip(sides, counts):
        for index in range(1, count + 1):
            fraction = index / (count + 1)
            points.append((x1 + fraction * (x2 - x1), y1 + fraction * (y2 - y1)))
    return points[:n]


def draw_pdf_page(c, d, page_number, total_pages):
    width, height = landscape(A3)
    margin = 10 * mm
    title_w = 58 * mm
    draw_right = width - margin - title_w
    c.setStrokeColor(black)
    c.setLineWidth(0.5)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    c.line(draw_right, margin, draw_right, height - margin)

    group_color = HexColor("#" + d["color"])
    c.setFillColor(group_color)
    c.rect(margin + 1 * mm, height - margin - 10 * mm, draw_right - margin - 2 * mm, 9 * mm, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString((margin + draw_right) / 2, height - margin - 7 * mm, f"DESPIECE DE VIGA — GRUPO {d['group']}")

    # Elevación longitudinal.
    x0 = margin + 28 * mm
    x1 = draw_right - 18 * mm
    y0 = height - margin - 82 * mm
    beam_h = 25 * mm
    support_w = 10 * mm
    Ldraw = x1 - x0
    c.setStrokeColor(HexColor("#666666"))
    c.rect(x0 - support_w, y0 - 8 * mm, support_w, beam_h + 16 * mm)
    c.rect(x1, y0 - 8 * mm, support_w, beam_h + 16 * mm)
    c.setStrokeColor(black)
    c.rect(x0, y0, Ldraw, beam_h)

    # Ejes y burbujas.
    for x, label in ((x0, "I"), (x1, "J")):
        c.setStrokeColor(HexColor("#999999"))
        c.line(x, y0 - 14 * mm, x, y0 + beam_h + 19 * mm)
        c.circle(x, y0 + beam_h + 14 * mm, 4 * mm)
        c.setFillColor(black)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x, y0 + beam_h + 12.8 * mm, label)

    # Barras continuas inferiores.
    c.setStrokeColor(red)
    c.setLineWidth(1.2)
    for i in range(min(d["n_inf"], 4)):
        yy = y0 + 3 * mm + i * 1.4 * mm
        c.line(x0 + 1 * mm, yy, x1 - 1 * mm, yy)
    # Dos barras superiores continuas y refuerzo adicional en apoyos.
    c.setStrokeColor(blue)
    for i in range(2):
        yy = y0 + beam_h - 3 * mm - i * 1.4 * mm
        c.line(x0 + 1 * mm, yy, x1 - 1 * mm, yy)
    extra = max(d["n_sup"] - 2, 0)
    extension = max(Ldraw / 3, 35 * mm)
    for i in range(min(extra, 5)):
        yy = y0 + beam_h - 6 * mm - i * 1.15 * mm
        c.line(x0 + 1 * mm, yy, x0 + extension, yy)
        c.line(x1 - extension, yy, x1 - 1 * mm, yy)
    # Barras longitudinales de torsión dedicadas y continuas.
    if d["n_lat"]:
        c.setStrokeColor(HexColor("#8B4513"))
        for i in range(min(d["n_lat"], 6)):
            yy = y0 + 8 * mm + i * max(1.2 * mm, (beam_h - 16 * mm) / max(min(d["n_lat"], 6) - 1, 1))
            c.line(x0 + 1 * mm, yy, x1 - 1 * mm, yy)

    # Estribos y zonas 2h.
    zone_draw = min(Ldraw * d["zone"] / max(d["Lmax"], 1), Ldraw / 2)
    positions = []
    for start, end, spacing in ((x0, x0 + zone_draw, d["s_end"]),
                                (x0 + zone_draw, x1 - zone_draw, d["s_center"]),
                                (x1 - zone_draw, x1, d["s_end"])):
        if end <= start:
            continue
        step = max(2.2 * mm, Ldraw * spacing / d["Lmax"])
        x = start + max(1.5 * mm, Ldraw * 50 / d["Lmax"])
        while x < end - 0.5 * mm:
            positions.append(x)
            x += step
    c.setStrokeColor(HexColor("#777777"))
    c.setLineWidth(0.35)
    for x in positions:
        c.line(x, y0 + 1 * mm, x, y0 + beam_h - 1 * mm)

    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x0, y0 + beam_h + 5 * mm, f"Superior: 2#{5} continuas + {extra}#{5} adicionales en cada apoyo")
    c.drawString(x0, y0 - 6 * mm, f"Inferior: {d['n_inf']}#5 continuas")
    c.drawString(x0, y0 - 11 * mm, f"Estribos {d['st_label']} — {d['legs']} ramas: 1º ≤50 mm; @ {int(d['s_end'])} mm en 2h; centro @ {int(d['s_center'])} mm")
    c.setFillColor(HexColor("#8B4513"))
    c.drawString(x0, y0 - 16 * mm, f"Torsión: {d['n_lat']}#5 dedicadas, continuas, perimetrales y adicionales a flexión")
    c.setFillColor(black)

    # Cota longitudinal.
    dim_y = y0 - 19 * mm
    c.setLineWidth(0.4)
    c.line(x0, dim_y, x1, dim_y)
    c.line(x0, dim_y - 2 * mm, x0, dim_y + 2 * mm)
    c.line(x1, dim_y - 2 * mm, x1, dim_y + 2 * mm)
    c.setFont("Helvetica", 8)
    c.drawCentredString((x0 + x1) / 2, dim_y + 2 * mm, f"L variable = {d['Lmin']/1000:.2f}–{d['Lmax']/1000:.2f} m")

    # Tres cortes.
    cut_y = margin + 53 * mm
    cut_positions = [x0 + 45 * mm, (x0 + x1) / 2, x1 - 45 * mm]
    cut_names = ["CORTE A-A — APOYO I", "CORTE B-B — CENTRO", "CORTE C-C — APOYO J"]
    section_h = 37 * mm
    section_w = section_h * d["b"] / d["h"]
    for cx, name in zip(cut_positions, cut_names):
        left = cx - section_w / 2
        bottom = cut_y
        c.setStrokeColor(black)
        c.setLineWidth(0.7)
        c.rect(left, bottom, section_w, section_h)
        inset = 3 * mm
        c.setStrokeColor(HexColor("#555555"))
        c.rect(left + inset, bottom + inset, section_w - 2 * inset, section_h - 2 * inset)
        if d["legs"] == 4:
            c.line(left + section_w / 3, bottom + inset, left + section_w / 3, bottom + section_h - inset)
            c.line(left + 2 * section_w / 3, bottom + inset, left + 2 * section_w / 3, bottom + section_h - inset)
        # Barras superiores e inferiores.
        top_n = d["n_sup"] if "APOYO" in name else 2
        bot_n = max(2, math.ceil(d["n_sup"] / 3)) if "APOYO" in name else d["n_inf"]
        for xx, layer in bar_positions(top_n, section_w, inset + 1.5 * mm, 7):
            c.setFillColor(blue)
            c.circle(left + xx, bottom + section_h - inset - 1.5 * mm - layer * 3 * mm, 1.1 * mm, fill=1, stroke=0)
        for xx, layer in bar_positions(bot_n, section_w, inset + 1.5 * mm, 7):
            c.setFillColor(red)
            c.circle(left + xx, bottom + inset + 1.5 * mm + layer * 3 * mm, 1.1 * mm, fill=1, stroke=0)
        if d["n_lat"]:
            c.setFillColor(HexColor("#8B4513"))
            for px, py in perimeter_bar_positions(d["n_lat"], section_w, section_h, inset + 3.5 * mm):
                c.circle(left + px, bottom + py, 0.85 * mm, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(cx, bottom + section_h + 5 * mm, name)
        c.setFont("Helvetica", 7)
        c.drawCentredString(cx, bottom - 5 * mm, f"{int(d['b'])}×{int(d['h'])} mm — rec. 40 mm")

    # Notas y listado de frames.
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(margin + 5 * mm, margin + 35 * mm, f"Nº de vigas: {d['count']} — Frames:")
    c.setFont("Helvetica", 6.5)
    text = c.beginText(margin + 5 * mm, margin + 30 * mm)
    text.setLeading(3.5 * mm)
    chunks = wrap_frame_text(d["frame_text"], 105)
    for chunk in chunks[:3]:
        text.textLine(chunk)
    c.drawText(text)

    c.setFont("Helvetica", 7)
    c.drawString(margin + 5 * mm, margin + 17 * mm, f"Mu− máx={d['mu_neg']:.1f} kN·m; Mu+ máx={d['mu_pos']:.1f} kN·m; Vu ENVCORT máx={d['vu']:.1f} kN")
    c.drawString(margin + 5 * mm, margin + 12 * mm, f"Tu diseño bruto={d['tu_design']:.1f} kN·m; sin reducción automática a φTcr; variantes de longitud: {d['variant_count']}")
    c.setFillColor(HexColor("#C00000"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margin + 5 * mm, margin + 7 * mm, "NO EMITIR PARA CONSTRUCCIÓN: detalle académico; usar el cuadro frame–nudos–longitud y completar planta/reanálisis SAP.")
    c.setFillColor(black)

    # Rótulo lateral.
    tx = draw_right
    tw = width - margin - draw_right
    c.setStrokeColor(black)
    c.setFillColor(black)
    blocks = [(height-margin-24*mm, 24), (height-margin-54*mm, 30), (height-margin-74*mm, 20),
              (height-margin-99*mm, 25), (height-margin-159*mm, 60), (margin+36*mm, 28), (margin, 36)]
    for y, hh in blocks:
        c.rect(tx, y, tw, hh*mm)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(tx + tw/2, height-margin-11*mm, "UNIVERSIDAD NACIONAL DE COLOMBIA")
    c.setFont("Helvetica", 7)
    c.drawCentredString(tx + tw/2, height-margin-17*mm, "DISEÑO ESTRUCTURAL — GRUPO 6")
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(tx + tw/2, height-margin-40*mm, "PROYECTO RESIDENCIAL")
    c.setFont("Helvetica", 8)
    c.drawCentredString(tx + tw/2, height-margin-47*mm, "SANTA MARTA")
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(tx + tw/2, height-margin-66*mm, f"VIGA {d['group']}")
    c.setFont("Helvetica", 7)
    c.drawCentredString(tx + tw/2, height-margin-86*mm, f"SECCIÓN {int(d['b'])}×{int(d['h'])} mm")
    c.drawCentredString(tx + tw/2, height-margin-92*mm, f"{d['count']} FRAMES")
    status_y = height-margin-127*mm
    c.setFillColor(HexColor("#C00000"))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(tx + tw/2, status_y, "NO EMITIR PARA CONSTRUCCIÓN")
    c.setFillColor(black)
    c.setFont("Helvetica", 6.2)
    if d["failures"]:
        c.drawCentredString(tx + tw/2, status_y-6*mm, f"{len(d['failures'])} frames NO CUMPLEN")
        failure_text = ", ".join(d["failures"][:8]) + ("…" if len(d["failures"]) > 8 else "")
        c.drawCentredString(tx + tw/2, status_y-11*mm, failure_text)
    else:
        c.drawCentredString(tx + tw/2, status_y-6*mm, "Verificación seccional cumple")
        c.drawCentredString(tx + tw/2, status_y-11*mm, "Falta planta/reanálisis global")
    c.setFont("Helvetica", 7)
    c.drawString(tx + 3*mm, margin + 53*mm, "Escala: indicadas")
    c.drawString(tx + 3*mm, margin + 47*mm, f"Fecha: {DATE_TEXT}")
    c.drawString(tx + 3*mm, margin + 41*mm, f"Lámina: {page_number}/{total_pages}")
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(tx + tw/2, margin + 20*mm, "DESPIECE DE VIGAS")
    c.setFont("Helvetica", 7)
    c.drawCentredString(tx + tw/2, margin + 12*mm, "PDF + DXF EDITABLE")


def draw_schedule_page(c, d, rows, page_number, total_pages, schedule_index, schedule_total):
    width, height = landscape(A3)
    margin = 10 * mm
    c.setStrokeColor(black)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    c.setFillColor(HexColor("#" + d["color"]))
    c.rect(margin, height - margin - 12 * mm, width - 2 * margin, 11 * mm, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin + 4 * mm, height - margin - 8 * mm,
                 f"CUADRO FRAME–NUDOS–LONGITUD–REFUERZO | {d['group']} | {schedule_index}/{schedule_total}")
    c.setFillColor(HexColor("#C00000"))
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(width - margin - 4 * mm, height - margin - 8 * mm, "NO EMITIR PARA CONSTRUCCIÓN")

    headers = ["Frame", "Var.", "Joint I", "Joint J", "L (mm)", "Xc", "Yc", "Z/nivel",
               "#5 sup", "#5 inf", "#5 tor.", "Estribo", "s ext/ctr", "Estado"]
    col_widths = [18, 12, 22, 22, 18, 17, 17, 18, 16, 16, 17, 34, 22, 27]
    x_positions = [margin]
    for value in col_widths:
        x_positions.append(x_positions[-1] + value * mm)
    table_top = height - margin - 25 * mm
    row_h = 9.2 * mm
    c.setFillColor(HexColor("#17365D"))
    c.rect(margin, table_top - row_h, x_positions[-1] - margin, row_h, fill=1, stroke=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 5.5)
    for index, header in enumerate(headers):
        c.drawCentredString((x_positions[index] + x_positions[index + 1]) / 2,
                            table_top - row_h + 3.2 * mm, header)
    c.setFillColor(black)
    for row_index, item in enumerate(rows):
        y_top = table_top - (row_index + 1) * row_h
        y_bottom = y_top - row_h
        if item["status"] != "CUMPLE":
            c.setFillColor(HexColor("#F4CCCC"))
            c.rect(margin, y_bottom, x_positions[-1] - margin, row_h, fill=1, stroke=0)
        c.setFillColor(black)
        c.setStrokeColor(HexColor("#808080"))
        c.line(margin, y_bottom, x_positions[-1], y_bottom)
        values = [
            item["frame"], item["variant"], item["joint_i"], item["joint_j"], item["length"],
            f"{item['x']:.2f}", f"{item['y']:.2f}", f"{item['z']:.2f}", item["n_sup"], item["n_inf"],
            item["n_tor"], f"{item['stirrup']} {item['legs']}R", f"{int(item['s_end'])}/{int(item['s_center'])}",
            item["status"] if item["reason"] == "—" else f"{item['status']} {item['reason']}",
        ]
        c.setFont("Helvetica", 5.2)
        for index, value in enumerate(values):
            c.drawCentredString((x_positions[index] + x_positions[index + 1]) / 2,
                                y_bottom + 3.0 * mm, str(value)[:22])
    for x in x_positions:
        c.line(x, table_top, x, table_top - (len(rows) + 1) * row_h)
    c.setFillColor(HexColor("#C00000"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(margin + 3 * mm, margin + 7 * mm,
                 "Coordenadas = centroides de Connectivity - Frame. Sin Joint Coordinates/planta: ubicación no construible.")
    c.setFillColor(black)
    c.drawRightString(width - margin - 3 * mm, margin + 7 * mm, f"Lámina {page_number}/{total_pages}")


def make_pdf(path, details):
    rows_per_page = 24
    page_counts = [1 + math.ceil(len(detail["schedule"]) / rows_per_page) for detail in details]
    total_pages = sum(page_counts)
    page_number = 1
    c = canvas.Canvas(str(path), pagesize=landscape(A3))
    for detail in details:
        draw_pdf_page(c, detail, page_number, total_pages)
        c.showPage()
        page_number += 1
        schedule_total = math.ceil(len(detail["schedule"]) / rows_per_page)
        for schedule_index in range(schedule_total):
            start = schedule_index * rows_per_page
            rows = detail["schedule"][start:start + rows_per_page]
            draw_schedule_page(c, detail, rows, page_number, total_pages, schedule_index + 1, schedule_total)
            c.showPage()
            page_number += 1
    c.save()


def dxf_text(msp, text, point, height=80, layer="TEXTO"):
    entity = msp.add_text(text, dxfattribs={"height": height, "layer": layer})
    entity.set_placement(point, align=TextEntityAlignment.LEFT)
    return entity


def make_dxf(path, d):
    doc = ezdxf.new("R2018", setup=True)
    for name, color in (("CONTORNO", 7), ("ACERO_SUP", 5), ("ACERO_INF", 1), ("ACERO_TOR", 30), ("ESTRIBOS", 8),
                        ("COTAS", 3), ("TEXTO", 7), ("EJES", 9), ("ALERTA", 1)):
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    msp = doc.modelspace()
    L = d["Lmax"]
    b, h = d["b"], d["h"]
    support = 500
    msp.add_lwpolyline([(0, 0), (L, 0), (L, h), (0, h)], close=True, dxfattribs={"layer": "CONTORNO"})
    msp.add_lwpolyline([(-support, -200), (0, -200), (0, h+200), (-support, h+200)], close=True, dxfattribs={"layer": "CONTORNO"})
    msp.add_lwpolyline([(L, -200), (L+support, -200), (L+support, h+200), (L, h+200)], close=True, dxfattribs={"layer": "CONTORNO"})
    # Acero longitudinal.
    for i in range(d["n_inf"]):
        y = 55 + (i // 7) * 45
        msp.add_line((40, y), (L-40, y), dxfattribs={"layer": "ACERO_INF"})
    for i in range(2):
        msp.add_line((40, h-55-i*35), (L-40, h-55-i*35), dxfattribs={"layer": "ACERO_SUP"})
    extra = max(d["n_sup"] - 2, 0)
    ext = max(L/3, 2*h)
    for i in range(extra):
        y = h-125-i*28
        msp.add_line((40, y), (min(ext, L/2), y), dxfattribs={"layer": "ACERO_SUP"})
        msp.add_line((max(L-ext, L/2), y), (L-40, y), dxfattribs={"layer": "ACERO_SUP"})
    for i in range(d["n_lat"]):
        y = 130 + i * max(25, (h - 260) / max(d["n_lat"] - 1, 1))
        msp.add_line((40, y), (L-40, y), dxfattribs={"layer": "ACERO_TOR"})
    # Estribos.
    zone = min(d["zone"], L/2)
    x = 50
    while x < L-20:
        msp.add_line((x, 40), (x, h-40), dxfattribs={"layer": "ESTRIBOS"})
        x += d["s_end"] if x < zone or x > L-zone else d["s_center"]
    msp.add_aligned_dim(p1=(0, -300), p2=(L, -300), distance=-180, override={"dimtxt": 100}, dxfattribs={"layer": "COTAS"}).render()
    dxf_text(msp, f"DESPIECE VIGA {d['group']}", (0, h+500), 150)
    dxf_text(msp, f"SECCION {int(b)}x{int(h)} mm | L={d['Lmin']:.0f}-{d['Lmax']:.0f} mm", (0, h+300), 90)
    dxf_text(msp, f"SUPERIOR: 2#5 CONTINUAS + {extra}#5 ADICIONALES EN CADA APOYO", (0, h+150), 80, "ACERO_SUP")
    dxf_text(msp, f"INFERIOR: {d['n_inf']}#5 CONTINUAS", (0, -650), 80, "ACERO_INF")
    dxf_text(msp, f"TORSION: {d['n_lat']}#5 DEDICADAS CONTINUAS Y PERIMETRALES", (0, -780), 80, "ACERO_TOR")
    dxf_text(msp, f"ESTRIBOS {d['st_label']} {d['legs']} RAMAS: PRIMERO <=50; @ {int(d['s_end'])} EN 2h; CENTRO @ {int(d['s_center'])}", (0, -910), 80)
    # Tres secciones.
    sy = -2100
    for index, label in enumerate(("A-A APOYO I", "B-B CENTRO", "C-C APOYO J")):
        ox = index * (b + 700)
        msp.add_lwpolyline([(ox, sy), (ox+b, sy), (ox+b, sy+h), (ox, sy+h)], close=True, dxfattribs={"layer": "CONTORNO"})
        msp.add_lwpolyline([(ox+40, sy+40), (ox+b-40, sy+40), (ox+b-40, sy+h-40), (ox+40, sy+h-40)], close=True, dxfattribs={"layer": "ESTRIBOS"})
        if d["legs"] == 4:
            msp.add_line((ox + b / 3, sy + 40), (ox + b / 3, sy + h - 40), dxfattribs={"layer": "ESTRIBOS"})
            msp.add_line((ox + 2 * b / 3, sy + 40), (ox + 2 * b / 3, sy + h - 40), dxfattribs={"layer": "ESTRIBOS"})
        top_n = d["n_sup"] if index != 1 else 2
        bot_n = max(2, math.ceil(d["n_sup"]/3)) if index != 1 else d["n_inf"]
        for xbar, layer in bar_positions(top_n, b, 60, 7):
            msp.add_circle((ox+xbar, sy+h-60-layer*45), d["bar_db"]/2, dxfattribs={"layer": "ACERO_SUP"})
        for xbar, layer in bar_positions(bot_n, b, 60, 7):
            msp.add_circle((ox+xbar, sy+60+layer*45), d["bar_db"]/2, dxfattribs={"layer": "ACERO_INF"})
        for xbar, ybar in perimeter_bar_positions(d["n_lat"], b, h, 60):
            msp.add_circle((ox+xbar, sy+ybar), d["bar_db"]/2, dxfattribs={"layer": "ACERO_TOR"})
        dxf_text(msp, label, (ox, sy+h+130), 75)
    dxf_text(msp, "NO EMITIR PARA CONSTRUCCION - DETALLE ACADEMICO", (0, -3000), 120, "ALERTA")
    if d["failures"]:
        dxf_text(msp, f"NO CUMPLEN {len(d['failures'])} FRAMES: " + ", ".join(d["failures"]), (0, -3160), 80, "ALERTA")
    dxf_text(msp, "SIN JOINT COORDINATES/PLANTA; COORDENADAS DEL CUADRO SON CENTROIDES", (0, -3300), 75, "ALERTA")
    dxf_text(msp, "FRAME | VAR | JOINT I-J | L mm | Xc,Yc,Z | SUP/INF/TOR | ESTRIBO ext/ctr | ESTADO", (0, -3500), 75)
    schedule_y = -3650
    for item in d["schedule"]:
        line = (f"{item['frame']} | {item['variant']} | {item['joint_i']}-{item['joint_j']} | {item['length']} | "
                f"{item['x']:.2f},{item['y']:.2f},{item['z']:.2f} | {item['n_sup']}/{item['n_inf']}/{item['n_tor']} | "
                f"{item['stirrup']} {item['legs']}R {int(item['s_end'])}/{int(item['s_center'])} | {item['status']} {item['reason']}")
        dxf_text(msp, line, (0, schedule_y), 60, "ALERTA" if item["status"] != "CUMPLE" else "TEXTO")
        schedule_y -= 110
    doc.saveas(path)


def main():
    design = load_design()
    records, _ = design.extract_inputs()
    results = [design.design_record(record) for record in records]
    details = [group_detail(design, group, records, results) for group in design.GROUP_ORDER]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    make_pdf(COMBINED_PDF, details)
    for detail in details:
        stem = f"DESPIECE-{safe_name(detail['group'])}"
        make_pdf(OUTPUT_DIR / f"{stem}.pdf", [detail])
        make_dxf(OUTPUT_DIR / f"{stem}.dxf", detail)
    print(f"OK: {COMBINED_PDF}")
    print(f"Planos por grupo: {len(details)} PDF + {len(details)} DXF")
    print(f"Grupos con incumplimientos seccionales: {[d['group'] for d in details if not d['design_ok']]}")
    print("Condición de emisión: 12/12 NO EMITIR PARA CONSTRUCCIÓN")


if __name__ == "__main__":
    main()

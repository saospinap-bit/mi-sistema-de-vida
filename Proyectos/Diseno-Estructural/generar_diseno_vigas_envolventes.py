#!/usr/bin/env python3
"""Genera el diseño final de las 592 vigas usando ENVFLEX y ENVCORT.

ENVFLEX aporta Mu-, Mu+, Vu reducido y Tu. ENVCORT aporta el límite elástico
para cortante. Para el sistema DMO se adopta:
    Vcap = Vu_ENVFLEX + (Mpr- + Mpr+) / Ln
    Vu_diseno = min(Vu_ENVCORT, max(Vu_ENVFLEX, Vcap))
El término Vu_ENVFLEX se conserva en Vcap como aproximación conservadora de la
contribución gravitacional, pues el archivo suministrado contiene envolventes y
no casos de gravedad separados.
"""
from __future__ import annotations

import hashlib
import math
import shutil
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

from lxml import etree
from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE = Path(__file__).resolve().parent
FLEX_FILE = BASE / "ENV FLEXION.xlsx"
SHEAR_FILE = BASE / "ENV CORTANTE.xlsx"
COMBINED_FILE = BASE / "cortante y flexion.xlsx"
OUTPUT_FILE = BASE / "DISENO-VIGAS-FINAL-ENVOLVENTES.xlsx"

# Materiales y detallado
FC = 28.0
FY = 420.0
FYT = 420.0
PHI_M = 0.90
PHI_V = 0.75
COVER = 40.0
DB_LONG = 15.9
AB_LONG = 199.0
DB_ST = 9.5
AB_ST = 71.0
CLEAR_BAR = 25.0
SYSTEM = "DMO"

# Secciones del modelo y secciones adoptadas. VR3 debe actualizarse en SAP.
SECTION_MODEL = {
    "VC": (300.0, 400.0),
    "VR": (350.0, 400.0),
}
SECTION_ADOPTED = {
    "VC": (300.0, 400.0),
    "VR": (350.0, 400.0),
    "VR3": (400.0, 550.0),
}

COLORS = {
    "VR1": "DDEBF7", "VR N1": "BDD7EE", "VR2": "9DC3E6", "VR3": "5B9BD5",
    "VRAUX": "A9D18E", "VC1": "F4B183", "VC2": "FFD966", "VC3": "FFF2CC",
    "VC4": "E2F0D9", "VC5": "C6E0B4", "VC6": "A5A5A5", "VC7": "D9EAD3",
}

NAVY = "17365D"
BLUE = "D9EAF7"
GREEN = "C6E0B4"
RED = "F4CCCC"
YELLOW = "FFF2CC"
ORANGE = "FCE4D6"
GRAY = "E7E6E6"
WHITE = "FFFFFF"
THIN = Side(style="thin", color="B7B7B7")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)


def iter_table(path: Path, sheet: str):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = ws.iter_rows(values_only=True)
    next(rows)
    headers = list(next(rows))
    next(rows)
    for values in rows:
        if values and values[0] is not None:
            yield dict(zip(headers, values))


def normalize_group(name: str) -> str:
    return "VRAUX" if name == "VR AUX" else name


def extract_inputs():
    # Los grupos son los definidos por el equipo en ENV FLEXION.xlsx.
    frame_group: dict[str, str] = {}
    group_frames: dict[str, set[str]] = {}
    wb = load_workbook(FLEX_FILE, read_only=True)
    for sheet in wb.sheetnames:
        group = normalize_group(sheet)
        frames = {str(r["Frame"]) for r in iter_table(FLEX_FILE, sheet)}
        group_frames[group] = frames
        for frame in frames:
            if frame in frame_group:
                raise ValueError(f"Frame {frame} repetido en {frame_group[frame]} y {group}")
            frame_group[frame] = group

    raw = defaultdict(lambda: defaultdict(list))
    for row in iter_table(COMBINED_FILE, "Element Forces - Frames"):
        raw[str(row["Frame"])][str(row["OutputCase"])].append(row)

    if len(raw) != 892:
        raise ValueError(f"Se esperaban 892 frames y se encontraron {len(raw)}")
    if len(frame_group) != 592:
        raise ValueError(f"Se esperaban 592 vigas agrupadas y se encontraron {len(frame_group)}")

    records = []
    for frame, group in frame_group.items():
        flex = raw[frame].get("ENVFLEX", [])
        shear = raw[frame].get("ENVCORT", [])
        if not flex or not shear:
            raise ValueError(f"El frame {frame} no tiene ambas envolventes")

        def vals(rows, key):
            return [float(r[key] or 0.0) for r in rows]

        stations = vals(flex + shear, "Station")
        m3 = vals(flex, "M3")
        v2_flex = vals(flex, "V2")
        v2_shear = vals(shear, "V2")
        torsion = vals(flex, "T")
        records.append({
            "frame": frame,
            "group": group,
            "L": max(stations),
            "Mu_neg": max(0.0, -min(m3)),
            "Mu_pos": max(0.0, max(m3)),
            "Vu_flex": max(abs(x) for x in v2_flex),
            "Vu_elastic": max(abs(x) for x in v2_shear),
            "Tu": max(abs(x) for x in torsion),
        })

    # Verificación exacta de libros separados contra el libro combinado.
    mismatches = []
    for path, case in ((FLEX_FILE, "ENVFLEX"), (SHEAR_FILE, "ENVCORT")):
        wb = load_workbook(path, read_only=True)
        for sheet in wb.sheetnames:
            by_frame = defaultdict(list)
            for row in iter_table(path, sheet):
                by_frame[str(row["Frame"])].append(row)
            for frame, separate_rows in by_frame.items():
                combined_rows = raw[frame][case]
                for key in ("M3", "V2", "T"):
                    a = max(abs(float(r[key] or 0.0)) for r in separate_rows)
                    b = max(abs(float(r[key] or 0.0)) for r in combined_rows)
                    if abs(a - b) > 1e-6:
                        mismatches.append((path.name, sheet, frame, key, a, b))
    if mismatches:
        raise ValueError(f"Hay {len(mismatches)} discrepancias entre archivos: {mismatches[:3]}")

    # Los otros 300 frames deben ser columnas (P != 0 y longitudes de entrepiso).
    other = set(raw) - set(frame_group)
    if len(other) != 300:
        raise ValueError(f"Se esperaban 300 elementos no-viga y se encontraron {len(other)}")
    return records, group_frames


def base_section(group: str):
    family = "VC" if group.startswith("VC") else "VR"
    b0, h0 = SECTION_MODEL[family]
    b, h = SECTION_ADOPTED.get(group, SECTION_ADOPTED[family])
    return b0, h0, b, h


def beta1():
    return 0.85 if FC <= 28 else max(0.65, 0.85 - 0.05 * (FC - 28) / 7)


def nominal_as_required(mu: float, b: float, d: float):
    as_min = max(1.4 / FY, 0.25 * math.sqrt(FC) / FY) * b * d
    rn = mu * 1e6 / (PHI_M * b * d * d) if mu > 0 else 0.0
    disc = 1 - 2 * rn / (0.85 * FC)
    if disc <= 0:
        return math.inf, as_min
    rho = (0.85 * FC / FY) * (1 - math.sqrt(disc))
    return max(rho * b * d, as_min), as_min


def bar_layout(n: int, b: float, h: float):
    available = b - 2 * COVER - 2 * DB_ST
    per_layer = max(2, math.floor((available + CLEAR_BAR) / (DB_LONG + CLEAR_BAR)))
    if n <= per_layer:
        layers, n1, n2 = 1, n, 0
    elif n <= 2 * per_layer:
        layers, n1, n2 = 2, math.ceil(n / 2), math.floor(n / 2)
    else:
        return {"fits": False, "layers": 3, "d": 0.0, "per_layer": per_layer}
    y1 = COVER + DB_ST + DB_LONG / 2
    y2 = y1 + DB_LONG + CLEAR_BAR
    centroid = y1 if layers == 1 else (n1 * y1 + n2 * y2) / n
    return {"fits": True, "layers": layers, "d": h - centroid, "per_layer": per_layer}


def flexural_design(mu: float, b: float, h: float, minimum_n: int = 2):
    d_nom = h - COVER - DB_ST - DB_LONG / 2
    as_req_nom, _ = nominal_as_required(mu, b, d_nom)
    n = max(minimum_n, math.ceil(as_req_nom / AB_LONG))
    for _ in range(30):
        layout = bar_layout(n, b, h)
        if not layout["fits"]:
            return {"ok": False, "n": n, "layers": layout["layers"], "d": 0.0,
                    "as_req": math.inf, "as_min": math.inf, "as_prov": n * AB_LONG,
                    "phi_mn": 0.0, "mpr": 0.0}
        d = layout["d"]
        as_req, as_min = nominal_as_required(mu, b, d)
        as_prov = n * AB_LONG
        a = as_prov * FY / (0.85 * FC * b)
        phi_mn = PHI_M * as_prov * FY * (d - a / 2) / 1e6
        rho = as_prov / (b * d)
        rho_max = 0.85 * beta1() * FC / FY * 3 / 8
        if as_prov + 1e-9 >= as_req and phi_mn + 1e-9 >= mu and rho <= rho_max:
            a_pr = as_prov * 1.25 * FY / (0.85 * FC * b)
            mpr = as_prov * 1.25 * FY * (d - a_pr / 2) / 1e6
            return {"ok": True, "n": n, "layers": layout["layers"], "d": d,
                    "as_req": as_req, "as_min": as_min, "as_prov": as_prov,
                    "phi_mn": phi_mn, "mpr": mpr, "rho": rho,
                    "per_layer": layout["per_layer"]}
        n += 1
    raise RuntimeError("No convergió el diseño a flexión")


def floor10(value: float):
    return max(10.0, math.floor(value / 10.0) * 10.0)


def design_record(record: dict, group_mode: bool = False):
    group = record["group"]
    b0, h0, b, h = base_section(group)

    neg = flexural_design(record["Mu_neg"], b, h, 2)
    if not neg["ok"]:
        raise ValueError(f"No cabe el acero superior de {group}/{record.get('frame','grupo')}")
    # Requisito de continuidad DMO: al menos 2 barras y no menos de 1/3 del acero superior.
    min_pos = max(2, math.ceil(neg["n"] / 3))
    pos = flexural_design(record["Mu_pos"], b, h, min_pos)
    if not pos["ok"]:
        raise ValueError(f"No cabe el acero inferior de {group}/{record.get('frame','grupo')}")

    d = min(neg["d"], pos["d"])
    length = record["L_min"] if group_mode else record["L"]
    vcap = record["Vu_flex"] + (neg["mpr"] + pos["mpr"]) / length
    vdesign = min(record["Vu_elastic"], max(record["Vu_flex"], vcap))
    vc = 0.17 * math.sqrt(FC) * b * d / 1000
    vs_req = max(vdesign / PHI_V - vc, 0.0)
    vs_max = 0.66 * math.sqrt(FC) * b * d / 1000
    shear_section_ok = vs_req <= vs_max + 1e-9

    acp = b * h
    pcp = 2 * (b + h)
    phi_tth = PHI_V * 0.083 * math.sqrt(FC) * acp * acp / pcp / 1e6
    aoh = (b - 2 * COVER) * (h - 2 * COVER)
    ao = 0.85 * aoh
    ph = 2 * ((b - 2 * COVER) + (h - 2 * COVER))
    at_s = 0.0 if record["Tu"] <= phi_tth else record["Tu"] * 1e6 / (PHI_V * 2 * ao * FYT)
    al = at_s * ph * FYT / FY
    n_torsion = math.ceil(al / AB_LONG) if at_s > 0 else 0

    selected = None
    for legs in (2, 4):
        av = legs * AB_ST
        s_shear = math.inf if vs_req <= 1e-12 else av * FYT * d / (vs_req * 1000)
        s_torsion = math.inf if at_s <= 1e-12 else AB_ST / at_s
        s_end = floor10(min(s_shear, s_torsion, d / 4, 8 * DB_LONG, 24 * DB_ST, 300))
        s_center = floor10(min(s_shear, s_torsion, d / 2, 600))
        if s_end >= 80:
            selected = (legs, s_end, s_center)
            break
    if selected is None:
        legs = 4
        av = legs * AB_ST
        s_shear = av * FYT * d / (max(vs_req, 1e-12) * 1000)
        s_torsion = AB_ST / max(at_s, 1e-12) if at_s > 0 else math.inf
        selected = (legs, floor10(min(s_shear, s_torsion, d / 4)), floor10(min(s_shear, s_torsion, d / 2)))
    legs, s_end, s_center = selected
    av = legs * AB_ST
    phi_vn = PHI_V * (vc + av * FYT * d / s_end / 1000)
    shear_ok = shear_section_ok and phi_vn + 1e-9 >= vdesign
    torsion_ok = at_s <= 1e-12 or AB_ST / s_end + 1e-12 >= at_s
    section_changed = (b0 != b or h0 != h)
    overall = neg["ok"] and pos["ok"] and shear_ok and torsion_ok

    return {**record, "b0": b0, "h0": h0, "b": b, "h": h,
            "neg": neg, "pos": pos, "d": d, "Vcap": vcap, "Vdesign": vdesign,
            "Vc": vc, "Vs_req": vs_req, "Vs_max": vs_max,
            "shear_section_ok": shear_section_ok, "legs": legs,
            "s_end": s_end, "s_center": s_center, "phi_vn": phi_vn,
            "shear_ok": shear_ok, "phi_tth": phi_tth, "at_s": at_s,
            "Al": al, "n_torsion": n_torsion, "torsion_ok": torsion_ok,
            "section_changed": section_changed, "overall": overall}


def build_group_records(records):
    by_group = defaultdict(list)
    for record in records:
        by_group[record["group"]].append(record)
    output = []
    for group, items in by_group.items():
        crit_neg = max(items, key=lambda x: x["Mu_neg"])
        crit_pos = max(items, key=lambda x: x["Mu_pos"])
        crit_v = max(items, key=lambda x: x["Vu_elastic"])
        crit_t = max(items, key=lambda x: x["Tu"])
        rec = {
            "group": group, "frame": "—", "count": len(items),
            "L_min": min(x["L"] for x in items), "L_max": max(x["L"] for x in items),
            "Mu_neg": crit_neg["Mu_neg"], "frame_Mu_neg": crit_neg["frame"],
            "Mu_pos": crit_pos["Mu_pos"], "frame_Mu_pos": crit_pos["frame"],
            "Vu_flex": max(x["Vu_flex"] for x in items),
            "Vu_elastic": crit_v["Vu_elastic"], "frame_Vu": crit_v["frame"],
            "Tu": crit_t["Tu"], "frame_Tu": crit_t["frame"],
        }
        output.append(design_record(rec, group_mode=True))
    order = ["VC1", "VC2", "VC3", "VC4", "VC5", "VC6", "VC7",
             "VR1", "VR N1", "VR2", "VR3", "VRAUX"]
    return sorted(output, key=lambda x: order.index(x["group"]))


def sort_frame(frame: str):
    try:
        return (0, int(frame))
    except ValueError:
        return (1, frame)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


HEADERS = [
    "Grupo", "Frame", "N vigas", "L mín (m)", "L máx (m)",
    "b modelo (mm)", "h modelo (mm)", "b adopt. (mm)", "h adopt. (mm)",
    "Mu− ENVFLEX (kN·m)", "Frame Mu−", "Mu+ ENVFLEX (kN·m)", "Frame Mu+",
    "Vu ENVFLEX (kN)", "Vu ENVCORT (kN)", "Frame Vu", "Tu ENVFLEX (kN·m)",
    "As req. sup (mm²)", "Nº5 sup", "Capas sup", "d sup (mm)", "As prov. sup (mm²)",
    "φMn− (kN·m)", "Flexión −", "As req. inf (mm²)", "Nº5 inf", "Capas inf",
    "d inf (mm)", "As prov. inf (mm²)", "φMn+ (kN·m)", "Flexión +",
    "Mpr− (kN·m)", "Mpr+ (kN·m)", "Vcap (kN)", "Vu diseño (kN)",
    "Vc (kN)", "Vs req. (kN)", "Vs máx. (kN)", "Sección cortante", "Estribo",
    "Ramas", "s extremo DMO (mm)", "s centro (mm)", "φVn (kN)", "Cortante",
    "φTth (kN·m)", "Torsión", "At/s (mm²/mm)", "Al (mm²)", "Nº5 torsión", "Chequeo torsión", "ESTADO"
]


def add_formula(ws, coord: str, formula: str, cached, cache):
    ws[coord] = formula
    cache[(ws.title, coord)] = cached


def write_design_sheet(wb, name: str, rows, grouped: bool, cache):
    ws = wb.create_sheet(name)
    last_col = get_column_letter(len(HEADERS))
    ws.merge_cells(f"A1:{last_col}1")
    ws["A1"] = f"DISEÑO DE VIGAS — {name.upper()}"
    ws["A1"].font = Font(bold=True, size=14, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A1"].alignment = CENTER
    ws.merge_cells(f"A2:{last_col}2")
    ws["A2"] = "ENVFLEX: flexión y torsión. ENVCORT: límite elástico de cortante. Vu diseño DMO = mín(ENVCORT; máx[ENVFLEX; Vcap])."
    ws["A2"].fill = PatternFill("solid", fgColor=BLUE)
    ws["A2"].alignment = LEFT
    for col, header in enumerate(HEADERS, 1):
        cell = ws.cell(3, col, header)
        cell.font = Font(bold=True, color=WHITE, size=9)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = CENTER
        cell.border = BORDER
    ws.row_dimensions[3].height = 64

    for r_idx, result in enumerate(rows, 4):
        group = result["group"]
        color = COLORS[group]
        length_min = result["L_min"] if grouped else result["L"]
        length_max = result["L_max"] if grouped else result["L"]
        frame = "—" if grouped else result["frame"]
        count = result.get("count", 1)
        crit_neg = result.get("frame_Mu_neg", frame)
        crit_pos = result.get("frame_Mu_pos", frame)
        crit_v = result.get("frame_Vu", frame)
        values = [group, frame, count, length_min, length_max, result["b0"], result["h0"],
                  result["b"], result["h"], result["Mu_neg"], crit_neg,
                  result["Mu_pos"], crit_pos, result["Vu_flex"], result["Vu_elastic"],
                  crit_v, result["Tu"]]
        for c_idx, value in enumerate(values, 1):
            ws.cell(r_idx, c_idx, value)

        # Adopted bar counts and detailing choices are explicit design decisions; capacities remain formulas.
        ws.cell(r_idx, 19, result["neg"]["n"])
        ws.cell(r_idx, 20, result["neg"]["layers"])
        ws.cell(r_idx, 26, result["pos"]["n"])
        ws.cell(r_idx, 27, result["pos"]["layers"])
        ws.cell(r_idx, 40, f"Nº3 cerrado")
        ws.cell(r_idx, 41, result["legs"])
        ws.cell(r_idx, 50, result["n_torsion"])

        # Formulas. Las referencias a Parametros mantienen el libro editable.
        p = "'Parametros'!"
        formulas = {
            18: (f"=MAX(MAX(1.4/{p}$B$3,0.25*SQRT({p}$B$2)/{p}$B$3)*H{r_idx}*U{r_idx},"
                 f"(0.85*{p}$B$2/{p}$B$3)*(1-SQRT(1-2*(J{r_idx}*1000000/({p}$B$5*H{r_idx}*U{r_idx}^2))/(0.85*{p}$B$2)))*H{r_idx}*U{r_idx})", result["neg"]["as_req"]),
            21: (f"=IF(T{r_idx}=1,I{r_idx}-({p}$B$7+{p}$B$9+{p}$B$12/2),I{r_idx}-(ROUNDUP(S{r_idx}/2,0)*({p}$B$7+{p}$B$9+{p}$B$12/2)+ROUNDDOWN(S{r_idx}/2,0)*({p}$B$7+{p}$B$9+{p}$B$12/2+{p}$B$12+{p}$B$10))/S{r_idx})", result["neg"]["d"]),
            22: (f"=S{r_idx}*{p}$B$8", result["neg"]["as_prov"]),
            23: (f"={p}$B$5*V{r_idx}*{p}$B$3*(U{r_idx}-(V{r_idx}*{p}$B$3/(0.85*{p}$B$2*H{r_idx}))/2)/1000000", result["neg"]["phi_mn"]),
            24: (f'=IF(W{r_idx}>=J{r_idx},"CUMPLE","NO CUMPLE")', "CUMPLE" if result["neg"]["phi_mn"] >= result["Mu_neg"] else "NO CUMPLE"),
            25: (f"=MAX(MAX(1.4/{p}$B$3,0.25*SQRT({p}$B$2)/{p}$B$3)*H{r_idx}*AB{r_idx},"
                 f"(0.85*{p}$B$2/{p}$B$3)*(1-SQRT(1-2*(L{r_idx}*1000000/({p}$B$5*H{r_idx}*AB{r_idx}^2))/(0.85*{p}$B$2)))*H{r_idx}*AB{r_idx})", result["pos"]["as_req"]),
            28: (f"=IF(AA{r_idx}=1,I{r_idx}-({p}$B$7+{p}$B$9+{p}$B$12/2),I{r_idx}-(ROUNDUP(Z{r_idx}/2,0)*({p}$B$7+{p}$B$9+{p}$B$12/2)+ROUNDDOWN(Z{r_idx}/2,0)*({p}$B$7+{p}$B$9+{p}$B$12/2+{p}$B$12+{p}$B$10))/Z{r_idx})", result["pos"]["d"]),
            29: (f"=Z{r_idx}*{p}$B$8", result["pos"]["as_prov"]),
            30: (f"={p}$B$5*AC{r_idx}*{p}$B$3*(AB{r_idx}-(AC{r_idx}*{p}$B$3/(0.85*{p}$B$2*H{r_idx}))/2)/1000000", result["pos"]["phi_mn"]),
            31: (f'=IF(AD{r_idx}>=L{r_idx},"CUMPLE","NO CUMPLE")', "CUMPLE" if result["pos"]["phi_mn"] >= result["Mu_pos"] else "NO CUMPLE"),
            32: (f"=V{r_idx}*1.25*{p}$B$3*(U{r_idx}-(V{r_idx}*1.25*{p}$B$3/(0.85*{p}$B$2*H{r_idx}))/2)/1000000", result["neg"]["mpr"]),
            33: (f"=AC{r_idx}*1.25*{p}$B$3*(AB{r_idx}-(AC{r_idx}*1.25*{p}$B$3/(0.85*{p}$B$2*H{r_idx}))/2)/1000000", result["pos"]["mpr"]),
            34: (f"=N{r_idx}+(AF{r_idx}+AG{r_idx})/D{r_idx}", result["Vcap"]),
            35: (f"=MIN(O{r_idx},MAX(N{r_idx},AH{r_idx}))", result["Vdesign"]),
            36: (f"=0.17*SQRT({p}$B$2)*H{r_idx}*MIN(U{r_idx},AB{r_idx})/1000", result["Vc"]),
            37: (f"=MAX(AI{r_idx}/{p}$B$6-AJ{r_idx},0)", result["Vs_req"]),
            38: (f"=0.66*SQRT({p}$B$2)*H{r_idx}*MIN(U{r_idx},AB{r_idx})/1000", result["Vs_max"]),
            39: (f'=IF(AK{r_idx}<=AL{r_idx},"CUMPLE","NO CUMPLE")', "CUMPLE" if result["shear_section_ok"] else "NO CUMPLE"),
            42: (f"=ROUNDDOWN(MIN(IF(AK{r_idx}=0,1000000000,AO{r_idx}*{p}$B$11*{p}$B$4*MIN(U{r_idx},AB{r_idx})/(AK{r_idx}*1000)),IF(AV{r_idx}=0,1000000000,{p}$B$11/AV{r_idx}),MIN(U{r_idx},AB{r_idx})/4,8*{p}$B$12,24*{p}$B$9,300)/10,0)*10", result["s_end"]),
            43: (f"=ROUNDDOWN(MIN(IF(AK{r_idx}=0,1000000000,AO{r_idx}*{p}$B$11*{p}$B$4*MIN(U{r_idx},AB{r_idx})/(AK{r_idx}*1000)),IF(AV{r_idx}=0,1000000000,{p}$B$11/AV{r_idx}),MIN(U{r_idx},AB{r_idx})/2,600)/10,0)*10", result["s_center"]),
            44: (f"={p}$B$6*(AJ{r_idx}+AO{r_idx}*{p}$B$11*{p}$B$4*MIN(U{r_idx},AB{r_idx})/AP{r_idx}/1000)", result["phi_vn"]),
            45: (f'=IF(AND(AM{r_idx}="CUMPLE",AR{r_idx}>=AI{r_idx}),"CUMPLE","NO CUMPLE")', "CUMPLE" if result["shear_ok"] else "NO CUMPLE"),
            46: (f"={p}$B$6*0.083*SQRT({p}$B$2)*(H{r_idx}*I{r_idx})^2/(2*(H{r_idx}+I{r_idx}))/1000000", result["phi_tth"]),
            47: (f'=IF(Q{r_idx}<=AT{r_idx},"DESPRECIABLE","DISEÑAR")', "DESPRECIABLE" if result["at_s"] == 0 else "DISEÑAR"),
            48: (f"=IF(Q{r_idx}<=AT{r_idx},0,Q{r_idx}*1000000/({p}$B$6*2*0.85*(H{r_idx}-2*{p}$B$7)*(I{r_idx}-2*{p}$B$7)*{p}$B$4))", result["at_s"]),
            49: (f"=AV{r_idx}*2*((H{r_idx}-2*{p}$B$7)+(I{r_idx}-2*{p}$B$7))*{p}$B$4/{p}$B$3", result["Al"]),
            51: (f'=IF(AV{r_idx}=0,"DESPRECIABLE",IF({p}$B$11/AP{r_idx}>=AV{r_idx},"CUMPLE","NO CUMPLE"))', "DESPRECIABLE" if result["at_s"] == 0 else ("CUMPLE" if result["torsion_ok"] else "NO CUMPLE")),
            52: (f'=IF(AND(X{r_idx}="CUMPLE",AE{r_idx}="CUMPLE",AS{r_idx}="CUMPLE",OR(AY{r_idx}="CUMPLE",AY{r_idx}="DESPRECIABLE")),IF(OR(F{r_idx}<>H{r_idx},G{r_idx}<>I{r_idx}),"CUMPLE - REANALIZAR SAP","CUMPLE"),"NO CUMPLE")',
                 "CUMPLE - REANALIZAR SAP" if result["overall"] and result["section_changed"] else ("CUMPLE" if result["overall"] else "NO CUMPLE")),
        }
        for col_idx, (formula, cached) in formulas.items():
            add_formula(ws, f"{get_column_letter(col_idx)}{r_idx}", formula, cached, cache)

        for c_idx in range(1, len(HEADERS) + 1):
            cell = ws.cell(r_idx, c_idx)
            cell.border = BORDER
            cell.alignment = CENTER
            if c_idx in (1, 2, 10, 12, 14, 15, 17):
                cell.fill = PatternFill("solid", fgColor=color if c_idx <= 2 else BLUE)
            if c_idx in (8, 9, 19, 26, 40, 41, 50):
                cell.fill = PatternFill("solid", fgColor=YELLOW)
            if c_idx >= 10 and isinstance(cell.value, (int, float)):
                cell.number_format = "0.00"
        if result["section_changed"]:
            ws.cell(r_idx, 8).fill = PatternFill("solid", fgColor=ORANGE)
            ws.cell(r_idx, 9).fill = PatternFill("solid", fgColor=ORANGE)

    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:{last_col}{3 + len(rows)}"
    ws.sheet_view.showGridLines = False
    widths = {1: 12, 2: 12, 3: 10, 4: 11, 5: 11, 6: 12, 7: 12, 8: 12, 9: 12}
    for col in range(1, len(HEADERS) + 1):
        ws.column_dimensions[get_column_letter(col)].width = widths.get(col, 14)
    ws.conditional_formatting.add(f"X4:X{3+len(rows)}", CellIsRule(operator="equal", formula=['"CUMPLE"'], fill=PatternFill("solid", fgColor=GREEN)))
    ws.conditional_formatting.add(f"AE4:AE{3+len(rows)}", CellIsRule(operator="equal", formula=['"CUMPLE"'], fill=PatternFill("solid", fgColor=GREEN)))
    ws.conditional_formatting.add(f"AS4:AS{3+len(rows)}", CellIsRule(operator="equal", formula=['"CUMPLE"'], fill=PatternFill("solid", fgColor=GREEN)))
    ws.conditional_formatting.add(f"AZ4:AZ{3+len(rows)}", CellIsRule(operator="equal", formula=['"NO CUMPLE"'], fill=PatternFill("solid", fgColor=RED)))
    return ws


def write_parameters(wb):
    ws = wb.create_sheet("Parametros")
    ws["A1"] = "PARÁMETROS GENERALES"
    ws["A1"].font = Font(bold=True, size=14, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws.merge_cells("A1:D1")
    data = [
        ("f'c", FC, "MPa", "Concreto del proyecto"),
        ("fy", FY, "MPa", "Acero longitudinal"),
        ("fyt", FYT, "MPa", "Acero transversal"),
        ("φ flexión", PHI_M, "—", "Secciones controladas por tracción"),
        ("φ cortante/torsión", PHI_V, "—", "NSR-10 Título C"),
        ("Recubrimiento", COVER, "mm", "Vigas interiores"),
        ("Área barra longitudinal", AB_LONG, "mm²", "Nº5"),
        ("db estribo", DB_ST, "mm", "Nº3"),
        ("Separación libre vertical", CLEAR_BAR, "mm", "Entre capas"),
        ("Área rama estribo", AB_ST, "mm²", "Nº3"),
        ("db longitudinal", DB_LONG, "mm", "Barra Nº5"),
    ]
    for r, row in enumerate(data, 2):
        for c, value in enumerate(row, 1):
            ws.cell(r, c, value)
            ws.cell(r, c).border = BORDER
            ws.cell(r, c).alignment = CENTER if c != 4 else LEFT
            if c == 1:
                ws.cell(r, c).font = Font(bold=True)
                ws.cell(r, c).fill = PatternFill("solid", fgColor=BLUE)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 48
    ws.sheet_view.showGridLines = False


def write_cover(wb, group_results, all_results):
    ws = wb.active
    ws.title = "Portada y criterio"
    ws.merge_cells("A1:H1")
    ws["A1"] = "DISEÑO FINAL DE VIGAS — ENVOLVENTES DE FLEXIÓN Y CORTANTE"
    ws["A1"].font = Font(bold=True, size=16, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A1"].alignment = CENTER
    lines = [
        (3, "Alcance", "592 vigas: 12 grupos suministrados por el equipo y diseño individual de cada frame. No incluye viguetas."),
        (4, "Fuente flexión", "ENVFLEX: M3 mínimo → Mu−; M3 máximo → Mu+; T → torsión de diseño."),
        (5, "Fuente cortante", "ENVFLEX aporta el cortante de combinaciones de diseño; ENVCORT aporta el cortante elástico no reducido."),
        (6, "Criterio DMO", "Vcap = Vu_ENVFLEX + (Mpr− + Mpr+)/Ln; Vu diseño = mín(Vu_ENVCORT; máx[Vu_ENVFLEX; Vcap])."),
        (7, "Agrupación", "Se respetan los grupos ya definidos en ENV FLEXION/ENV CORTANTE. Cada grupo usa máximos independientes y la menor longitud, de forma conservadora."),
        (8, "Secciones base", "VC: 0.30×0.40 m; VR: 0.35×0.40 m."),
        (9, "Cambio requerido", "VR3 se adopta 0.40×0.55 m. Debe actualizarse en SAP y reanalizarse antes de emitir planos finales."),
        (10, "Trazabilidad", "Las hojas muestran simultáneamente Mu, Vu de ambas envolventes, frames críticos, Mpr, Vcap y Vu final."),
    ]
    for row, title, text in lines:
        ws.cell(row, 1, title).font = Font(bold=True)
        ws.cell(row, 1).fill = PatternFill("solid", fgColor=BLUE)
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=8)
        ws.cell(row, 2, text).alignment = LEFT
        for col in range(1, 9):
            ws.cell(row, col).border = BORDER
    ws["A12"] = "RESULTADOS DE CONTROL"
    ws["A12"].font = Font(bold=True, color=WHITE)
    ws["A12"].fill = PatternFill("solid", fgColor=NAVY)
    ws.merge_cells("A12:H12")
    summary = [
        ("Frames totales SAP", 892), ("Vigas diseñadas", len(all_results)),
        ("Columnas excluidas", 300), ("Grupos", len(group_results)),
        ("Grupos que cumplen", sum(x["overall"] for x in group_results)),
        ("Vigas que cumplen", sum(x["overall"] for x in all_results)),
        ("Grupos con cambio de sección", sum(x["section_changed"] for x in group_results)),
        ("Vigas con cambio de sección", sum(x["section_changed"] for x in all_results)),
    ]
    for idx, (label, value) in enumerate(summary, 13):
        ws.cell(idx, 1, label)
        ws.cell(idx, 2, value)
        ws.cell(idx, 2).font = Font(bold=True)
        ws.cell(idx, 2).fill = PatternFill("solid", fgColor=GREEN if "cumplen" in label else YELLOW)
        for col in (1, 2): ws.cell(idx, col).border = BORDER
    ws.column_dimensions["A"].width = 32
    for col in range(2, 9): ws.column_dimensions[get_column_letter(col)].width = 19
    ws.sheet_view.showGridLines = False


def write_audit(wb, group_results, all_results, group_frames):
    ws = wb.create_sheet("Auditoria y fuentes")
    ws.merge_cells("A1:J1")
    ws["A1"] = "AUDITORÍA DE DATOS Y RESULTADOS"
    ws["A1"].font = Font(bold=True, size=14, color=WHITE)
    ws["A1"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A1"].alignment = CENTER
    audit = [
        ("Archivos separados vs combinado", "0 discrepancias en M3, V2 y T"),
        ("Frames en cortante y flexion.xlsx", "892"),
        ("Vigas incluidas en grupos", "592"),
        ("Elementos excluidos (columnas)", "300"),
        ("Grupos con estado NO CUMPLE", str(sum(not x["overall"] for x in group_results))),
        ("Vigas con estado NO CUMPLE", str(sum(not x["overall"] for x in all_results))),
        ("Advertencia", "VR3 cambia de 0.35×0.40 a 0.40×0.55 m: reanalizar SAP."),
    ]
    for r, (a, b) in enumerate(audit, 3):
        ws.cell(r, 1, a); ws.cell(r, 2, b)
        ws.cell(r, 1).font = Font(bold=True)
        ws.cell(r, 1).fill = PatternFill("solid", fgColor=BLUE)
        ws.cell(r, 1).border = ws.cell(r, 2).border = BORDER
        ws.cell(r, 2).alignment = LEFT

    start = 12
    headers = ["Archivo", "SHA-256"]
    for c, h in enumerate(headers, 1):
        ws.cell(start, c, h); ws.cell(start, c).font = Font(bold=True, color=WHITE); ws.cell(start, c).fill = PatternFill("solid", fgColor=NAVY)
    for i, path in enumerate((FLEX_FILE, SHEAR_FILE, COMBINED_FILE), start + 1):
        ws.cell(i, 1, path.name); ws.cell(i, 2, sha256(path))
        ws.cell(i, 1).border = ws.cell(i, 2).border = BORDER

    start = 18
    headers = ["Grupo", "N", "L mín", "L máx", "Frame Mu−", "Frame Mu+", "Frame Vu", "Estado", "Sección adoptada", "Nota"]
    for c, h in enumerate(headers, 1):
        ws.cell(start, c, h); ws.cell(start, c).font = Font(bold=True, color=WHITE); ws.cell(start, c).fill = PatternFill("solid", fgColor=NAVY); ws.cell(start, c).border = BORDER
    for r, result in enumerate(group_results, start + 1):
        values = [result["group"], result["count"], result["L_min"], result["L_max"], result["frame_Mu_neg"], result["frame_Mu_pos"], result["frame_Vu"],
                  "CUMPLE" if result["overall"] else "NO CUMPLE", f"{int(result['b'])}×{int(result['h'])} mm",
                  "Reanalizar SAP" if result["section_changed"] else "Sin cambio"]
        for c, v in enumerate(values, 1):
            ws.cell(r, c, v); ws.cell(r, c).border = BORDER; ws.cell(r, c).alignment = CENTER
            if c == 1: ws.cell(r, c).fill = PatternFill("solid", fgColor=COLORS[result["group"]])
    for col, width in enumerate([18, 10, 12, 12, 14, 14, 14, 16, 20, 26], 1):
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.sheet_view.showGridLines = False


def inject_cached_values(path: Path, cache: dict):
    """Inserta resultados precalculados sin eliminar las fórmulas."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
          "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(path, "r") as zin:
            zin.extractall(tmp_path)
        wb_tree = etree.parse(str(tmp_path / "xl/workbook.xml"))
        rel_tree = etree.parse(str(tmp_path / "xl/_rels/workbook.xml.rels"))
        rel_targets = {r.get("Id"): r.get("Target") for r in rel_tree.xpath("//pr:Relationship", namespaces=ns)}
        sheet_paths = {}
        for sheet in wb_tree.xpath("//m:sheets/m:sheet", namespaces=ns):
            rid = sheet.get(f"{{{ns['r']}}}id")
            target = rel_targets[rid].lstrip("/")
            sheet_paths[sheet.get("name")] = tmp_path / target
        for sheet_name, sheet_path in sheet_paths.items():
            items = {coord: val for (s, coord), val in cache.items() if s == sheet_name}
            if not items:
                continue
            tree = etree.parse(str(sheet_path))
            for cell in tree.xpath("//m:c[m:f]", namespaces=ns):
                coord = cell.get("r")
                if coord not in items:
                    continue
                value = items[coord]
                v_nodes = cell.xpath("m:v", namespaces=ns)
                v = v_nodes[0] if v_nodes else etree.SubElement(cell, f"{{{ns['m']}}}v")
                if isinstance(value, str):
                    cell.set("t", "str")
                    v.text = value
                else:
                    cell.attrib.pop("t", None)
                    v.text = f"{float(value):.15g}"
            tree.write(str(sheet_path), xml_declaration=True, encoding="UTF-8", standalone=True)
        calc = wb_tree.xpath("//m:calcPr", namespaces=ns)
        if calc:
            calc[0].set("calcMode", "auto")
            calc[0].set("fullCalcOnLoad", "1")
            calc[0].set("forceFullCalc", "1")
        wb_tree.write(str(tmp_path / "xl/workbook.xml"), xml_declaration=True, encoding="UTF-8", standalone=True)
        new_path = path.with_suffix(".tmp.xlsx")
        with zipfile.ZipFile(new_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for file in tmp_path.rglob("*"):
                if file.is_file(): zout.write(file, file.relative_to(tmp_path))
        shutil.move(new_path, path)


def main():
    records, group_frames = extract_inputs()
    group_results = build_group_records(records)
    all_results = []
    group_order = ["VC1", "VC2", "VC3", "VC4", "VC5", "VC6", "VC7", "VR1", "VR N1", "VR2", "VR3", "VRAUX"]
    for record in sorted(records, key=lambda x: (group_order.index(x["group"]), sort_frame(x["frame"]))):
        all_results.append(design_record(record))

    cache = {}
    wb = Workbook()
    write_cover(wb, group_results, all_results)
    write_parameters(wb)
    write_design_sheet(wb, "Vigas de Carga (7)", [x for x in group_results if x["group"].startswith("VC")], True, cache)
    write_design_sheet(wb, "Vigas de Rigidez (5)", [x for x in group_results if x["group"].startswith("VR")], True, cache)
    write_design_sheet(wb, "Todas las Vigas (592)", all_results, False, cache)
    write_audit(wb, group_results, all_results, group_frames)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.save(OUTPUT_FILE)
    inject_cached_values(OUTPUT_FILE, cache)

    print(f"OK: {OUTPUT_FILE}")
    print(f"Grupos: {len(group_results)}; vigas: {len(all_results)}")
    print(f"Grupos que cumplen: {sum(x['overall'] for x in group_results)}/{len(group_results)}")
    print(f"Vigas que cumplen: {sum(x['overall'] for x in all_results)}/{len(all_results)}")
    print(f"Celdas con cache: {len(cache)}")


if __name__ == "__main__":
    main()

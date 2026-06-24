# -*- coding: utf-8 -*-
"""
Genera los arboles de PROBLEMAS y OBJETIVOS como esquemas visuales (PNG),
con cajas conectadas por lineas, tipo arbol jerarquico.
Caso: acueducto del municipio de Tado (Choco).
Salida: arbol_problemas.png, arbol_objetivos.png
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def draw_box(ax, cx, cy, w, h, text, facecolor, edgecolor="#333333",
             textcolor="black", fontsize=9, bold=False):
    box = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=1.3, edgecolor=edgecolor, facecolor=facecolor,
                         mutation_aspect=1)
    ax.add_patch(box)
    wrapped = "\n".join(textwrap.wrap(text, width=int(w * 7)))
    ax.text(cx, cy, wrapped, ha="center", va="center",
            fontsize=fontsize, color=textcolor,
            fontweight="bold" if bold else "normal", wrap=True)
    return (cx, cy, w, h)


def connect(ax, top_box, bottom_box, color="#666666"):
    xt, yt, wt, ht = top_box
    xb, yb, wb, hb = bottom_box
    ax.annotate("", xy=(xb, yb + hb / 2), xytext=(xt, yt - ht / 2),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.1,
                                connectionstyle="arc3,rad=0"))


def build_tree(filename, titulo, top_label, tier2_labels, central_label,
               tier4_labels, tier5_labels, palette, lat_top, lat_bottom):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title(titulo, fontsize=15, fontweight="bold", color="#1F4E79", pad=14)

    xs = [2.4, 6.0, 9.6, 13.2]
    w_col = 3.3

    top = draw_box(ax, 7.5, 10.0, 9.0, 1.0, top_label,
                   palette["top"], fontsize=10, bold=True)

    boxes2 = []
    for i, t in enumerate(tier2_labels):
        b = draw_box(ax, xs[i], 7.9, w_col, 1.3, t, palette["tier2"], fontsize=8.3)
        boxes2.append(b)
        connect(ax, top, b)

    central = draw_box(ax, 7.5, 5.6, 9.8, 1.2, central_label,
                       palette["central"], textcolor="white", fontsize=10.2, bold=True)
    for b in boxes2:
        connect(ax, b, central)

    boxes4 = []
    for i, t in enumerate(tier4_labels):
        b = draw_box(ax, xs[i], 3.3, w_col, 1.3, t, palette["tier4"], fontsize=8.3)
        boxes4.append(b)
        connect(ax, central, b)

    for parent_idx, t in tier5_labels:
        cx = xs[parent_idx]
        b = draw_box(ax, cx, 1.0, w_col, 1.2, t, palette["tier5"], fontsize=7.8)
        connect(ax, boxes4[parent_idx], b)

    ax.text(0.15, 9.6, lat_top, rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette["lat"])
    ax.text(0.15, 2.1, lat_bottom, rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette["lat"])

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print("OK ->", filename)


# ----------------------------------------------------------------------
# ARBOL DE PROBLEMAS (tonos rojos/naranjas)
# ----------------------------------------------------------------------
palette_prob = {
    "top": "#F4B6B6", "tier2": "#FAD4D4", "central": "#C0392B",
    "tier4": "#FCE3CF", "tier5": "#FDEFE0", "lat": "#C0392B",
}
build_tree(
    "arbol_problemas.png",
    "ARBOL DE PROBLEMAS - ACUEDUCTO DE TADO (CHOCO)",
    "EFECTO FINAL: Bajo desarrollo humano y persistencia de la pobreza en Tado",
    ["Alta morbi-mortalidad por enfermedades de origen hidrico (EDA)",
     "Gasto familiar elevado en agua embotellada y en hervir agua",
     "Baja calidad de vida y freno al desarrollo economico local",
     "Desconfianza en el prestador y baja cultura de pago"],
    "PROBLEMA CENTRAL: Servicio de acueducto deficiente, discontinuo y con agua no apta "
    "en la cabecera de Tado (pese a estar en una de las zonas mas lluviosas del planeta)",
    ["Sistema de tratamiento insuficiente y obsoleto",
     "Agua cruda con alta turbiedad sin tratamiento adecuado",
     "Redes deterioradas, sin continuidad ni sectorizacion",
     "Baja cobertura, escasa micromedicion y alto IANC"],
    [(0, "Capacidad inferior al caudal de diseno (RAS 0330)"),
     (1, "Lluvias extremas (~7.900 mm/anio) elevan la turbiedad del rio San Juan"),
     (2, "Decadas de baja inversion y conflicto armado en el territorio")],
    palette_prob,
    "EFECTOS", "CAUSAS",
)

# ----------------------------------------------------------------------
# ARBOL DE OBJETIVOS (tonos verdes/azules)
# ----------------------------------------------------------------------
palette_obj = {
    "top": "#BFE3C0", "tier2": "#D6EFD7", "central": "#27772F",
    "tier4": "#D9ECF5", "tier5": "#E8F4FA", "lat": "#27772F",
}
build_tree(
    "arbol_objetivos.png",
    "ARBOL DE OBJETIVOS - ACUEDUCTO DE TADO (CHOCO)",
    "FIN ULTIMO: Mayor desarrollo humano y reduccion de la pobreza en Tado",
    ["Reduccion de la morbi-mortalidad por enfermedades de origen hidrico",
     "Eliminacion del gasto familiar en agua embotellada/hervida",
     "Mejor calidad de vida y reactivacion economica local",
     "Confianza en el prestador y mejor cultura de pago"],
    "OBJETIVO CENTRAL: Garantizar agua potable continua (24 h) y de calidad "
    "para la poblacion de la cabecera de Tado",
    ["Construir/optimizar la PTAP a la capacidad de diseno (45 L/s)",
     "Tratar adecuadamente la alta turbiedad del agua cruda",
     "Rehabilitar y sectorizar las redes para continuidad 24 h",
     "Ampliar cobertura al 98%, micromedicion y reduccion del IANC"],
    [(0, "Procesos y equipos dimensionados segun RAS 0330"),
     (1, "Pretratamiento y clarificacion para picos de turbiedad"),
     (2, "Plan de inversiones cofinanciado (SGR/PDA/cooperacion)")],
    palette_obj,
    "FINES", "MEDIOS",
)

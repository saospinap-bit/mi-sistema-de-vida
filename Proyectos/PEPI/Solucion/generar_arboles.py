# -*- coding: utf-8 -*-
"""
Genera los arboles de PROBLEMAS y OBJETIVOS como esquemas visuales (PNG),
con cajas conectadas por lineas, tipo arbol jerarquico.
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
    """Linea desde el borde inferior de la caja superior al borde superior de la inferior."""
    xt, yt, wt, ht = top_box
    xb, yb, wb, hb = bottom_box
    ax.annotate("", xy=(xb, yb + hb / 2), xytext=(xt, yt - ht / 2),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.1,
                                connectionstyle="arc3,rad=0"))

def build_tree(filename, titulo, top_label, tier2_labels, central_label,
               tier4_labels, tier5_labels, palette):
    """
    palette = dict con colores: top, tier2, central, tier4, tier5
    tier5_labels: lista de (indice_padre, texto)  -> cuelga de la causa/medio i
    """
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title(titulo, fontsize=15, fontweight="bold", color="#1F4E79", pad=14)

    # posiciones X de las 4 columnas
    xs = [2.4, 6.0, 9.6, 13.2]
    w_col = 3.3

    # Tier 1 (top)
    top = draw_box(ax, 7.5, 10.0, 8.5, 1.0, top_label,
                   palette["top"], fontsize=10, bold=True)

    # Tier 2 (consecuencias / fines)
    boxes2 = []
    for i, t in enumerate(tier2_labels):
        b = draw_box(ax, xs[i], 7.9, w_col, 1.2, t, palette["tier2"], fontsize=8.5)
        boxes2.append(b)
        connect(ax, top, b)

    # Tier 3 (problema / objetivo central) -> el tronco
    central = draw_box(ax, 7.5, 5.6, 9.5, 1.1, central_label,
                       palette["central"], textcolor="white", fontsize=10.5, bold=True)
    for b in boxes2:
        connect(ax, b, central)

    # Tier 4 (causas / medios)
    boxes4 = []
    for i, t in enumerate(tier4_labels):
        b = draw_box(ax, xs[i], 3.3, w_col, 1.2, t, palette["tier4"], fontsize=8.5)
        boxes4.append(b)
        connect(ax, central, b)

    # Tier 5 (causas raiz / medios fundamentales)
    for parent_idx, t in tier5_labels:
        cx = xs[parent_idx]
        b = draw_box(ax, cx, 1.0, w_col, 1.1, t, palette["tier5"], fontsize=8)
        connect(ax, boxes4[parent_idx], b)

    # etiquetas laterales
    ax.text(0.15, 9.6, "EFECTOS", rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette["lat"])
    ax.text(0.15, 2.1, "CAUSAS", rotation=90, va="center", ha="center",
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
    "ARBOL DE PROBLEMAS",
    "EFECTO FINAL: Bajo desarrollo social y economico del municipio",
    ["Aumento de enfermedades de origen hidrico (EDA)",
     "Sobrecostos por compra de agua en carrotanques",
     "Baja calidad de vida y deterioro economico local",
     "Perdida de credibilidad institucional del prestador"],
    "PROBLEMA CENTRAL: Deficiente prestacion del servicio de acueducto",
    ["PTAP obsoleta y sobrecargada",
     "Altas perdidas tecnicas y comerciales (IANC 48%)",
     "Redes antiguas y sin sectorizacion",
     "Baja micromedicion y cartera morosa"],
    [(0, "Equipos al final de su vida util"),
     (1, "Conexiones fraudulentas y fugas no detectadas"),
     (2, "Falta de inversion historica en infraestructura")],
    palette_prob,
)

# ----------------------------------------------------------------------
# ARBOL DE OBJETIVOS (tonos verdes)
# ----------------------------------------------------------------------
palette_obj = {
    "top": "#BFE3C0", "tier2": "#D6EFD7", "central": "#27772F",
    "tier4": "#D9ECF5", "tier5": "#E8F4FA", "lat": "#27772F",
}
# reetiquetamos las laterales para el arbol de objetivos
def build_tree_obj():
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 15); ax.set_ylim(0, 11); ax.axis("off")
    ax.set_title("ARBOL DE OBJETIVOS", fontsize=15, fontweight="bold", color="#1F4E79", pad=14)
    xs = [2.4, 6.0, 9.6, 13.2]; w_col = 3.3
    top = draw_box(ax, 7.5, 10.0, 8.5, 1.0,
                   "FIN ULTIMO: Mayor desarrollo social y economico del municipio",
                   palette_obj["top"], fontsize=10, bold=True)
    fines = ["Reduccion de enfermedades de origen hidrico",
             "Eliminacion del gasto en carrotanques",
             "Mejora de calidad de vida y reactivacion economica",
             "Fortalecimiento institucional del prestador"]
    boxes2 = []
    for i, t in enumerate(fines):
        b = draw_box(ax, xs[i], 7.9, w_col, 1.2, t, palette_obj["tier2"], fontsize=8.5)
        boxes2.append(b); connect(ax, top, b)
    central = draw_box(ax, 7.5, 5.6, 9.5, 1.1,
                       "OBJETIVO CENTRAL: Mejorar la prestacion del servicio de acueducto",
                       palette_obj["central"], textcolor="white", fontsize=10.5, bold=True)
    for b in boxes2: connect(ax, b, central)
    medios = ["Construir una nueva PTAP de 120 L/s",
              "Reducir el IANC del 48% al 25%",
              "Rehabilitar y sectorizar las redes",
              "Instalar micromedicion y mejorar el recaudo"]
    boxes4 = []
    for i, t in enumerate(medios):
        b = draw_box(ax, xs[i], 3.3, w_col, 1.2, t, palette_obj["tier4"], fontsize=8.5)
        boxes4.append(b); connect(ax, central, b)
    fundamentales = [(0, "Equipos modernos y eficientes"),
                     (1, "Programa de deteccion de fugas y control de fraude"),
                     (2, "Plan de inversiones plurianual financiado")]
    for parent_idx, t in fundamentales:
        b = draw_box(ax, xs[parent_idx], 1.0, w_col, 1.1, t, palette_obj["tier5"], fontsize=8)
        connect(ax, boxes4[parent_idx], b)
    ax.text(0.15, 9.6, "FINES", rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette_obj["central"])
    ax.text(0.15, 2.1, "MEDIOS", rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette_obj["central"])
    plt.tight_layout()
    plt.savefig("arbol_objetivos.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("OK -> arbol_objetivos.png")

build_tree_obj()

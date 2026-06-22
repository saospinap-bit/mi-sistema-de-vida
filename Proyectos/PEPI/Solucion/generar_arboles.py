# -*- coding: utf-8 -*-
"""
Genera los arboles de PROBLEMAS y OBJETIVOS como esquemas visuales (PNG),
con cajas conectadas por lineas, tipo arbol jerarquico.
Caso: Acueducto del municipio de Tesalia (Huila).
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
            fontweight="bold" if bold else "normal")
    return (cx, cy, w, h)


def connect(ax, top_box, bottom_box, color="#666666"):
    xt, yt, wt, ht = top_box
    xb, yb, wb, hb = bottom_box
    ax.annotate("", xy=(xb, yb + hb / 2), xytext=(xt, yt - ht / 2),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.1))


def build(filename, titulo, top, tier2, central, tier4, tier5, palette, lat_top, lat_bot):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 15); ax.set_ylim(0, 11); ax.axis("off")
    ax.set_title(titulo, fontsize=15, fontweight="bold", color="#1F4E79", pad=14)
    xs = [2.4, 6.0, 9.6, 13.2]; w_col = 3.3
    btop = draw_box(ax, 7.5, 10.0, 9.0, 1.0, top, palette["top"], fontsize=10, bold=True)
    boxes2 = []
    for i, t in enumerate(tier2):
        b = draw_box(ax, xs[i], 7.9, w_col, 1.2, t, palette["tier2"], fontsize=8.5)
        boxes2.append(b); connect(ax, btop, b)
    bc = draw_box(ax, 7.5, 5.6, 10.0, 1.1, central, palette["central"],
                  textcolor="white", fontsize=10.5, bold=True)
    for b in boxes2:
        connect(ax, b, bc)
    boxes4 = []
    for i, t in enumerate(tier4):
        b = draw_box(ax, xs[i], 3.3, w_col, 1.2, t, palette["tier4"], fontsize=8.5)
        boxes4.append(b); connect(ax, bc, b)
    for parent_idx, t in tier5:
        b = draw_box(ax, xs[parent_idx], 1.0, w_col, 1.1, t, palette["tier5"], fontsize=8)
        connect(ax, boxes4[parent_idx], b)
    ax.text(0.15, 9.6, lat_top, rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette["lat"])
    ax.text(0.15, 2.1, lat_bot, rotation=90, va="center", ha="center",
            fontsize=10, fontweight="bold", color=palette["lat"])
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print("OK ->", filename)


# ---------------- ARBOL DE PROBLEMAS (rojos) ----------------
pal_prob = {"top": "#F4B6B6", "tier2": "#FAD4D4", "central": "#C0392B",
            "tier4": "#FCE3CF", "tier5": "#FDEFE0", "lat": "#C0392B"}
build(
    "arbol_problemas.png",
    "ARBOL DE PROBLEMAS - ACUEDUCTO DE TADO (CHOCO)",
    "EFECTO FINAL: Bajo desarrollo social y economico de la cabecera de Tado",
    ["Enfermedades de origen hidrico (EDA) y vectoriales (malaria)",
     "Gasto de los hogares en agua de bloque/embotellada",
     "Baja calidad de vida y deficiente competitividad local",
     "Perdida de credibilidad institucional del prestador"],
    "PROBLEMA CENTRAL: Deficiente prestacion del servicio de acueducto en Tado",
    ["Infraestructura de potabilizacion insuficiente/obsoleta",
     "Altas perdidas tecnicas y comerciales (IANC alto)",
     "Redes antiguas, sin sectorizacion ni micromedicion",
     "Fuente (rio San Juan) vulnerable: alta turbiedad y mineria"],
    [(0, "Baja capacidad de tratamiento; intermitencia"),
     (1, "Conexiones fraudulentas y fugas no detectadas"),
     (3, "Lluvias extremas, sedimentos y mercurio de la mineria")],
    pal_prob, "EFECTOS", "CAUSAS",
)

# ---------------- ARBOL DE OBJETIVOS (verdes) ----------------
pal_obj = {"top": "#BFE3C0", "tier2": "#D6EFD7", "central": "#27772F",
           "tier4": "#D9ECF5", "tier5": "#E8F4FA", "lat": "#27772F"}
build(
    "arbol_objetivos.png",
    "ARBOL DE OBJETIVOS - ACUEDUCTO DE TADO (CHOCO)",
    "FIN ULTIMO: Mayor desarrollo social y economico de la cabecera de Tado",
    ["Reduccion de enfermedades de origen hidrico y vectorial",
     "Eliminacion del gasto de los hogares en agua alterna",
     "Mejora de la calidad de vida y la competitividad",
     "Fortalecimiento institucional del prestador"],
    "OBJETIVO CENTRAL: Mejorar la prestacion del servicio de acueducto en Tado",
    ["Construir una PTAP de 45 L/s (Resolucion 0330 de 2017)",
     "Reducir el IANC al 25% (meta Res 0330)",
     "Rehabilitar, sectorizar redes e instalar micromedicion",
     "Asegurar la fuente: captacion robusta y pretratamiento"],
    [(0, "Equipos modernos y eficientes; agua apta (Res 2115/2007)"),
     (1, "Programa de deteccion de fugas y control de fraude"),
     (3, "Bocatoma y desarenador para alta turbiedad del rio San Juan")],
    pal_obj, "FINES", "MEDIOS",
)

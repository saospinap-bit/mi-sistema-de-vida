# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

fig, ax = plt.subplots(figsize=(11, 9))

# Niveles (m) medidos desde N +/- 0.00 (piso terminado)
# capa: (y_top, y_bot, color, etiqueta, item)
capas = [
    (0.00, -0.05, "#f0e6d2", "Acabado de piso", "acabado"),
    (-0.05, -0.15, "#8c8c8c", "PLACA de contrapiso  e=0.10  (malla 150x150x5.0)", "item 4.3.1"),
    (-0.15, -0.45, "#c9c9c9", "SUB-BASE granular  e=0.30", "item 2.1.2  (corregir a 0.30)"),
    (-0.45, -0.65, "#d2a679", "RECEBO (relleno sobre vigas - va aparte)  e=0.20", "item 2.1.4"),
    (-0.65, -1.10, "#9e9e9e", "VIGA de cimentacion  0.40x0.45", "item 2.2.1"),
    (-1.10, -1.50, "#7a7a7a", "ZAPATA  H=0.40  (Z-1 2.30 / Z-2 2.15)", "cuadro zapatas"),
    (-1.50, -1.55, "#7fbf7f", "Solado de limpieza  e=0.05", "item 2.2.2"),
]
xL, xR = 0, 10
for ytop, ybot, color, lab, item in capas:
    ax.add_patch(Rectangle((xL, ybot), xR-xL, ytop-ybot, facecolor=color, edgecolor="black", lw=0.8))
    ym = (ytop+ybot)/2
    ax.text((xL+xR)/2, ym, f"{lab}", ha="center", va="center", fontsize=9.5,
            color="white" if color in ("#7a7a7a","#9e9e9e","#8c8c8c") else "black")
    ax.text(xR+0.15, ym, item, ha="left", va="center", fontsize=8.5, color="#1f3b73")

# terreno natural (hatch) a los lados de la zona profunda
ax.add_patch(Rectangle((xL, -1.55), xR-xL, 0.0, facecolor="none"))

# Lineas de nivel + etiquetas a la izquierda
niveles = {
    0.00: "N +/- 0.00  (piso terminado)",
    -0.05: "NE -0.05  (top placa)",
    -0.45: "-0.45  (fondo sub-base)",
    -0.65: "-0.65  (top viga / fondo recebo)",
    -1.10: "NE -1.10  (top zapata / fondo viga)",
    -1.50: "-1.50  Nivel de DESPLANTE",
    -1.55: "-1.55  (fondo excavacion)",
}
for y, txt in niveles.items():
    ax.plot([xL-0.4, xR], [y, y], color="red", lw=0.8, ls=(0,(4,3)))
    ax.text(xL-0.5, y, txt, ha="right", va="center", fontsize=8.5, color="red")

# Cota excavacion masiva = solo placa + sub-base (0.40 m)
ax.annotate("", xy=(xR+3.5, -0.05), xytext=(xR+3.5, -0.45), arrowprops=dict(arrowstyle="<->", color="green", lw=1.4))
ax.text(xR+3.7, -0.25, "EXCAVACION\nMASIVA (2.1.1)\n= 0.40 m\n(sub-base+placa)", ha="left", va="center", fontsize=9, color="green", fontweight="bold")
# Cota excavacion manual/profunda (desde -0.45 hacia abajo)
ax.annotate("", xy=(xR+3.5, -0.45), xytext=(xR+3.5, -1.55), arrowprops=dict(arrowstyle="<->", color="purple", lw=1.4))
ax.text(xR+3.7, -1.0, "EXCAVACION\nmanual (2.1.3)\nvigas y zapatas\n(desde -0.45)", ha="left", va="center", fontsize=9, color="purple", fontweight="bold")

ax.set_xlim(-4.2, 17.5)
ax.set_ylim(-1.9, 0.35)
ax.set_title("CORTE LOGICO DE LA CIMENTACION - Modulo 1 (niveles desde N +/- 0.00)", fontsize=12, fontweight="bold")
ax.axis("off")
p = os.path.join("_img", "esq_seccion_general.png")
fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
print("OK", p)

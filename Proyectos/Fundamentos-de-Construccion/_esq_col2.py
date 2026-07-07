# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

fig, axs = plt.subplots(1, 2, figsize=(8, 5))
datos = [
    (axs[0], 0.40, 4.70, "COLUMNA TIPO 1\n0.40 x 0.40\nh = 4.70 m\n4 unidades\n(ejes 1A,1B,3'B,4A)\nrefuerzo 6#6", "#7a7a7a"),
    (axs[1], 0.50, 4.90, "COLUMNA TIPO 2\n0.50 x 0.50\nh = 4.90 m\n4 unidades\n(ejes 2A,2B,3A,3B)\nrefuerzo 4#6+4#7", "#5a6a7a"),
]
for ax, b, h, txt, col in datos:
    ax.add_patch(Rectangle((0, 0), b, h, facecolor=col, edgecolor="k"))
    ax.text(b/2, h/2, txt, ha="center", va="center", color="white", fontsize=9)
    ax.annotate("", xy=(-0.12, 0), xytext=(-0.12, h), arrowprops=dict(arrowstyle="<->"))
    ax.text(-0.3, h/2, f"h = {h:.2f} m", rotation=90, va="center", fontsize=9)
    ax.annotate("", xy=(0, -0.25), xytext=(b, -0.25), arrowprops=dict(arrowstyle="<->"))
    ax.text(b/2, -0.55, f"{b:.2f} m", ha="center", fontsize=9)
    ax.set_xlim(-0.6, 0.8); ax.set_ylim(-0.9, 5.2); ax.axis("off")
fig.suptitle("Esquema 4. Columnas: 8 unidades en DOS tipos (verificado en el despiece del plano)", fontsize=11)
p = os.path.join("_img", "esq_columna2.png")
fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
print("OK", p)

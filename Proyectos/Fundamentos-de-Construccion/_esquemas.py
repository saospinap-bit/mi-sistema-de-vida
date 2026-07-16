# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import os

OUT = "_img"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 11})

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", name)

# ---------------------------------------------------------------
# 1. SECCION DE CAPAS BAJO PLACA (excavacion, recebo, subbase, placa)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
capas = [
    ("Terreno natural excavado (fondo)", 0.00, 0.00, "#b8860b", ""),
    ("Recebo comun compactado  e = 0.20 m  (item 2.1.4)", 0.00, 0.20, "#d2a679", "0.20"),
    ("Sub-base granular B-400  e = 0.15 m  (item 2.1.2)", 0.20, 0.15, "#c2c2c2", "0.15"),
    ("Placa de contrapiso concreto 3000 psi  e = 0.10 m  (item 4.3.1)", 0.35, 0.10, "#8c8c8c", "0.10"),
]
xw = 9.85
for label, y0, h, color, et in capas:
    if h == 0: continue
    ax.add_patch(Rectangle((0, y0), xw, h, facecolor=color, edgecolor="black"))
    ax.text(xw/2, y0 + h/2, label, ha="center", va="center", fontsize=9)
    if et:
        ax.annotate("", xy=(xw+0.4, y0), xytext=(xw+0.4, y0+h),
                    arrowprops=dict(arrowstyle="<->"))
        ax.text(xw+0.7, y0+h/2, et+" m", va="center", fontsize=9)
# geotextil line
ax.plot([0, xw], [0.20, 0.20], color="green", lw=2)
ax.text(0.2, 0.205, "Geotextil NT1600 (item 2.1.6)", color="green", fontsize=8, va="bottom")
# excavation depth arrow
ax.annotate("", xy=(-0.6, 0.0), xytext=(-0.6, 0.55), arrowprops=dict(arrowstyle="<->", color="red"))
ax.text(-1.4, 0.275, "Excavacion\nH = 0.55 m\n(item 2.1.1)", color="red", fontsize=9, va="center")
ax.plot([-0.9, xw], [0.55, 0.55], color="red", ls="--", lw=1)
ax.text(xw/2, 0.57, "Nivel N +/- 0.00 (piso terminado)", ha="center", fontsize=8, color="red")
ax.set_xlim(-2.2, xw+2)
ax.set_ylim(-0.1, 0.72)
ax.set_title("Esquema 1. Corte tipico del sistema de piso  (Ancho placa = 9.85 m ; Largo = 21.95 m)")
ax.axis("off")
save(fig, "esq_capas_placa.png")

# ---------------------------------------------------------------
# 2. PLANTA DE EJES ESQUEMATICA (columnas, vigas)
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))
L = 19.8; W = 7.3
ax.add_patch(Rectangle((0,0), L, W, fill=False, lw=1, ls="--"))
# ejes verticales (columnas) posiciones aprox: 1,2,3,3',4 -> 0,6.6,13.2,18.4,19.8
xs = [0, 6.6, 13.2, 18.4, 19.8]
ejes_x = ["1","2","3","3'","4"]
# usamos 5 ejes x 2 ejes(A,B) pero enunciado usa 10 columnas
xs5 = [0, 6.6, 13.2, 18.4, 19.8]
for i,x in enumerate(xs5):
    for y in [0, W]:
        ax.add_patch(Rectangle((x-0.2, y-0.2), 0.4, 0.4, facecolor="#555", edgecolor="k"))
    ax.text(x, W+0.6, ejes_x[i], ha="center", fontweight="bold")
ax.text(-0.9, 0, "B", va="center", fontweight="bold")
ax.text(-0.9, W, "A", va="center", fontweight="bold")
# vigas longitudinales
ax.plot([0,L],[0,0], color="orange", lw=3)
ax.plot([0,L],[W,W], color="orange", lw=3)
ax.text(L/2, W+0.05, "VC-A / VC-B  L = 19.80 m  (2 vigas long.)", color="darkorange", ha="center", fontsize=9)
# vigas transversales
for x in xs5:
    ax.plot([x,x],[0,W], color="royalblue", lw=2)
ax.text(xs5[2], W/2, "  VC transversales\n  luz libre 7.30 m (x5)", color="royalblue", fontsize=9, va="center")
# cota total
ax.annotate("", xy=(0,-1.1), xytext=(L,-1.1), arrowprops=dict(arrowstyle="<->"))
ax.text(L/2,-1.5,"19.80 m (entre ejes 1 y 4)", ha="center")
ax.annotate("", xy=(-0.5,0), xytext=(-0.5,W), arrowprops=dict(arrowstyle="<->"))
ax.text(-1.6, W/2, "7.30 m", rotation=90, va="center")
ax.set_xlim(-2.5, L+1)
ax.set_ylim(-2, W+1.4)
ax.set_title("Esquema 2. Planta estructural esquematica: 10 columnas (0.40x0.40), vigas long. (2) y transv. (5)")
ax.axis("off")
save(fig, "esq_planta_ejes.png")

# ---------------------------------------------------------------
# 3. SECCION VIGA DE CIMENTACION 0.40 x 0.45 + solado
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.6, 5))
ax.add_patch(Rectangle((0,0.05), 0.5, 0.05, facecolor="#cfcfcf", edgecolor="k"))  # solado 0.50 ancho
ax.text(0.25, 0.02, "Solado 1500 psi  e=0.05  ancho 0.50 (item 2.2.2)", ha="center", fontsize=7.5)
ax.add_patch(Rectangle((0.05,0.10), 0.40, 0.45, facecolor="#9e9e9e", edgecolor="k"))
ax.text(0.25, 0.32, "VIGA\n0.40 x 0.45\n(item 2.2.1)", ha="center", va="center", fontsize=9, color="white")
# cotas
ax.annotate("", xy=(0.05,-0.02), xytext=(0.45,-0.02), arrowprops=dict(arrowstyle="<->"))
ax.text(0.25,-0.06,"B = 0.40 m", ha="center", fontsize=9)
ax.annotate("", xy=(0.5,0.10), xytext=(0.5,0.55), arrowprops=dict(arrowstyle="<->"))
ax.text(0.54,0.32,"H = 0.45 m", va="center", fontsize=9)
ax.set_xlim(-0.05,0.75); ax.set_ylim(-0.12,0.62)
ax.set_title("Esquema 3. Seccion viga de cimentacion", fontsize=10)
ax.axis("off")
save(fig, "esq_viga_cim.png")

# ---------------------------------------------------------------
# 4. COLUMNA 0.40x0.40 h=4.90
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.6,5.2))
ax.add_patch(Rectangle((0,0),0.4,4.9, facecolor="#9e9e9e", edgecolor="k"))
ax.text(0.2,2.45,"COLUMNA\n0.40 x 0.40\nh = 4.90 m\n(x 10 und)\nitem 4.1.1", ha="center", va="center", color="white", fontsize=9)
ax.annotate("", xy=(-0.15,0), xytext=(-0.15,4.9), arrowprops=dict(arrowstyle="<->"))
ax.text(-0.35,2.45,"h = 4.90 m", rotation=90, va="center")
ax.annotate("", xy=(0,-0.2), xytext=(0.4,-0.2), arrowprops=dict(arrowstyle="<->"))
ax.text(0.2,-0.45,"0.40 m", ha="center")
ax.set_xlim(-0.6,0.7); ax.set_ylim(-0.7,5.2)
ax.set_title("Esquema 4. Columna tipo", fontsize=10)
ax.axis("off")
save(fig, "esq_columna.png")

# ---------------------------------------------------------------
# 5. PLACA DE CUBIERTA con viguetas
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8,4))
Wc = 7.3; Lc = 5.55+6.1+6.87
ax.add_patch(Rectangle((0,0), Lc, Wc, facecolor="#d9e6f2", edgecolor="k"))
# viguetas (6) a lo ancho
for i in range(1,7):
    y = Wc*i/7
    ax.plot([0,Lc],[y,y], color="#375d81", lw=2)
ax.text(Lc/2, Wc*0.5, "PLACA DE CUBIERTA  e = 0.08 m (aligerada)\nlargo = 5.55+6.10+6.87 = 18.52 m ; ancho 7.30 m",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round", fc="white", alpha=0.8))
ax.text(Lc*0.02, Wc/7*1.0+0.05, "6 viguetas 0.20 x 0.32 (item 4.3.3)", color="#375d81", fontsize=8)
ax.annotate("", xy=(0,-0.6), xytext=(Lc,-0.6), arrowprops=dict(arrowstyle="<->"))
ax.text(Lc/2,-1.05,"18.52 m", ha="center")
ax.annotate("", xy=(-0.5,0), xytext=(-0.5,Wc), arrowprops=dict(arrowstyle="<->"))
ax.text(-1.4,Wc/2,"7.30 m", rotation=90, va="center")
ax.set_xlim(-2.2,Lc+1); ax.set_ylim(-1.5,Wc+0.6)
ax.set_title("Esquema 5. Placa de cubierta aligerada y viguetas")
ax.axis("off")
save(fig, "esq_cubierta.png")

# ---------------------------------------------------------------
# 6. MURO (mamposteria) elevacion con descuento de vanos
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8,3.6))
Lm = 12; Hm = 2.9
ax.add_patch(Rectangle((0,0), Lm, Hm, facecolor="#e8d5b5", edgecolor="k", hatch="//"))
# vanos (puertas/ventanas) ~20%
ax.add_patch(Rectangle((2,0), 1.2, 2.1, facecolor="white", edgecolor="k"))
ax.text(2.6,1.05,"puerta", ha="center", fontsize=7, rotation=90)
ax.add_patch(Rectangle((6.5,0.9), 2.2, 1.2, facecolor="white", edgecolor="k"))
ax.text(7.6,1.5,"ventana", ha="center", fontsize=7)
# columnetas
for x in [0,3,6,9,12]:
    ax.add_patch(Rectangle((x-0.08,0),0.16,Hm, facecolor="#8c8c8c"))
ax.text(Lm/2, Hm+0.15, "Longitud total de muros L = 173.60 m  (item 5.1.1)  |  H = 2.90 m",
        ha="center", fontsize=9)
ax.text(0.1, -0.35, "Columnetas de confinamiento cada 3 m -> 58 und (item 5.1.2)", fontsize=8, color="#444")
ax.text(0.1, -0.75, "Descuento de vanos = 20%  |  Panete = 65% del area (items 5.1.1 y 5.1.4)", fontsize=8, color="#444")
ax.annotate("", xy=(-0.4,0), xytext=(-0.4,Hm), arrowprops=dict(arrowstyle="<->"))
ax.text(-1.1,Hm/2,"H=2.90", rotation=90, va="center")
ax.set_xlim(-1.6,Lm+0.5); ax.set_ylim(-1.0,Hm+0.6)
ax.set_title("Esquema 6. Elevacion tipica de muro (mamposteria confinada)")
ax.axis("off")
save(fig, "esq_muro.png")

print("TODOS LOS ESQUEMAS GENERADOS")

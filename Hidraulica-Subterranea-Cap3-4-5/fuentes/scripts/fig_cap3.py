import os
os.environ['MPLCONFIGDIR'] = '/tmp/mplcfg'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle, FancyArrow

OUT = '/projects/sandbox/.build/fig'
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'font.size': 9, 'font.family': 'DejaVu Sans',
    'axes.linewidth': 0.8, 'savefig.dpi': 200,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.15,
})

SOIL = '#e8e2d8'
AQ   = '#d6e4f0'
CLAY = '#cfc8bd'
WATER= '#bcd9ef'


def save(fig, name):
    fig.savefig(f'{OUT}/{name}.png', facecolor='white')
    plt.close(fig)
    print('  ->', name)


# ---------------------------------------------------------------- 3.6
def fig_306():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.6))

    for a in (ax, ax2):
        a.set_aspect('equal'); a.axis('off')

    # --- panel 1: geometry + solution
    B = (0, 0); C = (1000, 0); A = (0, 2000)
    tri = Polygon([B, C, A], closed=True, fc='#f4f4f0', ec='k', lw=1.4, zorder=1)
    ax.add_patch(tri)

    # equipotential 400 m : P(0,1000) - C(1000,0)
    P = (0, 1000)
    ax.plot([P[0], C[0]], [P[1], C[1]], '--', color='#1a4e8a', lw=1.8, zorder=3)
    ax.text(620, 520, 'equipotencial\n$h=400$ m', color='#1a4e8a',
            fontsize=8.5, rotation=-63, ha='center', va='center')

    # perpendicular from B to that line
    ax.plot([0, 500], [0, 500], '-', color='#b03030', lw=1.8, zorder=4)
    ax.annotate('', xy=(0, 0), xytext=(500, 500),
                arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=1.8))
    ax.text(300, 150, '$d_\\perp = 707$ m', color='#b03030', fontsize=8.5,
            rotation=45, ha='center')

    # flow arrow
    ax.annotate('', xy=(-420, -420), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=2.6))
    ax.text(-250, -520, 'FLUJO\nS 45° W\n$i=0.141$', color='#b03030',
            fontsize=9, ha='center', va='top', fontweight='bold')

    # nodes
    for (x, y), lab, h in [(A, 'A', 500), (B, 'B', 300), (C, 'C', 400)]:
        ax.plot(x, y, 'o', ms=9, mfc='white', mec='k', mew=1.5, zorder=5)
        ax.text(x, y, lab, ha='center', va='center', fontsize=8, zorder=6)
    ax.text(A[0], A[1] + 120, '$h = 500$ m', ha='center', fontsize=9.5)
    ax.text(B[0] - 90, B[1], '$h = 300$ m', ha='right', va='center', fontsize=9.5)
    ax.text(C[0] + 70, C[1], '$h = 400$ m', ha='left', va='center', fontsize=9.5)
    ax.text(P[0] - 60, P[1], 'P', ha='right', va='center', fontsize=8,
            color='#1a4e8a')
    ax.plot(P[0], P[1], 's', ms=6, color='#1a4e8a', zorder=5)

    # dimensions
    ax.annotate('', xy=(-230, 0), xytext=(-230, 2000),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
    ax.text(-270, 1000, '2000 m', rotation=90, va='center', ha='right', fontsize=8.5)
    ax.annotate('', xy=(0, -200), xytext=(1000, -200),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
    ax.text(500, -250, '1000 m', ha='center', va='top', fontsize=8.5)

    # north arrow
    ax.annotate('', xy=(900, 1900), xytext=(900, 1600),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2))
    ax.text(900, 1950, 'N', ha='center', fontsize=9, fontweight='bold')

    ax.set_xlim(-700, 1250); ax.set_ylim(-800, 2200)
    ax.set_title('Geometría y solución gráfica', fontsize=10, pad=2)

    # --- panel 2: gradient vector decomposition
    ax2.annotate('', xy=(1, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.6))
    ax2.annotate('', xy=(0, 1), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.6))
    ax2.annotate('', xy=(1, 1), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=2.6))
    ax2.plot([1, 1], [0, 1], ':', color='#999', lw=1)
    ax2.plot([0, 1], [1, 1], ':', color='#999', lw=1)
    ax2.annotate('', xy=(-0.78, -0.78), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=2.6))
    ax2.text(1.04, -0.02, '$\\partial h/\\partial x = 0.100$', fontsize=9, va='top')
    ax2.text(-0.03, 1.06, '$\\partial h/\\partial y = 0.100$', fontsize=9, ha='left')
    ax2.text(0.62, 0.78, '$\\nabla h$\n$|\\nabla h| = 0.141$\nN 45° E',
             color='#1a4e8a', fontsize=9, ha='left', va='center', fontweight='bold')
    ax2.text(-0.52, -0.62, '$\\mathbf{q} = -K\\nabla h$\nS 45° W',
             color='#b03030', fontsize=9, ha='center', va='top', fontweight='bold')
    th = np.linspace(0, np.pi / 4, 40)
    ax2.plot(0.33 * np.cos(th), 0.33 * np.sin(th), '-', color='#1a4e8a', lw=0.9)
    ax2.text(0.42, 0.14, '45°', fontsize=8, color='#1a4e8a')
    ax2.set_xlim(-1.15, 1.75); ax2.set_ylim(-1.3, 1.35)
    ax2.set_title('El flujo es opuesto al gradiente', fontsize=10, pad=2)
    save(fig, 'fig_3_06_tres_puntos')


# ---------------------------------------------------------------- 3.7
def fig_307():
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    xs = [0, 5000, 10000, 15000]
    names = ['A', 'B', 'C', 'D']
    ht = [300, 205, 110, 15]
    dep = [200, 190, 50, 8]
    z = [h - d for h, d in zip(ht, dep)]

    # ground surface (= top of piezometers, where water level is)
    gx = np.array([-1600] + xs + [16600])
    gy = np.array([300 + 1600 * 0.019] + ht + [15 - 1600 * 0.019])
    ax.plot(gx, gy, '-', color='#4a7c2f', lw=1.6, zorder=4)
    ax.fill_between(gx, gy, -40, color=SOIL, zorder=0)
    ax.text(8400, 420, 'superficie del terreno = tope de los piezómetros '
                       '(nivel de agua, $i = 0.019$)', fontsize=8,
            color='#2f5c1a', va='center', ha='center',
            bbox=dict(fc='white', ec='#4a7c2f', lw=.7, alpha=.92, pad=2.5))

    # sea level datum
    ax.axhline(0, color='#1a4e8a', lw=1.4, zorder=3)
    ax.text(16900, 8, 'nivel del mar (datum, $z=0$)', fontsize=8.5,
            color='#1a4e8a', ha='right', va='bottom')

    for i, (x, n) in enumerate(zip(xs, names)):
        w = 330
        # piezometer casing
        ax.add_patch(Rectangle((x - w / 2, z[i]), w, dep[i], fc=WATER,
                               ec='k', lw=1.2, zorder=5))
        ax.add_patch(Rectangle((x - w / 2, z[i]), w, dep[i], fc='none',
                               ec='#2b6ca3', lw=0, hatch='....', zorder=5,
                               alpha=.55))
        ax.plot(x, z[i], 'v', ms=7, color='k', zorder=7)

        # stacked label box above each piezometer
        ytxt = [370, 285, 200, 118][i]
        ax.text(x, ytxt, f'$\\bf{{{n}}}$\n$h$ = {ht[i]} m\n'
                         f'$h_p$ = {dep[i]} m\n$z$ = {z[i]} m',
                ha='center', va='bottom', fontsize=8.4, color='#13335c',
                linespacing=1.35,
                bbox=dict(fc='white', ec='#1a4e8a', lw=.9, alpha=.95, pad=2.5),
                zorder=9)
        ax.plot([x, x], [ht[i], ytxt], '-', color='#1a4e8a', lw=.7, zorder=4)

        # pressure-head and elevation-head dimension arrows
        ax.annotate('', xy=(x + w / 2 + 110, z[i]), xytext=(x + w / 2 + 110, ht[i]),
                    arrowprops=dict(arrowstyle='<|-|>', color='#2b6ca3', lw=1.0))
        ax.text(x + w / 2 + 160, (z[i] + ht[i]) / 2, '$h_p$', fontsize=9,
                color='#2b6ca3', va='center')
        ax.annotate('', xy=(x - w / 2 - 110, 0), xytext=(x - w / 2 - 110, z[i]),
                    arrowprops=dict(arrowstyle='<|-|>', color='#b05a00', lw=1.0))
        ax.text(x - w / 2 - 160, z[i] / 2 + 6, '$z$', fontsize=9,
                color='#b05a00', va='center', ha='right')

    # spacing
    for a, b in zip(xs[:-1], xs[1:]):
        ax.annotate('', xy=(a, -55), xytext=(b, -55),
                    arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
        ax.text((a + b) / 2, -72, '5000 m   ($\\Delta h = 95$ m)',
                ha='center', va='top', fontsize=8)

    ax.set_xlim(-2100, 17200); ax.set_ylim(-130, 470)
    ax.set_yticks([0, 100, 200, 300])
    ax.set_ylabel('cota (m sobre el nivel del mar)', fontsize=9)
    ax.set_xticks([])
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.set_title('Problema 3.7 — descomposición $h = z + h_p$ en cuatro piezómetros',
                 fontsize=10)
    save(fig, 'fig_3_07_piezometros')


# ---------------------------------------------------------------- 3.9
def fig_309():
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 3.1, fc=AQ, ec='none'))
    ax.add_patch(Rectangle((0, -0.35), 10, 0.35, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))
    ax.plot([0, 10], [3.1, 3.1], color='#4a7c2f', lw=1.5)
    ax.text(5, 3.2, 'superficie del terreno', ha='center', fontsize=8,
            color='#2f5c1a')
    ax.text(5, -0.55, 'base impermeable', ha='center', va='top', fontsize=8)

    for x, lab in [(2.0, '1'), (8.0, '2')]:
        ax.add_patch(Rectangle((x - .13, 1.3), .26, 1.8, fc='white', ec='k', lw=1.2))
        ax.plot(x, 1.3, 'v', ms=7, color='k')
        ax.text(x, 3.3, f'barreno {lab}', ha='center', fontsize=8.5)
        ax.plot(x, 1.3, 'o', ms=14, mfc='none', mec='#b03030', mew=1.4)
        ax.text(x, 0.95, f'$P_{lab}$', ha='center', fontsize=10, color='#b03030')

    ax.plot([0.4, 9.6], [1.3, 1.3], '--', color='#b03030', lw=1.2)
    ax.text(0.3, 1.3, 'misma\ncota $z$', ha='right', va='center', fontsize=8,
            color='#b03030')
    ax.annotate('', xy=(6.6, 2.1), xytext=(3.4, 2.1),
                arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=2.4))
    ax.text(5, 2.3, 'FLUJO HORIZONTAL', ha='center', fontsize=9,
            color='#1a4e8a', fontweight='bold')
    ax.annotate('', xy=(8, 0.55), xytext=(2, 0.55),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
    ax.text(5, 0.42, '$L$', ha='center', va='top', fontsize=9)

    ax.text(5, -1.25,
            'Condición: $\\partial z/\\partial x = 0$  (presiones medidas a igual elevación)\n'
            '$\\Rightarrow\\ q_x = -(k/\\mu)\\,\\partial P/\\partial x$',
            ha='center', va='top', fontsize=9.5)
    ax.set_xlim(-1.4, 11); ax.set_ylim(-2.3, 3.8)
    ax.set_title('Problema 3.9 — cuándo vale la forma de presión de la ley de Darcy',
                 fontsize=10)
    save(fig, 'fig_3_09_darcy_presion')


# ---------------------------------------------------------------- 3.11
def fig_311():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9))
    Ks = ['$K_1 = 10^{-6}$', '$K_2 = 10^{-7}$', '$K_3 = 10^{-8}$']
    cols = ['#9ec5e8', '#c9b9a0', '#b5a898']
    for a, title in zip((ax, ax2),
                        ['Flujo HORIZONTAL  (capas en PARALELO)',
                         'Flujo VERTICAL  (capas en SERIE)']):
        a.set_aspect('equal'); a.axis('off')
        for i in range(3):
            y = 2 - i
            a.add_patch(Rectangle((0, y), 6, 1, fc=cols[i], ec='k', lw=1))
            a.text(-0.2, y + .5, Ks[i], ha='right', va='center', fontsize=9)
            a.text(6.2, y + .5, '20 m', ha='left', va='center', fontsize=8)
        a.set_title(title, fontsize=9.5, pad=4)
        a.set_xlim(-2.1, 7.4); a.set_ylim(-1.5, 3.9)

    for i in range(3):
        y = 2.5 - i
        n = [5, 2, 1][i]
        for k in range(n):
            xx = 0.6 + k * (4.8 / max(n, 1))
            ax.annotate('', xy=(xx + .7, y), xytext=(xx, y),
                        arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=1.4))
    ax.text(3, -0.35, '$K_h=\\dfrac{\\sum K_ib_i}{\\sum b_i}=3.70\\times10^{-7}$ m/s\n'
                      'media ARITMÉTICA — la domina la capa MÁS permeable',
            ha='center', va='top', fontsize=9)

    for k in range(5):
        xx = 0.8 + k * 1.1
        ax2.annotate('', xy=(xx, 1.9), xytext=(xx, 3.1),
                     arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=1.4))
        ax2.annotate('', xy=(xx, 0.95), xytext=(xx, 1.9),
                     arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=1.4))
        ax2.annotate('', xy=(xx, -0.05), xytext=(xx, 0.95),
                     arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=1.4))
    ax2.text(3, -0.45, '$K_v=\\dfrac{\\sum b_i}{\\sum b_i/K_i}=2.70\\times10^{-8}$ m/s\n'
                       'media ARMÓNICA — la domina la capa MENOS permeable',
             ha='center', va='top', fontsize=9)
    fig.suptitle('Problema 3.11 — $K_h/K_v = 13.7$: la estratificación crea anisotropía',
                 fontsize=10, y=1.02)
    save(fig, 'fig_3_11_capas')


# ---------------------------------------------------------------- 3.13
def fig_313():
    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    ax.set_aspect('auto'); ax.axis('off')
    xe = [0.4, 2.4, 3.9, 8.4]          # equipotential positions
    be = [3.0, 2.55, 2.25, 1.65]       # thickness at each
    top = np.interp(np.linspace(0, 9, 300), [0] + xe + [9],
                    [3.1, 3.0, 2.55, 2.25, 1.65, 1.55])
    xx = np.linspace(0, 9, 300)
    ax.fill_between(xx, 0, top, color=AQ, ec='k', lw=1.2)
    ax.plot(xx, top, 'k-', lw=1.4)
    ax.plot([0, 9], [0, 0], 'k-', lw=1.4)
    ax.add_patch(Rectangle((0, -0.3), 9, 0.3, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))

    for x, b, lab in zip(xe, be, ['$b_4$', '$b_3$', '$b_2$', '$b_1$']):
        ax.plot([x, x], [0, b], '--', color='#1a4e8a', lw=1.6)
        ax.text(x, -0.45, lab, ha='center', va='top', fontsize=9.5)
    ax.text(8.75, 2.9, 'líneas de\nigual carga', color='#1a4e8a', fontsize=8.5,
            ha='right', va='top')

    for yy in [0.45, 1.05, 1.65]:
        ax.annotate('', xy=(8.9, yy), xytext=(0.05, yy),
                    arrowprops=dict(arrowstyle='-|>', color='#555', lw=1.2))
    ax.text(0.1, 2.0, 'líneas de flujo', fontsize=8.5, color='#555')

    for (a, b), lab, k in zip(list(zip(xe[:-1], xe[1:])),
                              ['$L_1$', '$L_2$', '$L_3$'],
                              ['$K_1$', '$K_2$', '$K_3$']):
        ax.annotate('', xy=(a, -0.95), xytext=(b, -0.95),
                    arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
        ax.text((a + b) / 2, -1.08, lab, ha='center', va='top', fontsize=9)
        ax.text((a + b) / 2, 2.95, k, ha='center', fontsize=12, color='#b03030')

    ax.text(4.5, -1.75,
            '$Q$ = cte  y  $\\Delta h$ = cte   $\\Rightarrow$   '
            '$K_i \\propto L_i / A_i$      '
            '(equipotenciales separadas $\\Rightarrow$ $K$ alta;  juntas $\\Rightarrow$ $K$ baja)',
            ha='center', va='top', fontsize=9.5)
    ax.set_xlim(-0.5, 9.5); ax.set_ylim(-2.6, 3.4)
    ax.set_title('Problema 3.13 — leer conductividades relativas en una red de flujo '
                 '(esquema de la figura 3.E4)', fontsize=10)
    save(fig, 'fig_3_13_redflujo')


# ---------------------------------------------------------------- 3.14
def fig_314():
    fig, axs = plt.subplots(2, 2, figsize=(9.2, 5.6),
                            gridspec_kw=dict(height_ratios=[1, 1.25]))
    x = np.linspace(0, 1, 400)

    # convex (recharge): h decreasing, gradient increasing
    h_r = 10 * np.sqrt(1 - x ** 2) * 0 + 10 * (1 - x ** 2) ** .5
    h_d = 10 * (1 - x)
    h_dd = 10 - 10 * (1 - (1 - x) ** 2) ** .5
    h_u = 10 * (1 - x)

    for col, (hh, ttl, arrows, note) in enumerate([
        (h_r, '(a) RECARGA uniforme', 'down',
         'Q aumenta  $\\Rightarrow$  $i$ aumenta  $\\Rightarrow$  equipotenciales se JUNTAN\n'
         'superficie CONVEXA hacia arriba'),
        (h_dd, '(b) DESCARGA uniforme', 'up',
         'Q disminuye  $\\Rightarrow$  $i$ disminuye  $\\Rightarrow$  equipotenciales se SEPARAN\n'
         'superficie CÓNCAVA hacia arriba')]):
        a = axs[0, col]
        a.plot(x, hh, '-', color='#1a4e8a', lw=2.2)
        a.plot(x, h_u, ':', color='#999', lw=1.4)
        for k in range(9):
            xa = 0.05 + k * 0.11
            if arrows == 'down':
                a.annotate('', xy=(xa, np.interp(xa, x, hh)), xytext=(xa, 12.3),
                           arrowprops=dict(arrowstyle='-|>', color='#2b8a3e', lw=1.1))
            else:
                a.annotate('', xy=(xa, 12.3), xytext=(xa, np.interp(xa, x, hh)),
                           arrowprops=dict(arrowstyle='-|>', color='#b05a00', lw=1.1))
        a.text(0.5, 13.2, 'recarga (lluvia)' if arrows == 'down'
               else 'descarga (ET, manantiales)', ha='center', fontsize=8.5,
               color='#2b8a3e' if arrows == 'down' else '#b05a00')
        a.text(0.97, 9.4, 'uniforme\n(referencia)', fontsize=7.5, color='#888',
               ha='right', va='top')
        a.set_ylim(-0.6, 15.5); a.set_xlim(-0.03, 1.03)
        a.set_title(ttl, fontsize=10)
        a.set_ylabel('carga $h$ (m)', fontsize=8.5)
        a.set_xticks([]); a.tick_params(labelsize=8)

        # equipotential spacing in plan
        b = axs[1, col]
        b.axis('off')
        b.add_patch(Rectangle((0, 0), 1, 0.55, fc=AQ, ec='k', lw=1.1))
        levels = np.linspace(hh[0], hh[-1], 11)[1:-1]
        for lv in levels:
            xi = np.interp(-lv, -hh, x)
            b.plot([xi, xi], [0, 0.55], '-', color='#1a4e8a', lw=1.3)
        b.annotate('', xy=(1.0, -0.13), xytext=(0.0, -0.13),
                   arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=2))
        b.text(0.5, -0.2, 'dirección del flujo', ha='center', va='top',
               fontsize=8.5, color='#b03030')
        b.text(0.5, 0.72, note, ha='center', va='bottom', fontsize=8.8)
        b.set_xlim(-0.05, 1.05); b.set_ylim(-0.55, 1.15)

    fig.suptitle('Problema 3.14 — el espaciamiento de las equipotenciales delata '
                 'recarga y descarga', fontsize=10.5, y=1.0)
    fig.tight_layout()
    save(fig, 'fig_3_14_recarga')


# ---------------------------------------------------------------- 3.15
def fig_315():
    fig, ax = plt.subplots(figsize=(9.2, 4.4))
    ax.set_aspect('auto'); ax.axis('off')
    W = 10
    ax.add_patch(Rectangle((0, 2.6), W, 1.4, fc=AQ, ec='k', lw=1.1))
    ax.add_patch(Rectangle((0, 1.5), W, 1.1, fc=CLAY, ec='k', lw=1.1,
                           hatch='xxx'))
    ax.add_patch(Rectangle((0, 0.1), W, 1.4, fc=AQ, ec='k', lw=1.1))
    ax.add_patch(Rectangle((0, -0.25), W, 0.35, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))
    ax.text(W + .15, 3.3, 'acuífero\nSUPERIOR', fontsize=8.5, va='center')
    ax.text(W + .15, 2.05, "ARCILLA  $K'$, $b'$", fontsize=8.5, va='center')
    ax.text(W + .15, 0.8, 'acuífero\nINFERIOR', fontsize=8.5, va='center')

    for x, hs, hi, nm, nar in [(2.2, 70, 60, '$h_4$', 4), (7.6, 30, 25, '$h_1$', 2)]:
        # piezometers
        ax.add_patch(Rectangle((x - .55, 2.6), .22, 2.2, fc=WATER, ec='k', lw=1))
        ax.add_patch(Rectangle((x + .33, 0.6), .22, 4.2, fc=WATER, ec='k', lw=1))
        ax.plot([x - .75, x - .13], [4.8, 4.8], '-', color='#1a4e8a', lw=2)
        hh = 4.8 - (hs - hi) * 0.055
        ax.plot([x + .13, x + .75], [hh, hh], '-', color='#b03030', lw=2)
        ax.text(x - .8, 4.95, f'{hs} m', ha='center', fontsize=9, color='#1a4e8a')
        ax.text(x + .85, hh + .1, f'{hi} m', ha='center', fontsize=9, color='#b03030')
        ax.annotate('', xy=(x + 1.15, hh), xytext=(x + 1.15, 4.8),
                    arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1))
        ax.text(x + 1.25, (hh + 4.8) / 2, f'$\\Delta h = {hs-hi}$ m',
                fontsize=9, va='center', fontweight='bold')
        ax.text(x, 5.3, nm, ha='center', fontsize=12, fontweight='bold')
        # downward leakage arrows
        for k in range(nar):
            xa = x - .3 + k * .35
            ax.annotate('', xy=(xa, 1.45), xytext=(xa, 2.65),
                        arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=2.0))
        ax.text(x, 1.15, f'$q_z = K\'\\,{hs-hi}/b\'$', ha='center', fontsize=8.5,
                color='#b03030')

    ax.annotate('', xy=(6.0, 2.9), xytext=(9.4, 2.9),
                arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=1.6))
    ax.annotate('', xy=(1.0, 2.9), xytext=(4.2, 2.9),
                arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=1.6))
    ax.text(5.0, 3.05, 'flujo horizontal\nde $h_4$ hacia $h_1$', ha='center',
            fontsize=8, color='#1a4e8a')

    ax.text(5, -0.85, 'El flujo vertical es DESCENDENTE en ambas regiones '
                      '(la carga del acuífero superior es mayor).\n'
                      'La velocidad es el DOBLE en $h_4$ porque $\\Delta h$ es el doble '
                      '($K\'$ y $b\'$ son iguales).',
            ha='center', va='top', fontsize=9.2)
    ax.set_xlim(-0.6, 13.0); ax.set_ylim(-2.2, 5.8)
    ax.set_title('Problema 3.15 — fuga vertical a través del acuitardo', fontsize=10)
    save(fig, 'fig_3_15_arcilla')


# ---------------------------------------------------------------- 3.16
def fig_316():
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.set_aspect('auto'); ax.axis('off')
    ax.add_patch(Rectangle((0, 4.0), 11, 1.0, fc=CLAY, ec='k', lw=1.2,
                           hatch='xxx'))
    ax.add_patch(Rectangle((0, 0.4), 11, 3.6, fc=AQ, ec='k', lw=1.2))
    ax.add_patch(Rectangle((0, 5.0), 11, 0.5, fc=SOIL, ec='k', lw=1))
    ax.plot([0, 11], [0.4, 0.4], 'k-', lw=1.4)
    ax.text(0.2, 5.25, 'terreno', fontsize=8)
    ax.text(11.2, 4.5, "capa confinante\n$K' = 10^{-7}$ cm/s", fontsize=8.6,
            va='center')
    ax.text(11.2, 2.2, 'ACUÍFERO', fontsize=8.6, va='center')
    ax.text(5.5, 0.2, 'Datum', ha='center', va='top', fontsize=8.5)

    # piezometer 1: shallow, in upper unit -> head 100
    ax.add_patch(Rectangle((2.9, 4.1), .22, 1.9, fc=WATER, ec='k', lw=1))
    ax.plot([2.6, 3.4], [6.0, 6.0], '-', color='#1a4e8a', lw=2.2)
    ax.text(3.0, 6.15, '100 m', ha='center', fontsize=9.5, color='#1a4e8a',
            fontweight='bold')
    # piezometer 2: deep, in aquifer -> head 95
    ax.add_patch(Rectangle((6.4, 1.2), .22, 4.45, fc=WATER, ec='k', lw=1))
    ax.plot(6.5, 1.2, 'v', ms=7, color='k')
    ax.plot([6.1, 6.9], [5.65, 5.65], '-', color='#b03030', lw=2.2)
    ax.text(7.1, 5.72, '95 m', ha='left', fontsize=9.5, color='#b03030',
            fontweight='bold')

    ax.annotate('', xy=(1.2, 4.0), xytext=(1.2, 5.0),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.1))
    ax.text(1.05, 4.5, "$b' = 10$ m", ha='right', va='center', fontsize=9)
    ax.annotate('', xy=(8.6, 5.65), xytext=(8.6, 6.0),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.1))
    ax.text(8.75, 5.82, '$\\Delta h = 5$ m', fontsize=9, va='center')

    for k in range(7):
        xa = 0.8 + k * 1.45
        ax.annotate('', xy=(xa, 3.95), xytext=(xa, 5.05),
                    arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=1.8))
    ax.text(5.5, -0.35,
            '$i = \\dfrac{100-95}{10} = 0.5$ m/m        '
            '$q = K\'i = 5\\times10^{-8}$ cm/s        DESCENDENTE  '
            '($\\approx 1.6$ cm/año)',
            ha='center', va='top', fontsize=10)
    ax.set_xlim(-0.4, 14.3); ax.set_ylim(-1.6, 6.6)
    ax.set_title('Problema 3.16 — descarga específica a través de la capa confinante',
                 fontsize=10)
    save(fig, 'fig_3_16_confinante')


# ---------------------------------------------------------------- 3.17
def fig_317():
    fig = plt.figure(figsize=(9.4, 7.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.15, 1], hspace=0.38)

    # --- top: block diagram with balance
    ax = fig.add_subplot(gs[0]); ax.set_aspect('auto'); ax.axis('off')
    W, dx, dy = 10.0, 1.5, 0.95
    def blk(y0, h, fc, lab):
        ax.add_patch(Polygon([(0, y0), (W, y0), (W, y0 + h), (0, y0 + h)],
                             fc=fc, ec='k', lw=1.2))
        ax.add_patch(Polygon([(W, y0), (W + dx, y0 + dy), (W + dx, y0 + dy + h),
                              (W, y0 + h)], fc=fc, ec='k', lw=1.0, alpha=.65))
        ax.add_patch(Polygon([(0, y0 + h), (W, y0 + h), (W + dx, y0 + h + dy),
                              (dx, y0 + h + dy)], fc=fc, ec='k', lw=1.0, alpha=.45))
        ax.text(W + dx + .25, y0 + h / 2 + dy / 2, lab, fontsize=8.6, va='center')
    blk(0.0, 1.0, AQ,  'acuífero INFERIOR\n10 m')
    blk(1.0, 2.0, CLAY, "capa confinante  20 m\n$K' = 10^{-9}$ m/s")
    blk(3.0, 1.0, AQ,  'acuífero SUPERIOR\n10 m')

    ax.annotate('', xy=(0, -0.6), xytext=(W, -0.6),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
    ax.text(W / 2, -0.75, '1000 m  (dirección del flujo)', ha='center', va='top',
            fontsize=8.5)
    ax.annotate('', xy=(W + .1, 4.1), xytext=(W + dx + .1, 4.1 + dy),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9))
    ax.text(W + dx / 2 + .55, 4.75, '100 m (ancho)', fontsize=8.5)

    for y, lab in [(0.5, ''), (3.5, '')]:
        ax.annotate('', xy=(0.9, y), xytext=(-1.5, y),
                    arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=2.6))
        ax.text(-1.6, y, '$Q_{in}=1\\times10^{-4}$\nm$^3$/s\n($i=0.1$)', ha='right',
                va='center', fontsize=8.2, color='#1a4e8a')
    ax.annotate('', xy=(W + 2.9, 3.5), xytext=(W + 1.8, 3.5),
                arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=3.2))
    ax.text(W + 3.05, 3.5, '$1.5\\times10^{-4}$\n($i=0.15$)', fontsize=8.2,
            va='center', color='#b03030')
    ax.annotate('', xy=(W + 2.6, 0.5), xytext=(W + 1.8, 0.5),
                arrowprops=dict(arrowstyle='-|>', color='#b03030', lw=1.6))
    ax.text(W + 3.05, 0.5, '$5\\times10^{-5}$\n($i=0.05$)', fontsize=8.2,
            va='center', color='#b03030')
    for k in range(7):
        xa = 0.9 + k * 1.3
        ax.annotate('', xy=(xa, 3.0), xytext=(xa, 1.0),
                    arrowprops=dict(arrowstyle='-|>', color='#2b8a3e', lw=1.7))
    ax.text(W / 2, 1.95, 'FUGA ASCENDENTE\n$Q = 5\\times10^{-5}$ m$^3$/s\n'
                         "$q=K'\\,10/20 = 5\\times10^{-10}$ m/s",
            ha='center', va='center', fontsize=8.4, color='#1b5e20',
            bbox=dict(fc='white', ec='#2b8a3e', lw=.8, alpha=.9, pad=2))
    ax.set_xlim(-4.6, 16.6); ax.set_ylim(-1.9, 5.4)
    ax.set_title('Problema 3.17 — balance de masa en dos acuíferos acoplados por fuga',
                 fontsize=10)

    # --- bottom: piezometric surfaces (integrated from gradients)
    ax2 = fig.add_subplot(gs[1])
    x = np.linspace(0, 1000, 400)
    # gradient varies linearly with Q, which varies linearly with x
    i_up = 0.10 + 0.05 * x / 1000
    i_lo = 0.10 - 0.05 * x / 1000
    h_up = 100 - np.cumsum(i_up) * (x[1] - x[0])
    h_lo = 110 - np.cumsum(i_lo) * (x[1] - x[0])
    ax2.plot(x, h_lo, '-', color='#b03030', lw=2.3, label='acuífero INFERIOR (cede agua: se APLANA, $i$: 0.10$\\to$0.05)')
    ax2.plot(x, h_up, '-', color='#1a4e8a', lw=2.3, label='acuífero SUPERIOR (recibe agua: se EMPINA, $i$: 0.10$\\to$0.15)')
    ax2.fill_between(x, h_up, h_lo, color='#2b8a3e', alpha=.13)
    for xa in np.linspace(60, 940, 9):
        ya_u = np.interp(xa, x, h_up); ya_l = np.interp(xa, x, h_lo)
        ax2.annotate('', xy=(xa, ya_u), xytext=(xa, ya_l),
                     arrowprops=dict(arrowstyle='-|>', color='#2b8a3e', lw=1.2))
    ax2.text(500, (np.interp(500, x, h_up) + np.interp(500, x, h_lo)) / 2,
             'fuga ascendente\n($\\Delta h$ decrece aguas abajo)', ha='center',
             va='center', fontsize=8.3, color='#1b5e20',
             bbox=dict(fc='white', ec='none', alpha=.85, pad=1))
    ax2.set_xlabel('distancia en la dirección del flujo (m)', fontsize=9)
    ax2.set_ylabel('carga hidráulica (m)', fontsize=9)
    ax2.legend(fontsize=8.0, loc='lower left', framealpha=.95)
    ax2.grid(alpha=.3, lw=.6)
    ax2.tick_params(labelsize=8)
    ax2.set_title('Inciso (d) — forma de las superficies piezométricas', fontsize=9.5)
    save(fig, 'fig_3_17_sistema')


for f in (fig_306, fig_307, fig_309, fig_311, fig_313, fig_314, fig_315,
          fig_316, fig_317):
    f()
print('cap3 ok')

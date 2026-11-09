import os
os.environ['MPLCONFIGDIR'] = '/tmp/mplcfg'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, atan2, cos, sin, pi
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

OUT = '/projects/sandbox/.calc/fig'
AP = '/projects/sandbox/.calc/apuntes'
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans',
                     'axes.linewidth': .8, 'savefig.dpi': 200,
                     'savefig.bbox': 'tight', 'savefig.pad_inches': .15})
AQ, CLAY, WATER, SOIL, SALT = '#d6e4f0', '#cfc8bd', '#bcd9ef', '#e8e2d8', '#f3cdcd'
CB, CR, CG, CY = '#1a4e8a', '#b03030', '#2b8a3e', '#d9a400'
FONT = os.path.join(os.path.dirname(matplotlib.__file__),
                    'mpl-data/fonts/ttf/DejaVuSans-Bold.ttf')
YEAR = 365.25


def save(f, n):
    f.savefig(f'{OUT}/{n}.png', facecolor='white'); plt.close(f); print('  ->', n)


# ===================================================== C1: Dupuit con recarga
def dupuit_h(x, h1, h2, L, W, K):
    return np.sqrt(h1**2 - (h1**2 - h2**2) * x / L + (W / K) * (L - x) * x)


def fig_dupuit():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.4))
    # --- ejemplo de clase
    K, h1, h2, L = 10.0, 15.0, 18.0, 200.0
    x = np.linspace(0, L, 300)
    for Wmm, c, ls, lab in [(-60, CR, '--', 'W = -60 mm/año (evaporación)'),
                            (0, '#777', ':', 'W = 0'),
                            (20, CB, '-', 'W = +20 mm/año (recarga)')]:
        ax.plot(x, dupuit_h(x, h1, h2, L, Wmm / 1000 / YEAR, K), ls,
                color=c, lw=2.0, label=lab)
    ax.fill_between(x, 0, dupuit_h(x, h1, h2, L, 20 / 1000 / YEAR, K),
                    color=AQ, alpha=.6, zorder=0)
    for xx in (0, L):
        ax.add_patch(Rectangle((xx - 8 if xx else -8, 0), 8, h1 if xx == 0 else h2,
                               fc=WATER, ec=CB, lw=1, zorder=1))
    for xa in (150, 100, 50):
        ax.annotate('', xy=(xa - 28, 7), xytext=(xa, 7),
                    arrowprops=dict(arrowstyle='-|>', color=CB, lw=1.8))
    ax.text(100, 8.4, "q' ≈ -2.47 m²/día (hacia x = 0)", ha='center',
            fontsize=8.6, color='#13335c')
    ax.text(4, 15.25, '$h_1$=15 m', fontsize=8.6)
    ax.text(196, 18.25, '$h_2$=18 m', fontsize=8.6, ha='right')
    ax.set_xlim(-12, 212); ax.set_ylim(0, 20)
    ax.set_xlabel('x (m)'); ax.set_ylabel('h (m sobre la base)')
    ax.legend(fontsize=7.6, loc='lower right', framealpha=.95)
    ax.grid(alpha=.3, lw=.5); ax.tick_params(labelsize=8)
    ax.set_title('Ejemplo de clase: las tres curvas casi coinciden.\n'
                 'Domina la diferencia de carga: NO hay divisoria', fontsize=9.4)

    # --- variante con divisoria
    K, h1, h2, L, W = 1.0, 20.0, 18.0, 1000.0, 200 / 1000 / YEAR
    x = np.linspace(0, L, 400)
    h = dupuit_h(x, h1, h2, L, W, K)
    d = L / 2 - (K / W) * (h1**2 - h2**2) / (2 * L)
    hm = dupuit_h(d, h1, h2, L, W, K)
    ax2.fill_between(x, 0, h, color=AQ, alpha=.7)
    ax2.plot(x, h, '-', color=CB, lw=2.2)
    ax2.plot(x, h1 - (h1 - h2) * x / L, ':', color='#888', lw=1.3)
    ax2.axvline(d, color=CG, lw=1.6, ls='--')
    ax2.plot([d], [hm], 'o', ms=8, mfc='white', mec=CG, mew=2)
    ax2.annotate(f'divisoria  d = {d:.0f} m\n$h_{{max}}$ = {hm:.2f} m',
                 xy=(d, hm), xytext=(d + 120, hm + 1.2), fontsize=8.6,
                 color='#1b5e20',
                 arrowprops=dict(arrowstyle='-|>', color='#1b5e20', lw=1.1))
    for xa in np.linspace(60, 940, 9):
        ax2.annotate('', xy=(xa, dupuit_h(xa, h1, h2, L, W, K) - 0.1),
                     xytext=(xa, 24.3),
                     arrowprops=dict(arrowstyle='-|>', color=CG, lw=1.0))
    ax2.text(500, 24.6, 'recarga W = 200 mm/año', ha='center', fontsize=8.4,
             color='#1b5e20')
    ax2.annotate('', xy=(80, 9), xytext=(330, 9),
                 arrowprops=dict(arrowstyle='-|>', color=CB, lw=2))
    ax2.annotate('', xy=(920, 9), xytext=(560, 9),
                 arrowprops=dict(arrowstyle='-|>', color=CB, lw=2))
    ax2.text(200, 10, "q'(0) = -0.236", ha='center', fontsize=8.4, color=CB)
    ax2.text(740, 10, "q'(L) = +0.312", ha='center', fontsize=8.4, color=CB)
    ax2.text(500, 4, 'suma de salidas 0.548 = W L  (balance cerrado)',
             ha='center', fontsize=8.3,
             bbox=dict(fc='white', ec='#999', lw=.7, pad=2))
    ax2.set_xlim(0, L); ax2.set_ylim(0, 26)
    ax2.set_xlabel('x (m)'); ax2.set_ylabel('h (m sobre la base)')
    ax2.grid(alpha=.3, lw=.5); ax2.tick_params(labelsize=8)
    ax2.set_title('Variante: domina la recarga. Se forma un\n'
                  'montículo y el agua sale por los dos bordes', fontsize=9.4)
    fig.suptitle('Dupuit-Forchheimer con recarga uniforme', fontsize=10.6, y=1.03)
    save(fig, 'fig_c1_dupuit')


# ===================================================== C2: costa y cambio climatico
def fig_costa():
    rf, rs = 1.000, 1.025
    G = (rs - rf) / rf
    K = 1e-4
    W = 0.5 / (YEAR * 86400)
    C = rs * (rs - rf) * K / (rf**2 * W)

    def H(x, L, s):
        return np.sqrt((W / K) * (L**2 - x**2) + (rs / rf) * s**2)

    cases = [(1000.0, 30.0, 0.0, CB, 'antes'), (967.0, 30.6, 0.6, CR, 'después')]
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.6, 7.4),
                                  gridspec_kw=dict(height_ratios=[1.25, 1]))
    ax.add_patch(Rectangle((0, -34), 1100, 4, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))
    ax.text(30, -33.2, 'base del acuífero (fija, -30 m respecto al nivel del mar inicial)',
            fontsize=7.8, color='white')
    for L, s, sea, c, lab in cases:
        xT = sqrt(L**2 - C * s**2)
        x = np.linspace(0, L, 400)
        wt = H(x, L, s) - 30.0            # elevacion del nivel freatico, datum fijo
        ax.plot(x, wt * 8, '-', color=c, lw=2.0,
                label=f'nivel freático {lab} (×8 en vertical)')
        xi = np.linspace(xT, L, 200)
        hf = H(xi, L, s) - s
        zi = sea - hf / G
        ax.plot(xi, zi, '-', color=c, lw=2.4, ls='-' if lab == 'antes' else '--',
                label=f'interfaz {lab}')
        ax.plot([xT], [-30], 'o', ms=8, mfc='white', mec=c, mew=2, zorder=6)
        ax.annotate(f'punta {lab}\n$x_T$ = {xT:.1f} m', xy=(xT, -30),
                    xytext=(xT - (230 if lab == 'antes' else 380), -22),
                    fontsize=8.4, color=c,
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1))
        ax.axvline(L, color=c, lw=1.0, ls=':')
    ax.fill_between([0, 1100], -30, 0, color=AQ, alpha=.45, zorder=0)
    ax.axhline(0, color=CB, lw=1, ls='-.')
    ax.axhline(0.6, color=CR, lw=1, ls='-.')
    ax.text(1095, 1.2, 'mar +0.6 m', ha='right', fontsize=8, color=CR)
    ax.text(1095, -1.9, 'mar inicial', ha='right', fontsize=8, color=CB)
    ax.text(1000, 12, 'costa\ninicial', ha='center', fontsize=8, color=CB)
    ax.text(967, 20, 'costa\nnueva', ha='center', fontsize=8, color=CR)
    ax.text(80, 8, 'divisoria (x = 0)', fontsize=8.2)
    ax.text(870, -12, 'AGUA\nSALADA', fontsize=8.5, color='#8a2020', ha='center')
    ax.text(400, -15, 'AGUA DULCE', fontsize=9.5, color='#13335c')
    ax.set_xlim(0, 1100); ax.set_ylim(-35, 28)
    ax.set_xlabel('x desde la divisoria (m)')
    ax.set_ylabel('elevación (m)')
    ax.legend(fontsize=7.6, loc='upper left', ncol=2, framealpha=.95)
    ax.grid(alpha=.25, lw=.5); ax.tick_params(labelsize=8)
    ax.set_title('Sección del acuífero costero: la costa retrocede 33 m y la '
                 'punta de la cuña se mueve 39.1 m', fontsize=9.8)

    # --- panel inferior: longitud invadida y subida del nivel
    names = ['Punta $x_T$', 'Longitud invadida\n$L - x_T$']
    a = [sqrt(1000**2 - C * 30**2), 1000 - sqrt(1000**2 - C * 30**2)]
    b = [sqrt(967**2 - C * 30.6**2), 967 - sqrt(967**2 - C * 30.6**2)]
    xs = np.arange(2)
    ax2.bar(xs - .18, a, .34, color=CB, ec='k', lw=.7, label='antes')
    ax2.bar(xs + .18, b, .34, color=CR, ec='k', lw=.7, label='después')
    for i in range(2):
        ax2.text(i - .18, a[i] + 15, f'{a[i]:.1f}', ha='center', fontsize=8.6)
        ax2.text(i + .18, b[i] + 15, f'{b[i]:.1f}', ha='center', fontsize=8.6)
    ax2.set_xticks(xs); ax2.set_xticklabels(names, fontsize=9)
    ax2.set_ylabel('m'); ax2.set_ylim(0, 1100)
    ax2.legend(fontsize=8.4, loc='upper right')
    ax2.grid(axis='y', alpha=.3, lw=.5); ax2.tick_params(labelsize=8)
    ax2.text(1.0, 520, 'la punta se mueve -39.1 m,\npero 33 m son la costa que retrocede:\n'
             'la cuña avanza de verdad sólo +6.1 m', ha='center', fontsize=8.6,
             bbox=dict(fc='#fff8f0', ec=CR, lw=.9, pad=3))
    ax2.set_title('Dos lecturas del mismo resultado', fontsize=9.6)
    fig.tight_layout()
    save(fig, 'fig_c2_costa')


# ===================================================== C3: rios ganadores/perdedores
def fig_rios():
    fig, axs = plt.subplots(2, 2, figsize=(9.6, 6.6),
                            gridspec_kw=dict(height_ratios=[1, 1.05]))
    x = np.linspace(-10, 10, 400)
    ground = 6 + 0.035 * x**2 * 1.4
    for col, kind in enumerate(['ganador', 'perdedor']):
        ax = axs[0, col]; ax.axis('off')
        g = np.where(np.abs(x) < 1.6, 4.6, ground)
        ax.fill_between(x, 0, g, color=SOIL)
        if kind == 'ganador':
            wt = 3.4 + 0.11 * x**2
            wt = np.minimum(wt, g - 0.3)
            wt = np.where(np.abs(x) < 1.6, 4.6, wt)
        else:
            wt = 1.6 + 0.02 * x**2
        ax.fill_between(x, 0, wt, color=AQ)
        ax.plot(x, g, '-', color='#4a7c2f', lw=1.6)
        ax.plot(x, wt, '-', color=CB, lw=2)
        ax.add_patch(Rectangle((-1.6, 4.0), 3.2, 0.6, fc=WATER, ec=CB, lw=1, zorder=5))
        ax.text(0, 5.0, 'río', ha='center', fontsize=8.6, zorder=6)
        if kind == 'ganador':
            for xs in (-7, -4.5, 4.5, 7):
                ax.annotate('', xy=(np.sign(-xs) * 1.4 + 0 * xs, 3.9),
                            xytext=(xs, 2.6 + 0.08 * xs**2),
                            arrowprops=dict(arrowstyle='-|>', color=CB, lw=1.6,
                                            connectionstyle='arc3,rad=-0.25'
                                            if xs < 0 else 'arc3,rad=0.25'))
            ax.set_title('GANADOR: el nivel freático está por encima del río\n'
                         'el acuífero DESCARGA hacia el río', fontsize=9.3,
                         color='#13335c')
        else:
            for xs in (-1.0, 0, 1.0):
                ax.annotate('', xy=(xs * 3.5, 1.2), xytext=(xs, 3.9),
                            arrowprops=dict(arrowstyle='-|>', color=CR, lw=1.6))
            ax.text(5.6, 2.2, 'zona no\nsaturada', fontsize=8, color='#7a5a2a')
            ax.set_title('PERDEDOR: el río está por encima del nivel freático\n'
                         'el río RECARGA al acuífero', fontsize=9.3, color='#8a2020')
        ax.set_xlim(-10.5, 10.5); ax.set_ylim(0, 10)

        # --- vista en planta: las curvas forman V
        ax = axs[1, col]; ax.set_aspect('equal')
        ys = np.linspace(-5, 5, 200)
        ax.plot(0 * ys, ys, '-.', color=CB, lw=2)
        ax.annotate('', xy=(0, 5.2), xytext=(0, 3.6),
                    arrowprops=dict(arrowstyle='-|>', color=CB, lw=2))
        ax.text(0.3, 4.6, 'sentido\ndel río', fontsize=8, color=CB)
        for k, hv in enumerate([10, 11, 12, 13]):
            y0 = -3 + 1.8 * k
            xx = np.linspace(-5, 5, 200)
            if kind == 'ganador':
                yy = y0 - 1.6 * np.exp(-xx**2 / 1.5) + 0.25 * np.abs(xx)
            else:
                yy = y0 + 1.6 * np.exp(-xx**2 / 1.5) - 0.25 * np.abs(xx)
            yy = yy if kind == 'ganador' else yy
            ax.plot(xx, yy, '-', color='#333', lw=1.3)
            ax.text(4.6, yy[-1] + 0.15, f'{hv if kind=="ganador" else 23-hv} m',
                    fontsize=7.8)
        ax.set_xlim(-5.5, 6.2); ax.set_ylim(-6, 6.5); ax.axis('off')
        if kind == 'ganador':
            ax.set_title('Planta: la V apunta AGUAS ARRIBA', fontsize=9.3)
        else:
            ax.set_title('Planta: la V apunta AGUAS ABAJO', fontsize=9.3)
    fig.suptitle('Taller en clase: ríos ganadores y perdedores', fontsize=10.6,
                 y=1.0)
    fig.tight_layout()
    save(fig, 'fig_c3_rios')


# ===================================================== C4: artesiano y goteo
def fig_artesiano():
    fig, ax = plt.subplots(figsize=(9.4, 4.6)); ax.axis('off')
    x = np.linspace(0, 10, 200)
    top = 6.2 - 0.30 * x
    ax.fill_between(x, top - 1.6, top, color=AQ, ec='none')          # acuifero
    ax.fill_between(x, top, top + 0.7, color=CLAY, ec='none', hatch='xx')  # confinante
    ax.fill_between(x, top - 2.4, top - 1.6, color='#9a9a9a', hatch='///')
    ground = np.maximum(top + 0.7, 5.6 - 0.18 * x)
    ground = np.where(x < 1.5, top + 0.7, ground)
    ax.fill_between(x, top + 0.7, ground, color=SOIL)
    ax.plot(x, ground, '-', color='#4a7c2f', lw=1.6)
    ax.plot(x, top, 'k-', lw=1); ax.plot(x, top - 1.6, 'k-', lw=1)
    pot = 6.3 - 0.07 * x
    ax.plot(x, pot, '--', color=CB, lw=1.8)
    ax.text(7.6, pot[-1] + 0.25 + 0.07 * 2.4, 'superficie potenciométrica',
            fontsize=8.6, color=CB)
    for xa in (0.3, 0.7, 1.1):
        ax.annotate('', xy=(xa, 4.9 - 0.3 * xa), xytext=(xa, 7.2),
                    arrowprops=dict(arrowstyle='-|>', color=CG, lw=1.5))
    ax.text(0.7, 7.35, 'RECARGA\n(afloramiento)', ha='center', fontsize=8.4,
            color='#1b5e20')
    # pozo surgente
    xw = 7.5; tw = 6.2 - 0.30 * xw
    ax.add_patch(Rectangle((xw - .07, tw - 1.0), .14, (5.6 - 0.18 * xw) - tw + 1.6,
                           fc='white', ec='k', lw=1.2, zorder=5))
    gw = 5.6 - 0.18 * xw
    ax.annotate('', xy=(xw, gw + 0.95), xytext=(xw, gw + 0.05),
                arrowprops=dict(arrowstyle='-|>', color=CB, lw=2.4), zorder=6)
    ax.text(xw + 0.15, gw + 0.6, 'AGUA SALTA\n(pozo surgente)', fontsize=8.6,
            color=CB, fontweight='bold')
    # pozo no surgente
    xn = 4.0; tn = 6.2 - 0.30 * xn; gn = max(tn + 0.7, 5.6 - 0.18 * xn)
    ax.add_patch(Rectangle((xn - .07, tn - 1.0), .14, gn - tn + 1.0 + 0.2,
                           fc='white', ec='k', lw=1.2, zorder=5))
    ax.add_patch(Rectangle((xn - .07, tn - 1.0), .14, (6.3 - 0.07 * xn) - tn + 1.0,
                           fc=WATER, ec='none', zorder=6))
    ax.text(xn, gn + 0.45, 'pozo artesiano\nno surgente', ha='center', fontsize=8)
    # goteo
    for xa in (5.4, 6.0):
        ta = 6.2 - 0.30 * xa
        ax.annotate('', xy=(xa, ta + 0.75), xytext=(xa, ta + 0.05),
                    arrowprops=dict(arrowstyle='-|>', color=CR, lw=1.4))
    ax.text(5.7, 6.2 - 0.30 * 5.7 + 0.95, 'GOTEO', ha='center', fontsize=8.4,
            color=CR, fontweight='bold')
    ax.text(2.6, 6.2 - 0.30 * 2.6 - 0.85, 'ACUÍFERO CONFINADO  ($S = S_s b$)',
            fontsize=8.6, rotation=-9.5)
    ax.text(3.0, 6.2 - 0.30 * 3.0 + 0.32, 'capa confinante', fontsize=7.8,
            rotation=-9.5)
    ax.text(9.95, 1.3, 'Si la superficie potenciométrica queda por encima del terreno,\n'
            'el pozo descarga solo, sin bomba.', ha='right', fontsize=8.4,
            bbox=dict(fc='white', ec='#999', lw=.7, pad=3))
    ax.set_xlim(-0.2, 10.2); ax.set_ylim(0.9, 8.2)
    ax.set_title('Página 1 de tus apuntes: acuífero confinado, recarga, goteo y '
                 '"agua salta"', fontsize=10.2)
    save(fig, 'fig_c4_artesiano')


# ===================================================== C5: figura 7.39 resuelta
def arrow_path(d, pts, color, width=7):
    d.line(pts, fill=color, width=width, joint='curve')
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = atan2(y2 - y1, x2 - x1); L = 30
    p = [(x2, y2),
         (x2 - L * cos(a - 0.45), y2 - L * sin(a - 0.45)),
         (x2 - L * cos(a + 0.45), y2 - L * sin(a + 0.45))]
    d.polygon(p, fill=color)


def smooth(pts, n=12):
    pts = np.array(pts, float)
    t = np.linspace(0, 1, len(pts))
    tt = np.linspace(0, 1, (len(pts) - 1) * n + 1)
    xs = np.interp(tt, t, pts[:, 0]); ys = np.interp(tt, t, pts[:, 1])
    k = 7
    xs = np.convolve(np.pad(xs, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    ys = np.convolve(np.pad(ys, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    xs[0], ys[0] = pts[0]; xs[-1], ys[-1] = pts[-1]
    return list(zip(xs, ys))


def fig_739():
    im = Image.open(f'{AP}/p07_full.png').convert('RGB')
    im = im.crop((420, 20, 2943, 842))
    off = (420, 20)
    d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(FONT, 44)
    fs = ImageFont.truetype(FONT, 25)

    def P(x, y):
        return (x - off[0], y - off[1])

    paths = {
        'X': [(835, 228), (848, 330), (875, 430), (915, 525), (965, 610),
              (1030, 680), (1105, 712), (1165, 680), (1192, 600), (1200, 525)],
        'Y': [(1450, 278), (1442, 370), (1420, 470), (1382, 560), (1325, 628),
              (1262, 622), (1222, 565), (1206, 522)],
        'Z': [(2715, 265), (2724, 380), (2718, 520), (2690, 660), (2622, 760),
              (2522, 800), (2420, 802), (2322, 782), (2232, 742), (2165, 708)],
    }
    for k, pts in paths.items():
        arrow_path(d, [P(*p) for p in smooth(pts)], (190, 30, 30), 7)
        x0, y0 = P(*pts[0])
        dx = -330 if k == 'Z' else 14
        d.text((x0 + dx, y0 - 52), f'línea de flujo desde {k}', fill=(190, 30, 30),
               font=fs)
    for (x, y), lab in [((1650, 120), 'R'), ((2755, 150), 'R'), ((850, 120), 'R')]:
        X, Y = P(x, y)
        d.ellipse([X - 34, Y - 34, X + 34, Y + 34], outline=(30, 120, 50), width=6,
                  fill=(225, 245, 228))
        d.text((X - 15, Y - 26), lab, fill=(30, 120, 50), font=fb)
    for (x, y), lab in [((1195, 445), 'D'), ((2080, 440), 'D')]:
        X, Y = P(x, y)
        d.ellipse([X - 34, Y - 34, X + 34, Y + 34], outline=(170, 70, 0), width=6,
                  fill=(255, 238, 220))
        d.text((X - 16, Y - 26), lab, fill=(170, 70, 0), font=fb)
    tags = {'A': ((945, 268), 'A: h≈12.5'), 'B': ((1190, 715), 'B: h≈2.5'),
            'C': ((2125, 703), 'C: h=5'), 'D': ((2363, 767), 'D: h≈8'),
            'E': ((2408, 503), 'E: h=5'), 'F': ((2632, 672), 'F: h≈12.5')}
    for k, ((x, y), txt) in tags.items():
        X, Y = P(x, y)
        d.ellipse([X - 13, Y - 13, X + 13, Y + 13], outline=(26, 78, 138), width=5)
        dx = {'C': -80, 'D': 22}.get(k, 22)
        dy = {'A': -40, 'E': -40, 'C': 46, 'D': 22}.get(k, 18)
        d.rectangle([X + dx - 4, Y + dy - 2, X + dx + len(txt) * 15 + 4, Y + dy + 30],
                    fill=(255, 255, 255), outline=(26, 78, 138), width=2)
        d.text((X + dx, Y + dy), txt, fill=(26, 78, 138), font=fs)
    im.save(f'{OUT}/fig_c5_fig739.png')
    print('  -> fig_c5_fig739')


# ===================================================== C6: mapa 3.31 anotado
def fig_331():
    im = Image.open(f'{AP}/p06_fig.png').convert('RGB')
    d = ImageDraw.Draw(im)
    fs = ImageFont.truetype(FONT, 34)
    s = 1 / 0.6

    def P(x, y):
        return (x * s, y * s)

    def darrow(p1, p2, col, w=7):
        d.line([p1, p2], fill=col, width=w)
        for (a, b) in ((p1, p2), (p2, p1)):
            ang = atan2(b[1] - a[1], b[0] - a[0]); L = 26
            d.polygon([b, (b[0] - L * cos(ang - .5), b[1] - L * sin(ang - .5)),
                       (b[0] - L * cos(ang + .5), b[1] - L * sin(ang + .5))], fill=col)

    # maximo gradiente (17-18 m, junto a la salida del rio)
    darrow(P(606, 86), P(614, 118), (200, 30, 30))
    X, Y = P(640, 92)
    d.rectangle([X + 40, Y - 10, X + 520, Y + 80], fill=(255, 245, 245),
                outline=(200, 30, 30), width=3)
    d.text((X + 52, Y - 4), 'MÁXIMO: 4 mm ≈ 100 m', fill=(200, 30, 30), font=fs)
    d.text((X + 52, Y + 38), 'i ≈ 1/100 = 0.010', fill=(200, 30, 30), font=fs)
    # minimo gradiente (22-23 m, al sur)
    darrow(P(640, 414), P(640, 628), (30, 110, 50))
    X, Y = P(660, 520)
    d.rectangle([X + 10, Y - 10, X + 500, Y + 80], fill=(240, 252, 242),
                outline=(30, 110, 50), width=3)
    d.text((X + 22, Y - 4), 'MÍNIMO: 25 mm ≈ 630 m', fill=(30, 110, 50), font=fs)
    d.text((X + 22, Y + 38), 'i ≈ 1/630 = 0.0016', fill=(30, 110, 50), font=fs)
    # pozo interpolado
    darrow(P(472, 430), P(472, 640), (26, 78, 138), 5)
    X, Y = P(472, 540)
    d.ellipse([X - 20, Y - 20, X + 20, Y + 20], outline=(26, 78, 138), width=6)
    d.rectangle([X - 470, Y - 30, X - 40, Y + 50], fill=(245, 248, 255),
                outline=(26, 78, 138), width=3)
    d.text((X - 460, Y - 24), 'h = 22 + 13/25', fill=(26, 78, 138), font=fs)
    d.text((X - 460, Y + 10), '   = 22.5 m', fill=(26, 78, 138), font=fs)
    im = im.resize((int(im.size[0] * .6), int(im.size[1] * .6)))
    im.save(f'{OUT}/fig_c6_mapa331.png')
    print('  -> fig_c6_mapa331')


fig_dupuit(); fig_costa(); fig_rios(); fig_artesiano(); fig_739(); fig_331()
print('figuras de apuntes ok')

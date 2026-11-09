import os
os.environ['MPLCONFIGDIR'] = '/tmp/mplcfg'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import pi, log10, sqrt
from matplotlib.patches import Rectangle, FancyBboxPatch
import sys
sys.path.insert(0, '/projects/sandbox/.calc')
from pumping_lib import W

OUT = '/projects/sandbox/.calc/fig'
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans',
                     'axes.linewidth': .8, 'savefig.dpi': 200,
                     'savefig.bbox': 'tight', 'savefig.pad_inches': .15})
CB, CR, CG, CY = '#1a4e8a', '#b03030', '#2b8a3e', '#d9a400'


def save(f, n):
    f.savefig(f'{OUT}/{n}.png', facecolor='white'); plt.close(f); print('  ->', n)


# ============================================== G1: anatomia de un ciclo
def g1():
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.6, 4.6),
                                  gridspec_kw=dict(height_ratios=[1, 1.15]))
    # --- escala lineal
    ax.set_xlim(0, 1); ax.set_ylim(-1, 1); ax.axis('off')
    ax.plot([0, 1], [0, 0], '-k', lw=1.6)
    for v in range(1, 11):
        x = (v - 1) / 9
        ax.plot([x, x], [0, .22], '-k', lw=1.3)
        ax.text(x, .30, str(v), ha='center', fontsize=9)
    ax.text(-0.02, 0, 'ESCALA\nLINEAL', ha='right', va='center', fontsize=9,
            fontweight='bold')
    ax.text(.5, -.62, 'divisiones IGUALES: la distancia de 1 a 2 es la misma '
                      'que de 9 a 10', ha='center', fontsize=8.8, color='#555')

    # --- escala logaritmica
    ax2.set_xlim(0, 1); ax2.set_ylim(-1.5, 1.2); ax2.axis('off')
    ax2.plot([0, 1], [0, 0], '-k', lw=1.6)
    for v in range(1, 11):
        x = log10(v)
        ax2.plot([x, x], [0, .24], '-k', lw=1.5)
        ax2.text(x, .33, str(v), ha='center', fontsize=9.5, fontweight='bold')
        if v < 10:
            ax2.text(x, -.30, f'{100*log10(v):.0f} %', ha='center', fontsize=7.4,
                     color=CB)
    # subdivisiones
    for v in np.arange(1.1, 10, .1):
        x = log10(v)
        ax2.plot([x, x], [0, .11], '-', color='#888', lw=.6)
    ax2.text(-0.02, 0, 'ESCALA\nLOGARÍTMICA', ha='right', va='center',
             fontsize=9, fontweight='bold', color=CB)
    # resaltar 1->2 y 5->10
    ax2.annotate('', xy=(log10(2), -.62), xytext=(0, -.62),
                 arrowprops=dict(arrowstyle='<|-|>', color=CR, lw=1.6))
    ax2.text(log10(2) / 2, -.78, 'de 1 a 2\n= 30 % del ciclo', ha='center',
             va='top', fontsize=8.2, color=CR)
    ax2.annotate('', xy=(1, -.62), xytext=(log10(5), -.62),
                 arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=1.6))
    ax2.text((log10(5) + 1) / 2, -.78, 'de 5 a 10\n= 30 % del ciclo',
             ha='center', va='top', fontsize=8.2, color='#1b5e20')
    ax2.text(.5, 1.0, 'UN CICLO LOGARÍTMICO  (×10)', ha='center', fontsize=10,
             fontweight='bold', color=CB)
    ax2.annotate('', xy=(1, .80), xytext=(0, .80),
                 arrowprops=dict(arrowstyle='<|-|>', color=CB, lw=1.4))
    fig.suptitle('Anatomía de la escala logarítmica: la posición de un número '
                 'es su logaritmo', fontsize=10.6, y=1.02)
    save(fig, 'fig_g1_escala')


# ============================================== G2: lineal vs semilog
def g2():
    Q, r, T, S = 1500., 50., 300., 1e-3
    tm = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60, 90, 120,
                   180, 240, 360, 480, 720, 1080, 1440], float)
    s = Q / (4 * pi * T) * W(r ** 2 * S / (4 * T * tm / 1440))
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2))
    ax.plot(tm, s, 'o-', color=CB, ms=5, lw=1.4)
    ax.set_xlabel('$t$ (min) — escala LINEAL', fontsize=9.5)
    ax.set_ylabel('$s$ (m)', fontsize=9.5)
    ax.grid(alpha=.3, lw=.5); ax.tick_params(labelsize=8)
    ax.set_title('Escala lineal: curva. No se puede\nmedir ninguna pendiente útil',
                 fontsize=9.6, color=CR)
    ax.text(.5, .12, 'los primeros 11 puntos\nse apelotonan aquí',
            transform=ax.transAxes, fontsize=8.3, color=CR, ha='center')
    ax.annotate('', xy=(.06, .32), xytext=(.40, .20),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='-|>', color=CR, lw=1.2))

    ax2.semilogx(tm, s, 'o', color=CB, ms=6, mfc='white', mew=1.6)
    val = (r ** 2 * S / (4 * T * tm / 1440)) < 0.01
    A = np.polyfit(np.log10(tm[val] / 1440), s[val], 1)
    tl = np.logspace(log10(3), log10(2500), 100)
    ax2.semilogx(tl, np.polyval(A, np.log10(tl / 1440)), '-', color=CR, lw=2)
    ax2.set_xlabel('$t$ (min) — escala LOGARÍTMICA', fontsize=9.5)
    ax2.set_ylabel('$s$ (m)', fontsize=9.5)
    ax2.grid(which='both', alpha=.3, lw=.5); ax2.tick_params(labelsize=8)
    ax2.set_title('Semilogarítmica: RECTA.\nLa pendiente da $T$ y el corte da $S$',
                  fontsize=9.6, color=CG)
    ax2.set_ylim(-.1, 2.5)
    fig.suptitle('Por qué se usa papel semilogarítmico: convierte la curva de '
                 'Theis en una recta', fontsize=10.5, y=1.03)
    save(fig, 'fig_g2_lineal_vs_log')


# ============================================== G3: como leer la recta
def g3():
    Q, r, T, S = 1500., 50., 300., 1e-3
    tm = np.array([30, 60, 120, 240, 480, 720, 1080, 1440], float)
    s = Q / (4 * pi * T) * W(r ** 2 * S / (4 * T * tm / 1440))
    A = np.polyfit(np.log10(tm[-5:] / 1440), s[-5:], 1)
    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    ax.semilogx(tm, s, 'o', ms=8, mfc='white', mec=CB, mew=2, zorder=5)
    tl = np.logspace(log10(1), log10(3000), 200)
    ax.semilogx(tl, np.polyval(A, np.log10(tl / 1440)), '-', color=CR, lw=2.2)
    ax.axhline(0, color='k', lw=1.2)
    ds = A[0]; t0 = 10 ** (-A[1] / A[0]) * 1440

    # paso 1
    ax.text(1.25, 2.28, 'PASO 1\nTraza la recta por los\npuntos de tiempo tardío',
            fontsize=8.8, color=CR, va='top',
            bbox=dict(fc='#fdf0f0', ec=CR, lw=1, pad=3))
    # paso 2: delta s
    ta, tb = 100., 1000.
    sa, sb = np.polyval(A, log10(ta / 1440)), np.polyval(A, log10(tb / 1440))
    ax.plot([ta, tb], [sa, sa], '--', color=CG, lw=1.5)
    ax.plot([ta, ta], [0, sa], ':', color='#aaa', lw=1)
    ax.plot([tb, tb], [0, sb], ':', color='#aaa', lw=1)
    ax.annotate('', xy=(tb, sb), xytext=(tb, sa),
                arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=2.2))
    ax.text(tb * 1.15, (sa + sb) / 2, f'PASO 2\n$\\Delta s$ = {ds:.2f} m',
            fontsize=9.2, color='#1b5e20', va='center', fontweight='bold',
            bbox=dict(fc='#f1f8f2', ec=CG, lw=1, pad=3))
    ax.annotate('', xy=(tb, -0.14), xytext=(ta, -0.14),
                arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=1.4))
    ax.text(sqrt(ta * tb), -0.20, 'UN ciclo completo (100 → 1000)', ha='center',
            va='top', fontsize=8.6, color='#1b5e20')
    # paso 3: t0
    ax.plot([t0], [0], 'D', ms=11, mfc=CY, mec='k', mew=1.3, zorder=7)
    ax.annotate(f'PASO 3\n$t_0$ = {t0:.1f} min\n(donde la recta corta $s=0$)',
                xy=(t0, 0), xytext=(2.0, 1.10), fontsize=9, color='#8a6a00',
                fontweight='bold',
                arrowprops=dict(arrowstyle='-|>', color='#8a6a00', lw=1.4),
                bbox=dict(fc='#fffaf0', ec=CY, lw=1, pad=3))
    # paso 4
    ax.text(.985, .06, 'PASO 4\n'
            '$T=\\dfrac{2.303\\,Q}{4\\pi\\,\\Delta s}$      '
            '$S=\\dfrac{2.25\\,T\\,t_0}{r^{2}}$',
            transform=ax.transAxes, ha='right', va='bottom', fontsize=11,
            bbox=dict(fc='#f3f7fb', ec=CB, lw=1.2, pad=5))
    ax.set_xlabel('tiempo $t$ (min)', fontsize=9.8)
    ax.set_ylabel('abatimiento $s$ (m)', fontsize=9.8)
    ax.set_xlim(1, 3000); ax.set_ylim(-0.45, 2.6)
    ax.grid(which='both', alpha=.3, lw=.5)
    ax.set_title('Los cuatro pasos para leer una recta en papel semilogarítmico',
                 fontsize=10.6)
    save(fig, 'fig_g3_leer_recta')


# ============================================== G4: log-log
def g4():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2))
    # cuadricula log-log a mano
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(1, 1000); ax.set_ylim(.1, 100)
    ax.grid(which='major', color='#555', lw=.9)
    ax.grid(which='minor', color='#bbb', lw=.5)
    for a, b, c in [(1, 10, '#fdf0f0'), (10, 100, '#f1f8f2'), (100, 1000, '#fffaf0')]:
        ax.axvspan(a, b, color=c, alpha=.6, zorder=0)
    ax.text(3.2, 40, 'ciclo 1', ha='center', fontsize=9, color=CR)
    ax.text(32, 40, 'ciclo 2', ha='center', fontsize=9, color='#1b5e20')
    ax.text(320, 40, 'ciclo 3', ha='center', fontsize=9, color='#8a6a00')
    ax.set_xlabel('3 ciclos en el eje horizontal', fontsize=9.3)
    ax.set_ylabel('3 ciclos en el vertical', fontsize=9.3)
    ax.tick_params(labelsize=8)
    ax.set_title('Papel log-log: AMBOS ejes logarítmicos\n'
                 'los cuadros no son cuadrados', fontsize=9.7)

    uu = np.logspace(-6, 0.3, 300)
    ax2.loglog(1 / uu, W(uu), '-', color=CB, lw=2.4)
    Q, r, T, S = 1500., 50., 300., 1e-3
    tm = np.logspace(0, log10(1440), 14)
    s = Q / (4 * pi * T) * W(r ** 2 * S / (4 * T * tm / 1440))
    ax2.loglog(tm * 2.2, s * 5.0, 'o', ms=7, mfc='white', mec=CR, mew=1.8)
    ax2.set_xlim(1, 1e6); ax2.set_ylim(.05, 60)
    ax2.grid(which='both', alpha=.35, lw=.5)
    ax2.set_xlabel('$1/u$   (y $t$ desplazado)', fontsize=9.3)
    ax2.set_ylabel('$W(u)$   (y $s$ desplazado)', fontsize=9.3)
    ax2.tick_params(labelsize=8)
    ax2.set_title('Theis: los datos (rojo) tienen la MISMA forma\nque la curva '
                  'patrón (azul); solo están desplazados', fontsize=9.7)
    ax2.text(.04, .93, 'desplazar manteniendo\nlos ejes PARALELOS',
             transform=ax2.transAxes, fontsize=8.4, va='top', color=CR,
             bbox=dict(fc='white', ec=CR, lw=.8, pad=2.5))
    fig.suptitle('Papel logarítmico doble (log-log): el que se usa para el '
                 'método de Theis', fontsize=10.5, y=1.03)
    save(fig, 'fig_g4_loglog')


# ============================================== G5: construir el papel
def g5():
    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    ax.set_xscale('log'); ax.set_xlim(1, 10000); ax.set_ylim(0, 3)
    ax.grid(which='major', axis='x', color='#444', lw=1.0)
    ax.grid(which='minor', axis='x', color='#bbb', lw=.5)
    ax.grid(axis='y', color='#bbb', lw=.5)
    ax.set_yticks(np.arange(0, 3.1, .25))
    ax.tick_params(labelsize=8.5)
    ax.set_xlabel('tiempo (min) — 4 ciclos logarítmicos', fontsize=9.5)
    ax.set_ylabel('abatimiento (m) — escala lineal', fontsize=9.5)
    ax.set_title('Plantilla: papel semilogarítmico de 4 ciclos\n'
                 'Cópiala a mano si no tienes papel milimetrado logarítmico',
                 fontsize=10.4)
    ax.text(.985, .96, 'Cómo dibujarlo a mano:\n'
            '1. Marca 4 tramos IGUALES en el eje x: 1, 10, 100, 1000, 10000.\n'
            '2. Dentro de cada tramo, divide con la regla de los porcentajes:\n'
            '     2 → 30 %   3 → 48 %   4 → 60 %   5 → 70 %\n'
            '     6 → 78 %   7 → 85 %   8 → 90 %   9 → 95 %\n'
            '3. El eje y es LINEAL y normal.',
            transform=ax.transAxes, ha='right', va='top', fontsize=8.6,
            family='DejaVu Sans',
            bbox=dict(fc='#fffef5', ec='#8a6a00', lw=1.1, pad=5))
    save(fig, 'fig_g5_plantilla')


g1(); g2(); g3(); g4(); g5()
print('figuras de papel log ok')

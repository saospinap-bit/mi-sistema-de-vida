import os
os.environ['MPLCONFIGDIR'] = '/tmp/mplcfg'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import erf, sqrt, pi
from matplotlib.patches import Polygon, Rectangle
import sys
sys.path.insert(0, '/projects/sandbox/.build')
from flownet import solve, velocity, streamline, equal_flux_starts, smooth_path

OUT = '/projects/sandbox/.build/fig'
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans',
                     'axes.linewidth': 0.8, 'savefig.dpi': 200,
                     'savefig.bbox': 'tight', 'savefig.pad_inches': 0.15})
SOIL, AQ, CLAY, WATER = '#e8e2d8', '#d6e4f0', '#cfc8bd', '#bcd9ef'
SALT = '#f3cdcd'
CEQ, CFL = '#1a4e8a', '#b03030'


def save(fig, name):
    fig.savefig(f'{OUT}/{name}.png', facecolor='white')
    plt.close(fig)
    print('  ->', name)


# ================================================================ 5.1
def fig_501():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2),
                                  gridspec_kw=dict(width_ratios=[1, 1]))
    # --- fig 5.5 type
    ax.set_aspect('auto'); ax.axis('off')
    x = np.linspace(0, 10, 300)
    top = 5.2 + 1.5 * (1 / (1 + np.exp(-(x - 5) * 1.1)))
    ax.fill_between(x, 0, top, color=AQ, ec='none')
    ax.plot(x, top, '-', color='#2b8a3e', lw=2.2)
    ax.plot([0, 0], [0, top[0]], '-', color='#333', lw=4)
    ax.plot([10, 10], [0, top[-1]], '-', color='#333', lw=4)
    ax.add_patch(Rectangle((0, -0.5), 10, 0.5, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))
    ax.text(5, top.max() + .55, '$h = f(x)$   nivel freático (Dirichlet, tipo 1)',
            ha='center', fontsize=9, color='#1b5e20')
    ax.text(-0.35, 2.7, '$\\dfrac{\\partial h}{\\partial x}=0$\ndivisoria',
            ha='right', va='center', fontsize=9.5)
    ax.text(10.35, 2.7, '$\\dfrac{\\partial h}{\\partial x}=0$\ndivisoria',
            ha='left', va='center', fontsize=9.5)
    ax.text(5, -0.95, '$\\dfrac{\\partial h}{\\partial z}=0$   base impermeable '
                      '(Neumann, tipo 2)', ha='center', va='top', fontsize=9.5)
    ax.set_xlim(-2.6, 13.0); ax.set_ylim(-2.3, 7.8)
    ax.set_title('Figura 5.5 — medio HOMOGÉNEO\ntres fronteras sin flujo + '
                 'nivel freático', fontsize=9.6)

    # --- fig 5.8 type
    ax2.set_aspect('auto'); ax2.axis('off')
    ys = [(0, 1.7, '#b9cfe0', '$K_3$, capa 3'), (1.7, 3.4, '#cdbfa8', '$K_2$, capa 2'),
          (3.4, 5.2, '#d9e8f5', '$K_1$, capa 1')]
    for y0, y1, c, lab in ys:
        ax2.add_patch(Rectangle((0, y0), 10, y1 - y0, fc=c, ec='k', lw=1.1))
        ax2.text(1.0, (y0 + y1) / 2, lab, fontsize=8.6, va='center')
    xs = np.linspace(0, 10, 60)
    wt = 5.2 + np.interp(xs, [0, 2.5, 4, 6.5, 8, 10], [0, .35, .15, .9, 1.3, 1.6])
    ax2.plot(xs, wt, '-', color='#2b8a3e', lw=2.2)
    for yy, lab in [(3.4, '$\\phi_1=\\phi_2$   ;   '
                          '$K_1\\dfrac{\\partial\\phi_1}{\\partial z}='
                          'K_2\\dfrac{\\partial\\phi_2}{\\partial z}$'),
                    (1.7, '$\\phi_2=\\phi_3$   ;   '
                          '$K_2\\dfrac{\\partial\\phi_2}{\\partial z}='
                          'K_3\\dfrac{\\partial\\phi_3}{\\partial z}$')]:
        ax2.annotate(lab, xy=(7.6, yy), xytext=(11.0, yy + .5), fontsize=8.4,
                     ha='left', color=CFL,
                     arrowprops=dict(arrowstyle='-|>', color=CFL, lw=1.1))
    ax2.text(5, 6.95, '$\\phi_1 = f(x)$  lineal por tramos ($C_1\\ldots C_{k+1}$)',
             ha='center', fontsize=8.8, color='#1b5e20')
    ax2.add_patch(Rectangle((0, -0.5), 10, 0.5, fc='#8a8a8a', ec='k', lw=1,
                            hatch='///'))
    ax2.plot([0, 0], [0, 5.2], '-', color='#333', lw=4)
    ax2.plot([10, 10], [0, 5.2], '-', color='#333', lw=4)
    ax2.set_xlim(-1.0, 19.5); ax2.set_ylim(-1.6, 7.8)
    ax2.set_title('Figura 5.8 — medio ESTRATIFICADO\nAÑADE continuidad de $\\phi$ '
                  'y del flujo normal', fontsize=9.6)
    fig.suptitle('Problema 5.1 — condiciones de borde en modelos de cuenca',
                 fontsize=10.4, y=1.02)
    save(fig, 'fig_5_01_fronteras')

    # --- refraccion
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 2.2), 8, 2.2, fc='#cdbfa8', ec='k', lw=1.1))
    ax.add_patch(Rectangle((0, 0), 8, 2.2, fc='#9ec5e8', ec='k', lw=1.1))
    ax.text(0.5, 3.9, '$K_1$ BAJA', fontsize=9.5)
    ax.text(0.5, 0.35, '$K_2$ ALTA  ($K_2 = 5K_1$)', fontsize=9.5)
    t1 = np.radians(18); t2 = np.radians(np.degrees(np.arctan(5 * np.tan(t1))))
    for x0 in (2.0, 4.2, 6.4):
        ax.plot([x0 - 2.2 * np.tan(t1), x0], [4.4, 2.2], '-', color=CFL, lw=1.9)
        ax.plot([x0, x0 + 2.2 * np.tan(t2)], [2.2, 0], '-', color=CFL, lw=1.9)
        ax.annotate('', xy=(x0 + 1.1 * np.tan(t2), 1.1), xytext=(x0, 2.2),
                    arrowprops=dict(arrowstyle='-|>', color=CFL, lw=1.9))
    ax.plot([4.2, 4.2], [1.3, 3.3], ':', color='#444', lw=1.2)
    ax.text(4.3, 3.1, '$\\theta_1$', fontsize=11)
    ax.text(4.3, 1.45, '$\\theta_2$', fontsize=11)
    ax.text(4.0, -0.9, '$\\dfrac{\\tan\\theta_1}{\\tan\\theta_2}=\\dfrac{K_1}{K_2}$'
                       '      (ley de refracción, análoga a la ley de Snell)',
            ha='center', va='top', fontsize=10.5)
    ax.set_xlim(-0.4, 8.6); ax.set_ylim(-2.4, 4.9)
    ax.set_title('Consecuencia de la continuidad del flujo normal:\n'
                 'las líneas de flujo se REFRACTAN en el contacto', fontsize=9.8)
    save(fig, 'fig_5_01_refraccion')


# ================================================================ 5.2
def toth(flow_left=False, dx=1.0):
    """Patron de flujo controlado topograficamente (tipo figura 5.4)."""
    Lx, Lz = 140.0, 50.0
    nx, nz = int(Lx / dx) + 1, int(Lz / dx) + 1
    X, Z = np.linspace(0, Lx, nx), np.linspace(0, Lz, nz)
    # nivel freatico: pendiente regional + ondulaciones locales
    ztop = 40 + 6.5 * X / Lx + 1.9 * np.sin(2 * np.pi * X / 35.0)
    hv = np.zeros((nz, nx)); fx = np.zeros((nz, nx), bool)
    inact = np.zeros((nz, nx), bool)
    for i in range(nx):
        kt = min(int(np.floor(ztop[i] / dx)), nz - 1)
        fx[kt, i] = True; hv[kt, i] = Z[kt]
        if kt + 1 < nz:
            inact[kt + 1:, i] = True
    if flow_left:                      # frontera izquierda: entra flujo regional
        kk = np.where(~inact[:, 0])[0]
        kk = kk[kk < int(0.55 * len(kk))]   # solo la parte PROFUNDA
        fx[kk, 0] = True
        hv[kk, 0] = ztop[0] + 3.0      # carga impuesta mayor -> entra caudal
    h, it, d = solve(hv, fx, inactive=inact, iters=60000, tol=1e-9)
    qx, qz = velocity(h, dx, dx)
    return dict(X=X, Z=Z, h=h, hm=np.ma.array(h, mask=inact), qx=qx, qz=qz,
                dx=dx, ztop=ztop, inact=inact, Lx=Lx, Lz=Lz)


def fig_502():
    a = toth(False)
    b = toth(True)
    fig, axs = plt.subplots(2, 1, figsize=(9.6, 7.0))
    for ax, c, ttl, fl in [
        (axs[0], a, 'ORIGINAL (figura 5.4) — laterales SIN FLUJO: dominio cerrado '
                    'y celdas locales anidadas', False),
        (axs[1], b, 'MODIFICADO — frontera IZQUIERDA de FLUJO: se pierde la '
                    'divisoria, el sistema regional se refuerza', True)]:
        X, Z, hm, ztop = c['X'], c['Z'], c['hm'], c['ztop']
        ax.set_aspect('equal')
        ax.fill_between(X, 0, ztop, color=AQ, zorder=0)
        hmin, hmax = float(hm.min()), float(hm.max())
        ax.contour(X, Z, hm, levels=np.linspace(hmin, hmax, 24)[1:-1],
                   colors=[CEQ], linewidths=.8, zorder=3)
        # lineas de corriente desde las zonas de recarga
        kk = np.array([max(min(int(np.floor(zt / c['dx'])), len(Z) - 1) - 5, 0)
                       for zt in ztop])
        qzt = c['qz'][kk, np.arange(len(X))]
        rech = qzt < 0
        if rech.sum() > 5:
            x0 = equal_flux_starts(np.abs(qzt[rech]), X[rech], 16)
        else:
            x0 = np.linspace(5, c['Lx'] - 5, 16)
        for xx in x0:
            zz = np.interp(xx, X, ztop) - 2.5
            p = streamline(c['qx'], c['qz'], xx, zz, 0, 0, c['dx'], c['dx'],
                           c['Lx'], c['Lz'])
            p = smooth_path(p, 21)
            ax.plot(p[:, 0], p[:, 1], '-', color=CFL, lw=1.25, zorder=4)
        ax.fill_between(X, ztop, c['Lz'] + 12, color='white', zorder=5)
        ax.plot(X, ztop, '-', color='#2b8a3e', lw=2.0, zorder=6)
        ax.add_patch(Rectangle((0, -3.2), c['Lx'], 3.2, fc='#8a8a8a', ec='k',
                               lw=1, hatch='///', zorder=6))
        if fl:
            for k in range(4):
                ax.annotate('', xy=(10, 3 + k * 6), xytext=(-9, 3 + k * 6),
                            arrowprops=dict(arrowstyle='-|>', color='#8a3b00',
                                            lw=2.2), zorder=8)
            ax.text(-10, 12, 'ENTRA\nflujo lateral\n(regional\nprofundo)',
                    ha='right', va='center',
                    fontsize=8.4, color='#8a3b00', fontweight='bold')
            ax.plot([0, 0], [0, 22], '-', color='#8a3b00', lw=4, zorder=7)
            ax.plot([0, 0], [22, ztop[0]], '-', color='#333', lw=4, zorder=7)
        else:
            ax.plot([0, 0], [0, ztop[0]], '-', color='#333', lw=4, zorder=7)
            ax.text(-3, 24, 'divisoria\n(sin flujo)', ha='right', va='center',
                    fontsize=8.6)
        ax.plot([c['Lx'], c['Lx']], [0, ztop[-1]], '-', color='#333', lw=4,
                zorder=7)
        ax.text(c['Lx'] + 3, 24, 'divisoria\n(sin flujo)', ha='left',
                va='center', fontsize=8.6)
        ax.set_xlim(-30, c['Lx'] + 24); ax.set_ylim(-8, c['Lz'] + 8)
        ax.axis('off'); ax.set_title(ttl, fontsize=9.5)
    fig.suptitle('Problema 5.2(a) — efecto de cambiar una frontera sin flujo por '
                 'una frontera de flujo', fontsize=10.4, y=1.0)
    fig.tight_layout()
    save(fig, 'fig_5_02_redes')

    # --- 5.27 K1 = K2
    fig, axs = plt.subplots(2, 1, figsize=(9.6, 5.4))
    x = np.linspace(0, 50, 500)
    topo = 1.0 + 0.55 * np.exp(-((x - 17) / 6) ** 2) + 0.75 * np.exp(-((x - 33) / 7) ** 2)
    for ax, same, ttl in [
        (axs[0], False, 'ORIGINAL ($K_2 \\gg K_1$) — la capa profunda es un '
                        'CONDUCTO regional: flujo de hasta 50 millas'),
        (axs[1], True, '$K_1 = K_2$ (medio homogéneo) — desaparece la refracción y '
                       'el conducto: DOMINAN los sistemas locales')]:
        ax.set_aspect('auto'); ax.axis('off')
        ax.fill_between(x, 0.45, topo, color='#cdbfa8')
        ax.fill_between(x, 0, 0.45, color='#9ec5e8' if not same else '#cdbfa8')
        ax.plot(x, topo, '-', color='#2b8a3e', lw=1.8)
        ax.plot([0, 50], [0.45, 0.45], '-', color='k',
                lw=1.2 if not same else .5,
                ls='-' if not same else ':')
        ax.text(1.0, 0.72, '$K_1$', fontsize=10)
        ax.text(1.0, 0.16, '$K_2$' if not same else '$K_2 = K_1$', fontsize=10)
        if not same:
            # local cells + deep regional conduit
            for xc, w in [(17, 6), (33, 7)]:
                for s in np.linspace(.25, 1.0, 4):
                    t = np.linspace(0, np.pi, 80)
                    ax.plot(xc + s * w * np.cos(t), 0.52 + s * 0.30 * np.sin(t),
                            '-', color=CFL, lw=1.1)
            for yy in (0.14, 0.26, 0.38):
                ax.annotate('', xy=(47.5, yy), xytext=(4, yy),
                            arrowprops=dict(arrowstyle='-|>', color=CFL, lw=1.6))
            ax.text(25, 0.05, 'flujo regional profundo', fontsize=8,
                    color=CFL, ha='center')
            ax.annotate('descarga salina\nlejana', xy=(48.5, 0.9),
                        xytext=(43, 1.72), fontsize=8, color='#8a3b00',
                        ha='center',
                        arrowprops=dict(arrowstyle='-|>', color='#8a3b00', lw=1.1))
        else:
            for xc, w in [(8, 8), (17, 6), (25, 7), (33, 7), (43, 8)]:
                for s in np.linspace(.25, 1.0, 4):
                    t = np.linspace(0, np.pi, 80)
                    ax.plot(xc + s * w * np.cos(t), 0.42 + s * 0.42 * np.sin(t),
                            '-', color=CFL, lw=1.1)
            ax.text(25, 0.08, 'sólo celdas LOCALES anidadas (patrón de Tóth)',
                    fontsize=8, color=CFL, ha='center')
        ax.set_xlim(-1, 54); ax.set_ylim(-0.1, 2.1)
        ax.set_title(ttl, fontsize=9.3)
        ax.annotate('', xy=(50, -0.03), xytext=(0, -0.03),
                    arrowprops=dict(arrowstyle='<|-|>', color='k', lw=.8))
        ax.text(25, -0.07, '50 millas', ha='center', va='top', fontsize=8)
    fig.suptitle('Problema 5.2(b) — perfil de pradera (figura 5.27) con $K_1=K_2$',
                 fontsize=10.4, y=1.0)
    fig.tight_layout()
    save(fig, 'fig_5_02_pradera')


# ================================================================ 5.3
def fig_503():
    K, Sy, h0 = 0.0835, 0.01, 12.0
    bbar = 15.0
    T = K * bbar; nu = T / Sy
    L = 3 * 1609.344
    xx = np.linspace(0, L, 500)

    # ---------- plate 1: geometry
    fig, ax = plt.subplots(figsize=(9.6, 4.0))
    ax.axis('off')
    ax.add_patch(Rectangle((0, -9), L, 21, fc=AQ, ec='none'))
    ax.add_patch(Rectangle((-520, -9), 520, 9, fc=WATER, ec='none'))
    ax.plot([-520, 0], [0, 0], '-', color='#1a4e8a', lw=2)
    ax.plot([-520, -520, 0, 0], [12, -9, -9, 12], '-', color='k', lw=1.6)
    ax.add_patch(Rectangle((-520, -13), L + 520, 4, fc='#8a8a8a', ec='k',
                           lw=1, hatch='///'))
    ax.axhline(0, color='#1a4e8a', lw=1.2, ls='--')
    ax.text(L, 1.2, 'nivel del mar  (datum, $h=0$)', ha='right', fontsize=8.8,
            color='#1a4e8a')
    ax.plot(xx, 12 * np.ones_like(xx), ':', color='#777', lw=1.5)
    ax.text(L * .52, 12.9, 'nivel freático inicial  $h_0 = 12$ m', fontsize=8.8,
            color='#555', ha='center')
    for yr, st, c in [(10, '-', '#1a4e8a'), (40, '--', '#d9a400'),
                      (100, '-.', '#b03030')]:
        t = yr * 365.25
        ax.plot(xx, h0 * np.array([erf(x / (2 * sqrt(nu * t))) for x in xx]),
                st, color=c, lw=2.0, label=f'{yr} años')
    ax.legend(fontsize=8.4, loc='center right', ncol=1, framealpha=.95,
              title='nivel freático a los:', title_fontsize=8.2)
    ax.text(-260, 5.5, 'CANAL', ha='center', fontsize=9.5, rotation=90,
            fontweight='bold')
    ax.annotate('', xy=(-640, 0), xytext=(-640, 12),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1))
    ax.text(-690, 6, '12 m', rotation=90, ha='right', va='center', fontsize=8.6)
    ax.annotate('', xy=(-640, -9), xytext=(-640, 0),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1))
    ax.text(-690, -4.5, '9 m', rotation=90, ha='right', va='center', fontsize=8.6)
    ax.annotate('', xy=(0, -17.5), xytext=(L, -17.5),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1))
    ax.text(L / 2, -19.2, '$L$ = 3 mi = 4828 m', ha='center', va='top',
            fontsize=9)
    ax.plot([L, L], [-9, 14], '-', color='#8a3b00', lw=2.4)
    ax.text(L, 15.2, 'DIVISORIA (manantiales)', ha='center', fontsize=8.8,
            color='#8a3b00', fontweight='bold')
    ax.text(L * .30, -5.0,
            'espesor saturado: 21 m en la divisoria, 9 m en el canal\n'
            '$\\bar b = (21+9)/2 = 15$ m        '
            f'$T = K\\bar b = {T:.4f}$ m²/día        '
            f'$\\nu = T/S_y = {nu:.2f}$ m²/día',
            ha='center', va='center', fontsize=8.8,
            bbox=dict(fc='white', ec='#1a4e8a', lw=.9, alpha=.95, pad=3.5))
    ax.set_xlim(-1150, L + 300); ax.set_ylim(-26, 18)
    ax.set_title('Problema 5.3 — geometría del canal a nivel del mar\n'
                 '$h(x,t)=h_0\\,\\mathrm{erf}\\!\\left(x/2\\sqrt{\\nu t}\\right)$,   '
                 '$K = 8.35$ cm/día,  $S_y = 0.01$', fontsize=10)
    save(fig, 'fig_5_03_canal')

    # ---------- plate 2: profiles + flow rate
    fig = plt.figure(figsize=(9.6, 7.4))
    g = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], hspace=.40, wspace=.30)

    ax = fig.add_subplot(g[0, :])
    yoff = {10: .55, 20: .55, 40: .55, 100: .55}
    for yr, c in zip([10, 20, 40, 100],
                     ['#1a4e8a', '#2b8a3e', '#d9a400', '#b03030']):
        t = yr * 365.25
        hh = h0 * np.array([erf(x / (2 * sqrt(nu * t))) for x in xx])
        ax.plot(xx, hh, '-', color=c, lw=2.2, label=f'{yr} años')
        ax.plot([L], [hh[-1]], 'o', ms=6, color=c, zorder=5)
    ax.axhline(h0, color='#888', ls=':', lw=1.4)
    ax.text(120, h0 + .18, 'nivel freático inicial  $h_0 = 12$ m', fontsize=8.4,
            color='#555')
    ax.axvline(L, color='#8a3b00', lw=1.8)
    tab = ('carga en la DIVISORIA\n'
           '  10 años :  12.00 m   (0.00 m de abatimiento)\n'
           '  20 años :  12.00 m   (0.00 m)\n'
           '  40 años :  11.86 m   (0.14 m)\n'
           ' 100 años :  10.67 m   (1.33 m)')
    ax.text(L * .40, 4.2, tab, ha='left', va='center', fontsize=8.5,
            family='DejaVu Sans Mono',
            bbox=dict(fc='#fffdf5', ec='#8a3b00', lw=.9, alpha=.97, pad=4))
    ax.text(L - 110, 1.0, 'divisoria', rotation=90, fontsize=8.4,
            color='#8a3b00', ha='right', va='bottom')
    ax.set_xlabel('distancia desde el canal, $x$ (m)', fontsize=9.2)
    ax.set_ylabel('carga $h$ (m sobre el nivel del mar)', fontsize=9.2)
    ax.legend(fontsize=8.6, loc='center left', framealpha=.95,
              bbox_to_anchor=(.015, .60))
    ax.grid(alpha=.3, lw=.6); ax.tick_params(labelsize=8.4)
    ax.set_xlim(0, L + 120); ax.set_ylim(0, 13.9)
    ax.set_title('(a) Perfiles del nivel freático: el abatimiento tarda más de '
                 '40 años en alcanzar la divisoria', fontsize=9.8)

    ax = fig.add_subplot(g[1, 0])
    tt = np.linspace(0.5, 120, 500) * 365.25
    qp = h0 * np.sqrt(T * Sy / (pi * tt))
    ax.plot(tt / 365.25, qp * 1000, '-', color=CEQ, lw=2.3)
    for yr, c, tx, ty in [(10, '#2b8a3e', 26, 26.5), (100, CFL, 34, 13.5)]:
        q = h0 * sqrt(T * Sy / (pi * yr * 365.25))
        ax.plot([yr], [q * 1000], 'o', ms=9, mfc='white', mec=c, mew=2.2, zorder=5)
        ax.annotate(f'{yr} años:  {q*1000:.1f} L/día·m\n'
                    f'$= {q*1e3:.2f}\\times10^{{-3}}$ m³/día·m',
                    xy=(yr, q * 1000), xytext=(tx, ty),
                    fontsize=8.2, color=c, ha='left',
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1))
    ax.set_xlabel('tiempo (años)', fontsize=9.2)
    ax.set_ylabel("$q'$ (L/día por metro de canal)", fontsize=9.2)
    ax.set_title("(b) $q' = h_0\\sqrt{T S_y/\\pi t}$", fontsize=9.8)
    ax.grid(alpha=.3, lw=.6); ax.tick_params(labelsize=8.4)
    ax.set_xlim(0, 120); ax.set_ylim(0, 34)

    ax = fig.add_subplot(g[1, 1])
    ax.loglog(tt / 365.25, qp, '-', color=CEQ, lw=2.3)
    for yr, c in [(10, '#2b8a3e'), (100, CFL)]:
        ax.loglog([yr], [h0 * sqrt(T * Sy / (pi * yr * 365.25))], 'o', ms=9,
                  mfc='white', mec=c, mew=2.2)
    ax.set_xlabel('tiempo (años)', fontsize=9.2)
    ax.set_ylabel("$q'$ (m³/día·m)", fontsize=9.2)
    ax.set_title('Verificación: pendiente $-1/2$\n'
                 "$q'(10)/q'(100)=\\sqrt{10}=3.16$", fontsize=9.8)
    ax.grid(alpha=.3, which='both', lw=.5); ax.tick_params(labelsize=8.4)
    fig.suptitle('Problema 5.3 — abatimiento y caudal hacia el canal',
                 fontsize=10.6, y=.98)
    save(fig, 'fig_5_03_perfiles')


# ================================================================ 5.4
def fig_504():
    gs_, gw, D, hp = 125.0, 62.4, 50.0, 70.0
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.3),
                                  gridspec_kw=dict(width_ratios=[1.05, 1]))
    ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 8, 1.6, fc='#f0d9a8', ec='k', lw=1.2))
    ax.text(4, .8, 'ACUÍFERO ARTESIANO  (carga $h_p$)', ha='center',
            va='center', fontsize=8.6)
    d = 1.2
    ax.add_patch(Polygon([(0, 1.6), (8, 1.6), (8, 3.6), (5.4, 3.6),
                          (5.4, 3.6 - d), (2.6, 3.6 - d), (2.6, 3.6), (0, 3.6)],
                         fc=CLAY, ec='k', lw=1.2, hatch='xx'))
    ax.add_patch(Rectangle((2.6, 3.6 - d), 2.8, d, fc=WATER, ec='#1a4e8a', lw=1))
    ax.text(4, 3.6 - d / 2, 'EXCAVACIÓN', ha='center', va='center', fontsize=8.4,
            color='#13335c')
    ax.text(1.1, 2.6, 'estrato\nconfinante\n$\\gamma_{sat}$', ha='center',
            fontsize=8.4)
    for k in range(7):
        xa = 2.8 + k * .42
        ax.annotate('', xy=(xa, 2.35), xytext=(xa, 1.65),
                    arrowprops=dict(arrowstyle='-|>', color=CFL, lw=2.0))
    ax.text(4, 1.25, 'FLUJO ASCENDENTE (zona de descarga)\n'
                     '$u$ empuja el tapón hacia arriba', ha='center', va='top',
            fontsize=8.5, color=CFL)
    ax.plot(4, 1.6, '*', ms=14, color=CFL, zorder=6)
    ax.annotate('', xy=(6.1, 1.6), xytext=(6.1, 3.6),
                arrowprops=dict(arrowstyle='<|-|>', color='#555', lw=.9))
    ax.text(6.25, 2.6, '$D$', fontsize=10, va='center')
    ax.annotate('', xy=(5.0, 3.6), xytext=(5.0, 3.6 - d),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=.9))
    ax.text(5.12, 3.6 - d / 2, '$d$', fontsize=10, va='center')
    ax.text(4, 0.25, "$\\sigma_T=\\gamma_{sat}(D-d)+\\gamma_w d_w$      "
                     "$u=\\gamma_w h_p$      $FS=\\sigma_T/u$",
            ha='center', va='top', fontsize=9.3)
    ax.set_xlim(-0.3, 7.6); ax.set_ylim(-0.9, 4.0)
    ax.set_title('Mecanismo: la excavación reduce $\\sigma_T$ mientras $u$ '
                 'permanece fijo', fontsize=9.5)

    dd = np.linspace(0, 45, 400)
    for dw_mode, c, lab in [('agua', '#1a4e8a', 'excavación llena de agua'),
                            ('seca', '#2b8a3e', 'excavación en seco')]:
        dw = dd if dw_mode == 'agua' else 0 * dd
        FS = (gs_ * (D - dd) + gw * dw) / (gw * hp)
        ax2.plot(dd, FS, '-', color=c, lw=2.3, label=lab)
        dc = dd[np.argmin(np.abs(FS - 1))]
        ax2.plot([dc], [1], 'o', ms=8, mfc='white', mec=c, mew=2, zorder=5)
        ax2.annotate(f'$d_{{crit}}$ = {dc:.1f} ft', xy=(dc, 1),
                     xytext=(dc + 1.5, 1.28 if dw_mode == 'agua' else 1.52),
                     fontsize=8.6, color=c,
                     arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1))
    ax2.axhline(1.0, color=CFL, lw=2, ls='--')
    ax2.axhline(1.3, color='#d9a400', lw=1.4, ls=':')
    ax2.text(44, 1.03, 'FS = 1  (condición crítica, $\\sigma\'=0$)', fontsize=8,
             color=CFL, ha='right')
    ax2.text(44, 1.33, 'FS = 1.3  (mínimo de diseño)', fontsize=8,
             color='#8a6a00', ha='right')
    ax2.fill_between(dd, 0, 1, color=CFL, alpha=.10)
    ax2.text(22, .5, 'FALLA  (reventón del fondo)', ha='center', fontsize=9,
             color=CFL, fontweight='bold')
    ax2.set_xlabel('profundidad excavada $d$ (ft)', fontsize=9)
    ax2.set_ylabel('factor de seguridad  $FS = \\sigma_T/u$', fontsize=9)
    ax2.legend(fontsize=8.3, loc='upper right'); ax2.grid(alpha=.3, lw=.6)
    ax2.tick_params(labelsize=8); ax2.set_xlim(0, 45); ax2.set_ylim(0, 1.7)
    ax2.set_title('$D=50$ ft, $\\gamma_{sat}=125$ lb/ft³, $h_p=70$ ft',
                  fontsize=9.5)
    fig.suptitle('Problema 5.4 — estabilidad del fondo de una excavación en zona '
                 'de descarga', fontsize=10.4, y=1.0)
    save(fig, 'fig_5_04_excavacion')


# ================================================================ 5.5
def fig_505():
    G, Kv = 0.025, 1e-3
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.3))
    ax.axis('off')
    dft, dm = 40.0, 40 * 0.3048
    ax.add_patch(Rectangle((0, 0), 10, 3.1, fc=AQ, ec='none'))
    x = np.linspace(0, 10, 400)
    rise = 1.25 * np.exp(-((x - 5) / 1.5) ** 2)
    ax.fill_between(x, 0, 0.9 + rise, color=SALT, ec=CFL, lw=1.6)
    ax.plot(x, 0.9 + rise, '-', color=CFL, lw=2)
    ax.plot([0, 10], [.9, .9], ':', color='#777', lw=1.3)
    ax.text(0.3, 0.35, 'AGUA SALADA  $\\rho_s = 1025$', fontsize=8.4)
    ax.text(0.3, 2.65, 'AGUA DULCE  $\\rho_f = 1000$', fontsize=8.4)
    ax.add_patch(Rectangle((4.85, 2.55), .3, 1.4, fc='white', ec='k', lw=1.3))
    ax.plot([5, 5], [2.55, 2.9], '-', color='k', lw=1.3)
    ax.plot(5, 2.55, 'v', ms=9, color='k')
    ax.annotate('', xy=(5, 4.4), xytext=(5, 3.9),
                arrowprops=dict(arrowstyle='-|>', color=CEQ, lw=2.4))
    ax.text(5, 4.5, '$Q$', ha='center', fontsize=11, color=CEQ)
    ax.annotate('', xy=(6.8, .9), xytext=(6.8, 2.55),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.1))
    ax.text(6.95, 1.7, f'$d$ = 40 ft\n= {dm:.2f} m', fontsize=8.6, va='center')
    ax.annotate('', xy=(3.5, .9), xytext=(3.5, 2.15),
                arrowprops=dict(arrowstyle='<|-|>', color=CFL, lw=1.1))
    ax.text(3.35, 1.5, '$z$', fontsize=11, ha='right', va='center', color=CFL)
    ax.plot([2.5, 7.5], [2.15, 2.15], '--', color=CFL, lw=1)
    ax.text(2.4, 2.2, '$z = 0.3d$\n(límite)', fontsize=8, color=CFL, ha='right')
    ax.text(5, -0.55, '$z=\\dfrac{Q}{2\\pi K d G}$      '
                      '$z\\leq 0.3d \\Rightarrow Q_{max}=0.6\\pi K d^2 G$',
            ha='center', va='top', fontsize=10)
    ax.set_xlim(-0.3, 10.3); ax.set_ylim(-1.9, 4.9)
    ax.set_title('Ascenso del cono salino bajo un pozo (upconing)', fontsize=9.6)

    dd = np.linspace(5, 80, 300) * 0.3048
    Qm = 0.6 * pi * Kv * dd ** 2 * G
    ax2.plot(dd / 0.3048, Qm * 1000, '-', color=CEQ, lw=2.3)
    Q40 = 0.6 * pi * Kv * dm ** 2 * G
    ax2.plot([40], [Q40 * 1000], 'o', ms=10, mfc='white', mec=CFL, mew=2.3,
             zorder=5)
    ax2.annotate(f'$d$ = 40 ft\n$Q_{{max}}$ = {Q40*1000:.2f} L/s\n'
                 f'= {Q40*86400:.0f} m³/día = 111 gpm',
                 xy=(40, Q40 * 1000), xytext=(44, Q40 * 1000 - 11), fontsize=8.6,
                 color=CFL,
                 arrowprops=dict(arrowstyle='-|>', color=CFL, lw=1.2))
    ax2.plot([80], [0.6 * pi * Kv * (80 * .3048) ** 2 * G * 1000], 'o', ms=8,
             mfc='white', mec='#2b8a3e', mew=2)
    ax2.annotate('duplicar $d$\n$\\Rightarrow$ 4 veces $Q_{max}$',
                 xy=(80, 0.6 * pi * Kv * (80 * .3048) ** 2 * G * 1000),
                 xytext=(52, 24), fontsize=8.6, color='#1b5e20',
                 arrowprops=dict(arrowstyle='-|>', color='#1b5e20', lw=1.2))
    ax2.set_xlabel('distancia a la interfaz, $d$ (ft)', fontsize=9)
    ax2.set_ylabel('$Q_{max}$ (L/s)', fontsize=9)
    ax2.set_title('$Q_{max}\\propto d^{2}$  ($K=10^{-1}$ cm/s, $G=0.025$)',
                  fontsize=9.6)
    ax2.grid(alpha=.3, lw=.6); ax2.tick_params(labelsize=8)
    fig.suptitle('Problema 5.5 — caudal máximo sin provocar upconing',
                 fontsize=10.4, y=1.0)
    save(fig, 'fig_5_06_upconing')


# ================================================================ 5.6
def fig_506():
    Kf, G, B = 3.3e-3, 0.025, 100.0
    KG = Kf * G
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.4),
                                  gridspec_kw=dict(width_ratios=[1.15, 1]))

    def toe(q):
        return KG * B ** 2 / (2 * q) - q / (2 * KG)

    ax.set_aspect('auto')
    xmax = 5200
    ax.add_patch(Rectangle((-700, -B), xmax + 700, B, fc=AQ, ec='none'))
    for q, c, ls, lab in [(2e-4, '#1a4e8a', '-', "$q' = 2\\times10^{-4}$ ft³/s·ft"),
                          (1e-4, '#b03030', '--', "$q'$ a la mitad $=1\\times10^{-4}$")]:
        xt = toe(q)
        xs = np.linspace(0, xt, 400)
        z = -np.sqrt(2 * q * xs / KG + (q / KG) ** 2)
        ax.plot(xs, z, ls, color=c, lw=2.3, label=lab)
        ax.plot([xt], [-B], 'o', ms=8, mfc='white', mec=c, mew=2.2, zorder=5)
        ax.annotate(f'pie: {xt:.0f} ft', xy=(xt, -B),
                    xytext=(xt + 120, -B + (16 if q > 1.5e-4 else 32)),
                    fontsize=8.8, color=c,
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.2))
    xs = np.linspace(0, toe(1e-4), 400)
    z2 = -np.sqrt(2 * 1e-4 * xs / KG + (1e-4 / KG) ** 2)
    ax.fill_between(xs, -B, z2, color=SALT, alpha=.65)
    ax.axhline(0, color='#1a4e8a', lw=1.6)
    ax.axvline(0, color='k', lw=1.2, ls=':')
    ax.add_patch(Rectangle((-700, -B - 9), xmax + 700, 9, fc='#8a8a8a', ec='k',
                           lw=1, hatch='///'))
    ax.text(-650, -50, 'TIERRA', fontsize=9, rotation=90, va='center')
    ax.text(150, -14, 'línea de costa', fontsize=8.4, rotation=90, va='top')
    ax.text(xmax * .55, -22, 'AGUA DULCE', fontsize=9.5, color='#13335c')
    ax.text(xmax * .12, -70, 'AGUA SALADA', fontsize=9, color='#8a2020')
    ax.annotate('', xy=(xmax, -18), xytext=(xmax * .78, -18),
                arrowprops=dict(arrowstyle='-|>', color='#1a4e8a', lw=2.2))
    ax.text(xmax * .88, -11, "$q'$ hacia el mar", fontsize=8.4, ha='center',
            color='#1a4e8a')
    ax.set_xlabel('distancia tierra adentro desde la costa, $x$ (ft)', fontsize=9)
    ax.set_ylabel('profundidad bajo el nivel del mar (ft)', fontsize=9)
    ax.set_ylim(-118, 14); ax.set_xlim(-700, xmax)
    ax.legend(fontsize=8.3, loc='center right', framealpha=.95,
              bbox_to_anchor=(.995, .62))
    ax.tick_params(labelsize=8); ax.grid(alpha=.25, lw=.5)
    ax.set_title('Reducir $q\'$ a la mitad DUPLICA la penetración de la cuña',
                 fontsize=9.6)
    ax.text(0.015, 0.045, '$z^2 = \\dfrac{2q\'x}{KG}+'
            '\\left(\\dfrac{q\'}{KG}\\right)^{2}$  (Glover, 1959)',
            transform=ax.transAxes, fontsize=9.5, va='bottom', ha='left',
            bbox=dict(fc='white', ec='#999', lw=.7, alpha=.95, pad=3))

    q = np.logspace(-5, -3.2, 300)
    xt = KG * B ** 2 / (2 * q) - q / (2 * KG)
    ax2.loglog(q, xt, '-', color=CEQ, lw=2.3)
    for qq, c in [(2e-4, '#1a4e8a'), (1e-4, '#b03030')]:
        ax2.plot([qq], [toe(qq)], 'o', ms=9, mfc='white', mec=c, mew=2.2, zorder=5)
        ax2.annotate(f'{toe(qq):.0f} ft', xy=(qq, toe(qq)),
                     xytext=(qq * 1.25, toe(qq) * 1.5), fontsize=8.8, color=c,
                     arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1))
    ax2.axvline(2e-1, color='#8a3b00', lw=2)
    ax2.set_xlim(1e-5, 3e-1)
    ax2.text(0.97, 0.93, "el $q'=2\\times10^{-1}$ del enunciado queda\n"
             'fuera de escala:  $x_{toe} < 0$,  NO hay cuña\n'
             '($i$ implícito $= 0.61$ m/m, imposible)',
             transform=ax2.transAxes, fontsize=8.2, color='#8a3b00',
             ha='right', va='top',
             bbox=dict(fc='#fff4ec', ec='#8a3b00', lw=.9, pad=3))
    ax2.set_xlabel("$q'$ (ft³/s por pie de costa)", fontsize=9)
    ax2.set_ylabel('$x_{toe}$ (ft)', fontsize=9)
    ax2.set_title('$x_{toe}\\approx \\dfrac{KGB^2}{2q\'} \\propto 1/q\'$',
                  fontsize=9.6)
    ax2.grid(alpha=.3, which='both', lw=.5); ax2.tick_params(labelsize=8)
    fig.suptitle('Problema 5.6 — posición del pie de la cuña salina '
                 '($B=100$ ft, $K=3.3\\times10^{-3}$ ft/s)', fontsize=10.6,
                 y=1.07)
    save(fig, 'fig_5_06_cuna')


print('cap5:')
fig_501(); fig_502(); fig_503(); fig_504(); fig_505(); fig_506()
print('cap5 ok')

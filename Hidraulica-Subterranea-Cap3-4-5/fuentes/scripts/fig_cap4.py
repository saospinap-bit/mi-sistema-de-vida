import os
os.environ['MPLCONFIGDIR'] = '/tmp/mplcfg'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle, Circle
import sys
sys.path.insert(0, '/projects/sandbox/.build')
from flownet import solve, velocity, streamline, equal_flux_starts, smooth_path

OUT = '/projects/sandbox/.build/fig'
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans',
                     'axes.linewidth': 0.8, 'savefig.dpi': 200,
                     'savefig.bbox': 'tight', 'savefig.pad_inches': 0.15})
SOIL, AQ, CLAY, WATER = '#e8e2d8', '#d6e4f0', '#cfc8bd', '#bcd9ef'
CEQ, CFL = '#1a4e8a', '#b03030'


def save(fig, name):
    fig.savefig(f'{OUT}/{name}.png', facecolor='white')
    plt.close(fig)
    print('  ->', name)


# ================================================================ 4.4
def fig_404():
    gs_, gw, D, hp = 125.0, 62.4, 50.0, 70.0
    fig = plt.figure(figsize=(9.4, 7.6))
    g = fig.add_gridspec(2, 2, height_ratios=[1.05, 1], hspace=.33, wspace=.26)

    # --- (A) original condition
    def section(ax, d, dw, title, vals):
        ax.axis('off')
        ax.add_patch(Rectangle((0, 0), 6, 2.0, fc='#f0d9a8', ec='k', lw=1.2))
        ax.text(3, 1.0, 'ARENA ARTESIANA', ha='center', va='center', fontsize=8.5)
        # clay, with trench
        if d > 0:
            ax.add_patch(Polygon([(0, 2), (6, 2), (6, 2 + D / 25),
                                  (4.2, 2 + D / 25), (4.2, 2 + (D - d) / 25),
                                  (1.8, 2 + (D - d) / 25), (1.8, 2 + D / 25),
                                  (0, 2 + D / 25)], fc=CLAY, ec='k', lw=1.2,
                                 hatch='xx'))
            if dw > 0:
                ax.add_patch(Rectangle((1.8, 2 + (D - d) / 25), 2.4, dw / 25,
                                       fc=WATER, ec='#1a4e8a', lw=1))
                ax.text(3, 2 + (D - d) / 25 + dw / 50, f'agua\n{dw:.0f} ft',
                        ha='center', va='center', fontsize=7.5, color='#13335c')
            else:
                ax.text(3, 2 + (D - d) / 25 + .25, 'SECA', ha='center',
                        fontsize=8, color=CFL, fontweight='bold')
            ax.annotate('', xy=(4.5, 2 + D / 25), xytext=(4.5, 2 + (D - d) / 25),
                        arrowprops=dict(arrowstyle='<|-|>', color='k', lw=.9))
            ax.text(4.62, 2 + (2 * D - d) / 50, f'$d$={d:.0f} ft', fontsize=7.6,
                    va='center')
        else:
            ax.add_patch(Rectangle((0, 2), 6, D / 25, fc=CLAY, ec='k', lw=1.2,
                                   hatch='xx'))
        ax.text(0.9, 2 + D / 50, 'ARCILLA\n$\\gamma_{sat}=125$', ha='center',
                va='center', fontsize=8)
        ax.plot([0, 6], [2, 2], 'k-', lw=1.6)
        ax.annotate('', xy=(5.55, 2), xytext=(5.55, 2 + D / 25),
                    arrowprops=dict(arrowstyle='<|-|>', color='#555', lw=.9))
        ax.text(5.68, 2 + D / 50, '$D$=50 ft', fontsize=7.6, va='center',
                rotation=90, ha='left')
        # piezometer
        ax.add_patch(Rectangle((0.42, 1.6), .16, D / 25 + hp / 25 - 0.4,
                               fc=WATER, ec='k', lw=1))
        ax.plot([.25, .75], [1.6 + D / 25 + hp / 25 - 0.4] * 2, '-',
                color='#1a4e8a', lw=2)
        ax.text(.5, 1.6 + D / 25 + hp / 25 - 0.25, '+20 ft', ha='center',
                fontsize=7.6, color='#1a4e8a')
        ax.plot([0, 6], [2 + D / 25] * 2, '--', color='#4a7c2f', lw=1)
        ax.annotate('', xy=(0.5, 2), xytext=(0.5, 2 + (D + hp - D) / 25 + D / 25),
                    arrowprops=dict(arrowstyle='-', color='none'))
        ax.text(3, 1.55, f'$\\sigma_T$={vals[0]:.0f}   $u$={vals[1]:.0f}   '
                         f"$\\sigma'$={vals[2]:.0f}   FS={vals[3]:.2f}",
                ha='center', va='top', fontsize=8.6,
                color='k' if vals[2] > 0 else CFL,
                bbox=dict(fc='#fff6f6' if vals[2] <= 0 else '#f3f7fb',
                          ec=CFL if vals[2] <= 0 else '#1a4e8a', lw=.9, pad=2.5))
        ax.plot(3, 2, '*', ms=13, color=CFL, zorder=6)
        ax.text(3.15, 2.1, 'punto de análisis', fontsize=7.3, color=CFL)
        ax.set_xlim(-0.3, 6.6); ax.set_ylim(0.6, 2 + D / 25 + hp / 25 + .35)
        ax.set_title(title, fontsize=9.3)

    def st(d, dw):
        sT = gs_ * (D - d) + gw * dw
        u = gw * hp
        return sT, u, sT - u, sT / u

    section(fig.add_subplot(g[0, 0]), 0, 0, '(a) Sin excavar', st(0, 0))
    section(fig.add_subplot(g[0, 1]), 20, 20,
            '(b) Zanja de 20 ft llena de agua', st(20, 20))
    section(fig.add_subplot(g[1, 0]), 20, 0,
            '(c) Zanja de 20 ft DESECADA  $\\Rightarrow$ FALLA', st(20, 0))

    # --- (d) plot
    ax = fig.add_subplot(g[1, 1])
    d = np.linspace(0, 45, 400)
    sT_w = gs_ * (D - d) + gw * d
    sT_d = gs_ * (D - d)
    u = gw * hp
    ax.plot(d, sT_w, '-', color='#1a4e8a', lw=2.2, label='$\\sigma_T$, zanja con agua')
    ax.plot(d, sT_d, '-', color='#2b8a3e', lw=2.2, label='$\\sigma_T$, zanja seca')
    ax.axhline(u, color=CFL, lw=2.2, ls='--', label=f'$u = \\gamma_w h_p$ = {u:.0f} lb/ft² (fija)')
    dc_w = (gs_ * D - gw * hp) / (gs_ - gw)
    dc_d = D - gw * hp / gs_
    for dc, c, lab in [(dc_w, '#1a4e8a', f'{dc_w:.1f} ft'), (dc_d, '#2b8a3e', f'{dc_d:.1f} ft')]:
        ax.plot([dc], [u], 'o', ms=8, mfc='white', mec=c, mew=2, zorder=5)
        ax.annotate(f'$d_{{crit}}$ = {lab}', xy=(dc, u), xytext=(dc + 1.5, u + 820),
                    fontsize=8.5, color=c,
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1))
    ax.fill_between(d, u, sT_w, where=sT_w >= u, color='#2b8a3e', alpha=.10)
    ax.fill_between(d, sT_w, u, where=sT_w < u, color=CFL, alpha=.13)
    ax.set_xlabel('profundidad excavada $d$ (ft)', fontsize=9)
    ax.set_ylabel('esfuerzo (lb/ft²)', fontsize=9)
    ax.set_title("(d) Profundidad crítica: $\\sigma_T = u \\Rightarrow \\sigma' = 0$",
                 fontsize=9.3)
    ax.legend(fontsize=7.6, loc='lower left', framealpha=.95)
    ax.grid(alpha=.3, lw=.6); ax.tick_params(labelsize=8)
    ax.set_xlim(0, 45); ax.set_ylim(0, 7000)
    fig.suptitle('Problema 4.4 — esfuerzo total, neutro y efectivo en el fondo de '
                 'una excavación sobre un acuífero artesiano', fontsize=10.5, y=.995)
    save(fig, 'fig_4_04_esfuerzos')


# ================================================================ 4.5
def fig_405():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.5),
                                  gridspec_kw=dict(width_ratios=[1.05, 1]))
    ax.set_aspect('equal'); ax.axis('off')
    nf = 8
    for r, hv in zip([1.0, 1.9, 2.9, 4.0], [60, 50, 40, 30]):
        ax.add_patch(Circle((0, 0), r, fc='none', ec=CEQ, lw=1.5))
        ax.text(0, r, f'{hv}', color=CEQ, fontsize=8, ha='center',
                va='bottom', bbox=dict(fc='white', ec='none', pad=.8))
    for k in range(nf):
        a = 2 * np.pi * k / nf + 0.12
        ax.annotate('', xy=(0.55 * np.cos(a), 0.55 * np.sin(a)),
                    xytext=(4.5 * np.cos(a), 4.5 * np.sin(a)),
                    arrowprops=dict(arrowstyle='-|>', color=CFL, lw=1.4,
                                    linestyle='--'))
    ax.plot(0, 0, 'o', ms=12, mfc='white', mec='k', mew=2, zorder=6)
    ax.text(0, -0.45, 'B', ha='center', va='top', fontsize=11, fontweight='bold')
    ax.text(0, -0.95, '$Q = 3\\times10^{4}$ m$^3$/día', ha='center', va='top',
            fontsize=9)
    ax.text(3.3, 3.3, f'$n_f = {nf}$ tubos\nde flujo', color=CFL, fontsize=9,
            ha='center')
    ax.text(-3.4, 3.4, 'equipotenciales\ncada 10 ft = 3.048 m', color=CEQ,
            fontsize=8.5, ha='center')
    ax.set_xlim(-5, 5); ax.set_ylim(-5.4, 5)
    ax.set_title('Cada tubo aporta $\\Delta Q = T\\,\\Delta h$', fontsize=9.6)

    # sensitivity
    Q, dh = 3e4, 10 * 0.3048
    n = np.arange(4, 17)
    T = Q / (n * dh)
    ax2.plot(n, T, 'o-', color=CEQ, lw=1.8, ms=6)
    ax2.plot([8], [Q / (8 * dh)], 'o', ms=12, mfc='none', mec=CFL, mew=2.2)
    ax2.annotate(f'$n_f=8$\n$T = {Q/(8*dh):.0f}$ m²/día', xy=(8, Q / (8 * dh)),
                 xytext=(9.5, 1900), fontsize=9, color=CFL,
                 arrowprops=dict(arrowstyle='-|>', color=CFL, lw=1.2))
    ax2.axhspan(984, 1640, color='#2b8a3e', alpha=.12)
    ax2.text(14.6, 1300, 'rango razonable\n984–1640 m²/día', fontsize=8,
             color='#1b5e20', ha='right', va='center')
    ax2.set_xlabel('número de tubos de flujo contados, $n_f$', fontsize=9)
    ax2.set_ylabel('$T$ (m²/día)', fontsize=9)
    ax2.set_title('$T = Q/(n_f\\,\\Delta h)$ — sensibilidad al conteo', fontsize=9.6)
    ax2.grid(alpha=.3, lw=.6); ax2.tick_params(labelsize=8)
    fig.suptitle('Problema 4.5 — transmisividad a partir de la red de flujo '
                 '(centro de bombeo B, figura 4.10)', fontsize=10.3, y=1.01)
    save(fig, 'fig_4_05_transmisividad')


# ================================================================ 4.6 / 4.7
def dam_case(blanket_start, dx=2.0, H=20.0):
    """Presa con delantal impermeable. Devuelve h, malla y Q/(K H)."""
    Lx, Lz = 300.0, 60.0
    nx, nz = int(Lx / dx) + 1, int(Lz / dx) + 1
    X = np.linspace(0, Lx, nx)
    Z = np.linspace(0, Lz, nz)
    hval = np.zeros((nz, nx))
    fixed = np.zeros((nz, nx), bool)
    top = nz - 1
    up = X <= blanket_start                     # lecho del embalse: h = H
    blank = (X > blanket_start) & (X <= 150)    # delantal impermeable
    dam = (X > 150) & (X <= 170)                # base de la presa
    down = X > 170                              # lecho aguas abajo: h = 0
    fixed[top, up] = True;   hval[top, up] = H
    fixed[top, down] = True; hval[top, down] = 0.0
    h, it, d = solve(hval, fixed, iters=40000, tol=1e-8)
    qx, qz = velocity(h, dx, dx)
    imid = np.argmin(np.abs(X - 160.0))
    Q = np.trapezoid(qx[:, imid], Z)            # caudal bajo la presa
    return dict(h=h, X=X, Z=Z, dx=dx, qx=qx, qz=qz, Q=Q, H=H,
                up=up, blank=blank, dam=dam, down=down,
                bstart=blanket_start, it=it, res=d)


def draw_dam(ax, c, nd=14, nf=5, labels=False, title=''):
    X, Z, h, H = c['X'], c['Z'], c['h'], c['H']
    Lx, Lz = X[-1], Z[-1]
    ax.set_aspect('equal')
    ax.add_patch(Rectangle((0, 0), Lx, Lz, fc=AQ, ec='none'))
    # equipotenciales
    lv = np.linspace(0, H, nd + 1)[1:-1]
    ax.contour(X, Z, h, levels=lv, colors=[CEQ], linewidths=.9)
    # lineas de corriente de caudal igual (arranque en el lecho del embalse)
    top = len(Z) - 1
    xin = X[c['up']]
    fin = np.abs(c['qz'][top, c['up']])
    x0 = equal_flux_starts(fin, xin, nf)
    for xx in x0:
        p = streamline(c['qx'], c['qz'], xx, Lz - 0.35, 0, 0, c['dx'], c['dx'],
                       Lx, Lz)
        ax.plot(p[:, 0], p[:, 1], '-', color=CFL, lw=1.5, zorder=4)
    # geometria
    ax.add_patch(Rectangle((0, -5), Lx, 5, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))
    if c['bstart'] < 150:
        ax.add_patch(Rectangle((c['bstart'], Lz - 1.6), 150 - c['bstart'], 3.2,
                               fc='#333', ec='k', lw=1, zorder=6))
    ax.add_patch(Polygon([(146, Lz), (170, Lz), (166, Lz + 17), (152, Lz + 17)],
                         fc='#c3b9a6', ec='k', lw=1.2, zorder=6))
    # agua
    ax.add_patch(Rectangle((0, Lz), 146, 20, fc=WATER, ec='none', zorder=2))
    ax.plot([0, 146], [Lz + 20] * 2, '-', color='#1a4e8a', lw=1.3, zorder=3)
    ax.add_patch(Rectangle((170, Lz), Lx - 170, 2.5, fc=WATER, ec='none', zorder=2))
    ax.plot([170, Lx], [Lz + 2.5] * 2, '-', color='#1a4e8a', lw=1.3, zorder=3)
    ax.plot([0, Lx], [Lz, Lz], '-', color='k', lw=1.2, zorder=5)

    if labels:
        pts = {'A': (2, Lz), 'B': (c['bstart'], Lz + 4), 'C': (150, Lz + 4),
               'D': (172, Lz), 'E': (Lx - 3, Lz), 'F': (2, 0), 'G': (Lx - 3, 0)}
        for k, (xx, zz) in pts.items():
            ax.text(xx, zz + 3.5, k, fontsize=11, fontweight='bold',
                    ha='center', zorder=9,
                    bbox=dict(fc='white', ec='k', lw=.7, alpha=.9, pad=1.4))
        ax.annotate('delantal impermeable (B–C)', xy=(112, Lz + 1.8),
                    xytext=(128, Lz + 33), fontsize=8.5, ha='center',
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1))
        ax.text(32, Lz + 26, 'nivel del embalse\n$H$ = 20 m', fontsize=8.5,
                color='#13335c', ha='center')
        ax.text(240, Lz + 9, 'nivel aguas abajo', fontsize=8.5, color='#13335c',
                ha='center')
        ax.text(Lx / 2, -11, 'base impermeable (F–G)', ha='center', va='top',
                fontsize=8.5)
    ax.set_xlim(-6, Lx + 6); ax.set_ylim(-18, Lz + 42)
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=9.6)


def fig_406_407():
    base = dam_case(60.0)
    half = dam_case(105.0)
    none_ = dam_case(150.0)
    K, H = 5e-4, 20.0
    print('    shape factors  base %.3f  half %.3f  none %.3f'
          % (base['Q'] / H, half['Q'] / H, none_['Q'] / H))
    for nm, c in [('base', base), ('half', half), ('none', none_)]:
        print(f'    {nm}: Q = {K*c["Q"]/1.0:.5e} m3/s por m   '
              f'(nf/nd = {c["Q"]/H:.3f})  iters={c["it"]}')

    # --- figura 4.6 (clasificacion de fronteras)
    fig, ax = plt.subplots(figsize=(9.6, 4.3))
    draw_dam(ax, base, nd=14, nf=5, labels=True)
    ax.set_title('Problema 4.6 — red de flujo y clasificación de fronteras\n'
                 'AB y DE: equipotenciales (carga constante)   ·   '
                 'BC, CD y FG: líneas de flujo (sin flujo)', fontsize=9.8)
    ax.plot([], [], '-', color=CEQ, lw=1.2, label='equipotenciales')
    ax.plot([], [], '-', color=CFL, lw=1.6, label='líneas de flujo (tubos de caudal igual)')
    ax.legend(fontsize=8.2, loc='lower center', ncol=2, framealpha=.95,
              bbox_to_anchor=(.5, -.07))
    save(fig, 'fig_4_06_presa')

    # --- figura 4.7 (comparacion)
    fig = plt.figure(figsize=(9.4, 8.2))
    g = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 1.15], hspace=.30)
    for k, (c, t) in enumerate([
            (base, 'Delantal COMPLETO (problema 6)'),
            (half, '(a) Delantal a la MITAD'),
            (none_, '(b) SIN delantal')]):
        ax = fig.add_subplot(g[k])
        draw_dam(ax, c, nd=14, nf=5)
        Qv = K * c['Q']
        ax.set_title(f'{t}   —   $Q = {Qv*1e3:.2f}\\times10^{{-3}}$ m³/s por metro  '
                     f'($= {Qv*86400:.0f}$ m³/día·m)', fontsize=9.4)
    ax = fig.add_subplot(g[3])
    names = ['Delantal\ncompleto', 'Delantal\na la mitad', 'Sin\ndelantal']
    Qs = np.array([K * base['Q'], K * half['Q'], K * none_['Q']])
    b = ax.bar(names, Qs * 1e3, color=['#2b8a3e', '#d9a400', '#b03030'],
               width=.5, ec='k', lw=.8)
    for r, q in zip(b, Qs):
        ax.text(r.get_x() + r.get_width() / 2, r.get_height() + .08,
                f'${q*1e3:.2f}\\times10^{{-3}}$ m³/s·m\n({q/Qs[0]*100:.0f} %)',
                ha='center', fontsize=8.6)
    ax.set_ylabel('$Q$ ($\\times10^{-3}$ m³/s por metro)', fontsize=9)
    ax.set_ylim(0, max(Qs) * 1e3 * 1.42)
    ax.grid(axis='y', alpha=.3, lw=.6); ax.tick_params(labelsize=8.5)
    ax.set_title('El delantal alarga la trayectoria de filtración: aumenta $n_d$ '
                 'sin cambiar $n_f$', fontsize=9.5)
    fig.suptitle('Problema 4.7 — filtración bajo la presa  '
                 '($K = 5\\times10^{-4}$ m/s, $H = 20$ m, solución por '
                 'diferencias finitas)', fontsize=10.4, y=.995)
    save(fig, 'fig_4_07_comparacion')
    return Qs


# ================================================================ 4.8
def fig_408():
    dx = 1.0
    Lx, Lz = 80.0, 40.0
    nx, nz = int(Lx / dx) + 1, int(Lz / dx) + 1
    X, Z = np.linspace(0, Lx, nx), np.linspace(0, Lz, nz)

    # (a) AB=60 arriba; DC izquierda=10; resto sin flujo
    hv = np.zeros((nz, nx)); fx = np.zeros((nz, nx), bool)
    fx[-1, :] = True; hv[-1, :] = 60.0
    left = X <= Lx / 2
    fx[0, left] = True; hv[0, left] = 10.0
    ha, _, _ = solve(hv, fx, iters=50000, tol=1e-9)

    # (b) AB=60 arriba; DC sin flujo; mitad inferior de los lados = 10
    hv2 = np.zeros((nz, nx)); fx2 = np.zeros((nz, nx), bool)
    fx2[-1, :] = True; hv2[-1, :] = 60.0
    low = Z <= Lz / 2
    fx2[low, 0] = True; hv2[low, 0] = 10.0
    fx2[low, -1] = True; hv2[low, -1] = 10.0
    hb, _, _ = solve(hv2, fx2, iters=50000, tol=1e-9)

    fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.5))
    for ax, h, mode, ttl in [
        (axs[0], ha, 'a', '(a) Salida sólo por la mitad izquierda de DC'),
        (axs[1], hb, 'b', '(b) Salida por los segmentos inferiores de AD y BC')]:
        ax.set_aspect('equal')
        ax.add_patch(Rectangle((0, 0), Lx, Lz, fc=AQ, ec='k', lw=1.4))
        ax.contour(X, Z, h, levels=np.linspace(10, 60, 11)[1:-1],
                   colors=[CEQ], linewidths=1.0)
        qx, qz = velocity(h, dx, dx)
        xin = X.copy(); fin = np.abs(qz[-1, :])
        x0 = equal_flux_starts(fin, xin, 7)
        for xx in x0:
            p = streamline(qx, qz, xx, Lz - 0.4, 0, 0, dx, dx, Lx, Lz)
            ax.plot(p[:, 0], p[:, 1], '-', color=CFL, lw=1.5)
        # bordes
        ax.plot([0, Lx], [Lz, Lz], '-', color=CEQ, lw=4, solid_capstyle='butt')
        ax.text(Lx / 2, Lz + 1.6, 'A  —  $h = 60$ m (carga constante)  —  B',
                ha='center', fontsize=8.6, color=CEQ)
        if mode == 'a':
            ax.plot([0, Lx / 2], [0, 0], '-', color=CEQ, lw=4, solid_capstyle='butt')
            ax.plot([Lx / 2, Lx], [0, 0], '-', color='#333', lw=4,
                    solid_capstyle='butt')
            ax.text(Lx / 4, -2.2, 'D — $h=10$ m', ha='center', va='top',
                    fontsize=8.4, color=CEQ)
            ax.text(3 * Lx / 4, -2.2, 'impermeable — C', ha='center', va='top',
                    fontsize=8.4, color='#333')
            ax.plot([0, 0], [0, Lz], '-', color='#333', lw=4, solid_capstyle='butt')
            ax.plot([Lx, Lx], [0, Lz], '-', color='#333', lw=4, solid_capstyle='butt')
            ax.text(3 * Lx / 4, Lz / 3, 'zona casi\nestancada', ha='center',
                    fontsize=8, color='#555',
                    bbox=dict(fc='white', ec='none', alpha=.8, pad=1.5))
            ax.plot(Lx / 2, 0, '*', ms=15, color='#d9a400', zorder=7)
            ax.annotate('singularidad\n($i\\to\\infty$)', xy=(Lx / 2, 0),
                        xytext=(Lx / 2 + 13, 9), fontsize=7.8, color='#8a6a00',
                        arrowprops=dict(arrowstyle='-|>', color='#8a6a00', lw=1))
        else:
            ax.plot([0, Lx], [0, 0], '-', color='#333', lw=4, solid_capstyle='butt')
            ax.text(Lx / 2, -2.2, 'D — impermeable — C', ha='center', va='top',
                    fontsize=8.4, color='#333')
            for xx in (0, Lx):
                ax.plot([xx, xx], [0, Lz / 2], '-', color=CEQ, lw=4,
                        solid_capstyle='butt')
                ax.plot([xx, xx], [Lz / 2, Lz], '-', color='#333', lw=4,
                        solid_capstyle='butt')
            ax.text(-1.6, Lz / 4, '$h=10$', rotation=90, ha='right',
                    va='center', fontsize=8.4, color=CEQ)
            ax.text(-1.6, 3 * Lz / 4, 'imperm.', rotation=90, ha='right',
                    va='center', fontsize=8.4, color='#333')
            ax.text(Lx + 1.6, Lz / 4, '$h=10$', rotation=90, ha='left',
                    va='center', fontsize=8.4, color=CEQ)
            ax.text(Lx + 1.6, 3 * Lz / 4, 'imperm.', rotation=90, ha='left',
                    va='center', fontsize=8.4, color='#333')
            ax.plot([Lx / 2, Lx / 2], [0, Lz], '--', color='#2b8a3e', lw=1.6)
            ax.text(Lx / 2, Lz * .42, 'divisoria de flujo\n(línea de flujo)',
                    ha='center', fontsize=8, color='#1b5e20', rotation=90,
                    va='center',
                    bbox=dict(fc='white', ec='none', alpha=.85, pad=1.2))
        ax.set_xlim(-11, Lx + 11); ax.set_ylim(-9, Lz + 6)
        ax.axis('off'); ax.set_title(ttl, fontsize=9.5)
    fig.suptitle('Problema 4.8 — redes de flujo (solución numérica de $\\nabla^2h=0$)',
                 fontsize=10.4, y=1.0)
    save(fig, 'fig_4_08_redes')


# ================================================================ 4.9 / 4.10
def wt_case(Kx=1.0, Kz=1.0, dx=0.5):
    """Seccion con nivel freatico inclinado: AD = 40, BC = 60, DC = 120.
    AB es nivel freatico con h = z ; AD, BC, DC sin flujo."""
    Lx, zA, zB = 120.0, 40.0, 60.0
    nx = int(Lx / dx) + 1
    nz = int(zB / dx) + 1
    X, Z = np.linspace(0, Lx, nx), np.linspace(0, zB, nz)
    ztop = zA + (zB - zA) * X / Lx
    hv = np.zeros((nz, nx)); fx = np.zeros((nz, nx), bool)
    inact = np.zeros((nz, nx), bool)
    for i, xx in enumerate(X):
        kt = int(np.floor(ztop[i] / dx))
        kt = min(kt, nz - 1)
        fx[kt, i] = True; hv[kt, i] = Z[kt]        # h = z en el nivel freatico
        if kt + 1 < nz:
            inact[kt + 1:, i] = True
    h, it, d = solve(hv, fx, inactive=inact, Kx=Kx, Kz=Kz, iters=60000, tol=1e-9)
    qx, qz = velocity(h, dx, dx, Kx=Kx, Kz=Kz)
    hm = np.ma.array(h, mask=inact)
    return dict(X=X, Z=Z, h=h, hm=hm, qx=qx, qz=qz, dx=dx, ztop=ztop,
                inact=inact, fx=fx, Lx=Lx, zA=zA, zB=zB, it=it)


def draw_wt(ax, c, nlev=20, nf=7, aniso=False):
    X, Z, hm, ztop = c['X'], c['Z'], c['hm'], c['ztop']
    ax.set_aspect('equal')
    ax.fill_between(X, 0, ztop, color=AQ, zorder=0)
    hmin, hmax = float(hm.min()), float(hm.max())
    ax.contour(X, Z, hm, levels=np.linspace(hmin, hmax, nlev + 2)[1:-1],
               colors=[CEQ], linewidths=1.0, zorder=3)
    # arranque de lineas de corriente: en la mitad de recarga del nivel freatico
    qzt = np.array([c['qz'][max(min(int(np.floor(zt / c['dx'])), len(Z) - 1) - 6, 0), i]
                    for i, zt in enumerate(ztop)])
    rech = qzt < 0            # flujo descendente = recarga
    if rech.sum() > 3:
        x0 = equal_flux_starts(np.abs(qzt[rech]), X[rech], nf)
    else:
        x0 = np.linspace(X[len(X) // 2], X[-2], nf)
    for xx in x0:
        zz = np.interp(xx, X, ztop) - 3.0
        p = streamline(c['qx'], c['qz'], xx, zz, 0, 0, c['dx'], c['dx'],
                       c['Lx'], c['zB'])
        p = smooth_path(p, 25)
        ax.plot(p[:, 0], p[:, 1], '-', color=CFL, lw=1.5, zorder=4)
    ax.plot(X, ztop, '-', color='#2b8a3e', lw=2.2, zorder=5)
    ax.fill_between(X, ztop, c['zB'] + 10, color='white', zorder=2)
    ax.plot(X, ztop, '-', color='#2b8a3e', lw=2.2, zorder=5)
    ax.add_patch(Rectangle((0, -4), c['Lx'], 4, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///', zorder=5))
    ax.plot([0, 0], [0, c['zA']], '-', color='#333', lw=3.5, zorder=6)
    ax.plot([c['Lx'], c['Lx']], [0, c['zB']], '-', color='#333', lw=3.5, zorder=6)
    ax.text(-3, c['zA'] / 2, 'AD\nsin flujo', rotation=90, ha='right',
            va='center', fontsize=8.2)
    ax.text(c['Lx'] + 3, c['zB'] / 2, 'BC\nsin flujo', rotation=90, ha='left',
            va='center', fontsize=8.2)
    ax.text(c['Lx'] / 2, -6, 'DC  sin flujo', ha='center', va='top', fontsize=8.4)
    ax.text(2, c['zA'] + 3, 'A', fontsize=11, fontweight='bold')
    ax.text(c['Lx'] - 4, c['zB'] + 3, 'B', fontsize=11, fontweight='bold')
    ax.text(c['Lx'] * .33, c['zA'] + 8.0, 'nivel freático:  $h = z$',
            color='#1b5e20', fontsize=9, ha='center', zorder=8)
    for k in range(4):
        xa = c['Lx'] * (.70 + k * .075)
        za = np.interp(xa, X, ztop)
        ax.annotate('', xy=(xa, za - 6), xytext=(xa, za + 7),
                    arrowprops=dict(arrowstyle='-|>', color='#1b5e20', lw=1.5),
                    zorder=7)
    ax.text(c['Lx'] * .80, c['zB'] + 10, 'RECARGA', fontsize=8.6,
            color='#1b5e20', ha='center', fontweight='bold', zorder=8)
    for k in range(3):
        xa = c['Lx'] * (.035 + k * .055)
        za = np.interp(xa, X, ztop)
        ax.annotate('', xy=(xa, za + 7), xytext=(xa, za - 6),
                    arrowprops=dict(arrowstyle='-|>', color='#8a3b00', lw=1.5),
                    zorder=7)
    ax.text(c['Lx'] * .10, c['zA'] + 12, 'DESCARGA', fontsize=8.6,
            color='#8a3b00', ha='center', fontweight='bold', zorder=8)
    ax.set_xlim(-12, c['Lx'] + 13); ax.set_ylim(-13, c['zB'] + 20)
    ax.axis('off')


def fig_409_410():
    iso = wt_case(1.0, 1.0)
    ani = wt_case(5.0, 1.0)

    fig, ax = plt.subplots(figsize=(9.4, 4.2))
    draw_wt(ax, iso)
    ax.set_title('Problema 4.9 — red de flujo con nivel freático inclinado '
                 '(medio isótropo)\nLas equipotenciales cortan el nivel freático '
                 'donde $h = z$, no a 90°', fontsize=9.8)
    save(fig, 'fig_4_09_freatico')

    fig, axs = plt.subplots(2, 1, figsize=(9.4, 7.6))
    draw_wt(axs[0], iso)
    axs[0].set_title('ISÓTROPO ($K_h = K_v$) — celdas cuadradas, '
                     'intersecciones a 90°', fontsize=9.6)
    draw_wt(axs[1], ani, aniso=True)
    axs[1].set_title('ANISÓTROPO ($K_h = 5K_v$) — el flujo se aplana, los sistemas '
                     'son más someros y extensos\n$K_{eq}=\\sqrt{K_hK_v}=2.24\\,K_v$   ·   '
                     'sección transformada: $x\' = x\\sqrt{K_v/K_h} = 0.447\\,x$',
                     fontsize=9.6)
    fig.suptitle('Problema 4.10 — efecto de la anisotropía sobre la red de flujo',
                 fontsize=10.4, y=1.0)
    fig.tight_layout()
    save(fig, 'fig_4_10_anisotropo')

    # transformed-section schematic
    fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.4))
    for ax, sx, ttl in [(axs[0], 0.447, "Sección TRANSFORMADA  $x'=0.447x$\n"
                                        'celdas CUADRADAS, cortes a 90°'),
                        (axs[1], 1.0, 'Sección REAL (destransformada)\n'
                                      'celdas 2.24 veces más anchas')]:
        ax.set_aspect('equal'); ax.axis('off')
        for i in range(5):
            for j in range(3):
                ax.add_patch(Rectangle((i * sx, j), sx, 1, fc=AQ, ec=CEQ, lw=1.2))
        ax.set_xlim(-.4, 5.4); ax.set_ylim(-.9, 3.9)
        ax.set_title(ttl, fontsize=9.3)
        ax.text(2.5 * sx, -.45, f'relación de lados = {1/sx:.2f} : 1',
                ha='center', va='top', fontsize=8.6)
    save(fig, 'fig_4_10_transformada')


print('cap4:')
fig_404()
fig_405()
Qs = fig_406_407()
fig_408()
fig_409_410()
print('cap4 ok')

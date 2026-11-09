import os
os.environ['MPLCONFIGDIR'] = '/tmp/mplcfg'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import pi, log, log10, sqrt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Circle
import sys
sys.path.insert(0, '/projects/sandbox/.calc')
from pumping_lib import W

OUT = '/projects/sandbox/.calc/fig'
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans',
                     'axes.linewidth': .8, 'savefig.dpi': 200,
                     'savefig.bbox': 'tight', 'savefig.pad_inches': .15})
AQ, CLAY, WATER, SOIL = '#d6e4f0', '#cfc8bd', '#bcd9ef', '#e8e2d8'
CB, CR, CG, CY = '#1a4e8a', '#b03030', '#2b8a3e', '#d9a400'

Q, r_obs, T, S, b_aq = 1500.0, 50.0, 300.0, 1.0e-3, 25.0
t_min = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60, 90, 120,
                  180, 240, 360, 480, 720, 1080, 1440], float)
t_d = t_min / 1440.0
u_obs = r_obs ** 2 * S / (4 * T * t_d)
s_obs = Q / (4 * pi * T) * W(u_obs)


def save(f, n):
    f.savefig(f'{OUT}/{n}.png', facecolor='white'); plt.close(f); print('  ->', n)


# ================================================================ 1 esquema
def fig_esquema():
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    ax.axis('off')
    X = np.linspace(-320, 320, 700)
    R0 = sqrt(2.25 * T * 1.0 / S)
    sd = np.where(np.abs(X) < .3, 8.2,
                  Q / (4 * pi * T) * W(np.abs(X) ** 2 * S / (4 * T * 1.0)))
    sd = np.clip(sd, 0, 9)
    top = 34.0
    ax.add_patch(Rectangle((-320, 25), 640, 9, fc=CLAY, ec='k', lw=1, hatch='xx'))
    ax.add_patch(Rectangle((-320, 0), 640, 25, fc=AQ, ec='k', lw=1.2))
    ax.add_patch(Rectangle((-320, -4), 640, 4, fc='#8a8a8a', ec='k', lw=1,
                           hatch='///'))
    ax.text(-310, 29.5, 'capa confinante', fontsize=8.3)
    ax.text(-310, 12, 'ACUÍFERO CONFINADO\n$b = 25$ m,  $T = Kb$,  $S$',
            fontsize=8.8, va='center')
    # superficie piezometrica
    ax.plot(X, top + 6 - sd, '-', color=CB, lw=2.3, zorder=5)
    ax.axhline(top + 6, color='#888', ls=':', lw=1.4)
    ax.text(300, top + 6.4, 'nivel piezométrico inicial', fontsize=8.3,
            color='#555', ha='right')
    ax.text(150, top + 6 - 1.0, 'cono de abatimiento', fontsize=8.6, color=CB,
            ha='center')
    # pozo
    ax.add_patch(Rectangle((-3, 0), 6, top + 9, fc='white', ec='k', lw=1.4,
                           zorder=6))
    ax.add_patch(Rectangle((-3, 0), 6, top + 6 - 8.2, fc=WATER, ec='none',
                           zorder=7))
    for y in np.arange(2, 24, 3):
        ax.plot([-3, 3], [y, y], '-', color='#555', lw=.8, zorder=8)
    ax.text(0, top + 10.5, 'POZO\n$Q$', ha='center', fontsize=9.5,
            fontweight='bold', color=CR)
    ax.annotate('', xy=(0, top + 14), xytext=(0, top + 9.5),
                arrowprops=dict(arrowstyle='-|>', color=CR, lw=2.6))
    # piezometro de observacion
    ax.add_patch(Rectangle((r_obs - 1.6, 0), 3.2, top + 9, fc='white', ec='k',
                           lw=1.2, zorder=6))
    sm = Q / (4 * pi * T) * float(W(r_obs ** 2 * S / (4 * T * 1.0)))
    ax.add_patch(Rectangle((r_obs - 1.6, 0), 3.2, top + 6 - sm, fc=WATER,
                           ec='none', zorder=7))
    ax.text(r_obs, top + 10.5, 'piezómetro\n$r = 50$ m', ha='center',
            fontsize=8.6, color=CB)
    ax.annotate('', xy=(r_obs + 14, top + 6), xytext=(r_obs + 14, top + 6 - sm),
                arrowprops=dict(arrowstyle='<|-|>', color=CR, lw=1.3))
    ax.text(r_obs + 18, top + 6 - sm / 2, '$s$ = abatimiento', fontsize=8.8,
            color=CR, va='center')
    # flechas de flujo radial
    for xx in [-280, -210, -140, 210, 280]:
        d = -1 if xx < 0 else 1
        ax.annotate('', xy=(xx - 45 * d, 13), xytext=(xx, 13),
                    arrowprops=dict(arrowstyle='-|>', color=CB, lw=1.7))
    ax.annotate('', xy=(-R0 * .62, top + 7.6), xytext=(R0 * .62, top + 7.6),
                arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=1.2))
    ax.text(0, top + 8.2, f'$2R_0$   ($R_0=\\sqrt{{2.25Tt/S}}$ = {R0:.0f} m '
                          'a 1 día)', ha='center', fontsize=8.5, color=CG)
    ax.set_xlim(-340, 345); ax.set_ylim(-9, top + 17)
    ax.set_title('Geometría de una prueba de bombeo en acuífero confinado',
                 fontsize=10.4)
    save(fig, 'fig_b1_esquema')


# ================================================================ 2 Cooper-Jacob
def fig_cj():
    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    val = u_obs < 0.01
    A = np.polyfit(np.log10(t_d[val]), s_obs[val], 1)
    ds, t0 = A[0], 10 ** (-A[1] / A[0])
    Tf = 2.303 * Q / (4 * pi * ds)
    Sf = 2.25 * Tf * t0 / r_obs ** 2

    tl = np.logspace(log10(t0 * .5), log10(2.2), 200)
    ax.semilogx(t_min, s_obs, 'o', ms=7, mfc='white', mec=CB, mew=1.8,
                label='datos medidos', zorder=5)
    ax.semilogx(t_d[val] * 1440, s_obs[val], 'o', ms=7, color=CB,
                label='puntos con $u<0.01$ (se usan para la recta)', zorder=6)
    ax.semilogx(tl * 1440, np.polyval(A, np.log10(tl)), '-', color=CR, lw=2.0,
                label='recta de Cooper-Jacob', zorder=4)
    ax.axhline(0, color='k', lw=1.0)

    # t0
    ax.plot([t0 * 1440], [0], 'D', ms=9, mfc=CY, mec='k', mew=1.2, zorder=7)
    ax.annotate(f'$t_0$ = {t0*1440:.1f} min\n(= {t0:.5f} d)',
                xy=(t0 * 1440, 0), xytext=(1.5, 0.75), fontsize=9, color='#8a6a00',
                arrowprops=dict(arrowstyle='-|>', color='#8a6a00', lw=1.2))
    # delta s por ciclo
    ta, tb = 100.0, 1000.0
    sa = np.polyval(A, np.log10(ta / 1440)); sb = np.polyval(A, np.log10(tb / 1440))
    ax.plot([ta, tb], [sa, sa], '--', color=CG, lw=1.4)
    ax.plot([tb, tb], [sa, sb], '-', color=CG, lw=2.4)
    ax.annotate('', xy=(tb, sb), xytext=(tb, sa),
                arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=1.8))
    ax.text(tb * 1.12, (sa + sb) / 2, f'$\\Delta s$ = {ds:.2f} m\npor ciclo\n'
                                      'logarítmico', fontsize=9, color='#1b5e20',
            va='center')
    ax.text(sqrt(ta * tb), sa - 0.13, '1 ciclo log', ha='center', fontsize=8.4,
            color='#1b5e20')

    # zona no valida
    tlim = t_min[val].min()
    ax.axvspan(0.7, tlim, color=CR, alpha=.07)
    ax.text(28, 2.33, 'zona sombreada: $u>0.01$, la aproximación de '
            'Cooper-Jacob NO vale', fontsize=8.6, color=CR, ha='center',
            bbox=dict(fc='white', ec=CR, lw=.8, alpha=.95, pad=2.5))

    box = (f'$T=\\dfrac{{2.303\\,Q}}{{4\\pi\\,\\Delta s}}='
           f'\\dfrac{{2.303(1500)}}{{4\\pi({ds:.2f})}}={Tf:.0f}$ m²/día\n\n'
           f'$S=\\dfrac{{2.25\\,T\\,t_0}}{{r^2}}=\\dfrac{{2.25({Tf:.0f})({t0:.5f})}}'
           f'{{50^2}}={Sf*1e4:.2f}\\times10^{{-4}}$')
    ax.text(0.985, 0.045, box, transform=ax.transAxes, ha='right', va='bottom',
            fontsize=10,
            bbox=dict(fc='#f3f7fb', ec=CB, lw=1.1, pad=5))

    ax.set_xlabel('tiempo $t$ (minutos)  —  escala logarítmica', fontsize=9.5)
    ax.set_ylabel('abatimiento $s$ (m)', fontsize=9.5)
    ax.set_xlim(0.7, 2200); ax.set_ylim(-0.25, 2.55)
    ax.grid(which='both', alpha=.3, lw=.5)
    ax.legend(fontsize=8.6, loc='upper left', framealpha=.95)
    ax.set_title('Método de Cooper-Jacob — $Q = 1500$ m³/día,  $r = 50$ m\n'
                 'Es el método que hay que dominar: una recta en papel semilog',
                 fontsize=10.3)
    save(fig, 'fig_b2_cooper_jacob')
    return Tf, Sf, ds, t0


# ================================================================ 3 Theis
def fig_theis():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.6))
    uu = np.logspace(-9, 0.3, 400)
    ax.loglog(1 / uu, W(uu), '-', color=CB, lw=2.4)
    ax.set_xlabel('$1/u$', fontsize=9.5)
    ax.set_ylabel('$W(u)$', fontsize=9.5)
    ax.grid(which='both', alpha=.3, lw=.5)
    ax.set_title('Curva patrón de Theis\n$W(u)$ frente a $1/u$', fontsize=9.8)
    # punto de coincidencia conveniente
    ax.plot([100], [float(W(1e-2))], 'o', ms=11, mfc='none', mec=CR, mew=2.4)
    ax.annotate('punto de\ncoincidencia\n$W=1$, $1/u=10$', xy=(10, 1.0),
                xytext=(1.6, 4.5), fontsize=8.4, color=CR,
                arrowprops=dict(arrowstyle='-|>', color=CR, lw=1.1))
    ax.plot([10], [1.0], 'o', ms=11, mfc='none', mec=CR, mew=2.4)
    ax.annotate('', xy=(100, float(W(1e-2))), xytext=(10, 1.0),
                arrowprops=dict(arrowstyle='-', color=CR, lw=.8, ls=':'))
    ax.set_xlim(1, 1e9); ax.set_ylim(1e-2, 50)

    ax2.loglog(t_min, s_obs, 'o', ms=7, mfc='white', mec=CB, mew=1.8)
    tl = np.logspace(log10(0.8), log10(2000), 300)
    sl = Q / (4 * pi * T) * W(r_obs ** 2 * S / (4 * T * tl / 1440))
    ax2.loglog(tl, sl, '-', color=CR, lw=1.6, alpha=.75)
    ax2.set_xlabel('$t$ (min)', fontsize=9.5)
    ax2.set_ylabel('$s$ (m)', fontsize=9.5)
    ax2.grid(which='both', alpha=.3, lw=.5)
    ax2.set_title('Datos  $s$ frente a $t$  (misma escala log-log)\n'
                  'se superponen y se lee el punto de coincidencia',
                  fontsize=9.8)
    ax2.text(.04, .93, '$T=\\dfrac{Q\\,W(u)}{4\\pi\\,s}$\n\n'
                       '$S=\\dfrac{4\\,T\\,t\\,u}{r^{2}}$',
             transform=ax2.transAxes, fontsize=11, va='top',
             bbox=dict(fc='#f3f7fb', ec=CB, lw=1.0, pad=4))
    fig.suptitle('Método de Theis (curva patrón) — el general, válido para '
                 'cualquier $u$', fontsize=10.4, y=1.02)
    save(fig, 'fig_b3_theis')


# ================================================================ 4 distancia
def fig_dist():
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    rr = np.array([10., 30., 50., 100., 200., 300.])
    uu = rr ** 2 * S / (4 * T * 1.0)
    ss = Q / (4 * pi * T) * W(uu)
    val = uu < 0.01
    B = np.polyfit(np.log10(rr[val]), ss[val], 1)
    ds_r, r0 = -B[0], 10 ** (-B[1] / B[0])
    Tf = 2.303 * Q / (2 * pi * ds_r)
    Sf = 2.25 * Tf * 1.0 / r0 ** 2
    rl = np.logspace(0.7, log10(r0 * 1.25), 200)
    ax.semilogx(rr, ss, 'o', ms=7, mfc='white', mec=CB, mew=1.8,
                label='piezómetros (t = 1 día)')
    ax.semilogx(rr[val], ss[val], 'o', ms=7, color=CB,
                label='con $u<0.01$')
    ax.semilogx(rl, np.polyval(B, np.log10(rl)), '-', color=CR, lw=2.0,
                label='recta distancia–abatimiento')
    ax.axhline(0, color='k', lw=1.0)
    ax.plot([r0], [0], 'D', ms=9, mfc=CY, mec='k', mew=1.2, zorder=6)
    ax.annotate(f'$r_0$ = {r0:.0f} m  (radio de influencia)', xy=(r0, 0),
                xytext=(r0 * .32, .52), fontsize=9, color='#8a6a00',
                arrowprops=dict(arrowstyle='-|>', color='#8a6a00', lw=1.2))
    ra, rb = 20.0, 200.0
    sa = np.polyval(B, log10(ra)); sb = np.polyval(B, log10(rb))
    ax.plot([ra, rb], [sa, sa], '--', color=CG, lw=1.4)
    ax.annotate('', xy=(rb, sb), xytext=(rb, sa),
                arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=1.8))
    ax.text(rb * 1.1, (sa + sb) / 2, f'$\\Delta s_r$ = {ds_r:.2f} m\npor ciclo de $r$',
            fontsize=9, color='#1b5e20', va='center')
    ax.text(.03, .055, f'$T=\\dfrac{{2.303\\,Q}}{{2\\pi\\,\\Delta s_r}}={Tf:.0f}$ '
                       'm²/día       '
                       f'$S=\\dfrac{{2.25\\,T\\,t}}{{r_0^{{2}}}}='
                       f'{Sf*1e4:.2f}\\times10^{{-4}}$',
            transform=ax.transAxes, fontsize=10.5, va='bottom',
            bbox=dict(fc='#f3f7fb', ec=CB, lw=1.1, pad=5))
    ax.set_xlabel('distancia radial $r$ (m)  —  escala logarítmica', fontsize=9.5)
    ax.set_ylabel('abatimiento $s$ (m)', fontsize=9.5)
    ax.grid(which='both', alpha=.3, lw=.5)
    ax.legend(fontsize=8.6, loc='upper right', framealpha=.95)
    ax.set_ylim(-0.3, 4.1)
    ax.set_title('Método distancia–abatimiento (varios piezómetros, un solo '
                 'tiempo)\nOjo: el denominador es $2\\pi$, no $4\\pi$',
                 fontsize=10.3)
    save(fig, 'fig_b4_distancia')


# ================================================================ 5 recuperacion
def fig_rec():
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    tp = 1.0
    tpr = np.array([5, 10, 20, 30, 60, 120, 240, 480], float) / 1440
    rw = 0.15
    u1 = rw ** 2 * S / (4 * T * (tp + tpr))
    u2 = rw ** 2 * S / (4 * T * tpr)
    sp = Q / (4 * pi * T) * (W(u1) - W(u2))
    rat = (tp + tpr) / tpr
    C = np.polyfit(np.log10(rat), sp, 1)
    ds = C[0]; Tf = 2.303 * Q / (4 * pi * ds)
    xl = np.logspace(0, log10(500), 100)
    ax.semilogx(rat, sp, 'o', ms=7, mfc='white', mec=CB, mew=1.8,
                label="datos de recuperación")
    ax.semilogx(xl, np.polyval(C, np.log10(xl)), '-', color=CR, lw=2.0,
                label='recta de recuperación')
    ax.axhline(0, color='k', lw=1.0)
    a, bb = 10.0, 100.0
    sa = np.polyval(C, log10(a)); sb = np.polyval(C, log10(bb))
    ax.plot([a, bb], [sa, sa], '--', color=CG, lw=1.4)
    ax.annotate('', xy=(bb, sb), xytext=(bb, sa),
                arrowprops=dict(arrowstyle='<|-|>', color=CG, lw=1.8))
    ax.text(bb * 1.12, (sa + sb) / 2, f"$\\Delta s'$ = {ds:.2f} m\npor ciclo",
            fontsize=9, color='#1b5e20', va='center')
    ax.text(.035, .07, f"$T=\\dfrac{{2.303\\,Q}}{{4\\pi\\,\\Delta s'}}={Tf:.0f}$ "
                       'm²/día\n\nLa recuperación da $T$,  pero NO da $S$',
            transform=ax.transAxes, fontsize=10.5, va='bottom',
            bbox=dict(fc='#f3f7fb', ec=CB, lw=1.1, pad=5))
    ax.set_xlabel("$t/t'$   (t = desde que arrancó la bomba,  "
                  "t' = desde que paró)", fontsize=9.5)
    ax.set_ylabel("abatimiento residual $s'$ (m)", fontsize=9.5)
    ax.grid(which='both', alpha=.3, lw=.5)
    ax.legend(fontsize=8.8, loc='upper left', framealpha=.95)
    ax.set_xlim(1, 500); ax.set_ylim(-0.12, 2.6)
    ax.set_title('Método de recuperación de Theis — se mide en el propio pozo '
                 'tras parar la bomba\nNo hace falta medir el caudal durante la '
                 'recuperación: es el método más barato', fontsize=10.3)
    save(fig, 'fig_b5_recuperacion')


# ================================================================ 6 cono
def fig_cono():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.4),
                                  gridspec_kw=dict(width_ratios=[1.1, 1]))
    rr = np.logspace(-0.8, 3.9, 400)
    for t, c, lab in [(1 / 24, CY, '1 hora'), (1., CG, '1 día'),
                      (30., CB, '30 días'), (365., CR, '1 año')]:
        ss = Q / (4 * pi * T) * W(rr ** 2 * S / (4 * T * t))
        ax.semilogx(rr, -ss, '-', color=c, lw=2.1, label=lab)
        R0 = sqrt(2.25 * T * t / S)
        ax.plot([R0], [0], 'v', ms=7, color=c)
    ax.axhline(0, color='k', lw=1.1)
    ax.set_xlabel('$r$ (m)', fontsize=9.5)
    ax.set_ylabel('$-s$  (descenso del nivel, m)', fontsize=9.5)
    ax.legend(fontsize=8.6, title='tiempo de bombeo', title_fontsize=8.2)
    ax.grid(which='both', alpha=.3, lw=.5)
    ax.set_title('El cono crece sin parar: nunca hay régimen\npermanente en un '
                 'acuífero confinado ideal', fontsize=9.8)
    ax.text(.03, .08, 'los triángulos marcan\n$R_0=\\sqrt{2.25Tt/S}$',
            transform=ax.transAxes, fontsize=8.4, va='bottom')

    tt = np.logspace(-2, 3, 300)
    R0 = np.sqrt(2.25 * T * tt / S)
    ax2.loglog(tt, R0, '-', color=CB, lw=2.3)
    for t in [1, 30, 365]:
        R = sqrt(2.25 * T * t / S)
        ax2.plot([t], [R], 'o', ms=8, mfc='white', mec=CR, mew=2)
        ax2.annotate(f'{t} d → {R:.0f} m', xy=(t, R), xytext=(t * 1.35, R * .62),
                     fontsize=8.6, color=CR)
    ax2.set_xlabel('tiempo (días)', fontsize=9.5)
    ax2.set_ylabel('$R_0$ (m)', fontsize=9.5)
    ax2.grid(which='both', alpha=.3, lw=.5)
    ax2.set_title('Radio de influencia  $R_0\\propto\\sqrt{t}$\n'
                  'cuadruplicar el tiempo duplica $R_0$', fontsize=9.8)
    fig.suptitle('Cálculos en el acuífero (1): evolución del cono de abatimiento  '
                 '— $T=300$ m²/día, $S=10^{-3}$, $Q=1500$ m³/día',
                 fontsize=10.3, y=1.02)
    save(fig, 'fig_b6_cono')


# ================================================================ 7 superposicion
def fig_super():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.5))
    wells = [(0., 0.), (300., 0.), (150., 260.)]
    x = np.linspace(-200, 500, 300)
    y = np.linspace(-200, 460, 290)
    Xg, Yg = np.meshgrid(x, y)
    tot = np.zeros_like(Xg)
    for xw, yw in wells:
        d = np.sqrt((Xg - xw) ** 2 + (Yg - yw) ** 2)
        d = np.maximum(d, 0.15)
        tot += Q / (4 * pi * T) * W(d ** 2 * S / (4 * T * 30.0))
    cf = ax.contourf(Xg, Yg, tot, levels=np.arange(2, 13, .5), cmap='YlGnBu',
                     extend='both')
    cs = ax.contour(Xg, Yg, tot, levels=np.arange(3, 13, 1), colors='k',
                    linewidths=.6)
    ax.clabel(cs, fmt='%.0f', fontsize=7.5)
    plt.colorbar(cf, ax=ax, label='abatimiento total $s$ (m)')
    for i, (xw, yw) in enumerate(wells, 1):
        ax.plot(xw, yw, 'o', ms=10, mfc=CR, mec='k', mew=1.4, zorder=5)
        ax.text(xw, yw + 24, f'P{i}', ha='center', fontsize=9.5,
                fontweight='bold')
    P = (150., 86.7)
    ax.plot(*P, '*', ms=16, color='white', mec='k', mew=1.2, zorder=6)
    ax.text(P[0] + 18, P[1] - 6, 'punto A\n$s=7.77$ m', fontsize=8.6)
    ax.set_aspect('equal'); ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)')
    ax.tick_params(labelsize=8)
    ax.set_title('Tres pozos de 1500 m³/día a los 30 días\nel abatimiento se '
                 'SUMA (superposición)', fontsize=9.7)

    ax2.axis('off')
    ax2.text(.02, .97, 'Superposición', fontsize=12, fontweight='bold',
             va='top', color=CB)
    ax2.text(.02, .88, 'La ecuación de flujo es LINEAL, de modo que los\n'
                       'abatimientos de varios pozos simplemente se suman:',
             fontsize=9.3, va='top')
    ax2.text(.5, .70, '$s_{total}=\\sum_i \\dfrac{Q_i}{4\\pi T}W(u_i)$\n\n'
                      '$u_i=\\dfrac{r_i^{2}S}{4Tt}$',
             fontsize=12.5, ha='center', va='center',
             bbox=dict(fc='#f3f7fb', ec=CB, lw=1.1, pad=6))
    rows = [('pozo P1', '173.3 m', '2.591 m'),
            ('pozo P2', '173.3 m', '2.591 m'),
            ('pozo P3', '173.3 m', '2.591 m'),
            ('TOTAL en A', '—', '7.774 m')]
    yy = .50
    ax2.text(.07, yy, 'contribución', fontsize=9, fontweight='bold')
    ax2.text(.45, yy, '$r_i$', fontsize=9, fontweight='bold')
    ax2.text(.72, yy, '$s_i$', fontsize=9, fontweight='bold')
    for k, (a, bb, c) in enumerate(rows):
        yy2 = .50 - (k + 1) * .075
        w = 'bold' if 'TOTAL' in a else 'normal'
        ax2.text(.07, yy2, a, fontsize=9, fontweight=w)
        ax2.text(.45, yy2, bb, fontsize=9, fontweight=w)
        ax2.text(.72, yy2, c, fontsize=9, fontweight=w,
                 color=CR if 'TOTAL' in a else 'k')
    ax2.plot([.05, .92], [.455, .455], '-', color='k', lw=.9)
    ax2.plot([.05, .92], [.165, .165], '-', color='k', lw=.9)
    ax2.text(.02, .09, 'La interferencia triplica el abatimiento respecto a un\n'
                       'pozo aislado. Por eso los campos de pozos se diseñan con\n'
                       'separación suficiente: cada pozo le roba carga al vecino.',
             fontsize=9, va='top', color='#333')
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    save(fig, 'fig_b7_superposicion')


# ================================================================ 8 fronteras
def fig_imagen():
    fig, axs = plt.subplots(1, 2, figsize=(9.8, 4.3))
    for ax, kind in zip(axs, ['barrera', 'rio']):
        ax.set_aspect('equal'); ax.axis('off')
        d = 150.0
        ax.plot([d, d], [-170, 170], '-',
                color='#333' if kind == 'barrera' else CB, lw=4)
        if kind == 'barrera':
            for yy in np.arange(-150, 160, 30):
                ax.plot([d, d + 14], [yy, yy + 10], '-', color='#333', lw=1.2)
            ax.text(d + 30, 150, 'frontera\nIMPERMEABLE', fontsize=9,
                    color='#333', fontweight='bold')
        else:
            ax.add_patch(Rectangle((d, -170), 95, 340, fc=WATER, ec='none'))
            ax.text(d + 46, 150, 'RÍO\n(carga constante)', fontsize=9,
                    color=CB, fontweight='bold', ha='center')
        ax.plot(0, 0, 'o', ms=13, mfc=CR, mec='k', mew=1.5, zorder=5)
        ax.text(0, -28, 'pozo real\n(bombea $+Q$)', ha='center', fontsize=8.6,
                va='top')
        col = CR if kind == 'barrera' else CG
        sgn = '+Q' if kind == 'barrera' else '-Q'
        ax.plot(2 * d, 0, 'o', ms=13, mfc=col, mec='k', mew=1.5, zorder=5,
                alpha=.85)
        ax.text(2 * d, -28, f'pozo imagen\n({"bombea" if kind=="barrera" else "inyecta"} ${sgn}$)',
                ha='center', fontsize=8.6, va='top', color=col)
        ax.annotate('', xy=(2 * d, 48), xytext=(0, 48),
                    arrowprops=dict(arrowstyle='<|-|>', color='#555', lw=1))
        ax.text(d, 56, '$2L$', ha='center', fontsize=10)
        ax.plot(100, 0, '*', ms=16, color='white', mec='k', mew=1.3, zorder=6)
        ax.text(100, 18, 'punto de cálculo\n$r_{real}=100$ m,  $r_{img}=200$ m',
                ha='center', fontsize=8.2)
        f = '+' if kind == 'barrera' else '-'
        ax.text(d / 2, -140,
                f'$s = s_{{real}} {f} s_{{imagen}}$\n'
                + ('$= 3.03 + 2.48 = 5.51$ m   (×1.82)' if kind == 'barrera'
                   else '$= 3.03 - 2.48 = 0.55$ m   (×0.18)'),
                ha='center', fontsize=10.5,
                bbox=dict(fc='#fff8f0' if kind == 'barrera' else '#f1f8f2',
                          ec=col, lw=1.1, pad=4))
        ax.set_xlim(-120, 280); ax.set_ylim(-195, 185)
        ax.set_title('Frontera impermeable: el abatimiento se DUPLICA cerca'
                     if kind == 'barrera' else
                     'Frontera de recarga: el río FRENA el abatimiento',
                     fontsize=9.6)
    fig.suptitle('Cálculos en el acuífero (2): fronteras mediante pozos imagen '
                 '(método de las imágenes)', fontsize=10.3, y=1.02)
    save(fig, 'fig_b8_imagenes')


# ================================================================ 9 permanente
def fig_thiem():
    fig, axs = plt.subplots(1, 2, figsize=(9.8, 4.3))
    for ax, kind in zip(axs, ['conf', 'libre']):
        ax.axis('off')
        if kind == 'conf':
            ax.add_patch(Rectangle((0, 25), 260, 8, fc=CLAY, ec='k', lw=1,
                                   hatch='xx'))
            ax.add_patch(Rectangle((0, 0), 260, 25, fc=AQ, ec='k', lw=1.2))
            rr = np.linspace(2, 255, 300)
            hh = 40 - (1500 / (2 * pi * 300)) * np.log(260 / rr)
            ax.plot(rr, hh, '-', color=CB, lw=2.3)
            ax.axhline(40, color='#888', ls=':', lw=1.3)
            ax.text(255, 40.5, 'nivel inicial', fontsize=8.2, color='#555',
                    ha='right')
            for r_, s_, lab in [(20, 2.80, '$r_1=20$ m\n$s_1=2.80$ m'),
                                (200, 1.00, '$r_2=200$ m\n$s_2=1.00$ m')]:
                ax.plot([r_, r_], [0, 40 - s_], '-', color='k', lw=1.2)
                ax.plot(r_, 40 - s_, 'o', ms=7, color=CR, zorder=5)
                ax.text(r_, 13, lab, ha='center', fontsize=8.4)
            ax.text(130, 45,
                    '$T=\\dfrac{Q\\,\\ln(r_2/r_1)}{2\\pi\\,(s_1-s_2)}=305$ m²/día',
                    ha='center', fontsize=11,
                    bbox=dict(fc='#f3f7fb', ec=CB, lw=1.0, pad=4))
            ax.set_ylim(-4, 54)
            ax.set_title('CONFINADO (Thiem): se trabaja con $s$', fontsize=9.7)
        else:
            rr = np.linspace(2, 255, 300)
            hh = np.sqrt(30 ** 2 - (1500 / (pi * 8.89)) * np.log(260 / rr))
            ax.add_patch(Rectangle((0, 0), 260, 30, fc=AQ, ec='none'))
            ax.fill_between(rr, hh, 31, color='white')
            ax.plot(rr, hh, '-', color=CB, lw=2.3)
            ax.plot([0, 260], [0, 0], '-', color='k', lw=1.4)
            ax.add_patch(Rectangle((0, -3.5), 260, 3.5, fc='#8a8a8a', ec='k',
                                   lw=1, hatch='///'))
            for r_, h_, lab in [(20, 27.0, '$r_1=20$ m\n$h_1=27.0$ m'),
                                (200, 29.2, '$r_2=200$ m\n$h_2=29.2$ m')]:
                ax.plot([r_, r_], [0, h_], '-', color='k', lw=1.2)
                ax.plot(r_, h_, 'o', ms=7, color=CR, zorder=5)
                ax.text(r_, 11, lab, ha='center', fontsize=8.4)
            ax.text(130, 35,
                    '$K=\\dfrac{Q\\,\\ln(r_2/r_1)}{\\pi\\,(h_2^{2}-h_1^{2})}'
                    '=8.9$ m/día', ha='center', fontsize=11,
                    bbox=dict(fc='#f1f8f2', ec=CG, lw=1.0, pad=4))
            ax.set_ylim(-5, 42)
            ax.set_title('LIBRE (Dupuit): se trabaja con $h^{2}$', fontsize=9.7)
        ax.set_xlim(-18, 272)
    fig.suptitle('Régimen permanente: cuando el abatimiento ya se estabilizó '
                 '(dos piezómetros, sin tiempo)', fontsize=10.3, y=1.02)
    save(fig, 'fig_b9_thiem')


# ================================================================ 10 diagrama
def fig_arbol():
    fig, ax = plt.subplots(figsize=(9.6, 6.4))
    ax.axis('off')

    def box(x, y, w, h, txt, fc, ec, fs=9.0, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.015',
                                    fc=fc, ec=ec, lw=1.3))
        ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center',
                fontsize=fs, fontweight='bold' if bold else 'normal')

    def arrow(x1, y1, x2, y2, lab=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', color='#444', lw=1.5))
        if lab:
            ax.text((x1 + x2) / 2 + .012, (y1 + y2) / 2, lab, fontsize=8.3,
                    ha='left', va='center', color='#b03030',
                    bbox=dict(fc='white', ec='none', alpha=.9, pad=1))

    box(.31, .885, .38, .085, '¿Qué datos te dan?', '#fff4d6', '#d9a400',
        10.5, True)
    box(.025, .70, .28, .10, '$s$ YA ESTABILIZADO\n(régimen permanente)',
        '#f1f8f2', CG)
    box(.36, .70, .28, .10, '$s$ frente al TIEMPO\nen un piezómetro',
        '#f3f7fb', CB)
    box(.695, .70, .28, .10, 'después de PARAR\nla bomba', '#fdf0f0', CR)
    arrow(.40, .885, .165, .805)
    arrow(.50, .885, .50, .805)
    arrow(.60, .885, .835, .805)

    box(.015, .50, .145, .11, 'CONFINADO\nThiem', '#f1f8f2', CG, 8.8, True)
    box(.175, .50, .145, .11, 'LIBRE\nDupuit', '#f1f8f2', CG, 8.8, True)
    arrow(.12, .70, .09, .615)
    arrow(.21, .70, .245, .615)

    box(.345, .50, .31, .11, '¿$u<0.01$ en los puntos\nde tiempo tardío?',
        '#f3f7fb', CB, 9.0)
    arrow(.50, .70, .50, .615)
    box(.345, .315, .145, .10, 'SÍ →\nCOOPER-JACOB', '#dff0d8', CG, 8.6, True)
    box(.51, .315, .145, .10, 'NO →\nTHEIS', '#e8e8f5', '#5c4b9e', 8.6, True)
    arrow(.42, .50, .42, .42)
    arrow(.58, .50, .58, .42)

    box(.695, .50, .28, .11, 'RECUPERACIÓN\nDE THEIS\n(da $T$, no da $S$)',
        '#fdf0f0', CR, 8.8, True)
    arrow(.835, .70, .835, .615)

    box(.30, .165, .40, .115, 'VARIOS PIEZÓMETROS a un mismo tiempo\n'
                              '→ DISTANCIA–ABATIMIENTO\n'
                              '(el denominador es $2\\pi$, no $4\\pi$)',
        '#fff4d6', '#d9a400', 8.8)
    box(.03, .005, .94, .115,
        'Con $T$ y $S$ en la mano:  predecir $s$ en cualquier $(r,t)$  ·  sumar '
        'pozos (superposición)  ·  $R_0=\\sqrt{2.25\\,Tt/S}$\n'
        '$K=T/b$  ·  capacidad específica $Q/s_w$  ·  fronteras con pozos imagen',
        '#eef3f8', CB, 9.0)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_title('Qué método usar: decídelo en los primeros 30 segundos del '
                 'parcial', fontsize=11, fontweight='bold')
    save(fig, 'fig_b0_arbol')


fig_arbol()
fig_esquema()
fig_cj()
fig_theis()
fig_dist()
fig_rec()
fig_cono()
fig_super()
fig_imagen()
fig_thiem()
print('figuras ok')

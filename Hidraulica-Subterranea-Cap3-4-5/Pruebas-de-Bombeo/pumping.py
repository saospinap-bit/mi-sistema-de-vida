"""Verificacion numerica completa del modulo de pruebas de bombeo."""
import numpy as np
from math import log, log10, pi, exp, sqrt

# ---------------------------------------------------------------- W(u)
def W(u):
    """Funcion de pozo de Theis = E1(u), por serie o continued fraction."""
    u = np.asarray(u, dtype=float)
    out = np.empty_like(u)
    small = u < 1.0
    # serie para u pequeno
    us = u[small]
    if us.size:
        s = -0.5772156649015329 - np.log(us)
        term = np.ones_like(us)
        for n in range(1, 40):
            term = term * (-us) / n
            s = s - term / n
        out[small] = s
    # fraccion continua para u grande
    ub = u[~small]
    if ub.size:
        b = ub + 1.0
        c = 1e300
        d = 1.0 / b
        h = d
        for i in range(1, 100):
            a = -i * i
            b = b + 2.0
            d = 1.0 / (a * d + b)
            c = b + a / c
            de = c * d
            h = h * de
            if np.all(np.abs(de - 1.0) < 1e-12):
                break
        out[~small] = h * np.exp(-ub)
    return out


print('=' * 72)
print('TABLA DE W(u)  (verificacion contra valores de referencia)')
print('=' * 72)
ref = {1e-1: 1.823, 1e-2: 4.038, 1e-3: 6.332, 1e-4: 8.633,
       1e-5: 10.94, 1e-6: 13.24, 1e-7: 15.54, 1e-8: 17.84,
       1e-9: 20.15, 1e-10: 22.45, 1.0: 0.2194, 5e-1: 0.5598}
for u in sorted(ref):
    print(f'  u={u:<10.0e}  W(u)={float(W(u)):8.4f}   ref={ref[u]}')

print()
print('Tabla para el documento:')
rows = []
for m in [1, 2, 5]:
    for e in range(-9, 1):
        u = m * 10.0 ** e
        if u <= 1.0:
            rows.append((u, float(W(u))))
rows.sort()
for u, w in rows:
    print(f'   {u:.0e}   {w:.4f}')

# ================================================================ CASO 1
print()
print('=' * 72)
print('CASO 1 — PRUEBA DE BOMBEO: datos sinteticos y analisis Cooper-Jacob')
print('=' * 72)
Q = 1500.0          # m3/dia
r = 50.0            # m
T_true, S_true = 300.0, 1.0e-3
b_aq = 25.0         # espesor del acuifero (m)

t_min = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60, 90, 120,
                  180, 240, 360, 480, 720, 1080, 1440], float)
t_d = t_min / 1440.0
u = r ** 2 * S_true / (4 * T_true * t_d)
s = Q / (4 * pi * T_true) * W(u)

print(f'Q = {Q} m3/dia   r = {r} m   (T real = {T_true}, S real = {S_true:.0e})')
print(f'{"t (min)":>9} {"t (d)":>10} {"u":>10} {"s Theis (m)":>12} '
      f'{"s C-J (m)":>10} {"error %":>8}')
s_cj_all = 2.303 * Q / (4 * pi * T_true) * np.log10(
    2.25 * T_true * t_d / (r ** 2 * S_true))
for i in range(len(t_min)):
    err = 100 * (s_cj_all[i] - s[i]) / s[i]
    print(f'{t_min[i]:9.0f} {t_d[i]:10.5f} {u[i]:10.4f} {s[i]:12.3f} '
          f'{s_cj_all[i]:10.3f} {err:8.2f}')

# --- ajuste de la recta en la zona valida (u < 0.01)
valid = u < 0.01
print(f'\nPuntos con u < 0.01: t >= {t_min[valid].min():.0f} min '
      f'({valid.sum()} puntos)')
A = np.polyfit(np.log10(t_d[valid]), s[valid], 1)
ds_cycle = A[0]
t0_d = 10 ** (-A[1] / A[0])
T_fit = 2.303 * Q / (4 * pi * ds_cycle)
S_fit = 2.25 * T_fit * t0_d / r ** 2
print(f'  pendiente (delta s por ciclo log) = {ds_cycle:.4f} m')
print(f'  t0 = {t0_d:.6f} d = {t0_d*1440:.2f} min')
print(f'  T = 2.303Q/(4*pi*ds) = {T_fit:.1f} m2/dia   (real {T_true})  '
      f'error {100*(T_fit-T_true)/T_true:+.2f} %')
print(f'  S = 2.25*T*t0/r^2    = {S_fit:.3e}        (real {S_true:.1e})  '
      f'error {100*(S_fit-S_true)/S_true:+.2f} %')
print(f'  K = T/b = {T_fit/b_aq:.2f} m/dia = {T_fit/b_aq/86400:.3e} m/s')
print(f'  Ss = S/b = {S_fit/b_aq:.3e} 1/m')

# valores "redondos" para el enunciado del documento
ds_doc = 0.92
t0_doc_min = 5.3
T_doc = 2.303 * Q / (4 * pi * ds_doc)
S_doc = 2.25 * T_doc * (t0_doc_min / 1440) / r ** 2
print(f'\nCon lectura grafica redondeada (ds = {ds_doc} m, t0 = {t0_doc_min} min):')
print(f'  T = {T_doc:.1f} m2/dia      S = {S_doc:.3e}')

# ================================================================ CASO 2
print()
print('=' * 72)
print('CASO 2 — DISTANCIA-ABATIMIENTO  (t fijo = 1 dia)')
print('=' * 72)
t_fix = 1.0
rr = np.array([10., 30., 50., 100., 200., 300.])
uu = rr ** 2 * S_true / (4 * T_true * t_fix)
ss = Q / (4 * pi * T_true) * W(uu)
print(f'{"r (m)":>8} {"u":>10} {"s (m)":>8}')
for i in range(len(rr)):
    print(f'{rr[i]:8.0f} {uu[i]:10.2e} {ss[i]:8.3f}')
vd = uu < 0.01
print(f'  ajuste solo con u<0.01 -> r <= {rr[vd].max():.0f} m ({vd.sum()} puntos)')
B = np.polyfit(np.log10(rr[vd]), ss[vd], 1)
ds_r = -B[0]
r0 = 10 ** (-B[1] / B[0])
T_r = 2.303 * Q / (2 * pi * ds_r)
S_r = 2.25 * T_r * t_fix / r0 ** 2
print(f'  delta s por ciclo log de r = {ds_r:.4f} m')
print(f'  r0 (s=0) = {r0:.1f} m')
print(f'  T = 2.303Q/(2*pi*ds_r) = {T_r:.1f} m2/dia  error '
      f'{100*(T_r-T_true)/T_true:+.2f} %')
print(f'  S = 2.25*T*t/r0^2      = {S_r:.3e}  error '
      f'{100*(S_r-S_true)/S_true:+.2f} %')
print(f'  comprobacion R0 = sqrt(2.25*T*t/S) = '
      f'{sqrt(2.25*T_true*t_fix/S_true):.1f} m')

# ================================================================ CASO 3
print()
print('=' * 72)
print('CASO 3 — RECUPERACION DE THEIS')
print('=' * 72)
tp = 1440.0 / 1440.0       # bombeo 1 dia
tpr = np.array([5, 10, 20, 30, 60, 120, 240, 480], float) / 1440.0  # t'
t_tot = tp + tpr
r_rec = 0.15               # se mide en el PROPIO pozo de bombeo
# abatimiento residual: s' = Q/(4 pi T) [W(u) - W(u')]
u1 = r_rec ** 2 * S_true / (4 * T_true * t_tot)
u2 = r_rec ** 2 * S_true / (4 * T_true * tpr)
print(f'medido en el pozo de bombeo (rw = {r_rec} m), bombeo previo tp = '
      f'{tp*1440:.0f} min')
print(f'  u\' maximo = {u2.max():.2e}  (muy << 0.01: Jacob siempre valido)')
sp = Q / (4 * pi * T_true) * (W(u1) - W(u2))
ratio = t_tot / tpr
print('  t_rec(min)      t/t_rec     s_res(m)')
for i in range(len(tpr)):
    print(f'{tpr[i]*1440:9.0f} {ratio[i]:9.2f} {sp[i]:8.3f}')
C = np.polyfit(np.log10(ratio), sp, 1)
ds_rec = C[0]
T_rec = 2.303 * Q / (4 * pi * ds_rec)
print(f'  delta s\' por ciclo = {ds_rec:.4f} m')
print(f'  T = {T_rec:.1f} m2/dia   error {100*(T_rec-T_true)/T_true:+.2f} %')
print('  (la recuperacion da T pero NO da S)')

# ================================================================ CASO 4
print()
print('=' * 72)
print('CASO 4 — REGIMEN PERMANENTE: THIEM')
print('=' * 72)
# confinado
r1, r2 = 20.0, 200.0
s1, s2 = 2.80, 1.00
T_th = Q * log(r2 / r1) / (2 * pi * (s1 - s2))
print(f'Confinado: Q={Q}, r1={r1} s1={s1}, r2={r2} s2={s2}')
print(f'  T = Q ln(r2/r1)/(2 pi (s1-s2)) = {T_th:.1f} m2/dia')
print(f'  K = T/b = {T_th/b_aq:.2f} m/dia')
# libre
H = 30.0
h1, h2 = 27.0, 29.2
K_un = Q * log(r2 / r1) / (pi * (h2 ** 2 - h1 ** 2))
print(f'Libre: H={H}, h1={h1} @ {r1} m, h2={h2} @ {r2} m')
print(f'  K = Q ln(r2/r1)/(pi (h2^2-h1^2)) = {K_un:.2f} m/dia')
print(f'  T aprox = K*H_media = {K_un*(h1+h2)/2:.1f} m2/dia')

# ================================================================ CASO 5
print()
print('=' * 72)
print('CASO 5 — CALCULOS EN EL ACUIFERO con T=300 m2/dia, S=1e-3')
print('=' * 72)
T, S = 300.0, 1.0e-3


def theis(Qp, rp, tp_, T=T, S=S):
    up = rp ** 2 * S / (4 * T * tp_)
    return Qp / (4 * pi * T) * float(W(up)), up


def cj(Qp, rp, tp_, T=T, S=S):
    return 2.303 * Qp / (4 * pi * T) * log10(2.25 * T * tp_ / (rp ** 2 * S))


print('(a) Abatimiento a 200 m despues de 30 dias, Q=1500 m3/dia')
sa, ua = theis(Q, 200.0, 30.0)
print(f'    u = {ua:.3e} -> W(u) = {float(W(ua)):.3f}   s = {sa:.3f} m')
print(f'    por Cooper-Jacob: s = {cj(Q,200.,30.):.3f} m  (u<0.01, valido)')

print('(b) Abatimiento en el pozo (rw=0.15 m) a 30 dias y capacidad especifica')
sw, uw = theis(Q, 0.15, 30.0)
print(f'    u = {uw:.3e}   s_w = {sw:.2f} m')
print(f'    capacidad especifica Q/s_w = {Q/sw:.1f} m3/dia por m de abatimiento')

print('(c) Interferencia: 3 pozos de 1500 m3/dia; punto P')
# pozos en (0,0), (300,0), (150,260); P en (150,87) aprox centroide
wells = [(0., 0.), (300., 0.), (150., 260.)]
P = (150., 86.7)
tot = 0.0
for i, (xw, yw) in enumerate(wells, 1):
    d = sqrt((P[0] - xw) ** 2 + (P[1] - yw) ** 2)
    si, ui_ = theis(Q, d, 30.0)
    tot += si
    print(f'    pozo {i}: r = {d:.1f} m -> s = {si:.3f} m')
print(f'    ABATIMIENTO TOTAL (superposicion) = {tot:.3f} m')
s_one, _ = theis(Q, 173.3, 30.0)
print(f'    un solo pozo a 173.3 m daria {s_one:.3f} m -> la interferencia '
      f'multiplica por {tot/s_one:.2f}')

print('(d) Radio de influencia a 30 dias')
R0 = sqrt(2.25 * T * 30.0 / S)
print(f'    R0 = sqrt(2.25 T t/S) = {R0:.0f} m = {R0/1000:.2f} km')
for tt in [1, 7, 30, 365]:
    print(f'      t={tt:4d} d -> R0 = {sqrt(2.25*T*tt/S):7.0f} m')

print('(e) K, q y velocidad real a 200 m (n_e=0.2)')
K = T / b_aq
# gradiente en r=200 a t=30 d:  ds/dr = -Q/(2 pi T r) * exp(-u) aprox = Q/(2 pi T r)
grad = Q / (2 * pi * T * 200.0)
qd = K * grad
print(f'    K = T/b = {K:.1f} m/dia   gradiente = Q/(2 pi T r) = {grad:.2e}')
print(f'    q = K i = {qd:.4f} m/dia    v = q/n_e = {qd/0.2:.4f} m/dia')
print(f'    verificacion por continuidad: q = Q/(2 pi r b) = '
      f'{Q/(2*pi*200.0*b_aq):.4f} m/dia')

print('(f) Volumen extraido del almacenamiento en 30 dias')
print(f'    V = Q t = {Q*30:.0f} m3')
print(f'    area equivalente con descenso medio 1 m: {Q*30/S:.3e} m2 '
      f'(= {Q*30/S/1e6:.1f} km2 con 1 m)')

print('(g) Tiempo para que s = 2.00 m a r = 100 m')
s_obj = 2.0
# invertir Cooper-Jacob
t_sol = (r ** 0 * 100.0 ** 2 * S / (2.25 * T)) * 10 ** (
    s_obj * 4 * pi * T / (2.303 * Q))
print(f'    t = (r^2 S/2.25T) * 10^(4 pi T s/2.303Q) = {t_sol:.2f} dias')
sc, uc = theis(Q, 100.0, t_sol)
print(f'    verificacion Theis a t={t_sol:.2f} d: s = {sc:.3f} m (u={uc:.2e})')

print('(h) Caudal maximo con 8 m de abatimiento disponible en el pozo, 180 dias')
s_av = 8.0
sw1, _ = theis(1.0, 0.15, 180.0)       # abatimiento por unidad de caudal
Qmax = s_av / sw1
print(f'    s por unidad de Q a 180 d = {sw1:.5f} m por (m3/dia)')
print(f'    Q_max = {Qmax:.0f} m3/dia = {Qmax/86.4:.1f} L/s')

print('(i) Frontera impermeable a 150 m: pozo imagen')
d_bound = 150.0
r_real, r_img = 100.0, sqrt(100.0 ** 2 + (2 * d_bound) ** 2)
s_r, _ = theis(Q, r_real, 30.0)
s_i, _ = theis(Q, r_img, 30.0)
print(f'    punto a 100 m del pozo; imagen a {r_img:.1f} m')
print(f'    s = {s_r:.3f} + {s_i:.3f} = {s_r+s_i:.3f} m  '
      f'(frontera IMPERMEABLE: se SUMA)')
print(f'    si fuera de carga constante (rio): s = {s_r:.3f} - {s_i:.3f} = '
      f'{s_r-s_i:.3f} m  (se RESTA)')

print()
print('=' * 72)
print('CONVERSIONES UTILES')
print('=' * 72)
print(f'  1 m3/dia = {1/86400:.5e} m3/s = {1000/86400:.4f} L/s')
print(f'  1 L/s = {86.4:.1f} m3/dia')
print(f'  1 m2/dia = {1/86400:.4e} m2/s')
print(f'  2.303/(4 pi) = {2.303/(4*pi):.5f}')
print(f'  2.303/(2 pi) = {2.303/(2*pi):.5f}')
print(f'  1/(4 pi) = {1/(4*pi):.5f}')

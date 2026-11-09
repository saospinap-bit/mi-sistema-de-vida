"""Verificacion de TODOS los ejercicios propuestos en la guia maestra."""
import numpy as np
from math import pi, log, log10, sqrt, exp
from pumping_lib import W

def hr(t):
    print('\n' + '=' * 70); print(t); print('=' * 70)

hr('PARTE II — PAPEL LOGARITMICO')
print('II.1  La recta pasa por (20 min, 0.60 m) y (200 min, 1.42 m)')
ds = 1.42 - 0.60
print(f'   un ciclo exacto (20->200) => ds = {ds:.2f} m por ciclo')
t0 = 20 * 10 ** (-0.60 / ds)
print(f'   t0: 0 = 0.60 + {ds:.2f} log(t/20) -> t0 = {t0:.2f} min = {t0/1440:.5f} d')
Q, r = 1200.0, 40.0
T = 2.303 * Q / (4 * pi * ds); S = 2.25 * T * (t0 / 1440) / r ** 2
print(f'   con Q=1200 m3/d, r=40 m:  T = {T:.1f} m2/d   S = {S:.3e}')

print('\nII.2  Posicion dentro del ciclo logaritmico')
for v in [2, 3.5, 5, 7]:
    print(f'   el {v} esta al {100*log10(v):.1f} % del ciclo')
print(f'   un punto al 65 % de un ciclo que empieza en 100: '
      f'{100*10**0.65:.1f}')
print(f'   un punto al 30 % de un ciclo que empieza en 10:  '
      f'{10*10**0.30:.2f}')

hr('PARTE III — DARCY')
print('III.1  K=2.5e-5 m/s, i=0.004, A=120 m2, ne=0.18, L=500 m')
K, i, A, ne = 2.5e-5, 0.004, 120.0, 0.18
q = K * i; Qv = q * A; v = q / ne
print(f'   q = {q:.3e} m/s = {q*86400:.5f} m/dia')
print(f'   Q = {Qv:.3e} m3/s = {Qv*86400:.3f} m3/dia')
print(f'   v = {v:.3e} m/s = {v*86400:.4f} m/dia')
print(f'   t = L/v = {500/(v*86400):.0f} dias = {500/(v*86400)/365.25:.1f} anos')

print('\nIII.2  Piezometro: terreno 450 m, 180 m de profundidad, agua a 12 m')
z = 450 - 180; h = 450 - 12; hp = h - z
print(f'   z = {z} m   h = {h} m   hp = {hp} m   (columna = 180-12 = {180-12}) OK')

hr('PARTE IV — HETEROGENEIDAD')
print('IV.1  Cuatro capas')
bs = np.array([5., 12., 8., 15.]); Ks = np.array([3e-4, 5e-7, 2e-4, 8e-6])
Kh = (Ks * bs).sum() / bs.sum(); Kv = bs.sum() / (bs / Ks).sum()
for bb, kk in zip(bs, Ks):
    print(f'   b={bb:5.0f} m   K={kk:.1e} m/s')
print(f'   sum b = {bs.sum():.0f} m')
print(f'   Kh = {Kh:.3e} m/s     Kv = {Kv:.3e} m/s     Kh/Kv = {Kh/Kv:.1f}')
print(f'   (Kh la domina la capa de {Ks.max():.0e};  Kv la de {Ks.min():.0e})')

print('\nIV.2  Tensor: i_x=0.05 -> q_y=2e-4 cm/s ;  i_y=0.02 -> q_x=?')
Kyx = 2e-4 / 0.05
print(f'   Kyx = {Kyx:.1e} cm/s = Kxy  ->  q_x = {Kyx*0.02:.1e} cm/s')

hr('PARTE V — ECUACION DE FLUJO Y ALMACENAMIENTO')
print('V.1  S=5e-4, n=0.25, bw=4.8e-10 m2/N, b=40 m')
S_, n_, bw, b_ = 5e-4, 0.25, 4.8e-10, 40.0
rho, g = 1000., 9.81
V = S_ * 2e6 * 1.5
print(f'   (a) V = S*A*dh = {S_}*2e6*1.5 = {V:.0f} m3')
S_inc = rho * g * b_ * n_ * bw
print(f'   (b) S (matriz incompresible) = rho g b n bw = {S_inc:.3e}'
      f'  ({100*S_inc/S_:.1f} % del real)')
bp = S_ / (rho * g * b_) - n_ * bw
print(f'   (c) beta_p = S/(rho g b) - n bw = {S_/(rho*g*b_):.4e} - '
      f'{n_*bw:.4e} = {bp:.3e} m2/N')
print(f'       verificacion: S = {rho*g*b_*(bp+n_*bw):.3e} OK')

print('\nV.2  T=250 m2/dia, S=4e-4: difusividad y longitud de difusion')
Tt, Ss = 250., 4e-4
nu = Tt / Ss
print(f'   nu = T/S = {nu:.3e} m2/dia')
print(f'   sqrt(nu t) = 1000 m  ->  t = 1e6/nu = {1e6/nu:.3f} dias = '
      f'{1e6/nu*24:.1f} horas')
for d in [100, 500, 2000]:
    print(f'   para {d:5d} m:  t = {d**2/nu:.4f} dias')

hr('PARTE VI — REDES DE FLUJO')
print('VI.1  nf=4, nd=12, K=2e-4 m/s, H=15 m, ancho 80 m')
Kd, H, nf, nd, Wd = 2e-4, 15., 4, 12, 80.
qm = Kd * H * nf / nd
print(f'   Q por metro = K H nf/nd = {qm:.3e} m3/s/m')
print(f'   Q total = {qm*Wd:.4f} m3/s = {qm*Wd*86400:.0f} m3/dia')
print(f'   gradiente medio si el recorrido es 60 m: {H/60:.3f}')

print('\nVI.2  Kh=4e-4, Kv=1e-5 m/s')
Kh2, Kv2 = 4e-4, 1e-5
print(f'   Keq = sqrt(Kh Kv) = {sqrt(Kh2*Kv2):.3e} m/s')
print(f'   factor de escala x = sqrt(Kv/Kh) = {sqrt(Kv2/Kh2):.4f}')
print(f'   relacion de lados de las celdas = sqrt(Kh/Kv) = {sqrt(Kh2/Kv2):.2f} : 1')

hr('PARTE VII — ESFUERZO EFECTIVO')
print('VII.1  Arcilla 40 ft, gsat=120 lb/ft3, artesiano +15 ft sobre el terreno')
gs, gw, D = 120., 62.4, 40.
hp2 = D + 15
sT = gs * D; u = gw * hp2
print(f'   hp = {hp2:.0f} ft')
print(f'   sigma_T = {sT:.0f}   u = {u:.1f}   sigma\' = {sT-u:.1f} lb/ft2   '
      f'FS = {sT/u:.3f}')
dcw = (gs * D - gw * hp2) / (gs - gw); dcd = D - gw * hp2 / gs
print(f'   d_crit con agua = {dcw:.2f} ft      d_crit en seco = {dcd:.2f} ft')

print('\nVII.2  Version metrica: 12 m, gsat=19.5 kN/m3, artesiano +5 m')
gs2, gw2, D2 = 19.5, 9.81, 12.
hp3 = D2 + 5
sT2 = gs2 * D2; u2 = gw2 * hp3
print(f'   sigma_T = {sT2:.1f} kPa   u = {u2:.2f} kPa   '
      f'sigma\' = {sT2-u2:.2f} kPa   FS = {sT2/u2:.3f}')
print(f'   d_crit con agua = {(gs2*D2-gw2*hp3)/(gs2-gw2):.2f} m   '
      f'en seco = {D2-gw2*hp3/gs2:.2f} m')

hr('PARTE VIII — PRUEBA DE BOMBEO (ejercicios propuestos)')
print('VIII.1  Q=2500 m3/dia, r=80 m, b=40 m   (T real 800, S real 3e-4)')
Qe, re, Te, Se, be = 2500., 80., 800., 3e-4, 40.
tm = np.array([1, 2, 3, 5, 8, 12, 20, 30, 45, 60, 90, 120, 180, 300,
               480, 720, 1080, 1440], float)
td = tm / 1440
ue = re ** 2 * Se / (4 * Te * td)
se = Qe / (4 * pi * Te) * W(ue)
print(f'   {"t(min)":>7} {"u":>10} {"s(m)":>8}')
for k in range(len(tm)):
    print(f'   {tm[k]:7.0f} {ue[k]:10.4f} {se[k]:8.3f}')
val = ue < 0.01
Af = np.polyfit(np.log10(td[val]), se[val], 1)
dsf = Af[0]; t0f = 10 ** (-Af[1] / Af[0])
Tf = 2.303 * Qe / (4 * pi * dsf); Sf = 2.25 * Tf * t0f / re ** 2
print(f'   validos (u<0.01): t >= {tm[val].min():.0f} min')
print(f'   ds = {dsf:.4f} m/ciclo   t0 = {t0f*1440:.3f} min = {t0f:.6f} d')
print(f'   T = {Tf:.1f} m2/dia  (real {Te})   S = {Sf:.3e}  (real {Se:.0e})')
print(f'   K = T/b = {Tf/be:.2f} m/dia = {Tf/be/86400:.2e} m/s')

print('\nVIII.2  Distancia-abatimiento, t=2 dias, Q=1800 (T real 450, S real 8e-4)')
Qd2, Td2, Sd2, tf2 = 1800., 450., 8e-4, 2.0
rl = np.array([25., 75., 150., 250.])
ul = rl ** 2 * Sd2 / (4 * Td2 * tf2)
sl = Qd2 / (4 * pi * Td2) * W(ul)
for k in range(len(rl)):
    print(f'   r={rl[k]:6.0f} m   u={ul[k]:.2e}   s={sl[k]:.3f} m')
vv = ul < 0.01
Bf = np.polyfit(np.log10(rl[vv]), sl[vv], 1)
dsr = -Bf[0]; r0 = 10 ** (-Bf[1] / Bf[0])
Tr = 2.303 * Qd2 / (2 * pi * dsr); Sr = 2.25 * Tr * tf2 / r0 ** 2
print(f'   ds_r = {dsr:.4f} m/ciclo   r0 = {r0:.1f} m')
print(f'   T = {Tr:.1f} m2/dia (real {Td2})   S = {Sr:.3e} (real {Sd2:.0e})')

print('\nVIII.3  Recuperacion en el pozo: Q=2500, tp=12 h, rw=0.2 m (T real 800)')
tp3 = 0.5
tpr = np.array([5, 10, 20, 40, 80, 160, 320], float) / 1440
u1 = 0.2 ** 2 * 3e-4 / (4 * 800. * (tp3 + tpr))
u2 = 0.2 ** 2 * 3e-4 / (4 * 800. * tpr)
sp = 2500. / (4 * pi * 800.) * (W(u1) - W(u2))
rat = (tp3 + tpr) / tpr
for k in range(len(tpr)):
    print(f"   t'={tpr[k]*1440:6.0f} min   t/t'={rat[k]:8.2f}   s'={sp[k]:.3f} m")
Cf = np.polyfit(np.log10(rat), sp, 1)
print(f"   ds' = {Cf[0]:.4f} m/ciclo   T = {2.303*2500/(4*pi*Cf[0]):.1f} m2/dia")

print('\nVIII.4  Thiem: Q=2200 m3/dia, r1=15 m s1=3.40 m, r2=150 m s2=1.15 m, b=30')
Qth = 2200.; Tth = Qth * log(150 / 15) / (2 * pi * (3.40 - 1.15))
print(f'   T = {Tth:.1f} m2/dia    K = {Tth/30:.2f} m/dia')

hr('PARTE IX — CALCULOS EN EL ACUIFERO (propuestos)')
T9, S9 = 800., 3e-4
def th(Qp, rp, tp_, T=T9, S=S9):
    up = rp ** 2 * S / (4 * T * tp_); return Qp / (4 * pi * T) * float(W(up)), up
print('IX.1  T=800 m2/dia, S=3e-4, Q=2500 m3/dia')
s1, uu1 = th(2500., 150., 60.)
print(f'   (a) s a r=150 m, t=60 d:  u={uu1:.3e}  W={float(W(uu1)):.3f}  s={s1:.3f} m')
sw, uw = th(2500., 0.2, 60.)
print(f'   (b) s en el pozo (rw=0.2 m): u={uw:.2e}  s={sw:.2f} m')
print(f'       capacidad especifica = {2500/sw:.1f} m3/dia por m')
print(f'   (c) R0 a 60 d = {sqrt(2.25*T9*60/S9):.0f} m')

print('\nIX.2  Dos pozos de 2000 m3/dia separados 400 m, punto medio, t=90 d')
sA, _ = th(2000., 200., 90.)
print(f'   cada pozo: r=200 m -> s={sA:.3f} m   TOTAL = {2*sA:.3f} m')
print(f'   R0 a 90 d = {sqrt(2.25*T9*90/S9):.0f} m')
print(f'   un pozo solo daria {sA:.3f} m -> la interferencia duplica')

hr('PARTE X — COSTA')
print('X.1  Upconing: d=25 m, K=5e-4 m/s, G=0.025')
Qm = 0.6 * pi * 5e-4 * 25 ** 2 * 0.025
print(f'   Qmax = 0.6 pi K d^2 G = {Qm:.5f} m3/s = {Qm*1000:.2f} L/s = '
      f'{Qm*86400:.0f} m3/dia')
print('X.2  Glover: q\'=3e-4 ft3/s/ft, B=120 ft, K=4e-3 ft/s')
KG = 4e-3 * 0.025
xt = KG * 120 ** 2 / (2 * 3e-4) - 3e-4 / (2 * KG)
print(f'   KG = {KG:.1e}   q\'/KG = {3e-4/KG:.2f} ft')
print(f'   x_toe = {xt:.1f} ft')
xt2 = KG * 120 ** 2 / (2 * 1.5e-4) - 1.5e-4 / (2 * KG)
print(f'   con la mitad del caudal: x_toe = {xt2:.1f} ft  '
      f'(factor {xt2/xt:.2f})')

"""Verificacion de todos los ejercicios de los apuntes de clase."""
import numpy as np
from math import pi, sqrt, log, log10

def hr(t):
    print('\n'+'='*72); print(t); print('='*72)

A = 365.25            # dias por ano
hr('1. ALMACENAMIENTO:  S = Sy + Ss*b   (acuifero Valle del Cauca, b = 500 m)')
b = 500.
for Ss in (1e-3, 1e-5, 1e-6):
    for Sy in (0.27,):
        print(f'   Ss={Ss:.0e} 1/m -> Ss*b = {Ss*b:.4f}   Sy = {Sy}   '
              f'S = {Sy+Ss*b:.4f}   (Sy aporta {100*Sy/(Sy+Ss*b):.1f} %)')
print('   Conclusion: en acuifero libre el drenaje (Sy) domina sobre la')
print('   descompresion (Ss*b) por 1 a 2 ordenes de magnitud.')

hr('2. DUPUIT-FORCHHEIMER con recarga  (ejemplo de los apuntes)')
K, Sy, bq, h1, h2, L = 10.0, 0.27, 30.0, 15.0, 18.0, 200.0
print(f'   K={K} m/d  Sy={Sy}  b={bq} m  h1={h1} m  h2={h2} m  L={L} m')
dh2 = h1**2 - h2**2
print(f'   h1^2 - h2^2 = {h1**2:.0f} - {h2**2:.0f} = {dh2:.0f} m^2  (negativo: h2>h1)')
base = K*dh2/(2*L)
print(f'   termino de carga  K(h1^2-h2^2)/(2L) = {base:.4f} m^2/d')
for nombre, Wmma in (('CASO A:  W = -60 mm/ano', -60.), ('CASO B:  W = +20 mm/ano', 20.)):
    W = Wmma/1000/A
    print(f'\n   {nombre}   ->  W = {W:.6e} m/d')
    q0 = base - W*(L/2 - 0)
    qL = base - W*(L/2 - L)
    print(f'     q\'(x=0)   = {base:.4f} - ({W:.3e})({L/2:.0f})  = {q0:.4f} m^2/d')
    print(f'     q\'(x=L)   = {base:.4f} - ({W:.3e})({-L/2:.0f}) = {qL:.4f} m^2/d')
    print(f'     balance:  q\'(L) - q\'(0) = {qL-q0:.6f}   W*L = {W*L:.6f}  OK')
    d = L/2 - (K/W)*dh2/(2*L)
    print(f'     d = L/2 - (K/W)(h1^2-h2^2)/(2L) = {d:.1f} m')
    if 0 <= d <= L:
        hmax = sqrt(h1**2 - dh2*d/L + (W/K)*(L-d)*d)
        print(f'     d esta DENTRO [0,L] -> hmax = {hmax:.3f} m')
    else:
        print(f'     d esta FUERA de [0,{L:.0f}] -> NO hay divisoria ni hmax interno')
    print(f'     |termino carga| = {abs(base):.4f}  vs  |W L/2| = {abs(W*L/2):.4f}'
          f'  -> domina {"la CARGA" if abs(base)>abs(W*L/2) else "la RECARGA"}')
print('\n   Perfil del caso B (h en m):')
W = 20/1000/A
for x in (0, 50, 100, 150, 200):
    h = sqrt(h1**2 - dh2*x/L + (W/K)*(L-x)*x)
    print(f'     x={x:4.0f} m -> h = {h:.3f} m')

hr('3. VARIANTE donde SI existe divisoria (para practicar hmax)')
Kv, Wv, Lv, h1v, h2v = 1.0, 200/1000/A, 1000.0, 20.0, 18.0
dh2v = h1v**2 - h2v**2
basev = Kv*dh2v/(2*Lv)
print(f'   K={Kv} m/d  W=200 mm/ano={Wv:.4e} m/d  L={Lv:.0f} m  h1={h1v} h2={h2v}')
print(f'   |carga| = {abs(basev):.4f}  vs  |W L/2| = {Wv*Lv/2:.4f} -> domina la RECARGA')
dv = Lv/2 - (Kv/Wv)*dh2v/(2*Lv)
hmaxv = sqrt(h1v**2 - dh2v*dv/Lv + (Wv/Kv)*(Lv-dv)*dv)
print(f'   d = {dv:.1f} m  (dentro de [0,{Lv:.0f}])')
print(f'   hmax = {hmaxv:.3f} m   (sube {hmaxv-max(h1v,h2v):.2f} m sobre el borde mas alto)')
q0v = basev - Wv*(Lv/2); qLv = basev + Wv*(Lv/2)
print(f'   q\'(0) = {q0v:.4f} m^2/d (sale por la izquierda)')
print(f'   q\'(L) = {qLv:.4f} m^2/d (sale por la derecha)')
print(f'   suma de salidas = {abs(q0v)+abs(qLv):.4f}   recarga total W*L = {Wv*Lv:.4f}  OK')

hr('4. EJERCICIO COSTERO  (ejercicios 4, 5 y 6 de los apuntes)')
W6 = 500/1000/A/86400       # 500 mm/ano -> m/s
L0, Kc, ne = 1000.0, 1e-4, 0.35
rf, rs = 1.000, 1.025
dr = rs - rf
S0 = 30.0
tanth, dS, dLce = 0.02, 0.6, 3.0
print(f'   W = 500 mm/ano = {500/1000/A:.6f} m/d = {W6:.4e} m/s')
print(f'   K/W = {Kc/W6:.1f} (adimensional)')
C = (rs*dr*Kc)/(rf**2*W6)
print(f'   C = (rho_s * d_rho * K)/(rho_f^2 * W) = '
      f'({rs})({dr})({Kc:.0e})/({rf**2})({W6:.3e}) = {C:.2f}')
print(f'   Ghyben-Herzberg: 1/G = rho_f/(rho_s-rho_f) = {rf/dr:.0f}  -> z = 40 h')
dL = -dS/tanth - dLce
Lf, Sf = L0 + dL, S0 + dS
print(f'\n   Retroceso de la costa: dL = -dS/tan(theta) - dL_CE = '
      f'-({dS}/{tanth}) - {dLce} = {dL:.0f} m')
print(f'   Nuevo largo L_f = {Lf:.0f} m     nuevo S_f = {Sf:.1f} m')
xT0 = sqrt(L0**2 - C*S0**2); xTf = sqrt(Lf**2 - C*Sf**2)
print(f'\n   PREGUNTA 1: punta de la cuna  x_T = sqrt(L^2 - C s^2)')
print(f'     antes:   x_T0 = sqrt({L0:.0f}^2 - {C:.1f}x{S0:.0f}^2) = '
      f'sqrt({L0**2 - C*S0**2:.0f}) = {xT0:.1f} m')
print(f'     despues: x_Tf = sqrt({Lf:.0f}^2 - {C:.1f}x{Sf:.1f}^2) = '
      f'sqrt({Lf**2 - C*Sf**2:.0f}) = {xTf:.1f} m')
print(f'     delta x_T = {xTf-xT0:.1f} m')
print(f'     LONGITUD INVADIDA (L - x_T):  antes {L0-xT0:.1f} m   '
      f'despues {Lf-xTf:.1f} m   -> avanza {(Lf-xTf)-(L0-xT0):.1f} m')
def H(x, Lx, s):
    return sqrt((W6/Kc)*(Lx**2 - x**2) + (rs/rf)*s**2)
print(f'\n   PREGUNTA 2: nivel freatico  H(x) = sqrt((W/K)(L^2-x^2) + (rho_s/rho_f)s^2)')
print(f'     H es la carga medida DESDE LA BASE del acuifero')
for x in (10., 100., 500.):
    Ha, Hb = H(x, L0, S0), H(x, Lf, Sf)
    print(f'     x={x:5.0f} m: antes {Ha:.3f} m  despues {Hb:.3f} m  '
          f'-> sube {Hb-Ha:+.3f} m')
print(f'\n   Verificacion Ghyben-Herzberg en la punta de la cuna:')
Ht = H(xT0, L0, S0)
print(f'     H(x_T0) = {Ht:.3f} m ; nivel sobre el mar = {Ht-S0:.3f} m')
print(f'     teorico = s*d_rho/rho_f = {S0*dr/rf:.3f} m   COINCIDE')
print(f'   En la costa (x=L): H = {H(L0,L0,S0):.3f} m -> nivel sobre el mar = '
      f'{H(L0,L0,S0)-S0:.3f} m (cara de descarga)')

hr('5. THIEM con dos piezometros  (pagina 8 de los apuntes)')
r1, r2, s1, s2 = 0.8, 30.0, 2.236, 1.088
f = 2.303/(2*pi*(s1-s2))*log10(r2/r1)
print(f'   r1={r1} m  r2={r2} m  s1={s1} m  s2={s2} m')
print(f'   T = [2.303/(2pi({s1}-{s2}))] x log10({r2}/{r1}) = {f:.5f} Q')
print(f'   log10(r2/r1) = {log10(r2/r1):.4f}   2.303/(2pi x {s1-s2:.3f}) = '
      f'{2.303/(2*pi*(s1-s2)):.5f}')
for Q in (788.,):
    print(f'   con Q = {Q:.0f} m3/d  ->  T = {f*Q:.1f} m2/d')
print(f'   equivalente: T = Q ln(r2/r1)/(2pi(s1-s2)) = '
      f'{788*log(r2/r1)/(2*pi*(s1-s2)):.1f} m2/d  (identico)')

hr('6. THEIS: T y S desde un punto de coincidencia  (pagina 8)')
Qg = 500*1440/7.4805        # 500 gal/min -> ft3/dia
print(f'   Q = 500 gal/min = {Qg:.0f} ft3/dia')
Wu, u, sm, r2t = 1.0, 0.1, 0.56, 2.8e7
Tt = Qg*Wu/(4*pi*sm)
St = 4*Tt*u/r2t
print(f'   T = Q W(u)/(4 pi s) = {Qg:.0f}(1)/(4pi x {sm}) = {Tt:.0f} ft2/dia')
print(f'   S = 4 T u/(r^2/t) = 4({Tt:.0f})({u})/{r2t:.1e} = {St:.3e}')
print(f'   (los apuntes traen 13667 y 0.00019: coincide salvo redondeo)')
t_ = 240/1440
print(f'   radio de influencia a 240 min = {t_:.4f} d:')
print(f'     1.5 sqrt(Tt/S) = {1.5*sqrt(Tt*t_/St):.0f} ft')
print(f'     2.0 sqrt(Tt/S) = {2.0*sqrt(Tt*t_/St):.0f} ft')

hr('7. SUPERPOSICION DE DOS POZOS  (pagina 9)')
T9, S9, d9, r9, t9 = 100., 1e-4, 200., 50., 12/24
Q1, Q2 = 20*86.4, 50*86.4
print(f'   T={T9} m2/d  S={S9:.0e}  r={r9} m  t=12 h={t9} d')
print(f'   Q1 = 20 L/s = {Q1:.0f} m3/d     Q2 = 50 L/s = {Q2:.0f} m3/d')
arg = 2.25*T9*t9/(r9**2*S9)
Lam = log(arg)
print(f'   ln(2.25 T t/(r^2 S)) = ln(2.25x{T9:.0f}x{t9}/({r9**2:.0f}x{S9:.0e}))'
      f' = ln({arg:.0f}) = {Lam:.4f}')
print(f'   4 pi T = {4*pi*T9:.1f} m2/d')
sa, sb = Q1/(4*pi*T9)*Lam, Q2/(4*pi*T9)*Lam
print(f'   s1 = ({Q1:.0f}/{4*pi*T9:.1f}) x {Lam:.3f} = {sa:.2f} m')
print(f'   s2 = ({Q2:.0f}/{4*pi*T9:.1f}) x {Lam:.3f} = {sb:.2f} m')
print(f'   SUPERPOSICION: s = {sa+sb:.2f} m')
print(f'   R_i = 1.5 sqrt(Tt/S) = {1.5*sqrt(T9*t9/S9):.0f} m')
print('\n   Extension: frontera a 200 m  ->  pozo imagen a 400 m del punto')
def sTh(Q, r):
    return Q/(4*pi*T9)*log(2.25*T9*t9/(r**2*S9))
si1, si2 = sTh(Q1, 400.), sTh(Q2, 400.)
print(f'     imagen de Q1 a 400 m: {si1:.2f} m    imagen de Q2: {si2:.2f} m')
print(f'     frontera IMPERMEABLE: s = {sa+sb:.2f} + {si1+si2:.2f} = '
      f'{sa+sb+si1+si2:.2f} m')
print(f'     frontera de CARGA CONSTANTE: s = {sa+sb:.2f} - {si1+si2:.2f} = '
      f'{sa+sb-si1-si2:.2f} m')

hr('8. CORRECCIONES BAROMETRICA Y POR MAREA (ejemplo numerico)')
gw = 9.81
dPa = 1.0           # kPa de aumento de presion atmosferica
BE = 0.45
dh = -BE*dPa/gw
print(f'   Un aumento de {dPa} kPa en la presion atmosferica con BE={BE}:')
print(f'     equivalente en columna de agua = {dPa}/{gw} = {dPa/gw:.4f} m')
print(f'     el nivel en el pozo BAJA {abs(dh)*100:.2f} cm')
print(f'   Correccion: h_corr = h_obs + BE x (P_atm - P_ref)/gamma_w')
print(f'   Eficiencia de marea TE = 1 - BE = {1-BE:.2f}')
dmar = 1.2
print(f'   Con una marea de {dmar} m: el pozo oscila '
      f'{(1-BE)*dmar:.2f} m  (TE x amplitud)')

"""Cálculos en el acuífero, superposición, Dupuit con recarga, costa y canal."""
from xl_lib import *
from xl_part1 import SH
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import ColorScaleRule

# =========================================================== CÁLCULOS EN EL ACUÍFERO
h = Hoja('Calc_acuifero', 'Cálculos en el acuífero con T y S conocidos',
         'Abatimiento en cualquier punto, capacidad específica, radio de influencia, caudal máximo y velocidades.',
         cols={'G': 11, 'H': 10, 'I': 3, 'J': 11, 'K': 11, 'L': 11, 'M': 11, 'N': 11})
SH['Calc_acuifero'] = h
ws = h.ws
h.sec('1. Datos del acuífero')
h.inp('T', 'Transmisividad T', 300, 'm²/día', note='Sale de una prueba de bombeo (hojas Cooper_Jacob, Theis…).')
h.inp('S', 'Almacenamiento S', 1e-3, '—', fmt=SCI)
h.inp('Q', 'Caudal de bombeo Q', 1500, 'm³/día')
h.inp('b', 'Espesor b', 25, 'm')
h.inp('ne', 'Porosidad efectiva nₑ', 0.2, '—')
h.sec('2. Función de pozo W(u)')
h.inp('uu', 'u', 0.001, '', fmt=GEN)
h.out(None, 'W(u)', W(h.v['uu']), '', fmt=F4, main=True, note='Tabla de referencia a la derecha.')
h.sec('3. Abatimiento en un punto (r, t)')
h.inp('r', 'Distancia al pozo r', 200, 'm')
h.inp('t', 'Tiempo de bombeo t', 30, 'días')
h.out('u', 'u = r²S / (4Tt)', '{r}^2*{S}/(4*{T}*{t})', '', fmt=SCI)
h.out('Wu', 'W(u)', W('{u}'), '', fmt=F4)
h.out('sT', 's (Theis) = Q·W(u) / (4πT)', '{Q}/(4*PI()*{T})*{Wu}', 'm', fmt=F3, main=True)
h.out(None, 's (Cooper-Jacob) = 2.303Q/(4πT)·log(2.25Tt/(r²S))', 'IF({u}<0.05,2.303*{Q}/(4*PI()*{T})*LOG10(2.25*{T}*{t}/({r}^2*{S})),"no aplica (u ≥ 0.05)")', 'm', fmt=F3)
h.chk('¿Sirve Cooper-Jacob aquí?', 'IF({u}<0.01,"✔ sí: u < 0.01",IF({u}<0.05,"⚠ aproximado: u < 0.05","✘ no: usa Theis (u ≥ 0.05)"))')
h.sec('4. Abatimiento en el propio pozo y capacidad específica')
h.inp('rw', 'Radio del pozo r_w', 0.15, 'm')
h.inp('tw', 'Tiempo', 30, 'días')
h.out('uw', 'u en el pozo', '{rw}^2*{S}/(4*{T}*{tw})', '', fmt=SCI)
h.out('sw', 's_w = Q·W(u_w) / (4πT)', '{Q}/(4*PI()*{T})*(' + W('{uw}') + ')', 'm', fmt=F2, main=True)
h.out(None, 'Capacidad específica Q/s_w', '{Q}/{sw}', 'm³/día por m', fmt=F1, main=True,
      note='No es constante: baja con el tiempo porque s_w crece. Di siempre a qué t corresponde.')
h.out(None, 'Capacidad específica en L/s por m', '{Q}/{sw}/86.4', 'L/s por m', fmt=F2)
h.sec('5. Radio de influencia')
h.inp('tR', 'Tiempo', 30, 'días')
h.out(None, 'R₀ = 1.5·√(T·t/S)', '1.5*SQRT({T}*{tR}/{S})', 'm', fmt=F0, main=True,
      note='Es donde la recta de Cooper-Jacob da s = 0. Crece con √t.')
h.out(None, 'R₀ con el criterio 2·√(T·t/S)', '2*SQRT({T}*{tR}/{S})', 'm', fmt=F0,
      note='Otro criterio que aparece en los apuntes. Di cuál usas.')
h.sec('6. ¿Cuándo llega el abatimiento a un valor dado?')
h.inp('so', 'Abatimiento buscado', 2.0, 'm')
h.inp('ro', 'A la distancia', 100, 'm')
h.out('to', 't = (r²S / 2.25T) · 10^(4πT·s / 2.303Q)', '{ro}^2*{S}/(2.25*{T})*10^(4*PI()*{T}*{so}/(2.303*{Q}))', 'días', fmt=F3, main=True)
h.out('uo', 'u en ese tiempo', '{ro}^2*{S}/(4*{T}*{to})', '', fmt=SCI)
h.out(None, 'Comprobación con Theis: s en ese t', '{Q}/(4*PI()*{T})*(' + W('{uo}') + ')', 'm', fmt=F3)
h.sec('7. Caudal máximo con abatimiento disponible en el pozo')
h.inp('sd', 'Abatimiento disponible', 8, 'm')
h.inp('rq', 'Radio del pozo', 0.15, 'm')
h.inp('tq', 'Tiempo de bombeo', 180, 'días')
h.out('uq', 'u en el pozo', '{rq}^2*{S}/(4*{T}*{tq})', '', fmt=SCI)
h.out('su', 'Abatimiento por cada m³/día = W(u)/(4πT)', '(' + W('{uq}') + ')/(4*PI()*{T})', 'm por m³/día', fmt=SCI)
h.out('Qmx', 'Q máximo = s disponible / (s por unidad de Q)', '{sd}/{su}', 'm³/día', fmt=F0, main=True,
      note='Funciona porque s es proporcional a Q.')
h.out(None, 'Q máximo en L/s', '{Qmx}/86.4', 'L/s', fmt=F1)
h.sec('8. Velocidad del agua hacia el pozo')
h.inp('rv', 'Distancia', 200, 'm')
h.inp('tv', 'Tiempo', 30, 'días')
h.out('Kv', 'K = T/b', '{T}/{b}', 'm/día', fmt=F2)
h.out('uv', 'u', '{rv}^2*{S}/(4*{T}*{tv})', '', fmt=SCI)
h.out('iv', 'Gradiente i = Q·e^(−u) / (2πT·r)', '{Q}*EXP(-{uv})/(2*PI()*{T}*{rv})', '—', fmt=SCI)
h.out('qv', 'q = K·i', '{Kv}*{iv}', 'm/día', fmt=F4)
h.out(None, 'v = q/nₑ', '{qv}/{ne}', 'm/día', fmt=F4, main=True)
h.out(None, 'Comprobación por continuidad: q = Q/(2πrb)', '{Q}/(2*PI()*{rv}*{b})', 'm/día', fmt=F4,
      note='Coincide con q cuando u es pequeño (todo el caudal cruza el cilindro de radio r).')
h.sec('9. Volumen extraído')
h.inp('tV', 'Tiempo de bombeo', 30, 'días')
h.out(None, 'V = Q·t', '{Q}*{tV}', 'm³', fmt=F0, main=True,
      note='En un acuífero confinado infinito todo sale del almacenamiento.')
# ---- tabla W(u)
tlabel(ws, 5, 7, 'Tabla de W(u)', bold=True)
thead(ws, 6, 7, ['u', 'W(u)'])
us = [m * 10.0 ** e for e in range(-10, 1) for m in (1, 2, 5) if m * 10.0 ** e <= 1.0]
for k, uval in enumerate(us):
    rr = 7 + k
    c = tlabel(ws, rr, 7, uval)
    c.number_format = '0E+00'
    c.font = Font(bold=True, size=10)
    tout(ws, rr, 8, f'={W(f"G{rr}")}', fmt=F4)
# ---- cono de abatimiento
thead(ws, 6, 10, ['r (m)', '−s  t₁', '−s  t₂', '−s  t₃', '−s  t₄'])
tlabel(ws, 4, 10, 'Tiempos (días) →', bold=True)
TT = [1 / 24, 1, 30, 365]
for j, tv in enumerate(TT):
    tin(ws, 5, 11 + j, tv, fmt=GEN)
NR = 26
for k in range(NR):
    rr = 7 + k
    tout(ws, rr, 10, f'=0.2*10^({k}*5/{NR - 1})', fmt=GEN)
    for j in range(4):
        col = CL(11 + j)
        u = f'(J{rr}^2*{h.v["S"]}/(4*{h.v["T"]}*{col}$5))'
        tout(ws, rr, 11 + j, f'=-{h.v["Q"]}/(4*PI()*{h.v["T"]})*({W(u)})', fmt=F2)
ch = chart('Cono de abatimiento a distintos tiempos', 'distancia r (m)', 'descenso del nivel (m)',
           logx=True, w=20, h=11)
for j, col in enumerate(['E0A800', '2B8A3E', '1F4E79', 'B03030']):
    serie(ch, ws, 10, 11 + j, 7, 6 + NR, f't = {["1 hora", "1 día", "30 días", "1 año"][j]}', 'line', col)
ws.add_chart(ch, 'J35')

# =========================================================== SUPERPOSICIÓN
h = Hoja('Superposicion', 'Superposición de pozos y pozos imagen',
         'Hasta 4 pozos y una frontera recta x = constante. Incluye un mapa de abatimientos.',
         cols={'G': 9, **{CL(c): 8 for c in range(8, 21)}})
SH['Superposicion'] = h
ws = h.ws
h.sec('1. Acuífero y tiempo')
h.inp('T', 'Transmisividad T', 300, 'm²/día')
h.inp('S', 'Almacenamiento S', 1e-3, '—', fmt=SCI)
h.inp('t', 'Tiempo de bombeo', 30, 'días')
h.inp('rw', 'Radio mínimo (radio del pozo)', 0.1, 'm', note='Evita dividir entre cero si el punto cae sobre un pozo.')
h.sec('2. Punto donde quieres el abatimiento')
h.inp('xp', 'x del punto', 150, 'm')
h.inp('yp', 'y del punto', 86.6, 'm')
h.sec('3. Frontera (opcional)')
h.inp('tipo', 'Tipo de frontera', 'Ninguna', '', note='Elige de la lista: Ninguna, Impermeable o Carga constante (río, lago).')
h.inp('xb', 'Posición de la frontera: recta x =', 450, 'm', note='Orienta tus ejes para que la frontera quede vertical.')
dv = DataValidation(type='list', formula1='"Ninguna,Impermeable,Carga constante"', allow_blank=False)
ws.add_data_validation(dv)
dv.add(h.v['tipo'].replace('$', ''))
h.out('fac', 'Signo del pozo imagen', 'IF({tipo}="Impermeable",1,IF({tipo}="Carga constante",-1,0))', '', fmt=F0,
      note='+1: el imagen bombea (suma). −1: el imagen inyecta (resta). 0: sin frontera.')
# ---- tabla de pozos (filas 7-14)
tlabel(ws, 5, 7, 'Pozos reales (amarillo) y pozos imagen (se calculan solos)', bold=True)
thead(ws, 6, 7, ['Pozo', 'x (m)', 'y (m)', 'Q (m³/día)', 'r al punto (m)', 'u', 'W(u)', 's (m)'])
WELLS = [(0, 0, 1500), (300, 0, 1500), (150, 259.8, 1500), (None, None, None)]
v = h.v
for k in range(8):
    rr = 7 + k
    if k < 4:
        tlabel(ws, rr, 7, f'P{k + 1}', bold=True)
        x, y, q = WELLS[k]
        tin(ws, rr, 8, x)
        tin(ws, rr, 9, y)
        tin(ws, rr, 10, q)
    else:
        src = rr - 4
        tlabel(ws, rr, 7, f'imagen {k - 3}', bold=True)
        tout(ws, rr, 8, f'=2*{v["xb"]}-N(H{src})', fmt=F1)
        tout(ws, rr, 9, f'=N(I{src})', fmt=F1)
        tout(ws, rr, 10, f'=N(J{src})*{v["fac"]}', fmt=F0)
    tout(ws, rr, 11, f'=MAX(SQRT((N(H{rr})-{v["xp"]})^2+(N(I{rr})-{v["yp"]})^2),{v["rw"]})', fmt=F1)
    tout(ws, rr, 12, f'=K{rr}^2*{v["S"]}/(4*{v["T"]}*{v["t"]})', fmt=SCI)
    tout(ws, rr, 13, f'={W(f"L{rr}")}', fmt=F3)
    tout(ws, rr, 14, f'=IF(N(J{rr})=0,0,J{rr}/(4*PI()*{v["T"]})*M{rr})', fmt=F3, main=True)
h.sec('4. Resultado en el punto')
h.out('sr', 'Abatimiento de los pozos reales', 'SUM($N$7:$N$10)', 'm', fmt=F3)
h.out('si', 'Aporte de los pozos imagen', 'SUM($N$11:$N$14)', 'm', fmt=F3)
h.out(None, 'ABATIMIENTO TOTAL', '{sr}+{si}', 'm', fmt=F3, main=True)
h.out(None, 'Efecto de la frontera', 'IF({sr}=0,0,{si}/{sr})', 'respecto a sin frontera', fmt='+0%;-0%;0%')
h.chk('Lado de la frontera', 'IF({fac}=0,"✔ sin frontera",IF(SIGN({xp}-{xb})=SIGN(N($H$7)-{xb}),"✔ el punto está del mismo lado que los pozos","✘ el punto está al otro lado de la frontera: el resultado no tiene sentido"))')
h.sec('5. Mapa de abatimientos (rango del mapa)')
h.inp('x0', 'x mínimo', -200, 'm')
h.inp('x1', 'x máximo', 500, 'm')
h.inp('y0', 'y mínimo', -200, 'm')
h.inp('y1', 'y máximo', 460, 'm')
h.note('El mapa de la derecha suma todos los pozos en una malla de 13 × 13 puntos. Las celdas '
       'oscuras tienen más abatimiento. Si hay frontera, el otro lado queda en blanco.')
N_ = 13
MR, MC = 18, 8          # fila de las x y columna de las y del mapa
tlabel(ws, MR - 1, 7, 'Mapa de abatimientos s (m). Filas: y. Columnas: x.', bold=True)
c = ws.cell(row=MR, column=7, value='y \\ x')
c.fill, c.font = FILL_HEAD, F_HEAD
for i in range(N_):
    c = ws.cell(row=MR, column=MC + i, value=f'={v["x0"]}+{i}*({v["x1"]}-{v["x0"]})/{N_ - 1}')
    c.fill, c.font, c.number_format = FILL_HEAD, F_HEAD, F0
for j in range(N_):
    c = ws.cell(row=MR + 1 + j, column=7, value=f'={v["y1"]}-{j}*({v["y1"]}-{v["y0"]})/{N_ - 1}')
    c.fill, c.font, c.number_format = FILL_HEAD, F_HEAD, F0

# ---- hoja auxiliar oculta con los bloques u y s de cada pozo
ax = wb.create_sheet('Aux_mapa')
ax.sheet_state = 'hidden'
SP = "'Superposicion'!"
for w_ in range(8):
    wr = 7 + w_
    base = 1 + w_ * (N_ + 2)
    for j in range(N_):
        for i in range(N_):
            gx = f'{SP}{CL(MC + i)}${MR}'
            gy = f'{SP}$G${MR + 1 + j}'
            ucell = ax.cell(row=base + j, column=2 + i)
            ucell.value = (f'=MAX(({gx}-N({SP}$H${wr}))^2+({gy}-N({SP}$I${wr}))^2,{SP}{v["rw"]}^2)'
                           f'*{SP}{v["S"]}/(4*{SP}{v["T"]}*{SP}{v["t"]})')
            uref = f'{CL(2 + i)}{base + j}'
            ax.cell(row=base + j, column=17 + i).value = (
                f'=IF(N({SP}$J${wr})=0,0,{SP}$J${wr}/(4*PI()*{SP}{v["T"]})*({W(uref)}))')
for j in range(N_):
    for i in range(N_):
        terms = '+'.join(f"'Aux_mapa'!{CL(17 + i)}{1 + w_ * (N_ + 2) + j}" for w_ in range(8))
        gx = f'{CL(MC + i)}${MR}'
        c = ws.cell(row=MR + 1 + j, column=MC + i)
        c.value = (f'=IF(AND({v["fac"]}<>0,SIGN({gx}-{v["xb"]})<>SIGN(N($H$7)-{v["xb"]})),"",{terms})')
        c.number_format = F1
        c.border = BOX
        c.alignment = Alignment(horizontal='center')
rngmap = f'{CL(MC)}{MR + 1}:{CL(MC + N_ - 1)}{MR + N_}'
ws.conditional_formatting.add(rngmap, ColorScaleRule(start_type='min', start_color='FFFFFF',
                                                     mid_type='percentile', mid_value=50, mid_color='9DC3E6',
                                                     end_type='max', end_color='1F4E79'))
tlabel(ws, MR + N_ + 1, 7, 'Ejemplo cargado: 3 pozos de 1500 m³/día en triángulo; el punto (150, 86.6) '
       'está a 173 m de cada uno. Total = 7.77 m, el triple de un pozo aislado.', italic=True)

# =========================================================== DUPUIT CON RECARGA
h = Hoja('Dupuit_recarga', 'Dupuit-Forchheimer con recarga uniforme',
         'Acuífero libre entre dos cuerpos de agua. Dos casos de recarga lado a lado (apuntes, página 2).',
         widths={'C': 16, 'D': 16}, cols={'G': 9, 'H': 11, 'I': 11, 'J': 11, 'K': 12, 'L': 12})
SH['Dupuit_recarga'] = h
ws = h.ws
h.sec('1. Datos comunes')
h.inp('K', 'Conductividad K', 10, 'm/día')
h.inp('h1', 'Nivel en x = 0, h₁ (desde la base)', 15, 'm')
h.inp('h2', 'Nivel en x = L, h₂ (desde la base)', 18, 'm')
h.inp('L', 'Longitud L', 200, 'm')
h.inp('dpy', 'Días por año', 365.25, 'días')
h.sec('2. Recarga y resultados por caso')
h.head2('Caso A', 'Caso B')
h.inp2('Wmm', 'Recarga W (mm/año)', -60, 20, note='Negativa = evapotranspiración neta (el acuífero pierde agua por arriba).')
h.out2('W', 'W en m/día', '{Wmm}/1000/{dpy}', ('Wmm',), fmt=SCI)
h.out2('carga', 'Término de carga K(h₁² − h₂²)/(2L)  (m²/día)', '{K}*({h1}^2-{h2}^2)/(2*{L})', fmt=F4)
h.out2('wl2', 'Término de recarga W·L/2  (m²/día)', '{W}*{L}/2', ('W',), fmt=F4)
h.out2('q0', "q′ en x = 0  (m²/día)", '{carga}-{wl2}', ('carga', 'wl2'), fmt=F4, main=True)
h.out2('qL', "q′ en x = L  (m²/día)", '{carga}+{wl2}', ('carga', 'wl2'), fmt=F4, main=True)
h.out2(None, 'En x = 0 el agua…', 'IF({q0}<0,"sale",IF({q0}>0,"entra","q′ = 0"))', ('q0',), fmt=None)
h.out2(None, 'En x = L el agua…', 'IF({qL}>0,"sale",IF({qL}<0,"entra","q′ = 0"))', ('qL',), fmt=None)
h.chk2('Balance: q′(L) − q′(0) = W·L', 'IF(ABS(({qL}-{q0})-{W}*{L})<0.000001,"✔ cierra","✘ no cierra")', ('qL', 'q0', 'W'))
h.out2(None, 'Quién domina', 'IF(ABS({carga})>ABS({wl2}),"la diferencia de carga","la recarga")', ('carga', 'wl2'), fmt=None)
h.out2('d', 'Divisoria d = L/2 − (K/W)(h₁² − h₂²)/(2L)  (m)', 'IF({W}=0,"no aplica",{L}/2-({K}/{W})*({h1}^2-{h2}^2)/(2*{L}))', ('W',), fmt=F1)
h.chk2('¿La divisoria cae dentro del acuífero?', 'IF(ISNUMBER({d}),IF(AND({d}>=0,{d}<={L}),"✔ sí: 0 ≤ d ≤ L, hay montículo","⚠ no: d cae fuera, NO hay divisoria ni h máx"),"⚠ no hay divisoria")', ('d',))
h.out2('hmax', 'h máx en la divisoria (m)', 'IF(ISNUMBER({d}),IF(AND({d}>=0,{d}<={L}),SQRT({h1}^2-({h1}^2-{h2}^2)*{d}/{L}+({W}/{K})*({L}-{d})*{d}),"no existe"),"no existe")', ('d', 'W'), fmt=F3, main=True)
h.sec('3. ¿Cuánta recarga haría falta para que aparezca divisoria?')
h.out(None, 'Recarga mínima |W| = 2·|K(h₁² − h₂²)/(2L)| / L', '2*ABS({carga_A})/{L}*1000*{dpy}', 'mm/año', fmt=F0, main=True)
h.note('En el ejemplo de clase la recarga mínima es unos 9000 mm/año: imposible. Por eso NO hay '
       'divisoria ni h máx, y el nivel freático sube monótonamente de h₁ a h₂. Esa es la respuesta.')
NP = 21
tlabel(ws, 5, 7, 'Perfil del nivel freático', bold=True)
thead(ws, 6, 7, ['x (m)', 'h caso A', 'h caso B', 'h sin recarga', "q′ caso A", "q′ caso B"])
v = h.v
for k in range(NP):
    rr = 7 + k
    tout(ws, rr, 7, f'={v["L"]}*{k}/{NP - 1}', fmt=F1)
    for j, (Wc) in enumerate([v['W_A'], v['W_B'], '0']):
        arg = f'{v["h1"]}^2-({v["h1"]}^2-{v["h2"]}^2)*G{rr}/{v["L"]}+({Wc}/{v["K"]})*({v["L"]}-G{rr})*G{rr}'
        tout(ws, rr, 8 + j, f'=IF(({arg})<0,NA(),SQRT({arg}))', fmt=F3)
    tout(ws, rr, 11, f'={v["carga_A"]}-{v["W_A"]}*({v["L"]}/2-G{rr})', fmt=F4)
    tout(ws, rr, 12, f'={v["carga_B"]}-{v["W_B"]}*({v["L"]}/2-G{rr})', fmt=F4)
ch = chart('Perfil del nivel freático (Dupuit con recarga)', 'x (m)', 'h (m sobre la base)', w=20, h=11)
serie(ch, ws, 7, 8, 7, 6 + NP, 'caso A', 'line', 'B03030')
serie(ch, ws, 7, 9, 7, 6 + NP, 'caso B', 'line', '1F4E79')
serie(ch, ws, 7, 10, 7, 6 + NP, 'sin recarga', 'line', '7F7F7F', dash='dash')
ws.add_chart(ch, 'G30')

# =========================================================== COSTA
h = Hoja('Costa', 'Acuíferos costeros e intrusión salina',
         'Ghyben-Herzberg, upconing, cuña de Glover y el problema de cambio climático de clase.',
         widths={'C': 16, 'D': 16}, cols={'G': 9, 'H': 12, 'I': 12, 'J': 12, 'K': 12})
SH['Costa'] = h
ws = h.ws
h.sec('1. Ghyben-Herzberg')
h.inp('rf', 'Densidad del agua dulce ρf', 1.000, 'g/cm³', fmt=F3)
h.inp('rs', 'Densidad del agua salada ρs', 1.025, 'g/cm³', fmt=F3)
h.inp('hg', 'Nivel de agua dulce sobre el mar h', 0.75, 'm')
h.out('G', 'G = (ρs − ρf)/ρf', '({rs}-{rf})/{rf}', '—', fmt=F4)
h.out(None, 'Factor ρf/(ρs − ρf)', '{rf}/({rs}-{rf})', '—', fmt=F1, main=True, note='Con agua de mar: 40.')
h.out(None, 'Profundidad de la interfaz bajo el mar z = h·ρf/(ρs − ρf)', '{hg}*{rf}/({rs}-{rf})', 'm', fmt=F2, main=True)
h.sec('2. Upconing: caudal máximo bajo un pozo (ejercicio 5.5)')
h.inp('du', 'Distancia del fondo del pozo a la interfaz d', 12.192, 'm', note='40 ft = 12.192 m.')
h.inp('Ku', 'Conductividad K', 1e-3, 'm/s', fmt=SCI)
h.inp('Gu', 'Densidad relativa G', 0.025, '—')
h.inp('fu', 'Ascenso admisible (fracción de d)', 0.3, '—', note='Criterio de estabilidad: z ≤ 0.3·d.')
h.out('Qmu', 'Q máx = 2π·(fracción)·K·d²·G', '2*PI()*{fu}*{Ku}*{du}^2*{Gu}', 'm³/s', fmt=SCI, main=True,
      note='Con fracción 0.3 es la fórmula 0.6π·K·d²·G.')
h.out(None, 'Q máx en L/s', '{Qmu}*1000', 'L/s', fmt=F2)
h.out(None, 'Q máx en m³/día', '{Qmu}*86400', 'm³/día', fmt=F0)
h.out(None, 'Q máx en gpm', '{Qmu}*1000*15.850323', 'gpm', fmt=F0)
h.inp('Qt', 'Caudal que piensas bombear', 0.005, 'm³/s', fmt=GEN)
h.out('zu', 'Ascenso de la interfaz z = Q/(2π·K·d·G)', '{Qt}/(2*PI()*{Ku}*{du}*{Gu})', 'm', fmt=F2)
h.chk('¿Es estable?', 'IF({zu}<={fu}*{du},"✔ estable: el ascenso no supera "&ROUND({fu}*{du},2)&" m","✘ inestable: la interfaz colapsa hacia el pozo")')
h.sec('3. Cuña salina de Glover (ejercicio 5.6)')
h.inp('qg', "Caudal de agua dulce al mar q′ (por unidad de costa)", 2e-4, 'ft³/s por ft', fmt=SCI,
      note='Unidades consistentes con K y B. El enunciado del libro trae 2×10⁻¹ (errata).')
h.inp('Kg', 'Conductividad K', 3.3e-3, 'ft/s', fmt=SCI)
h.inp('Bg', 'Espesor del acuífero B', 100, 'ft')
h.inp('Gg', 'Densidad relativa G', 0.025, '—')
h.out('KG', 'K·G', '{Kg}*{Gg}', '', fmt=SCI)
h.out(None, "Profundidad de la interfaz en la costa = q′/(KG)", '{qg}/{KG}', 'ft', fmt=F2)
h.out('xt', "x_toe = KGB²/(2q′) − q′/(2KG)", '{KG}*{Bg}^2/(2*{qg})-{qg}/(2*{KG})', 'ft', fmt=F1, main=True)
h.out(None, 'x_toe con la mitad del caudal', '{KG}*{Bg}^2/(2*{qg}/2)-({qg}/2)/(2*{KG})', 'ft', fmt=F1, main=True)
h.out('ig', "Gradiente implícito i = q′/(K·B)", '{qg}/({Kg}*{Bg})', '—', fmt=SCI)
h.chk('¿Hay cuña?', 'IF({xt}<0,"✘ x_toe < 0: no hay cuña (el agua dulce expulsa al mar)","✔ hay cuña: el pie está a "&ROUND({xt},0)&" tierra adentro")')
h.chk('¿El gradiente es razonable?', 'IF({ig}>0.01,"✘ gradiente > 0.01: inverosímil en un acuífero costero, revisa q′","✔ gradiente en el rango real (10⁻⁴ a 10⁻³)")')

h.sec('4. Problema de clase: cambio climático (apuntes, páginas 3 y 4)')
h.inp('Wmm', 'Recarga W', 500, 'mm/año')
h.inp('L0', 'Largo inicial del acuífero L₀', 1000, 'm')
h.inp('Kc', 'Conductividad K', 1e-4, 'm/s', fmt=SCI)
h.inp('rfc', 'ρf', 1.000, '', fmt=F3)
h.inp('rsc', 'ρs', 1.025, '', fmt=F3)
h.inp('s0', 'Profundidad del fondo bajo el mar s₀', 30, 'm')
h.inp('tan', 'Pendiente de la playa tan θ', 0.02, '—')
h.inp('dS', 'Subida del nivel del mar ΔS', 0.6, 'm')
h.inp('dce', 'Erosión costera ΔL_CE', 3, 'm')
h.inp('xe', 'Punto donde evaluar el nivel freático x', 10, 'm', note='Medido desde la divisoria (x = 0).')
h.out('Ws', 'W en m/s (¡mismas unidades que K!)', '{Wmm}/1000/(365.25*86400)', 'm/s', fmt=SCI)
h.out('dr', 'Δρ = ρs − ρf', '{rsc}-{rfc}', '', fmt=F3)
h.out('C', 'C = ρs·Δρ·K / (ρf²·W)', '{rsc}*{dr}*{Kc}/({rfc}^2*{Ws})', '—', fmt=F2, main=True)
h.out('dL', 'Retroceso de la costa ΔL = −ΔS/tan θ − ΔL_CE', '-{dS}/{tan}-{dce}', 'm', fmt=F1, main=True,
      note='Con playa al 2 %, 0.6 m de mar son 30 m de retroceso horizontal.')
h.head2('Antes', 'Después')
h.out2('Lx', 'Largo del acuífero L (m)', ('{L0}', '{L0}+{dL}'), fmt=F1)
h.out2('sx', 'Profundidad del fondo bajo el mar s (m)', ('{s0}', '{s0}+{dS}'), fmt=F2)
h.out2('xT', 'Punta de la cuña x_T = √(L² − C·s²)  (m)', 'IF({Lx}^2-{C}*{sx}^2<0,0,SQRT({Lx}^2-{C}*{sx}^2))', ('Lx', 'sx'), fmt=F1, main=True)
h.out2('inv', 'Longitud invadida L − x_T (m)', '{Lx}-{xT}', ('Lx', 'xT'), fmt=F1)
h.out2('Hx', 'Carga desde la base H(x) = √[(W/K)(L² − x²) + (ρs/ρf)s²]  (m)', 'SQRT(({Ws}/{Kc})*({Lx}^2-{xe}^2)+({rsc}/{rfc})*{sx}^2)', ('Lx', 'sx'), fmt=F3, main=True)
h.out2('hs', 'Nivel freático sobre el mar H − s (m)', '{Hx}-{sx}', ('Hx', 'sx'), fmt=F3)
h.out(None, 'Desplazamiento de la punta Δx_T', '{xT_B}-{xT_A}', 'm', fmt=F1, main=True)
h.out(None, 'Avance REAL de la cuña respecto a la costa', '{inv_B}-{inv_A}', 'm', fmt=F1, main=True,
      note='La punta se mueve más, pero gran parte es sólo la costa que retrocede.')
h.out(None, 'Subida absoluta del nivel freático', '{Hx_B}-{Hx_A}', 'm', fmt=F3, main=True)
h.out('dhs', 'Cambio del nivel freático RESPECTO AL MAR', '{hs_B}-{hs_A}', 'm', fmt=F3)
h.out(None, 'Equivale a perder de agua dulce en profundidad', '-{dhs}*{rfc}/{dr}', 'm', fmt=F1,
      note='Por Ghyben-Herzberg (×40). Por eso avanza la cuña aunque el nivel suba.')
h.out('Ht', 'Comprobación: H(x_T) − s antes', 'SQRT(({Ws}/{Kc})*({L0}^2-{xT_A}^2)+({rsc}/{rfc})*{s0}^2)-{s0}', 'm', fmt=F3)
h.out('Htt', 'Teórico s·Δρ/ρf', '{s0}*{dr}/{rfc}', 'm', fmt=F3)
h.chk('Consistencia de las fórmulas', 'IF(ABS({Ht}-{Htt})<0.001,"✔ en la punta de la cuña se cumple Ghyben-Herzberg exactamente","✘ revisa las unidades de W y K")')
# ---- perfil
FR = [0, .1, .2, .3, .4, .5, .6, .7, .8] + [round(0.8 + 0.01 * i, 2) for i in range(1, 21)]
tlabel(ws, 5, 7, 'Perfil (elevaciones respecto al nivel del mar inicial)', bold=True)
thead(ws, 6, 7, ['x (m)', 'nivel freático antes', 'nivel freático después', 'interfaz antes', 'interfaz después'])
v = h.v
Hb = lambda L, s, x: f'SQRT(({v["Ws"]}/{v["Kc"]})*({L}^2-{x}^2)+({v["rsc"]}/{v["rfc"]})*{s}^2)'
for k, fr in enumerate(FR):
    rr = 7 + k
    tout(ws, rr, 7, f'={v["L0"]}*{fr}', fmt=F0)
    x = f'G{rr}'
    tout(ws, rr, 8, f'=IF({x}<={v["Lx_A"]},{Hb(v["Lx_A"], v["sx_A"], x)}-{v["s0"]},NA())', fmt=F3)
    tout(ws, rr, 9, f'=IF({x}<={v["Lx_B"]},{Hb(v["Lx_B"], v["sx_B"], x)}-{v["s0"]},NA())', fmt=F3)
    tout(ws, rr, 10, f'=IF(OR({x}>{v["Lx_A"]},{x}<{v["xT_A"]}),NA(),-H{rr}*{v["rfc"]}/{v["dr"]})', fmt=F2)
    tout(ws, rr, 11, f'=IF(OR({x}>{v["Lx_B"]},{x}<{v["xT_B"]}),NA(),{v["dS"]}-(I{rr}-{v["dS"]})*{v["rfc"]}/{v["dr"]})', fmt=F2)
NF = len(FR)
ch = chart('Interfaz agua dulce / agua salada', 'x desde la divisoria (m)', 'elevación (m)', w=20, h=11,
           ymin=-35)
serie(ch, ws, 7, 10, 7, 6 + NF, 'interfaz antes', 'line', '1F4E79')
serie(ch, ws, 7, 11, 7, 6 + NF, 'interfaz después', 'line', 'B03030', dash='dash')
ws.add_chart(ch, 'G38')
ch2 = chart('Nivel freático (sobre el mar inicial)', 'x desde la divisoria (m)', 'elevación (m)', w=20, h=9, ymin=0)
serie(ch2, ws, 7, 8, 7, 6 + NF, 'antes', 'line', '1F4E79')
serie(ch2, ws, 7, 9, 7, 6 + NF, 'después', 'line', 'B03030', dash='dash')
ws.add_chart(ch2, 'G61')

# =========================================================== CANAL
h = Hoja('Canal', 'Canal a nivel del mar (ejercicio 5.3)',
         'Medio semi-infinito con cambio escalón: h = h₀·erf(x / 2√(νt)) y q′ = h₀√(T·Sy/πt).',
         cols={'G': 10, 'H': 11, 'I': 11, 'J': 11, 'K': 11, 'L': 12, 'M': 12, 'N': 12})
SH['Canal'] = h
ws = h.ws
h.sec('1. Datos')
h.inp('h0', 'Carga inicial h₀ (nivel freático sobre el canal)', 12, 'm')
h.inp('Kcm', 'Conductividad K', 8.35, 'cm/día')
h.inp('Sy', 'Rendimiento específico Sy', 0.01, '—')
h.inp('bm', 'Espesor saturado medio (linealización)', 15, 'm', note='(21 + 9)/2 = 15 m. Prueba 21 m para ver la sensibilidad.')
h.inp('Lc', 'Distancia a la divisoria L', 4828.032, 'm', fmt=F1, note='3 millas.')
h.out('Km', 'K en m/día', '{Kcm}/100', 'm/día', fmt=F4)
h.out('T', 'T = K·b', '{Km}*{bm}', 'm²/día', fmt=F4)
h.out('nu', 'Difusividad ν = T/Sy', '{T}/{Sy}', 'm²/día', fmt=F2, main=True)
h.note('En el canal (x = 0) la carga es 0 para todo t: es la condición de borde. La tabla de la '
       'derecha da la carga en la divisoria y el caudal hacia el canal para cuatro tiempos.')
tlabel(ws, 5, 7, 'Resultados por tiempo (escribe los años en amarillo)', bold=True)
thead(ws, 6, 7, ['t (años)', 't (días)', 'L / 2√(νt)', 'erf', 'h en la divisoria (m)', 'abatimiento (m)',
                 "q′ (m³/día por m)", "q′ (L/día por m)"])
v = h.v
for k, yr in enumerate([10, 20, 40, 100]):
    rr = 7 + k
    tin(ws, rr, 7, yr)
    tout(ws, rr, 8, f'=G{rr}*365.25', fmt=F0)
    tout(ws, rr, 9, f'={v["Lc"]}/(2*SQRT({v["nu"]}*H{rr}))', fmt=F3)
    tout(ws, rr, 10, f'=ERF(I{rr})', fmt='0.00000')
    tout(ws, rr, 11, f'={v["h0"]}*J{rr}', fmt=F2, main=True)
    tout(ws, rr, 12, f'={v["h0"]}-K{rr}', fmt=F2)
    tout(ws, rr, 13, f'={v["h0"]}*SQRT({v["T"]}*{v["Sy"]}/(PI()*H{rr}))', fmt=SCI, main=True)
    tout(ws, rr, 14, f'=M{rr}*1000', fmt=F2)
h.sec('2. Comprobación  q′ ∝ t^(−1/2)')
h.out('rq', "q′(t₁)/q′(t₄)", "'Canal'!$M$7/'Canal'!$M$10", '', fmt=F3)
h.out('rt', '√(t₄/t₁)', "SQRT('Canal'!$H$10/'Canal'!$H$7)", '', fmt=F3)
h.chk('Verificación', 'IF(ABS({rq}-{rt})<0.001,"✔ el caudal decae con la raíz del tiempo","✘ revisa los datos")')
h.note('Si el canal recibe agua por los dos flancos, multiplica q′ por 2.')
tlabel(ws, 13, 7, 'Perfil del nivel freático h(x, t)', bold=True)
thead(ws, 14, 7, ['x (m)', 't₁', 't₂', 't₃', 't₄'])
NP = 21
for k in range(NP):
    rr = 15 + k
    tout(ws, rr, 7, f'={v["Lc"]}*{k}/{NP - 1}', fmt=F0)
    for j in range(4):
        tout(ws, rr, 8 + j, f'={v["h0"]}*ERF(G{rr}/(2*SQRT({v["nu"]}*$H${7 + j})))', fmt=F2)
ch = chart('Descenso del nivel freático hacia el canal', 'distancia al canal x (m)', 'h (m sobre el canal)',
           w=20, h=11, ymin=0)
for j, col in enumerate(['1F4E79', '2B8A3E', 'E0A800', 'B03030']):
    s = serie(ch, ws, 7, 8 + j, 15, 14 + NP, f't{j + 1}', 'line', col)
ws.add_chart(ch, 'G38')

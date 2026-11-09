"""Hojas de fundamentos."""
from xl_lib import *

SH = {}

# =========================================================== UNIDADES
h = Hoja('Unidades', 'Conversión de unidades',
         'Escribe el valor en la celda amarilla: los equivalentes salen en verde.')
SH['Unidades'] = h
h.sec('1. Conductividad hidráulica K')
h.inp('K', 'K', 1e-6, 'm/s', fmt=SCI)
h.out(None, 'K en m/día', '{K}*86400', 'm/día', fmt=GEN)
h.out(None, 'K en cm/s', '{K}*100', 'cm/s', fmt=GEN)
h.out(None, 'K en ft/s', '{K}/0.3048', 'ft/s', fmt=GEN)
h.out(None, 'K en ft/día', '{K}/0.3048*86400', 'ft/día', fmt=GEN)
h.out(None, 'K en galones/día por ft²', '{K}/0.3048*7.48052*86400', 'gpd/ft²', fmt=GEN,
      note='Ejercicio 3.8(b) del taller: con 10⁻⁶ m/s da 2.12.')
h.inp('Kmd', 'K (si la tienes en m/día)', 10, 'm/día')
h.out(None, 'K en m/s', '{Kmd}/86400', 'm/s', fmt=GEN)
h.sec('2. Permeabilidad intrínseca  k = K·μ / (ρ·g)')
h.inp('mu', 'Viscosidad μ', 1.0e-3, 'Pa·s', fmt=SCI,
      note='1.00×10⁻³ a 20 °C y 1.124×10⁻³ a 15.6 °C. Declara la temperatura que usas.')
h.inp('rho', 'Densidad del agua ρ', 1000, 'kg/m³')
h.inp('g', 'Gravedad g', 9.81, 'm/s²')
h.out('k', 'k en m²', '{K}*{mu}/({rho}*{g})', 'm²', fmt=SCI)
h.out(None, 'k en cm²', '{k}*10000', 'cm²', fmt=SCI, note='1 m² = 10⁴ cm² (al cuadrado, no 10²).')
h.out('kd', 'k en darcy', '{k}*10000/9.869233E-09', 'darcy', fmt=F4)
h.out(None, 'k en milidarcy', '{kd}*1000', 'md', fmt=F1)
h.sec('3. Caudal')
h.inp('Qls', 'Caudal Q', 20, 'L/s')
h.out(None, 'Q en m³/día', '{Qls}*86.4', 'm³/día', fmt=F1)
h.out(None, 'Q en m³/s', '{Qls}/1000', 'm³/s', fmt=GEN)
h.out(None, 'Q en galones/min (US)', '{Qls}*15.850323', 'gpm', fmt=F1)
h.out(None, 'Q en ft³/día', '{Qls}/1000/0.0283168*86400', 'ft³/día', fmt=F0)
h.inp('Qg', 'Caudal Q', 500, 'gal/min (US)')
h.out(None, 'Q en ft³/día', '{Qg}*1440/7.48052', 'ft³/día', fmt=F0,
      note='Apuntes, página 8: 500 gal/min = 96 250 ft³/día.')
h.out(None, 'Q en m³/día', '{Qg}*0.003785412*1440', 'm³/día', fmt=F1)
h.out(None, 'Q en L/s', '{Qg}/15.850323', 'L/s', fmt=F2)
h.inp('Qm', 'Caudal Q', 1500, 'm³/día')
h.out(None, 'Q en L/s', '{Qm}/86.4', 'L/s', fmt=F2)
h.out(None, 'Q en m³/s', '{Qm}/86400', 'm³/s', fmt=GEN)
h.sec('4. Recarga y tiempo')
h.inp('Wmm', 'Recarga W', 500, 'mm/año')
h.out(None, 'W en m/día', '{Wmm}/1000/365.25', 'm/día', fmt=GEN)
h.out(None, 'W en m/s', '{Wmm}/1000/(365.25*86400)', 'm/s', fmt=SCI)
h.inp('tmin', 'Tiempo', 360, 'min')
h.out(None, 'en días', '{tmin}/1440', 'días', fmt=GEN)
h.inp('th', 'Tiempo', 12, 'horas')
h.out(None, 'en días', '{th}/24', 'días', fmt=GEN)
h.inp('ty', 'Tiempo', 10, 'años')
h.out(None, 'en días', '{ty}*365.25', 'días', fmt=F1)
h.sec('5. Transmisividad')
h.inp('Tm', 'T', 300, 'm²/día')
h.out(None, 'T en m²/s', '{Tm}/86400', 'm²/s', fmt=SCI)
h.out('Tft', 'T en ft²/día', '{Tm}/0.09290304', 'ft²/día', fmt=F0)
h.out(None, 'T en galones/día por ft', '{Tft}*7.48052', 'gpd/ft', fmt=F0)
h.sec('6. Peso unitario, presión y longitud')
h.inp('glb', 'Peso unitario', 62.4, 'lb/ft³')
h.out(None, 'en kN/m³', '{glb}*0.1570875', 'kN/m³', fmt=F3)
h.inp('plb', 'Esfuerzo o presión', 6250, 'lb/ft²')
h.out(None, 'en kPa', '{plb}*0.04788026', 'kPa', fmt=F1)
h.inp('mi', 'Longitud', 3, 'millas')
h.out(None, 'en metros', '{mi}*1609.344', 'm', fmt=F1)
h.inp('ft', 'Longitud', 40, 'ft')
h.out(None, 'en metros', '{ft}*0.3048', 'm', fmt=F3)

# =========================================================== PAPEL LOG
h = Hoja('Papel_log', 'Papel logarítmico y semilogarítmico',
         'Ubicar números en un ciclo y leer una recta con dos puntos (Guía, Parte 1).',
         cols={'G': 10, 'H': 14})
SH['Papel_log'] = h
h.sec('1. ¿En qué porcentaje del ciclo cae un número?')
h.inp('n', 'Número', 3.5)
h.out(None, 'Inicio de su ciclo (potencia de 10)', '10^INT(LOG10({n}))', '', fmt=GEN)
h.out(None, 'Posición dentro del ciclo', 'LOG10({n})-INT(LOG10({n}))', '', fmt=PCT, main=True,
      note='Mídela desde el inicio del ciclo con la regla: es la fracción del ancho del ciclo.')
h.sec('2. ¿Qué número cae en cierta posición de un ciclo?')
h.inp('st', 'Inicio del ciclo', 100)
h.inp('fr', 'Posición (fracción del ancho del ciclo)', 0.65, '', fmt='0%')
h.out(None, 'Número en esa posición', '{st}*10^{fr}', '', fmt=F2, main=True)
h.sec('3. El punto medio de un ciclo')
h.inp('a', 'Extremo inferior', 10)
h.inp('b', 'Extremo superior', 100)
h.out(None, 'Punto medio en el papel (media geométrica)', 'SQRT({a}*{b})', '', fmt=F2, main=True)
h.out(None, 'Promedio aritmético (NO es el punto medio)', '({a}+{b})/2', '', fmt=F2)
h.sec('4. Leer una recta con dos puntos (lo que harás en el parcial)')
h.note('Escribe dos puntos cualesquiera de tu recta s–log t. No hace falta que estén separados '
       'un ciclo: la fórmula normaliza la pendiente.')
h.inp('t1', 't₁', 20, 'min')
h.inp('s1', 's₁', 0.60, 'm')
h.inp('t2', 't₂', 200, 'min')
h.inp('s2', 's₂', 1.42, 'm')
h.out('cy', 'Ciclos entre los dos puntos = log₁₀(t₂/t₁)', 'LOG10({t2}/{t1})', 'ciclos', fmt=F3)
h.out('ds', 'Δs por ciclo = (s₂ − s₁) / ciclos', '({s2}-{s1})/{cy}', 'm', fmt=F3, main=True)
h.out('t0', 't₀ = t₁ · 10^(−s₁/Δs)', '{t1}*10^(-{s1}/{ds})', 'min', fmt=F2, main=True)
h.out('t0d', 't₀ en días', '{t0}/1440', 'días', fmt='0.000000')
h.inp('Q', 'Caudal Q (opcional, para T y S)', 1200, 'm³/día')
h.inp('r', 'Distancia r', 40, 'm')
h.out('T', 'T = 2.303·Q / (4π·Δs)', '2.303*{Q}/(4*PI()*{ds})', 'm²/día', fmt=F1, main=True)
h.out(None, 'S = 2.25·T·t₀ / r²', '2.25*{T}*{t0d}/{r}^2', '—', fmt=SCI, main=True)
h.note('Ejemplo 1.2 de la Guía: con (20 min, 0.60 m) y (200 min, 1.42 m) salen Δs = 0.82 m, '
       't₀ = 3.71 min, T = 268 m²/día y S = 9.7×10⁻⁴.')
ws = h.ws
thead(ws, 6, 7, ['Número', 'Posición en el ciclo'])
for i, n in enumerate(range(1, 11)):
    tlabel(ws, 7 + i, 7, n)
    tout(ws, 7 + i, 8, f'=LOG10(G{7 + i})', fmt='0%')
tlabel(ws, 18, 7, 'Para dibujar un ciclo a mano basta con 2 → 30 %, 3 → 48 %, 4 → 60 %, 5 → 70 %.',
       italic=True)

# =========================================================== DARCY
h = Hoja('Darcy', 'Ley de Darcy, cargas y gradientes',
         'Descarga específica, velocidad real, piezómetros y problema de los tres puntos.',
         cols={c: 12 for c in 'GHIJKLM'})
SH['Darcy'] = h
h.sec('1. Descarga específica, caudal y velocidad real')
h.inp('K', 'Conductividad hidráulica K', 1e-6, 'm/s', fmt=SCI)
h.inp('i', 'Gradiente hidráulico i', 0.019, '—')
h.inp('A', 'Área transversal A', 1, 'm²')
h.inp('ne', 'Porosidad efectiva nₑ', 0.1, '—')
h.inp('L', 'Distancia a recorrer', 100, 'm')
h.out('q', 'q = K·i', '{K}*{i}', 'm/s', fmt=SCI, main=True)
h.out('qd', 'q en m/día', '{q}*86400', 'm/día', fmt=GEN)
h.out(None, 'q en m/año', '{qd}*365.25', 'm/año', fmt=F3)
h.out(None, 'Q = q·A', '{q}*{A}', 'm³/s', fmt=SCI)
h.out(None, 'Q en m³/día', '{q}*{A}*86400', 'm³/día', fmt=GEN)
h.out('v', 'v = q/nₑ (velocidad real)', '{q}/{ne}', 'm/s', fmt=SCI, main=True,
      note='Siempre v > q, porque nₑ < 1. Si te sale al revés, invertiste la fórmula.')
h.out('vd', 'v en m/día', '{v}*86400', 'm/día', fmt=GEN)
h.out('tv', 'Tiempo de viaje = L/v', '{L}/{vd}', 'días', fmt=F1)
h.out(None, 'Tiempo de viaje en años', '{tv}/365.25', 'años', fmt=F2)
h.sec('2. Gradiente entre dos piezómetros')
h.inp('h1', 'Carga en el punto 1', 105, 'm')
h.inp('h2', 'Carga en el punto 2', 100, 'm')
h.inp('Lg', 'Distancia entre ellos', 500, 'm')
h.out(None, 'Gradiente i = |h₁ − h₂| / L', 'ABS({h1}-{h2})/{Lg}', '—', fmt=F4, main=True)
h.out(None, 'Sentido del flujo', 'IF({h1}>{h2},"del punto 1 al punto 2",IF({h1}<{h2},"del punto 2 al punto 1","no hay flujo"))', '', fmt=None)
h.sec('3. Un piezómetro: h = z + hₚ')
h.inp('cota', 'Cota del terreno', 450, 'm')
h.inp('prof', 'Profundidad del piezómetro', 180, 'm')
h.inp('nivel', 'Profundidad del nivel de agua bajo el terreno', 12, 'm')
h.out('zp', 'Carga de elevación z (cota del fondo)', '{cota}-{prof}', 'm', fmt=F2)
h.out('hp', 'Carga total h (cota del nivel de agua)', '{cota}-{nivel}', 'm', fmt=F2, main=True)
h.out('hpp', 'Carga de presión hₚ = h − z', '{hp}-{zp}', 'm', fmt=F2, main=True)
h.chk('Verificación', 'IF(ABS({hpp}-({prof}-{nivel}))<0.0001,"✔ hₚ coincide con la columna de agua dentro del tubo","✘ revisa los datos")')

# ---- tabla de piezómetros (ejercicio 3.7)
h.sec('4. Tabla de piezómetros alineados (ejercicio 3.7 del taller)')
r0 = h.r
h.inp('hA', 'Carga total en el primer piezómetro', 300, 'm')
h.inp('ig', 'Gradiente hidráulico', 0.019, '—')
h.inp('sep', 'Separación entre piezómetros', 5000, 'm')
h.note('En la tabla de la derecha escribe la profundidad de cada piezómetro y a qué profundidad '
       'bajo su tope está el agua (0 si el agua llega al tope, como en el taller).')
ws = h.ws
thead(ws, r0, 7, ['Piezómetro', 'Distancia (m)', 'Profundidad (m)', 'Agua bajo el tope (m)',
                  'h total (m)', 'hₚ presión (m)', 'z elevación (m)'])
for k, (nm, dep) in enumerate(zip('ABCDEF', [200, 190, 50, 8, None, None])):
    rr = r0 + 1 + k
    tlabel(ws, rr, 7, nm, bold=True)
    tout(ws, rr, 8, f'={k}*{h.v["sep"]}', fmt=F0)
    tin(ws, rr, 9, dep)
    tin(ws, rr, 10, 0 if dep is not None else None)
    tout(ws, rr, 11, f'=IF(ISNUMBER(I{rr}),{h.v["hA"]}-{h.v["ig"]}*H{rr},"")', fmt=F2, main=True)
    tout(ws, rr, 12, f'=IF(ISNUMBER(I{rr}),I{rr}-N(J{rr}),"")', fmt=F2, main=True)
    tout(ws, rr, 13, f'=IF(ISNUMBER(I{rr}),K{rr}-L{rr},"")', fmt=F2, main=True)
h.to(r0 + 8)

# ---- tres puntos
h.sec('5. Problema de los tres puntos (ejercicio 3.6)')
r0 = h.r
ws = h.ws
thead(ws, r0, 7, ['Pozo', 'x (m, este)', 'y (m, norte)', 'h (m)'])
pts = [('1', 0, 0, 300), ('2', 1000, 0, 400), ('3', 0, 2000, 500)]
for k, (nm, x, y, hh) in enumerate(pts):
    rr = r0 + 1 + k
    tlabel(ws, rr, 7, nm, bold=True)
    tin(ws, rr, 8, x)
    tin(ws, rr, 9, y)
    tin(ws, rr, 10, hh)
    h.v[f'x{k + 1}'] = f'$H${rr}'
    h.v[f'y{k + 1}'] = f'$I${rr}'
    h.v[f'h{k + 1}p'] = f'$J${rr}'
h.note('Escribe las coordenadas y cargas de los tres pozos en la tabla de la derecha. Usa x hacia '
       'el este y y hacia el norte.')
h.out('den', 'Determinante (≠ 0 si no están alineados)',
      '({x2}-{x1})*({y3}-{y1})-({x3}-{x1})*({y2}-{y1})', '', fmt=GEN)
h.out('ga', '∂h/∂x', '(({h2p}-{h1p})*({y3}-{y1})-({h3p}-{h1p})*({y2}-{y1}))/{den}', 'm/m', fmt=F4)
h.out('gb', '∂h/∂y', '(({x2}-{x1})*({h3p}-{h1p})-({x3}-{x1})*({h2p}-{h1p}))/{den}', 'm/m', fmt=F4)
h.out(None, 'Gradiente |i| = √[(∂h/∂x)² + (∂h/∂y)²]', 'SQRT({ga}^2+{gb}^2)', 'm/m', fmt=F4, main=True)
h.out('az', 'Azimut del FLUJO (desde el norte, horario)', 'MOD(DEGREES(ATAN2(-{gb},-{ga})),360)', '°', fmt=F1, main=True,
      note='El flujo va contra el gradiente: q = −K∇h.')
h.out(None, 'Rumbo del flujo',
      'IF({az}<=90,"N "&ROUND({az},1)&"° E",IF({az}<=180,"S "&ROUND(180-{az},1)&"° E",IF({az}<=270,"S "&ROUND({az}-180,1)&"° O","N "&ROUND(360-{az},1)&"° O")))',
      '', fmt=None, main=True, note='O = oeste (en inglés W).')
h.out(None, 'Hacia el', 'CHOOSE(MOD(ROUND({az}/45,0),8)+1,"norte","noreste","este","sureste","sur","suroeste","oeste","noroeste")', '', fmt=None)
h.out(None, 'Dirección en que SUBE la carga (∇h)', 'MOD({az}+180,360)', '°', fmt=F1)
h.chk('Verificación', 'IF({den}=0,"✘ los tres pozos están alineados: no definen un plano","✔ los tres pozos definen el plano de la superficie piezométrica")')

# =========================================================== CAPAS
h = Hoja('Capas', 'Capas: conductividad equivalente y anisotropía',
         'K horizontal (media aritmética), K vertical (media armónica), tensor y refracción.',
         cols={'G': 8, 'H': 11, 'I': 12, 'J': 11, 'K': 12, 'L': 12, 'M': 13, 'N': 14})
SH['Capas'] = h
h.sec('1. Medio estratificado equivalente (ejercicio 3.11)')
r0 = h.r
ws = h.ws
thead(ws, r0, 7, ['Capa', 'Espesor b (m)', 'K (m/s)', 'b usado', 'b·K', 'b/K',
                  '% del flujo horizontal', '% de la resistencia vertical'])
R1, R2 = r0 + 1, r0 + 6
for k, (bb, kk) in enumerate([(20, 1e-6), (20, 1e-7), (20, 1e-8), (None, None), (None, None), (None, None)]):
    rr = r0 + 1 + k
    tlabel(ws, rr, 7, k + 1, bold=True)
    tin(ws, rr, 8, bb)
    tin(ws, rr, 9, kk, fmt=SCI)
    tout(ws, rr, 10, f'=IF(AND(ISNUMBER(H{rr}),ISNUMBER(I{rr})),IF(AND(H{rr}>0,I{rr}>0),H{rr},0),0)', fmt=F1)
    tout(ws, rr, 11, f'=IF(J{rr}>0,J{rr}*I{rr},0)', fmt=SCI)
    tout(ws, rr, 12, f'=IF(J{rr}>0,J{rr}/I{rr},0)', fmt=SCI)
    tout(ws, rr, 13, f'=IF(SUM($K${R1}:$K${R2})>0,K{rr}/SUM($K${R1}:$K${R2}),0)', fmt=PCT)
    tout(ws, rr, 14, f'=IF(SUM($L${R1}:$L${R2})>0,L{rr}/SUM($L${R1}:$L${R2}),0)', fmt=PCT)
J, Kc, Lc = f'$J${R1}:$J${R2}', f'$K${R1}:$K${R2}', f'$L${R1}:$L${R2}'
h.note('Escribe espesor y K de cada capa en la tabla de la derecha (hasta 6). Las filas vacías '
       'se ignoran.')
h.out('sb', 'Espesor total Σb', f'SUM({J})', 'm', fmt=F2)
h.out('Kh', 'K horizontal = Σ(Kᵢbᵢ) / Σbᵢ', f'SUM({Kc})/{{sb}}', 'm/s', fmt=SCI, main=True,
      note='Media aritmética (capas en paralelo). La domina la capa MÁS permeable.')
h.out('Kv', 'K vertical = Σbᵢ / Σ(bᵢ/Kᵢ)', f'{{sb}}/SUM({Lc})', 'm/s', fmt=SCI, main=True,
      note='Media armónica (capas en serie). La domina la capa MENOS permeable.')
h.out(None, 'Anisotropía Kh/Kv', '{Kh}/{Kv}', '—', fmt=F2, main=True)
h.out(None, 'Transmisividad T = Kh·Σb', '{Kh}*{sb}', 'm²/s', fmt=SCI)
h.out(None, 'T en m²/día', '{Kh}*{sb}*86400', 'm²/día', fmt=F2)
h.out(None, 'Capa que domina Kh', f'"capa "&MATCH(MAX({Kc}),{Kc},0)&" ("&ROUND(100*MAX({Kc})/SUM({Kc}),0)&" % del flujo)"', '', fmt=None)
h.out(None, 'Capa que domina Kv', f'"capa "&MATCH(MAX({Lc}),{Lc},0)&" ("&ROUND(100*MAX({Lc})/SUM({Lc}),0)&" % de la resistencia)"', '', fmt=None)
h.chk('Verificación', 'IF({Kv}<={Kh}*1.000001,"✔ Kv ≤ Kh, como debe ser siempre","✘ revisa los datos")')
h.to(r0 + 8)
h.sec('2. Términos cruzados del tensor (ejercicio 3.12)')
h.inp('ix', 'Gradiente aplicado en x (ensayo 1)', 0.1, 'cm/cm')
h.inp('qy', 'Flujo medido en y (ensayo 1)', 0.001, 'cm/s')
h.inp('iy', 'Gradiente aplicado en y (ensayo 2)', 0.01, 'cm/cm')
h.out('kyx', 'K_yx = q_y / (∂h/∂x)', '{qy}/{ix}', 'cm/s', fmt=SCI)
h.out(None, 'q_x = K_xy · ∂h/∂y  (K_xy = K_yx por simetría)', '{kyx}*{iy}', 'cm/s', fmt=SCI, main=True)
h.sec('3. Refracción de las líneas de flujo en un contacto')
h.inp('K1', 'K del medio 1 (de donde viene el flujo)', 1e-6, 'm/s', fmt=SCI)
h.inp('K2', 'K del medio 2', 5e-6, 'm/s', fmt=SCI)
h.inp('th1', 'Ángulo θ₁ respecto a la normal al contacto', 18, '°')
h.out(None, 'θ₂ = atan(tan θ₁ · K₂/K₁)', 'DEGREES(ATAN(TAN(RADIANS({th1}))*{K2}/{K1}))', '°', fmt=F1, main=True,
      note='Al pasar a un medio más permeable la línea de flujo se "tumba" hacia el contacto.')

# =========================================================== ALMACENAMIENTO
h = Hoja('Almacenamiento', 'Almacenamiento, difusividad y correcciones',
         'S = ρg·b(βp + nβw), S = Sy + Ss·b, difusividad y eficiencia barométrica.')
SH['Almacenamiento'] = h
h.sec('1. Almacenamiento elástico a partir de las compresibilidades')
h.inp('rho', 'Densidad del agua ρ', 1000, 'kg/m³')
h.inp('g', 'Gravedad g', 9.81, 'm/s²')
h.inp('b', 'Espesor del acuífero b', 60, 'm')
h.inp('n', 'Porosidad n', 0.3, '—')
h.inp('bw', 'Compresibilidad del agua βw', 4.8e-10, 'm²/N', fmt=SCI)
h.inp('bp', 'Compresibilidad de la matriz βp', 3.657e-10, 'm²/N', fmt=SCI)
h.out('Ss', 'Ss = ρg(βp + nβw)', '{rho}*{g}*({bp}+{n}*{bw})', '1/m', fmt=SCI)
h.out(None, 'S = Ss·b', '{Ss}*{b}', '—', fmt=SCI, main=True)
h.out(None, 'Aporte de la matriz', '{bp}/({bp}+{n}*{bw})', '', fmt=PCT)
h.out(None, 'Aporte del agua', '{n}*{bw}/({bp}+{n}*{bw})', '', fmt=PCT)
h.sec('2. Compresibilidad de la matriz a partir de S (ejercicio 4.2)')
h.inp('S2', 'Almacenamiento S medido', 3e-4, '—', fmt=SCI)
h.out('bp2', 'βp = S/(ρgb) − nβw', '{S2}/({rho}*{g}*{b})-{n}*{bw}', 'm²/N', fmt=SCI, main=True,
      note='Usa ρ, g, b, n y βw de la sección 1.')
h.out('Sinc', 'S si la matriz fuera incompresible = ρgb·nβw', '{rho}*{g}*{b}*{n}*{bw}', '—', fmt=SCI, main=True)
h.out(None, 'Fracción del S real que aporta el agua', '{Sinc}/{S2}', '', fmt=PCT)
h.chk('Verificación', 'IF({bp2}>0,"✔ βp positiva: el dato es físicamente posible","✘ βp negativa: imposible, revisa S o el espesor")')
h.sec('3. Volumen liberado')
h.inp('S3', 'Almacenamiento S', 3e-4, '—', fmt=SCI)
h.inp('A3', 'Área', 1e6, 'm²', fmt=GEN)
h.inp('dh3', 'Descenso de la carga Δh', 1, 'm')
h.out('V3', 'V = S·A·Δh', '{S3}*{A3}*{dh3}', 'm³', fmt=F1, main=True)
h.out(None, 'Lámina de agua equivalente', '{V3}/{A3}*1000', 'mm', fmt=F3)
h.sec('4. Acuífero libre: S = Sy + Ss·b (apuntes, Valle del Cauca)')
h.inp('Sy', 'Rendimiento específico Sy (drenaje)', 0.27, '—')
h.inp('Ss4', 'Almacenamiento específico Ss', 1e-5, '1/m', fmt=SCI)
h.inp('b4', 'Espesor saturado b', 500, 'm')
h.out('Ssb', 'Ss·b (descompresión)', '{Ss4}*{b4}', '—', fmt=F4)
h.out('S4', 'S = Sy + Ss·b', '{Sy}+{Ssb}', '—', fmt=F4, main=True)
h.out(None, 'Aporte del drenaje (Sy)', '{Sy}/{S4}', '', fmt=PCT)
h.out(None, 'Aporte de la descompresión (Ss·b)', '{Ssb}/{S4}', '', fmt=PCT)
h.sec('5. Difusividad hidráulica y longitud de difusión')
h.inp('T5', 'Transmisividad T', 250, 'm²/día')
h.inp('S5', 'Almacenamiento S', 4e-4, '—', fmt=SCI)
h.inp('d5', 'Distancia', 1000, 'm')
h.inp('t5', 'Tiempo', 30, 'días')
h.out('nu', 'Difusividad D = T/S', '{T5}/{S5}', 'm²/día', fmt=GEN, main=True,
      note='Es T/S, no S/T (errata de los apuntes).')
h.out(None, 'Tiempo para que la perturbación llegue a esa distancia = d²/D', '{d5}^2/{nu}', 'días', fmt=F4)
h.out(None, 'Longitud de difusión en ese tiempo = √(D·t)', 'SQRT({nu}*{t5})', 'm', fmt=F1)
h.out(None, 'Radio de influencia R₀ = 1.5·√(T·t/S)', '1.5*SQRT({T5}*{t5}/{S5})', 'm', fmt=F1)
h.sec('6. Corrección barométrica y por marea (acuífero confinado)')
h.inp('BE', 'Eficiencia barométrica BE', 0.45, '—')
h.inp('dP', 'Aumento de la presión atmosférica', 1.0, 'kPa')
h.inp('gw', 'Peso unitario del agua γw', 9.81, 'kN/m³')
h.inp('mar', 'Amplitud de la marea', 1.2, 'm')
h.out(None, 'ΔP en columna de agua = ΔP/γw', '{dP}/{gw}', 'm', fmt=F4)
h.out('dhb', 'Cambio del nivel del pozo = −BE·ΔP/γw', '-{BE}*{dP}/{gw}', 'm', fmt=F4, main=True,
      note='Negativo = baja. Sube la presión atmosférica → baja el nivel del pozo.')
h.out(None, 'en cm', '{dhb}*100', 'cm', fmt=F2)
h.out('TE', 'Eficiencia de marea TE = 1 − BE', '1-{BE}', '—', fmt=F2, main=True)
h.out(None, 'Oscilación del pozo = TE · amplitud de la marea', '{TE}*{mar}', 'm', fmt=F3)
h.inp('hobs', 'Nivel medido en el pozo', 25.300, 'm')
h.inp('Patm', 'Presión atmosférica en la medición', 101.8, 'kPa')
h.inp('Pref', 'Presión atmosférica de referencia', 101.3, 'kPa')
h.out(None, 'Nivel corregido = h + BE·(P − Pref)/γw', '{hobs}+{BE}*({Patm}-{Pref})/{gw}', 'm', fmt=F3, main=True)

# =========================================================== REDES DE FLUJO
h = Hoja('Redes_flujo', 'Redes de flujo',
         'Q = K·H·nf/nd, medio anisótropo y gradiente de salida (tubificación).',
         cols={'G': 20, 'H': 9, 'I': 9, 'J': 10, 'K': 15, 'L': 15, 'M': 13})
SH['Redes_flujo'] = h
h.sec('1. Caudal a partir de la red (ejercicio 4.7)')
h.inp('K', 'Conductividad K', 5e-4, 'm/s', fmt=SCI)
h.inp('H', 'Carga total disponible H', 20, 'm')
h.inp('nf', 'Canales de flujo nf', 5, '—')
h.inp('nd', 'Saltos de potencial nd', 14, '—')
h.inp('B', 'Ancho de la estructura', 1, 'm')
h.out('ff', 'Factor de forma nf/nd', '{nf}/{nd}', '—', fmt=F3)
h.out('Qm', 'Q por metro = K·H·nf/nd', '{K}*{H}*{ff}', 'm³/s por m', fmt=SCI, main=True)
h.out(None, 'Q por metro en m³/día', '{Qm}*86400', 'm³/día por m', fmt=F1)
h.out(None, 'Q total', '{Qm}*{B}', 'm³/s', fmt=SCI)
h.out(None, 'Q total en m³/día', '{Qm}*{B}*86400', 'm³/día', fmt=F1)
h.out('dhs', 'Caída de carga por salto Δh = H/nd', '{H}/{nd}', 'm', fmt=F3)
h.sec('2. Medio anisótropo: sección transformada')
h.inp('Kh', 'K horizontal', 4e-4, 'm/s', fmt=SCI)
h.inp('Kv', 'K vertical', 1e-5, 'm/s', fmt=SCI)
h.out('Keq', 'K equivalente = √(Kh·Kv)', 'SQRT({Kh}*{Kv})', 'm/s', fmt=SCI, main=True,
      note='Media geométrica. No uses Kh.')
h.out(None, 'Factor para contraer x:  x′ = x·√(Kv/Kh)', 'SQRT({Kv}/{Kh})', '—', fmt=F4)
h.out(None, 'Relación de lados de las celdas al destransformar', 'SQRT({Kh}/{Kv})', ': 1', fmt=F2)
h.out(None, 'Q por metro con K equivalente', '{Keq}*{H}*{ff}', 'm³/s por m', fmt=SCI)
h.sec('3. Gradiente de salida y tubificación')
h.inp('a', 'Lado de la última celda, aguas abajo', 5, 'm')
h.inp('gsat', 'Peso unitario saturado del suelo', 19.5, 'kN/m³')
h.inp('gw', 'Peso unitario del agua', 9.81, 'kN/m³')
h.out('ie', 'Gradiente de salida = Δh / a', '{dhs}/{a}', '—', fmt=F3)
h.out('ic', 'Gradiente crítico = (γsat − γw)/γw', '({gsat}-{gw})/{gw}', '—', fmt=F3)
h.out('FSp', 'Factor de seguridad = i_crít / i_salida', '{ic}/{ie}', '—', fmt=F2, main=True)
h.chk('Riesgo de tubificación', 'IF({FSp}>=3,"✔ FS ≥ 3: seguro",IF({FSp}>=1.5,"⚠ FS entre 1.5 y 3: aceptable con cuidado","✘ FS < 1.5: riesgo de tubificación (piping)"))')
r0 = 6
ws = h.ws
tlabel(ws, r0 - 1, 7, 'Comparación de casos (usa K y H de la sección 1)', bold=True)
thead(ws, r0, 7, ['Caso', 'nf', 'nd', 'nf/nd', 'Q (m³/s por m)', 'Q (m³/día por m)', '% del caso 1'])
for k, (nm, nf, nd) in enumerate([('Delantal completo', 5, 14), ('Delantal a la mitad', 5, 10),
                                  ('Sin delantal', 6, 7), ('Tu caso', None, None)]):
    rr = r0 + 1 + k
    tin(ws, rr, 7, nm)
    tin(ws, rr, 8, nf)
    tin(ws, rr, 9, nd)
    tout(ws, rr, 10, f'=IF(AND(ISNUMBER(H{rr}),ISNUMBER(I{rr})),H{rr}/I{rr},"")', fmt=F3)
    tout(ws, rr, 11, f'=IF(ISNUMBER(J{rr}),{h.v["K"]}*{h.v["H"]}*J{rr},"")', fmt=SCI, main=True)
    tout(ws, rr, 12, f'=IF(ISNUMBER(K{rr}),K{rr}*86400,"")', fmt=F1)
    tout(ws, rr, 13, f'=IF(ISNUMBER(K{rr}),K{rr}/$K${r0 + 1},"")', fmt='0%')

# =========================================================== ESFUERZOS
h = Hoja('Esfuerzos', 'Esfuerzo efectivo y estabilidad de excavaciones',
         'σ′ = σT − u, factor de seguridad, profundidad crítica y despresurización.',
         cols={'G': 10, 'H': 13, 'I': 13, 'J': 13, 'K': 12, 'L': 12})
SH['Esfuerzos'] = h
h.sec('1. Datos (unidades consistentes: ft y lb/ft³, o m y kN/m³)')
h.inp('D', 'Espesor del estrato confinante D', 50, 'ft o m')
h.inp('gs', 'Peso unitario saturado γsat', 125, 'lb/ft³ o kN/m³')
h.inp('gw', 'Peso unitario del agua γw', 62.4, 'lb/ft³ o kN/m³', note='62.4 lb/ft³ = 9.81 kN/m³.')
h.inp('art', 'Carga artesiana SOBRE el terreno', 20, 'ft o m', note='Cuánto sube el agua del piezómetro por encima del terreno.')
h.inp('d', 'Profundidad excavada d', 20, 'ft o m')
h.inp('dw', 'Agua dentro de la excavación', 20, 'ft o m', note='0 si está seca; igual a d si está llena hasta la superficie.')
h.inp('FSr', 'Factor de seguridad exigido', 1.3, '—')
h.out('hp', 'Carga de presión en la base hₚ = D + carga artesiana', '{D}+{art}', 'ft o m', fmt=F2,
      note='Error clásico: usar sólo la parte artesiana. Hay que sumar el espesor.')
h.out('u', 'Presión neutra u = γw·hₚ (no cambia al excavar)', '{gw}*{hp}', 'lb/ft² o kPa', fmt=F1, main=True)
h.sec('2. Sin excavar')
h.out('sT0', 'Esfuerzo total σT = γsat·D', '{gs}*{D}', 'lb/ft² o kPa', fmt=F1)
h.out(None, "Esfuerzo efectivo σ′ = σT − u", '{sT0}-{u}', 'lb/ft² o kPa', fmt=F1, main=True)
h.out('FS0', 'Factor de seguridad FS = σT/u', '{sT0}/{u}', '—', fmt=F3)
EST = ('IF({F}>=1.5,"✔ SEGURO (FS ≥ 1.5)",IF({F}>=1.3,"✔ ACEPTABLE (1.3 ≤ FS < 1.5)",'
       'IF({F}>1,"⚠ MARGINAL (1 < FS < 1.3)","✘ FALLA: reventón del fondo (FS ≤ 1)")))')
h.chk('Estado', EST.replace('{F}', '{FS0}'))
h.sec('3. Con la excavación')
h.out('sT', 'Esfuerzo total σT = γsat(D − d) + γw·(agua)', '{gs}*({D}-{d})+{gw}*{dw}', 'lb/ft² o kPa', fmt=F1)
h.out(None, "Esfuerzo efectivo σ′ = σT − u", '{sT}-{u}', 'lb/ft² o kPa', fmt=F1, main=True)
h.out('FS', 'Factor de seguridad FS = σT/u', '{sT}/{u}', '—', fmt=F3, main=True)
h.chk('Estado', EST.replace('{F}', '{FS}'))
h.sec('4. Profundidad crítica (σ′ = 0)')
h.out('dcw', 'Con la excavación llena de agua = (γsat·D − γw·hₚ)/(γsat − γw)', '({gs}*{D}-{gw}*{hp})/({gs}-{gw})', 'ft o m', fmt=F2, main=True)
h.out('dcd', 'En seco = D − γw·hₚ/γsat', '{D}-{gw}*{hp}/{gs}', 'ft o m', fmt=F2, main=True)
h.chk('Lectura', 'IF({dcd}<=0,"✘ el fondo ya es inestable sin excavar en seco","✔ rellenar con agua permite excavar "&ROUND({dcw}/{dcd},2)&" veces más hondo")')
h.sec('5. Despresurización necesaria')
h.out('hpa', 'Carga de presión admisible = σT/(γw·FS exigido)', '{sT}/({gw}*{FSr})', 'ft o m', fmt=F2)
h.out(None, 'Hay que bajar la carga del acuífero', 'MAX(0,{hp}-{hpa})', 'ft o m', fmt=F2, main=True,
      note='Con pozos de alivio, antes de excavar. 0 = no hace falta.')
r0 = 6
ws = h.ws
tlabel(ws, r0 - 1, 7, 'Esfuerzos según la profundidad excavada', bold=True)
thead(ws, r0, 7, ['d', 'σT con agua', 'σT en seco', 'u', 'FS con agua', 'FS en seco'])
for k in range(11):
    rr = r0 + 1 + k
    tout(ws, rr, 7, f'={h.v["D"]}*{k}/10', fmt=F1)
    tout(ws, rr, 8, f'={h.v["gs"]}*({h.v["D"]}-G{rr})+{h.v["gw"]}*G{rr}', fmt=F0)
    tout(ws, rr, 9, f'={h.v["gs"]}*({h.v["D"]}-G{rr})', fmt=F0)
    tout(ws, rr, 10, f'={h.v["u"]}', fmt=F0)
    tout(ws, rr, 11, f'=H{rr}/J{rr}', fmt=F2)
    tout(ws, rr, 12, f'=I{rr}/J{rr}', fmt=F2)
ch = chart('Esfuerzo total frente a la presión neutra', 'profundidad excavada d',
           'esfuerzo', w=19, h=10, ymin=0)
serie(ch, ws, 7, 8, r0 + 1, r0 + 11, 'σT, excavación con agua', 'line', '1F4E79')
serie(ch, ws, 7, 9, r0 + 1, r0 + 11, 'σT, excavación seca', 'line', '2B8A3E')
serie(ch, ws, 7, 10, r0 + 1, r0 + 11, 'u (fija)', 'line', 'B03030', dash='dash')
ws.add_chart(ch, f'G{r0 + 14}')

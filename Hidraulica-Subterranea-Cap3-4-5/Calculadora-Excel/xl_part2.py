"""Hojas de pruebas de bombeo."""
from xl_lib import *
from xl_part1 import SH

# =========================================================== COOPER-JACOB
CJ_T = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 60, 90, 120, 180, 240, 360, 480, 720, 1080, 1440]
CJ_S = [0.005, 0.040, 0.087, 0.181, 0.261, 0.360, 0.486, 0.583, 0.725, 0.830, 0.982, 1.137,
        1.248, 1.406, 1.519, 1.679, 1.792, 1.953, 2.113, 2.228]
R0, R1 = 7, 36                    # filas de datos
h = Hoja('Cooper_Jacob', 'Prueba de bombeo: método de Cooper-Jacob',
         'Pega tus datos t–s en la tabla amarilla. La recta, T, S y las verificaciones salen solas.',
         cols={**{c: 10 for c in 'GHIJKLMNOPQR'}, 'S': 3, 'T': 12, 'U': 12})
SH['Cooper_Jacob'] = h
ws = h.ws
h.sec('1. Datos de la prueba')
h.inp('Q', 'Caudal de bombeo Q', 1500, 'm³/día', note='Si lo tienes en L/s, multiplícalo por 86.4.')
h.inp('r', 'Distancia del piezómetro al pozo r', 50, 'm')
h.inp('b', 'Espesor del acuífero b', 25, 'm', note='Sólo para K = T/b y Ss = S/b.')
h.inp('tc', 'Usar en la recta los puntos con t ≥', 360, 'min',
      note='Los primeros puntos se curvan (u > 0.01). Sube este valor hasta que la validez salga ✔.')
rng = lambda col: f'${col}${R0}:${col}${R1}'
h.sec('2. Ajuste de la recta s = Δs·log₁₀(t) + c  (sólo puntos usados)')
h.out('n', 'Puntos usados', f'SUM({rng("J")})', '', fmt=F0)
h.out('ds', 'Δs = caída de abatimiento por ciclo log', f'SLOPE({rng("L")},{rng("K")})', 'm', fmt=F4, main=True)
h.out('c', 'Ordenada c (abatimiento en t = 1 día)', f'INTERCEPT({rng("L")},{rng("K")})', 'm', fmt=F4)
h.out('R2', 'R² del ajuste', f'RSQ({rng("L")},{rng("K")})', '', fmt='0.00000')
h.out('t0d', 't₀ = 10^(−c/Δs), donde la recta corta s = 0', '10^(-{c}/{ds})', 'días', fmt='0.000000')
h.out('t0m', 't₀ en minutos', '{t0d}*1440', 'min', fmt=F2)
h.sec('3. Resultados')
h.out('T', 'T = 2.303·Q / (4π·Δs)', '2.303*{Q}/(4*PI()*{ds})', 'm²/día', fmt=F1, main=True)
h.out(None, 'T en m²/s', '{T}/86400', 'm²/s', fmt=SCI)
h.out('S', 'S = 2.25·T·t₀ / r²', '2.25*{T}*{t0d}/{r}^2', '—', fmt=SCI, main=True,
      note='t₀ en DÍAS, igual que T. Con t₀ en minutos te equivocas por 1440.')
h.out('Kd', 'K = T/b', '{T}/{b}', 'm/día', fmt=F2)
h.out('Ks', 'K en m/s', '{Kd}/86400', 'm/s', fmt=SCI)
h.out(None, 'Ss = S/b', '{S}/{b}', '1/m', fmt=SCI)
h.sec('4. Verificaciones')
h.out('umax', 'u máximo entre los puntos usados', f'MAX({rng("O")})', '', fmt='0.00000')
h.chk('Validez de Cooper-Jacob (u < 0.01)',
      'IF({n}<2,"✘ hacen falta al menos 2 puntos con t ≥ el corte",IF({umax}<0.01,"✔ VÁLIDO: todos los puntos usados tienen u < 0.01",IF({umax}<0.05,"⚠ ACEPTABLE: u < 0.05 (error < 2 %)","✘ NO VÁLIDO: sube el t de corte o usa la hoja Theis")))')
h.out(None, 't mínimo recomendado (donde u = 0.01)', '{r}^2*{S}/(0.04*{T})*1440', 'min', fmt=F1,
      note='Usa como corte un valor igual o mayor que este.')
h.chk('Calidad del ajuste', 'IF({R2}>=0.995,"✔ R² ≥ 0.995: los puntos están alineados",IF({R2}>=0.98,"⚠ R² entre 0.98 y 0.995: revisa si hay puntos raros","✘ R² < 0.98: hay puntos que no siguen la recta"))')
h.chk('¿S tiene sentido?', 'IF({S}<0.00001,"⚠ S muy bajo: revisa las unidades de t₀",IF({S}<=0.001,"✔ rango típico de acuífero confinado (10⁻⁵ a 10⁻³)",IF({S}<0.05,"⚠ alto para confinado: ¿semiconfinado o libre?","⚠ valor de acuífero libre (Sy): ¿t₀ en minutos en vez de días?")))')
h.out(None, 'Material probable según K', 'IF({Ks}>=0.01,"grava",IF({Ks}>=0.00001,"arena limpia",IF({Ks}>=0.00000001,"arena fina o limo","arcilla")))', '', fmt=None)
h.sec('5. Si lo haces a mano: dos puntos leídos de tu recta')
h.note('Lee dos puntos de la recta que trazaste en papel semilog (no de los datos). Así compruebas '
       'tu lectura gráfica con lo que calcula la hoja.')
h.inp('mt1', 't₁ leído de la recta', 100, 'min')
h.inp('ms1', 's₁ en t₁', 1.17, 'm')
h.inp('mt2', 't₂ leído de la recta', 1000, 'min')
h.inp('ms2', 's₂ en t₂', 2.08, 'm')
h.out('mcy', 'Ciclos entre t₁ y t₂', 'LOG10({mt2}/{mt1})', 'ciclos', fmt=F3)
h.out('mds', 'Δs por ciclo', '({ms2}-{ms1})/{mcy}', 'm', fmt=F3)
h.out('mt0', 't₀ = t₁·10^(−s₁/Δs)', '{mt1}*10^(-{ms1}/{mds})', 'min', fmt=F2)
h.out('mT', 'T', '2.303*{Q}/(4*PI()*{mds})', 'm²/día', fmt=F1, main=True)
h.out(None, 'S', '2.25*{mT}*({mt0}/1440)/{r}^2', '—', fmt=SCI, main=True)
# ---- tabla de datos
tlabel(ws, 5, 7, 'Datos: escribe t y s en las columnas amarillas (hasta 30 filas)', bold=True)
thead(ws, 6, 7, ['t (min)', 's (m)', 't (días)', '¿usar? 1 = sí', 'log₁₀ t (usados)',
                 's (usados)', 'u', '¿u < 0.01?', 'u (usados)', 's de la recta',
                 't usado (gráfica)', 's usado (gráfica)'])
v = h.v
for k in range(R0, R1 + 1):
    i = k - R0
    tin(ws, k, 7, CJ_T[i] if i < len(CJ_T) else None)
    tin(ws, k, 8, CJ_S[i] if i < len(CJ_S) else None, fmt=F3)
    tout(ws, k, 9, f'=IF(ISNUMBER(G{k}),G{k}/1440,"")', fmt='0.00000')
    tout(ws, k, 10, f'=IF(AND(ISNUMBER(G{k}),ISNUMBER(H{k})),IF(G{k}>={v["tc"]},1,0),0)', fmt=F0)
    tout(ws, k, 11, f'=IF(J{k}=1,LOG10(I{k}),"")', fmt=F4)
    tout(ws, k, 12, f'=IF(J{k}=1,H{k},"")', fmt=F3)
    tout(ws, k, 13, f'=IF(ISNUMBER(G{k}),{v["r"]}^2*{v["S"]}/(4*{v["T"]}*I{k}),"")', fmt='0.0000')
    tout(ws, k, 14, f'=IF(ISNUMBER(M{k}),IF(M{k}<0.01,"sí","no"),"")')
    tout(ws, k, 15, f'=IF(J{k}=1,M{k},"")', fmt='0.0000')
    tout(ws, k, 16, f'=IF(ISNUMBER(G{k}),{v["ds"]}*LOG10(I{k})+{v["c"]},"")', fmt=F3)
    tout(ws, k, 17, f'=IF(J{k}=1,G{k},NA())')
    tout(ws, k, 18, f'=IF(J{k}=1,H{k},NA())', fmt=F3)
ws.conditional_formatting.add(f'N{R0}:N{R1}', FormulaRule(formula=[f'N{R0}="no"'], fill=FILL_BAD))
ws.conditional_formatting.add(f'N{R0}:N{R1}', FormulaRule(formula=[f'N{R0}="sí"'], fill=FILL_OK))
thead(ws, 6, 20, ['t recta (min)', 's recta (m)'])
tout(ws, 7, 20, f'={v["t0m"]}', fmt=F2)
tout(ws, 8, 20, f'=MAX({rng("G")})*1.5', fmt=F1)
for k in (7, 8):
    tout(ws, k, 21, f'={v["ds"]}*LOG10(T{k}/1440)+{v["c"]}', fmt=F3)
ch = chart('Cooper-Jacob: abatimiento frente a log t', 'tiempo t (min), escala logarítmica',
           'abatimiento s (m)', logx=True, w=24, h=12, ymin=0)
serie(ch, ws, 7, 8, R0, R1, 'datos medidos', 'pts', '1F4E79', hollow=True)
serie(ch, ws, 17, 18, R0, R1, 'puntos usados en la recta', 'pts', '1F4E79')
serie(ch, ws, 20, 21, 7, 8, 'recta de Cooper-Jacob', 'line', 'B03030')
ws.add_chart(ch, 'G38')
CJ = h

# =========================================================== THEIS
h = Hoja('Theis', 'Prueba de bombeo: método de Theis',
         'Punto de coincidencia de la curva patrón y ajuste interactivo de T y S.',
         cols={**{c: 10 for c in 'GHIJKLM'}, 'N': 3, 'O': 9, 'P': 6, 'Q': 10, 'R': 10, 'S': 10, 'T': 10})
SH['Theis'] = h
ws = h.ws
h.sec('1. T y S a partir del punto de coincidencia')
h.note('Superpón la curva patrón W(u)–1/u sobre los datos s–t (o s–t/r²) en papel log-log, elige '
       'un punto de coincidencia y lee sus cuatro coordenadas. Unidades consistentes.')
h.inp('Qa', 'Caudal Q', 96250, 'ft³/día o m³/día', fmt=F0, note='Apuntes, página 8: 500 gal/min = 96 250 ft³/día.')
h.inp('Wa', 'W(u) del punto de coincidencia', 1)
h.inp('ua', 'u del punto de coincidencia', 0.1)
h.inp('sa', 's del punto de coincidencia', 0.56, 'ft o m')
h.inp('r2t', 'r²/t del punto de coincidencia', 2.8e7, 'ft²/día o m²/día', fmt=SCI,
      note='Si leíste t con un solo piezómetro, r²/t = r² dividido entre ese t (en días).')
h.out('Ta', 'T = Q·W(u) / (4π·s)', '{Qa}*{Wa}/(4*PI()*{sa})', 'ft²/día o m²/día', fmt=F0, main=True)
h.out(None, 'S = 4·T·u / (r²/t)', '4*{Ta}*{ua}/{r2t}', '—', fmt=SCI, main=True)
h.sec('2. Ajuste interactivo: cambia T y S hasta que la curva pase por los puntos')
h.note('Por defecto toma los datos y el resultado de la hoja Cooper_Jacob. Puedes escribir encima '
       'tus propios valores. Baja el RMSE probando T y S; si tienes Solver, minimiza la celda RMSE.')
h.inp('Q', 'Caudal Q', f'={CJ.ext("Q")}', 'm³/día')
h.inp('r', 'Distancia r', f'={CJ.ext("r")}', 'm')
h.inp('T', 'T de prueba', f'=ROUND({CJ.ext("T")},0)', 'm²/día', fmt=F1)
h.inp('S', 'S de prueba', f'={CJ.ext("S")}', '—', fmt=SCI)
rng = lambda col: f'${col}${R0}:${col}${R1}'
h.out('rmse', 'RMSE entre datos y curva', f'SQRT(SUM({rng("M")})/COUNT({rng("M")}))', 'm', fmt=F4, main=True)
h.out(None, 'Puntos comparados', f'COUNT({rng("M")})', '', fmt=F0)
h.chk('Ajuste', 'IF({rmse}<0.02,"✔ la curva pasa por los puntos (RMSE < 2 cm)",IF({rmse}<0.08,"⚠ ajuste regular: afina T y S","✘ la curva no coincide: cambia T y S"))')
h.out('tmn', 't mínimo de la curva', f'MIN({rng("N")})/2', 'min', fmt=F2)
h.out('tmx', 't máximo de la curva', f'MAX({rng("N")})*2', 'min', fmt=F1)
h.note('Lectura física: si la curva queda POR ENCIMA de los puntos, sube T; si los puntos tardíos '
       'tienen la forma bien pero la curva está corrida en el tiempo, cambia S.')
tlabel(ws, 5, 7, 'Datos (por defecto, los de Cooper_Jacob) y curva de Theis', bold=True)
thead(ws, 6, 7, ['t (min)', 's (m)', 't (días)', 'u', 'W(u)', 's Theis (m)', 'error²'])
thead(ws, 6, 15, ['k', 't (min)', 'u', 'W(u)', 's Theis (m)'])
ws.cell(row=6, column=14, value='').fill = PatternFill()
for k in range(R0, R1 + 1):
    tin(ws, k, 7, f"=IF(ISNUMBER('Cooper_Jacob'!G{k}),'Cooper_Jacob'!G{k},NA())")
    tin(ws, k, 8, f"=IF(ISNUMBER('Cooper_Jacob'!H{k}),'Cooper_Jacob'!H{k},NA())", fmt=F3)
    tout(ws, k, 9, f'=IF(ISNUMBER(G{k}),G{k}/1440,NA())', fmt='0.00000')
    tout(ws, k, 10, f'=IF(ISNUMBER(I{k}),{h.v["r"]}^2*{h.v["S"]}/(4*{h.v["T"]}*I{k}),NA())', fmt='0.00000')
    tout(ws, k, 11, f'=IF(ISNUMBER(J{k}),{W(f"J{k}")},NA())', fmt=F4)
    tout(ws, k, 12, f'=IF(ISNUMBER(K{k}),{h.v["Q"]}/(4*PI()*{h.v["T"]})*K{k},NA())', fmt=F3)
    tout(ws, k, 13, f'=IF(AND(ISNUMBER(H{k}),ISNUMBER(L{k})),(H{k}-L{k})^2,"")', fmt='0.000000')
    c = ws.cell(row=k, column=14, value=f'=IF(ISNUMBER(G{k}),G{k},"")')
    c.font = Font(color='FFFFFF', size=8)
NC = 41
for k in range(NC):
    rr = R0 + k
    tlabel(ws, rr, 15, k)
    tout(ws, rr, 16, f'={h.v["tmn"]}*({h.v["tmx"]}/{h.v["tmn"]})^(O{rr}/{NC - 1})', fmt=F2)
    tout(ws, rr, 17, f'={h.v["r"]}^2*{h.v["S"]}/(4*{h.v["T"]}*P{rr}/1440)', fmt='0.00000')
    tout(ws, rr, 18, f'={W(f"Q{rr}")}', fmt=F4)
    tout(ws, rr, 19, f'={h.v["Q"]}/(4*PI()*{h.v["T"]})*R{rr}', fmt=F4)
ch = chart('Theis: datos y curva en papel log-log', 'tiempo t (min)', 'abatimiento s (m)',
           logx=True, logy=True, w=24, h=12)
serie(ch, ws, 7, 8, R0, R1, 'datos medidos', 'pts', '1F4E79', hollow=True)
serie(ch, ws, 16, 19, R0, R0 + NC - 1, 'curva de Theis con T y S de prueba', 'line', 'B03030')
ws.add_chart(ch, 'G50')
TH = h

# =========================================================== DISTANCIA-ABATIMIENTO
DR = [10, 30, 50, 100, 200, 300]
DS = [3.508, 2.634, 2.228, 1.679, 1.137, 0.830]
D0, D1 = 7, 21
h = Hoja('Dist_abatimiento', 'Prueba de bombeo: método distancia–abatimiento',
         'Varios piezómetros leídos al MISMO tiempo. Ojo: el denominador es 2π, no 4π.',
         cols={**{c: 10 for c in 'GHIJKLMNOPQ'}, 'R': 3, 'S': 11, 'T': 11})
SH['Dist_abatimiento'] = h
ws = h.ws
rng = lambda col: f'${col}${D0}:${col}${D1}'
h.sec('1. Datos')
h.inp('Q', 'Caudal de bombeo Q', 1500, 'm³/día')
h.inp('t', 'Tiempo de la lectura', 1, 'días')
h.inp('rc', 'Usar piezómetros con r ≤', 100, 'm',
      note='Los piezómetros lejanos tienen u > 0.01. Baja este valor hasta que la validez salga ✔.')
h.sec('2. Ajuste de la recta s = m·log₁₀(r) + c')
h.out('n', 'Piezómetros usados', f'SUM({rng("I")})', '', fmt=F0)
h.out('m', 'Pendiente m (negativa)', f'SLOPE({rng("K")},{rng("J")})', 'm', fmt=F4)
h.out('c', 'Ordenada c', f'INTERCEPT({rng("K")},{rng("J")})', 'm', fmt=F4)
h.out('R2', 'R² del ajuste', f'RSQ({rng("K")},{rng("J")})', '', fmt='0.00000')
h.out('dsr', 'Δs_r = −m, caída por ciclo de distancia', '-{m}', 'm', fmt=F4, main=True)
h.out('r0', 'r₀ = 10^(−c/m), donde la recta corta s = 0', '10^(-{c}/{m})', 'm', fmt=F1, main=True)
h.sec('3. Resultados')
h.out('T', 'T = 2.303·Q / (2π·Δs_r)', '2.303*{Q}/(2*PI()*{dsr})', 'm²/día', fmt=F1, main=True)
h.out('S', 'S = 2.25·T·t / r₀²', '2.25*{T}*{t}/{r0}^2', '—', fmt=SCI, main=True)
h.out('umax', 'u máximo entre los usados', f'MAX({rng("N")})', '', fmt='0.00000')
h.chk('Validez (u < 0.01)', 'IF({n}<2,"✘ hacen falta al menos 2 piezómetros",IF({umax}<0.01,"✔ VÁLIDO: todos los usados tienen u < 0.01",IF({umax}<0.05,"⚠ ACEPTABLE: u < 0.05","✘ NO VÁLIDO: baja el r de corte")))')
h.out(None, 'r máximo recomendado (donde u = 0.01)', 'SQRT(0.04*{T}*{t}/{S})', 'm', fmt=F1)
tlabel(ws, 5, 7, 'Datos: r y s de cada piezómetro (hasta 15)', bold=True)
thead(ws, 6, 7, ['r (m)', 's (m)', '¿usar?', 'log₁₀ r (usados)', 's (usados)', 'u',
                 '¿u < 0.01?', 'u (usados)', 's de la recta', 'r usado (gráfica)', 's usado (gráfica)'])
v = h.v
for k in range(D0, D1 + 1):
    i = k - D0
    tin(ws, k, 7, DR[i] if i < len(DR) else None)
    tin(ws, k, 8, DS[i] if i < len(DS) else None, fmt=F3)
    tout(ws, k, 9, f'=IF(AND(ISNUMBER(G{k}),ISNUMBER(H{k})),IF(G{k}<={v["rc"]},1,0),0)', fmt=F0)
    tout(ws, k, 10, f'=IF(I{k}=1,LOG10(G{k}),"")', fmt=F4)
    tout(ws, k, 11, f'=IF(I{k}=1,H{k},"")', fmt=F3)
    tout(ws, k, 12, f'=IF(ISNUMBER(G{k}),G{k}^2*{v["S"]}/(4*{v["T"]}*{v["t"]}),"")', fmt='0.00000')
    tout(ws, k, 13, f'=IF(ISNUMBER(L{k}),IF(L{k}<0.01,"sí","no"),"")')
    tout(ws, k, 14, f'=IF(I{k}=1,L{k},"")', fmt='0.00000')
    tout(ws, k, 15, f'=IF(ISNUMBER(G{k}),{v["m"]}*LOG10(G{k})+{v["c"]},"")', fmt=F3)
    tout(ws, k, 16, f'=IF(I{k}=1,G{k},NA())')
    tout(ws, k, 17, f'=IF(I{k}=1,H{k},NA())', fmt=F3)
ws.conditional_formatting.add(f'M{D0}:M{D1}', FormulaRule(formula=[f'M{D0}="no"'], fill=FILL_BAD))
ws.conditional_formatting.add(f'M{D0}:M{D1}', FormulaRule(formula=[f'M{D0}="sí"'], fill=FILL_OK))
thead(ws, 6, 19, ['r recta (m)', 's recta (m)'])
tout(ws, 7, 19, f'=MIN({rng("G")})/2', fmt=F2)
tout(ws, 8, 19, f'={v["r0"]}', fmt=F1)
for k in (7, 8):
    tout(ws, k, 20, f'={v["m"]}*LOG10(S{k})+{v["c"]}', fmt=F3)
ch = chart('Distancia–abatimiento', 'distancia r (m), escala logarítmica', 'abatimiento s (m)',
           logx=True, w=22, h=11, ymin=0)
serie(ch, ws, 7, 8, D0, D1, 'piezómetros', 'pts', '1F4E79', hollow=True)
serie(ch, ws, 16, 17, D0, D1, 'usados en la recta', 'pts', '1F4E79')
serie(ch, ws, 19, 20, 7, 8, 'recta', 'line', 'B03030')
ws.add_chart(ch, 'G24')

# =========================================================== RECUPERACIÓN
RT = [5, 10, 20, 30, 60, 120, 240, 480]
RS = [2.255, 1.980, 1.707, 1.549, 1.281, 1.021, 0.774, 0.552]
E0, E1 = 7, 26
h = Hoja('Recuperacion', 'Prueba de recuperación de Theis',
         'Se mide la subida del nivel después de apagar la bomba. Da T, pero NO da S.',
         cols={**{c: 10 for c in 'GHIJKLMNOP'}, 'Q': 3, 'R': 11, 'S': 11})
SH['Recuperacion'] = h
ws = h.ws
rng = lambda col: f'${col}${E0}:${col}${E1}'
h.sec('1. Datos')
h.inp('Q', 'Caudal con que se bombeó Q', 1500, 'm³/día')
h.inp('tp', 'Tiempo que estuvo bombeando tp', 1440, 'min')
h.inp('rc', "Usar puntos con t/t′ ≤", 100000, '—',
      note='En pozos de observación los primeros puntos (t/t′ grande) pueden desviarse.')
h.sec("2. Ajuste de la recta s′ = Δs′·log₁₀(t/t′) + c")
h.out('n', 'Puntos usados', f'SUM({rng("K")})', '', fmt=F0)
h.out('ds', "Δs′ = caída por ciclo de t/t′", f'SLOPE({rng("M")},{rng("L")})', 'm', fmt=F4, main=True)
h.out('c', 'Ordenada c (debería ser casi 0)', f'INTERCEPT({rng("M")},{rng("L")})', 'm', fmt=F4)
h.out('R2', 'R² del ajuste', f'RSQ({rng("M")},{rng("L")})', '', fmt='0.00000')
h.out('T', "T = 2.303·Q / (4π·Δs′)", '2.303*{Q}/(4*PI()*{ds})', 'm²/día', fmt=F1, main=True)
h.chk('¿Pasa por el origen?', 'IF(ABS({c})<0.1*{ds},"✔ la recta pasa casi por el origen, como debe ser","⚠ la recta no pasa por el origen: revisa tp o puntos tempranos")')
h.note('La recuperación NO permite calcular S: la recta pasa obligatoriamente por el origen '
       '(s′ = 0 cuando t/t′ = 1) y no hay ningún corte del cual sacar S.')
tlabel(ws, 5, 7, "Datos: t′ (desde que se apagó) y s′ (abatimiento residual)", bold=True)
thead(ws, 6, 7, ["t′ (min)", "s′ (m)", 't = tp + t′', "t/t′", '¿usar?', "log₁₀(t/t′)",
                 "s′ (usados)", 's′ de la recta', "t/t′ (gráfica)", "s′ (gráfica)"])
v = h.v
for k in range(E0, E1 + 1):
    i = k - E0
    tin(ws, k, 7, RT[i] if i < len(RT) else None)
    tin(ws, k, 8, RS[i] if i < len(RS) else None, fmt=F3)
    tout(ws, k, 9, f'=IF(ISNUMBER(G{k}),{v["tp"]}+G{k},"")', fmt=F0)
    tout(ws, k, 10, f'=IF(ISNUMBER(G{k}),I{k}/G{k},"")', fmt=F2)
    tout(ws, k, 11, f'=IF(AND(ISNUMBER(J{k}),ISNUMBER(H{k})),IF(J{k}<={v["rc"]},1,0),0)', fmt=F0)
    tout(ws, k, 12, f'=IF(K{k}=1,LOG10(J{k}),"")', fmt=F4)
    tout(ws, k, 13, f'=IF(K{k}=1,H{k},"")', fmt=F3)
    tout(ws, k, 14, f'=IF(ISNUMBER(J{k}),{v["ds"]}*LOG10(J{k})+{v["c"]},"")', fmt=F3)
    tout(ws, k, 15, f'=IF(K{k}=1,J{k},NA())', fmt=F2)
    tout(ws, k, 16, f'=IF(K{k}=1,H{k},NA())', fmt=F3)
thead(ws, 6, 18, ["t/t′ recta", "s′ recta"])
tout(ws, 7, 18, '=1', fmt=F0)
tout(ws, 8, 18, f'=MAX({rng("J")})*1.5', fmt=F1)
for k in (7, 8):
    tout(ws, k, 19, f'={v["ds"]}*LOG10(R{k})+{v["c"]}', fmt=F3)
ch = chart('Recuperación de Theis', "t/t′, escala logarítmica", "abatimiento residual s′ (m)",
           logx=True, w=22, h=11, ymin=0, xmin=1)
serie(ch, ws, 15, 16, E0, E1, 'datos', 'pts', '1F4E79')
serie(ch, ws, 18, 19, 7, 8, 'recta', 'line', 'B03030')
ws.add_chart(ch, 'G29')

# =========================================================== THIEM / DUPUIT
h = Hoja('Thiem_Dupuit', 'Régimen permanente: Thiem (confinado) y Dupuit (libre)',
         'Cuando el abatimiento ya se estabilizó. No se puede obtener S.')
SH['Thiem_Dupuit'] = h
h.sec('1. Acuífero confinado: Thiem')
h.inp('Q', 'Caudal Q', 788, 'm³/día')
h.inp('r1', 'Piezómetro cercano r₁', 0.8, 'm')
h.inp('s1', 'Abatimiento en r₁', 2.236, 'm')
h.inp('r2', 'Piezómetro lejano r₂', 30, 'm')
h.inp('s2', 'Abatimiento en r₂', 1.088, 'm')
h.inp('b', 'Espesor b', 30, 'm')
h.out('T', 'T = Q·ln(r₂/r₁) / [2π(s₁ − s₂)]', '{Q}*LN({r2}/{r1})/(2*PI()*({s1}-{s2}))', 'm²/día', fmt=F1, main=True)
h.out(None, 'Misma fórmula con log₁₀: T/Q = 2.303·log₁₀(r₂/r₁) / [2π(s₁ − s₂)]', '2.303*LOG10({r2}/{r1})/(2*PI()*({s1}-{s2}))', 'por unidad de Q', fmt=F4,
      note='Apuntes, página 8: con estos datos da 0.503·Q.')
h.out(None, 'K = T/b', '{T}/{b}', 'm/día', fmt=F2)
h.chk('Verificación', 'IF(AND({r2}>{r1},{s1}>{s2}),"✔ datos coherentes: el piezómetro más cercano tiene más abatimiento","✘ revisa: r₂ debe ser mayor que r₁ y s₁ mayor que s₂")')
h.sec('2. Acuífero libre: Dupuit (con h², medido desde la base)')
h.inp('Ql', 'Caudal Q', 1500, 'm³/día')
h.inp('H', 'Espesor saturado inicial H', 30, 'm')
h.inp('ra', 'Piezómetro cercano r₁', 20, 'm')
h.inp('ha', 'Espesor saturado h₁ en r₁', 27.0, 'm', note='Si te dan abatimiento: h = H − s (sección 3).')
h.inp('rb', 'Piezómetro lejano r₂', 200, 'm')
h.inp('hb', 'Espesor saturado h₂ en r₂', 29.2, 'm')
h.out('Kl', 'K = Q·ln(r₂/r₁) / [π(h₂² − h₁²)]', '{Ql}*LN({rb}/{ra})/(PI()*({hb}^2-{ha}^2))', 'm/día', fmt=F2, main=True)
h.out(None, 'K en m/s', '{Kl}/86400', 'm/s', fmt=SCI)
h.out(None, 'T aproximada = K·(h₁ + h₂)/2', '{Kl}*({ha}+{hb})/2', 'm²/día', fmt=F1)
h.chk('Verificación', 'IF(AND({rb}>{ra},{hb}>{ha},{hb}<={H}),"✔ datos coherentes","✘ revisa: h crece con r y no puede superar H")')
h.sec('3. Pasar de abatimiento a espesor saturado')
h.inp('H3', 'Espesor saturado inicial H', 30, 'm')
h.inp('s3', 'Abatimiento s', 3, 'm')
h.out(None, 'h = H − s', '{H3}-{s3}', 'm', fmt=F2, main=True)
h.sec('4. Predecir el abatimiento con Thiem')
h.inp('T4', 'Transmisividad T', 300, 'm²/día')
h.inp('Q4', 'Caudal Q', 1500, 'm³/día')
h.inp('R4', 'Radio de influencia R', 4500, 'm')
h.inp('r4', 'Distancia r', 50, 'm')
h.out(None, 's = Q·ln(R/r) / (2πT)', '{Q4}*LN({R4}/{r4})/(2*PI()*{T4})', 'm', fmt=F3, main=True)

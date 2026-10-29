"""Transforma los dos .md: inserta las 26 figuras, quita los diagramas ASCII,
actualiza los resultados numericos de 4.7 y convierte a .docx con ecuaciones
nativas de Word (OMML) mediante pandoc."""
import os, re, shutil, subprocess

SB = '/projects/sandbox'
BD = f'{SB}/.build'
SRC = f'{BD}/src'
shutil.rmtree(SRC, ignore_errors=True)
os.makedirs(SRC, exist_ok=True)
shutil.copytree(f'{BD}/fig', f'{SRC}/fig')

W = '15.8cm'

# contador global de figuras por documento
_n = {'v': 0}


def figmd(name, caption, w=W):
    _n['v'] += 1
    return f'\n![**Figura {_n["v"]}.** {caption}](fig/{name}.png){{width={w}}}\n'


# ============================================================ SOLUCIONARIO
SOL_BLOCKS = {           # bloque ASCII -> figura (None = borrar)
    1: ('fig_3_17_sistema',
        'Problema 3.17 — balance de masa en los dos acuíferos acoplados por fuga '
        'y forma de las superficies piezométricas del inciso (d).'),
    2: ('fig_4_08_redes',
        'Problema 4.8 — redes de flujo de los incisos (a) y (b), obtenidas '
        'resolviendo $\\nabla^2h=0$ por diferencias finitas. En azul las '
        'equipotenciales; en rojo las líneas de flujo que delimitan tubos de '
        'caudal igual.'),
    3: None,
    4: None,
    5: ('fig_4_10_transformada',
        'Problema 4.10 — método de la sección transformada: la red se dibuja con '
        'celdas cuadradas en la sección contraída y al destransformar quedan '
        'rectángulos de relación 2.24:1.'),
    6: ('fig_5_02_redes',
        'Problema 5.2(a) — patrón de flujo de la figura 5.4 con los laterales sin '
        'flujo (arriba) y con la frontera izquierda convertida en frontera de '
        'flujo (abajo).'),
}

SOL_INSERTS = [
    ('## 3.6 Problema de los tres puntos', 'fig_3_06_tres_puntos',
     'Problema 3.6 — solución gráfica del problema de los tres puntos '
     '(izquierda) y descomposición del vector gradiente (derecha). El flujo es '
     'opuesto a $\\nabla h$.'),
    ('## 3.7 Piezómetros A, B, C, D', 'fig_3_07_piezometros',
     'Problema 3.7 — los cuatro piezómetros con su carga total $h$, su carga de '
     'presión $h_p$ y su carga de elevación $z$.'),
    ('## 3.9 Condiciones para $q_x = (k/\\mu)(\\partial P/\\partial x)$',
     'fig_3_09_darcy_presion',
     'Problema 3.9 — las dos presiones deben medirse a la misma elevación para '
     'que el término gravitatorio desaparezca.'),
    ('## 3.11 Conductividad equivalente de tres capas', 'fig_3_11_capas',
     'Problema 3.11 — flujo horizontal (capas en paralelo, media aritmética) y '
     'flujo vertical (capas en serie, media armónica).'),
    ('## 3.13 Conductividades relativas en la figura 3.E4', 'fig_3_13_redflujo',
     'Problema 3.13 — esquema de la figura 3.E4 con las distancias $L_i$ entre '
     'equipotenciales y los espesores $b_i$ que hay que escalar con regla.'),
    ('## 3.14 Espaciamiento de equipotenciales con recarga y descarga',
     'fig_3_14_recarga',
     'Problema 3.14 — con recarga uniforme el caudal crece en la dirección del '
     'flujo y las equipotenciales se juntan; con descarga uniforme ocurre lo '
     'contrario.'),
    ('## 3.15 Dirección y magnitud del flujo vertical a través de la arcilla',
     'fig_3_15_arcilla',
     'Problema 3.15 — fuga descendente a través del acuitardo. La velocidad es '
     'el doble en la región de $h_4$ porque $\\Delta h$ es el doble.'),
    ('## 3.16 Descarga específica a través de la capa confinante',
     'fig_3_16_confinante',
     'Problema 3.16 — las dos cargas (100 m y 95 m) y el espesor de la capa '
     'confinante que las separa.'),
    ('## 4.4 Esfuerzos en una excavación en arcilla sobre un acuífero artesiano',
     'fig_4_04_esfuerzos',
     'Problema 4.4 — los tres estados de esfuerzo de los incisos (a), (b) y (c), '
     'y la curva que define la profundidad crítica del inciso (d).'),
    ('## 4.5 Transmisividad en el centro de bombeo B (figura 4.10)',
     'fig_4_05_transmisividad',
     'Problema 4.5 — tubos de flujo que convergen en el centro de bombeo B y '
     'sensibilidad de $T$ al número de tubos contados.'),
    ('## 4.6 Clasificación de las fronteras (figura del problema 6)',
     'fig_4_06_presa',
     'Problema 4.6 — red de flujo bajo la presa calculada por diferencias '
     'finitas, con las fronteras A–G clasificadas.'),
    ('## 4.7 Caudal de filtración con y sin delantal', 'fig_4_07_comparacion',
     'Problema 4.7 — las tres redes de flujo y el caudal de filtración '
     'resultante. Acortar el delantal a la mitad aumenta la filtración un 39 % y '
     'eliminarlo la aumenta un 140 %.'),
    ('## 4.9 Red de flujo con nivel freático inclinado', 'fig_4_09_freatico',
     'Problema 4.9 — red de flujo con nivel freático inclinado. Las '
     'equipotenciales cortan el nivel freático en el punto donde $h=z$, no a 90°.'),
    ('## 4.10 La misma red en medio anisótropo ($K_h = 5K_v$)',
     'fig_4_10_anisotropo',
     'Problema 4.10 — la misma sección resuelta como medio isótropo (arriba) y '
     'como medio anisótropo con $K_h=5K_v$ (abajo). El flujo se aplana y los '
     'sistemas se vuelven más someros.'),
    ('## 5.1 Condiciones de borde de las figuras 5.5 y 5.8',
     'fig_5_01_fronteras',
     'Problema 5.1 — condiciones de borde del modelo homogéneo (figura 5.5) y '
     'del modelo estratificado (figura 5.8), que añade la continuidad del '
     'potencial y del flujo normal en las interfaces.'),
    ('## 5.2 Construcción de redes de flujo (figuras 5.4 y 5.27)',
     'fig_5_02_pradera',
     'Problema 5.2(b) — el perfil de pradera de la figura 5.27 con $K_2\\gg K_1$ '
     '(arriba) y con $K_1=K_2$ (abajo): al desaparecer el conducto profundo '
     'dominan los sistemas locales.'),
    ('## 5.3 El canal a nivel del mar', 'fig_5_03_canal',
     'Problema 5.3 — geometría del canal a nivel del mar y descenso progresivo '
     'del nivel freático a los 10, 40 y 100 años.'),
    ('## 5.4 Estabilidad de excavaciones — procedimiento del caso histórico',
     'fig_5_04_excavacion',
     'Problema 5.4 — mecanismo de falla del fondo de la excavación y factor de '
     'seguridad en función de la profundidad excavada, con y sin agua.'),
    ('## 5.5 Caudal máximo de bombeo sin ascenso de la interfaz (upconing)',
     'fig_5_06_upconing',
     'Problema 5.5 — ascenso del cono salino bajo el pozo y dependencia '
     'cuadrática de $Q_{max}$ con la distancia $d$ a la interfaz.'),
    ('## 5.6 Posición del pie de la cuña de agua salada', 'fig_5_06_cuna',
     'Problema 5.6 — posición de la interfaz según la solución de Glover para '
     'los dos caudales, y relación $x_{toe}\\propto 1/q\'$.'),
]

# figura adicional que va dentro de 5.3 (perfiles y caudal)
SOL_EXTRA = [
    ('### (b) Caudal de entrada al canal $q\'$', 'fig_5_03_perfiles',
     'Problema 5.3 — perfiles del nivel freático a los 10, 20, 40 y 100 años '
     '(arriba) y decaimiento del caudal hacia el canal, proporcional a '
     '$t^{-1/2}$ (abajo).'),
]

# ============================================================ GUIA
GUIA_BLOCKS = {
    1: ('fig_3_09_darcy_presion',
        'Problema 3.9 — las presiones se miden a la misma cota, de modo que el '
        'término gravitatorio de la ley de Darcy desaparece.'),
    2: ('fig_3_14_recarga',
        'Problema 3.14 — el espaciamiento de las equipotenciales delata recarga '
        '(se juntan) o descarga (se separan) en la dirección del flujo.'),
    3: None,
    4: ('fig_3_16_confinante',
        'Problema 3.16 — cómo leer las dos cargas y el espesor de la capa '
        'confinante en la figura del libro.'),
    5: ('fig_3_17_sistema',
        'Problema 3.17 — geometría del bloque, balance de masa y superficies '
        'piezométricas resultantes.'),
    6: None,
    7: ('fig_4_04_esfuerzos',
        'Problema 4.4 — los tres estados de esfuerzo y la profundidad crítica de '
        'la zanja.'),
    8: ('fig_4_06_presa',
        'Problema 4.6 — clasificación de las cinco fronteras sobre la red de '
        'flujo calculada.'),
    9: None,
    10: ('fig_4_08_redes',
         'Problema 4.8 — redes de flujo de los incisos (a) y (b). El inciso (a) '
         'produce un flujo asimétrico con una zona muerta; el (b), dos celdas '
         'espejo separadas por una divisoria de flujo.'),
    11: None,
    12: ('fig_4_09_freatico',
         'Problema 4.9 — red de flujo con nivel freático inclinado, con las '
         'zonas de recarga (derecha, alta) y de descarga (izquierda, baja).'),
    13: ('fig_4_10_transformada',
         'Problema 4.10 — sección transformada (celdas cuadradas) y sección real '
         '(rectángulos de relación 2.24:1).'),
    14: ('fig_5_06_upconing',
         'Problema 5.5 — ascenso de la interfaz salina bajo el pozo y caudal '
         'máximo admisible.'),
    15: ('fig_5_06_cuna',
         'Problema 5.6 — solución de Glover: posición de la interfaz y del pie '
         'de la cuña salina.'),
}

GUIA_INSERTS = [
    ('## 3.6 — El problema de los tres puntos', 'fig_3_06_tres_puntos',
     'Problema 3.6 — método gráfico (izquierda) y descomposición del gradiente '
     '(derecha). Los dos métodos dan $i=0.141$ m/m y flujo hacia el S 45° W.'),
    ('## 3.7 — Tabla de piezómetros', 'fig_3_07_piezometros',
     'Problema 3.7 — descomposición $h=z+h_p$ en los cuatro piezómetros. '
     'Observa cómo $h_p$ decrece hacia D: es una zona de descarga.'),
    ('## 3.11 — Capas: conductividad equivalente', 'fig_3_11_capas',
     'Problema 3.11 — la analogía con circuitos: en paralelo para el flujo '
     'horizontal, en serie para el vertical.'),
    ('## 3.13 — Leer conductividades relativas en una red de flujo',
     'fig_3_13_redflujo',
     'Problema 3.13 — qué hay que medir con regla sobre la figura 3.E4: la '
     'separación $L_i$ entre equipotenciales y el espesor medio $b_i$.'),
    ('## 3.15 — Fuga vertical a través de una arcilla', 'fig_3_15_arcilla',
     'Problema 3.15 — el flujo vertical lo controla la diferencia de carga entre '
     'acuíferos en el mismo punto, no las cargas absolutas.'),
    ('## 4.5 — Transmisividad a partir de una red de flujo',
     'fig_4_05_transmisividad',
     'Problema 4.5 — conteo de tubos de flujo convergentes y sensibilidad del '
     'resultado al conteo.'),
    ('## 4.7 — Caudal de filtración y el efecto del delantal',
     'fig_4_07_comparacion',
     'Problema 4.7 — efecto de acortar el delantal sobre la red de flujo y sobre '
     'el caudal de filtración.'),
    ('## 4.10 — La misma red en medio anisótropo', 'fig_4_10_anisotropo',
     'Problema 4.10 — la red isótropa y la anisótropa en la misma sección.'),
    ('## 5.1 — Condiciones de borde de los modelos de cuenca',
     'fig_5_01_fronteras',
     'Problema 5.1 — condiciones de borde del modelo homogéneo y del '
     'estratificado.'),
    ('## 5.2 — Modificar redes de flujo regionales', 'fig_5_02_redes',
     'Problema 5.2(a) — el patrón original cerrado y simétrico, y el resultado '
     'de abrir la frontera izquierda al flujo.'),
    ('## 5.3 — El canal a nivel del mar (el problema estrella del capítulo)',
     'fig_5_03_perfiles',
     'Problema 5.3 — perfiles del nivel freático y decaimiento del caudal hacia '
     'el canal.'),
    ('## 5.4 — Estabilidad de excavaciones', 'fig_5_04_excavacion',
     'Problema 5.4 — mecanismo de falla y factor de seguridad frente a la '
     'profundidad excavada.'),
]

GUIA_EXTRA = [
    ('### La condición de borde clave', 'fig_5_01_refraccion',
     'La continuidad del flujo normal en una interfaz produce la refracción de '
     'las líneas de flujo, análoga a la ley de Snell.'),
]


# ----------------------------------------------------------------- utilidades
def replace_blocks(text, mapping):
    out, n, inb, buf = [], 0, False, []
    for ln in text.split('\n'):
        if ln.startswith('```'):
            if not inb:
                inb, buf, n = True, [], n + 1
            else:
                inb = False
                rep = mapping.get(n, 'KEEP')
                if rep == 'KEEP':
                    out += ['```'] + buf + ['```']
                elif rep is not None:
                    out.append(figmd(rep[0], rep[1]))
            continue
        (buf if inb else out).append(ln)
    return '\n'.join(out)


def insert_after_first_para(text, anchor, fig, cap):
    lines = text.split('\n')
    try:
        i = lines.index(anchor)
    except ValueError:
        print('   !! encabezado no encontrado:', anchor[:65])
        return text
    j = i + 1
    while j < len(lines) and lines[j].strip() == '':
        j += 1
    while j < len(lines) and lines[j].strip() != '':
        j += 1
    lines.insert(j, figmd(fig, cap))
    return '\n'.join(lines)


# ----------------------------------------------------------------- cabeceras
PRE_SOL = """---
title: "Solucionario de los ejercicios de los capítulos 3, 4 y 5"
subtitle: "Domenico & Schwartz · Physical and Chemical Hydrogeology · 2.ª edición · Wiley, 1997"
author: "Hidráulica Subterránea  ·  Preparación para el parcial"
lang: es
toc: true
toc-title: "Contenido"
toc-depth: 2
---

**Fuente de los enunciados.** Domenico, P. A. & Schwartz, F. W. (1997).
*Physical and Chemical Hydrogeology*, 2.ª edición, John Wiley & Sons.
Secciones *Problems* de los capítulos 3, 4 y 5, páginas 55–57, 73–74 y 102.

**Qué contiene este documento.** Las 33 soluciones completas (17 del capítulo 3,
10 del capítulo 4 y 6 del capítulo 5), con el desarrollo algebraico, las
verificaciones y 25 figuras. Las redes de flujo de los problemas 4.6 a 4.10 y
5.2 no son esquemas a mano alzada: se obtuvieron resolviendo la ecuación de
Laplace $\\nabla^2h=0$ por diferencias finitas, y las líneas de flujo se
integraron de modo que cada tubo transporte el mismo caudal.

**Documento complementario.** La *Guía explicada paso a paso* desarrolla el
método de cada ejercicio: qué reconocer en el enunciado, qué fórmula aplica y
por qué, en qué orden, cómo verificar y dónde está la trampa.

"""

PRE_GUIA = """---
title: "Guía explicada paso a paso"
subtitle: "Cómo se resuelve cada ejercicio de los capítulos 3, 4 y 5 de Domenico & Schwartz"
author: "Hidráulica Subterránea  ·  Preparación para el parcial"
lang: es
toc: true
toc-title: "Contenido"
toc-depth: 2
---

"""

# ------------------------------------------- actualizacion numerica de 4.7
OLD_47 = """| Caso | $n_f$ | $n_d$ | $Q$ (m³/s por m) | % respecto al caso base |
|---|---|---|---|---|
| Delantal completo (problema 6) | 5 | 15 | $3.33\\times10^{-3}$ | 100 % |
| Delantal a la mitad (a) | 5 | 12 | $4.17\\times10^{-3}$ | 125 % |
| Sin delantal (b) | 5 | 9 | $5.56\\times10^{-3}$ | 167 % |

Ejemplo de cálculo (caso base):

$$Q = (5\\times10^{-4})(20)\\left(\\frac{5}{15}\\right) = 3.33\\times10^{-3}\\ \\mathrm{m^3/s\\ por\\ m} = 288\\ \\mathrm{m^3/día\\ por\\ m}$$"""

NEW_47 = """| Caso | $n_f$ | $n_d$ | $n_f/n_d$ | $Q$ (m³/s por m) | $Q$ (m³/día·m) | % del caso base |
|---|---|---|---|---|---|---|
| Delantal completo (problema 6) | 5 | 14 | 0.357 | $3.64\\times10^{-3}$ | 315 | 100 % |
| Delantal a la mitad (a) | 5 | 10 | 0.500 | $5.05\\times10^{-3}$ | 437 | 139 % |
| Sin delantal (b) | 6 | 7 | 0.857 | $8.73\\times10^{-3}$ | 755 | 240 % |

Ejemplo de cálculo (caso base):

$$Q = K\\,H\\,\\frac{n_f}{n_d} = (5\\times10^{-4})(20)\\left(\\frac{5}{14}\\right) = 3.6\\times10^{-3}\\ \\mathrm{m^3/s\\ por\\ m} = 315\\ \\mathrm{m^3/día\\ por\\ m}$$

**Verificación numérica.** Las tres redes de la figura se obtuvieron resolviendo
$\\nabla^2h = 0$ por diferencias finitas (malla de 2 m, SOR rojo-negro) sobre una
cimentación permeable de 60 m de espesor y 300 m de longitud, con el delantal
ocupando 90 m, 45 m y 0 m respectivamente. El caudal se integró en una sección
vertical bajo la presa, por donde pasa todo el flujo. Los factores de forma
calculados son $0.364$, $0.505$ y $0.873$, que coinciden con los conteos
$5/14$, $5/10$ y $6/7$ de la tabla con un error inferior al 2 %. Las
proporciones de la figura del libro no están a escala, de modo que los valores
absolutos dependen de la geometría supuesta; lo que no depende de ella es la
**tendencia**, que es lo que el problema pide."""


def build(src, out_md, pre, blocks, inserts, extra, strip, clean_index=False):
    _n['v'] = 0
    t = open(src, encoding='utf-8').read()
    t = '\n'.join(t.split('\n')[strip:])
    if clean_index:
        t = re.sub(r'## Índice\n+(?:- \[[^\]]*\]\([^)]*\)\n)+\n*---\n', '', t)
        t = re.sub(r'<a name="[^"]*"></a>\n?', '', t)
        t = t.replace('`01_Solucionario_Cap3-4-5.md`',
                      'el documento *Solucionario de los ejercicios de los '
                      'capítulos 3, 4 y 5*')
    else:
        t = t.replace(OLD_47, NEW_47)
    t = replace_blocks(t, blocks)
    for anchor, fig, cap in inserts:
        t = insert_after_first_para(t, anchor, fig, cap)
    for anchor, fig, cap in extra:
        t = insert_after_first_para(t, anchor, fig, cap)
    # las reglas horizontales son redundantes: Heading1 ya abre pagina nueva
    t = re.sub(r'\n---\n', '\n', t)
    # secciones finales del solucionario al nivel de capitulo
    t = t.replace('## Resumen de resultados', '# Resumen de resultados')
    t = t.replace('## Advertencias sobre datos que dependen de las figuras del libro',
                  '# Advertencias sobre datos que dependen de las figuras del libro')
    t = re.sub(r'\n{4,}', '\n\n\n', t)
    open(out_md, 'w', encoding='utf-8').write(pre + t)
    print(f'   {os.path.basename(out_md)}: {_n["v"]} figuras insertadas')


print('1) transformando fuentes markdown')
build(f'{SB}/01_Solucionario_Cap3-4-5.md', f'{SRC}/sol.md', PRE_SOL,
      SOL_BLOCKS, SOL_INSERTS, SOL_EXTRA, strip=5)
build(f'{SB}/02_Guia_Explicada_Paso_a_Paso.md', f'{SRC}/guia.md', PRE_GUIA,
      GUIA_BLOCKS, GUIA_INSERTS, GUIA_EXTRA, strip=5, clean_index=True)

print('2) convirtiendo a docx')
import pypandoc
PD = pypandoc.get_pandoc_path()
jobs = [('sol.md', 'Solucionario_Ejercicios_Cap3-4-5.docx'),
        ('guia.md', 'Guia_Explicada_Paso_a_Paso_Cap3-4-5.docx')]
for md, docx in jobs:
    cmd = [PD, md, '-o', f'{SB}/{docx}',
           '--reference-doc', f'{BD}/reference.docx',
           '--toc', '--toc-depth=2',
           '--from', 'markdown+tex_math_dollars+pipe_tables+raw_tex',
           '--resource-path', SRC,
           '--metadata', 'lang=es']
    r = subprocess.run(cmd, cwd=SRC, capture_output=True, text=True)
    if r.returncode:
        print('   ERROR:', r.stderr[:2000])
    else:
        sz = os.path.getsize(f'{SB}/{docx}')
        print(f'   {docx}  ({sz/1024:.0f} KB)')
print('listo')

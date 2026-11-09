"""Ensambla el libro completo: fundamentos, bombeo, acuífero, resumen e inicio."""
import sys
sys.path.insert(0, '/projects/sandbox/.calc')
from xl_lib import *
import xl_part1, xl_part2, xl_part3          # noqa: F401  (construyen las hojas)
from openpyxl.workbook.properties import CalcProperties

OUT = '/projects/sandbox/Hidraulica_Subterranea_Calculadora.xlsx'

# =========================================================== RESUMEN
h = Hoja('Resumen', 'Respuestas del taller y de los apuntes',
         'Para comprobar tus resultados. El desarrollo está en la Guía Maestra.',
         widths={'B': 12, 'C': 110, 'D': 3, 'E': 3})
ws = h.ws
BLOQUES = [
    ('Capítulo 3: movimiento del agua subterránea', [
        ('3.1', 'q = 1.9×10⁻⁸ m/s'),
        ('3.2', 'v = 1.9×10⁻⁷ m/s (nₑ = 0.1) y 1.9×10⁻⁴ m/s (nₑ = 10⁻⁴)'),
        ('3.3', 'Medio granular frente a roca fracturada'),
        ('3.4–3.5', '[P/ρg] = L;  [h] = L (energía/peso);  [φ] = L²/T² (energía/masa)'),
        ('3.6', 'i = 0.141 m/m, flujo hacia el S 45° O'),
        ('3.7', 'h: 300 / 205 / 110 / 15 m;  hₚ: 200 / 190 / 50 / 8 m;  z: 100 / 15 / 60 / 7 m'),
        ('3.8', '3.28×10⁻⁶ ft/s;  2.12 gpd/ft²;  1.02×10⁻⁹ cm²;  0.103 darcy'),
        ('3.9', 'Flujo horizontal (∂z/∂x = 0), ρ y μ constantes'),
        ('3.10', 'Sólo (a) es correcta; (d) invierte q y v; b, c, e, f, g omiten el signo menos'),
        ('3.11', 'Kh = 3.70×10⁻⁷ m/s;  Kv = 2.70×10⁻⁸ m/s;  Kh/Kv = 13.7'),
        ('3.12', 'q_x = 1×10⁻⁴ cm/s (simetría del tensor)'),
        ('3.13', 'K más alta: K₃;  más baja: K₂;  razón ≈ 3–4'),
        ('3.14', 'Recarga: las equipotenciales se juntan;  descarga: se separan'),
        ('3.15', 'Mayor velocidad en h₄ (el doble); flujo descendente en ambas regiones'),
        ('3.16', 'q = 5×10⁻⁸ cm/s, descendente'),
        ('3.17', 'Q entrada 1×10⁻⁴ m³/s en cada uno;  salidas 1.5×10⁻⁴ y 5×10⁻⁵ m³/s;  i = 0.15 y 0.05'),
    ]),
    ('Capítulo 4: ecuaciones de flujo, fronteras y redes', [
        ('4.1', '∂²h/∂x² = (Ss/K)∂h/∂t;  ∇²h = (ρgβp/K)∂h/∂t;  ∇²h = 0;  arcilla'),
        ('4.2', '300 m³;  S = 8.48×10⁻⁵ con matriz incompresible;  βp = 3.66×10⁻¹⁰ m²/N'),
        ('4.3', 'El caudal de bombeo Q;  el volumen total extraído Q·t'),
        ('4.4', '6250 / 4368 / 1882 lb/ft²;  4998 / 4368 / 630;  no se puede desecar (FS = 0.86);  d crít ≈ 30.1 ft'),
        ('4.5', 'T = Q/(nf·Δh) ≈ 1.2×10³ m²/día'),
        ('4.6', 'AB y DE: equipotenciales (carga constante);  BC, CD y FG: líneas de flujo (sin flujo)'),
        ('4.7', 'Q = K·H·nf/nd:  3.6 / 5.1 / 8.7 ×10⁻³ m³/s por m'),
        ('4.8–4.10', 'Redes de flujo (Guía, Parte 5);  x′ = 0.447x;  K eq = √(Kh·Kv) = 2.24·Kv'),
    ]),
    ('Capítulo 5: el agua subterránea en el ciclo hidrológico', [
        ('5.1', '5.8 añade continuidad del potencial y del flujo normal en las interfaces'),
        ('5.2', 'Se pierde la simetría y se refuerza el flujo regional;  con K₁ = K₂ dominan las celdas locales'),
        ('5.3', 'h en la divisoria: 12.00 / 12.00 / 11.86 / 10.67 m;  q′ = 1.25×10⁻² y 3.96×10⁻³ m³/día por m'),
        ('5.4', 'FS = σT/u;  d crít = (γsat·D − γw·hₚ)/(γsat − γw)'),
        ('5.5', 'Q máx = 0.6π·K·d²·G = 7.0×10⁻³ m³/s = 7 L/s'),
        ('5.6', 'x toe = 2061 ft (con q′ = 2×10⁻⁴);  4124 ft con la mitad del caudal'),
    ]),
    ('Apuntes de clase', [
        ('Dupuit', 'q′ ≈ −2.46 y −2.49 m²/día;  d cae fuera del acuífero: NO hay divisoria ni h máx'),
        ('Costa', 'ΔL = −33 m;  x_T: 924.4 → 885.2 m;  la cuña avanza 6.1 m;  el nivel sube 0.41 m'),
        ('Thiem', 'T = 0.503·Q = 396 m²/día con Q = 788 m³/día'),
        ('Theis', 'T = 13 677 ft²/día;  S = 1.95×10⁻⁴'),
        ('Pozos', 's₁ = 8.40 m;  s₂ = 21.00 m;  total 29.40 m;  R₀ = 1061 m'),
        ('Fig. 3.31', 'i máx ≈ 0.010 (17–18 m);  i mín ≈ 0.0016 (22–23 m);  pozo sur 22.5 m'),
        ('Fig. 7.39', 'A ≈ 12.5;  B ≈ 2.5;  C = 5;  D ≈ 8;  E = 5;  F ≈ 12.5 m'),
    ]),
]
r = 5
for titulo, filas in BLOQUES:
    r += 1
    for col in 'BC':
        ws[f'{col}{r}'].fill = FILL_SEC
    ws[f'B{r}'] = titulo
    ws[f'B{r}'].font = F_SEC
    r += 1
    for num, txt in filas:
        a = ws[f'B{r}']
        a.value = num
        a.font = Font(bold=True, color='1F3864')
        a.border = BOX
        b = ws[f'C{r}']
        b.value = txt
        b.border = BOX
        b.alignment = Alignment(wrap_text=True)
        r += 1

# =========================================================== INICIO
ws = INI
ws.sheet_view.showGridLines = False
for k, wd in {'A': 2, 'B': 24, 'C': 62, 'D': 40}.items():
    ws.column_dimensions[k].width = wd
for col in 'BCD':
    for rr in (1, 2):
        ws[f'{col}{rr}'].fill = FILL_T
ws['B1'] = 'Hidráulica Subterránea: calculadora programada'
ws['B1'].font = Font(size=18, bold=True, color='FFFFFF')
ws['B2'] = ('Todas las fórmulas del curso en hojas que se calculan solas. '
            'Cada hoja trae cargado un ejemplo de la Guía para que compruebes que funciona.')
ws['B2'].font = F_S
ws.row_dimensions[1].height = 34
ws.row_dimensions[2].height = 20
r = 4


def sec(text):
    global r
    for col in 'BCD':
        ws[f'{col}{r}'].fill = FILL_SEC
    ws[f'B{r}'] = text
    ws[f'B{r}'].font = F_SEC
    r += 1


sec('Cómo se usa')
LEY = [(FILL_IN, F_IN, '1500', 'Celda AMARILLA: dato. Escribe aquí tus valores.'),
       (FILL_OUT, F_OUT, '300.5', 'Celda VERDE: resultado. Se calcula sola; no la escribas.'),
       (FILL_MAIN, F_MAIN, '9.8E-04', 'Verde oscuro: resultado principal de la hoja.'),
       (FILL_OK, Font(bold=True, color='006100'), '✔ VÁLIDO', 'Verificación correcta.'),
       (FILL_WARN, Font(bold=True, color='9C5700'), '⚠ ACEPTABLE', 'Verificación dudosa: revisa.'),
       (FILL_BAD, Font(bold=True, color='9C0006'), '✘ NO VÁLIDO', 'Verificación fallida: corrige el dato.')]
for fill, font, ej, txt in LEY:
    c = ws[f'B{r}']
    c.value, c.fill, c.font, c.border = ej, fill, font, BOX
    c.alignment = Alignment(horizontal='center')
    ws[f'C{r}'] = txt
    r += 1
for txt in ['Unidades: metros, días y m³/día, salvo que la celda diga otra cosa. La hoja Unidades convierte todo.',
            'Para volver a los ejemplos originales, cierra sin guardar o descarga el archivo otra vez.',
            'Si al abrir ves celdas vacías (vista previa del celular o de GitHub), ábrelo en Excel, '
            'LibreOffice o Google Sheets: las fórmulas se calculan al abrir.']:
    ws.merge_cells(f'B{r}:D{r}')
    ws[f'B{r}'] = '• ' + txt
    ws[f'B{r}'].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 30
    r += 1
r += 1
sec('¿Qué hoja uso?')
DEC = [('Una tabla de t y s en un piezómetro', 'Cooper_Jacob (y Theis si u > 0.01)'),
       ('s en varios piezómetros al mismo tiempo', 'Dist_abatimiento'),
       ('Mediciones después de apagar la bomba', 'Recuperacion'),
       ('"El abatimiento se estabilizó"', 'Thiem_Dupuit'),
       ('Ya tienes T y S y te piden s, Q máx, R₀…', 'Calc_acuifero'),
       ('Varios pozos, un río o una falla', 'Superposicion'),
       ('Acuífero libre entre dos canales con lluvia', 'Dupuit_recarga'),
       ('Costa, cuña salina o subida del mar', 'Costa'),
       ('Zanja o excavación sobre un acuífero artesiano', 'Esfuerzos'),
       ('Varias capas con distinta K', 'Capas')]
thead(ws, r, 2, ['Si te dan…', 'Usa la hoja'], height=22)
ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
r += 1
for a, b in DEC:
    ws[f'B{r}'] = a
    ws[f'B{r}'].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 28
    link(ws[f'C{r}'], b.split(' ')[0], b)
    r += 1
r += 1
sec('Índice de hojas')
for name, title, sub in INDEX:
    link(ws[f'B{r}'], name, name)
    ws[f'C{r}'] = title
    ws[f'C{r}'].font = Font(bold=True)
    ws[f'D{r}'] = sub
    ws[f'D{r}'].font = F_NOTE
    ws[f'D{r}'].alignment = Alignment(wrap_text=True, vertical='center')
    ws.row_dimensions[r].height = 30
    r += 1

# =========================================================== cierre
apply_checks()
wb.calculation = CalcProperties(fullCalcOnLoad=True)
for wsx in wb.worksheets:
    wsx.sheet_properties.tabColor = {'INICIO': '1F3864', 'Resumen': '7F7F7F'}.get(wsx.title, None)
for nm in ('Cooper_Jacob', 'Theis', 'Dist_abatimiento', 'Recuperacion', 'Thiem_Dupuit'):
    wb[nm].sheet_properties.tabColor = 'B03030'
for nm in ('Calc_acuifero', 'Superposicion'):
    wb[nm].sheet_properties.tabColor = 'E0A800'
for nm in ('Dupuit_recarga', 'Costa', 'Canal'):
    wb[nm].sheet_properties.tabColor = '2B8A3E'
wb.active = 0
wb.save(OUT)
print('guardado:', OUT)
print('hojas:', [s.title for s in wb.worksheets])

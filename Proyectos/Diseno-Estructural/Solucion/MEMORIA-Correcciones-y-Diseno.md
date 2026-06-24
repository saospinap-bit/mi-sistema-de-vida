# MEMORIA DE CÁLCULO — CORRECCIONES Y DISEÑO DE ELEMENTOS
**Proyecto:** Edificio Residencial Santa Marta · **Sistema:** Pórticos de concreto reforzado DMO · **Materiales:** f'c = 28 MPa, fy = 420 MPa

> Este documento (1) corrige, parte por parte, los datos desactualizados de la memoria entregada y (2) agrega el capítulo de diseño de viguetas, vigas y riostras que faltaba. Pensado para copiarse/adaptarse al documento final y para sustentar.

---

# PARTE A — CORRECCIONES A LA MEMORIA (ERRATA)

## A.1 Parámetros sísmicos y coeficiente R  ⚠️ (sección que obtuvo 0.00)
**Problema:** la memoria no identifica el sistema sismorresistente ni el coeficiente de disipación de energía.

**Corrección (agregar):**
- Sistema estructural: **pórticos resistentes a momentos de concreto reforzado con capacidad MODERADA de disipación de energía (DMO)**, en las dos direcciones (NSR-10 Tabla A.3-3).
- **R₀ = 5.0** (DMO) · **Ω₀ = 3.0** (sobrerresistencia).
- Coeficiente de disipación de diseño: **R = R₀·φa·φp·φr**.
- Justificación del DMO: Santa Marta → Aa = 0.15 → **amenaza sísmica intermedia**, donde el mínimo exigido para pórticos de concreto es DMO.

## A.2 Pesos de la edificación y cortante basal  ⚠️ (dato desactualizado)
**Problema:** la memoria reporta **Vs = 11 717.7 kN** con masa **m = 31 813 kN**, valores de una versión anterior.

**Corrección:** con los pesos finales (incluye columnas, vigas y fachada actualizadas):
| Parámetro | Memoria (viejo) | **Valor actualizado** |
|---|---|---|
| Peso total W | 31 813 kN | **41 074 kN** |
| Sa | 0.368 | 0.368 (T = Ta) |
| **Cortante basal Vs = Sa·W** | 11 718 kN | **15 128 kN** |

Fuerzas por piso (Fx = Fy), k = 1.027:
| Piso | h (m) | Fx (kN) |
|---|---|---|
| 1 | 3.5 | 991.6 |
| 2 | 6.5 | 2 477.8 |
| 3 | 9.5 | 3 658.6 |
| 4 | 12.5 | 4 849.7 |
| 5 | 15.5 | 3 151.1 |
| **Σ** | | **15 128.7** |

## A.3 Análisis de irregularidades  ⚠️ (faltaba)
Agregar la evaluación NSR-10 A.3 (hoja *Irregularidades* del Excel):
- **Torsión (1aP):** δmax/δprom = **1.02 (X)** y **1.01 (Y)** < 1.20 → sin irregularidad.
- **Masa (2A):** 9 604/7 257 = 1.32 < 1.50 → regular.
- **Rigidez (1aA):** rigidez creciente hacia la base → sin piso flexible.
- **Diafragma (3P):** abertura 27.0 m² < 0.5·A·B = 292.6 m² → regular.
- **Retrocesos (2P):** 13.9 % y 16.6 % (no ambas > 15 %) → regular.
- **Conclusión:** φp = φa = φr = 1.0 → **R = 5.0**.

## A.4 Losa aligerada (verificar consistencia)
- Loseta superior **hf = 0.06 m**, vigueta **0.15 × 0.34 m**, separación **0.80 m** (consistente con el avalúo). En el modelo SAP la loseta debe llevar este espesor (un error frecuente fue dejarla en 0, lo que invalida el análisis).

## A.5 Derivas y combinaciones de carga
- **Derivas:** se verifican con las fuerzas sísmicas **sin reducir** por R (NSR-10 A.6). Con las fuerzas actualizadas, la deriva máxima resultó **0.029 < 0.030 m (1 % h)** → CUMPLE.
- **Combinaciones:** distinguir las usadas para **derivas** (servicio/fuerza sísmica sin reducir) de las de **diseño de resistencia** (E ÷ R). Las solicitaciones sísmicas de diseño de cada elemento = (efecto del análisis elástico) **/ R = / 5**.

---

# PARTE B — DISEÑO DE VIGUETAS, VIGAS Y RIOSTRAS

> Todos los cálculos automáticos están en el libro **Diseno-Estructural-Calculos.xlsx** (hojas *Cuadro Viguetas*, *Cuadro Vigas-Riostras*, *Diseño Vigas/Riostras/Viguetas*). Las solicitaciones de las vigas y riostras se obtuvieron de la **envolvente del modelo SAP** con el **sismo reducido por R = 5**.

## B.1 Criterios y materiales
- f'c = 28 MPa, fy = 420 MPa. Recubrimiento 0.04 m (vigas) / 0.03 m (viguetas).
- φ = 0.90 (flexión), φ = 0.75 (cortante y torsión).
- Cuantía máxima DMO: ρ ≤ 0.025. Cuantía mínima: As_min = máx(0.25√f'c/fy ; 1.4/fy)·b·d.
- Detallado sísmico DMO (C.21.3): confinamiento de estribos en 2h desde la cara del nudo, ganchos sísmicos a 135°, cortante por capacidad.

## B.2 Diseño de VIGUETAS (losa aligerada — sección T, gravedad)
**Método:** vigueta continua. wu = (1.2D + 1.6L)·sv. Momentos por coeficientes (C.8.3.3): M⁻ = wuLn²/10, M⁺ = wuLn²/14; cortante Vu = 1.15·wuLn/2. La loseta actúa como ala a compresión (bf = mín(Ln/4 ; bw+16hf ; sv)).

**Cargas:** entrepiso D = 7.04 kN/m², L = 1.8 kN/m²; **cubierta** (terraza social) D = 4.38 kN/m², **L = 5.0 kN/m² (gobierna)**.

**Cuadro de viguetas (sección 15×34, d = 304 mm):**
| Tipo | L ejes | Ln | wu | M⁻ | M⁺ | Vu | Refuerzo | Estribos |
|---|---|---|---|---|---|---|---|---|
| VT-1 | 2.20 | 1.85 | 9.1–10.6 | 3.1 | 2.2 | 9.6 | 2#4 + 2#4 | No |
| VT-2 | 3.60 | 3.25 | 9.1–10.6 | 11.2 | 8.0 | 19.8 | 2#4 + 2#4 | No |
| VT-3 | 4.80 | 4.45 | 9.1–10.6 | 21.0 | 15.0 | 27.1 | 2#4 + 2#4 | No |
| VT-4 | 5.15 | 4.80 | 10.6 | 24.4 | 17.4 | 29.3 | 2#4 + 2#4 | No |

Como las solicitaciones son bajas, **todas** las viguetas quedan con el **acero mínimo (2#4)** y **no requieren estribos** (Vu ≤ φ·1.1·Vc = 33.8 kN). Loseta con malla de retracción Ø6 @ 250 mm.

## B.3 Diseño de VIGAS DE CARGA (VC 40×30)
**Solicitaciones (envolvente SAP, sismo/R):** se agrupan en 3 tipos por nivel de demanda. Diseño por flexión (ρ, As, ductilidad), cortante (Vc + estribos + capacidad DMO Ve) y torsión.

**Ejemplo tipo crítico VC-3** (d = 342.6 mm, Mu⁻ = 142 kN·m):
Rn = 4.48 MPa → ρ = 0.0119 → As = 1 226 mm² → **7 #5** (As = 1 393 mm²); a = 81.9 mm; **φMn = 158.8 ≥ 142 kN·m ✓**. Cortante: Vc = 92.4 kN, Vs_req = 51.6 kN, estribos #3 @ 86 mm en confinamiento. Capacidad: Ve = 76 kN < Vu → gobierna Vu. Torsión Tu = 20 > Tumbral 3.4 → diseñar refuerzo por torsión.

**Cuadro de vigas VC 40×30:**
| Tipo | N° vigas | M⁻ | Acero sup | Acero inf | Estribos |
|---|---|---|---|---|---|
| VC-1 | 148 | ≤80 | 4 #5 | 3 #5 | #3 @86/150 |
| VC-2 | 120 | ≤120 | 6 #5 | 5 #5 | #3 @86/150 |
| VC-3 | 12 | ≤142 | 7 #5 | 4 #5 | #3 @86/150 |

## B.4 Diseño de RIOSTRAS / VIGAS DE RIGIDEZ (VR 40×35)
**Ejemplo tipo crítico VR-4** (d = 342.6 mm, Mu⁻ = 250 kN·m):
ρ = 0.020 → As = 2 330 mm² → **12 #5** (As = 2 388, ρ = 1.99 % < 2.5 % ✓); **φMn = 254.9 ≥ 250 ✓**. Cortante: Vu = 202 kN, estribos #3 @ 85 mm; capacidad Ve. Torsión Tu = 26 > 4.3 → diseñar. (Para reducir el número de barras puede usarse #6 o #7.)

**Cuadro de riostras VR 40×35:**
| Tipo | N° vigas | M⁻ | Acero sup | Acero inf | Estribos |
|---|---|---|---|---|---|
| VR-1 | 170 | ≤100 | 5 #5 | 4 #5 | #3 @85/150 |
| VR-2 | 120 | ≤140 | 6 #5 | 5 #5 | #3 @85/150 |
| VR-3 | 6 | ≤200 | 9 #5 | 6 #5 | #3 @85/150 |
| VR-4 | 14 | ≤250 | 12 #5 | 6 #5 | #3 @85/150 |

## B.5 Despiece (planos)
Planos en DXF (editables en AutoCAD), uno por familia y tipo:
- `Despiece-Viguetas.dxf` · `Despiece-Vigas-VC.dxf` · `Despiece-Riostras-VR.dxf`

Cada despiece muestra: elevación con acero inferior corrido y bastones superiores (L/4 + ld), estribos con zona de confinamiento (2h) y zona central, sección transversal con distribución de barras y notas de armado.

---

## Nota de integridad
Todos los valores provienen de tu modelo SAP (envolvente de las 10 combinaciones) y de tu avalúo de cargas, con la metodología NSR-10 / ACI 318. Verifica las **dimensiones reales de las secciones** (b×h) en tu modelo y confirma con tu grupo el sistema **DMO (R = 5)** antes de la entrega.

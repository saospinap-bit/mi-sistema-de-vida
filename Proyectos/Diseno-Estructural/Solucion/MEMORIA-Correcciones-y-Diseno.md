# MEMORIA DE CÁLCULO — ANÁLISIS SÍSMICO, IRREGULARIDADES Y DISEÑO DE ELEMENTOS
**Proyecto:** Edificio Residencial Santa Marta · **Sistema:** Pórticos de concreto reforzado **DMO** · **Materiales:** f'c = 28 MPa, fy = 420 MPa

> Documento para integrar a la memoria final. Contiene: (1) el **análisis sísmico completo y corregido** (FHE), (2) el **análisis de irregularidades** (NSR-10 A.3) y (3) el **diseño de viguetas, vigas y riostras**. Cálculos automáticos en `Diseno-Estructural-Calculos.xlsx`.

---

# 1. ANÁLISIS SÍSMICO — FUERZA HORIZONTAL EQUIVALENTE (NSR-10 Cap. A.4)

## 1.1 Espectro de diseño (A.2.6)
| Parámetro | Valor | Fuente |
|---|---|---|
| Aceleración horizontal pico efectiva, **Aa** | 0.15 | Santa Marta (A.2.3) |
| Velocidad horizontal pico efectiva, **Av** | 0.10 | Santa Marta (A.2.3) |
| Tipo de perfil de suelo | **C** | Estudio de suelos |
| Coef. amplificación, **Fa / Fv** | 1.20 / 1.70 | A.2.4 |
| Coef. de importancia, **I** | 1.0 | Grupo I, residencial (A.2.5) |
| Período inicial, **T₀ = 0.1·Av·Fv/(Aa·Fa)** | 0.094 s | |
| Período corto, **Tc = 0.48·Av·Fv/(Aa·Fa)** | 0.453 s | |
| Período largo, **TL = 2.4·Fv** | 4.08 s | |
| Aceleración espectral máxima, **Sa = 2.5·Aa·Fa·I** | **0.450** | meseta |

## 1.2 Período fundamental y cortante basal (A.4.2 – A.4.3)
- Período aproximado: **Ta = Ct·hⁿ** con Ct = 0.047 y α = 0.90 (pórtico de concreto), h = 15.5 m → **Ta = 0.554 s**.
- Coef. de período: **Cu = 1.75 − 1.2·Av·Fv = 1.546** → T_máx = Cu·Ta = 0.856 s.
- Se adopta **T = Ta = 0.554 s** (> Tc, rama descendente):
  **Sa = 1.2·Av·Fv·I / T = 0.368**
- Peso sísmico total de la edificación: **W = 41 074 kN** *(valor actualizado; la versión previa de la memoria usaba 31 813 kN)*.
- **Cortante sísmico en la base:  Vs = Sa·W = 0.368 × 41 074 = 15 129 kN**  (Vs/W = 0.368).

## 1.3 Distribución vertical de la fuerza sísmica (A.4.3.2)
Exponente **k = 0.75 + 0.5·T = 1.027**. Fuerza por nivel **Fx = Cvx·Vs**, con **Cvx = Wx·hx^k / Σ(Wi·hi^k)**.
Torsión accidental: **MFx = Fx·0.05·Ly** y **MFy = Fy·0.05·Lx** (Lx = 36.6 m, Ly = 15.99 m).

| Piso | hx (m) | Wx (kN) | Wx·hx^k | Cvx | **Fx = Fy (kN)** | MFx (kN·m) | MFy (kN·m) |
|---|---|---|---|---|---|---|---|
| 1 | 3.5 | 7 257.7 | 26 273 | 0.0655 | **991.6** | 792.7 | 1 814.5 |
| 2 | 6.5 | 9 604.3 | 65 655 | 0.1638 | **2 477.8** | 1 981.0 | 4 534.4 |
| 3 | 9.5 | 9 604.3 | 96 943 | 0.2418 | **3 658.6** | 2 925.1 | 6 695.2 |
| 4 | 12.5 | 9 604.3 | 128 503 | 0.3206 | **4 849.7** | 3 877.3 | 8 874.9 |
| 5 (cub.) | 15.5 | 5 003.6 | 83 496 | 0.2083 | **3 151.1** | 2 519.3 | 5 766.5 |
| **Σ** | | **41 074** | 400 870 | 1.000 | **15 128.7** | | |

> **Nota metodológica:** Vs y las derivas se calculan con la fuerza sísmica **sin reducir** por R (NSR-10 A.6). La reducción por R se aplica a las **solicitaciones de diseño de los elementos**: E_diseño = E_análisis / R.

---

# 2. ANÁLISIS DE IRREGULARIDADES Y COEFICIENTE R (NSR-10 A.3)

## 2.1 Coeficiente básico
Sistema: pórticos resistentes a momentos de concreto reforzado **DMO** (Santa Marta, amenaza intermedia) → **R₀ = 5.0**, **Ω₀ = 3.0** (Tabla A.3-3).

## 2.2 Irregularidades en planta (φp) — Tabla A.3-6
| Tipo | Criterio | Verificación | ¿Irregular? | Coef. |
|---|---|---|---|---|
| 1aP Torsional | δmax/δprom > 1.20 | **1.02 (X), 1.01 (Y)** (183 nudos/piso) | No | 1.0 |
| 2P Retrocesos esquinas | ambas proy. > 15 % | 13.9 % y 16.6 % (no ambas) | No | 1.0 |
| 3P Discontinuidad diafragma | abertura > 50 % área | 27.0 < 292.6 m² | No | 1.0 |
| 4P Desplaz. fuera del plano | — | columnas continuas | No | 1.0 |
| 5P Sistemas no paralelos | — | ejes ortogonales | No | 1.0 |
| | | | **φp =** | **1.0** |

## 2.3 Irregularidades en altura (φa) — Tabla A.3-7
| Tipo | Criterio | Verificación | ¿Irregular? | Coef. |
|---|---|---|---|---|
| 1aA Piso flexible | ki/ki+1 < 0.70 | mín = 1.07 (rigidez crece a la base) | No | 1.0 |
| 2A Masa | mi/mi±1 > 1.50 | 9 604/7 257 = 1.32 | No | 1.0 |
| 3A Geométrica vertical | dim > 1.30 adyacente | planta constante | No | 1.0 |
| 4A Desplaz. en el plano | — | sin offset | No | 1.0 |
| 5A Piso débil | resist < 0.80 | pórtico regular | No | 1.0 |
| | | | **φa =** | **1.0** |

## 2.4 Ausencia de redundancia (φr — A.3.3.8)
Pórtico completo, ≥ 2 líneas de resistencia por dirección → **φr = 1.0**.

## 2.5 Coeficiente de disipación de energía de diseño
**R = R₀·φa·φp·φr = 5.0 × 1.0 × 1.0 × 1.0 = 5.0**

> **Conclusión:** la estructura es **regular** en planta y en altura. Las solicitaciones sísmicas de diseño de los elementos se reducen con **R = 5**.

## 2.6 Derivas (A.6)
Calculadas con las fuerzas sin reducir; deriva máxima **0.029 m < 0.030 m (1 % de hpi)** → **CUMPLE**.

---

# 3. DISEÑO DE VIGUETAS, VIGAS Y RIOSTRAS

## 3.1 Criterios y materiales
- f'c = 28 MPa, fy = 420 MPa. Recubrimiento 0.04 m (vigas) / 0.03 m (viguetas).
- φ = 0.90 (flexión), φ = 0.75 (cortante y torsión).
- ρ_máx (DMO) ≤ 0.025; As_min = máx(0.25√f'c/fy ; 1.4/fy)·b·d.
- Detallado DMO (C.21.3): estribos de confinamiento en 2h desde la cara del nudo, ganchos a 135°, cortante por capacidad (Mpr con 1.25 fy).

## 3.2 Viguetas (losa aligerada — sección T, gravedad)
wu = (1.2D + 1.6L)·sv. Momentos por coeficientes (C.8.3.3): M⁻ = wuLn²/10, M⁺ = wuLn²/14; Vu = 1.15·wuLn/2. Ala efectiva bf = mín(Ln/4 ; bw+16hf ; sv).
Cargas: entrepiso D = 7.04 / L = 1.8 kN/m²; **cubierta (terraza social) D = 4.38 / L = 5.0 kN/m² (gobierna)**.

**Cuadro de viguetas (15×34, d = 304 mm):** todas resultan con **acero mínimo 2 #4** (sup. e inf.) y **sin estribos** (Vu ≤ φ·1.1·Vc = 33.8 kN). Loseta con malla Ø6 @ 250 mm.
| Tipo | L ejes | Ln | M⁻ máx | Refuerzo |
|---|---|---|---|---|
| VT-1 | 2.20 | 1.85 | 3.6 | 2#4 + 2#4 |
| VT-2 | 3.60 | 3.25 | 11.2 | 2#4 + 2#4 |
| VT-3 | 4.80 | 4.45 | 21.0 | 2#4 + 2#4 |
| VT-4 | 5.15 | 4.80 | 24.4 | 2#4 + 2#4 |

## 3.3 Vigas de carga (VC 40×30)
Solicitaciones de la envolvente SAP con sismo ÷ R = 5, agrupadas en 3 tipos.
**Tipo crítico VC-3** (d = 342.6 mm, Mu⁻ = 142): ρ = 0.0119 → As = 1 226 mm² → **7 #5**; φMn = 158.8 ≥ 142 ✓. Cortante Vc = 92.4, estribos #3 @ 86 mm. Torsión Tu = 20 > 3.4 → diseñar.
| Tipo | N° | M⁻ | Acero sup | Acero inf | Estribos |
|---|---|---|---|---|---|
| VC-1 | 148 | ≤80 | 4 #5 | 3 #5 | #3 @86/150 |
| VC-2 | 120 | ≤120 | 6 #5 | 5 #5 | #3 @86/150 |
| VC-3 | 12 | ≤142 | 7 #5 | 4 #5 | #3 @86/150 |

## 3.4 Riostras / vigas de rigidez (VR 40×35)
**Tipo crítico VR-4** (d = 342.6, Mu⁻ = 250): ρ = 0.020 → As = 2 330 → **12 #5**; φMn = 254.9 ≥ 250 ✓. Vu = 202, estribos #3 @ 85 mm; torsión Tu = 26 > 4.3 → diseñar. (Puede usarse #6/#7 para reducir el número de barras.)
| Tipo | N° | M⁻ | Acero sup | Acero inf | Estribos |
|---|---|---|---|---|---|
| VR-1 | 170 | ≤100 | 5 #5 | 4 #5 | #3 @85/150 |
| VR-2 | 120 | ≤140 | 6 #5 | 5 #5 | #3 @85/150 |
| VR-3 | 6 | ≤200 | 9 #5 | 6 #5 | #3 @85/150 |
| VR-4 | 14 | ≤250 | 12 #5 | 6 #5 | #3 @85/150 |

## 3.5 Despiece (planos DXF)
`Despiece-Viguetas.dxf`, `Despiece-Vigas-VC.dxf`, `Despiece-Riostras-VR.dxf` — elevación (acero corrido + bastones L/4+ld), estribos con confinamiento (2h), sección transversal y notas.

---

# 4. RESUMEN DE CORRECCIONES RESPECTO A LA MEMORIA ENTREGADA
| Ítem | Antes | Corregido |
|---|---|---|
| Coeficiente R | no definido (0.00) | **DMO, R₀=5, Ω₀=3, R=5** |
| Peso total W | 31 813 kN | **41 074 kN** |
| Cortante basal Vs | 11 718 kN | **15 129 kN** |
| Irregularidades | ausentes | **φp=φa=φr=1.0** (análisis completo) |
| Diseño de elementos | ausente | **viguetas + vigas + riostras** |

> Verificar las dimensiones reales b×h de las secciones en el modelo SAP y confirmar el sistema DMO con el grupo antes de la entrega final.

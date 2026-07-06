# SOLUCIONARIO PARCIAL — DISEÑO ESTRUCTURAL EN CONCRETO REFORZADO
### Ejemplos resueltos de las diapositivas (NSR-10 / ACI 318)
**Temas:** Columnas · Provisiones sísmicas · Escaleras · Zapatas · Vigas de amarre

> Este documento resuelve **los ejemplos de las diapositivas** (13-Columnas, 14-Provisiones
> sísmicas, 15-Escaleras, 16-Zapatas, 17-Vigas de amarre), paso a paso y con la teoría
> necesaria para entender *por qué* se hace cada cosa. No incluye el proyecto de Santa Marta.

---

## 0. Repaso rápido de datos que usarás siempre

**Áreas de las barras (NSR-10, sistema "número = octavos de pulgada"):**

| Barra | Ø (mm) | Área (mm²) |
|------|--------|-----------|
| #3 | 9.5 | 71 |
| #4 | 12.7 | 129 |
| #5 | 15.9 | 199 |
| #6 | 19.1 | 284 |
| #7 | 22.2 | 387 |
| #8 | 25.4 | 510 |

**Factores de reducción de resistencia φ (ACI/NSR-10):**
- Flexión / tracción controlada: **φ = 0.90**
- Compresión (columna con estribos): **φ = 0.65**
- Compresión (columna con espiral): **φ = 0.75**
- Cortante: **φ = 0.75**

**Constantes:** εcu = 0.003 (deformación última del concreto) · Es = 200 000 MPa ·
εy = fy/Es = 420/200000 = **0.0021** · β1 = 0.85 (para f'c ≤ 28 MPa).

**Combinaciones de carga mayorada más usadas:** `1.2D + 1.6L` (gravedad) y las que incluyen sismo `1.2D + 1.0E + 1.0L`.

---


# 1. COLUMNAS

## 1.1 Teoría esencial (lo que preguntan en el parcial)

**Clasificación**
- **Columna corta:** falla por resistencia del material (aplastamiento del concreto / fluencia del acero). Poca deformación por flexión.
- **Columna esbelta (larga):** las deformaciones por flexión crecen y aparecen **momentos de segundo orden** (P·δ y P·Δ) que hay que amplificar.

**Comportamiento del material**
- El **concreto** no aporta a tracción (se fisura con deformaciones muy pequeñas). Toda la tracción la toma el acero: `Fs = As·fy`.
- A **compresión** el concreto alcanza su máximo cerca de ε=0.002 y se agota en ε=0.003. Bloque equivalente de Whitney: esfuerzo `0.85f'c` sobre profundidad `a = β1·c`.
- Se debe **confinar** con estribos o espirales para evitar el pandeo de las barras longitudinales cuando el concreto se deteriora.

**Resistencia nominal a carga axial pura (compresión):**
```
Po = 0.85·f'c·(Ag − Ast) + fy·Ast
```
- `0.85f'c(Ag−Ast)` = aporte del concreto (se descuenta el área ocupada por el acero).
- `fy·Ast` = aporte de todas las barras trabajando en fluencia a compresión.

El código **limita** la carga axial máxima (por excentricidad accidental):
- Estribos: `Pn,max = 0.80·Po` → `φPn,max = 0.65·0.80·Po`
- Espirales: `Pn,max = 0.85·Po` → `φPn,max = 0.75·0.85·Po`

---

## 1.2 EJEMPLO 1 — Máxima fuerza axial (diapositiva 15)

> **Enunciado:** Calcular la máxima fuerza axial que se puede aplicar a la columna de la
> figura. Sección **500 × 400 mm**, refuerzo **3#8 + 3#8 + 4#7**, `f'c = 21 MPa`, `fy = 420 MPa`.

**Paso 1 — Áreas.**
```
Ag  = 500 × 400 = 200 000 mm²
Ast = 6(#8) + 4(#7) = 6(510) + 4(387) = 3060 + 1548 = 4608 mm²
ρ   = Ast/Ag = 4608/200000 = 2.30 %   (entre 1% y 4% → OK NSR C.21)
```
> Nota: "3#8 arriba + 3#8 abajo" = 6 barras #8; "4#7" = 2 barras #7 en cada cara lateral.

**Paso 2 — Resistencia axial nominal Po.**
```
Po = 0.85·f'c·(Ag − Ast) + fy·Ast
Po = 0.85(21)(200000 − 4608) + 420(4608)
Po = 17.85 × 195392 + 1 935 360
Po = 3 487 747 + 1 935 360 = 5 423 107 N
```
> **Po = 5 423 kN**  (resistencia nominal a compresión pura, sin reducir)

**Paso 3 — Máximo admisible por norma (estribos).**
```
Pn,max  = 0.80·Po = 0.80(5423) = 4 338 kN
φPn,max = 0.65·Pn,max = 0.65(4338) = 2 820 kN
```

**RESULTADO**

| Cantidad | Valor |
|---|---|
| Nominal pura `Po` | **5 423 kN** |
| Nominal máx. `Pn,max = 0.80Po` | **4 338 kN** |
| **De diseño `φPn,max`** | **≈ 2 820 kN** |

> **Interpretación:** aunque el material "aguanta" 5 423 kN, la carga axial **de diseño**
> que puedes aplicar (con φ y el tope del 0.80) es **2 820 kN**.

---

## 1.3 EJEMPLO 2 — Diagrama de interacción (diapositiva 23)

> **Enunciado:** Construir el diagrama de interacción P–M de la MISMA columna (500×400,
> 3#8+3#8+4#7, f'c=21, fy=420), flexión sobre el eje fuerte (h = 500 mm).

**Idea:** el diagrama es la "frontera de falla". Para cada posición del eje neutro `c` se
calcula una pareja (Pn, Mn). Se recorren desde compresión pura hasta tracción pura.

**Geometría de capas (medidas desde la fibra comprimida), recubrimiento al centroide ≈ 65 mm:**
- Capa 1 (superior): 3#8 = 1530 mm² @ d = 65 mm
- Capa 2 (media): 4#7 = 774 mm² (2 por cara) @ d = 250 mm
- Capa 3 (inferior): 3#8 = 1530 mm² @ d = 435 mm

**Procedimiento para cada `c`:**
1. `a = β1·c`, fuerza del concreto `Cc = 0.85·f'c·a·b`.
2. Deformación de cada capa por triángulos: `εsi = 0.003·(c − di)/c`.
3. Esfuerzo `fsi = Es·εsi`, limitado a ±fy. (Si la barra está dentro del bloque a compresión, se descuenta `0.85f'c`.)
4. `Pn = Cc + ΣFsi` ; `Mn = Cc·(h/2 − a/2) + ΣFsi·(h/2 − di)` (momentos respecto al centro).

**Puntos calculados:**

| Condición | c (mm) | Pn (kN) | Mn (kN·m) |
|---|---|---|---|
| Compresión pura | ∞ | 5 423 | 0 |
| — | 600 | 4 925 | 72 |
| — | 500 | 4 206 | 206 |
| — | 400 | 3 283 | 323 |
| — | 346 | 2 709 | 374 |
| — | 300 | 2 150 | 413 |
| **Balanceado** | **256** | **1 547** | **452** ← Mn máx |
| — | 200 | 931 | 429 |
| — | 150 | 141 | 380 |
| **Flexión pura** | **138** | **0** | **363.5** |
| Tracción pura | — | −1 935 | 0 |

**Puntos notables (para memorizar el "mapa"):**
- **Compresión pura:** `Po = 5 423 kN`.
- **Punto balanceado** (`c_b`): el acero en tracción fluye justo cuando el concreto llega a 0.003.
  ```
  c_b = εcu/(εcu+εy) · d = 0.003/(0.003+0.0021) × 435 = 256 mm
  → Pb = 1 547 kN ,  Mb = 452 kN·m  (momento máximo del diagrama)
  ```
- **Flexión pura** (P = 0): `Mn = 363.5 kN·m` → `φMn = 0.90 × 363.5 = 327 kN·m`.
- **Tracción pura:** `Pnt = −As·fy = −4608 × 420 = −1 935 kN` → `φ = 0.90 → −1 742 kN`.

**Cómo se usa:** una pareja de diseño (Pu, Mu) es segura si cae **dentro** de la curva φPn–φMn.
Por encima del punto balanceado la falla es frágil (controla compresión, φ=0.65); por debajo
es dúctil (controla tracción, φ tiende a 0.90). La transición se hace con la deformación εt.

```
P(kN)
5423 *  ← compresión pura (Po)
     |\
4338 |  (tope 0.80Po)
     |    \
     |      *  (256, 1547) ← BALANCEADO, Mn máx=452
     |     /
     |   /
  0  |_/______*___ M(kN·m)
     |       363.5 ← flexión pura
-1935*  ← tracción pura
```


---

## 1.4 Flexión biaxial — ecuaciones de Bresler

Cuando hay momento en las dos direcciones (Mx y My) se usan las **ecuaciones de Bresler**,
que aproximan la superficie de interacción 3D:

**Carga recíproca (la más usada):**
```
1/Pn ≈ 1/Pnx + 1/Pny − 1/Po
```
donde `Pnx`, `Pny` = capacidad axial con la excentricidad en X y en Y por separado, y `Po` = axial pura.

**Contorno de carga:**
```
(Mnx/Mnbx)^α + (Mny/Mnby)^α ≤ 1     (con α ≈ 1.15–1.5)
```
> El método recíproco **no es válido** cuando `Pn < Pb` (por debajo del balanceado); ahí se usa el de contorno.

---

## 1.5 EJEMPLO 3 — Longitud efectiva y esbeltez (diapositiva 40)

> **Enunciado:** Calcular el factor de longitud efectiva `k` y la longitud efectiva de la
> columna central, en 1° y 2° piso. Vigas **30×40**, Columnas **40×60**, alturas de piso
> **3.50 m (N1)** y **3.00 m (N2)**, luces de vigas **7.00 / 8.00 / 6.00 m**. Determinar si es esbelta.

**Paso 1 — Inercias brutas.**
```
Columna 40×60:  Ic = 0.40 × 0.60³/12 = 0.00720 m⁴
Viga 30×40:     Ib = 0.30 × 0.40³/12 = 0.00160 m⁴
```

**Paso 2 — Coeficientes ψ (psi) en cada extremo (Jackson–Moreland).**
```
ψ = Σ(EI/L)_columnas  /  Σ(EI/L)_vigas
```
En el **nudo superior** de la columna del 1° piso concurren la columna de abajo (3.50 m) y
la de arriba (3.00 m), y **dos vigas** (tomo las luces 8.0 y 6.0 m que llegan a ese nudo):
```
Σ(Ic/Lc) = 0.0072/3.50 + 0.0072/3.00 = 0.002057 + 0.002400 = 0.004457
Σ(Ib/Lb) = 0.0016/8.00 + 0.0016/6.00 = 0.000200 + 0.000267 = 0.000467
ψ_sup = 0.004457 / 0.000467 = 9.55
```
En la **base** (empotrada en la cimentación) se recomienda `ψ_inf = 1.0`
(no se usa 0 porque no existe el empotramiento perfecto).

**Paso 3 — Factor k (ábaco de alineamiento / fórmulas aproximadas).**
```
Pórtico NO arriostrado (con desplazamiento lateral):  k ≈ 2.25
Pórtico    arriostrado (sin desplazamiento lateral):  k ≈ 0.86
```
> **Regla clave:** en pórticos **no arriostrados** k > 1 (siempre); en **arriostrados** k ≤ 1.

**Paso 4 — Radio de giro y esbeltez.**
```
Lu (1° piso) = 3.50 − 0.40 (peralte viga) = 3.10 m
r = 0.30·h = 0.30 × 0.60 = 0.18 m
```

| Caso | k·Lu/r | Límite NSR C.10.10.1 | ¿Esbelta? |
|---|---|---|---|
| **No arriostrado** | 2.25×3.10/0.18 = **38.8** | > **22** | **SÍ, esbelta** |
| Arriostrado | 0.86×3.10/0.18 = **14.9** | 34 − 12(M1/M2) ≈ 34 | No (corta) |

**Conclusión:** si el pórtico **no está arriostrado** (lo habitual en un pórtico resistente a
momento), `kLu/r = 38.8 > 22` ⇒ **la columna es esbelta** y hay que **magnificar momentos**
(efectos de segundo orden). Si estuviera arriostrado, sería corta.

> ⚠️ Los valores de ψ dependen de **cuáles vigas** llegan al nudo central (según la figura del
> examen). El **método** es siempre el mismo: inercias → ψ en cada extremo → k del ábaco →
> comparar kLu/r con el límite. Cambia solo qué luces `Lb` entran en la suma.

**Recordatorio de esbeltez (NSR-10 C.10.10.1):**
- **Sin** desplazamiento lateral (arriostrada): corta si `kLu/r ≤ 34 − 12(M1/M2) ≤ 40`.
- **Con** desplazamiento lateral (no arriostrada): corta si `kLu/r ≤ 22`.
- `M1/M2` es (+) en curvatura simple y (−) en curvatura doble.

---

## 1.6 Efectos de segundo orden — magnificación de momentos

- **Efecto P-δ** (local, entre extremos de la columna): domina en pórticos **arriostrados**.
- **Efecto P-Δ** (global, desplazamiento del piso): domina en pórticos **no arriostrados**.

**Sin desplazamiento lateral (C.10.10.6):**
```
Mc = δns·M2      con   δns = Cm / (1 − Pu/(0.75·Pc)) ≥ 1
Pc = π²·EI / (k·Lu)²        (carga crítica de Euler)
Cm = 0.6 + 0.4·(M1/M2)      (para columnas sin carga transversal)
```
**Con desplazamiento lateral (C.10.10.7):**
```
M1 = M1ns + δs·M1s   ;   M2 = M2ns + δs·M2s
δs = 1 / (1 − ΣPu/(0.75·ΣPc)) ≥ 1
```
> **Tope de la norma:** los momentos totales (2° orden) no deben superar **1.4 veces** los de
> primer orden. Si `δs > 1.5`, hay que hacer análisis de 2° orden real.

---


# 2. PROVISIONES SÍSMICAS PARA COLUMNAS (NSR-10 Capítulo C.21)

Estas reglas garantizan **ductilidad**: que la columna se deforme sin colapsar durante el sismo.
Hay dos niveles de capacidad de disipación de energía:

| Requisito | **DMO** (moderada, C.21.3.5) | **DES** (especial, C.21.6) |
|---|---|---|
| Dimensión mínima | ≥ 250 mm | ≥ 300 mm |
| Área mínima (col. T,C,I) | ≥ 0.0625 m² | ≥ 0.09 m² |
| Relación lados b/h | — | ≥ 0.35 / 0.25 / 0.20 según tamaño |
| Cuantía longitudinal Ast | 0.01·Ag ≤ Ast ≤ 0.04·Ag | igual (mín. 6 barras si es circular) |
| Empalmes | solo en la **mitad central**, como empalme a tracción | igual |

## 2.1 Confinamiento — separación y longitud de estribos

**Longitud de confinamiento `ℓo` (desde la cara del nudo):**
- **DMO:** el mayor de → `Lu/6`, mayor dimensión de la sección, `500 mm`.
- **DES:** el mayor de → altura del elemento, `Lu/6`, `450 mm`.

**Separación `so` en la zona confinada (DMO, C.21.3.5.6):** el **menor** de:
- 8 × Ø barra longitudinal menor
- 16 × Ø estribo
- ⅓ de la menor dimensión de la columna
- 150 mm

**Alternativa DMO (C.21.3.5.9):** estribos #3 @ **100 mm** (válido si f'c ≤ 35 MPa).

> **Fuera de `ℓo`:** la separación puede ser hasta **2·so** (C.21.3.5.11).
> El primer estribo va a **so/2** de la cara del nudo.

### Ejemplo aplicado (columna del Ejemplo 1: 500×400, long. #7, estribos #3, DMO)
```
so ≤ menor de:
   8 × 22.2 (Ø#7)   = 177.6 mm
   16 × 9.5 (Ø#3)   = 152.0 mm
   (1/3)×400        = 133.3 mm   ← GOBIERNA
   150 mm
→ so ≈ 130 mm   (o usar la alternativa: #3 @ 100 mm)

ℓo ≥ mayor de:
   Lu/6 = 2600/6 = 433 mm
   mayor dim = 500 mm            ← GOBIERNA
   500 mm
→ ℓo = 500 mm  en cada extremo
```

## 2.2 Área de refuerzo transversal de confinamiento `Ash`

Se debe cumplir **simultáneamente** (C.21-7 y C.21-8, forma general DES):
```
Ash ≥ 0.3·(s·bc·f'c/fyt)·(Ag/Ach − 1)
Ash ≥ 0.09·(s·bc·f'c/fyt)
```
- `bc` = dimensión del núcleo confinado (centro a centro de estribos perimetrales).
- `Ach` = área del núcleo confinado (medido al exterior del estribo).

### Ejemplo (misma columna, s = 100 mm, recubrimiento 40 mm, dirección bc = 420 mm)
```
Ach = (400−2·40)(500−2·40) = 320 × 420 = 134 400 mm²
Ag/Ach = 200000/134400 = 1.488

(C.21-8): Ash = 0.09 × 100 × 420 × 21/420 = 189 mm²
(C.21-7): Ash = 0.3 × 100 × 420 × (1.488−1) × 21/420 = 307 mm²  ← GOBIERNA
```
→ Se necesitan **≈ 307 mm²** de ramas de estribo en 100 mm.
Con estribo #4 (129 mm²): `307/129 = 2.4` ⇒ **3 ramas de #4** en esa dirección
(estribo perimetral + 1 gancho suplementario). Con #3 harían falta ~4–5 ramas.

## 2.3 Columna fuerte – viga débil (C.21.6.2 / C.21-4)

El objetivo es que **las rótulas plásticas se formen en las vigas, no en las columnas**
(para no perder la estabilidad vertical). En cada nudo:
```
ΣMnc ≥ (6/5)·ΣMnb        →   ΣMnc / ΣMnb ≥ 1.2
```
- `ΣMnc` = suma de momentos nominales de las **columnas** que llegan al nudo (arriba y abajo),
  calculados con la carga axial que da el **menor** valor.
- `ΣMnb` = suma de momentos nominales de las **vigas** que llegan al nudo.

> Si **no** se cumple, esa columna no puede contarse en la resistencia lateral del sistema.

## 2.4 Cortante de diseño por capacidad (C.21.3.3 / C.21.5)

El cortante NO se toma del análisis, sino de la **capacidad a flexión** de la columna (diseño
por capacidad), para asegurar que **falle a flexión (dúctil) y no a cortante (frágil)**:
```
Ve = (Mpr,sup + Mpr,inf) / Lu
```
- `Mpr` = momento probable, calculado con **1.25·fy** (sobre-resistencia del acero) y φ = 1.0.
- El aporte del concreto `Vc` se **desprecia** (Vc = 0) si el sismo produce ≥ 50% del cortante
  y la carga axial es baja (`Pu < Ag·f'c/20`).

**Diseño de estribos por cortante:**
```
φVn = φ(Vc + Vs) ≥ Ve      con   Vs = Av·fyt·d/s
```

---


# 3. ESCALERAS (NSR-10 Título K + diseño como losa)

## 3.1 Teoría

- Una escalera se comporta como una **losa maciza unidireccional** apoyada en sus extremos
  (descansos o vigas). Se diseña por **metro de ancho**.
- **Predimensionamiento del espesor:** `e ≈ L/20` (L = luz total del tramo, incluyendo descansos si no hay apoyo intermedio).
- Requisitos geométricos (Título K):
  - Huella `H ≥ 280 mm`; Contrahuella `100 ≤ CH ≤ 180 mm`.
  - **Regla de comodidad:** `600 ≤ 2·CH + H ≤ 640 mm`.
  - Ancho mínimo vivienda ≥ 0.90 m (interior ≥ 0.75 m).

## 3.2 EJEMPLO — Escalera de un tramo (método de las diapositivas 8–10)

> Datos típicos del ejemplo: CH = 0.175 m, H = 0.28 m, luz L ≈ 4.0 m, `f'c=21`, `fy=420`,
> carga viva de escalera residencial `L = 3.0 kN/m²`.

**Paso 1 — Verificar geometría.**
```
2·CH + H = 2(175) + 280 = 630 mm   → dentro de 600–640 ✔
Ángulo de inclinación α = atan(CH/H) = atan(0.175/0.28) = 32.0°
```

**Paso 2 — Espesor.**
```
e = L/20 = 4.0/20 = 0.20 m  → adopto e = 0.20 m
```

**Paso 3 — Cargas (por m² en planta).** Peso específico concreto γc = 24 kN/m³.

*Tramo inclinado:*
```
Losa (proyectada): γc·e/cos α = 24·0.20/cos32° = 5.66 kN/m²
Peso de escalones:  γc·CH/2   = 24·0.175/2      = 2.10 kN/m²
Acabados:                                        ≈ 1.50 kN/m²
D_incl = 5.66 + 2.10 + 1.50 = 9.26 kN/m²
```
*Tramo del descanso:*
```
D_desc = γc·e + acabados = 24·0.20 + 1.50 = 6.30 kN/m²
```

**Paso 4 — Cargas mayoradas (`wu = 1.2D + 1.6L`, franja de 1 m):**
```
wu(inclinado) = 1.2(9.26) + 1.6(3.0) = 15.9 kN/m
wu(descanso)  = 1.2(6.30) + 1.6(3.0) = 12.4 kN/m
```

**Paso 5 — Momento (simplemente apoyada, se toma la wu mayor):**
```
Mu = wu·L²/8 = 15.9 × 4.0²/8 = 31.8 kN·m/m
```

**Paso 6 — Acero principal (d = e − 0.03 = 0.17 m):**
```
Rn = Mu/(φ·b·d²) = 31.8e6/(0.9·1000·170²) = 1.22 MPa
ρ  = (0.85f'c/fy)[1 − √(1 − 2Rn/0.85f'c)] = 0.00302
As = ρ·b·d = 0.00302·1000·170 = 514 mm²/m
```
→ **#4 @ 250 mm** (129/514×1000 ≈ 251 mm) como refuerzo principal (a lo largo del tramo).

**Paso 7 — Acero de repartición / temperatura (transversal):**
```
As,temp = 0.0018·b·e = 0.0018·1000·200 = 360 mm²/m  → #4 @ 350 mm
```

> **Resumen:** e = 0.20 m · principal **#4 @ 250 mm** (cara inferior en el vano, cara superior
> en los apoyos) · repartición **#4 @ 350 mm**. El refuerzo negativo se coloca en el quiebre
> entre descanso y tramo inclinado (donde el momento tira de la cara superior).

---

# 4. ZAPATAS (NSR-10 C.15 / ACI)

## 4.1 Teoría — los 3 chequeos

1. **Dimensionamiento (área en planta):** con cargas de **servicio** (sin mayorar) y la
   capacidad **admisible** del suelo:  `A = P_servicio / σadm`.
2. **Diseño (h y acero):** con cargas **mayoradas** y la presión neta `qu = Pu/A`.
   - **Cortante en dos direcciones (punzonamiento):** sección crítica a **d/2** de la cara de la
     columna. Suele **gobernar el espesor h**.
     ```
     φVc = φ·(menor de) :
        0.33·λ·√f'c·bo·d
        0.17·(1 + 2/β)·λ·√f'c·bo·d          (β = lado largo/corto de la columna)
        0.083·(αs·d/bo + 2)·λ·√f'c·bo·d      (αs = 40 interior, 30 borde, 20 esquina)
     bo = perímetro crítico = 4(c + d) para columna cuadrada
     ```
   - **Cortante en una dirección (como viga):** sección crítica a **d** de la cara.
     `φVc = φ·0.17·λ·√f'c·b·d`.
   - **Flexión:** momento en la **cara de la columna**, `Mu = qu·B·(volado)²/2`.

## 4.2 EJEMPLO — Zapata cuadrada (diapositiva 10)

> Columna **0.40×0.40**, `PD=1700 kN`, `PL=500 kN`, `σadm=180 kN/m²`, `f'c=21`, `fy=420`.

**Paso 1 — Área y lado.**
```
P_servicio = 1700 + 500 = 2200 kN
A = 2200/180 = 12.22 m²  →  B = √12.22 = 3.50 m   → adopto B = 3.50 m (A = 12.25 m²)
```

**Paso 2 — Presión última.**
```
Pu = 1.2(1700) + 1.6(500) = 2040 + 800 = 2840 kN
qu = Pu/B² = 2840/12.25 = 231.8 kN/m²
```

**Paso 3 — Espesor por punzonamiento** (probando alturas):

| h (m) | d (m) | Punzonamiento Vu / φVc (kN) | ¿OK? |
|---|---|---|---|
| 0.60 | 0.51 | 2648 / 2106 | NO |
| 0.65 | 0.56 | 2626 / 2439 | NO |
| **0.70** | **0.61** | **2604 / 2795** | **SÍ** ✔ |

```
bo = 4(c+d) = 4(0.40+0.61) = 4.04 m
Vu = Pu − qu·(c+d)² = 2840 − 231.8·(1.01)² = 2604 kN
φVc = 0.75·0.33·√21·(4040)·(610)/1000 = 2795 kN  > Vu ✔
```
→ **h = 0.70 m** (d ≈ 0.61 m). El cortante en una dirección da holgado (Vu1=763 < φVc1=1247).

**Paso 4 — Flexión (volado = (3.50−0.40)/2 = 1.55 m):**
```
Mu = qu·B·volado²/2 = 231.8·3.50·1.55²/2 = 975 kN·m
Rn = Mu/(φ·b·d²) = 975e6/(0.9·3500·610²) = 0.83 MPa
ρ  = 0.00203  →  As = ρ·b·d = 0.00203·3500·610 = 4328 mm²
As,min = 0.0018·b·h = 0.0018·3500·700 = 4410 mm²  ← GOBIERNA
```
→ **As = 4410 mm² ⇒ 16 #6 (16×284 = 4544 mm²)** en cada dirección (parrilla).

> **Resumen:** zapata **3.50 × 3.50 × 0.70 m**, refuerzo **16 #6 @ ~22 cm en ambas direcciones**.

## 4.3 EJEMPLO — Zapata rectangular de voladizos iguales (diapositiva 17)

> Columna **0.30×1.20**, `PD=1800`, `PL=600`, `σadm=220 kN/m²`, peso propio `Wpp=10%·P`.

**Paso 1 — Área (incluyendo peso propio).**
```
P_servicio = 1800 + 600 = 2400 kN ;  con Wpp:  2400×1.10 = 2640 kN
A = 2640/220 = 12.0 m²
```

**Paso 2 — Dimensiones con voladizos iguales.** Para que los voladizos sean iguales en ambas
direcciones: `L − 1.20 = B − 0.30` ⇒ `L = B + 0.90`.
```
B·(B+0.90) = 12.0  →  B² + 0.9B − 12 = 0  →  B = 3.04 m
L = 3.94 m   → adopto B = 3.05 m , L = 3.95 m (A = 12.05 m²)
Voladizo = (3.05−0.30)/2 = (3.95−1.20)/2 = 1.38 m  (igual en las dos direcciones ✔)
```

**Paso 3 — Presión última.**
```
Pu = 1.2(1800)+1.6(600) = 3120 kN ;  qu = 3120/(3.05·3.95) = 259 kN/m²
```

**Paso 4 — Flexión en cada dirección** (h = 0.70 m, d = 0.61 m):
```
Dir. larga  (franja B): Mu = qu·B·vol²/2 = 259·3.05·1.38²/2 = 747 kN·m → As ≈ 3843 (mín) → 14 #6
Dir. corta  (franja L): Mu = qu·L·vol²/2 = 259·3.95·1.38²/2 = 967 kN·m → As ≈ 4977 (mín) → 18 #6
```
**Distribución en la dirección corta:** una fracción del refuerzo se concentra en la banda
central de ancho B:
```
fracción = 2/(β+1),  β = L/B = 3.95/3.05 = 1.30  →  2/2.30 = 0.87
```
→ el 87 % de las barras de la dirección corta van en la franja central de ancho B, el resto se reparte a los lados.

## 4.4 EJEMPLO — Zapata excéntrica con viga de contrapeso (diapositiva 26)

> Columna **0.40×0.50** (0.50 en dirección de la excentricidad), `σadm=200 kN/m²`,
> `PD=400`, `PL=120`, `Wpp=10%`, `C=6.0 m` (distancia al centro de la columna interior).

**El problema:** la columna está en el **borde** (lindero), así que no puede quedar centrada
en su zapata → la reacción del suelo sería **trapezoidal** (no uniforme). **Solución:** una
**viga de contrapeso (strap beam)** que une esta zapata con la de la columna interior; esa
viga "presta rigidez" y logra que la presión bajo la zapata excéntrica sea **uniforme**.

**Paso 1 — Área y dimensiones.**
```
P_servicio = 400 + 120 = 520 kN ;  con Wpp: 572 kN
A = 572/200 = 2.86 m²  →  supongo B = 2.0 m  →  L = 2.86/2.0 = 1.43 m → adopto L = 1.50 m
```

**Paso 2 — Excentricidad de la columna respecto al centro de la zapata.**
```
e = L/2 − a/2 = 1.50/2 − 0.50/2 = 0.50 m   (la columna queda al borde)
```

**Paso 3 — Presión última (uniforme, gracias al contrapeso).**
```
Pu = 1.2(400)+1.6(120) = 672 kN ;  qu = Pu/(B·L) = 672/(2.0·1.50) = 224 kN/m²  ≈ uniforme
```

**Paso 4 — Estática de la viga de contrapeso.** La viga transfiere el momento de la
excentricidad hacia la columna interior. Las reacciones bajo cada zapata resultan:
```
R1 (zapata excéntrica) = P1 · C/(C − e)
R2 (zapata interior)   = P2 − P1·e/(C − e)
```
Con esto se **redistribuye la carga**: la zapata excéntrica recibe algo más y la interior algo
menos, pero la presión bajo cada una queda **uniforme**. La viga se diseña a flexión para el
momento `M ≈ P1·e` y a cortante, con estribos en toda su longitud.

> **Idea clave para el examen:** *zapata excéntrica sola* → presión trapezoidal (limitada);
> *con viga de contrapeso* → presión uniforme y diseño mucho más eficiente.

---


# 5. VIGAS DE AMARRE (NSR-10 C.15.13 + A.3.6.4.2)

## 5.1 ¿Para qué sirven? (6 criterios de diseño de las diapositivas)

1. **Amarre sísmico** entre zapatas (evita que se muevan independientemente).
2. **Control de asentamientos diferenciales** (rigidizan la cimentación).
3. **Reacción del terreno** bajo la propia viga.
4. **Cargas aplicadas directamente** sobre la viga (escaleras, rampas, muros, columnas secundarias).
5. **Momentos de empotramiento** transmitidos por las columnas (muchas veces se prefiere que los
   tomen las vigas de amarre y no las zapatas).
6. Otras condiciones particulares.

## 5.2 Requisitos geométricos y de refuerzo (C.15.13)

- **Peralte mínimo** según capacidad de disipación:
  `h ≥ L/20 (DES)` · `L/30 (DMO)` · `L/40 (DMI)`.
- **Refuerzo longitudinal continuo**, capaz de desarrollar `fy` por anclaje en la columna exterior.
- **Estribos cerrados** en toda la longitud, separación `s ≤ menor(½·menor dimensión, 300 mm)`.

## 5.3 EJEMPLO — Amarre sísmico (diapositiva 4)

> Viga de amarre **0.50 × 0.70 m** que conecta dos columnas con cargas verticales mayoradas
> de **4000 kN** y **5200 kN**. `Aa = 0.15`. Diseñar el refuerzo por amarre sísmico.

**Requisito A.3.6.4.2:** la viga debe resistir, en tracción o compresión, una fuerza no menor a:
```
T = 0.25 · Aa · P_mayor = 0.25 · 0.15 · 5200 = 195 kN
```
(se toma la **mayor** de las dos cargas de columna que interconecta = 5200 kN)

**Acero para esa fuerza de tracción (φ = 0.90):**
```
As = T/(φ·fy) = 195 000/(0.90·420) = 516 mm²
```
→ Bastarían **3 #5 (597 mm²)** por el requisito estricto de amarre.

> ⚠️ **Nota sobre el "Total: 2013 mm²" de la diapositiva:** ese valor (≈ **4 #8 = 2040 mm²**) es
> **mayor** que los 516 mm² del requisito de amarre. Corresponde a que, además del amarre, la
> viga se detalla con un **refuerzo longitudinal mínimo** para rigidez / control de asentamientos
> y para tomar momentos de las columnas (criterios 2 y 5). Es decir: el amarre sísmico exige
> 516 mm², pero **por detalle y funcionamiento real** el profesor adopta ≈ 2013 mm² (4#8).
> Verifica en clase cuál criterio pide el enunciado del parcial; el **procedimiento normativo**
> del amarre es `0.25·Aa·P → As = T/(φ·fy)`.

**Detallado del refuerzo transversal:**
```
s ≤ menor( ½·menor dim, 300 mm ) = menor( 0.5·500, 300 ) = 250 mm
→ estribos #3 @ 250 mm en toda la longitud
```

---

# 6. FORMULARIO RESUMEN (para llevar al parcial)

**Columnas**
```
Po = 0.85f'c(Ag−Ast) + fy·Ast
Pn,max = 0.80Po (estribos) | 0.85Po (espiral)
φ = 0.65 (estribos) | 0.75 (espiral) para compresión; 0.90 flexión
c_balanceado = εcu/(εcu+εy)·d ;  εy = fy/Es = 0.0021
Bresler: 1/Pn = 1/Pnx + 1/Pny − 1/Po
Esbeltez: r = 0.3h (rect.) ; ψ = Σ(EI/L)col / Σ(EI/L)viga
   corta si:  kLu/r ≤ 34−12(M1/M2)  (arriostrado)  |  ≤ 22 (no arriostrado)
δns = Cm/(1 − Pu/0.75Pc) ;  Pc = π²EI/(kLu)²
```
**Provisiones sísmicas (C.21)**
```
DMO: dim ≥ 250mm ; DES: dim ≥ 300mm ;  0.01Ag ≤ Ast ≤ 0.04Ag
so = menor(8dbL, 16dbE, dim/3, 150mm)  |  ℓo = mayor(Lu/6, dim mayor, 500mm[DMO]/450[DES])
Ash ≥ 0.3(s·bc·f'c/fyt)(Ag/Ach−1)  y  ≥ 0.09(s·bc·f'c/fyt)
Columna fuerte-viga débil: ΣMnc ≥ (6/5)ΣMnb
Cortante capacidad: Ve = (Mpr,sup+Mpr,inf)/Lu ; Mpr con 1.25fy
```
**Escaleras**
```
e ≈ L/20 ;  600 ≤ 2CH+H ≤ 640 mm ;  wu=1.2D+1.6L ;  Mu=wuL²/8
As,temp = 0.0018·b·e
```
**Zapatas**
```
Dimensionar (servicio): A = P/σadm
Diseñar (mayorado): qu = Pu/A
Punzonamiento (a d/2): φVc = φ0.33√f'c·bo·d ; bo=4(c+d)   ← suele fijar h
Cortante viga (a d):   φVc = φ0.17√f'c·b·d
Flexión (cara col):    Mu = qu·B·volado²/2 ;  As,min = 0.0018·b·h
Banda central (rect.): fracción = 2/(β+1) , β=L/B
```
**Vigas de amarre**
```
Amarre sísmico: T = 0.25·Aa·P_mayor ;  As = T/(φ·fy)
h ≥ L/20(DES) | L/30(DMO) | L/40(DMI)
Estribos: s ≤ menor(½·dim menor, 300mm)
```

---

### Tabla maestra de resultados de los ejemplos

| Ejemplo | Resultado principal |
|---|---|
| Col. capacidad axial | Po=5423 kN · Pn,max=4338 kN · **φPn,max=2820 kN** |
| Col. diagrama interacción | Balanceado (1547 kN, 452 kN·m) · Flexión pura φMn=327 kN·m · Tracción −1742 kN |
| Col. esbeltez | ψsup=9.55, ψinf=1.0 · k=2.25(no arr.)/0.86(arr.) · **kLu/r=38.8 → esbelta** |
| Zapata cuadrada | **3.50×3.50×0.70 m** · 16#6 c/dirección (punzonamiento gobierna h) |
| Zapata rectangular | **3.05×3.95×0.70 m** · larga 14#6, corta 18#6 (87% en banda central) |
| Zapata excéntrica | 2.0×1.50 m + viga de contrapeso · e=0.50 m · presión uniforme |
| Escalera | e=0.20 m · principal #4@250 · reparto #4@350 |
| Viga de amarre | T=195 kN → As=516 mm² (norma); detalle ≈4#8 · estribos #3@250 |

> **Nota final:** los cálculos numéricos se verificaron con scripts de Python. Los valores de
> `ψ`/`k` en la columna esbelta dependen de la figura exacta del enunciado (qué vigas llegan al
> nudo); el método mostrado es el que debes aplicar con los datos que te den.

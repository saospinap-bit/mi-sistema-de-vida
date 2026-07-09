# Guía de Estudio – Parcial de Diseño Estructural (Concreto Reforzado, NSR-10)

> Basada en las 5 presentaciones del curso (Prof. Ing. Sergio Daniel Ladino).
> Contiene la **teoría explicada** y **todos los ejercicios resueltos paso a paso**.

## Contenido
1. [Columnas](#1-columnas)
2. [Provisiones sísmicas para columnas (C.21)](#2-provisiones-sismicas-para-columnas-c21)
3. [Escaleras](#3-escaleras)
4. [Zapatas](#4-zapatas)
5. [Vigas de amarre](#5-vigas-de-amarre)
6. [Formulario rápido](#6-formulario-rapido)

---

## Datos de referencia (áreas de barras NSR-10)

| Barra | Diámetro (mm) | Área (mm²) |
|-------|--------------|-----------|
| #3 (3/8") | 9.5  | 71  |
| #4 (1/2") | 12.7 | 129 |
| #5 (5/8") | 15.9 | 199 |
| #6 (3/4") | 19.1 | 284 |
| #7 (7/8") | 22.2 | 387 |
| #8 (1")   | 25.4 | 510 |

Factores de reducción **φ**: flexión y tracción controlada = 0.90; cortante = 0.75;
columna con estribos = 0.65; columna con espiral = 0.75.

---

# 1. COLUMNAS

## 1.1 ¿Qué es una columna y cómo se clasifica?
Una columna es un elemento que trabaja principalmente a **compresión** (con o sin flexión).
Se clasifica en:

- **Columna corta:** falla por **resistencia del material** (aplastamiento del concreto +
  fluencia/pandeo del acero). Es robusta y poco flexible.
- **Columna esbelta (larga):** las deformaciones por flexión generan **momentos de segundo
  orden** (P·Δ y P·δ) que reducen su capacidad.
- **Columna sismo-resistente:** además cumple requisitos del Capítulo C.21 (ver sección 2).

## 1.2 Comportamiento a carga axial

### Tracción pura
El concreto **no aporta** (se fisura a deformaciones muy pequeñas). Toda la fuerza la toma el acero:

$$T_n = A_{st}\,f_y \qquad \phi T_n = 0.90\,A_{st}\,f_y$$

### Compresión pura
El concreto alcanza su máximo a ε≈0.002 y se considera que falla a **ε = 0.003**. Si hay
compatibilidad de deformaciones, el acero alcanza la fluencia antes de la falla. La resistencia
nominal a compresión axial pura es:

$$P_o = 0.85\,f'_c\,(A_g - A_{st}) + f_y\,A_{st}$$

- `0.85 f'c (Ag − Ast)` → aporte del concreto (Cc).
- `fy·Ast` → aporte del acero.

Como **nunca** existe compresión perfectamente axial (siempre hay una excentricidad mínima), el
código limita la carga máxima y obliga a refuerzo transversal (estribos o espiral):

$$\boxed{\phi P_{n,max} = 0.80\,\phi\,[\,0.85f'_c(A_g-A_{st})+f_yA_{st}\,]}\quad(\text{estribos, }\phi=0.65)$$

$$\phi P_{n,max} = 0.85\,\phi\,[\dots]\quad(\text{espiral, }\phi=0.75)$$

---

### ✏️ EJERCICIO 1.1 — Máxima fuerza axial (columna corta)
**Enunciado:** Calcular la máxima fuerza axial que se puede aplicar a la columna de la figura.
Sección **500 × 400 mm**; refuerzo **3#8 + 3#8 (caras de 400) + 4#7 (caras de 500)**;
`f'c = 21 MPa`, `fy = 420 MPa`.

**Paso 1 – Geometría y acero**
- `Ag = 500 × 400 = 200 000 mm²`
- Barras: 6#8 + 4#7 → `Ast = 6(510) + 4(387) = 3060 + 1548 = 4608 mm²`
- Cuantía: `ρ = 4608 / 200000 = 0.023 = 2.3 %` ✔ (entre 1 % y 4 %)

**Paso 2 – Resistencia nominal a compresión pura (Po)**
$$P_o = 0.85(21)(200000-4608) + 420(4608)$$
$$P_o = 17.85(195392) + 1\,935\,360 = 3\,487\,747 + 1\,935\,360 = 5\,423\,107\,N$$
$$\boxed{P_o \approx 5423\ kN}$$

**Paso 3 – Carga máxima de diseño (estribos)**
$$\phi P_{n,max} = 0.80(0.65)(5423) = \boxed{2820\ kN}$$

> **Interpretación:** la columna puede recibir, como máximo, una carga axial mayorada
> **Pu ≈ 2820 kN**. (La resistencia nominal pura es 5423 kN, pero el 0.80 y el φ=0.65
> reflejan la excentricidad accidental y la seguridad.)

---

## 1.3 Flexo-compresión y diagrama de interacción

Cuando actúan **carga axial + momento** simultáneamente, el modo de falla **no es único**.
Para revisar todas las combinaciones (P, M) posibles se construye el **diagrama de interacción**:
la curva que une todas las parejas (Pn, Mn) en las que la sección alcanza su resistencia.

**Casos típicos a lo largo del diagrama (de arriba hacia abajo):**
1. **Compresión pura** (P = Po, M = 0).
2. **Compresión con momento pequeño:** toda la sección a compresión.
3. **Falla por compresión:** el acero del lado de tracción no llega a fluir; falla el concreto.
4. **Punto balanceado:** el acero a tracción fluye (εs = εy) **al mismo tiempo** que el concreto
   aplasta a 0.003. Es el punto de **máximo momento** aproximado.
5. **Falla por tracción:** momento grande, axial pequeña; inicia por fluencia del acero.
6. **Flexión pura** (P = 0, M = Mn), igual que una viga.
7. **Tracción pura** (P = −T, M = 0).

**Cómo se calcula cada punto:** se fija la profundidad del eje neutro `c`, se calcula
`a = β1·c`, las deformaciones de cada capa de acero `εsi = 0.003 (c − di)/c`, sus esfuerzos
`fsi = Es·εsi ≤ fy`, y se hace equilibrio:

$$P_n = 0.85f'_c\,a\,b + \sum A_{si} f_{si} \qquad
M_n = 0.85f'_c\,a\,b\left(\tfrac{h}{2}-\tfrac{a}{2}\right) + \sum A_{si} f_{si}\left(\tfrac{h}{2}-d_i\right)$$

(Tracción negativa, compresión positiva). Luego se aplica φ que **varía** entre 0.65 (compresión)
y 0.90 (tracción controlada) según εt.

### ✏️ EJERCICIO 1.2 — Diagrama de interacción (misma columna)
Misma sección 500×400 con 3#8/3#8/4#7, `f'c=21`, `fy=420`. Puntos clave:

- **Compresión pura:** `Po = 5423 kN` (calculado arriba), `M = 0`.
- **Tracción pura:** `Tn = Ast·fy = 4608(420) = 1 935 360 N = 1935 kN`, `M = 0`.
- **Punto balanceado** (acero en tracción fluye al tiempo que ε_c=0.003):
  con `d ≈ 440 mm` (h=500, recubrim. al centroide ≈ 60 mm), `Es=200000 MPa`, `εy=fy/Es=0.0021`:
  $$c_b = \frac{0.003}{0.003+0.0021}\,d = \frac{0.003}{0.0051}(440) \approx 259\ mm,\quad a=\beta_1 c=0.85(259)=220\ mm$$
  Con eso se obtiene aproximadamente `Pb ≈ 1500–1700 kN` y `Mb` máximo. (El valor exacto
  depende de la posición real de las 3 capas de barras; el procedimiento es el del recuadro de
  arriba evaluado en `c=259 mm`.)

> **Importante para el parcial:** lo esencial es saber **construir** el diagrama: fijar varios
> valores de `c` (∞, balanceado, d, etc.), hacer equilibrio y graficar (φPn vs φMn). El punto
> balanceado separa la zona de **falla por compresión** (arriba) de la de **falla por tracción**
> (abajo).

---

## 1.4 Flexión biaxial
Cuando hay momento en las dos direcciones (Mx y My), se usan ecuaciones aproximadas que se
"acercan" a la superficie de interacción. La más usada es la **fórmula de Bresler** (carga
recíproca):

$$\frac{1}{P_n} = \frac{1}{P_{nx}} + \frac{1}{P_{ny}} - \frac{1}{P_o}$$

Donde `Pnx`, `Pny` son las capacidades con flexión uniaxial en cada eje y `Po` la de compresión
pura. **No es válida** cuando `φPnx` y `φPny` son menores que `φPb` (zona de tracción).

---

## 1.5 Esbeltez y efectos de segundo orden

### ¿Columna corta o esbelta?
Se compara la esbeltez `k·Lu/r` con un límite:

- **Arriostrada (sin desplazamiento lateral):** es corta si
  $$\frac{k\,L_u}{r} \le 34 - 12\frac{M_1}{M_2} \quad(\le 40)$$
  `M1/M2` es **positivo** en curvatura simple y **negativo** en curvatura doble.
- **No arriostrada (con desplazamiento lateral):** es corta si `k·Lu/r ≤ 22`.

Donde: `Lu` = longitud libre, `k` = factor de longitud efectiva, `r` = radio de giro
(`r ≈ 0.3h` en la dirección de `h` para sección rectangular; `r=√(I/A)`).

### Factor de longitud efectiva k
Se obtiene de los **nomogramas de Jackson–Moreland** a partir de los factores de rigidez en cada
extremo:

$$\psi = \frac{\sum (EI/L)_{columnas}}{\sum (EI/L)_{vigas}}$$

- Extremo articulado → ψ = ∞; empotrado → ψ = 0 (en la práctica se usa 1.0).
- Estructura **arriostrada**: `k ≤ 1.0`. **No arriostrada**: `k ≥ 1.0`.

### Efectos de segundo orden
- **Efecto P-Δ (global):** por desplazamiento lateral relativo de piso → momento de volcamiento
  extra `P·Δ`. Propio de estructuras **no arriostradas**.
- **Efecto P-δ (local):** la carga P actúa a una distancia δ del eje deformado del miembro →
  momento adicional `P·δ`. Propio de estructuras **arriostradas**.

**Procedimiento de magnificación de momentos** (método simplificado de NSR-10):

*Sin desplazamiento lateral (C.10.10.6):*
$$M_c = \delta\,M_2,\qquad \delta = \frac{C_m}{1 - \dfrac{P_u}{0.75\,P_c}} \ge 1.0,\qquad
P_c = \frac{\pi^2 EI}{(k\,L_u)^2}$$

*Con desplazamiento lateral (C.10.10.7):*
$$M_1 = M_{1ns} + \delta_s M_{1s},\quad M_2 = M_{2ns} + \delta_s M_{2s},\quad
\delta_s = \frac{1}{1 - \dfrac{\sum P_u}{0.75\sum P_c}} \ge 1$$

**Nota (límite):** los momentos totales de 2.º orden no deben exceder **1.4 veces** los de
primer orden.

### ✏️ EJERCICIO 1.3 — Longitud efectiva (planteamiento)
**Enunciado:** Pórtico con **vigas 30×40** y **columnas 40×60**; alturas de piso 3.50 m y 3.00 m;
luces 7.00, 8.00 y 6.00 m. Calcular `k` y la longitud efectiva de la **columna central** en
1.º y 2.º piso, y decir si es esbelta.

**Paso 1 – Inercias** (mismo E):
- Columna: `Ic = (0.40)(0.60)³/12 = 0.0072 m⁴`
- Viga: `Iv = (0.30)(0.40)³/12 = 0.0016 m⁴`

**Paso 2 – Rigideces (EI/L), tomando E común y omitiéndolo:**
- Columna piso 1 (h=3.50): `Ic/L = 0.0072/3.50 = 0.002057`
- Columna piso 2 (h=3.00): `Ic/L = 0.0072/3.00 = 0.002400`
- Viga luz 8.00: `Iv/L = 0.0016/8 = 0.000200`
- Viga luz 6.00: `Iv/L = 0.0016/6 = 0.000267`

**Paso 3 – Factor ψ en cada nudo** (ejemplo nudo entre piso 1 y 2, columna central que recibe
dos vigas, una a cada lado):
$$\psi = \frac{(Ic/L)_{sup} + (Ic/L)_{inf}}{(Iv/L)_{izq} + (Iv/L)_{der}}
= \frac{0.002400 + 0.002057}{0.000200 + 0.000267} = \frac{0.004457}{0.000467} \approx 9.5$$

**Paso 4 – k del nomograma:** con ψ en ambos extremos se lee `k` en el ábaco de Jackson–Moreland
(arriostrado → k<1; no arriostrado → k>1). Con ψ≈9–10 y el otro extremo, en pórtico **no
arriostrado** sale `k ≈ 2.0` aprox.

**Paso 5 – Esbeltez:** `r = 0.3 h = 0.3(0.60) = 0.18 m`; `Lu ≈ 3.50 − 0.40 = 3.10 m`.
$$\frac{kL_u}{r} = \frac{2.0(3.10)}{0.18} \approx 34 > 22 \Rightarrow \textbf{columna esbelta}$$

> ⚠️ Como el enunciado depende de la **figura** del pórtico (qué luces llegan a la columna
> central y la condición de arriostramiento), los valores de ψ y k cambian según esa
> configuración. Aquí te dejo **el método completo**: calcula inercias → EI/L → ψ en cada nudo →
> lee k en el nomograma → compara kLu/r con el límite. Si me confirmas qué luces (7/8/6) llegan
> a la columna central, te entrego el número exacto.


---

# 2. PROVISIONES SÍSMICAS PARA COLUMNAS (C.21)

El Capítulo **C.21 de la NSR-10** da requisitos extra de detallado según la capacidad de
disipación de energía del sistema: **DMI** (mínima), **DMO** (moderada) y **DES** (especial).

## 2.1 Columnas DMO (C.21.3.5)
- **Dimensión mínima:** ≥ **250 mm** (en T, C o I ≥ 0.20 m y área ≥ 0.0625 m²).
- **Refuerzo longitudinal:** `0.01 Ag ≤ Ast ≤ 0.04 Ag`.
- **Empalmes por traslapo:** solo en la **mitad central** del elemento, diseñados a tracción.
- **Confinamiento (estribos) en longitud ℓ₀ desde la cara del nudo:**
  - Separación `s₀ ≤ menor de`:
    - 8 × (diámetro barra longitudinal menor)
    - 16 × (diámetro del estribo)
    - 1/3 de la menor dimensión de la columna
    - 150 mm
  - Longitud `ℓ₀ ≥ mayor de`: Lu/6, mayor dimensión de la columna, 500 mm.
  - Primer estribo a ≤ `s₀/2` de la cara del nudo.
  - Fuera de ℓ₀: separación ≤ 2·(la usada dentro de ℓ₀).
- Estribo mínimo **#3 (3/8") ó 10M**.
- **Cortante (C.21.3.3):** ΦVn ≥ menor de (a) cortante por desarrollo de los momentos nominales
  en ambos extremos (curvatura inversa), (b) cortante máximo de combinaciones con E amplificado.

## 2.2 Columnas DES (C.21.6) — más exigentes
- **Dimensión mínima:** ≥ **300 mm**; relación lado menor/lado mayor ≥ 0.40 (ó según el rango).
- **Refuerzo longitudinal:** `0.01 Ag ≤ Ast ≤ 0.04 Ag`; mínimo 6 barras si estribo circular.
- **Refuerzo transversal en ℓ₀:** `ℓ₀ ≥ mayor de`: altura del elemento, Lu/6, 450 mm.
  - Separación `s ≤ menor de`: ¼ de la dimensión mínima, 6·db longitudinal, `s₀`
    (con `100 mm ≤ s₀ ≤ 150 mm`).
  - Cuantía de confinamiento: espiral `ρs` por (C.21-6); estribos rectangulares `Ash` por
    (C.21-7) y (C.21-8).

## 2.3 Principio de **columna fuerte – viga débil** (C.21.6.2.2)
En los nudos, la suma de resistencias a flexión de las **columnas** debe superar a la de las
**vigas**:

$$\sum M_{nc} \ge \tfrac{6}{5}\sum M_{nb} \quad\Longleftrightarrow\quad \sum M_{nc} \ge 1.2\sum M_{nb}$$

Esto obliga a que las **rótulas plásticas** se formen en las vigas (no en las columnas),
evitando el colapso del piso.

> 💡 **Para el parcial:** memoriza dimensiones mínimas (250 mm DMO / 300 mm DES), el rango de
> acero `1 %–4 %`, las reglas de `s₀` y `ℓ₀`, y el concepto columna fuerte–viga débil.

---

# 3. ESCALERAS

## 3.1 Comportamiento estructural
Una escalera se diseña, en la mayoría de los casos, como una **losa maciza unidireccional**
apoyada en sus extremos (descansos o vigas). El refuerzo principal va en la dirección de la luz.

## 3.2 Requisitos geométricos (Título K, NSR-10)
- **Ancho mínimo:** 1.20 m si ocupación > 50 personas; 0.90 m si < 50; 0.75 m en viviendas
  unifamiliares.
- **Huella:** ancho mínimo **280 mm**.
- **Contrahuella:** entre **100 mm y 180 mm**.
- **Regla de comodidad:** `600 mm ≤ 2·(contrahuella) + 1·(huella) ≤ 640 mm`.
- Ángulo huella–contrahuella entre 75° y 90°; bordes redondeados (r ≤ 1 cm); piso antideslizante.

## 3.3 Tipologías
- **Un solo tramo:** se comporta como losa unidireccional apoyada en dos extremos.
- **Doble tramo:** común entrepisos; cada tramo se analiza como losa unidireccional independiente.
- **En voladizo:** cada peldaño es un voladizo empotrado en muro/viga; refuerzo principal en la
  cara de tracción + acero de retracción/temperatura transversal.
- **Autoportante:** el descanso "vuela"; aparecen **momentos de torsión** en la losa.

## 3.4 Procedimiento de diseño (el de la presentación)
1. **Predimensionar el espesor:** `e = L/20` (losa).
2. **Evaluar cargas** en los dos tramos por separado:
   - **Tramo de descanso** (horizontal): peso propio losa + acabados + carga viva.
   - **Tramo inclinado:** el peso propio se mayora por la inclinación; se suma el peso de los
     escalones (área triangular de cada peldaño × γ_concreto) + acabados + carga viva.
   - Carga viva típica de escaleras `≈ 3.0 kN/m²` (residencial) según uso (Título B).
3. **Modelo:** viga/losa simplemente apoyada (o continua) de 1 m de ancho con la carga
   distribuida `wu = 1.2 CM + 1.6 CV`.
4. **Momentos y cortantes:** `Mu = wu L²/8` (apoyo simple) y `Vu = wu L/2`.
5. **Diseño a flexión** del acero principal y **acero mínimo de retracción** (0.0018·Ag)
   en la dirección transversal.

### ✏️ EJERCICIO 3.1 — Escalera (procedimiento con valores ilustrativos)
La presentación plantea el ejemplo con **figuras** (geometría del tramo y descanso) cuyos números
no vienen en el texto del archivo. Te muestro el **método completo** con valores típicos para que
lo repliques con los datos exactos de tu figura:

*Supón:* luz total `L = 4.0 m`, espesor `e = L/20 = 0.20 m`, huella 0.30 m, contrahuella 0.18 m,
acabados 1.5 kN/m², carga viva 3.0 kN/m², γ_concreto = 24 kN/m³.

1. **Descanso:** `CM = 0.20(24) + 1.5 = 4.8 + 1.5 = 6.3 kN/m²`; `CV = 3.0`.
2. **Tramo inclinado:** factor de inclinación `√(h²+b²)/b = √(0.18²+0.30²)/0.30 = 0.35/0.30 = 1.166`.
   Peso losa inclinada `= 0.20(24)(1.166) = 5.6 kN/m²`; peso escalones `≈ γ·(contrahuella/2) =
   24(0.18/2) = 2.16 kN/m²`; `CM ≈ 5.6 + 2.16 + 1.5 = 9.3 kN/m²`; `CV = 3.0`.
3. **Carga mayorada** (tramo inclinado, por metro de ancho): `wu = 1.2(9.3)+1.6(3.0) = 11.16+4.8
   = 15.96 ≈ 16.0 kN/m`.
4. **Momento:** `Mu = wu L²/8 = 16.0(4.0²)/8 = 32.0 kN·m`.
5. **Cortante:** `Vu = wu L/2 = 16.0(4.0)/2 = 32.0 kN`.
6. **Acero a flexión** (d ≈ e − 0.03 = 0.17 m, b=1 m, f'c=21, fy=420):
   `Rn = Mu/(φbd²) = 32e6/(0.9·1000·170²) = 1.23 MPa` →
   `ρ = (0.85·21/420)[1−√(1−2·1.23/(0.85·21))] = 0.0425(0.0719) = 0.00306` →
   `As = 0.00306(1000)(170) = 520 mm²/m` → **#4 @ 0.20 m** (645 mm²/m) ✔
7. **Acero de temperatura (transversal):** `As = 0.0018(1000)(200) = 360 mm²/m` → **#3 @ 0.15 m**.

> ⚠️ Reemplaza los valores supuestos por los de **tu figura** (luces del descanso y del tramo
> inclinado, número de contrahuellas) y el procedimiento es idéntico. Si me pasas la geometría
> exacta (o una imagen clara de la diapositiva 8–10), te lo resuelvo con tus números.


---

# 4. ZAPATAS

## 4.1 Idea general y procedimiento
La zapata transmite las cargas de la columna al suelo. El diseño tiene **dos etapas**:

1. **Dimensionamiento (en servicio):** se usan **cargas de servicio** (sin mayorar) y la
   **capacidad admisible del suelo** `σadm` para hallar el área en planta:
   $$A_{req} = \frac{P_{servicio}}{\sigma_{adm}}$$
2. **Diseño (mayorado):** con las cargas mayoradas se halla la **presión neta de diseño**
   `qu = Pu/A`, y con ella se revisa **cortante** y se diseña la **flexión**.

Combinaciones de carga (las de la presentación): `1.4D`; `1.2D+1.6L+0.5(Lr/G/Le)`; etc.

## 4.2 Las tres verificaciones de una zapata
1. **Flexión:** la presión del suelo flexiona los voladizos. La sección crítica está en la
   **cara de la columna**.
   $$M_u = q_u \cdot B \cdot \frac{L_{vol}^2}{2}$$
2. **Cortante en una dirección (como viga):** sección crítica a **`d`** de la cara de la columna.
   $$\phi V_c = \phi\,0.17\sqrt{f'_c}\,b\,d \quad(\phi=0.75)$$
3. **Cortante en dos direcciones (punzonamiento):** sección crítica a **`d/2`** de la cara.
   La columna tiende a "perforar" la zapata. `Vc` es el **menor** de:
   $$V_c = 0.33\sqrt{f'_c}\,b_o d;\quad
   V_c = 0.17\left(1+\tfrac{2}{\beta}\right)\sqrt{f'_c}\,b_o d;\quad
   V_c = 0.083\left(2+\tfrac{\alpha_s d}{b_o}\right)\sqrt{f'_c}\,b_o d$$
   con `β =` lado largo/lado corto de la columna; `αs = 40` (interior), 30 (borde), 20 (esquina);
   `bo =` perímetro crítico.

---

### ✏️ EJERCICIO 4.1 — Zapata cuadrada
**Enunciado:** Dimensionar y diseñar una zapata cuadrada para una columna de **0.40×0.40 m**.
`PD = 1700 kN`, `PL = 500 kN`, `σadm = 180 kN/m²`. (Tomamos `f'c = 21 MPa`, `fy = 420 MPa`.)

**Paso 1 – Dimensionamiento (servicio)**
`P_serv = 1700 + 500 = 2200 kN`
$$A_{req} = \frac{2200}{180} = 12.22\ m^2 \Rightarrow B = \sqrt{12.22} = 3.50\ m$$
Adopto **B = 3.50 m** (A = 12.25 m²). Verifico: `σ = 2200/12.25 = 179.6 ≤ 180` ✔

**Paso 2 – Presión neta de diseño**
`Pu = 1.2(1700) + 1.6(500) = 2040 + 800 = 2840 kN`
$$q_u = \frac{2840}{12.25} = 231.8\ kN/m^2$$

**Paso 3 – Altura por punzonamiento (dos direcciones)** → gobierna casi siempre.
Sección crítica a d/2: cuadrado de lado `(0.40 + d)`; `bo = 4(0.40 + d)`.
Probando **d = 0.60 m**:
- `Vu = qu[A − (0.40+d)²] = 231.8[12.25 − (1.00)²] = 231.8(11.25) = 2608 kN`
- `φVc = 0.75(0.33√21)(bo)(d) = 0.75(0.33)(4.583)(4·1000)(600) = 2722 kN`  *(bo=4000 mm)*
- `φVc = 2722 kN ≥ Vu = 2608 kN` ✔ (gobierna el término 0.33√f'c; β=1)

Adopto **d = 0.60 m → h ≈ 0.70 m** (recubrimiento 75 mm contra el suelo).

**Paso 4 – Cortante en una dirección (como viga)**
Voladizo `Lvol = (3.50−0.40)/2 = 1.55 m`; sección crítica a `d`: `x = 1.55 − 0.60 = 0.95 m`.
- `Vu = qu·B·x = 231.8(3.50)(0.95) = 771 kN`
- `φVc = 0.75(0.17√21)(3500)(600) = 1227 kN ≥ 771` ✔

**Paso 5 – Diseño a flexión** (sección crítica en la cara de la columna)
$$M_u = q_u\,B\,\frac{L_{vol}^2}{2} = 231.8(3.50)\frac{1.55^2}{2} = 974.6\ kN\cdot m$$
- `Rn = Mu/(φ b d²) = 974.6e6/(0.9·3500·600²) = 0.859 MPa`
- `ρ = (0.85·21/420)[1−√(1−2·0.859/17.85)] = 0.0425(0.0494) = 0.00210`
- `As = ρ·b·d = 0.00210(3500)(600) = 4406 mm²`
- **As mínimo** (retracción) `= 0.0018·b·h = 0.0018(3500)(700) = 4410 mm²` → **gobierna**.

`As = 4410 mm²` en **cada dirección** (zapata cuadrada → refuerzo igual en ambos sentidos).
Con **#6 (284 mm²): 4410/284 ≈ 16 barras** → **16 #6 @ ~0.22 m** en cada dirección.

> **Resumen Ej. 4.1:** Zapata **3.50 × 3.50 m**, **h = 0.70 m**, **16#6 en cada dirección**.

---

### ✏️ EJERCICIO 4.2 — Zapata rectangular (voladizos iguales)
**Enunciado:** Columna **0.30×1.20 m**, `PD=1800 kN`, `PL=600 kN`, `σadm=220 kN/m²`,
`Wpp = 10% P(B×L)`.

**Paso 1 – Dimensionamiento** (incluyendo 10 % de peso propio)
`P_serv = 1800+600 = 2400 kN` → con 10 %: `P_total = 2640 kN`.
`A_req = 2640/220 = 12.0 m²`.
**Voladizos iguales** ⇒ `(B−0.30)/2 = (L−1.20)/2` ⇒ `L = B + 0.90`.
`B(B+0.90) = 12.0 → B² + 0.90B − 12 = 0 → B = 3.05 m`, `L = 3.95 m`.
Voladizo `= (3.05−0.30)/2 = (3.95−1.20)/2 = 1.375 m` ✔ (iguales).
`σ = 2400/(3.05·3.95) = 199 ≤ 220` ✔

**Paso 2 – Presión de diseño**
`Pu = 1.2(1800)+1.6(600) = 2160+960 = 3120 kN`; `qu = 3120/12.05 = 258.9 kN/m²`.

**Paso 3 – Punzonamiento** (columna `β = 1.20/0.30 = 4` ⇒ gobierna el término `0.17(1+2/β)`)
Probando **d = 0.60 m**: perímetro `(0.30+d)×(1.20+d) = 0.90×1.80`; `bo = 2(0.90+1.80) = 5.40 m`.
- `Vu = 258.9[12.05 − (0.90)(1.80)] = 258.9(10.43) = 2700 kN`
- `φVc = 0.75[0.17(1+2/4)√21](5400)(600) = 0.75(0.255)(4.583)(5400)(600) = 2840 kN ≥ 2700` ✔

Adopto **d = 0.60 m, h = 0.70 m**.

**Paso 4 – Flexión en cada dirección** (voladizo 1.375 m en ambas):
- **Dirección larga** (ancho B=3.05): `Mu = 258.9(3.05)(1.375²/2) = 746 kN·m` →
  `As ≈ 3360 mm²`; pero `As,min = 0.0018(3050)(700) = 3843 mm²` **gobierna**.
- **Dirección corta** (ancho L=3.95): `Mu = 258.9(3.95)(1.375²/2) = 967 kN·m` →
  `As,min = 0.0018(3950)(700) = 4977 mm²` **gobierna**.

**Distribución del refuerzo corto:** una fracción se concentra en la franja central de ancho B:
$$\frac{A_{s,banda}}{A_{s,total}} = \frac{2}{\beta+1},\qquad \beta = \frac{L}{B} = \frac{3.95}{3.05} = 1.30
\Rightarrow \frac{2}{2.30} = 0.87\ (87\%\ \text{en la franja central})$$

> **Resumen Ej. 4.2:** Zapata **3.05 × 3.95 m**, **h = 0.70 m**; refuerzo por dirección según
> `As,min`, concentrando el 87 % del acero corto en la franja central de ancho B.

---

### ✏️ EJERCICIO 4.3 — Zapata excéntrica (con viga de contrapeso)
**Enunciado:** Columna **0.40×0.50** (0.50 en la dirección de la excentricidad).
`σadm=200 kN/m²`, `PD=400 kN`, `PL=120 kN`, peso propio = 10 % de P, `C = 6.0 m`
(distancia al centro de la columna interior).

**Idea clave:** la zapata está en el **lindero** (no se puede centrar bajo la columna), así que la
reacción del suelo sería **trapezoidal/triangular**. Para volverla **uniforme** se conecta con una
**viga de contrapeso** a la columna interior, que toma el momento de la excentricidad.

**Paso 1 – Carga total** `P = 400+120 = 520 kN`; con 10 %: `P_total = 572 kN`.

**Paso 2 – Geometría/excentricidad:** con la cara de la columna en el lindero, la excentricidad
entre el centro de la columna y el centroide de la zapata es `e = L/2 − 0.50/2 = L/2 − 0.25`.

**Paso 3 – Reacción amplificada por la viga (estática):** tomando momentos respecto a la columna
interior, la reacción bajo la zapata exterior se amplifica:
$$R_1 = P_1\cdot\frac{C}{C - e}$$
Se **supone B**, se impone presión uniforme `σadm` y se despeja `L`:
$$A = B\cdot L = \frac{R_1}{\sigma_{adm}}\quad\text{(iterando, porque } e \text{ depende de } L)$$

**Paso 4 – Diseño:** una vez fijadas `B` y `L`, se halla `qu = Pu/A`, se revisa **punzonamiento**
(a d/2) y **cortante como viga** (a d), y se diseña la **flexión** de la zapata. La **viga de
contrapeso** se diseña a flexión para el momento `ΔPu·(brazo)` que equilibra la excentricidad, con
estribos por cortante.

> ⚠️ El número final de `B` y `L` exige iterar (e depende de L) y leer la geometría exacta de la
> figura (posición de la columna respecto al lindero). Aquí tienes **el planteamiento completo y
> las ecuaciones de equilibrio**; con la distancia exacta del eje de la columna al borde te entrego
> los valores numéricos cerrados.

---

# 5. VIGAS DE AMARRE

## 5.1 ¿Para qué sirven? (6 funciones)
Las vigas de amarre de cimentación se diseñan considerando, según la presentación:
1. **Viga de enlace/contrapeso** de zapatas excéntricas.
2. **Amarre sísmico** (la función principal exigida por norma).
3. **Control de asentamientos diferenciales** (transmiten carga entre zapatas vecinas).
4. **Reacción del terreno** bajo la viga (no siempre se considera, pero existe).
5. **Cargas aplicadas directamente** sobre la viga (escaleras, rampas, muros, columnas secundarias).
6. **Momentos de empotramiento** transmitidos por las columnas.

## 5.2 Requisitos (C.15.13)
- **Sección mínima** (dimensión mayor ≥ luz / k): `L/20` (DES), `L/30` (DMO), `L/40` (DMI).
- **Refuerzo longitudinal continuo** capaz de desarrollar `fy` anclado en la columna exterior.
- **Estribos cerrados** en toda la longitud, separación ≤ menor de (½ de la dimensión menor, 300 mm).

## 5.3 Amarre sísmico (A.3.6.4.2)
La viga debe resistir, en **tracción o compresión**, una fuerza no menor de:
$$T = 0.25\,A_a \times (\text{carga del elemento más cargado que conecta})$$

### ✏️ EJERCICIO 5.1 — Amarre sísmico
**Enunciado:** Viga de amarre **0.50×0.70 m** que conecta dos columnas con cargas verticales
mayoradas de **4000 kN** y **5200 kN**. Diseñar el refuerzo por amarre sísmico. `Aa = 0.15`.

**Paso 1 – Fuerza de amarre** (se toma la columna **más cargada** = 5200 kN):
$$T = 0.25\,A_a\,P_{max} = 0.25(0.15)(5200) = \boxed{195\ kN}$$

**Paso 2 – Acero requerido por tracción** (φ = 0.90):
$$A_{s,req} = \frac{T}{\phi f_y} = \frac{195\,000}{0.90(420)} = 516\ mm^2$$

**Paso 3 – Verificar mínimos de C.15.13 y proveer refuerzo:**
La norma exige **refuerzo longitudinal continuo arriba y abajo** y estribos cerrados. Con
**3#7 arriba y 3#7 abajo** (`6 × 387 = 2322 mm² > 516 mm²` requeridos) se cumple con holgura, y
la sección 0.50×0.70 supera ampliamente la capacidad a tracción/compresión necesaria.
**Estribos:** separación ≤ ½(0.50) = 0.25 m → usar **#3 @ 0.20 m** (≤ 300 mm) en toda la luz.

> **Resumen Ej. 5.1:** `T = 195 kN`; basta el refuerzo mínimo continuo (≈ **3#7 arriba y abajo**)
> con estribos #3 @ 0.20 m. El amarre sísmico casi nunca gobierna frente a los mínimos de sección.

---

# 6. FORMULARIO RÁPIDO

**Columnas**
- Compresión pura: `Po = 0.85f'c(Ag−Ast) + fy·Ast`
- Máxima (estribos): `φPn,max = 0.80·0.65·Po` | (espiral): `0.85·0.75·Po`
- Tracción pura: `φTn = 0.90·Ast·fy`
- Punto balanceado: `cb = 0.003·d/(0.003+εy)`, `εy = fy/Es`
- Esbeltez corta: arriostrada `kLu/r ≤ 34−12(M1/M2)`; no arriostrada `kLu/r ≤ 22`
- `r ≈ 0.3h`; `ψ = Σ(EI/L)col / Σ(EI/L)vig`
- Magnificador: `δ = Cm/(1 − Pu/0.75Pc) ≥ 1`, `Pc = π²EI/(kLu)²`
- Columna fuerte–viga débil: `ΣMnc ≥ 1.2 ΣMnb`

**Zapatas**
- Área: `A = P_serv/σadm` | Presión diseño: `qu = Pu/A`
- Punzonamiento (a d/2): `φVc = φ·(menor de 0.33√f'c; 0.17(1+2/β)√f'c; 0.083(2+αs·d/bo)√f'c)·bo·d`
- Cortante viga (a d): `φVc = φ·0.17√f'c·b·d`
- Flexión (cara col): `Mu = qu·B·Lvol²/2`
- `As,min = 0.0018·b·h` (retracción)
- Franja central (rectangular): `As,banda/As = 2/(β+1)`, `β=L/B`

**Escaleras**
- Espesor: `e = L/20` | `wu = 1.2CM + 1.6CV`
- `Mu = wuL²/8`, `Vu = wuL/2` (apoyo simple)
- Factor de inclinación: `√(h²+b²)/b`

**Vigas de amarre**
- Amarre sísmico: `T = 0.25·Aa·Pmax`
- Sección: dim. mayor ≥ L/20 (DES), L/30 (DMO), L/40 (DMI)
- Estribos: s ≤ menor de (½ dim. menor, 300 mm)

**Diseño a flexión (general)**
- `Rn = Mu/(φ·b·d²)`, φ=0.90
- `ρ = (0.85f'c/fy)·[1 − √(1 − 2Rn/0.85f'c)]`
- `As = ρ·b·d`

---

*Guía generada para repaso del parcial. Verifica siempre con tus apuntes y la NSR-10 vigente.*
*Los ejercicios que dependen de figuras (diagrama de interacción detallado, longitud efectiva,
escaleras y zapata excéntrica) incluyen el método completo; con los datos exactos de la figura se
cierran numéricamente.*

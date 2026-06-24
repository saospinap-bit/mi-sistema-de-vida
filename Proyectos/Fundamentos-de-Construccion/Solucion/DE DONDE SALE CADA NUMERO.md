# 🔎 DE DÓNDE SALE CADA NÚMERO — Cantidades de obra
### CDI Tesalia · Módulo 1 · explicación literal, número por número

> Aquí rastreo el origen exacto de **cada cifra** que aparece en las cantidades de obra.
> Hay 3 orígenes posibles para cada número:
> - 🟩 **DADO** = venía resuelto en el archivo del profesor (las 3 memorias de ejemplo).
> - 🟦 **PLANO** = lo leí de los planos (cotas, rótulos, secciones, despieces).
> - 🟨 **SUPUESTO** = lo asumí con criterio de ingeniería (y debes confirmarlo en CAD).

---

## 1. Los 3 números que vienen DADOS por el profesor 🟩

El archivo `FORMATO MEMORIAS DE CÁLCULO.xlsx` trae **3 memorias ya resueltas**. De ahí salen 3 cantidades exactas:

### a) Contrapiso (ítem 4.3.1) → el famoso 9.85 × 21.95
La hoja **"4.3.1 Placa-Contrapiso"** dice: Ancho **9.85 m**, Largo **21.95 m**, espesor **0.10 m**.
- Área del piso = 9.85 × 21.95 = **216.20 m²**
- Volumen de concreto = 216.20 × 0.10 = **21.62 m³**
- *9.85 = ancho del edificio; 21.95 = largo del edificio.* (medidos por el grupo guía)

### b) Placa de cubierta (ítem 4.3.3)
La hoja **"4.3.3 PLACA CUBIERTA"** dice: Ancho **7.30 m**, Largo **18.52 m**.
- Área de cubierta = 7.30 × 18.52 = **135.20 m²**
- (La placa de cubierta es más pequeña que el piso porque no cubre aleros/corredores.)

### c) Adoquín (ítem 8.1.1)
La hoja **"8.1 PISOS ACABADOS"** trae 9 áreas ya medidas. Las sumé:
`18.62 + 17.49 + 22.25 + 7.76 + 14.60 + 15.00 + 1.91 + 1.91 + 15.76 = ` **115.30 m²**

> ✅ Estas 3 son 100% confiables porque las puso el profesor.

---

## 2. Los datos que leí de los PLANOS 🟦

Abriendo los planos DWG (convertidos a datos), leí estos valores **escritos en el dibujo**:

| Dato leído | Valor | Dónde aparece en el plano |
|---|---|---|
| Separación ejes A–B | **7.70 m** | planta estructural (distancia entre las 2 filas de columnas) |
| Largo ejes 1 a 4 | **19.80 m** | cota repetida en la planta estructural |
| Sección viga cimentación | **0.40 × 0.45 m** | rótulos "VC-A 40x45", "VC-1 40x45"… |
| Sección viga cubierta | **0.40 × 0.50 m** | rótulos "VG-1 40x50"… |
| Sección columna | **~0.40 × 0.40 m** | despiece de columnas |
| Altura de columna | hasta **N+4.90 m** | nivel de la placa de cubierta |
| Zapatas | **1.20×1.20×0.40 m** | rótulo "ZAPATA 120x120x40cm" |
| Refuerzo columnas | **2#6 + 2#7**, estribo #2 c/0.20 | despiece "2#6+2#7 L=5.95" |
| Refuerzo vigas | 3#6+3#5 / 2#6+2#7, estribos #3 | callouts "3#6L=...", "36E#3..." |
| Espesor placa cubierta | **0.08 m** | "PLACA … LOSA ALIGERADA e: 0.08m" |
| Bloque mampostería | **No.4** (muros), No.5 (columnetas) | notas y rótulos |

---

## 3. Cómo combiné esos datos para cada cantidad

### Vigas de cimentación – concreto (ítem 2.2.1) → 13.70 m³
Las vigas forman una cuadrícula. Sumé su **longitud total**:
- 2 vigas largas (sobre ejes A y B): 2 × 19.80 = **39.60 m**
- 5 vigas cortas (ejes 1,2,3,3',4), midiendo la **luz libre** entre las vigas largas: 5 × (7.70 − 0.40) = 5 × 7.30 = **36.50 m**
- Longitud total = 39.60 + 36.50 = **76.10 m**
- Volumen = 76.10 × **0.40** (ancho) × **0.45** (alto) = **13.70 m³**

> El "− 0.40" es para no contar dos veces el cruce de las vigas (el ancho de la viga larga).

### Solado (ítem 2.2.2) → 38.05 m²
Es la capa delgada bajo las vigas: 76.10 m × 0.50 m de ancho = **38.05 m²**

### Columnas – concreto (ítem 4.1.1) → 7.84 m³
- N° de columnas = ejes A,B (2) × ejes 1,2,3,3',4 (5) = **10 columnas**
- Volumen = 10 × 0.40 × 0.40 × 4.90 (alto) = **7.84 m³**

### Vigas de cubierta – concreto (ítem 4.2.1) → 15.22 m³
Misma cuadrícula (76.10 m) pero sección 0.40 × 0.50:
- 76.10 × 0.40 × 0.50 = **15.22 m³**

---

## 4. El ACERO (kg) — ítems 2.3.1, 4.7.1, 4.8.1, 5.2.1

El acero se pesa: cada varilla tiene un **peso por metro** según su grosor (tabla estándar):
`#3 = 0.560 · #4 = 0.994 · #5 = 1.552 · #6 = 2.235 · #7 = 3.042 kg/m` (esto es de tabla, no del plano).

**Ejemplo — acero vigas de cimentación (2.3.1) = 1.302,6 kg:**
- Refuerzo a lo largo (3 varillas #6 + 3 varillas #5) sobre los 76.10 m:
  76.10 × (3×2.235 + 3×1.552) = 76.10 × 11.36 = **864,6 kg**
- Estribos #3 cada 0.20 m: caben 76.10 / 0.20 = 381 estribos; cada uno mide ≈1.50 m:
  381 × 1.50 × 0.560 = **319,6 kg**
- Suma = 1.184,2 kg → **+10%** por desperdicio y traslapos = **1.302,6 kg**

(Los demás aceros se calcularon igual, leyendo el refuerzo de cada elemento del despiece del plano.)

### Mallas (ítems 4.6.1 y 4.9.1)
La malla 8 mm cada 0.15 m pesa **5.27 kg/m²** (cálculo de tabla):
- Contrapiso: 216.20 m² × 5.27 × 1.10 = **1.252,5 kg**
- Cubierta: 135.20 m² × 5.27 × 1.10 = **783,3 kg**

---

## 5. Lo que es SUPUESTO (confírmalo en CAD) 🟨

Estos dependen de medidas que el DWG no deja leer limpio (muchas vistas encimadas):

| Ítem | Valor | Supuesto |
|---|---|---|
| 5.1.1 Muros (m²) | 402.75 | 173.6 m de muro × 2.90 m alto × 0.80 (descuento de puertas/ventanas) |
| 5.1.2 Columnetas (ml) | 168.2 | una cada 3 m de muro × altura |
| 5.1.4 Pañete (m²) | 261.79 | 65% del área de muro |
| 2.1.1 Excav. máquina (m³) | 118.91 | 216.20 m² × 0.55 m de profundidad |
| 2.1.2 Subbase (m³) | 32.43 | 216.20 m² × 0.15 m |
| 2.1.4 Relleno (m³) | 43.24 | 216.20 m² × 0.20 m |

> El único realmente importante de confirmar es el **corrido de muros** (5.1.1): mídelo en la planta de mampostería y reemplázalo; columnetas y pañete se ajustan solos con la proporción.

---

## Resumen visual del origen

```
9.85 y 21.95  ──► del EJEMPLO del profesor (memoria 4.3.1)
7.30 y 18.52  ──► del EJEMPLO del profesor (memoria 4.3.3)
115.30        ──► del EJEMPLO del profesor (memoria 8.1)
7.70 / 19.80  ──► COTAS del plano estructural
0.40x0.45 etc ──► RÓTULOS de secciones del plano
2#6+2#7 etc   ──► DESPIECE de acero del plano
0.560.. kg/m  ──► TABLA estándar de pesos de varilla
0.55/0.15 m   ──► SUPUESTO de ingeniería (verificar)
173.6 m muro  ──► SUPUESTO (medir en CAD)
```

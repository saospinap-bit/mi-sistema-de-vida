# 🧮 CÓMO SE CALCULÓ TODO — Memoria metodológica
### Presupuesto CDI Tesalia · Módulo 1 · Obra gris

> Este documento NO explica cómo usar el Excel, sino **cómo se obtuvo cada número**: cómo se midieron los planos,
> cómo se calcula cada cantidad de material, el acero, los APU y el total. Si entiendes esto, puedes reproducir
> y defender todo el proyecto.

---

## 0. El método en una frase

Un presupuesto se arma multiplicando, para cada actividad:

> **COSTO = CANTIDAD (cuánto hay en la obra) × PRECIO UNITARIO (cuánto cuesta hacer 1 unidad)**

- La **CANTIDAD** sale de **medir los planos** (geometría: largo × ancho × alto, áreas, conteos).
- El **PRECIO UNITARIO** sale del **APU** (Análisis de Precio Unitario), que suma material + mano de obra + equipo.
- Al final se suman todas las actividades (= **costo directo**) y se le agrega el **AIU**.

Todo lo demás es repetir esto 19 veces (una por actividad) con cuidado.

---

## 1. Cómo se leyeron los planos

Los planos venían en `.dwg` (AutoCAD 2018). El procedimiento fue:

1. **Convertir** el `.dwg` a un formato de datos legible.
2. **Extraer** de la geometría del dibujo:
   - Los **textos y rótulos** (nombres de ambientes, áreas escritas, especificaciones).
   - Las **cotas/dimensiones** (las medidas acotadas en metros).
   - Los **despieces de acero** (textos tipo `3#6 L=3.00` = 3 varillas No.6 de 3.00 m).
   - Las **secciones de los elementos** (`B=0.40 H=0.45`, `ZAPATA 120x120x40`).
3. Con esas medidas se calcularon las cantidades. **Cada número es trazable a un plano.**

**Datos base que se confirmaron en los planos:**

| Dato | Valor | Plano |
|---|---|---|
| Proyecto | CDI (jardín infantil) en Tesalia, Huila | rótulo estructural |
| Ejes (retícula) | A, B (separados 7.70 m) × 1, 2, 3, 3', 4 (largo 19.80 m) | planta columnas |
| Columnas | 8 (4 de 0.50×0.50 + 4 de 0.40×0.40), refuerzo 2#6+2#7, hasta N+4.90 | despiece columnas |
| Vigas cimentación | 0.40×0.45 m (VC-1..4, VC-A, VC-B) | planta cimentación |
| Vigas cubierta | 0.40×0.50 m (VG-1..7) | planta cubierta |
| Zapatas | Z-1 2.30×2.30 y Z-2 2.15×2.15 (×0.40), concreto 3000 psi | detalle zapata |
| Placa contrapiso | área 216.20 m² (9.85×21.95), e=0.10 | memoria/arquitectónico |
| Placa cubierta | losa aligerada e=0.08, viguetas 0.20×0.40, área 135.20 m² | planta cubierta |
| Adoquín | 9 áreas que suman 115.30 m² | planta adoquín |
| Acero | fy = 4200 kg/cm² = 420 MPa = 60.000 psi | notas estructurales |
| Mampostería | bloque No.4 (muros), No.5 (columnetas) | plano mampostería |

---

## 2. Concepto clave: ¿cómo se mide una "cantidad"?

Depende de la **unidad** de la actividad:

| Si la unidad es… | Se calcula… | Ejemplo |
|---|---|---|
| **m³** (volumen) | largo × ancho × alto | una viga de 0.40×0.45×10 m = 1.80 m³ |
| **m²** (área) | largo × ancho | una placa de 9.85×21.95 = 216.2 m² |
| **ml** (metro lineal) | solo el largo | 50 m de columneta |
| **kg** (acero) | longitud de varilla × peso por metro | ver sección 5 |
| **und** (unidad) | conteo | 8 columnas |

Todo el truco es identificar bien las dimensiones en el plano y multiplicarlas. Para las vigas hay que tener cuidado de **no contar dos veces** los cruces (por eso a las vigas transversales les resté el ancho de la viga longitudinal: "luz libre").

---

## 3. Cálculo de cada CANTIDAD (las 19 actividades)

> Notación: L = 19.80 m (largo entre ejes 1–4), W = 7.70 m (ancho entre ejes A–B).

### CAPÍTULO 2 — CIMENTACIÓN

**2.1.1 Excavación a máquina (m³)** = plataforma + zanjas de cimentación al desplante de **1.5 m** (dato del plano: *"nivel de desplante mínimo 1.5 m a partir de piso"*)
`(4×2.30² + 4×2.15²)×1.5 (pozos zapatas) + (58.5×0.60×1.5) (zanjas) = 59.48 + 52.65 = 112.12 m³`

**2.1.2 Relleno subbase granular B-400 (m³)** = colchón granular de **0.30 m** (plano: *"mínimo 0.30 m"*) × área
`216.20 × 0.30 = 64.86 m³`

**2.1.3 Excavación manual (m³)** = afinado del fondo de las zanjas
`(39.65 pozos + 35.10 zanjas) × 0.10 = 7.48 m³`

**2.1.4 Relleno recebo común (m³)** = área × espesor de nivelación
`9.85 × 21.95 × 0.20 = 43.24 m³`

**2.1.6 Geotextil NT 1600 (m²)** = área de la placa = `216.20 m²`

**2.2.1 Vigas de cimentación – concreto (m³)** = longitud de vigas × sección
- Vigas largas (VC-A, VC-B): 2 × 19.80 = 39.60 m
- Vigas transversales (VC-1,2,3,3',4), luz libre: 5 × (7.70 − 0.40) = 5 × 7.30 = 36.50 m
- **Longitud total = 76.10 m**
- Volumen = `76.10 × 0.40 × 0.45 = 13.70 m³`

**2.2.2 Solado 1500 psi e=0.05 (m²)** = huella de las vigas (con sobreancho)
`76.10 × 0.50 = 38.05 m²`

**2.3.1 Acero vigas cimentación (kg)** → ver sección 5. = **1.302,6 kg**

### CAPÍTULO 4 — ESTRUCTURA

**4.1.1 Columnas – concreto (m³)** = N° columnas × sección × altura
`4×(0.50×0.50) + 4×(0.40×0.40), × 4.90 = (1.00+0.64)×4.90 = 8.04 m³`

**4.2.1 Vigas de cubierta – concreto (m³)** = longitud × sección (mismo grid)
`76.10 × 0.40 × 0.50 = 15.22 m³`

**4.3.1 Contrapiso – concreto (m³)** = área × espesor
`216.20 × 0.10 = 21.62 m³`

**4.3.3 Placa aligerada cubierta (m²)** = área de cubierta = `135.20 m²` (7.30×18.52)

**4.6.1 Malla contrapiso (kg)** → sección 5 = **1.252,5 kg**
**4.7.1 Acero columnas (kg)** → 8 columnas = **644,2 kg**
**4.8.1 Acero vigas cubierta (kg)** → sección 5 = **1.757,7 kg**
**4.9.1 Malla placa cubierta (kg)** → sección 5 = **783,3 kg**

### CAPÍTULO 5 — MAMPOSTERÍA

**5.1.1 Muros bloque No.4 (m²)** = longitud de muro × altura − vanos
`173.60 m × 3.00 m × 0.80 (descuento 20% de puertas/ventanas) = 416.64 m²`
(173.6 m = perímetro exterior ≈ 63.6 m + particiones interiores ≈ 110 m. **Este es el dato a verificar midiendo el plano de mampostería.**)

**5.1.2 Columneta No.5 (ml)** = N° columnetas × altura
`(173.60 / 1.5) ≈ 116 columnetas × 3.00 m = 348.0 ml`
(El plano de columnetas indica **una cada 1.5 m**, sección 0.20×0.15, refuerzo 2 Ø 1/2".)
(Se pone una columneta cada ≈3 m de muro, en esquinas e intersecciones.)

**5.1.4 Pañete impermeabilizado (m²)** = 65% del área de muro (fachadas + zonas húmedas)
`416.64 × 0.65 = 270.82 m²`

**5.2.1 Acero mampostería confinada (kg)** → sección 5 = **1.031,7 kg**

### CAPÍTULO 8 — PISOS

**8.1.1 Adoquín (m²)** = suma de las 9 áreas adoquinadas del plano = **115.30 m²**
(18.62 + 17.49 + 22.25 + 7.76 + 14.60 + 15.00 + 1.91 + 1.91 + 15.76)

---

## 4. Resumen de cantidades

| Ítem | Descripción | Und | Cantidad |
|---|---|---|---|
| 2.1.1 | Excavación máquina | m³ | 112.12 |
| 2.1.2 | Relleno subbase B-400 | m³ | 64.86 |
| 2.1.3 | Excavación manual | m³ | 7.48 |
| 2.1.4 | Relleno recebo | m³ | 43.24 |
| 2.1.6 | Geotextil NT 1600 | m² | 216.20 |
| 2.2.1 | Vigas cimentación concreto | m³ | 13.70 |
| 2.2.2 | Solado 1500 psi | m² | 38.05 |
| 2.3.1 | Acero vigas cimentación | kg | 1.302,6 |
| 4.1.1 | Columnas concreto | m³ | 8.04 |
| 4.2.1 | Vigas cubierta concreto | m³ | 15.22 |
| 4.3.1 | Contrapiso concreto | m³ | 21.62 |
| 4.3.3 | Placa aligerada cubierta | m² | 135.20 |
| 4.6.1 | Malla contrapiso | kg | 1.252,5 |
| 4.7.1 | Acero columnas | kg | 644,2 |
| 4.8.1 | Acero vigas cubierta | kg | 1.757,7 |
| 4.9.1 | Malla placa cubierta | kg | 783,3 |
| 5.1.1 | Muros bloque No.4 | m² | 416.64 |
| 5.1.2 | Columneta No.5 | ml | 348.0 |
| 5.1.4 | Pañete impermeabilizado | m² | 270.82 |
| 5.2.1 | Acero mampostería | kg | 1.031,7 |
| 8.1.1 | Adoquín | m² | 115.30 |

---

## 5. Cómo se calculó el ACERO (la cartilla de hierros)

El acero se mide en **kilogramos**. La idea es: cada varilla tiene un **peso por metro** según su diámetro; se suma la longitud de todas las varillas y se multiplica por su peso.

**Pesos por metro (tabla estándar):**

| Varilla | Diámetro | kg por metro |
|---|---|---|
| #2 | 1/4" | 0.250 |
| #3 | 3/8" | 0.560 |
| #4 | 1/2" | 0.994 |
| #5 | 5/8" | 1.552 |
| #6 | 3/4" | 2.235 |
| #7 | 7/8" | 3.042 |

**Pasos para cada elemento:**
1. Mirar el **despiece** del plano (ej: viga con `3#6 + 3#5` longitudinal y `estribos #3 c/0.20`).
2. **Refuerzo longitudinal:** (n° barras × peso/m) × longitud del elemento.
3. **Estribos:** contar cuántos caben (longitud/espaciamiento) × perímetro de cada estribo × peso/m.
4. Sumar y añadir **+10%** por desperdicio y traslapos.

### Ejemplo trabajado — Acero de vigas de cimentación (ítem 2.3.1)
Longitud total de vigas = 76.10 m; sección 0.40×0.45; refuerzo 3#6 + 3#5, estribos #3 c/0.20.

- **Longitudinal:** `76.10 × (3×2.235 + 3×1.552) = 76.10 × 11.36 = 864.6 kg`
- **Estribos #3 @0.20:**
  - cantidad = 76.10 / 0.20 = 381 estribos
  - longitud de 1 estribo (perímetro con recubrimiento + ganchos) ≈ `2×(0.30+0.35)+0.20 = 1.50 m`
  - peso = `381 × 1.50 × 0.560 = 319.6 kg`
- **Subtotal = 864.6 + 319.6 = 1.184,2 kg**
- **+10% = 1.302,6 kg** ✅

Lo mismo se hizo para columnas (644,2 kg), vigas de cubierta (1.757,7 kg) y columnetas (1.031,7 kg). Ver hoja **CARTILLA HIERROS** del Excel.

### Mallas electrosoldadas (ítems 4.6.1 y 4.9.1)
La malla 8 mm @0.15 en ambos sentidos pesa **5.27 kg/m²**:
`peso/m² = 2 × (1/0.15) × 0.395 kg/m = 5.27 kg/m²`
- Contrapiso: `216.20 × 5.27 × 1.10 = 1.252,5 kg`
- Cubierta: `135.20 × 5.27 × 1.10 = 783,3 kg`

---

## 6. Cómo se arma un APU (Análisis de Precio Unitario)

El APU responde: *¿cuánto cuesta hacer **1 unidad** de la actividad?* Suma 4 grupos:

```
APU = MATERIALES + MANO DE OBRA + EQUIPO + HERRAMIENTA MENOR (5% de la mano de obra)
```

El concepto difícil es el **rendimiento**: cuánto produce una cuadrilla en un día.
> Si una cuadrilla funde 8 m³ de concreto por día, entonces para 1 m³ gasta 1/8 = 0.125 días de cuadrilla.
> Ese 0.125 multiplicado por el costo/día de la cuadrilla da el costo de mano de obra por m³.

### Ejemplo trabajado — APU del adoquín (ítem 8.1.1), por m²

| Recurso | Cantidad por m² | Precio unitario | Parcial |
|---|---|---|---|
| Adoquín (50 und/m²) | 50 | $1.350 | $67.500 |
| Arena de cama | 0.05 m³ | $74.000 | $3.700 |
| Arena de sello | 0.01 m³ | $82.000 | $820 |
| Vibrocompactador (rend. 80 m²/día) | 1/80 día | $62.000 | $775 |
| Oficial (rend. 15 m²/día) | 1/15 día | $145.000 | $9.667 |
| Ayudante ×2 | 2/15 día | $105.000 | $14.000 |
| **Herramienta menor** (5% de la M.O.) | — | — | $1.183 |
| **TOTAL por m²** | | | **≈ $97.645** |

Así se hicieron los **19 APU**. La mano de obra (oficial $145.000/día, ayudante $105.000/día) se calculó del **salario mínimo 2026 ($1.750.905)** más el **factor prestacional ≈ 1.55** (prestaciones, salud, pensión, ARL, parafiscales).

---

## 7. Cómo se fijaron los precios de los insumos

- **Materiales:** precios de mercado 2026 de proveedores reales (Argos para concreto, ferreterías/figurado para acero, bloqueras del Huila, etc.). Cada uno con su **fuente** en la hoja INSUMOS.
- **Mano de obra:** a partir del SMLMV 2026 + factor prestacional.
- **Equipo:** tarifas de alquiler 2026.

> El enunciado pide "no inventar" los precios; por eso cada insumo tiene una fuente. Si necesitas cotizaciones con membrete, se reemplaza el precio en INSUMOS y todo se recalcula.

---

## 8. Cómo se calcula el total (costo directo → AIU → total)

1. **Costo directo** = suma de (cantidad × precio unitario) de las 21 líneas (los 19 ítems).
   → **$184.633.102**
2. **AIU** (sobre el costo directo):
   - Administración 8% = $14.770.648
   - Imprevistos 3% = $5.538.993
   - Utilidad 5% = $9.231.655
3. **IVA 19% sobre la utilidad** (obra pública, Art. 462-1 E.T.) = $1.754.014
4. **COSTO TOTAL** = costo directo + A + I + U + IVA = **$215.927.970**
   → ÷ 216 m² ≈ **$999.000/m²** de obra gris (valor coherente con el mercado).

---

## 9. Chuleta de fórmulas geométricas

| Elemento | Fórmula |
|---|---|
| Volumen de viga/columna/zapata | largo × ancho × alto |
| Volumen de placa/contrapiso | área × espesor |
| Área de muro/placa | largo × alto (o largo × ancho) |
| Área de excavación masiva | área en planta × profundidad |
| Acero longitudinal | n° barras × longitud × (kg/m del diámetro) |
| Estribos | (longitud/espaciamiento) × perímetro estribo × (kg/m) |
| Malla | área × densidad (kg/m²) |
| Desperdicio acero | × 1.10 (10%) |

---

### En resumen
1. Medir el plano → **cantidad**.
2. Armar el APU (material + obra + equipo + herramienta) → **precio unitario**.
3. cantidad × precio unitario → **valor del ítem**.
4. Sumar todo → **costo directo**, y agregar **AIU + IVA** → **total**.

Eso es exactamente lo que está en el Excel, y eso es lo que debes saber explicar. 💡

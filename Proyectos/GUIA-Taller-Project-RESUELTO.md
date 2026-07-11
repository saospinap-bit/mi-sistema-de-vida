# Taller MS Project — Proyecto casa primer piso (RESUELTO)

Este documento acompaña al archivo **`Parcial Project 2 - RESUELTO.xml`** (formato MSPDI que MS Project abre directamente). Explica la metodología y detalla todo lo que quedó cargado en Project, para que puedas **verificarlo y sustentarlo**.

## 1. Cómo abrir el archivo en MS Project

1. Abre Microsoft Project.
2. `Archivo > Abrir > Examinar`.
3. En tipo de archivo elige **XML (*.xml)** y selecciona `Parcial Project 2 - RESUELTO.xml`.
4. Acepta importar como **proyecto nuevo**. Verás el Gantt, la Hoja de recursos y las asignaciones ya cargadas.
5. Verifica el total en **Proyecto → Información del proyecto → Estadísticas**: debe dar **≈ $39.080.104**.

> **Nota importante sobre los materiales en el archivo entregado.**
> Al importar desde XML, MS Project interpreta mal las *unidades de material*, lo que
> disparaba el costo. Para que el **total quede exacto**, en este archivo los **materiales y
> los costos** se cargaron como **costo directo** (tipo *Costo*), y la **mano de obra** se
> dejó como *Trabajo* (tasa × horas) para conservar el **factor multiplicador**.
> El monto de cada material es el mismo (*Cantidad × (1+Desperdicio) × V. Unitario × CP*),
> como se detalla más abajo. Si tu profesor exige que los materiales figuren como tipo
> *Material* con su tasa, ábrelos en la Hoja de recursos y cambia el tipo a *Material*,
> poniendo Tasa = *V. Unitario* y en la tarea Unidades = la cantidad indicada en las tablas
> de la sección 3 (MS Project, ingresando los datos a mano, sí calcula bien).

## 2. Metodología usada (la del formato del profesor)

Todas las tareas quedan con **Duración fija** (como pide el enunciado). Cada actividad = un ítem del presupuesto; sus recursos salen del APU correspondiente.

| Tipo de recurso | En la Hoja de recursos | En la tarea (asignación) |
|---|---|---|
| **Material** | Tasa estándar = *V. Unitario* | Unidades = *Cantidad × (1+Desperdicio) × Cantidad presupuesto (CP)* |
| **Costo** | (sin tasa) | Se escribe **directo** el Costo = *V. Parcial × CP* |
| **Trabajo** (mano de obra) | Tasa estándar = *V. Unitario* | Se asigna **% de unidades = FACTOR MULTIPLICADOR** |

### El FACTOR MULTIPLICADOR (mano de obra)

Project calcula el costo de la mano de obra como *tasa × horas*, y las horas dependen de la duración. Como la duración es fija, para que el costo real del APU se refleje se asigna el recurso a un porcentaje de unidades:

```
F = costo real de la mano de obra en la actividad = V. Parcial × CP
D = V. Unitario × 8 (horas/día) × C (días = duración de la tarea)
FACTOR MULTIPLICADOR = F / D     (se ingresa como % en 'Unidades' de la asignación)
```

**Ejemplo (localización y replanteo, dur = 2 d):** mano de obra topográfica V.Unitario = $25,904/h.
- F = V.Parcial × CP = $18,651
- D = $25,904 × 8 × 2 = $414,471
- FACTOR = F/D = **4.50%** (0,72 h de trabajo) → costo $18,651.

## 3. Detalle por actividad (lo que quedó cargado)

### localización y replanteo

*CP = 72.0 m2 · Duración = 2 d · Valor ítem presupuesto = $127,656*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Puntilla 2" 1/2 a 3" 1/2 | Material | $2,100 | 0.720 lb | $1,512 |
| Madera medio cerco | Material | $3,900 | 14.400 ml | $56,160 |
| Herramienta menor | Costo | (costo directo) | — | $933 |
| Equipo topografico precision | Costo | (costo directo) | — | $50,400 |
| Mano de obra cuadrilla topografica | Trabajo | $25,904/h | 4.50 % | $18,651 |
| **TOTAL** |  |  |  | **$127,656** |

### Excavacion

*CP = 7.12 m3 · Duración = 2 d · Valor ítem presupuesto = $208,944*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Herramienta menor 2 | Costo | (costo directo) | — | $9,950 |
| Mano de obra cuadrilla aa | Trabajo | $15,527/h | 80.10 % | $198,995 |
| **TOTAL** |  |  |  | **$208,945** |

### Retiro material sobrante

*CP = 5.53 m3 · Duración = 1 d · Valor ítem presupuesto = $92,368*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Escombrera | Costo | (costo directo) | — | $23,038 |
| mano de obra cuadrilla aa | Trabajo | $15,527/h | 27.65 % | $34,346 |
| volqueta | Costo | (costo directo) | — | $33,268 |
| Herramienta menor 3 | Costo | (costo directo) | — | $1,717 |
| **TOTAL** |  |  |  | **$92,370** |

### SOLADO e=0.05m

*CP = 26.87 m2 · Duración = 4 d · Valor ítem presupuesto = $522,457*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Mezcla de concreto pobre de 3000psi | Material | $277,197 | 1.411 m3 | $391,035 |
| mano de obra cuadrilla aa | Trabajo | $15,527/h | 25.19 % | $125,164 |
| Herramienta menor 4 | Costo | (costo directo) | — | $6,258 |
| **TOTAL** |  |  |  | **$522,457** |

### RELLENO Y COMPACTACION MATERIAL IMPORTADO

*CP = 8.2 m2 · Duración = 3 d · Valor ítem presupuesto = $262,236*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Material de rio sucio-tierra | Material | $8,000 | 9.840 m3 | $78,720 |
| Mano de obra albeñeleria 1A | Trabajo | $6,500/h | 68.33 % | $106,600 |
| Pison | Costo | (costo directo) | — | $2,296 |
| Volqueta transporte petreos 1-10 km | Costo | (costo directo) | — | $74,620 |
| **TOTAL** |  |  |  | **$262,236** |

### Figurado y armada acero 60000 psi vaciado zapatas en concreto de 3000 psi

*CP = 823.45 kg · Duración = 6 d · Valor ítem presupuesto = $2,919,056*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Acero de 420 Mpa | Material | $2,083 | 848.154 kg | $1,766,984 |
| Alambre negro | Material | $3,500 | 65.876 kg | $230,566 |
| Mano de obra cuadrilla aa | Trabajo | $15,527/h | 102.93 % | $767,145 |
| Segueta sin marco | Material | $3,522 | 32.938 glb | $116,008 |
| Herramienta menor 5 | Costo | (costo directo) | — | $38,357 |
| **TOTAL** |  |  |  | **$2,919,060** |

### VIGA DE CIMENTACION DE 3000 PSI (0.25 X 0.25) (m3)

*CP = 3.38 m2 · Duración = 1 d · Valor ítem presupuesto = $1,871,279*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Puntilla 2" 1/2 a 3" 1/2 | Material | $2,100 | 3.380 lbs | $7,098 |
| Tabla 1x 10 x 300 otobo | Material | $10,600 | 18.590 und | $197,054 |
| Vareta 2" x 2" x 3m otobo | Material | $3,200 | 9.025 Hrs | $28,879 |
| Mezcla concreto 3000 psi | Material | $337,000 | 3.549 m3 | $1,196,013 |
| Mano de obra cuadrilla aa 2+1 | Trabajo | $20,839/h | 249.28 % | $415,575 |
| vibrador electrico | Costo | (costo directo) | — | $5,881 |
| Herramienta menor 6 | Costo | (costo directo) | — | $20,779 |
| **TOTAL** |  |  |  | **$1,871,279** |

### LOSA DE CONTRAPISO

*CP = 72.0 m2 · Duración = 1 d · Valor ítem presupuesto = $4,143,024*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Puntilla 2" | Material | $2,000 | 14.400 lb | $28,800 |
| Tabla 1 x 10 x 300 | Material | $8,500 | 72.000 U | $612,000 |
| Mezcla de concreto 1:2:3 21 Mpa | Material | $337,000 | 8.280 m3 | $2,790,360 |
| Mano de obra albañeleria 3a 1o | Trabajo | $28,600/h | 225.00 % | $514,800 |
| Vibrador electrico | Costo | (costo directo) | — | $50,400 |
| Volqueta transporte petreos 1-10 km | Costo | (costo directo) | — | $113,400 |
| Herramienta menor 7 | Costo | (costo directo) | — | $33,264 |
| **TOTAL** |  |  |  | **$4,143,024** |

### Figurado y armada acero de Columnas primer piso

*CP = 449.6 kg · Duración = 4 d · Valor ítem presupuesto = $1,593,792*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Acero de 420 Mpa | Material | $2,083 | 463.088 Kg | $964,765 |
| Alambre negro | Material | $3,500 | 35.968 Kg | $125,888 |
| Mano de Obra cuadrilla aa | Trabajo | $15,527/h | 84.30 % | $418,858 |
| Segueta sin marco | Material | $3,522 | 17.984 glb | $63,340 |
| Herramienta menor 8 | Costo | (costo directo) | — | $20,943 |
| **TOTAL** |  |  |  | **$1,593,794** |

### Encofrado y vaciado columnar primer piso

*CP = 2.53 m2 · Duración = 4 d · Valor ítem presupuesto = $1,408,542*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Mezcla concreto de 3000 psi | Material | $337,000 | 2.606 m3 | $878,188 |
| formaleta | Costo | (costo directo) | — | $108,368 |
| andamios | Costo | (costo directo) | — | $8,804 |
| Herramienta menor 9 | Costo | (costo directo) | — | $19,508 |
| vibrador electrico | Costo | (costo directo) | — | $3,522 |
| mano de obra cuadrilla aa 2+1 | Trabajo | $20,839/h | 58.51 % | $390,152 |
| **TOTAL** |  |  |  | **$1,408,542** |

### Figurado y armado acero losa de contrapiso

*CP = 252.72 kg · Duración = 2 d · Valor ítem presupuesto = $895,870*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Acero de 420 Mpa | Material | $2,083 | 260.302 Kg | $542,294 |
| Alambre negro | Material | $3,500 | 20.218 Kg | $70,762 |
| mano de obra cuadrilla aa | Trabajo | $15,527/h | 94.77 % | $235,440 |
| Segueta sin marco | Material | $3,522 | 10.109 Glb | $35,603 |
| Herramienta menor 10 | Costo | (costo directo) | — | $11,772 |
| **TOTAL** |  |  |  | **$895,871** |

### Losa de entrepiso concreto de 3000 psi e=0.05m incluye encofrado

*CP = 62.1 m2 · Duración = 10 d · Valor ítem presupuesto = $4,943,736*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Mezcla concreto de 3000 psi | Material | $337,000 | 6.390 m3 | $2,153,460 |
| Caseton de guadua | Material | $9,726 | 43.470 Un | $422,811 |
| Formaleta | Costo | (costo directo) | — | $189,874 |
| Andamio | Costo | (costo directo) | — | $10,805 |
| Herramienta menor 11 | Costo | (costo directo) | — | $99,064 |
| Vibrador electrico | Costo | (costo directo) | — | $86,443 |
| mano de obra cuadrilla aa 3+1 | Trabajo | $26,151/h | 94.70 % | $1,981,278 |
| **TOTAL** |  |  |  | **$4,943,736** |

### Muro en bloque ceramico

*CP = 140.28 m3 · Duración = 8 d · Valor ítem presupuesto = $6,099,771*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Impermeable sika imprimante | Material | $6,200 | 42.084 Kg | $260,921 |
| Bloque ceramico | Material | $680 | 4,334.652 Un | $2,947,563 |
| Mortero de pega 1:4 | Material | $312,000 | 2.806 m3 | $875,347 |
| Herramienta menor 12 | Costo | (costo directo) | — | $81,253 |
| Mezcla grouting 3000psi | Material | $337,000 | 0.867 m3 | $292,156 |
| Andamio | Costo | (costo directo) | — | $17,086 |
| mano de obra cuadrilla aa 5 | Trabajo | $11,587/h | 219.19 % | $1,625,445 |
| **TOTAL** |  |  |  | **$6,099,771** |

### Pañete en interiores primer piso, e= 0.02 m, 1:3

*CP = 195.49 m2 · Duración = 6 d · Valor ítem presupuesto = $3,600,416*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Mortero de pega 1:4 | Material | $312,000 | 6.158 m3 | $1,921,276 |
| mano de obra cuadrilla aa 6 | Trabajo | $15,527/h | 183.27 % | $1,365,923 |
| Herramienta menor 13 | Costo | (costo directo) | — | $68,296 |
| Andamio | Costo | (costo directo) | — | $21,504 |
| Volqueta transporte materiales petreos | Costo | (costo directo) | — | $223,417 |
| **TOTAL** |  |  |  | **$3,600,416** |

### Suministro e instalación perfil cajón hr 120x60mm

*CP = 105.6 m · Duración = 3 d · Valor ítem presupuesto = $4,727,247*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Thinner | Material | $15,500 | 5.280 Gls | $81,840 |
| Anticorrosivo rojo | Material | $24,000 | 8.448 Gls | $202,752 |
| Soldadura 6011 x 1/8” | Material | $8,100 | 17.530 Kg | $141,990 |
| Perfil hr c120mmx60mm‑1.5 | Material | $56,900 | 35.904 Und | $2,042,938 |
| Mano obra albañilería 2 ayudante | Trabajo | $10,625/h | 22.00 % | $56,099 |
| Mano obra carp.taller ayudante‑1 ofi | Trabajo | $23,370/h | 220.00 % | $1,233,930 |
| Mano obra pintura 1 ayudante‑1 ofi | Trabajo | $17,324/h | 44.00 % | $182,940 |
| Pulidora con piedra o disco | Costo | (costo directo) | — | $219,648 |
| Soldador eléctrico | Costo | (costo directo) | — | $363,686 |
| Oxicorte (oxígeno‑acetileno) | Costo | (costo directo) | — | $116,160 |
| Andamio metálico tubular | Costo | (costo directo) | — | $11,616 |
| Herramienta menor 14 | Costo | (costo directo) | — | $73,649 |
| **TOTAL** |  |  |  | **$4,727,248** |

### Suministro e instalación lámina policarbonato alveolar

*CP = 65.2 m · Duración = 6 d · Valor ítem presupuesto = $4,182,005*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Torn autoge. 3/4x‑3/16 | Material | $252 | 65.200 Und | $16,430 |
| Lámina policarbonato 8 mm | Material | $552,900 | 5.400 Und | $2,985,585 |
| Remate u 6x2010 mm policarb | Material | $8,750 | 10.106 Und | $88,428 |
| Silicona transparent. 11 oz | Material | $8,900 | 0.652 Und | $5,803 |
| Cinta aluminio industrial | Material | $61,000 | 1.956 Und | $119,316 |
| Mano obra albañilería 2 ayudante‑1 ofi | Trabajo | $20,839/h | 88.29 % | $883,165 |
| Herramienta menor 15 | Costo | (costo directo) | — | $44,158 |
| Andamio metálico tubular | Costo | (costo directo) | — | $35,860 |
| Cruceta andamio | Costo | (costo directo) | — | $3,260 |
| **TOTAL** |  |  |  | **$4,182,005** |

### Suministro e instalación de canaletas

*CP = 12.0 m · Duración = 1 d · Valor ítem presupuesto = $969,881*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Igas gris (sellante) 5 kg | Material | $13,100 | 1.440 Kg | $18,864 |
| Canaleta 43 de 4.00 | Material | $115,810 | 7.200 Und | $833,832 |
| Torn met. Canaleta 43 | Material | $2,600 | 7.200 Und | $18,720 |
| Mano obra albañilería 3 ayudante‑1 oficina | Trabajo | $26,151/h | 30.00 % | $62,763 |
| Herramienta menor 16 | Costo | (costo directo) | — | $31,382 |
| Andamio metálico tubular | Costo | (costo directo) | — | $3,960 |
| Cruceta andamio | Costo | (costo directo) | — | $360 |
| **TOTAL** |  |  |  | **$969,881** |

### Bajante aguas lluvias

*CP = 16.2 m · Duración = 1 d · Valor ítem presupuesto = $511,813*

| Recurso | Tipo | Tasa / Costo | Unidades / Factor | Costo |
|---|---|---|---|---|
| Bajante pvc cuadrado | Material | $63,896 | 5.395 Und | $344,693 |
| Bajante pvc soporte | Material | $2,700 | 24.300 Und | $65,610 |
| Soldadura pvc 1/4 gls | Material | $78,400 | 0.162 Und | $12,701 |
| Torn p/mad 1 x 6 | Material | $29 | 48.600 Und | $1,409 |
| Limpiador pvc 760‑g 1/4 gl | Material | $38,400 | 0.162 Und | $6,221 |
| Mano obra albañilería 1 ayudante‑1 ofi | Trabajo | $15,527/h | 60.75 % | $75,462 |
| Herramienta menor 17 | Costo | (costo directo) | — | $3,773 |
| Andamio metálico tubular | Costo | (costo directo) | — | $1,782 |
| Cruceta andamio | Costo | (costo directo) | — | $162 |
| **TOTAL** |  |  |  | **$511,813** |

## 4. Verificación de costos

- **Costo total del cronograma (Project): $39,080,102**
- Cada actividad coincide exactamente con el *Valor del ítem en el presupuesto* del APU.
- La celda TOTAL de la hoja PRESUPUESTO marca $38.952.435, pero esa fórmula **dejó por fuera la actividad 'localización y replanteo' ($127,656)**. Sumando las 18 actividades el total correcto es **$39,080,102**. Conviene mencionarlo en la sustentación.

## 5. Hoja de recursos

Se crearon los recursos únicos con su tipo (Material / Costo / Trabajo) y su tasa. La mano de obra y los materiales llevan tasa; los recursos tipo **Costo** (herramienta menor, equipos, andamios, volquetas, etc.) no llevan tasa porque su valor se carga directo en la tarea.


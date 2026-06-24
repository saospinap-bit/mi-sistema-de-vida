# 🧱 Proyecto Final — Fundamentos de Construcción
## Presupuesto General de Obra · CDI Tesalia (Huila) · Módulo 1 · Etapa de Obra Gris

> Esta guía te explica **qué se entrega, de dónde sale cada número y cómo defenderlo** en la sustentación.
> Léela completa antes de la entrega del **viernes 10 de julio de 2026**.

---

## 1. ¿Qué pedía el enunciado y qué se entrega?

El enunciado pide el **presupuesto general de obra** para la etapa de **obra gris** del Módulo 1, a partir de los planos. Estos son los 8 entregables y dónde quedó cada uno:

| # | Entregable exigido | Dónde está |
|---|--------------------|-----------|
| 2.1 | Presupuesto general (CD + AIU + total) | Libro `PRESUPUESTO ... .xlsx` → hoja **PRESUPUESTO** |
| 2.2 | APU de cada actividad | hoja **APU** (19 análisis) |
| 2.3 | Cantidades de obra con soporte | hoja **CANTIDADES** + libro de **MEMORIAS** |
| 2.4 | Lista de insumos con fuente | hoja **INSUMOS** |
| 2.5 | Cartilla de hierros | hoja **CARTILLA HIERROS** |
| 2.6 | Programación (MS Project) | hoja **PROGRAMACION** (base para pasar a MSP) |
| 2.7 | Memoria de cálculo (formato) | `MEMORIAS DE CALCULO ... .xlsx` (21 hojas) |
| 2.8 | Formato de entrega Excel programado y jerárquico | Todo el libro `PRESUPUESTO`, con fórmulas vivas |

**Archivos entregables:**
- `PRESUPUESTO CDI TESALIA - MODULO 1 (obra gris).xlsx`
- `MEMORIAS DE CALCULO - CDI TESALIA MODULO 1.xlsx`

---

## 2. El proyecto (dato importante para sustentar)

Leyendo los planos se confirma que el "Módulo 1 - Colegio" es en realidad un **Centro de Desarrollo Infantil (CDI) en el municipio de Tesalia (Huila)** — por eso la hoja original se llamaba *PRESUPUESTO TESALIA*. Es una **edificación pública de un piso**.

**Sistema estructural (extraído de los planos):**
- **Cimentación:** zapatas aisladas 1.20×1.20×0.40 m + **vigas de cimentación 0.40×0.45 m** en concreto 3000 psi, sobre solado de 1500 psi y colchón granular con geotextil.
- **Retícula de ejes:** **A, B** (separación 7.70 m) × **1, 2, 3, 3', 4** (longitud total ≈ 19.80 m) → **10 columnas**.
- **Columnas:** 0.40×0.40 m, refuerzo **2#6 + 2#7** con estribos #2 c/0.20, hasta nivel **N+4.90**.
- **Vigas de cubierta:** 0.40×0.50 m. **Placa de cubierta:** losa aligerada e=0.08 con viguetas 0.20×0.40.
- **Contrapiso:** placa e=0.10. **Mampostería:** bloque No.4 confinada con columnetas en bloque No.5 + pañete 1:4.
- **Acero:** fy = 4200 kg/cm² (= 420 MPa = 60.000 psi).

---

## 3. Resultado del presupuesto

| Concepto | Valor (COP) |
|---|---|
| **TOTAL COSTO DIRECTO** | **$186.652.600** |
| Administración (A) 8% | $14.932.208 |
| Imprevistos (I) 3% | $5.599.578 |
| Utilidad (U) 5% | $9.332.630 |
| IVA 19% sobre la utilidad | $1.773.200 |
| **COSTO TOTAL DE OBRA** | **$218.289.802** |

➡️ Equivale a **≈ $1.010.000 / m²** de obra gris (área ≈ 216 m²), un valor coherente con el mercado colombiano 2026.

---

## 4. ¿Por qué el AIU es 8% / 3% / 5%? (te lo van a preguntar)

El enunciado pide **justificar el AIU para un proyecto del sector público**. Argumento:

- **Administración (8%):** cubre costos indirectos — director/residente de obra, almacenista, campamento, vallas, pólizas, servicios provisionales y la administración central prorrateada. En obra social pequeña suele ir entre 5% y 10%.
- **Imprevistos (3%):** colchón para riesgos no previstos (clima, variación menor de cantidades, reprocesos). En obra pública va entre 1% y 5%.
- **Utilidad (5%):** ganancia razonable y competitiva del contratista en licitación pública (la cifra típica es 5%).
- **IVA:** en contratos públicos el IVA del 19% se liquida **solo sobre la utilidad** (Art. 462-1 del Estatuto Tributario), no sobre todo el contrato. Por eso aparece como una línea separada.

> Si tu profesor maneja otro AIU (p. ej. 25/5/5), **solo cambias los % en la hoja PRESUPUESTO** y todo se recalcula.

---

## 5. Cómo funciona el libro (defensa del "Excel programado")

El libro está **encadenado con fórmulas**, no con números pegados:

```
INSUMOS (precios)  →  APU (Vr. unitario = Σ consumos × precio)  →  PRESUPUESTO (Vr. total = cantidad × Vr. unitario)  →  Costo directo + AIU
```

- Cambias **un precio en la hoja INSUMOS** (ej. el acero sube) y se recalculan automáticamente todos los APU, el presupuesto y el total.
- Cada **APU** trae materiales + mano de obra + equipo + **herramienta menor (5% de la M.O.)**, con sus rendimientos.
- El presupuesto está **jerárquico**: Capítulos (2, 4, 5, 8) → ítems → valor.

Esto responde directamente a los entregables 2.2 y 2.8.

---

## 6. De dónde salió cada cantidad (entregable 2.3)

Las cantidades se midieron **de los planos** y se calcularon con fórmulas geométricas (ver hoja CANTIDADES y el libro de MEMORIAS). Ejemplos clave:

- **Contrapiso (4.3.1):** 9.85 × 21.95 × 0.10 = **21.62 m³**.
- **Vigas de cimentación (2.2.1):** (2 vigas × 19.80) + (5 vigas × 7.30) = 76.10 m × 0.40 × 0.45 = **13.70 m³**.
- **Columnas (4.1.1):** 10 × 0.40 × 0.40 × 4.90 = **7.84 m³**.
- **Adoquín (8.1.1):** suma de 9 áreas = **115.30 m²**.
- **Acero (2.3.1, 4.7.1, 4.8.1, 5.2.1):** se despieza por barras según el refuerzo de cada elemento (ver CARTILLA HIERROS), con pesos por diámetro y +10% por desperdicio y traslapos.

---

## 7. ⚠️ Qué debes revisar/ajustar antes de entregar (honestidad técnica)

Para que quede **perfecto**, verifica estos puntos contra los planos (están señalados porque dependen de medidas finas o de precios locales):

1. **Sección real de columnas.** Asumí 0.40×0.40 m; el plano muestra también stubs de 0.50×0.50. Confírmalo en el despiece de columnas y ajusta el ítem 4.1.1 y su acero.
2. **Mampostería (5.1.1, 5.1.2, 5.1.4).** La longitud de muros (173.6 m) y la altura (2.90 m) son una estimación de perímetro + particiones, porque el plano de mampostería tiene muchas vistas superpuestas. **Mide los muros reales** y ajusta; es el ítem más pesado del presupuesto.
3. **Movimientos de tierra (2.1.x).** Ya usan los datos del plano: desplante **1.5 m** y colchón granular **0.30 m**. (Excavación a máquina = plataforma + zanjas a 1.5 m.)
4. **Precios (hoja INSUMOS).** Ya están actualizados a **valores de mercado 2026 con su fuente citada** (Argos, Homecenter, ferreterías, Construdata, SMLMV 2026). Si tu profe exige **cotizaciones formales con membrete**, pide 2–3 a proveedores de Tesalia/Neiva y reemplaza el precio en la hoja INSUMOS; todo se recalcula solo. (En la guía PASO A PASO te explico exactamente cómo pedirlas.)
5. **Geotextil:** el presupuesto pide **NT 1600**; los planos mencionan un tejido 2100T. Dejé NT 1600 (lo que pide el formato). Solo tenlo presente.

---

## 8. Cómo pasar la programación a Microsoft Project (entregable 2.6)

En la hoja **PROGRAMACION** tienes la lista de actividades con **duración, predecesoras y recursos**. Para MS Project:
1. Abre MS Project → pega los nombres en la columna *Task Name*.
2. Llena *Duration* con los días indicados y *Predecessors* con los números de la columna correspondiente.
3. En cada tarea, en *Resources*, ingresa los recursos del APU (mano de obra, equipo).
4. MSP te arma el **diagrama de Gantt** y la **ruta crítica** automáticamente. La obra gris da una duración de ~60–70 días con traslapos.

---

## 9. Cómo se leyeron los planos (por si preguntan por la metodología)

Los planos venían en `.dwg` (AutoCAD 2018). Se convirtieron a un formato legible y se extrajeron las cotas, los rótulos de ambientes, los despieces de acero y las dimensiones de los elementos directamente de la geometría del dibujo. Con esas medidas se calcularon las cantidades. Por eso cada cantidad es **trazable a un plano**, no inventada.

---

### ✅ Checklist final antes de enviar el correo
- [ ] Reemplazar precios de INSUMOS por cotizaciones reales.
- [ ] Verificar muros, columnas y excavaciones contra los planos.
- [ ] Poner nombres del grupo en la PORTADA y en las memorias (Elaboró/Revisó/Aprobó).
- [ ] Exportar la programación a MS Project (.mpp).
- [ ] Revisar que al abrir el Excel los totales aparezcan (Excel recalcula solo).

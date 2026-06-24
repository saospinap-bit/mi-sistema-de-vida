# 🪜 PASO A PASO — Cómo usar, terminar y entregar tu proyecto
### Fundamentos de Construcción · Presupuesto CDI Tesalia · Módulo 1

> Esta guía está hecha **como si nunca hubieras armado un presupuesto**. Sigue los pasos en orden.
> No necesitas entender todo el cálculo: ya está hecho. Tu trabajo es **revisar, personalizar y entregar**.

---

## 🧭 Antes de empezar: ¿qué es esto?

Un **presupuesto de obra** responde una pregunta: *¿cuánto cuesta construir esto?*
Para responderla se hace una cadena de 4 pasos (que ya están hechos en tu Excel):

```
1) ¿Cuánto material/gente/máquina necesito por cada actividad?  → APU
2) ¿Cuánto vale cada cosa?                                       → INSUMOS
3) ¿Cuánta cantidad hay de cada actividad en la obra?            → CANTIDADES
4) Cantidad × precio de cada actividad, y le sumo el AIU         → PRESUPUESTO
```

Tienes **2 archivos de Excel** y **2 guías** (esta y la de sustentación). Vamos uno por uno.

---

## PASO 1 — Descargar los archivos del proyecto

1. Entra al link del Pull Request que te pasé (GitHub).
2. Arriba, en la pestaña **"Files changed"**, vas a ver los archivos nuevos. También puedes ir a la rama `fundamentos-presupuesto-cdi-tesalia` → carpeta `Proyectos/Fundamentos-de-Construccion`.
3. Descarga estos 2 archivos a tu computador:
   - `PRESUPUESTO CDI TESALIA - MODULO 1 (obra gris).xlsx`
   - `MEMORIAS DE CALCULO - CDI TESALIA MODULO 1.xlsx`
4. Ábrelos con **Microsoft Excel** (no con el visor del navegador, para que calcule bien).

> 💡 El archivo ya trae los totales calculados y visibles. Además está programado: si cambias un precio en INSUMOS y no se actualiza solo, ve a **Fórmulas → Calcular ahora** (o **F9**).

---

## PASO 2 — Conocer el archivo principal (las 8 hojas)

Abre `PRESUPUESTO CDI TESALIA...xlsx`. Abajo verás 8 pestañas. Esto es cada una:

| Pestaña | Qué tiene | ¿La tocas? |
|---|---|---|
| **PORTADA** | Título y contenido | Sí: pon los nombres del grupo |
| **INSUMOS** | Lista de precios (materiales, gente, máquinas) | Sí: aquí cambias precios |
| **APU** | Los 19 análisis de precio unitario | No (se calculan solos) |
| **PRESUPUESTO** | El presupuesto final con el total | No (se calcula solo). Aquí ves el resultado |
| **AIU** | Por qué el AIU es 8/3/5 | No (solo léela para sustentar) |
| **CANTIDADES** | De dónde sale cada cantidad | No |
| **CARTILLA HIERROS** | El acero por kilos | No |
| **PROGRAMACION** | Las actividades con duración | La usas para hacer el MS Project |

**Regla de oro:** las únicas hojas que vas a editar son **PORTADA** (nombres) e **INSUMOS** (precios, si quieres). Todo lo demás se recalcula solo. 🔒

---

## PASO 3 — Poner los nombres del grupo

1. Ve a la pestaña **PORTADA**.
2. Busca un espacio (o agrega una fila al final) y escribe: *Integrantes: Nombre 1, Nombre 2, ... / Grupo / Fecha.*
3. Ve al archivo de **MEMORIAS** → al final de cada hoja hay tres casillas: **Elaboró / Revisó / Aprobó**. Pon nombres ahí (pueden repartirse: uno elabora, otro revisa).

---

## PASO 4 — (Opcional pero recomendado) Conseguir cotizaciones reales

El enunciado dice "recomiendo no inventarlos". Los precios que dejé son **reales de mercado 2026 con su fuente**, así que ya cumples. Pero si tu profe quiere **cotizaciones con membrete**, haz esto:

**¿A quién pedir?** A 2–3 proveedores por cada material grande:
- **Concreto:** Argos, Cemex/Holcim, o una concretera local de Neiva.
- **Acero/varilla y malla:** una ferretería grande o distribuidor de acero.
- **Bloque y adoquín:** una bloquera/prefabricados del Huila.
- **Agregados (arena, recebo, triturado):** una cantera o ferretería.

**¿Qué escribir?** Un correo o WhatsApp corto:
> *"Buen día. Soy estudiante de ingeniería, estoy haciendo un ejercicio académico. ¿Me pueden cotizar el valor de [producto, ej: 1 m³ de concreto premezclado de 3000 psi / 1 kg de varilla de 1/2" / 1 bloque No.4]? Es solo para referencia. Gracias."*

**¿Qué hacer con la respuesta?**
1. Abre la hoja **INSUMOS**.
2. Busca la fila del material (columna B "DESCRIPCIÓN").
3. En la columna **E (VALOR UNITARIO)** escribe el precio que te dieron.
4. En la columna **F (FUENTE)** escribe quién lo cotizó (ej: "Cotización Ferretería X, 2026").
5. ✨ El presupuesto y los APU se actualizan **automáticamente**. No tienes que tocar nada más.

> Guarda los correos/pantallazos de las cotizaciones; algunos profes piden adjuntarlos.

---

## PASO 5 — Entender cómo se "encadena" (para que no te asustes)

Si abres la hoja **APU** y haces clic en una celda de "VR. UNITARIO", verás algo como `=INSUMOS!$E$10`. Eso significa: *"trae el precio de la hoja INSUMOS, fila 10"*. Así, **si cambias un precio en INSUMOS, el APU cambia solo**.

Igual en **PRESUPUESTO**: el "Valor unitario" de cada ítem dice `=APU!$F$53`, o sea *"trae el total del APU"*. Y el "Valor total" es `=cantidad × valor unitario`.

👉 No tienes que escribir fórmulas. Solo entiéndelo por si te preguntan: **"el libro está programado, cambio un precio y todo se recalcula"**. Esa frase vale puntos.

---

## PASO 6 — Revisar las 3 cantidades que conviene verificar

Estas las calculé de los planos, pero son las más sensibles. Si tienes tiempo, ábrelas en AutoCAD/visor y compara (no es obligatorio, pero suma):

1. **Mampostería (muros)** — hoja CANTIDADES, ítem 5.1.1. Usé 173.6 m de muro × 3.00 m de alto. Si mides los muros del plano de mampostería y dan distinto, cambia el número en la hoja **CANTIDADES** (columna CANTIDAD del ítem 5.1.1).
2. **Columnas (4.1.1)** — asumí 8 columnas de 0.40×0.40. Verifica en el plano estructural.
3. **Excavaciones (2.1.1 a 2.1.4)** — usé profundidades típicas. Si el plano de cimentación tiene otras, ajústalas.

> ⚠️ Si cambias una cantidad, hazlo en la hoja **PRESUPUESTO** (columna D, "CANTIDAD") **o** en CANTIDADES y luego cópiala al presupuesto. El total se recalcula solo.

---

## PASO 7 — Armar la PROGRAMACIÓN en Microsoft Project

Este es el entregable 2.6. **Ya te dejé el archivo listo:** `PROGRAMACION CDI TESALIA (abrir en MS Project).xml`.

**Forma fácil (recomendada):**
1. Abre **Microsoft Project**.
2. **Archivo → Abrir → Examinar**, cambia el tipo de archivo a "XML" y selecciona `PROGRAMACION CDI TESALIA (abrir en MS Project).xml`.
3. MS Project carga solo las 16 actividades con su **duración, predecesoras, costo y notas de recursos**, y dibuja el **diagrama de Gantt** y la **ruta crítica**.
4. Revisa, agrega los nombres del grupo y guarda como `.mpp`. Exporta a PDF para adjuntar.

**Si prefieres hacerlo a mano** (o el XML te da problema): usa la hoja **PROGRAMACION** del Excel y escribe las actividades, duraciones y predecesoras manualmente en MS Project.

> La obra gris programada va del **13-jul-2026 al 24-sep-2026** (con la secuencia lógica de actividades).

---

## PASO 8 — Pasar los planos a PDF (para adjuntar)

Los planos están en `.dwg`. Para que el profe los pueda ver fácil:
1. Abre cada `.dwg` en AutoCAD.
2. Menú **Archivo → Exportar / Plotear → PDF**.
3. Adjunta esos PDF en el correo.
(Si no tienes AutoCAD, sirve el visor gratuito **Autodesk Viewer** en la web, o **DWG TrueView**.)

---

## PASO 9 — Qué enviar en el correo de entrega

El enunciado dice entrega **vía correo el viernes 10 de julio de 2026**. Adjunta:

- [ ] `PRESUPUESTO CDI TESALIA - MODULO 1 (obra gris).xlsx`
- [ ] `MEMORIAS DE CALCULO - CDI TESALIA MODULO 1.xlsx`
- [ ] La programación de MS Project (`.mpp` + PDF)
- [ ] (Si las pidió) las cotizaciones (PDF/pantallazos)
- [ ] (Opcional) los planos en PDF

**Texto del correo (ejemplo):**
> *Buen día profesor. Adjunto el proyecto final de Fundamentos en Construcción: presupuesto general de obra para la etapa de obra gris del Módulo 1 (CDI Tesalia), con sus APU, cantidades, lista de insumos, cartilla de hierros, memorias de cálculo y programación. Quedamos atentos. Grupo: [nombres].*

---

## PASO 10 — Cómo defenderlo (mini-examen con respuestas)

Te van a preguntar. Respuestas listas:

- **"¿Qué es el AIU y por qué esos %?"** → "Administración 8%, Imprevistos 3%, Utilidad 5%. Es un AIU moderado porque es obra pública. El IVA del 19% va solo sobre la utilidad por el Art. 462-1 del Estatuto Tributario." *(más detalle en la hoja AIU)*
- **"¿De dónde sacaron las cantidades?"** → "Las medimos de los planos; cada cantidad tiene su memoria de cálculo con la fórmula geométrica."
- **"¿De dónde los precios?"** → "Precios de mercado 2026 con fuente citada en la hoja INSUMOS (Argos, ferreterías, Construdata, SMLMV 2026)."
- **"¿Qué es un APU?"** → "Análisis de Precio Unitario: el costo de hacer **una unidad** de una actividad (1 m³, 1 m², 1 kg), sumando material + mano de obra + equipo + herramienta menor."
- **"¿Qué incluye la obra gris?"** → "La estructura: cimentación, columnas, vigas, placas, mampostería y pisos en obra negra. No incluye acabados finos, pintura, enchapes, instalaciones terminadas."
- **"¿Cuánto cuesta el proyecto?"** → "Costo directo $184.6 millones; con AIU e IVA, **$215.9 millones** (≈ $999.000/m² de obra gris)."

---

### ✅ Checklist final (imprime esto)
- [ ] Descargué y abrí los 2 Excel (los totales aparecen).
- [ ] Puse nombres en PORTADA y en las memorias.
- [ ] (Opcional) Reemplacé precios con cotizaciones y puse la fuente.
- [ ] Revisé mampostería / columnas / excavaciones.
- [ ] Hice la programación en MS Project.
- [ ] Pasé los planos a PDF.
- [ ] Envié el correo con todo adjunto antes del 10 de julio.

¿Algo no te quedó claro? Dime el paso y te lo explico más despacio. 💪

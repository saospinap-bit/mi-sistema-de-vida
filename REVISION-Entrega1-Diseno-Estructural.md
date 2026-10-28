# Revisión de la memoria — Proyecto final Grupo 2, primera entrega

Revisión del archivo `Proyecto_final_grupo_2_entrega1.docx` contra el anexo del
proyecto (`Proyectos/Diseno-Estructural/Anexo-Proyecto_Diseño_Estructural (2).pdf`)
y contra el Título A de la NSR-10.

---

## 0. Lo primero al abrir el archivo

Los 85 rótulos ya traen su número grabado: **Tabla 1 a 50** e **Ilustración 1 a 35**.
Se ven correctos desde que se abre el archivo, sin tener que actualizar nada.

Lo único que hay que refrescar son las **tres listas** (tabla de contenido, lista
de ilustraciones y lista de tablas), porque los números de página los calcula
Word con su propia paginación:

1. Clic derecho sobre cada lista → **Actualizar campos** → **Actualizar toda la tabla**.
2. Si algún número de página queda en 1, repetir una vez más: en la primera pasada
   Word a veces todavía no ha paginado el documento.

También funciona `Ctrl + E` (seleccionar todo) y luego `F9`, que actualiza las tres
de un golpe. Es seguro hacerlo cuantas veces quieran: los campos `SEQ` devuelven
exactamente los mismos números que ya están grabados.

> Nota: en la primera versión de esta revisión los 85 rótulos quedaron con el
> número en caché en «1». Word, al abrir, actualiza los índices pero no los campos
> del cuerpo, así que las listas se regeneraban copiando ese «1» y salían todas
> como «Ilustración 1 … 1». Ya está corregido.

A partir de ahora, para citar una tabla o una figura en el texto use
**Referencias → Referencia cruzada → Tabla / Ilustración**. Cada rótulo quedó con
su propio marcador, así que aparecen todos en esa lista y la numeración se
mantiene sola si insertan o mueven algo.

---

## 1. Lo que hay que resolver antes de entregar

### 1.1 La carga de viento no está calculada
El anexo lo pide expresamente dos veces: en el numeral 3.1 («deben ser calculadas
y reportadas en la memoria») y en el contenido mínimo del numeral 4.1.1 («avalúo
de cargas muertas, vivas de entrepisos y cubierta, granizo y **viento**»). La
excepción que concede el anexo es solo para *no asignarlas al modelo*, no para
omitir el cálculo. Además advierte que no se admiten reportes de software
comercial como sustituto del procedimiento.

Agregué el numeral **3.4 Carga de viento** con el marco normativo del Capítulo
B.6 y un **recuadro amarillo** con la lista exacta de lo que falta llenar.
No puse números: son suyos y deben salir de su copia de la norma.

### 1.2 Sa aparece con dos valores distintos
- El texto de «Distribución vertical de la fuerza sísmica» dice **Sa = 0.450**.
- La tabla del cortante en la base trabaja con **Sa = 0.506**
  (13 501.24 kN ÷ 26 669.11 kN = 0.5063).

Hay que unificarlo. No lo toqué porque no sé cuál es el correcto, y de ese valor
depende todo el cortante basal.

### 1.3 ¿Oficinas o vivienda?
El anexo describe **«una edificación residencial de cinco niveles»**, con piso
laminado en apartamentos, muros interiores de apartamento, enchape en baños y
cocina, y **la cubierta como zona comunal recreativa**. La memoria la define como
**oficinas**, con carga viva de 2.00 kN/m² y cubierta «con acceso restringido»
de 1.80 kN/m².

Verifiquen contra el listado técnico del Grupo 2. Si es residencial cambian:
- la carga viva de entrepiso (1.80 kN/m² en vivienda, no 2.00);
- y sobre todo **la carga viva de cubierta**: si la cubierta es zona comunal
  recreativa, no aplica el valor de acceso restringido y sube bastante. Eso mueve
  el peso de la cubierta, el cortante basal y las derivas.

### 1.4 Faltan las combinaciones con efectos ortogonales
El numeral A.3.6.3 obliga, en zona de amenaza sísmica intermedia, a considerar
los efectos ortogonales: 100 % del sismo en una dirección más 30 % en la
perpendicular (o la raíz de la suma de cuadrados).

Para **derivas** sí lo resolvieron bien, con la composición vectorial de la
ecuación A.6.3-1. Pero las combinaciones de **diseño por resistencia** que
aparecen (`D+L±Fx`, `D+L±Fy`) no recogen el 30 % transversal. Hay que añadirlas
en el modelo y en el numeral 3.7.

### 1.5 Ω₀ sin valor
El anexo pide, en el análisis sísmico, «coeficientes de sobrerresistencia (Ω)».
Escribí el numeral **3.6.8.6 Coeficiente de sobrerresistencia, Ω₀** con el
numeral A.3.3.9 y la ecuación A.3.3-2, y dejé un recuadro amarillo para que
consignen el valor de la tabla A.3-3. No lo puse yo para no inventar un número
normativo.

### 1.6 Verifiquen las combinaciones de B.2.4 que agregué
Las escribí en el numeral 3.7 a partir del Título B. Revísenlas contra su edición
del reglamento, en especial el coeficiente de carga del viento: cambia según el
conjunto de velocidades que se use (primera edición impresa frente a la
modificación del Decreto 340 de 2012).

---

## 2. Lo que conviene mejorar

### 2.1 Las figuras del SAP están en inglés
El anexo exige que «las figuras y tablas presentadas en la memoria de cálculo
deben tener la información en español». Quedan en inglés, entre otras:
`Shear Force 2-2 Diagram`, `Combination`, `Joint`, `Max`. Lo ideal es cambiar el
idioma en SAP2000 y volver a capturar; si no, reetiquetar las imágenes.

### 2.2 El orden de los capítulos
«Descripción del modelo de análisis» quedó como capítulo 5, después del «Análisis
de estabilidad» (capítulo 4). Pero las derivas y el índice Q salen del modelo, así
que el modelo debería describirse antes. El contenido mínimo del anexo también lo
lista antes del análisis de irregularidades y del cálculo de derivas.

**No lo moví** porque es reubicar un bloque de ~60 elementos (texto y 19 figuras)
y preferí no reordenar el documento sin su visto bueno. Si quieren, lo hago.

### 2.3 Numerales que el anexo pide y no existen como tal
- **«Determinación del sistema estructural de resistencia sísmica»**: el sustento
  quedó en el capítulo 1 (sistema A.3-3, pórtico DMO, límites de altura), pero no
  como numeral propio.
- **«Predimensionamiento de elementos verticales»**: el numeral 1.5 muestra las
  tres tipologías de columna (0.25×0.50, 0.40×0.50 y 0.45×0.60 m) pero no explica
  de dónde salen esas secciones. Falta el criterio: carga axial estimada,
  dimensión mínima y relación de esbeltez.
- **Deflexiones a largo plazo**: el numeral 3.4 del anexo pide verificar los
  estados límite de servicio «incluyendo control de deflexiones a largo plazo».
  No aparece en la memoria. Como el espesor de losa cumple C.9.5 el cálculo no es
  obligatorio, pero conviene decirlo explícitamente.

### 2.4 Pendientes de la entrega, además de la memoria
- Planos en `.pdf` y `.dwg`: planta de primer piso, planta tipo, planta de
  cubierta y planta de localización de ejes y elementos verticales.
- Copia completa del modelo (`.sdb` y `.$2k`).
- Anexos con el avalúo detallado, el predimensionamiento y los datos de entrada y
  salida del modelo. Ojo con la regla del anexo: **cada tabla anexa debe estar
  citada y explicada en el documento**.
- En la contraportada quedaron vacías las celdas de documento de identidad y
  firma, y puse «octubre de 2026» como fecha: ajústenla.

---

## 3. Lo que cambié en el documento

### 3.1 Numeración y referenciación (lo que pedían)
- **85 rótulos** quedan con campo `SEQ` de Word, estilo «Descripción» y marcador
  propio: **50 tablas** y **35 ilustraciones**. Numeración automática, y con el
  número correcto ya grabado en el resultado del campo (Tabla 1 a 50,
  Ilustración 1 a 35) para que no dependa de que alguien actualice los campos.
- **25 rótulos nuevos** para objetos que no tenían ninguno:
  - 8 tablas: espesores mínimos de losa, predimensionamiento de elementos,
    carga muerta de piso tipo, carga muerta de cubierta, cargas vivas de
    entrepiso, carga viva de cubierta, y cargas sobre vigas de rigidez de
    entrepiso y de cubierta.
  - 4 tablas de derivas: faltaban las de las columnas C-2/C-7/C-12/C-17,
    C-3/C-8/C-13/C-18, C-4/C-9/C-14/C-19 y C-5/C-10/C-15 (un solo rótulo cubría
    las cinco tablas).
  - Centroide y centros de masa, fuerzas de piso en sentido Y, momentos torsores
    accidentales, umbrales y evaluación de piso flexible, combinaciones del
    índice Q, datos de entrada y diseño a cortante de la vigueta, y las dos de
    transferencia de carga de la escalera.
  - 3 ilustraciones: los dos alzados de columnas (cortes A-A y B-B) y el diagrama
    de cortante de diseño de la vigueta.
- **60 rótulos existentes** reescritos: todos empiezan con mayúscula, terminan en
  punto y describen el objeto. Antes había «materiales para construcción»,
  «asignación de torsión accidental», «índice Q Com 1», «Irregularidades» (sin
  decir de qué eje), «secciones de elementos frame planta NE+4.00».
- La URL de la resina epóxica salió del rótulo de la Tabla 3 y pasó a una línea
  «Fuente:» debajo de la imagen. Antes la URL completa aparecía dentro de la
  lista de tablas.
- Rótulos de tabla con `keepNext`: ya no se separan de su tabla al final de página.

### 3.2 Estructura
- **Jerarquía corregida.** «Descripción y alcance del proyecto» y
  «Predimensionamiento de los elementos» eran Título 2 sin ningún Título 1 que
  los contuviera, así que la numeración arrancaba en un capítulo fantasma
  («1.1 Descripción y alcance…» sin que existiera un «1»). Ahora son capítulos 1
  y 2, y «Altura de losa» y «Dimensionamiento de vigas…» subieron de Título 3 a
  Título 2. Los 59 encabezados quedan sin saltos de nivel.
- **«Referencias»** era el único Título 1 sin numeración y sin centrar; ya quedó
  igual que los demás.
- La **tabla de contenido ya existía** (dentro de un control de contenido después
  de la portada) pero solo recogía los niveles 1 a 3. La amplié a 1–4 para que
  entren los numerales de cuarto nivel, como «Diseño a flexión» o «Coeficiente de
  sobrerresistencia».
- «Tabla de Ilustraciones» → **«Lista de Ilustraciones»**; «Tabla de Tablas» →
  **«Lista de Tablas»**, que era redundante.
- **Contraportada nueva** entre la portada y la tabla de contenido, con nombre del
  proyecto, localización, sistema estructural, normativa, alcance de la entrega,
  fecha y tabla de responsables con espacio para firmas. El anexo la pide
  explícitamente («Portada y contraportada: debe contener el nombre del proyecto,
  localización, fecha de entrega y responsables del diseño con sus respectivas
  firmas»).

### 3.3 Redacción y sustento normativo
Capítulos nuevos: **1.1 Localización y condiciones del sitio**,
**1.2 Normatividad aplicable**, **3.4 Carga de viento**,
**3.6.8.6 Coeficiente de sobrerresistencia Ω₀**,
**3.7 Combinaciones de carga para el diseño por resistencia** y **7 Conclusiones**.

Lo que se explicó, con el numeral de la norma en cada caso:
- Por qué se puede usar la fuerza horizontal equivalente: A.3.4.2.1, literales
  (b) —grupo de uso I en amenaza intermedia— y (d) —no más de 6 niveles ni 18 m—.
- `Ta = Ct·h^α` con Ct = 0.047 y α = 0.9 de la tabla A.4.2-1, el límite `Cu·Ta`
  de A.4.2-2 y la revisión del 10 % que exige A.4.2.3.
- Las cuatro ramas del espectro de A.2.6 y por qué, al haber microzonificación,
  los parámetros salen del Decreto 523 (A.2.9).
- `Vs = Sa·g·M` (A.4.3-1), `Vx = ΣFi` (A.3.6-1), el reparto `Cvx` (A.4.3-3) y de
  dónde sale `k = 1.035`.
- Torsión accidental: el 5 % de A.3.6.7.1, de dónde sale `e = 1.35 m`, la
  **ecuación del coeficiente Ax** (A.3.6-2) y la torsión de diseño de A.3.6.7.3.
- **Índice de estabilidad de piso.** Este numeral solo tenía dos tablas, sin una
  línea de texto ni la ecuación. Ahora lleva la ecuación A.6.2-2, el significado
  de cada término y los tres criterios de A.6.2.3: Q ≤ 0.10 se desprecia,
  0.10 < Q ≤ 0.30 se amplifica por 1/(1−Q) con la deflexión adicional de A.6.2-3,
  y Q > 0.30 la estructura es potencialmente inestable.
- Irregularidades: el tipo normativo de cada una (1aP, 1bP, 2P, 3P, 1aA, 1bA, 2A,
  3A, 4A, 5aA, 5bA) con su φ y su umbral numérico. En particular:
  - retrocesos en las esquinas: el recorte de 2.50 × 2.50 m es el 9.3 % de los
    27.00 m en X y el 11.4 % de los 22.00 m en Y, ambos por debajo del 15 %;
  - diafragma: los vacíos son ~10 m² sobre 577.4 m², el 1.8 %, muy por debajo
    del 50 %;
  - piso flexible: la justificación decía «se evidencia… porque todos los pisos
    presentan las mismas características», cuando en realidad **sí calcularon**
    las rigideces de piso en la tabla siguiente. Lo reescribí apoyándolo en sus
    propios números y añadí la verificación alterna de A.3.3.5.1 (ninguna deriva
    supera 1.3 veces la del piso de arriba), que confirma φa = 1.0.
  - Se dice además que A.3.3.7 permitía revisar menos irregularidades de las que
    revisaron: la verificación quedó más exigente que el mínimo, y eso suma.
- Redundancia: el párrafo citaba A.3.3.8.2 a medias. Ahora está la condición
  completa (el 35 % del cortante basal, el 33 % de pérdida de resistencia, la
  irregularidad 1bP) y la vía alterna de los dos vanos en la periferia, que es la
  que realmente aplica aquí.
- Deriva: la definición de A.6.1.2, el desplazamiento total de A.6.2-4, el
  procedimiento de A.6.3.1.2 para plantas con retrocesos, el límite del 1 % de la
  tabla A.6.4-1 traducido a **40 mm en el primer nivel y 30 mm en los demás**, y
  el factor 0.7 de A.6.4.1.1 que no se usó (queda del lado conservador).
- **Descripción del modelo**: tenía un solo párrafo y 19 figuras sin texto. Ahora
  cubre lo que pide el anexo: tipo de análisis, casos, elementos empleados,
  tratamiento de la masa y de la rigidez (A.3.4.3), condiciones de apoyo,
  metodología de asignación de cargas y los resultados mínimos de A.4.4.2.
- Predimensionamiento: los factores de C.9.5 (16, 18.5, 21 y 8) y por qué se tomó
  el promedio de los dos escenarios; los requisitos de C.8.13 para nervios,
  loseta y riostras.
- Cargas: el Capítulo B.3 y las tablas B.3.4.1-1, B.3.4.1-3 y B.3.4.3-1 que ya
  citaban en sus tablas; la tabla B.4.2.1-1 para las cargas vivas; la definición
  de la masa M del Capítulo A.4 y por qué no entra carga viva.
- Viguetas y escalera: A.3.6.1.2 (no hacen parte del sistema de resistencia
  sísmica, qué hay que verificar en ellas) y el criterio de viga T para el momento
  positivo frente a sección rectangular para el negativo.
- **Conclusiones** con los resultados del propio documento: h losa 0.50 m,
  W = 26 669 kN, Ta = 0.570 s, k = 1.035, Vs = 13 501 kN, fuerzas de piso de
  1 186 a 3 789 kN, R = 5.0, deriva máxima 23.5 mm = 0.78 % de hp frente al 1 %,
  índice Q muy por debajo de 0.10, y el refuerzo de la vigueta tipo 1.
- El párrafo de apertura decía «se realizó con el fin de afianzar conocimientos y
  conceptos vistos en la clase de estructuras». El anexo pide justo lo contrario:
  «debe presentar el proyecto como si se tratara de una consultoría profesional y
  no como un trabajo de clase». Lo reescribí.

### 3.4 Dos cosas que había que limpiar
- **Ilustración duplicada.** «Numeración de nudos NE+7.00» aparecía dos veces, y
  las dos apuntaban al mismo archivo de imagen (`image45.png`). Como los niveles
  son NE +0.00, +4.00, +7.00, +10.00, +13.00 y +16.00 —seis— y había siete
  figuras, eliminé la repetida. **Confirmen** que no era un nivel distinto cuya
  captura se perdió.
- **Comentario heredado de otro documento.** Había un comentario de
  «Juan David Arroyo López» fechado el 18 de junio de **2023** que decía «No
  especificar ecuación, simplemente ponerla». Lo eliminé. Vale la pena revisar qué
  más viene arrastrado de esa plantilla.

### 3.5 Lo que NO toqué
- Fuentes, tamaños, márgenes, encabezados y pies de página.
- Ninguna tabla, imagen o ecuación existente: las 68 imágenes y las 24 tablas
  siguen intactas y en su sitio.
- Ningún resultado numérico de cálculo. Todos los números que aparecen en el texto
  nuevo están tomados de sus propias tablas.
- La tabla de contenido original, que se conserva (solo se amplió a cuatro
  niveles).

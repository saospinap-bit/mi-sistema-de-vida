# 🏗 Diseño Estructural 2

Carpeta de trabajo para la **segunda parte** del proyecto de diseño estructural (Grupo 2 — edificación de 5 niveles para oficinas, Bogotá D.C., zona Cerros).

La primera parte está en `../Diseno-Estructural/` y la memoria en la raíz del repositorio (`Proyecto_final_grupo_2_entrega1.docx`). Esta carpeta es para lo que falta, no para rehacer lo que ya está.

---

## Qué falta (en orden de impacto)

Esto sale de comparar nuestra memoria con la del grupo que le fue bien (`Memorias de cálculo.docx`, Grupo 1):

- [ ] **Elementos que SÍ hacen parte del sistema de resistencia sísmica** — el capítulo completo no existe todavía:
  - [ ] Combinaciones de carga para diseño (las de B.2.4, escritas una por una)
  - [ ] Carga muerta y viva en las vigas de carga y de rigidez, a partir de las reacciones de las viguetas
  - [ ] Esquemas de carga por viga
  - [ ] Diseño a flexión y cortante de las vigas de carga y de rigidez
  - [ ] Envolventes de cortante y de momento por viga tipo
- [ ] **Columnas**: tipificación, propiedades y diagramas de interacción $P$–$M_2$ y $P$–$M_3$
- [ ] **Cimentación**: zapatas (dimensionamiento, cortante unidireccional y punzonamiento) y vigas de amarre
- [ ] **Periodo real desde el modelo** con la ecuación A.4.2-1 y verificación de $T \le C_u T_a$
- [ ] **Índice Q con secciones fisuradas** ($0.35\,I_g$ en vigas, $0.70\,I_g$ en columnas) y verificación de arriostramiento
- [ ] **Viguetas tipo 2, 3 y 4** (solo está diseñada la tipo 1)
- [ ] **Cerrar el diseño de la escalera**: cortante y momento de diseño, acero principal y de retracción

## Qué subir aquí

- [ ] Enunciado o anexo de la entrega 2 y la rúbrica
- [ ] Resultados de SAP2000 de esta etapa (envolventes por elemento, reacciones, fuerzas en columnas)
- [ ] El modelo `.sdb` o los exports en Excel
- [ ] Planos actualizados

## Insumos que ya tenemos

| Archivo | Dónde | Para qué sirve |
|---|---|---|
| `Proyecto diseño (1) (5).xlsx` | `../Diseno-Estructural/` | Hojas de LOSA, Avalúo, Pesos, Espectro, FHE, Derivas, Irreg. Torsional y Viguetas C.8.3.3 |
| `Diseño de vigas proyecto diseño DEF.xlsx` | `../Diseno-Estructural/` | Vigas de carga y de rigidez |
| `Memorias de cálculo.docx` | raíz del repo | Memoria del Grupo 1, como molde de estructura y profundidad |
| `13-COLUMNAS.pptx`, `16-Zapatas.pptx`, `17- Vigas de amarre.pptx` | `../Diseno-Estructural/` | Material de clase de los temas pendientes |

## Acuerdos de formato

Esto sale de la auditoría de la entrega 1, para no repetir los mismos problemas:

- **Tablas como tablas de Word**, no capturas de Excel. En la entrega 1, 17 de 28 tablas eran capturas: no se leen impresas y no se pueden revisar.
- **Rótulos con campos automáticos** (Insertar → Título), nunca el número escrito a mano, y todos con el estilo Caption del documento.
- **Rótulo de tabla arriba** del objeto, **rótulo de figura debajo**.
- **Ecuaciones desarrolladas con los números reemplazados**, no solo el resultado. Es la diferencia más grande frente a la memoria del Grupo 1: 262 ecuaciones contra 99.
- **Cada capítulo con su Heading 1**, para que la numeración multinivel no se rompa.
- Antes de entregar: **Ctrl+E y F9** para actualizar los tres índices.

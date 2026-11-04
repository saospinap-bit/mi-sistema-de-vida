# Propuesta – Ejercicio de licitación (sábado 7 de noviembre de 2026)

Licitación L02-2009, Municipio de Sandoná: construcción del polideportivo cubierto.
Presupuesto oficial: **$872.826.612**. **Nuestra oferta: $820.489.073 (94,00 %)**.

## Qué imprimir y cómo entregarlo (en físico, antes de las 7:00 a.m.)

| Sobre | Archivo | Contenido |
|---|---|---|
| **Sobre No. 1** | `SOBRE_1_Habilitantes_y_Programa.pdf` | Rótulo, índice, carta de presentación (Anexo 1), formato de experiencia (Anexo 3), programa de obra (Anexo 6) y cronograma (Anexo 7) |
| **Sobre No. 2** | `SOBRE_2_Oferta_Economica_ORIGINAL.pdf` + `..._COPIA.pdf` | Rótulo + oferta económica en el formato (Anexo 4) |
| Si quedamos primeros | `APU_3.06_4.05_7.01_12.02.pdf` | Costo de mano de obra 2026 + los 4 APU pedidos |
| Si quedamos primeros | `HOJAS_DE_VIDA_Director_Residente_Maestro.docx` | Formatos de hoja de vida con los requisitos del numeral 4.3 |
| Solo si van en grupo | `ANEXO_2_Consorcio_o_UT_(si_aplica).docx` | Documento de conformación (no se puede corregir después) |

Antes de imprimir hay que llenar los datos entre corchetes: nombre del proponente, representante, cédula, dirección, teléfono y correo.

## Archivos de trabajo (no se entregan)

- `PROPUESTA_ECONOMICA.xlsx`: oferta, APU, mano de obra, programa y cronograma, todo con fórmulas. En la hoja **AJUSTE**, la celda C4 es el factor que se aplica a los precios del formato. Si se cambia, se recalculan la oferta, el programa y el cronograma. Los PDF **no** se actualizan solos.
- `SIMULADOR_CALIFICACION.xlsx`: se escriben las ofertas y la balota, y calcula las 6 medias y el puntaje de cada proponente.
- `scripts/`: generadores en Python (`datos.py` contiene todos los datos).

## Cómo se armó la oferta

- **Las cantidades y unidades del formato no se tocaron** (se verificaron los 85 ítems uno por uno).
- **Los ítems 3.06, 4.05, 7.01 y 12.02 tienen el precio de su APU**: $561.026, $72.103, $85.260 y $424.904. Así el APU coincide exactamente con la oferta.
- Los demás ítems valen el precio del formato × 0,9427, ajustado al peso.
- **AIU** igual al formato: A 15 %, I 7 %, U 2 %.
- **Se corrigieron dos errores del formato**: el total de 12.01 (13 × precio unitario) y el de 12.02.
- La oferta queda en el **94 %** del presupuesto. Tiene puntos si la media sorteada cae entre $804,4 M (−2 %) y $863,7 M (+5,3 %), es decir, entre el 92,2 % y el 98,9 % del presupuesto oficial.

## Preguntas para el profesor

1. ¿Cómo se calcula el puntaje "proporcional"? El simulador trae dos opciones.
2. ¿Se pueden cambiar los porcentajes del AIU? ¿Hay que incluir IVA sobre la utilidad?
3. El Anexo 6 (programa, Sobre 1) pide la columna "costo actividad", y con eso se puede deducir el costo directo antes de abrir el Sobre 2. ¿Se deja?
4. ¿Qué documentos habilitantes se simulan (póliza, RUP, experiencia, patrimonio)?
5. Zapatas: el formato dice 24 m³ y el pliego 23 m³. Se usaron los 24 m³ del formato.
6. El ítem 7.01 dice "cerámica" en el formato y "porcelanato" en el pliego. El APU es de porcelanato.

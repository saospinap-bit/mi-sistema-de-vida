# Propuesta – Ejercicio de licitación (cierre: 7 de noviembre de 2025)

Licitación L02-2009, Municipio de Sandoná: construcción del polideportivo cubierto.
Presupuesto oficial (formulario Excel): **$872.826.612**. **Nuestra oferta: $820.442.412 (94,00 %)**.

## Datos que salen de la fecha de cierre y del presupuesto

| Concepto | Valor |
|---|---|
| Fecha de cierre | 7 de noviembre de 2025 |
| Garantía de seriedad | 10 % × $872.826.612 = **$87.282.661** |
| Vigencia de la póliza | 7 de noviembre de 2025 al **7 de mayo de 2026** (6 meses) |
| Experiencia mínima | 50 % × $872.826.612 = **$436.413.306** |
| Experiencia en SMMLV 2025 | $436.413.306 ÷ $1.423.500 = **306,58 SMMLV** |
| Periodo de la experiencia | Contratos terminados entre el 7-nov-2015 y el 7-nov-2025 |
| Cámara de Comercio | Expedida entre el 8-oct-2025 y el 7-nov-2025 (máximo 30 días) |
| Duración de la sociedad | Hasta el 7-abr-2027 o después (plazo + 1 año) |
| Duración del consorcio / UT | Hasta el 7-abr-2028 o después (plazo + 2 años) |
| Antecedentes | Vigentes a la fecha de cierre |

## Qué imprimir

| Sobre | Archivo | Contenido |
|---|---|---|
| **Sobre No. 1** | `SOBRE_1_Documentos_Habilitantes.pdf` | Rótulo, índice y las 7 secciones del profesor: carta de presentación, carta de consorcio/UT, garantía, cédulas, Cámara de Comercio, experiencia (Anexo 3) y antecedentes disciplinarios y fiscales. Cada sección trae una hoja separadora con lo que hay que adjuntar |
| **Sobre No. 2** | `SOBRE_2_Oferta_Economica_ORIGINAL.pdf` + `..._COPIA.pdf` | Rótulo + oferta económica (Anexo 4) |
| Si quedamos primeros | `APU_3.06_4.05_7.01_12.02.pdf` | Costo de la mano de obra 2025 + los 4 APU |
| Si quedamos primeros | `HOJAS_DE_VIDA_Director_Residente_Maestro.docx` | Formatos de hoja de vida (numeral 4.3) |
| Solo si lo piden | `PROGRAMA_DE_OBRA_Anexos_6_y_7.pdf` | Programa de obra y cronograma (no está en la lista del Sobre 1 del profesor) |

Antes de imprimir hay que llenar los datos entre corchetes: nombre del proponente, representante, cédula, NIT, dirección, teléfono y correo.

## Archivos de trabajo (no se entregan)

- `PROPUESTA_ECONOMICA.xlsx`: oferta, APU, mano de obra, programa y cronograma con fórmulas. El factor de ajuste está en la hoja AJUSTE, celda C4. Los PDF no se actualizan solos.
- `EXPERIENCIA_CALCULO.xlsx`: se escriben los contratos (valor, % de participación, año de terminación) y dice si cumplen los 306,58 SMMLV.
- `SIMULADOR_CALIFICACION.xlsx`: calcula las 6 medias y el puntaje de cada proponente.
- `ANEXO_2_Consorcio_o_UT_(si_aplica).docx`: versión editable del Anexo 2.
- `scripts/`: generadores en Python (`datos.py` tiene todos los datos).

## Cómo se armó la oferta

- Cantidades y unidades del formato sin cambios (85 ítems verificados).
- Mano de obra con valores de 2025: SMMLV $1.423.500 (Decreto 1572 de 2024), auxilio de transporte $200.000 (Decreto 1573 de 2024) y jornada de 44 horas semanales (Ley 2101 de 2021).
- Ítems con APU: 3.06 $550.868, 4.05 $69.223, 7.01 $80.609 y 12.02 $415.603. Los demás: precio del formato × 0,948, ajustado al peso.
- AIU: A 15 %, I 7 %, U 2 %. Se corrigieron los totales de 12.01 y 12.02 del formato.

## Preguntas para el profesor

1. ¿El programa de obra (Anexos 6 y 7, 200 puntos de calidad) va en el Sobre 1 o ya no se califica?
2. ¿Cómo se calcula el puntaje "proporcional"? El simulador trae dos opciones.
3. ¿Se pueden cambiar los porcentajes del AIU? ¿Hay que incluir IVA sobre la utilidad?
4. Zapatas: el formato dice 24 m³ y el pliego 23 m³. Se usaron los 24 m³ del formato.

# Taller 1 – Simulación de sistemas de distribución (EPANET 2.0 y WaterGEMS)

| Archivo o carpeta | Contenido |
|---|---|
| `Informe_Taller1_EPANET_WaterGEMS.docx` | Informe completo en Word. Al abrirlo, Word pregunta si actualiza los campos: responda **Sí** para que aparezca la tabla de contenido con números de página. |
| `modelos/` | Modelos de EPANET de los escenarios 1, 2, 3 y 3b (J-6 residencial). En `modelos/recomendaciones/` están los casos 1 a 4 de la sección 12. |
| `resultados/` | Reportes completos de EPANET 2.0.12 y 2.2, y `Resultados_Taller1.xlsx` con todas las tablas. |
| `figuras/` | Figuras del informe. |
| `scripts/` | Código que genera los modelos, corre EPANET, verifica los resultados y arma el informe. Necesita el motor EPANET 2.0.12 compilado desde https://github.com/OpenWaterAnalytics/EPANET. |

Los modelos tienen los mismos datos que los `.inp` de la carpeta `Proyectos/`, con P-16 dibujada de J-7 a T-1 (caudal positivo = entra al tanque) y una precisión de cálculo más estricta (0.0001).

## Pendiente

- Simular en WaterGEMS siguiendo el Anexo B del informe.
- Agregar las capturas de WaterGEMS en la sección 10.3 y llenar la columna WaterGEMS de la Tabla 21.
- Escribir los nombres y códigos de los integrantes en la portada.

## Supuesto por confirmar con el profesor

El enunciado no asigna curva de consumo al nudo J-6, así que se modeló con demanda constante. La sección 7.4 muestra que asignarle uso residencial cambia las presiones menos de 0.9 m.

# Auditoría del Taller 1 (EPANET y WaterGEMS)

Revisión de los archivos de esta carpeta, hecha el 18 de noviembre de 2026.

## Resultado de la revisión

| Archivo | Qué se revisó | Resultado |
|---|---|---|
| `EPANET/Escenario1_Estatico_sin_P16.inp` | Datos contra el enunciado, ecuaciones y resultados | Correcto |
| `EPANET/Escenario2_Estatico_con_tanque.inp` | Lo mismo | Correcto |
| `EPANET/Escenario3_Periodo_extendido_24h.inp` | Lo mismo, más curvas de consumo y tiempos | Correcto |
| `EPANET/Escenario3b_Sensibilidad_J6_residencial.inp` | Lo mismo, con J-6 residencial | Correcto |
| `WaterGEMS/Taller1_Esc1.wtg` | Configuración del proyecto | Calculado una vez, sin mensajes guardados. Presión en kPa y caudal sin decimales |
| `WaterGEMS/Taller1_Esc2.wtg` | Lo mismo | Igual que el anterior |
| `WaterGEMS/Taller1_Esc3.wtg` | Lo mismo | Igual que el anterior |
| `WaterGEMS/Taller1_Esc3_b.wtg` | Lo mismo | **Es una copia exacta de `Taller1_Esc1.wtg`** (mismo contenido byte por byte), no el escenario 3b |
| `Informe_Taller1_EPANET_WaterGEMS.docx` | Todo el texto y las tablas | Actualizado (ver abajo) |

**EPANET.** Los cuatro `.inp` tienen los mismos datos del enunciado: elevaciones, demandas, longitudes, diámetros, C = 100, conexiones, sentido y consignas de las PRV, bomba, tanque, reservorio y curvas. Corrí los cuatro con el motor de EPANET 2.0 (versión 2.00.12). Cumplen continuidad, Hazen-Williams, la curva de la bomba y el estado de las PRV en todos los pasos, sin avisos. Comparé los 760 valores que aparecen en las tablas del informe, redondeados como en el informe, y no hay ninguna diferencia.

**WaterGEMS.** El archivo `.wtg` solo guarda la configuración del proyecto (unidades, simbología, escenario activo). Los datos del modelo y los resultados quedan en el archivo `.wtg.sqlite`, que no está en la carpeta, así que no pude revisar los resultados de WaterGEMS. Lo que sí se ve en los `.wtg`:

- Los tres se crearon con WaterGEMS 26.0.0.532 y cada uno registra un cálculo del escenario.
- La presión está en **kPa con 0 decimales** y el caudal en **L/s con 0 decimales**. Así los pantallazos no se pueden comparar con EPANET: hay que cambiarlo antes de tomarlos (paso 1 de la lista de WaterGEMS).
- `Taller1_Esc3_b.wtg` es el mismo archivo del Escenario 1. Si quieren el 3b en WaterGEMS, importen `Escenario3b_Sensibilidad_J6_residencial.inp`; si no, bórrenlo. El informe no lo necesita.

## Cambios en el informe

- Formato sencillo: letra Arial negra, tablas con cuadrícula negra, sin colores ni recuadros.
- Se quitaron todas las figuras hechas por computador. Las dos figuras que quedan (esquema de la red y curvas de consumo) salen del enunciado y lo dicen. Las demás son espacios marcados como **[Pantallazo …]** para pegar las capturas de EPANET y WaterGEMS.
- La sección 4.2 describe lo que hicieron en WaterGEMS: importar los `.inp`, las tuberías cortas que agrega la importación y la compatibilidad con el motor de EPANET 2.00.12.
- La sección 10 quedó para los resultados de WaterGEMS: espacios para los pantallazos y la Tabla 20, con la columna de EPANET llena y la de WaterGEMS vacía.
- Se quitaron la guía paso a paso de WaterGEMS, las comparaciones con otras versiones de EPANET y la sección de verificación con programas. Queda la verificación a mano (sección 11).
- Todos los números se recalcularon con sus propios archivos `.inp`.

## Pantallazos que faltan

No los pude tomar yo: EPANET 2.0 y WaterGEMS son programas de Windows con interfaz gráfica, y en el entorno donde trabajo no hay Windows ni forma de abrir ventanas. Cada pantallazo va en el espacio **[Pantallazo …]** de la figura indicada; peguen la imagen ahí y borren el texto entre corchetes.

### EPANET 2.0 (5 pantallazos)

Antes de empezar, abran el archivo, corran el cálculo (*Project → Run Analysis*) y verifiquen que diga *Run was successful*.

| Figura | Archivo | Cómo sacarlo |
|---|---|---|
| 3 | `Escenario1_Estatico_sin_P16.inp` | En el *Browser*, pestaña *Map*: Nodes = *Pressure*, Links = *Flow*. En *View → Options → Notation* marquen *Display Node Values* y *Display Link Values*. Activen las leyendas (*View → Legends*). Capturen el mapa completo. |
| 4 | `Escenario2_Estatico_con_tanque.inp` | Igual que la Figura 3. |
| 5 | `Escenario3_Periodo_extendido_24h.inp` | *Report → Graph*, tipo *Time Series*, objeto *Nodes*, parámetro *Head*, ítem T-1. |
| 6 | Mismo archivo | *Report → Graph*, *Time Series*, objeto *Links*, parámetro *Flow*, ítem PMP-1. |
| 7 | Mismo archivo | *Report → Graph*, *Time Series*, objeto *Nodes*, parámetro *Pressure*, ítems J-1, J-3 y J-7 en la misma gráfica. |

Valores para revisar que todo esté bien: en el Escenario 1, J-1 debe mostrar 84.67 m y PMP-1 27.20 L/s. En el Escenario 2, J-7 debe mostrar 43.58 m y P-16 31.86 L/s. En el Escenario 3, el tanque debe llegar a 326 m a las 7:46.

### WaterGEMS (7 pantallazos)

Paso 1, antes de cualquier captura y en cada archivo: *Tools → Options → Units*, Pressure = **m H2O** con 2 decimales y Flow = **L/s** con 2 decimales. También se puede hacer en cada FlexTable con clic derecho sobre el encabezado de la columna → *Units and Formatting*. Después corran el cálculo (*Compute*).

| Figura | Archivo | Cómo sacarlo |
|---|---|---|
| 8 | `Taller1_Esc1.wtg` | *Element Symbology*: color de los nudos según *Pressure*, con la leyenda visible. Capturen el dibujo de la red. |
| 9 | `Taller1_Esc1.wtg` | *Analysis → Calculation Options*, seleccionen *Base Calculation Options* y capturen el panel de propiedades donde se vean *Friction Method* y *Engine Compatibility*. |
| 10 | `Taller1_Esc1.wtg` | *View → FlexTables → Junction Table* con Label, Elevation, Demand, Hydraulic Grade y Pressure. |
| 11 | `Taller1_Esc1.wtg` | *Pump Table* (Flow, Pump Head) y *Pressure Reducing Valve Table* (Flow, Status). Pueden ir las dos tablas en la misma captura. |
| 12 | `Taller1_Esc2.wtg` | *Junction Table*, como la Figura 10. |
| 13 | `Taller1_Esc2.wtg` | *Pump Table* y *Pipe Table* (Flow, Velocity). En la de tuberías se deben ver P-11 y P-16. |
| 14 | `Taller1_Esc3.wtg` | Revisen primero que el cálculo sea EPS de 24 h. Luego clic derecho sobre T-1 → *Graph* (Hydraulic Grade) y sobre PMP-1 → *Graph* (Flow). Las dos gráficas en una captura. |

### Cuando tengan los pantallazos

1. Péguenlos en el informe en el orden de la tabla.
2. Llenen las columnas *WaterGEMS* y *Diferencia* de la Tabla 20 con los valores de las Figuras 10 a 14. También me los pueden subir a esta carpeta y la lleno yo.
3. Suban a la carpeta `WaterGEMS/` los archivos `.wtg.sqlite` de cada modelo. Sin ellos, quien abra el `.wtg` no ve la red.
4. Escriban los nombres y códigos en la portada y, al abrir el Word, respondan **Sí** cuando pregunte si actualiza los campos, para que salga la tabla de contenido.

La carpeta se llama *Taller-3*, pero el enunciado dice *Taller 1*. El informe usa el título del enunciado; si el profesor lo numera distinto, cambien la portada.

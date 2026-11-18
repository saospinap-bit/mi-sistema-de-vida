# Auditoría del Taller 1 (EPANET y WaterGEMS)

## EPANET

Los cuatro `.inp` de `EPANET/` tienen los mismos datos del enunciado: elevaciones, demandas, longitudes, diámetros, C = 100, conexiones, sentido y consignas de las PRV, bomba, tanque, reservorio y curvas de consumo. Corridos con el motor de EPANET 2.0 (2.00.12), cumplen continuidad, Hazen-Williams, la curva de la bomba y el estado de las PRV en todos los pasos, sin avisos. Los 760 valores de las tablas del informe coinciden con estos archivos.

## WaterGEMS

Se revisaron los pantallazos de los tres modelos (carpeta `WaterGEMS/capturas/`):

- **Datos:** C = 100, longitudes y diámetros correctos en las 16 tuberías; tanque con base 308 m y niveles 314 / 320 / 326 m; bomba BOMBA-1; J-6 con demanda constante en el Escenario 3.
- **Opciones de cálculo (Escenario 3):** EPS, 24 h, paso de 1 h, *Engine Compatibility* = EPANET 2.00.12.
- **Corrección hecha:** las PRV llegaron con la consigna como presión y WaterGEMS dejaba su salida en 286.52 m. Se cambiaron a *Hydraulic Grade* con 285.0 / 286.5 / 286.5 m y la salida quedó en 286.50 m, igual que en EPANET.
- **Resultados:** caudales, altura de la bomba y alturas piezométricas iguales a EPANET en los tres escenarios; el tanque se llena a las 7.77 h (7:46) en los dos programas. Las presiones en WaterGEMS salen 0.02 a 0.04 m más bajas por la conversión de unidades del programa (la altura piezométrica es la misma). El detalle está en la Tabla 20 del informe.

Pendiente en esta carpeta:

- Subir los modelos corregidos (`Taller1_Esc1cor.wtg`, `Taller1_Esc2cor.wtg`, `Taller1_Esc3cor.wtg`) con sus `.wtg.sqlite`. Los `.wtg` que están ahora son los de antes de corregir las PRV, y sin el `.sqlite` no se pueden abrir.
- `Taller1_Esc3_b.wtg` es una copia exacta de `Taller1_Esc1.wtg`; se puede borrar.

## Pantallazos de EPANET

Los cinco pantallazos de EPANET (carpeta `EPANET/capturas/`) se revisaron contra los resultados: caudales y presiones de los mapas de los Escenarios 1 y 2, y las gráficas del tanque, la bomba y las presiones del Escenario 3 coinciden con las tablas del informe. Se tomaron en EPANET 2.2, que da los mismos resultados que la versión 2.0; el informe lo aclara en la sección 4.1.

## Estado del informe

Todas las figuras están puestas. Solo falta escribir los nombres y códigos de los integrantes en la portada.

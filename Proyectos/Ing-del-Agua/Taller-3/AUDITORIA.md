# Auditoría del Taller 1 (EPANET y WaterGEMS)

## EPANET

Los cuatro `.inp` de `EPANET/` tienen los mismos datos del enunciado: elevaciones, demandas, longitudes, diámetros, C = 100, conexiones, sentido y consignas de las PRV, bomba, tanque, reservorio y curvas de consumo. Corridos con el motor de EPANET 2.0 (2.00.12), cumplen continuidad, Hazen-Williams, la curva de la bomba y el estado de las PRV en todos los pasos, sin avisos. Los 760 valores de las tablas del informe coinciden con estos archivos.

Los casos de las recomendaciones están en `EPANET/recomendaciones/` (Caso 1 a Caso 4).

## WaterGEMS

Se revisaron los pantallazos de los tres modelos (carpeta `WaterGEMS/capturas/`):

- **Datos:** C = 100, longitudes y diámetros correctos en las 16 tuberías; tanque con base 308 m y niveles 314 / 320 / 326 m; bomba BOMBA-1 (importada como curva de varios puntos); J-6 con patrón CONSTANTE en el Escenario 3.
- **Opciones de cálculo (Escenario 3):** EPS, 24 h, paso de 1 h, *Engine Compatibility* = EPANET 2.00.12, gravedad específica 1.0.
- **Corrección hecha:** las PRV se cambiaron a *Hydraulic Grade* con 285.0 / 286.5 / 286.5 m y la salida quedó igual que en EPANET.
- **Resultados:** caudales, altura de la bomba y alturas piezométricas iguales a EPANET; el tanque se llena a las 7:46 en los dos programas. Las presiones de WaterGEMS salen 0.02 a 0.04 m más bajas con la misma altura piezométrica (Tabla 20 del informe).

## Correcciones de la revisión

| Punto | Estado |
|---|---|
| A1. Caso 4: reglas exactas, tiempos, presiones, energía, archivos | Hecho. Reglas `CLOSED IF T-1 ABOVE 18` / `OPEN IF T-1 BELOW 12`; apaga 7:46, prende 17:44; 405.0 vs 475.9 kWh/día (−14.9 %). Archivos en `EPANET/recomendaciones/`. |
| A2. Patrones del .inp iguales al .bak | Hecho. E3: J-6 CONSTANTE, J-7 sin patrón. E3b: J-6 RESIDENCIAL. Resultados sin cambio. |
| A3. Patrones escalonados en WaterGEMS | Pendiente: pantallazo de la ventana Patterns. |
| A4. Material Cast Iron | Texto quitado del informe. Pendiente cambiarlo en WaterGEMS. |
| B1. Anexo B igual a lo entregado | Hecho en el informe. Pendiente subir `Taller1_Esc1/2/3.wtg` con su `.wtg.sqlite` (sin "cor"). |
| B2. Autores en .inp y .docx | Pendiente: nombres. |
| C1. Portada (apellidos, códigos, fecha) | Pendiente: datos del grupo. |
| C2. Índice | Actualizar en Word al final (clic derecho → Actualizar campos). |
| C3. Tabla 7 | Hecho: datos numéricos del gráfico del enunciado. |
| C4. Causa de la diferencia de presión | Hecho: redacción suavizada; SG = 1.0 en el escenario activo. |
| C5. Encabezado Tabla 19 | Hecho. |
| D. Figuras 5–7 y 14–16 | Pendiente: pantallazos originales más grandes. |
| E. Normativa y valores | Hecho: arts. 61, 62 y 63 verificados con la Res. 799 de 2021. PRV y reservorio leídos del enunciado. |

## Archivos quitados

- Copias de los `.inp` y los `.net` en la raíz de `Taller-3` (duplicados; `Escenario3.net` quedó desactualizado con el cambio de patrones).
- `WaterGEMS/Taller1_Esc3_b.wtg` (copia de Esc1) y los `.wtg.sqlite.01.bak`.

Los `.wtg` de `WaterGEMS/` son los de antes de corregir las PRV; se reemplazan cuando se suban los nuevos.

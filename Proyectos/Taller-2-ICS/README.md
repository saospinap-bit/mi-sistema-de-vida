# Taller 2 ICS 2026-2S: Vensim, difusión de un producto y epidemias

Entrega: domingo 29 de noviembre de 2026, 11:59 pm, por Moodle (PDF + modelos MDL).

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `Informe_Taller2_ICS.pdf` | Informe completo, puntos 1 a 6 |
| `Informe_Taller2_ICS.docx` | El mismo informe en Word, para poner los nombres y las capturas |
| `modelos/Cap09_difusion1_clientes.mdl` | Punto 2: difusión por boca a boca (cust1). Corrida `clientes1` |
| `modelos/Cap09_difusion2_capacidad.mdl` | Punto 2: vistas Clientes, Capacidad e Ingresos por Ventas (cust2). Corrida `clientes2` |
| `modelos/Cap09-10_difusion3_capacidad_detallada.mdl` | Puntos 2 y 3: capacidad detallada (cust3). Corridas `clientes3` y `clientes4` (tiempo para ajustar la capacidad = 4). Trae los gráficos personalizados del capítulo 10 |
| `modelos/Cap12_boca_a_boca_1_estructura.mdl` | Punto 4: modelo de ventas por boca a boca (wom1) |
| `modelos/Cap12_boca_a_boca_2_controles.mdl` | Punto 4: vistas Inicio, Estructura, Simular y Juego, deslizadores, gráfico, GAME INTERVAL |
| `modelos/JMG_2.1_desarrollo_epidemia.mdl` | Punto 6: caso 2.1 del libro de Juan Martín García |
| `figuras/` | Diagramas y gráficas que usa el informe |
| `scripts/` | Código que genera los .mdl, las simulaciones y el informe (Python + PySD) |

## Antes de entregar (hacerlo en Vensim PLE)

1. Abrir cada `.mdl`, correr **Model > Check Model** y **Units Check**. Las ecuaciones se verificaron al simularlas con PySD, pero el boceto no se probó en Vensim.
2. Simular con estos nombres de corrida: `clientes1`, `clientes2`, `clientes3` y `clientes4` (en el modelo difusion3 con *tiempo para ajustar la capacidad* = 4). Los gráficos personalizados de difusion3 usan esos nombres.
3. Reemplazar o complementar las figuras de diagramas del informe con **capturas de Vensim**. Las del informe las dibujó el script y no son pantallazos de Vensim.
4. En `Cap12_boca_a_boca_2_controles.mdl`, revisar que los deslizadores y el gráfico de salida aparezcan. Si no aparecen, crearlos con la herramienta Input Output (los rangos están en el informe, sección 4). Los **enlaces de navegación** de la vista Inicio se crean con la herramienta Comment, botón *Navigate…*.
5. Escribir los nombres del grupo en la portada del `.docx` y exportarlo a PDF.

## Resultados de control

Los valores del caso 2.1 coinciden con el libro (págs. 27 a 30): Infectados llega a un máximo de 196 en el mes 3, Susceptibles baja a un mínimo de 213 en el mes 7 y los avisos del rango [50,150] salen en los meses 2 (Above), 6 (In) y 9 (Below).

## Fuentes

- Guía de Vensim, capítulos 9, 10 y 12: https://vensim.com/documentation/users_guide.html (el punto 4 del enunciado dice "capítulo 10", pero los controles de entrada y salida están en el capítulo 12, `usr12.html`).
- Juan Martín García, *Ejercicios avanzados en Dinámica de Sistemas*, apartado 2.1, págs. 22 a 29.

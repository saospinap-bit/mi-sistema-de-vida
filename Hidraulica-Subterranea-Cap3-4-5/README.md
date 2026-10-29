# Hidráulica Subterránea — Ejercicios de los capítulos 3, 4 y 5

Solucionario y guía de los ejercicios de las secciones *Problems* de los capítulos 3, 4 y 5 de
Domenico, P. A. & Schwartz, F. W. (1997), *Physical and Chemical Hydrogeology*, 2.ª edición,
John Wiley & Sons (páginas 55–57, 73–74 y 102).

## Documentos

| Archivo | Contenido |
|---|---|
| [`Solucionario_Ejercicios_Cap3-4-5.docx`](Solucionario_Ejercicios_Cap3-4-5.docx) | Las 33 soluciones: 17 del capítulo 3, 10 del capítulo 4 y 6 del capítulo 5. 802 ecuaciones, 25 figuras, 17 tablas. |
| [`Guia_Explicada_Paso_a_Paso_Cap3-4-5.docx`](Guia_Explicada_Paso_a_Paso_Cap3-4-5.docx) | El método de cada ejercicio: qué reconocer en el enunciado, qué fórmula aplica y por qué, en qué orden, cómo verificar y dónde está la trampa. 873 ecuaciones, 24 figuras, 15 tablas. |

Las ecuaciones son objetos nativos de Word (OMML), no imágenes: se pueden editar y copiar.
Formato A4, márgenes de 2.5 cm, tabla de contenido navegable y numeración de páginas.

## Carpetas

- `figuras/` — las 26 figuras en PNG a 200 dpi, por separado.
- `fuentes/` — el Markdown fuente de ambos documentos.
- `fuentes/scripts/` — los scripts de Python que generan las figuras y los `.docx`:
  - `flownet.py` — resolvedor de la ecuación de Laplace por diferencias finitas (SOR
    rojo-negro) e integración de líneas de corriente por RK4 con tubos de caudal igual.
  - `fig_cap3.py`, `fig_cap4.py`, `fig_cap5.py` — generación de las figuras.
  - `make_ref.py` — plantilla de estilos de Word.
  - `build_docx.py` — ensamblado final con pandoc.

## Nota sobre las redes de flujo

Las redes de flujo de los problemas 4.6 a 4.10 y 5.2 no son esquemas a mano alzada. Se
obtuvieron resolviendo numéricamente

$$\nabla^2 h = 0$$

por diferencias finitas, y las líneas de corriente se integraron repartiendo los puntos de
arranque de modo que cada tubo de flujo transporte el mismo caudal. Por eso las
equipotenciales y las líneas de flujo se cortan a 90° de verdad.

Eso permitió además verificar el problema 4.7 numéricamente: los factores de forma
calculados ($0.364$, $0.505$ y $0.873$) coinciden con los conteos $5/14$, $5/10$ y $6/7$
con menos del 2 % de error.

## Advertencias

Cuatro puntos no se pueden cerrar sin datos que no están disponibles aquí. En todos la
fórmula y el criterio están completos; sólo falta sustituir la lectura propia:

1. **Capítulo 3, problema 13** — hay que escalar con regla la figura 3.E4 del libro
   ($K_i \propto L_i/A_i$).
2. **Capítulo 4, problema 5** — hay que contar los tubos de flujo que convergen en el centro
   de bombeo B en la figura 4.10 ($T = Q/(n_f \Delta h)$). Se incluye una gráfica de
   sensibilidad al conteo.
3. **Capítulo 5, problema 4** — remite al caso histórico de las páginas 99–101 del libro, no
   disponible. Se usa el conjunto de datos equivalente del capítulo 4, problema 4.
4. **Capítulo 5, problema 6** — el exponente del enunciado parece estar mal transcrito. Con
   $q' = 2\times10^{-1}$ ft³/s·ft el pie de la cuña sale negativo y el gradiente implícito
   sería 0.61 m/m, físicamente imposible. Se resuelven los dos casos.

Además, el problema 5.3 requiere linealizar un acuífero libre; se usa el espesor saturado
medio $\bar b = 15$ m y se incluye el análisis de sensibilidad.

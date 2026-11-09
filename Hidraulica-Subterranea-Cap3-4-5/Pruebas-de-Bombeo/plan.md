---
title: "Plan de estudio para el parcial de Hidráulica Subterránea"
subtitle: "Qué estudiar, en qué orden, con qué material y cuánto tiempo"
author: "Repaso guiado"
lang: es
toc: true
toc-title: "Contenido"
toc-depth: 2
---

# Cómo se ve el parcial

Tienes dos señales del profesor y hay que leerlas juntas:

1. Te dio una **lista de ejercicios de los capítulos 3, 4 y 5** de Domenico &
   Schwartz y dijo que con eso estarías listo.
2. Dijo que **probablemente salga una prueba de bombeo**: calcular la
   transmisividad y después hacer cálculos en el acuífero.

Eso define la estructura más probable del examen:

| Parte | Qué | Peso probable | De dónde sale |
|---|---|---|---|
| **A** | Un problema largo de **prueba de bombeo**: hallar $T$ y $S$ y luego calcular abatimientos, interferencia o caudales | 35–45 % | anunciado por el profesor (capítulo 6) |
| **B** | Problemas cortos de **Darcy**: $q$, $v$, unidades, cargas, gradientes | 20–25 % | ejercicios 3.1 a 3.12 |
| **C** | **Conceptual o de dibujo**: redes de flujo, condiciones de frontera, recarga/descarga | 15–20 % | ejercicios 4.6 a 4.10, 5.1, 5.2 |
| **D** | **Ecuación de flujo y almacenamiento**, o esfuerzo efectivo | 10–15 % | ejercicios 4.1 a 4.4 |
| **E** | Extras: intrusión salina, flujo regional | 5–10 % | ejercicios 5.5, 5.6 |

La consecuencia práctica: **la prueba de bombeo vale más que cualquier otro tema
individual, pero Darcy aparece dentro de todos los demás.** Por eso el plan
empieza por Darcy (es la base y es rápido) y después se va de lleno a bombeo.

# El plan, bloque por bloque

Cada bloque tiene: el tema, por qué importa, qué leer, qué ejercicios hacer y un
vídeo. Los vídeos son del curso libre de **F. Javier Sánchez San Román**
(Universidad de Salamanca), que está en español y cubre justo estos temas.

## Bloque 1 — Darcy, cargas y unidades

**Tiempo: 45 min.  Prioridad: MÁXIMA (es la base de todo lo demás).**

**El tema.** El agua subterránea se mueve de mayor a menor **carga hidráulica**
$h = z + P/\rho g$, no de mayor a menor presión. La ley de Darcy
$\mathbf{q} = -K\nabla h$ da el caudal por unidad de área, y la velocidad real
del agua es $v = q/n_e$, bastante mayor.

**Por qué importa.** No es un tema del examen: es el lenguaje del examen. Si
confundes $q$ con $v$ o te equivocas en las unidades de $K$, fallas también los
problemas de bombeo.

**Qué leer.** Guía explicada, Parte 0 (las 5 ideas) y secciones 3.1 a 3.8.

**Ejercicios.** 3.1, 3.2 (q y v) · 3.7 (la tabla de piezómetros, muy probable) ·
3.8 (conversiones de unidades) · 3.6 (problema de los tres puntos).

**Vídeos.**

- [Hidrogeología: conceptos fundamentales (48 min)](https://drive.google.com/file/d/1_ZzDJni79RehLY5Ow3k0-pfre8caxGw5/view)
- [Ley de Darcy, 1ª parte (41 min)](https://drive.google.com/file/d/1QOwI2T3hiTrX-fJVXHAFiUF7hjJ1KRCG/view)
- [Ley de Darcy, 2ª parte (27 min)](https://drive.google.com/file/d/1Od5wnaRtPqG9oveE5VFvgKvwQ0Vjzf_q/view)

**Apuntes:** [Ley de Darcy (PDF)](https://hidrologia.usal.es/temas/Ley_Darcy.pdf)

> Si vas muy justo de tiempo, ve solo la 1ª parte de Darcy y lee la Parte 0 de la
> guía. Es lo mínimo imprescindible.

## Bloque 2 — Prueba de bombeo: Cooper-Jacob

**Tiempo: 1 h 30 min.  Prioridad: MÁXIMA (es lo anunciado).**

**El tema.** Se bombea un pozo a caudal constante y se mide cómo baja el nivel en
un piezómetro. Graficando el abatimiento contra el **logaritmo** del tiempo sale
una recta, y de la recta se leen los dos parámetros del acuífero:

$$T = \frac{2.303\,Q}{4\pi\,\Delta s}
\qquad\qquad
S = \frac{2.25\,T\,t_0}{r^{2}}$$

**Por qué importa.** Es el método que el profesor va a pedir con más
probabilidad: es el estándar de la práctica profesional y el único que se puede
resolver a mano en un examen sin papel de curva patrón.

**Qué leer.** Guía de pruebas de bombeo, Parte 4 completa. **Rehaz el ejemplo a
mano**, dibujando el eje logarítmico tú mismo. Esto no se aprende leyendo.

**Ejercicios.** El ejemplo de la Parte 4 (tabla de 20 puntos). Luego repítelo
cambiando $Q$ a 2000 m³/día: $T$ debe crecer proporcionalmente y $S$ no debe
cambiar. Si eso no te sale, hay un error de concepto.

**Vídeos.**

- [Hidráulica de captaciones (36 min)](https://drive.google.com/file/d/1JHiybYBLyWJ3M2jCJupAt9OskjYNaeh7/view) — la teoría del pozo
- [Bombeo de ensayo, método de Jacob (16 min)](https://drive.google.com/file/d/1uD6Yqw8T6XfGAQqDEOaBf6XjTKoDjRwD/view) — **el más importante de todos**
- [Bombeo de ensayo, método de Theis (12 min)](https://drive.google.com/file/d/1JMmd73ipMCFG48-LF8I7ICLD-nRk20bi/view)

**Apuntes y ejemplos resueltos:**

- [Hidráulica de captaciones (PDF)](https://hidrologia.usal.es/temas/Hidraulica_captaciones.pdf)
- [Ejemplo resuelto, método de Jacob (PDF)](https://hidrologia.usal.es/practicas/confinado/Jacob_EXPLICACION.pdf)
- [Ejemplo resuelto, método de Theis (PDF)](https://hidrologia.usal.es/practicas/confinado/Theis_EXPLICACION.pdf)

> Haz los dos ejemplos resueltos de Salamanca **además** del mío. Son el mismo
> método con otra notación, y ver la misma cosa dos veces es lo que la fija.

## Bloque 3 — Cálculos en el acuífero

**Tiempo: 1 h.  Prioridad: MÁXIMA (es la segunda mitad del problema anunciado).**

**El tema.** Ya tienes $T$ y $S$. Ahora el problema pregunta cosas como: ¿cuánto
baja el nivel a 200 m en 30 días? ¿cuánto si hay tres pozos? ¿hasta dónde llega
el efecto? ¿cuál es el caudal máximo?

**Por qué importa.** El profesor lo dijo explícitamente: «calcular la
transmisividad **y luego hacer cálculos en el acuífero**». Esta es la parte que
la mayoría no estudia porque se queda en hallar $T$.

**Qué leer.** Guía de pruebas de bombeo, Parte 8, incisos (a) a (d) como mínimo.

**Ejercicios.** Los incisos (a), (b), (c) y (d) de la Parte 8. Practica el (a)
cambiando $r$ y $t$ hasta que te salga sin mirar.

**Lo que hay que tener automatizado:**

$$s = \frac{Q}{4\pi T}W(u),\quad u = \frac{r^{2}S}{4Tt}
\qquad
s_{total} = \sum_i s_i
\qquad
R_0 = \sqrt{\frac{2.25\,T\,t}{S}}$$

**Vídeo.**

- [Principio de superposición y teoría de las imágenes (26 min)](https://drive.google.com/file/d/1ToGQtD3NfHq7wmsGDKG5JFdULSkhyMmE/view)

**Apuntes:** [Superposición (PDF)](https://hidrologia.usal.es/temas/superposicion.pdf)

## Bloque 4 — Heterogeneidad, anisotropía y almacenamiento

**Tiempo: 45 min.  Prioridad: ALTA.**

**El tema.** Dos cosas que van juntas. Primera: varias capas se comportan como un
medio equivalente anisótropo, con $K_h$ = media aritmética (flujo paralelo a las
capas) y $K_v$ = media armónica (flujo perpendicular). Segunda: el almacenamiento
$S = \rho g b(\beta_p + n\beta_w)$ dice cuánta agua suelta el acuífero al bajar
la carga.

**Por qué importa.** El 3.11 es un ejercicio de calculadora que casi siempre cae,
y el concepto de $S$ es lo que conecta la prueba de bombeo con la física del
acuífero.

**Qué leer.** Guía explicada, secciones 3.11, 3.12, 4.1 y 4.2.

**Ejercicios.** 3.11 (muy probable) · 4.2 (almacenamiento) · 3.12 (tensor, si te
sobra tiempo) · 4.1 (simplificaciones de la ecuación de flujo: respuesta corta de
teoría).

**Vídeo.**

- [Hidráulica subterránea: principios básicos (42 min)](https://drive.google.com/file/d/1YbODhWk2on1QdNjXBbG_dTbocxWQtFcH/view)

**Apuntes:** [Hidráulica subterránea, principios básicos (PDF)](https://hidrologia.usal.es/temas/Hidraulica_Subt.pdf)

> Mnemotecnia para no equivocarte nunca: **$K_h$ la domina la capa más permeable,
> $K_v$ la domina la menos permeable.** El flujo horizontal se escapa por la
> autopista, el vertical queda atrapado en el cuello de botella.

## Bloque 5 — Redes de flujo y condiciones de frontera

**Tiempo: 45 min.  Prioridad: MEDIA-ALTA (es lo que más se dibuja).**

**El tema.** En régimen permanente $\nabla^2h = 0$, y la solución se dibuja: las
equipotenciales y las líneas de flujo se cortan a 90° formando celdas cuadradas.
El caudal sale de la pura geometría: $Q = K H\,n_f/n_d$.

**Por qué importa.** Es el tipo de pregunta donde se gana nota fácil si sabes
clasificar fronteras, y se pierde todo si no. Son solo dos reglas.

**Qué leer.** Guía explicada, secciones 4.6, 4.7 y 4.9.

**Ejercicios.** 4.6 (clasificar las fronteras AB, BC, CD, DE, FG: respuesta de
memoria) · 4.7 (calcular $Q$ con $n_f/n_d$) · 4.9 (nivel freático inclinado:
$h = z$) · 5.1 (condiciones de borde de las figuras 5.5 y 5.8).

**Las dos reglas, que es todo lo que hay que saber:**

| Frontera | Es una… | Las líneas de flujo… |
|---|---|---|
| Carga constante ($h$ = cte) | equipotencial | la cruzan a 90° |
| Impermeable ($\partial h/\partial n = 0$) | línea de flujo | son paralelas a ella |
| Nivel freático ($h = z$) | ninguna de las dos | la cruzan (recarga o descarga) |

**Material:** [Redes de flujo (presentación)](https://hidrologia.usal.es/temas/Redes_flujo.pps)

## Bloque 6 — Esfuerzo efectivo y excavaciones

**Tiempo: 25 min.  Prioridad: MEDIA.**

**El tema.** Principio de Terzaghi, $\sigma' = \sigma_T - u$. Si la presión de
poro iguala al esfuerzo total, el suelo pierde toda su resistencia y el fondo de
una excavación revienta.

**Por qué importa.** Es el único tema del curso que conecta con geotecnia, y por
eso es un favorito para preguntar. Además se resuelve con sumas y restas.

**Qué leer.** Guía explicada, sección 4.4 completa.

**Ejercicios.** 4.4, los cuatro incisos. La clave conceptual: **excavar reduce
$\sigma_T$ pero no cambia $u$**, porque $u$ la fija el acuífero artesiano.

**Material:** no hay vídeo específico; con la sección 4.4 de la guía basta.

## Bloque 7 — Flujo regional e intrusión salina

**Tiempo: 25 min.  Prioridad: BAJA (leer en diagonal).**

**El tema.** Cómo se organizan los sistemas de flujo en una cuenca (celdas
locales anidadas dentro de un sistema regional, patrón de Tóth) y qué pasa en la
costa, donde el agua dulce flota sobre la salada en relación 1:40
(Ghyben-Herzberg).

**Por qué importa.** Probablemente sea una pregunta conceptual corta, no un
problema. No inviertas más de 25 minutos.

**Qué leer.** Solucionario, secciones 5.1, 5.2, 5.5 y 5.6 (solo los resultados y
la interpretación).

**Ejercicios.** 5.5 (upconing, $Q_{max} = 0.6\pi K d^2 G$) y 5.6 (cuña salina).
Si te preguntan algo de costa, casi seguro es uno de estos dos.

**Apuntes:** [Agua subterránea en regiones costeras (PDF)](https://hidrologia.usal.es/temas/Regiones_costeras.pdf)

# Horario concreto

## Si tienes una noche completa (6 horas)

| Tiempo | Bloque | Qué haces |
|---|---|---|
| 0:00 – 0:45 | 1 | Darcy: vídeo 1ª parte + ejercicios 3.1, 3.2, 3.7, 3.8 |
| 0:45 – 2:15 | 2 | Cooper-Jacob: vídeo de Jacob + rehacer el ejemplo a mano + el ejemplo de Salamanca |
| 2:15 – 2:30 | — | **Descanso** |
| 2:30 – 3:30 | 3 | Cálculos en el acuífero: Parte 8 incisos (a) a (d) |
| 3:30 – 4:15 | 4 | $K_h/K_v$ y almacenamiento: ejercicios 3.11 y 4.2 |
| 4:15 – 5:00 | 5 | Redes de flujo: ejercicios 4.6 y 4.7, memorizar las dos reglas |
| 5:00 – 5:25 | 6 | Esfuerzo efectivo: ejercicio 4.4 |
| 5:25 – 5:45 | 7 | Costa y flujo regional, en diagonal |
| 5:45 – 6:00 | — | Releer la chuleta y la tabla de trampas. **Dormir.** |

## Si solo tienes 3 horas

Olvida los bloques 5, 6 y 7. Haz esto:

| Tiempo | Qué |
|---|---|
| 0:00 – 0:30 | Parte 0 de la guía explicada (las 5 ideas) + ejercicios 3.1, 3.2, 3.7 |
| 0:30 – 1:45 | Cooper-Jacob completo, rehaciendo el ejemplo a mano |
| 1:45 – 2:30 | Cálculos en el acuífero, incisos (a) a (d) |
| 2:30 – 2:50 | Ejercicio 3.11 ($K_h$, $K_v$) y las dos reglas de fronteras |
| 2:50 – 3:00 | Chuleta de la primera página |

## Si solo tienes 1 hora

Lee la **primera página** de la guía de pruebas de bombeo (la chuleta), rehaz el
ejemplo de Cooper-Jacob, y memoriza estas cuatro cosas:

$$q = -K\frac{dh}{dL}
\qquad
v = \frac{q}{n_e}
\qquad
T = \frac{2.303\,Q}{4\pi\,\Delta s}
\qquad
S = \frac{2.25\,T\,t_0}{r^{2}}$$

# Mañana, en el parcial

**Los primeros 2 minutos, antes de escribir nada:**

1. Lee **todo** el examen y marca el problema de bombeo. Empieza por ese: es el
   que más vale y el que mejor sabes.
2. En el problema de bombeo, mira qué variable acompaña al abatimiento:
   ¿tiempo? → Cooper-Jacob. ¿distancia? → distancia–abatimiento ($2\pi$).
   ¿nada, ya estabilizado? → Thiem.
3. Convierte **todos** los tiempos a días antes de calcular.
4. Escribe las fórmulas antes de meter números.

**Al terminar cada problema, 20 segundos de verificación:**

- ¿Las unidades cuadran?
- ¿$u < 0.01$ si usé Cooper-Jacob?
- ¿$S$ está entre $10^{-5}$ y $10^{-3}$ si el acuífero es confinado?
- ¿$K$ corresponde a un material real? Dilo: «arena limpia», «limo».

**Si te bloqueas:** dibuja. El esquema del pozo con su cono te recuerda la
geometría, y la recta en papel semilog te recuerda las dos fórmulas. Casi todo
este curso se puede reconstruir desde un dibujo.

# Fuentes del material externo

Los vídeos, presentaciones y ejercicios resueltos enlazados en este plan
provienen del sitio de docencia libre de **F. Javier Sánchez San Román**,
profesor jubilado del Departamento de Geología de la **Universidad de Salamanca**
(España): <https://hidrologia.usal.es>. El autor permite expresamente la copia y
difusión sin ánimo de lucro citando la procedencia.

Otros dos recursos gratuitos en español que valen la pena si después del parcial
quieres profundizar:

- **Freeze & Cherry (1979), *Groundwater*,** el texto clásico, traducido
  íntegramente al español y de acceso libre:
  <https://fc79.gw-project.org/espanol/>. El capítulo 2 cubre Darcy, el 5 las
  redes de flujo y el 8 las pruebas de bombeo.
- **Woessner, Stringer & Poeter (2023), *Una introducción a las pruebas
  hidráulicas en hidrogeología*,** libro libre de The Groundwater Project:
  <https://gw-project.org/es/books/una-introduccion-a-las-pruebas-hidraulicas-en-hidrogeologia-metodos-basicos-de-bombeo-y-packer/>

*El contenido externo fue parafraseado y resumido para cumplir con las
restricciones de licencia.*

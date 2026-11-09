---
title: "Guía maestra de Hidráulica Subterránea"
subtitle: "Todo el parcial en un solo documento: teoría, ejemplos resueltos, ejercicios para practicar y tus apuntes de clase resueltos (Parte 11)"
author: "Preparación intensiva · un día"
lang: es
toc: true
toc-title: "Contenido"
toc-depth: 2
---

# PARTE 0 — Orientación

## Cómo usar esta guía

Esta guía reemplaza a todas las anteriores. Está ordenada **en el orden en que
conviene estudiar**, no en el orden del libro. Cada parte tiene la misma
estructura:

1. **La teoría**, explicada desde cero y sin pasos saltados.
2. **Ejemplos resueltos** con todo el detalle, como si nunca hubieras visto el
   tema.
3. **Ejercicios para desarrollar**, con las respuestas en el anexo final para
   que te autocalifiques.

Lee en orden. Si te quedas sin tiempo, el anexo D trae un plan de emergencia.

**Lo único que necesitas tener al lado:** calculadora, regla, lápiz y hojas. El
papel semilogarítmico lo vas a aprender a dibujar a mano en la Parte 1.

## Cómo se ve el parcial

Dos señales del profesor, leídas juntas:

- Te dio una lista de ejercicios de los **capítulos 3, 4 y 5** de Domenico &
  Schwartz, diciendo que con eso estarías listo.
- Anunció que **probablemente salga una prueba de bombeo**: calcular la
  transmisividad y después hacer cálculos en el acuífero.

| Parte | Tema | Peso probable | Parte de esta guía |
|---|---|---|---|
| A | Prueba de bombeo: hallar $T$ y $S$ | 25–30 % | 1 y 7 |
| B | Cálculos en el acuífero con $T$ y $S$ | 10–15 % | 8 |
| C | Darcy: $q$, $v$, cargas, unidades | 20–25 % | 2 |
| D | Redes de flujo y fronteras | 15–20 % | 5 |
| E | Ecuación de flujo, almacenamiento, esfuerzo efectivo | 10–15 % | 4 y 6 |
| F | Costa, flujo regional | 5–10 % | 9 |

> **Actualización tras revisar tus apuntes de clase.** En clase se trabajaron,
> con datos concretos, **Dupuit con recarga** y un **acuífero costero con cambio
> climático**. Los dos están resueltos en la **Parte 11** y deben considerarse tan
> probables como la prueba de bombeo. La Parte 11 también resuelve los problemas
> de las figuras 3.31 y 7.39 que fotografiaste, y corrige cuatro erratas de los
> apuntes.

**La conclusión operativa:** la prueba de bombeo es el bloque más grande, pero
Darcy aparece dentro de todos los demás. Y para resolver la prueba de bombeo hay
que saber leer papel semilogarítmico, que es la Parte 1.

## Las seis ideas que explican todo el curso

Si entiendes estas seis, el resto son fórmulas que se deducen.

### Idea 1 — El agua se mueve por diferencias de carga, no de presión

$$h = z + \frac{P}{\rho_w g}$$

La **carga hidráulica** $h$ es energía mecánica por unidad de peso del agua, y por
eso se mide en metros. El agua va siempre de mayor a menor $h$, aunque eso
signifique subir (zonas de descarga) o ir contra la gravedad.

| Término | Nombre | Cómo se mide |
|---|---|---|
| $h$ | carga total | cota del nivel de agua en el piezómetro |
| $z$ | carga de elevación | cota del **fondo** del piezómetro |
| $P/\rho_w g$ | carga de presión, $h_p$ | longitud de la columna de agua en el tubo |

$$h = z + h_p$$

### Idea 2 — La ley de Darcy, con su signo

$$\mathbf{q} = -K\,\nabla h
\qquad\qquad
Q = q\,A = -K A\frac{dh}{dL}$$

$q$ es la **descarga específica**: caudal por unidad de área **total** (sólidos
incluidos). No es la velocidad del agua. La velocidad real es

$$v = \frac{q}{n_e}$$

y es mucho mayor, porque el agua sólo circula por los poros conectados.

### Idea 3 — Hay dos permeabilidades y se confunden

$$K = \frac{k\,\rho_w\,g}{\mu}$$

$k$ (m², darcy) depende **sólo del medio**. $K$ (m/s, m/día) depende del medio
**y del fluido**. En hidrogeología siempre se usa $K$.

Y dos parámetros más que son los de la prueba de bombeo:

$$T = K\,b
\qquad\qquad
S = S_s\,b = \rho_w g\,b\,(\beta_p + n\beta_w)$$

### Idea 4 — La ecuación de flujo es conservación de masa

$$\nabla^{2}h = \frac{S}{T}\frac{\partial h}{\partial t}$$

Dos casos límite que hay que reconocer de inmediato:

- **Régimen permanente** ($\partial h/\partial t = 0$): queda $\nabla^{2}h = 0$,
  la ecuación de Laplace. Es la base de las **redes de flujo**.
- **Régimen transitorio**: aparece la combinación $\sqrt{Tt/S}$, la **longitud de
  difusión**, que es la distancia a la que ha llegado la perturbación. Está
  dentro de todas las fórmulas de pruebas de bombeo.

### Idea 5 — Esfuerzo efectivo (Terzaghi)

$$\sigma' = \sigma_T - u$$

El esqueleto del suelo sólo resiste a través de $\sigma'$. Si la presión de poro
$u$ iguala al esfuerzo total $\sigma_T$, el suelo pierde toda su resistencia:
reventón del fondo de una excavación, arenas movedizas.

### Idea 6 — La ecuación es lineal, así que todo se suma

Los efectos de varios pozos, o de un pozo más una frontera, se suman:

$$s_{total} = \sum_i s_i$$

De aquí salen la interferencia entre pozos, el método de recuperación y el método
de los pozos imagen.

## Mapa de fórmulas

| Tema | Fórmula |
|---|---|
| Darcy | $q = -K\,dh/dL$,  $Q = qA$,  $v = q/n_e$ |
| Carga | $h = z + h_p$,  $\phi = gh$ |
| Permeabilidad | $K = k\rho g/\mu$,  $T = Kb$,  $S = S_s b$ |
| Capas, horizontal | $K_h = \dfrac{\sum K_ib_i}{\sum b_i}$  (aritmética) |
| Capas, vertical | $K_v = \dfrac{\sum b_i}{\sum b_i/K_i}$  (armónica) |
| Red anisótropa | $K_{eq} = \sqrt{K_hK_v}$,  $x' = x\sqrt{K_v/K_h}$ |
| Flujo | $\nabla^2h = (S/T)\,\partial h/\partial t$;  permanente: $\nabla^2h=0$ |
| Redes de flujo | $Q = K\,H\,n_f/n_d$ |
| Esfuerzos | $\sigma'=\sigma_T-u$,  $u=\gamma_w h_p$,  $FS=\sigma_T/u$ |
| | $d_{crit} = \dfrac{\gamma_{sat}D-\gamma_w h_p}{\gamma_{sat}-\gamma_w}$ |
| Theis | $s = \dfrac{Q}{4\pi T}W(u)$,  $u = \dfrac{r^2S}{4Tt}$ |
| Cooper-Jacob | $T = \dfrac{2.303Q}{4\pi\,\Delta s}$,  $S = \dfrac{2.25\,T\,t_0}{r^2}$ |
| Distancia–abatimiento | $T = \dfrac{2.303Q}{2\pi\,\Delta s_r}$,  $S = \dfrac{2.25\,T\,t}{r_0^2}$ |
| Recuperación | $T = \dfrac{2.303Q}{4\pi\,\Delta s'}$,  $s'=\dfrac{2.303Q}{4\pi T}\log\dfrac{t}{t'}$ |
| Thiem (confinado) | $T = \dfrac{Q\ln(r_2/r_1)}{2\pi(s_1-s_2)}$ |
| Dupuit (libre) | $K = \dfrac{Q\ln(r_2/r_1)}{\pi(h_2^2-h_1^2)}$ |
| Radio de influencia | $R_0 = \sqrt{2.25\,Tt/S} = 1.5\sqrt{Tt/S}$ |
| Upconing | $Q_{max} = 0.6\pi K d^2 G$,  $G=\Delta\rho/\rho_f=0.025$ |
| Cuña salina | $x_{toe} = \dfrac{KGB^2}{2q'} - \dfrac{q'}{2KG}$ |

**Constantes y conversiones**

$$\rho_w = 1000\ \mathrm{kg/m^3}
\quad g = 9.81\ \mathrm{m/s^2}
\quad \gamma_w = 9810\ \mathrm{N/m^3} = 62.4\ \mathrm{lb/ft^3}$$

$$\frac{2.303}{4\pi} = 0.1833
\quad \frac{2.303}{2\pi} = 0.3665
\quad \frac{1}{4\pi} = 0.07958
\quad \sqrt{2.25} = 1.5$$

$$1\ \mathrm{L/s} = 86.4\ \mathrm{m^3/día}
\qquad 1\ \mathrm{día} = 1440\ \mathrm{min} = 86\,400\ \mathrm{s}
\qquad 1\ \mathrm{ft} = 0.3048\ \mathrm{m}$$

## La regla de oro de las unidades

Elige al principio **un** sistema y no lo cambies. Para pruebas de bombeo lo más
cómodo es:

$$Q\ \text{en m}^3/\text{día}
\qquad r\ \text{en m}
\qquad t\ \text{en días}
\qquad T\ \text{en m}^2/\text{día}$$

Los tiempos de las tablas vienen casi siempre en **minutos**: divídelos por 1440
antes de hacer cualquier cosa. El error más común y más caro del parcial es meter
$t_0$ en minutos en la fórmula de $S$: te equivocas por un factor de 1440.

# PARTE 1 — Papel logarítmico y semilogarítmico

Este es el capítulo que hay que leer primero, porque sin él la prueba de bombeo
es imposible. No es matemática avanzada: es aprender a leer una regla distinta.

## 1.1 Qué es una escala logarítmica

En una escala **lineal**, la distancia entre marcas es la misma: de 1 a 2 hay lo
mismo que de 9 a 10. En una escala **logarítmica**, la posición de un número es
su logaritmo, de modo que las marcas se van apretando.

![**Figura 1.** Comparación de las dos escalas. En la logarítmica, la posición del número 3 está al 48 % del ciclo porque $\log_{10}3 = 0.477$. Fíjate en que de 1 a 2 hay el mismo espacio que de 5 a 10: en ambos casos el número se duplica.](fig/fig_g1_escala.png){width=15.8cm}

**La regla fundamental:** en una escala logarítmica, **distancias iguales
corresponden a multiplicaciones iguales**. Avanzar un tramo fijo siempre
significa multiplicar por el mismo factor.

Un **ciclo logarítmico** es el tramo en que el número se multiplica por 10:
de 1 a 10, de 10 a 100, de 100 a 1000. Todos los ciclos miden lo mismo en el
papel.

## 1.2 Los porcentajes que hay que memorizar

Para dibujar o leer dentro de un ciclo, basta con saber a qué porcentaje del
ciclo cae cada número. Es $100\log_{10}$ del número:

| Número | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| % del ciclo | 0 | **30** | **48** | **60** | **70** | 78 | 85 | 90 | 95 | 100 |

Con los cuatro primeros (30, 48, 60, 70) ya puedes dibujar un ciclo decente a
mano. Nota el patrón: la primera mitad del ciclo (de 1 a 3) se come casi la mitad
del espacio, y de 5 a 10 sólo queda el 30 %.

## 1.3 Cómo dibujar papel semilogarítmico a mano

![**Figura 2.** Plantilla de papel semilogarítmico de cuatro ciclos, con las instrucciones para reproducirlo a mano. El eje horizontal es logarítmico; el vertical, lineal y normal.](fig/fig_g5_plantilla.png){width=15.8cm}

**Procedimiento (3 minutos con regla):**

1. Decide cuántos ciclos necesitas. Si los tiempos van de 1 a 1440 minutos,
   necesitas **4 ciclos** (1–10, 10–100, 100–1000, 1000–10000).
2. Divide el ancho de la hoja en 4 tramos **iguales**. Rotula las divisiones
   1, 10, 100, 1000, 10000.
3. Dentro de cada tramo, marca los porcentajes de la tabla: 30 %, 48 %, 60 %,
   70 %, 78 %, 85 %, 90 %, 95 %. Esos son el 2, 3, 4, 5, 6, 7, 8, 9 del tramo.
4. El eje vertical (abatimiento) es **lineal**: divisiones iguales, como siempre.

> **Atajo si no tienes regla:** para medir $\Delta s$ sólo necesitas **dos puntos
> de la recta separados exactamente un ciclo** (por ejemplo 100 y 1000 minutos).
> No hace falta dibujar las subdivisiones intermedias con precisión.

## 1.4 Por qué se usa: convierte curvas en rectas

![**Figura 3.** Los mismos datos de una prueba de bombeo. A la izquierda, en escala lineal: una curva de la que no se puede extraer nada, con los primeros once puntos apelotonados. A la derecha, en escala logarítmica: una recta.](fig/fig_g2_lineal_vs_log.png){width=15.8cm}

La razón matemática es que la solución del flujo hacia un pozo tiene la forma

$$s = \text{constante} \times \log t + \text{otra constante}$$

Y eso, graficado contra $\log t$, es una recta. Cuando una cantidad depende del
**logaritmo** de otra, el papel semilog la endereza. Entonces la pendiente y el
punto de corte de la recta tienen significado físico.

## 1.5 Semilog contra log-log: cuándo cada uno

| Papel | Qué ejes | Para qué |
|---|---|---|
| **Semilogarítmico** | $x$ logarítmico, $y$ lineal | Cooper-Jacob, distancia–abatimiento, recuperación. **Es el del 90 % de los casos.** |
| **Logarítmico doble (log-log)** | ambos logarítmicos | método de Theis (curva patrón) |

![**Figura 4.** Papel log-log. Se usa para Theis porque la curva patrón $W(u)$ frente a $1/u$ y los datos $s$ frente a $t$ tienen **la misma forma** en log-log: sólo están desplazados uno respecto al otro. Al superponerlos se mide el desplazamiento y de ahí salen $T$ y $S$.](fig/fig_g4_loglog.png){width=15.8cm}

**La idea de fondo de log-log:** si $s \propto Q\,W(u)$ y $t \propto 1/u$, al tomar
logaritmos en ambos ejes la relación entre $s$ y $t$ es la misma que entre $W$ y
$1/u$, más una constante. Una constante aditiva en logaritmos es un
**desplazamiento** en el papel. Por eso las dos curvas coinciden al deslizar una
sobre otra sin girarla.

## 1.6 Cómo leer una recta en papel semilogarítmico

Esto es el corazón del método. Son cuatro pasos.

![**Figura 5.** Los cuatro pasos. Nota que $\Delta s$ se mide **sobre un ciclo completo** (100 → 1000 min) y que $t_0$ se obtiene **extrapolando** la recta hasta cortar el eje $s = 0$, aunque allí no haya datos.](fig/fig_g3_leer_recta.png){width=15.8cm}

**Paso 1 — Trazar la recta.** Por los puntos de tiempo **tardío**. Los primeros
puntos siempre se curvan por debajo de la recta; eso no es error de medición
(se explica en la Parte 7).

**Paso 2 — Medir $\Delta s$.** Elige dos tiempos separados **exactamente un
ciclo** (1 y 10, 10 y 100, 100 y 1000) y resta las dos ordenadas de la recta:

$$\Delta s = s(t_2) - s(t_1)
\qquad\text{con } t_2 = 10\,t_1$$

**Paso 3 — Leer $t_0$.** Prolonga la recta hacia la izquierda hasta que corte la
horizontal $s = 0$. Ese tiempo es $t_0$. Casi siempre cae fuera del rango de
datos, en los primeros minutos; es normal.

**Paso 4 — Aplicar las fórmulas.** $T$ sale de la pendiente, $S$ del corte.

### Si no quieres dibujar: la versión algebraica

Si tienes dos puntos de la recta $(t_1, s_1)$ y $(t_2, s_2)$ **cualesquiera**:

$$\Delta s = \frac{s_2 - s_1}{\log_{10}(t_2/t_1)}
\qquad\qquad
t_0 = t_1 \times 10^{\,-s_1/\Delta s}$$

La primera fórmula normaliza la pendiente a un ciclo completo. La segunda
extrapola hasta $s=0$. **Memoriza estas dos**: te salvan si el dibujo te sale
torcido.

## 1.7 Ejemplo resuelto 1.1 — Ubicar números en la escala

**Enunciado.** (a) ¿A qué porcentaje del ciclo cae el número 3.5? (b) En un ciclo
que empieza en 100, ¿qué número está al 65 % del tramo? (c) ¿Qué número está a la
mitad exacta de un ciclo que empieza en 10?

**Solución.**

**(a)** La posición es el logaritmo:

$$100\log_{10}(3.5) = 100\,(0.5441) = \boxed{54.4\ \%}$$

Es decir, un poco más allá de la mitad del tramo. Comprobación de sensatez: el 3
está al 48 % y el 4 al 60 %, así que 3.5 debe caer entre ambos ✓

**(b)** Hay que invertir el logaritmo. Si el ciclo empieza en 100 y avanzamos una
fracción $f$ del ciclo:

$$\text{número} = 100 \times 10^{\,f} = 100 \times 10^{0.65} = 100\,(4.467)
= \boxed{446.7}$$

**(c)** A la mitad exacta, $f = 0.5$:

$$10 \times 10^{0.5} = 10\,(3.162) = \boxed{31.6}$$

> **Lo interesante del inciso (c):** el punto medio geométrico de un ciclo no es
> el promedio aritmético (que sería 55), sino $\sqrt{10\times100} = 31.6$. En
> escala logarítmica, "la mitad" significa la **media geométrica**. Esto explica
> por qué más adelante, para medir $\Delta s$, no sirve promediar tiempos.

## 1.8 Ejemplo resuelto 1.2 — Leer una recta ya trazada

**Enunciado.** En una prueba de bombeo con $Q = 1200$ m³/día y un piezómetro a
$r = 40$ m, la recta de Cooper-Jacob pasa por los puntos
$(t = 20\ \mathrm{min},\ s = 0.60\ \mathrm{m})$ y
$(t = 200\ \mathrm{min},\ s = 1.42\ \mathrm{m})$.
Hallar $\Delta s$, $t_0$, $T$ y $S$.

**Solución paso a paso.**

**Paso 1 — ¿Están separados un ciclo?** $200/20 = 10$. Sí, exactamente un ciclo.
Entonces $\Delta s$ es la resta directa:

$$\Delta s = 1.42 - 0.60 = \boxed{0.82\ \mathrm{m\ por\ ciclo}}$$

(Si no estuvieran separados un ciclo, habría que dividir por $\log_{10}(t_2/t_1)$.)

**Paso 2 — Hallar $t_0$.** La ecuación de la recta, tomando el punto $(20, 0.60)$
como referencia, es

$$s = 0.60 + 0.82\,\log_{10}\!\left(\frac{t}{20}\right)$$

Imponemos $s = 0$:

$$0 = 0.60 + 0.82\log_{10}\!\left(\frac{t_0}{20}\right)
\;\Longrightarrow\;
\log_{10}\!\left(\frac{t_0}{20}\right) = -\frac{0.60}{0.82} = -0.7317$$

$$t_0 = 20 \times 10^{-0.7317} = 20\,(0.1855) = \boxed{3.71\ \mathrm{min}}$$

En días: $t_0 = 3.71/1440 = 2.58\times10^{-3}$ días.

**Paso 3 — Transmisividad.**

$$T = \frac{2.303\,Q}{4\pi\,\Delta s}
= \frac{2.303\,(1200)}{4\pi\,(0.82)}
= \frac{2763.6}{10.304}
= \boxed{268\ \mathrm{m^2/día}}$$

**Paso 4 — Almacenamiento.**

$$S = \frac{2.25\,T\,t_0}{r^{2}}
= \frac{2.25\,(268)\,(2.58\times10^{-3})}{(40)^{2}}
= \frac{1.556}{1600}
= \boxed{9.7\times10^{-4}}$$

**Paso 5 — ¿Tiene sentido?** $S \approx 10^{-3}$ es el rango típico de un acuífero
confinado ✓. Si el espesor fuera, digamos, 20 m, entonces
$K = 268/20 = 13.4$ m/día $= 1.6\times10^{-4}$ m/s, que es arena limpia ✓

> **El error que evita este ejemplo:** si hubieras metido $t_0 = 3.71$ (minutos)
> en la fórmula de $S$, te habría salido $S = 1.4$, un valor imposible (mayor que
> la porosidad). Cuando $S$ te salga absurdo, lo primero que hay que revisar son
> las unidades de $t_0$.

## 1.9 Ejemplo resuelto 1.3 — Dos puntos que no están a un ciclo

**Enunciado.** La recta pasa por $(t = 15\ \mathrm{min},\ s = 0.44\ \mathrm{m})$ y
$(t = 600\ \mathrm{min},\ s = 1.73\ \mathrm{m})$. Hallar $\Delta s$ por ciclo.

**Solución.** Primero, cuántos ciclos hay entre los dos tiempos:

$$\log_{10}\!\left(\frac{600}{15}\right) = \log_{10}(40) = 1.602\ \text{ciclos}$$

El abatimiento subió 1.29 m en 1.602 ciclos, de modo que por ciclo:

$$\Delta s = \frac{1.73 - 0.44}{1.602} = \frac{1.29}{1.602}
= \boxed{0.805\ \mathrm{m\ por\ ciclo}}$$

**La trampa:** si hubieras restado sin dividir ($1.29$ m) habrías sobrestimado la
pendiente un 60 %, y por tanto subestimado $T$ en la misma proporción. **Siempre
verifica cuántos ciclos abarcan tus dos puntos.**

## 1.10 Ejercicios para desarrollar

**P1.1** En una prueba de bombeo con $Q = 2000$ m³/día y $r = 60$ m, la recta pasa
por $(t = 10\ \mathrm{min},\ s = 0.35\ \mathrm{m})$ y
$(t = 1000\ \mathrm{min},\ s = 1.55\ \mathrm{m})$.

a. ¿Cuántos ciclos separan los dos puntos?
b. Calcula $\Delta s$ por ciclo.
c. Calcula $t_0$ en minutos y en días.
d. Calcula $T$ y $S$.
e. Si el acuífero tiene 18 m de espesor, calcula $K$ en m/día y en m/s, y di a
   qué material corresponde.

**P1.2** Preguntas de escala:

a. ¿A qué porcentaje del ciclo cae el número 6.5?
b. En un ciclo que empieza en 1000, ¿qué número está al 25 % del tramo?
c. ¿Cuál es el punto medio (en el papel) de un ciclo que va de 100 a 1000?
d. Dos puntos están separados por 2.3 ciclos. Si el primero es $t = 5$ min,
   ¿cuál es el segundo?

*Respuestas en el Anexo C.*

# PARTE 2 — Darcy, cargas y unidades

## 2.1 Teoría

### La ley

Darcy (1856) midió que el caudal por un filtro de arena es proporcional al área y
a la pérdida de carga, e inversamente proporcional a la longitud:

$$Q = -K\,A\,\frac{dh}{dL}
\qquad\qquad
q = \frac{Q}{A} = -K\,\frac{dh}{dL} = -K\,i$$

El **signo menos** dice que el flujo va hacia donde la carga **disminuye**. Si lo
omites, la respuesta queda mal firmada. El gradiente $i = dh/dL$ es adimensional.

### Las tres velocidades que se confunden

| Nombre | Símbolo | Qué es |
|---|---|---|
| Descarga específica, "velocidad de Darcy" | $q$ | caudal / área **total** |
| Velocidad lineal media, velocidad **real** | $v = q/n_e$ | la del agua en los poros |
| Caudal | $Q = qA$ | volumen por tiempo |

**Por qué $v = q/n_e$ y no al contrario.** El caudal se conserva. Pasa por un área
total $A$, pero sólo por la fracción $n_e A$ hay agua circulando:

$$Q = q\,A = v\,(n_e A)
\qquad\Longrightarrow\qquad
v = \frac{q}{n_e}$$

Como $n_e < 1$, dividir aumenta: la velocidad real es **mayor** que $q$. Esa es la
comprobación mental que evita invertir la fórmula.

### Las tres cargas

$$h = z + h_p$$

$z$ es la cota del **fondo** del piezómetro (donde está la rejilla). $h_p$ es la
altura de la columna de agua **por encima de ese fondo**. $h$ es la cota del nivel
de agua. Con dos cualesquiera obtienes la tercera.

### Permeabilidad y unidades

$$K = \frac{k\,\rho_w\,g}{\mu}
\qquad\Longleftrightarrow\qquad
k = \frac{K\,\mu}{\rho_w\,g}$$

Factores que conviene llevar memorizados:

$$1\ \mathrm{ft} = 0.3048\ \mathrm{m}
\quad 1\ \mathrm{ft^3} = 7.4805\ \mathrm{gal}
\quad 1\ \mathrm{darcy} = 9.87\times10^{-9}\ \mathrm{cm^2}$$

$$1\ \mathrm{m^2} = 10^{4}\ \mathrm{cm^2}\ \text{(al cuadrado, no } 10^2)$$

**Verificación rápida:** para agua a 20 °C, $1\ \text{darcy} \approx 9.66\times10^{-6}$ m/s.

### Órdenes de magnitud (para el paso de "¿tiene sentido?")

| Material | $K$ (m/s) | $K$ (m/día) |
|---|---|---|
| Grava | $10^{-2}$–1 | $10^{3}$–$10^{5}$ |
| Arena limpia | $10^{-5}$–$10^{-2}$ | 1–$10^{3}$ |
| Arena fina, limo | $10^{-8}$–$10^{-5}$ | $10^{-3}$–1 |
| Arcilla | $<10^{-8}$ | $<10^{-3}$ |

## 2.2 Ejemplo resuelto 2.1 — Descarga específica y velocidad real

**Enunciado.** Un acuífero tiene $K = 10^{-6}$ m/s y el gradiente hidráulico es
0.019. Calcular $q$. Luego calcular la velocidad real si la porosidad efectiva es
(a) 0.1 y (b) 0.0001. Explicar la diferencia.

*(Es el ejercicio 1-3 del taller del profesor.)*

**Solución.**

**Paso 1 — Descarga específica.** Aplicación directa de Darcy en magnitudes:

$$q = K\,i = (10^{-6}\ \mathrm{m/s})(0.019) = \boxed{1.9\times10^{-8}\ \mathrm{m/s}}$$

Para "sentir" el número, pásalo a m/año multiplicando por $3.156\times10^{7}$:

$$q = 1.9\times10^{-8} \times 3.156\times10^{7} = 0.60\ \mathrm{m/año}$$

**Paso 2 — Velocidad real.**

$$v_a = \frac{1.9\times10^{-8}}{0.1} = \boxed{1.9\times10^{-7}\ \mathrm{m/s}}
= 6.0\ \mathrm{m/año}$$

$$v_b = \frac{1.9\times10^{-8}}{0.0001} = \boxed{1.9\times10^{-4}\ \mathrm{m/s}}
= 5990\ \mathrm{m/año}$$

**Paso 3 — Interpretar.** El caudal por unidad de área es **idéntico** en los dos
casos, pero la velocidad real difiere en un factor de 1000. La razón:

- $n_e = 0.1$ → medio **granular** (arena, grava): el agua usa todo el espacio
  intergranular.
- $n_e = 0.0001$ → **roca fracturada** (granito, basalto, caliza fisurada): el
  agua circula por un puñado de fracturas que son una fracción diminuta del
  volumen.

**Por qué importa.** $n_e$ no controla el caudal, controla el **tiempo de
tránsito**. En roca fracturada un contaminante puede recorrer kilómetros en el
tiempo que en arena tardaría siglos. Esta es la respuesta que el profesor busca.

## 2.3 Ejemplo resuelto 2.2 — Tabla de piezómetros

**Enunciado.** Gradiente 0.019. El nivel de agua en el punto A está a 300 m sobre
el nivel del mar. El nivel de agua en todos los piezómetros está en el tope del
piezómetro. Están separados 5000 m. Completar la tabla.

| Piezómetro | A | B | C | D |
|---|---|---|---|---|
| Profundidad (m) | 200 | 190 | 50 | 8 |

*(Es el ejercicio 7 del taller.)*

![**Figura 6.** Los cuatro piezómetros con su carga total, carga de presión y carga de elevación. Observa cómo $h_p$ decrece hacia D: es una zona de descarga.](fig/fig_3_07_piezometros.png){width=15.8cm}

**Solución.**

**Paso 1 — Carga total.** Es la única fila que se puede calcular sin más
información. La pérdida de carga entre piezómetros consecutivos es

$$\Delta h = i\,\Delta L = (0.019)(5000) = 95\ \mathrm{m}$$

$$h_A = 300 \quad h_B = 205 \quad h_C = 110 \quad h_D = 15\ \mathrm{m}$$

**Paso 2 — Carga de presión.** Aquí está la frase clave del enunciado: *"el nivel
de agua está en el tope del piezómetro"*. Eso significa que la columna de agua
ocupa **todo** el tubo. Y como la medida se refiere al fondo:

$$h_p = \text{profundidad del piezómetro}$$

$$h_{p,A}=200 \quad h_{p,B}=190 \quad h_{p,C}=50 \quad h_{p,D}=8\ \mathrm{m}$$

> Sin esa frase el problema no tendría solución. En los enunciados de
> hidrogeología, **las frases aparentemente decorativas suelen ser el dato que
> falta**. Subráyalas.

**Paso 3 — Carga de elevación.** Por diferencia, $z = h - h_p$:

| Piezómetro | A | B | C | D |
|---|---|---|---|---|
| $h$ (m) | **300** | **205** | **110** | **15** |
| $h_p$ (m) | **200** | **190** | **50** | **8** |
| $z$ (m) | **100** | **15** | **60** | **7** |

**Paso 4 — Verificar.** $z$ es la cota del fondo del piezómetro, y debe ser
positiva (están sobre el nivel del mar según la figura) ✓. Y la topografía
descendente de A a D es coherente ✓

**Paso 5 — Interpretar.** $h_p$ cae de 200 a 8 m: los piezómetros se vuelven cada
vez más someros porque la superficie piezométrica se acerca al terreno. Eso es la
firma de una **zona de descarga**, donde el agua subterránea tiende a salir.

## 2.4 Ejemplo resuelto 2.3 — Conversiones de unidades

**Enunciado.** Una formación tiene $K = 10^{-6}$ m/s. Calcular (a) $K$ en ft/s,
(b) $K$ en gal/día por ft², (c) la permeabilidad en cm², (d) la permeabilidad en
darcys.

*(Es el ejercicio 8 del taller.)*

**Solución.**

**(a)** Dividir por la longitud del pie:

$$K = \frac{10^{-6}\ \mathrm{m/s}}{0.3048\ \mathrm{m/ft}}
= \boxed{3.28\times10^{-6}\ \mathrm{ft/s}}$$

**(b)** El truco conceptual: $K$ en ft/s **ya es** un caudal por unidad de área,
porque $L/T$ es idéntico a $L^3/T$ dividido por $L^2$. Entonces sólo hay que
convertir el volumen a galones y el tiempo a días:

$$K = (3.28\times10^{-6})\,(7.4805)\,(86\,400)
= \boxed{2.12\ \mathrm{gal/día\cdot ft^2}}$$

**(c)** Invertir la relación entre $K$ y $k$, con $\mu = 1.0\times10^{-3}$ Pa·s a
20 °C:

$$k = \frac{K\mu}{\rho_w g}
= \frac{(10^{-6})(1.0\times10^{-3})}{(1000)(9.81)}
= 1.019\times10^{-13}\ \mathrm{m^2}$$

$$k = 1.019\times10^{-13}\ \mathrm{m^2} \times 10^{4}\ \frac{\mathrm{cm^2}}{\mathrm{m^2}}
= \boxed{1.02\times10^{-9}\ \mathrm{cm^2}}$$

**(d)**

$$k = \frac{1.019\times10^{-9}\ \mathrm{cm^2}}{9.87\times10^{-9}\ \mathrm{cm^2/darcy}}
= \boxed{0.103\ \mathrm{darcy} = 103\ \mathrm{md}}$$

**Verificación independiente.** Usando la equivalencia práctica
$1\ \text{darcy} \approx 9.66\times10^{-6}$ m/s:

$$0.103 \times 9.66\times10^{-6} = 1.0\times10^{-6}\ \mathrm{m/s}\ \checkmark$$

**Sentido físico.** $K = 10^{-6}$ m/s ≈ 0.1 darcy es una **arena fina a limo
arenoso**: transmite agua, pero mal.

> **Declara siempre la temperatura.** $\mu$ vale $1.00\times10^{-3}$ Pa·s a 20 °C
> y $1.124\times10^{-3}$ a 15.6 °C (60 °F, el estándar americano antiguo). La
> diferencia en el resultado es del 12 %. Escribir la hipótesis vuelve la
> respuesta inatacable.

## 2.5 Ejercicios para desarrollar

**P2.1** Un acuífero confinado tiene $K = 2.5\times10^{-5}$ m/s. El gradiente
hidráulico es 0.004 y la sección transversal del flujo es 120 m². La porosidad
efectiva es 0.18.

a. Calcula la descarga específica $q$ en m/s y en m/día.
b. Calcula el caudal $Q$ en m³/s y en m³/día.
c. Calcula la velocidad real $v$ en m/día.
d. ¿Cuánto tarda una partícula de agua en recorrer 500 m? Da el resultado en
   años.
e. ¿A qué material corresponde esa $K$?

**P2.2** Un piezómetro se perfora en un terreno cuya superficie está a la cota
450 m. El piezómetro tiene 180 m de profundidad y el nivel de agua se encuentra a
12 m por debajo de la superficie del terreno.

a. ¿Cuál es la carga total $h$ en el punto de medida?
b. ¿Cuál es la carga de elevación $z$?
c. ¿Cuál es la carga de presión $h_p$?
d. Verifica tu resultado comprobando la longitud de la columna de agua dentro
   del tubo.

*Respuestas en el Anexo C.*

# PARTE 3 — Heterogeneidad y anisotropía

## 3.1 Teoría

### Capas: la analogía eléctrica

| Hidráulica | Electricidad |
|---|---|
| Carga $h$ | Voltaje |
| Caudal $Q$ | Corriente |
| $L/(KA)$ | Resistencia |

**Flujo HORIZONTAL (paralelo a las capas).** El agua puede escoger por cuál capa
viajar y todas ven la misma pérdida de carga: es un circuito en **paralelo**, y
los caudales se suman:

$$\boxed{K_h = \frac{\sum K_i b_i}{\sum b_i}}\qquad \text{media ARITMÉTICA ponderada}$$

**Flujo VERTICAL (perpendicular a las capas).** El agua está obligada a cruzar
todas las capas en secuencia: circuito en **serie**, el caudal es el mismo y las
pérdidas de carga se suman:

$$\boxed{K_v = \frac{\sum b_i}{\sum (b_i/K_i)}}\qquad \text{media ARMÓNICA ponderada}$$

![**Figura 7.** Flujo horizontal (capas en paralelo, media aritmética) y flujo vertical (capas en serie, media armónica).](fig/fig_3_11_capas.png){width=15.8cm}

**Cómo no confundirlas nunca más:**

$$\boxed{K_h \text{ la domina la capa MÁS permeable}
\qquad
K_v \text{ la domina la capa MENOS permeable}}$$

El flujo horizontal se escapa por la autopista; el vertical queda atrapado en el
cuello de botella. Y siempre $K_v \le K_h$.

### Anisotropía: $K$ es un tensor

En un medio anisótropo, un gradiente en $x$ puede producir flujo en $y$:

$$q_x = -\left(K_{xx}\frac{\partial h}{\partial x} + K_{xy}\frac{\partial h}{\partial y}\right)
\qquad
q_y = -\left(K_{yx}\frac{\partial h}{\partial x} + K_{yy}\frac{\partial h}{\partial y}\right)$$

El tensor es **simétrico**: $K_{xy} = K_{yx}$. Esa propiedad es la que permite
resolver los problemas de términos cruzados.

**Consecuencia:** si $K_{xy} \ne 0$, el vector $\mathbf{q}$ **no es paralelo** a
$\nabla h$. El flujo se desvía respecto a la máxima pendiente de la superficie
piezométrica. Esto es lo que hace que en medios anisótropos las líneas de flujo
**no** corten a las equipotenciales a 90°.

## 3.2 Ejemplo resuelto 3.1 — Tres capas

**Enunciado.** Tres formaciones horizontales, homogéneas e isótropas, de 20 m de
espesor cada una, con conductividades $10^{-6}$, $10^{-7}$ y $10^{-8}$ m/s.
Calcular las componentes horizontal y vertical de la conductividad del medio
equivalente.

*(Es el ejercicio 11 del taller.)*

**Solución.**

**Paso 1 — Horizontal (aritmética).**

$$K_h = \frac{\sum K_ib_i}{\sum b_i}
= \frac{20\,(10^{-6}+10^{-7}+10^{-8})}{60}
= \frac{20\,(1.11\times10^{-6})}{60}
= \frac{2.22\times10^{-5}}{60}$$

$$\boxed{K_h = 3.70\times10^{-7}\ \mathrm{m/s}}$$

**Paso 2 — Vertical (armónica).**

$$K_v = \frac{\sum b_i}{\sum (b_i/K_i)}
= \frac{60}{\dfrac{20}{10^{-6}}+\dfrac{20}{10^{-7}}+\dfrac{20}{10^{-8}}}$$

Los tres términos del denominador son $2\times10^{7}$, $2\times10^{8}$ y
$2\times10^{9}$, que suman $2.22\times10^{9}$:

$$K_v = \frac{60}{2.22\times10^{9}} = \boxed{2.70\times10^{-8}\ \mathrm{m/s}}$$

**Paso 3 — Anisotropía.**

$$\frac{K_h}{K_v} = \frac{3.70\times10^{-7}}{2.70\times10^{-8}} = \boxed{13.7}$$

**Paso 4 — Verificar.** $K_h = 3.7\times10^{-7}$ está cerca del valor **mayor**
($10^{-6}$) ✓. $K_v = 2.7\times10^{-8}$ está cerca del **menor** ($10^{-8}$) ✓.
Y $K_v < K_h$ ✓

**Conclusión que hay que escribir.** Aunque cada capa es isótropa, el conjunto se
comporta a escala macroscópica como un medio **anisótropo** con $K_h/K_v = 13.7$.
Esto explica por qué los acuíferos regionales son "planos" y por qué las plumas
de contaminación se extienden lateralmente en vez de hundirse.

## 3.3 Ejemplo resuelto 3.2 — Términos cruzados del tensor

**Enunciado.** Una muestra se somete a un gradiente $\partial h/\partial x = 0.1$
cm/cm en la dirección $x$ y se mide un flujo de 0.001 cm/s en la dirección $y$
(no hay gradiente en $y$). Luego se somete a un gradiente
$\partial h/\partial y = 0.01$ cm/cm y se mide un flujo $q_x$. ¿Cuánto vale $q_x$?

*(Es el ejercicio 12 del taller.)*

**Solución.**

**Paso 1 — Del primer ensayo, despejar el término cruzado.** El enunciado dice que
**no hay gradiente en $y$**, así que el segundo término de la ecuación de $q_y$
desaparece y queda una sola incógnita:

$$q_y = K_{yx}\frac{\partial h}{\partial x}
\;\Longrightarrow\;
K_{yx} = \frac{q_y}{\partial h/\partial x} = \frac{0.001}{0.1} = 0.01\ \mathrm{cm/s}$$

**Paso 2 — Invocar la simetría.** Este es el concepto que se evalúa:

$$\boxed{K_{xy} = K_{yx} = 0.01\ \mathrm{cm/s}}$$

Sin esta propiedad el problema no tendría solución, porque el primer ensayo mide
$K_{yx}$ y la pregunta es sobre $K_{xy}$.

**Paso 3 — Aplicar al segundo ensayo.** Ahora no hay gradiente en $x$:

$$q_x = K_{xy}\frac{\partial h}{\partial y} = (0.01)(0.01)
= \boxed{1\times10^{-4}\ \mathrm{cm/s}}$$

**Paso 4 — Verificar la coherencia.** El gradiente del segundo ensayo es 10 veces
menor que el del primero (0.01 frente a 0.1) y el flujo cruzado resultante es 10
veces menor ($10^{-4}$ frente a $10^{-3}$). La proporcionalidad directa confirma
el resultado ✓

## 3.4 Ejercicios para desarrollar

**P3.1** Cuatro capas horizontales se superponen, con los siguientes espesores y
conductividades:

| Capa | Espesor (m) | $K$ (m/s) |
|---|---|---|
| 1 | 5 | $3\times10^{-4}$ |
| 2 | 12 | $5\times10^{-7}$ |
| 3 | 8 | $2\times10^{-4}$ |
| 4 | 15 | $8\times10^{-6}$ |

a. Calcula $K_h$ y $K_v$ del medio equivalente.
b. Calcula la relación de anisotropía $K_h/K_v$.
c. ¿Cuál capa domina cada resultado? Justifica.
d. Si el conjunto fuera un acuífero, ¿cuál sería su transmisividad?

**P3.2** Una muestra anisótropa se somete a un gradiente de 0.05 en la dirección
$x$ y se mide un flujo de $2\times10^{-4}$ cm/s en la dirección $y$. Después se
aplica un gradiente de 0.02 en la dirección $y$.

a. Calcula $K_{yx}$.
b. ¿Qué propiedad del tensor te permite continuar?
c. Calcula el flujo $q_x$ que resulta del segundo ensayo.
d. ¿Qué significa físicamente que $K_{xy} \ne 0$?

*Respuestas en el Anexo C.*

# PARTE 4 — Ecuación de flujo y almacenamiento

## 4.1 Teoría

### La ecuación general

Combinando Darcy con el balance de masa en un volumen de control se obtiene

$$\nabla^{2}h = \frac{\rho_w g\,(\beta_p + n\beta_w)}{K}\,\frac{\partial h}{\partial t}
\;\approx\; \frac{S_s}{K}\,\frac{\partial h}{\partial t}$$

**Cómo leerla:** el lado izquierdo es el desbalance entre lo que entra y lo que
sale; el derecho es la rapidez con que cambia el almacenamiento.

| Término | Qué representa |
|---|---|
| $\nabla^2 h$ | entrada menos salida (vía Darcy) |
| $\beta_p$ | compresibilidad de la **matriz**: el esqueleto se compacta y expulsa agua |
| $n\beta_w$ | compresibilidad del **agua**: se expande al despresurizarse |
| $\partial h/\partial t$ | tasa de cambio del almacenamiento |

### Los tres casos particulares que hay que saber

**1-D:** $\dfrac{\partial^{2}h}{\partial x^{2}} = \dfrac{S_s}{K}\dfrac{\partial h}{\partial t}$ — es la **ecuación de difusión**, idéntica a la del calor, con difusividad $\nu = K/S_s = T/S$.

**Fluido incompresible** ($\beta_w = 0$): $\nabla^2h = \dfrac{\rho_w g\beta_p}{K}\dfrac{\partial h}{\partial t}$. Todo el agua sale de la compactación de la matriz.

**Fluido y matriz incompresibles** ($\beta_p = \beta_w = 0$): $\boxed{\nabla^2h = 0}$, la **ecuación de Laplace**. Régimen permanente, sin almacenamiento. **Es la ecuación de todas las redes de flujo.** Esta conexión es la que el profesor quiere ver.

### Almacenamiento

$$S = \rho_w g\,b\,(\beta_p + n\beta_w) \qquad\text{(definición física)}$$

$$V = S\,A\,\Delta h \qquad\text{(definición operacional)}$$

La segunda dice en palabras: $S$ es el **volumen de agua liberado por unidad de
área de acuífero y por unidad de descenso de carga**.

| Parámetro | Rango |
|---|---|
| $S$ confinado | $10^{-5}$ a $10^{-3}$ |
| $S_y$ libre (rendimiento específico) | 0.05 a 0.30 |

Cuatro órdenes de magnitud de diferencia. Por eso los conos de abatimiento de los
acuíferos confinados son gigantescos comparados con los de los libres.

### Dónde se desprecia la compresibilidad del agua

$n\beta_w \approx 0.3 \times 4.8\times10^{-10} \approx 1.4\times10^{-10}$ m²/N es
un valor **fijo**. Entonces la pregunta es: ¿en qué material $\beta_p$ lo supera
con holgura?

| Material | $\beta_p$ (m²/N) | ¿Se desprecia $n\beta_w$? |
|---|---|---|
| **Arcilla** | $10^{-6}$–$10^{-8}$ | **Sí**, por 2 a 4 órdenes |
| Arena, limo | $10^{-8}$–$10^{-9}$ | Sí, con cuidado |
| Grava | $10^{-9}$–$10^{-10}$ | Marginal |
| Caliza, granito | $10^{-10}$–$10^{-11}$ | **No**, es el término dominante |

## 4.2 Ejemplo resuelto 4.1 — Simplificar la ecuación de flujo

**Enunciado.** Para la ecuación $\nabla^2h = \dfrac{\rho_wg(\beta_p+n\beta_w)}{K}\dfrac{\partial h}{\partial t}$:
(a) exprésala para flujo unidimensional; (b) para un medio con fluido
incompresible; (c) para fluido y matriz incompresibles; (d) ¿en qué material
despreciarías $\rho_w g n\beta_w$?

*(Es el ejercicio 1 del capítulo 4 del taller.)*

**Solución.**

**(a)** El laplaciano en una dimensión es sólo la segunda derivada en esa
dirección:

$$\boxed{\frac{\partial^{2}h}{\partial x^{2}} = \frac{S_s}{K}\frac{\partial h}{\partial t}}$$

Y en términos de acuífero, multiplicando por el espesor:
$\dfrac{\partial^2h}{\partial x^2} = \dfrac{S}{T}\dfrac{\partial h}{\partial t}$.

**Nómbrala:** es la ecuación de difusión. Decir eso vale puntos.

**(b)** "Incompresible" se traduce en $\beta_w = 0$. Táchalo:

$$\boxed{\nabla^{2}h = \frac{\rho_w g\,\beta_p}{K}\frac{\partial h}{\partial t}}$$

Interpretación: todo el agua liberada proviene de la compactación del esqueleto.

**(c)** Ahora $\beta_p = \beta_w = 0$ y el lado derecho se anula:

$$\boxed{\nabla^{2}h = 0}$$

Es la **ecuación de Laplace**: no hay almacenamiento, entrada igual salida,
régimen permanente. Es la que gobierna las redes de flujo de la Parte 5.

**(d)** Comparando órdenes de magnitud con la tabla anterior:

$$\boxed{\text{En la ARCILLA}}$$

**La frase que remata:** en materiales rígidos (granito, caliza densa) ocurre lo
**contrario**: $\beta_p$ es tan pequeña que es ella la que se desprecia y domina
la compresibilidad del agua. Por eso la arcilla libera tantísima más agua por
unidad de descenso, y por eso bombear acuíferos con acuitardos arcillosos produce
**subsidencia del terreno**.

## 4.3 Ejemplo resuelto 4.2 — Almacenamiento de un acuífero elástico

**Enunciado.** El almacenamiento de un acuífero elástico es $3\times10^{-4}$. La
porosidad es 0.3, la compresibilidad del agua es $4.8\times10^{-10}$ m²/N y el
espesor es 60 m.

a. ¿Cuántos metros cúbicos se extraen del almacenamiento bajo un área de
   $1\times10^{6}$ m² cuando la carga baja un metro?
b. ¿Cuál sería el almacenamiento si la matriz fuera incompresible?
c. ¿Cuál es el coeficiente de compresibilidad vertical del acuífero?

*(Es el ejercicio 2 del capítulo 4 del taller.)*

**Solución.**

**(a)** Aplicación literal de la definición operacional:

$$V = S\,A\,\Delta h = (3\times10^{-4})(1\times10^{6}\ \mathrm{m^2})(1\ \mathrm{m})
= \boxed{300\ \mathrm{m^3}}$$

**Dale perspectiva:** 300 m³ sobre 1 km² equivale a una lámina de agua de sólo
**0.3 mm**. Eso es lo notable de los acuíferos confinados: para producir
volúmenes útiles hay que bajar muchísimo la carga sobre áreas enormes.

**(b)** Si la matriz es incompresible, $\beta_p = 0$:

$$S = \rho_w g\,b\,n\beta_w = (1000)(9.81)(60)(0.3)(4.8\times10^{-10})$$

Paso a paso: $1000 \times 9.81 = 9810$; $\times 60 = 588\,600$;
$\times 0.3 = 176\,580$; $\times 4.8\times10^{-10}$:

$$\boxed{S = 8.48\times10^{-5}}$$

**Interpreta:** es el 28 % del almacenamiento real
($8.48\times10^{-5}/3\times10^{-4}$). Conclusión para escribir: **el 72 % del
agua que produce este acuífero proviene de la compactación del esqueleto**, no de
la expansión del agua. En consecuencia, bombearlo produce subsidencia.

**(c)** Despejar $\beta_p$ de la misma ecuación:

$$\beta_p = \frac{S}{\rho_w g\,b} - n\beta_w
= \frac{3\times10^{-4}}{(1000)(9.81)(60)} - (0.3)(4.8\times10^{-10})$$

$$\beta_p = 5.097\times10^{-10} - 1.44\times10^{-10}
= \boxed{3.66\times10^{-10}\ \mathrm{m^2/N}}$$

**Verificación obligatoria.** Sustituye de vuelta:
$S = (9810)(60)(3.66\times10^{-10}+1.44\times10^{-10}) = 3.0\times10^{-4}$ ✓

**Contexto:** $\beta_p \approx 3.7\times10^{-10}$ m²/N corresponde a arena o grava
densa. Su inverso, el módulo de compresión $1/\beta_p \approx 2.7$ GPa, es del
orden del módulo volumétrico del agua (2.2 GPa). Por eso los dos términos
compiten en este acuífero.

> **Si $\beta_p$ te sale negativo**, el enunciado sería físicamente imposible
> (significaría que la matriz se expande al cargarla). Es señal de error
> aritmético.

## 4.4 Ejercicios para desarrollar

**P4.1** Un acuífero elástico tiene $S = 5\times10^{-4}$, porosidad 0.25,
espesor 40 m. La compresibilidad del agua es $4.8\times10^{-10}$ m²/N.

a. ¿Qué volumen de agua se libera de un área de 2 km² si la carga baja 1.5 m?
b. ¿Cuál sería $S$ si la matriz fuera incompresible, y qué porcentaje del real
   representa?
c. Calcula $\beta_p$ y verifica tu resultado.
d. ¿Qué fracción del agua producida proviene de la compactación de la matriz?

**P4.2** Un acuífero tiene $T = 250$ m²/día y $S = 4\times10^{-4}$.

a. Calcula la difusividad hidráulica $\nu = T/S$.
b. La longitud de difusión es $\sqrt{\nu t}$. ¿Cuánto tiempo tarda una
   perturbación de carga en "llegar" a 1000 m?
c. Repite para 100 m y para 2000 m. ¿Cómo escala el tiempo con la distancia?
d. ¿Qué significa este resultado para el radio de influencia de un pozo?

*Respuestas en el Anexo C.*

# PARTE 5 — Redes de flujo y condiciones de frontera

## 5.1 Teoría

### La ecuación y las reglas

En régimen permanente, $\nabla^2h = 0$. La solución se puede **dibujar**: dos
familias de curvas ortogonales.

| | Qué es | Propiedad |
|---|---|---|
| **Equipotenciales** | líneas de $h$ = constante | el agua las cruza perpendicularmente |
| **Líneas de flujo** | trayectorias del agua | el agua no las cruza nunca |

**Las seis reglas de construcción:**

1. Líneas de flujo y equipotenciales se cortan a **90°** (en medio isótropo).
2. Las celdas deben ser **cuadrados curvilíneos** (ancho ≈ largo).
3. Las fronteras de **carga constante** son equipotenciales.
4. Las fronteras **impermeables** son líneas de flujo.
5. El flujo va de mayor a menor carga.
6. En esquinas y cambios de tipo de frontera hay **singularidades** (gradiente
   teóricamente infinito).

### Las tres condiciones de frontera

| Frontera | Condición | ¿Es equipotencial? | ¿Es línea de flujo? |
|---|---|---|---|
| Carga constante (embalse, río, mar) | $h$ = cte | **Sí** | No |
| Impermeable (roca, pantalla, divisoria) | $\partial h/\partial n = 0$ | No | **Sí** |
| Nivel freático | $h = z$ | No | No |

**El nivel freático es la sutil.** En él la presión es atmosférica, así que
$h = z + 0 = z$. Consecuencia práctica: **la equipotencial de valor 50 m corta el
nivel freático exactamente en el punto cuya cota es 50 m.** No lo corta a 90°. Y
el agua sí lo cruza: entra como recarga, sale como descarga.

### Caudal a partir de la geometría

$$\boxed{Q = K\,H\,\frac{n_f}{n_d}}$$

$n_f$ = número de canales (tubos) de flujo, $n_d$ = número de saltos de
potencial, $H$ = carga total disponible. El cociente $n_f/n_d$ es el **factor de
forma**: pura geometría, independiente de $K$ y de $H$.

**De dónde sale.** Cada tubo lleva $\Delta Q = K\,\Delta h$ (por unidad de ancho),
y la caída por salto es $\Delta h = H/n_d$. Con $n_f$ tubos, $Q = n_f K H/n_d$.

### Medio anisótropo: la sección transformada

Si $K_h \ne K_v$, las celdas cuadradas no valen. Procedimiento:

1. **Transformar:** $x' = x\sqrt{K_v/K_h}$ (contrae la horizontal).
2. **Dibujar** la red con celdas cuadradas en la sección transformada.
3. **Destransformar:** las celdas quedan rectángulos de relación
   $\sqrt{K_h/K_v}:1$.
4. **Caudal** con la media geométrica: $K_{eq} = \sqrt{K_hK_v}$.

> **Mnemotecnia de las tres medias:** aritmética para capas en paralelo,
> armónica para capas en serie, **geométrica** para la red de flujo anisótropa.

## 5.2 Ejemplo resuelto 5.1 — Clasificar fronteras y calcular filtración

**Enunciado.** En el diagrama de una presa con delantal impermeable, indicar si
AB, BC, CD, DE y FG son equipotenciales o líneas de flujo, y si son fronteras de
carga constante o de no flujo. Después, para una altura de embalse de 20 m y
$K = 5\times10^{-4}$ m/s, calcular el caudal de filtración, y repetirlo con el
delantal a la mitad y sin delantal.

*(Son los ejercicios 6 y 7 del capítulo 4 del taller.)*

![**Figura 8.** Red de flujo bajo la presa, obtenida resolviendo $\nabla^2h = 0$ por diferencias finitas. En azul las equipotenciales; en rojo las líneas de flujo, trazadas de modo que cada tubo transporte el mismo caudal.](fig/fig_4_06_presa.png){width=15.8cm}

**Solución, parte 1 — Clasificar.**

El método son dos preguntas:

> **¿Hay un cuerpo de agua libre en contacto con el medio poroso?**
> Sí → carga constante = equipotencial.
>
> **¿Hay material impermeable, o una simetría que impida el paso?**
> Sí → sin flujo = línea de flujo.

| Frontera | Qué es físicamente | Clasificación |
|---|---|---|
| **AB** | lecho del embalse aguas arriba | **equipotencial, carga constante** ($h$ = nivel del embalse) |
| **BC** | delantal impermeable | **línea de flujo, sin flujo** |
| **CD** | base de la presa | **línea de flujo, sin flujo** |
| **DE** | lecho aguas abajo | **equipotencial, carga constante** ($h$ = nivel de salida) |
| **FG** | base impermeable del estrato | **línea de flujo, sin flujo** |

**Observaciones que suben la nota:** AB y DE son las **únicas** equipotenciales
del contorno; entre ellas se reparte toda la carga $H$. BC, CD y FG forman un
contorno continuo de líneas de flujo: son las paredes del "tubo" por el que
circula el agua. La primera línea de flujo es B-C-D (la más corta) y la última es
F-G (la más larga).

**Solución, parte 2 — Caudal.**

![**Figura 9.** Las tres redes de flujo y el caudal resultante. Acortar el delantal a la mitad aumenta la filtración un 39 %; eliminarlo, un 140 %.](fig/fig_4_07_comparacion.png){width=15.8cm}

Contando sobre cada red y aplicando $Q = KH\,n_f/n_d$:

| Caso | $n_f$ | $n_d$ | $n_f/n_d$ | $Q$ (m³/s por m) | % del base |
|---|---|---|---|---|---|
| Delantal completo | 5 | 14 | 0.357 | $3.64\times10^{-3}$ | 100 % |
| Delantal a la mitad | 5 | 10 | 0.500 | $5.05\times10^{-3}$ | 139 % |
| Sin delantal | 6 | 7 | 0.857 | $8.73\times10^{-3}$ | 240 % |

Cálculo del caso base:

$$Q = K H\frac{n_f}{n_d} = (5\times10^{-4})(20)\left(\frac{5}{14}\right)
= 3.6\times10^{-3}\ \mathrm{m^3/s\ por\ m} = 315\ \mathrm{m^3/día\cdot m}$$

**El concepto, dicho correctamente.** El delantal impermeable no reduce la
filtración "tapando" nada: **alarga la trayectoria del flujo**. Al forzar un
recorrido más largo con la misma carga disponible, el gradiente medio baja y con
él el caudal. En términos de la red: **aumenta $n_d$ sin cambiar $n_f$**.

**Lo que casi nadie añade y vale puntos.** El criterio de diseño real de una presa
no es el caudal de filtración (unos litros por metro y día son irrelevantes),
sino el **gradiente de salida** aguas abajo, que controla la **tubificación**
(*piping*). Si el gradiente de salida supera el crítico

$$i_{crit} = \frac{\gamma_{sat}-\gamma_w}{\gamma_w} \approx 1$$

el suelo es arrastrado y empieza una erosión regresiva que puede destruir la
presa. Nota que es **el mismo principio de esfuerzo efectivo nulo** de la Parte 6.

## 5.3 Ejemplo resuelto 5.2 — Nivel freático inclinado y anisotropía

**Enunciado.** En una sección donde el lado derecho BC es 1.5 veces el lado
izquierdo AD, el fondo DC es horizontal y la frontera superior AB es un nivel
freático inclinado, dibujar la red de flujo suponiendo que DC, AD y BC son
impermeables. Repetirlo para material anisótropo con $K_h = 5K_v$.

*(Son los ejercicios 9 y 10 del capítulo 4 del taller.)*

![**Figura 10.** Red de flujo con nivel freático inclinado. Las equipotenciales cortan el nivel freático donde $h = z$, no a 90°. A la derecha (zona alta) el flujo desciende: es recarga. A la izquierda (zona baja) asciende: es descarga.](fig/fig_4_09_freatico.png){width=15.8cm}

**Solución, parte 1 — Isótropo.**

**Paso 1 — Rotular cada frontera.** AD, BC y DC: impermeables, por tanto líneas de
flujo; las equipotenciales las cortan a 90°. AB: nivel freático, con $h = z$.

**Paso 2 — Usar la condición del nivel freático.** Rotula las cotas a lo largo de
AB. Esos son los valores de $h$ de las equipotenciales que llegan allí, y marcan
**dónde** cada equipotencial debe intersecar el nivel freático.

**Paso 3 — Trazar.** Equipotenciales desde esos puntos hacia abajo, cortando a 90°
las fronteras impermeables. Luego líneas de flujo a 90° de las equipotenciales,
buscando celdas cuadradas. Dos o tres iteraciones de borrador.

**Lo que el dibujo debe mostrar:**

1. **Recarga en B** (zona alta): las líneas de flujo entran al dominio con
   componente descendente. Un piezómetro profundo mediría **menos** carga que uno
   somero.
2. **Descarga en A** (zona baja): las líneas de flujo salen, con componente
   ascendente. Un piezómetro profundo mediría **más** carga que uno somero:
   condición artesiana.
3. **Balance:** $\sum Q_{recarga} = \sum Q_{descarga}$, porque el dominio está
   cerrado salvo por el nivel freático.
4. Las líneas de flujo profundas son largas y lentas (sistema regional); las
   someras, cortas y rápidas (sistema local).

**Solución, parte 2 — Anisótropo.**

![**Figura 11.** Comparación isótropo / anisótropo en la misma sección. Con $K_h = 5K_v$ el flujo se aplana, los sistemas se vuelven más someros y más extensos lateralmente.](fig/fig_4_10_anisotropo.png){width=15.8cm}

**Paso 1 — Transformar.**

$$x' = x\sqrt{\frac{K_v}{K_h}} = x\sqrt{\frac{1}{5}} = 0.447\,x$$

La sección se contrae horizontalmente al 44.7 %.

**Verifica que funciona:** la ecuación anisótropa
$K_h\partial^2h/\partial x^2 + K_v\partial^2h/\partial z^2 = 0$ se convierte, con
ese cambio de variable, en $\partial^2h/\partial x'^2 + \partial^2h/\partial z^2 = 0$,
que **es** Laplace. Hacer esta verificación demuestra que entiendes de dónde sale
el factor.

**Paso 2 — Dibujar** con celdas cuadradas en la sección transformada (ahí el
medio es isótropo).

**Paso 3 — Destransformar** multiplicando por $\sqrt{K_h/K_v} = 2.236$. Las celdas
quedan rectángulos de relación **2.24 : 1**.

![**Figura 12.** El método de la sección transformada.](fig/fig_4_10_transformada.png){width=15.8cm}

**Paso 4 — Caudal** con la media geométrica:

$$K_{eq} = \sqrt{K_hK_v} = \sqrt{5}\,K_v = 2.24\,K_v = 0.447\,K_h$$

**Qué cambia físicamente:** las líneas de flujo se **aplanan** (el agua prefiere
viajar horizontalmente), los sistemas son **más someros y más extensos**, aumenta
la proporción de flujo local frente al regional, y —la pregunta trampa— **en la
sección real las líneas de flujo ya no cortan a las equipotenciales a 90°**. Sólo
lo hacen en la transformada.

## 5.4 Ejercicios para desarrollar

**P5.1** En una red de flujo bajo una pantalla impermeable se cuentan 4 canales de
flujo y 12 saltos de potencial. La carga disponible es 15 m, la conductividad
$2\times10^{-4}$ m/s y el ancho de la estructura 80 m.

a. Calcula el caudal de filtración por metro de ancho.
b. Calcula el caudal total en m³/s y en m³/día.
c. Si el recorrido medio de filtración es de 60 m, ¿cuál es el gradiente medio?
d. ¿Qué pasaría con $Q$ si se duplicara la longitud de la pantalla? Justifica en
   términos de $n_f$ y $n_d$ sin hacer cálculos.

**P5.2** Un medio estratificado tiene $K_h = 4\times10^{-4}$ m/s y
$K_v = 1\times10^{-5}$ m/s.

a. Calcula la conductividad equivalente para el cálculo del caudal.
b. Calcula el factor de escala horizontal de la sección transformada.
c. ¿Cuál será la relación de lados de las celdas al destransformar?
d. ¿Cortan las líneas de flujo a las equipotenciales a 90° en la sección real?
   Explica.

*Respuestas en el Anexo C.*

# PARTE 6 — Esfuerzo efectivo y excavaciones

## 6.1 Teoría

### El principio de Terzaghi

$$\boxed{\sigma' = \sigma_T - u}$$

| Cantidad | Fórmula | Depende de la excavación? |
|---|---|---|
| **Esfuerzo total** $\sigma_T$ | $\sum \gamma_i z_i$ (peso de todo lo que está encima) | **Sí**: si quitas material, baja |
| **Presión neutra** $u$ | $\gamma_w h_p$ | **No**: la fija el acuífero |
| **Esfuerzo efectivo** $\sigma'$ | $\sigma_T - u$ | sí, por diferencia |

**La idea central de todo el tema:** el acuífero artesiano está conectado a una
zona de recarga lejana, así que **excavar no cambia su presión**. Pero sí reduce
el peso que la contiene. Esa asimetría es el peligro.

$$FS = \frac{\sigma_T}{u}$$

| $FS$ | Estado |
|---|---|
| $>1.5$ | Seguro |
| 1.0–1.3 | Marginal: exige instrumentación |
| $=1.0$ | **Crítico**: $\sigma'=0$, condición de arena movediza |
| $<1.0$ | **Falla**: reventón del fondo |

### Profundidad crítica

Imponiendo $\sigma_T = u$ y despejando la profundidad $d$:

$$\boxed{d_{crit} = \frac{\gamma_{sat}D - \gamma_w h_p}{\gamma_{sat}-\gamma_w}}
\qquad\text{(excavación llena de agua)}$$

$$\boxed{d_{crit} = D - \frac{\gamma_w h_p}{\gamma_{sat}}}
\qquad\text{(excavación en seco)}$$

La primera forma es elegante: es el **esfuerzo efectivo inicial dividido por el
peso sumergido** del suelo. Dice "tengo tanto margen y cada metro que excavo me
cuesta tanto".

### Cómo calcular $h_p$ (donde más se falla)

$h_p$ es la **altura total de la columna de agua por encima del punto**. Si el
piezómetro está a 50 ft de profundidad y el agua sube 20 ft **sobre** el terreno:

$$h_p = 50 + 20 = 70\ \mathrm{ft}$$

Poner 20 ignora el espesor; poner 50 ignora el artesianismo. **Hay que sumar.**

## 6.2 Ejemplo resuelto 6.1 — El problema completo de la zanja

**Enunciado.** Una capa de arcilla que va de la superficie a 50 ft de profundidad
está sobre una arena artesiana. Un piezómetro perforado hasta el techo del
acuífero registra una carga de 20 ft **sobre** la superficie del terreno. El peso
unitario saturado de la arcilla es 125 lb/ft³. El nivel freático está en la
superficie.

a. ¿Cuáles son los esfuerzos total, neutro y efectivo en la base de la arcilla?
b. Si se excava una zanja de 20 ft, llena de agua hasta la superficie, ¿cuáles
   son esos tres valores bajo la zanja?
c. ¿Se puede mantener la estabilidad si se deseca la zanja?
d. ¿Cuál es la profundidad mínima de zanja que causa falla, suponiéndola llena
   de agua?

*(Es el ejercicio 4 del capítulo 4 del taller, y uno de los dos más completos de
todo el taller.)*

![**Figura 13.** Los tres estados de esfuerzo de los incisos (a), (b) y (c), y la curva que define la profundidad crítica del inciso (d).](fig/fig_4_04_esfuerzos.png){width=15.8cm}

**Datos:** $D = 50$ ft, $\gamma_{sat} = 125$ lb/ft³, $\gamma_w = 62.4$ lb/ft³,
carga artesiana $= +20$ ft.

**Paso 0 — La carga de presión en la base de la arcilla.**

$$h_p = 50 + 20 = 70\ \mathrm{ft}$$

Este valor **no cambia en ningún inciso**. Escríbelo aparte y subráyalo.

### Inciso (a) — Condición original

$$\sigma_T = \gamma_{sat}\,D = (125)(50) = \boxed{6250\ \mathrm{lb/ft^2}}$$

$$u = \gamma_w\,h_p = (62.4)(70) = \boxed{4368\ \mathrm{lb/ft^2}}$$

$$\sigma' = 6250 - 4368 = \boxed{1882\ \mathrm{lb/ft^2}}$$

$$FS = \frac{6250}{4368} = 1.43$$

### Inciso (b) — Zanja de 20 ft llena de agua

**Lo que cambia:** sólo $\sigma_T$. Encima del punto quedan ahora 30 ft de arcilla
**más** 20 ft de agua:

$$\sigma_T = (125)(50-20) + (62.4)(20) = 3750 + 1248 = \boxed{4998\ \mathrm{lb/ft^2}}$$

**Lo que NO cambia:** $u = 4368$ lb/ft².

$$\sigma' = 4998 - 4368 = \boxed{630\ \mathrm{lb/ft^2}}
\qquad FS = \frac{4998}{4368} = 1.14$$

**El resultado interesante:** $\sigma'$ se desploma de 1882 a 630 lb/ft² (una
pérdida del 66 %) por excavar sólo el 40 % del espesor. La razón: el agua que
rellena la zanja pesa la mitad que la arcilla que reemplazó, así que cada pie
excavado cuesta $125 - 62.4 = 62.6$ lb/ft² de esfuerzo efectivo.

### Inciso (c) — ¿Se puede desecar?

Al retirar los 20 ft de agua se pierde la contrapresión de 1248 lb/ft²:

$$\sigma_T = (125)(30) = 3750\ \mathrm{lb/ft^2} < u = 4368\ \mathrm{lb/ft^2}$$

$$\sigma' = 3750 - 4368 = \boxed{-618\ \mathrm{lb/ft^2}}
\qquad FS = 0.86 < 1$$

$$\boxed{\textbf{NO.}\ \text{El fondo falla.}}$$

**Y hay que explicar por qué:** un esfuerzo efectivo negativo no tiene sentido
físico, lo cual indica que **antes de alcanzar ese estado el suelo falla**. La
presión artesiana levanta el tapón de arcilla: se produce un **reventón de fondo**
(*blowout*), el agua irrumpe arrastrando arena y la excavación se inunda.

**Soluciones de ingeniería (inclúyelas, es lo que pide un parcial de este nivel):**

1. **Despresurizar el acuífero** con pozos de alivio antes de desecar. La carga
   máxima admisible para $FS = 1$ es $h_p = \sigma_T/\gamma_w = 3750/62.4 = 60.1$
   ft, de modo que hay que bajar la carga **al menos 10 ft** (y más, para
   $FS \ge 1.3$).
2. **Mantener la zanja inundada** y excavar con draga (es el inciso b).
3. Dejar un **tapón de arcilla más grueso** o lastrarlo.

### Inciso (d) — Profundidad crítica

Sea $d$ la profundidad excavada. Quedan $(50-d)$ ft de arcilla más $d$ ft de agua.
Condición de falla $\sigma_T = u$:

$$\gamma_{sat}(50-d) + \gamma_w d = \gamma_w(70)$$

$$125(50) - 125d + 62.4d = 4368$$

$$6250 - 62.6\,d = 4368
\qquad\Longrightarrow\qquad
d = \frac{1882}{62.6} = \boxed{30.1\ \mathrm{ft}}$$

**Verificación:** con $d = 30.1$ ft,
$\sigma_T = 125(19.9) + 62.4(30.1) = 2487 + 1878 = 4365 \approx 4368$ ✓

**Comparación que es el aprendizaje del ejercicio.** Si la zanja **no** se
rellenara de agua, el término $\gamma_w d$ desaparece y

$$d_{crit} = 50 - \frac{(62.4)(70)}{125} = 50 - 34.9 = 15.1\ \mathrm{ft}$$

**Rellenar la excavación con agua duplica la profundidad alcanzable.** Eso es lo
que un ingeniero se lleva de este problema.

### Por qué este tema está en un libro de hidrogeología

La conexión que el autor quiere que hagas: **las zonas de descarga de agua
subterránea son terreno peligroso para excavar**, porque allí la carga aumenta con
la profundidad (condición artesiana). En zonas de **recarga** ocurre lo contrario
y el problema no existe. Identificar si estás en recarga o descarga —comparando
piezómetros someros y profundos, como en la Parte 5— es el **primer** paso de
cualquier investigación geotécnica en terreno saturado.

## 6.3 Ejercicios para desarrollar

**P6.1** Una capa de arcilla de 40 ft de espesor, con $\gamma_{sat} = 120$ lb/ft³,
está sobre un acuífero artesiano cuya carga sube 15 ft sobre la superficie del
terreno. $\gamma_w = 62.4$ lb/ft³.

a. Calcula $h_p$, $\sigma_T$, $u$, $\sigma'$ y $FS$ en la base de la arcilla.
b. Calcula la profundidad crítica si la excavación se mantiene llena de agua.
c. Calcula la profundidad crítica si se excava en seco.
d. ¿Hasta qué carga habría que despresurizar el acuífero para excavar en seco
   hasta 20 ft con $FS = 1.3$?

**P6.2** Versión métrica. Un estrato confinante de 12 m de espesor tiene
$\gamma_{sat} = 19.5$ kN/m³ y descansa sobre un acuífero cuya carga asciende 5 m
sobre el terreno. Toma $\gamma_w = 9.81$ kN/m³.

a. Calcula $\sigma_T$, $u$ y $\sigma'$ en la base del estrato, en kPa.
b. Calcula el factor de seguridad.
c. Calcula la profundidad crítica con la excavación llena de agua y en seco.
d. Compara los dos resultados y comenta qué implica para la obra.

*Respuestas en el Anexo C.*

# PARTE 7 — Pruebas de bombeo y transmisividad

Este es el bloque más grande del parcial. Lee la Parte 1 antes si no la has leído.

## 7.1 Teoría

### La geometría del problema

![**Figura 14.** Geometría de una prueba de bombeo en acuífero confinado. El pozo extrae $Q$ constante, el cono de abatimiento crece con el tiempo y un piezómetro a distancia $r$ registra el abatimiento $s$.](fig/fig_b1_esquema.png){width=15.8cm}

| Símbolo | Nombre | Unidades |
|---|---|---|
| $Q$ | caudal de bombeo (constante) | m³/día |
| $s$ | abatimiento $= h_0 - h$ (descenso) | m |
| $T = Kb$ | transmisividad | m²/día |
| $S$ | coeficiente de almacenamiento | adimensional |
| $r$ | distancia del pozo al piezómetro | m |

### La ecuación de flujo radial

$$\frac{\partial^{2}s}{\partial r^{2}} + \frac{1}{r}\frac{\partial s}{\partial r}
= \frac{S}{T}\,\frac{\partial s}{\partial t}$$

Theis (1935) la resolvió para un pozo puntual bombeando $Q$ constante en un
acuífero infinito. **Todo lo demás de esta parte son casos particulares o
aproximaciones de esa solución.**

### Las hipótesis de Theis (pregunta de teoría casi segura)

1. Acuífero **confinado**, homogéneo, isótropo, de espesor uniforme.
2. Extensión **infinita** en planta (sin fronteras).
3. Superficie piezométrica inicial **horizontal**.
4. Caudal $Q$ **constante**.
5. El pozo **penetra todo el espesor**.
6. Diámetro del pozo **despreciable** (sin almacenamiento en el pozo).
7. El agua se libera **instantáneamente** al bajar la carga.
8. Flujo **radial horizontal**, laminar (válido Darcy).

Cuando el enunciado menciona "acuífero libre", "semiconfinado", un río o una
falla, está avisando que alguna de estas hipótesis se rompe.

### Qué método usar

![**Figura 15.** Árbol de decisión. La pregunta que lo define todo es qué variable acompaña al abatimiento en la tabla de datos.](fig/fig_b0_arbol.png){width=15.8cm}

| Si en el enunciado ves… | Usa |
|---|---|
| tabla de $t$ y $s$ en **un** piezómetro | Cooper-Jacob (o Theis si $u > 0.01$) |
| $s$ en **varios** piezómetros al **mismo** tiempo | distancia–abatimiento |
| "el abatimiento se estabilizó" + dos piezómetros | Thiem (confinado) o Dupuit (libre) |
| mediciones **después de apagar** la bomba | recuperación de Theis |
| $T$ y $S$ ya dados, piden $s$ | Theis o Cooper-Jacob directo |

### Método de Theis

$$\boxed{s = \frac{Q}{4\pi T}\,W(u)}
\qquad\qquad
\boxed{u = \frac{r^{2}S}{4Tt}}$$

$W(u)$ es la **función de pozo** (integral exponencial):

$$W(u) = -0.5772 - \ln u + u - \frac{u^{2}}{2\cdot2!} + \frac{u^{3}}{3\cdot3!} - \cdots$$

Tabla completa en el Anexo A. **Atajo:** para $u < 0.01$,
$W(u) \approx -0.5772 - \ln u$, con error menor al 1 %.

Procedimiento de curva patrón (ver figura 4 de la Parte 1): superponer los dos
gráficos log-log manteniendo los ejes paralelos, elegir un punto de coincidencia
y leer sus cuatro coordenadas. Entonces

$$T = \frac{Q\,W(u)}{4\pi\,s}
\qquad\qquad
S = \frac{4\,T\,t\,u}{r^{2}}$$

### Método de Cooper-Jacob (el importante)

Para $u$ pequeño la serie se corta en dos términos y, pasando a logaritmo
decimal:

$$s = \frac{2.303\,Q}{4\pi T}\,\log\!\left(\frac{2.25\,Tt}{r^{2}S}\right)$$

Eso es una **recta** contra $\log t$. De la pendiente y del corte:

$$\boxed{T = \frac{2.303\,Q}{4\pi\,\Delta s}}
\qquad\qquad
\boxed{S = \frac{2.25\,T\,t_0}{r^{2}}}$$

**Deducción de las dos (hazla en el examen, son dos líneas).** Por cada ciclo
logarítmico, $\log t$ aumenta 1, así que la caída de abatimiento es
$\Delta s = 2.303Q/4\pi T$: despejas $T$. Y en el corte $s = 0$ el logaritmo vale
cero, o sea su argumento vale 1: $2.25Tt_0/r^2S = 1$, y despejas $S$.

**Condición de validez:**

$$u = \frac{r^{2}S}{4Tt} < 0.01
\qquad\Longleftrightarrow\qquad
t > \frac{r^{2}S}{0.04\,T}$$

| $u$ | Error de Cooper-Jacob |
|---|---|
| 0.01 | 0.2 % |
| 0.03 | 1 % |
| 0.05 | 2 % |
| 0.1 | 5 % |

En la práctica se acepta hasta $u \approx 0.05$, pero **declara el criterio que
usaste**. Leído al revés, la condición explica por qué los primeros puntos de la
tabla siempre se curvan por debajo de la recta: no es error de medición, es que
la aproximación todavía no vale.

### Distancia–abatimiento

$$\boxed{T = \frac{2.303\,Q}{2\pi\,\Delta s_r}}
\qquad\qquad
\boxed{S = \frac{2.25\,T\,t}{r_0^{2}}}$$

**De dónde sale el $2\pi$:** en la fórmula, $r^2$ está en el denominador y al
cuadrado, así que $\log(r^{-2}) = -2\log r$. Al derivar respecto de $\log r$ sale
un 2 que se cancela con el $4\pi$ y deja $2\pi$. **Es el error de signo-factor más
común del tema.**

### Recuperación de Theis

Se apaga la bomba y se mide cómo sube el nivel. Definiciones (hay que tenerlas
claras o el método falla):

- $t$ = tiempo desde que **arrancó** la bomba.
- $t'$ = tiempo desde que **paró**.
- $s'$ = **abatimiento residual**: lo que falta para recuperar el nivel inicial.

Por superposición (bomba real $+Q$ más bomba imaginaria $-Q$ desde el apagado):

$$\boxed{s' = \frac{2.303\,Q}{4\pi T}\log\frac{t}{t'}}
\qquad\Longrightarrow\qquad
\boxed{T = \frac{2.303\,Q}{4\pi\,\Delta s'}}$$

> **La recuperación da $T$ pero NO da $S$**, porque la recta pasa
> obligatoriamente por el origen ($s'=0$ cuando $t/t'=1$) y no hay intercepto del
> cual extraer $S$. Es una pregunta frecuente.

### Régimen permanente

Si el abatimiento **se estabilizó**, el tiempo desaparece y ya no se puede
obtener $S$ (no hay cambio de almacenamiento).

**Confinado (Thiem):** $\boxed{T = \dfrac{Q\ln(r_2/r_1)}{2\pi(s_1-s_2)}}$

**Libre (Dupuit):** $\boxed{K = \dfrac{Q\ln(r_2/r_1)}{\pi(h_2^{2}-h_1^{2})}}$

![**Figura 16.** En acuífero confinado se trabaja con los abatimientos; en acuífero libre, con los cuadrados de los espesores saturados medidos desde la base.](fig/fig_b9_thiem.png){width=15.8cm}

> **La trampa del acuífero libre:** usar $s$ en vez de $h^2$. Y $h$ se mide
> **desde la base del acuífero**, no desde el nivel inicial. Si el enunciado da
> abatimientos, convierte: $h = H - s$.

## 7.2 Ejemplo resuelto 7.1 — Cooper-Jacob completo

**Este es el ejemplo más importante de toda la guía.** Si sólo haces uno, haz
este, y hazlo con lápiz y papel.

**Enunciado.** Prueba de bombeo en un acuífero confinado de 25 m de espesor.
$Q = 1500$ m³/día constante. Piezómetro de observación a $r = 50$ m. Se midió:

| $t$ (min) | $s$ (m) | $t$ (min) | $s$ (m) | $t$ (min) | $s$ (m) |
|---|---|---|---|---|---|
| 1 | 0.005 | 30 | 0.725 | 360 | 1.679 |
| 2 | 0.040 | 40 | 0.830 | 480 | 1.792 |
| 3 | 0.087 | 60 | 0.982 | 720 | 1.953 |
| 5 | 0.181 | 90 | 1.137 | 1080 | 2.113 |
| 7 | 0.261 | 120 | 1.248 | 1440 | 2.228 |
| 10 | 0.360 | 180 | 1.406 |  |  |
| 15 | 0.486 | 240 | 1.519 |  |  |
| 20 | 0.583 |  |  |  |  |

Determinar $T$, $S$, $K$ y $S_s$.

![**Figura 17.** El ajuste de Cooper-Jacob. Los puntos huecos de tiempo corto no se usan: ahí $u > 0.01$. La recta se traza sólo con los puntos llenos.](fig/fig_b2_cooper_jacob.png){width=15.8cm}

### Paso 1 — Preparar los datos

Convierte los tiempos a días dividiendo por 1440. **Hazlo antes de nada.**
$t = 1440$ min $= 1$ día; $t = 360$ min $= 0.25$ día; etc.

### Paso 2 — Graficar

Dibuja el papel semilog de 4 ciclos (Parte 1.3), con $t$ en minutos en el eje
horizontal y $s$ en el vertical. Marca los 20 puntos.

### Paso 3 — Trazar la recta

Por los puntos de **tiempo tardío**. Observa que desde $t \approx 360$ min los
puntos se alinean perfectamente, mientras que los primeros se curvan por debajo.
Traza la recta por los últimos cinco y **prolóngala hacia la izquierda** hasta
cortar $s = 0$.

### Paso 4 — Medir $\Delta s$

Entre $t = 100$ min y $t = 1000$ min (un ciclo logarítmico exacto) la recta sube
de 1.17 m a 2.08 m:

$$\Delta s = 2.08 - 1.17 = 0.91\ \mathrm{m\ por\ ciclo}$$

### Paso 5 — Leer $t_0$

La recta extrapolada corta $s = 0$ en

$$t_0 = 5.2\ \mathrm{min} = \frac{5.2}{1440} = 3.61\times10^{-3}\ \mathrm{días}$$

### Paso 6 — Transmisividad

$$T = \frac{2.303\,Q}{4\pi\,\Delta s}
= \frac{2.303\,(1500\ \mathrm{m^3/día})}{4\pi\,(0.91\ \mathrm{m})}
= \frac{3454.5}{11.44}$$

$$\boxed{T = 301\ \mathrm{m^2/día}}$$

### Paso 7 — Almacenamiento

$$S = \frac{2.25\,T\,t_0}{r^{2}}
= \frac{2.25\,(301)\,(3.61\times10^{-3})}{(50)^{2}}
= \frac{2.445}{2500}$$

$$\boxed{S = 9.8\times10^{-4}}$$

### Paso 8 — Verificar la validez

Con el último punto ($t = 1$ día):

$$u = \frac{r^{2}S}{4Tt} = \frac{(50)^{2}(9.8\times10^{-4})}{4(301)(1)}
= \frac{2.45}{1204} = 2.0\times10^{-3} < 0.01\ \checkmark$$

Y con el primer punto de la recta ($t = 0.25$ d): $u = 8.1\times10^{-3} < 0.01$ ✓.
Los puntos anteriores tenían $u > 0.01$ y por eso quedaron fuera. **Esto cierra
el razonamiento: la zona que descartaste a ojo es exactamente la que el criterio
descarta.**

### Paso 9 — Parámetros derivados

$$K = \frac{T}{b} = \frac{301}{25} = 12.0\ \mathrm{m/día}
= 1.4\times10^{-4}\ \mathrm{m/s}$$

$$S_s = \frac{S}{b} = \frac{9.8\times10^{-4}}{25}
= 3.9\times10^{-5}\ \mathrm{m^{-1}}$$

### Paso 10 — ¿Tiene sentido?

$K = 1.4\times10^{-4}$ m/s corresponde a **arena limpia a arena gruesa**, y
$S \approx 10^{-3}$ es el rango típico de un acuífero confinado ($10^{-5}$ a
$10^{-3}$). Coherente. **Haz siempre este paso y escríbelo:** si te saliera
$S = 0.2$ en un confinado, o $K$ de grava en una arcilla, hay un error de
unidades.

### Receta de bolsillo

1. Tiempos a días (÷1440).
2. Graficar $s$ contra $\log t$.
3. Recta por los puntos tardíos.
4. Medir $\Delta s$ sobre **un ciclo completo**.
5. Extrapolar hasta $s=0$: leer $t_0$.
6. $T = 2.303Q/(4\pi\Delta s)$.
7. $S = 2.25Tt_0/r^2$.
8. Comprobar $u<0.01$ y la plausibilidad.

## 7.3 Ejemplo resuelto 7.2 — Distancia–abatimiento

**Enunciado.** Mismo acuífero, $Q = 1500$ m³/día. A $t = 1$ día se leen cuatro
piezómetros:

| $r$ (m) | 10 | 30 | 50 | 100 | 200 | 300 |
|---|---|---|---|---|---|---|
| $s$ (m) | 3.508 | 2.634 | 2.228 | 1.679 | 1.137 | 0.830 |

Determinar $T$ y $S$.

![**Figura 18.** Distancia–abatimiento a $t = 1$ día. Ojo con el denominador: aquí es $2\pi$, no $4\pi$.](fig/fig_b4_distancia.png){width=15.8cm}

**Paso 1 — Verificar validez.** $u = r^2S/4Tt$ crece con $r$, de modo que los
piezómetros **lejanos** son los que fallan. Con $T\approx300$, $S\approx10^{-3}$,
$t=1$ d: $u(100) = 8.3\times10^{-3}$ ✓, pero
$u(200) = 3.3\times10^{-2}$ ✗ y $u(300) = 7.5\times10^{-2}$ ✗.
**Usa sólo $r \le 100$ m.**

**Paso 2 — Graficar $s$ contra $\log r$** y trazar la recta por esos cuatro puntos.

**Paso 3 — Medir la pendiente por ciclo de distancia.** Entre $r = 20$ y
$r = 200$ m: $\Delta s_r = 1.83$ m por ciclo.

**Paso 4 — Leer $r_0$.** La recta corta $s = 0$ en $r_0 = 826$ m.

**Paso 5 — Calcular.**

$$T = \frac{2.303\,Q}{2\pi\,\Delta s_r} = \frac{2.303(1500)}{2\pi(1.83)}
= \frac{3454.5}{11.50} = \boxed{300\ \mathrm{m^2/día}}$$

$$S = \frac{2.25\,T\,t}{r_0^{2}} = \frac{2.25(300)(1)}{(826)^{2}}
= \frac{675}{682\,276} = \boxed{9.9\times10^{-4}}$$

**Paso 6 — Comparar.** Idéntico al resultado de Cooper-Jacob, como debe ser: es
el mismo acuífero medido de otra forma. **Que dos métodos independientes
coincidan es la mejor verificación posible.**

## 7.4 Ejemplo resuelto 7.3 — Recuperación

**Enunciado.** Se bombeó $Q = 1500$ m³/día durante 1440 min y se midió la
recuperación en el propio pozo:

| $t'$ (min) | 5 | 10 | 20 | 30 | 60 | 120 | 240 | 480 |
|---|---|---|---|---|---|---|---|---|
| $s'$ (m) | 2.255 | 1.980 | 1.707 | 1.549 | 1.281 | 1.021 | 0.774 | 0.552 |

Determinar $T$.

![**Figura 19.** Recuperación. Se grafica $s'$ contra $\log(t/t')$ y la recta pasa por el origen.](fig/fig_b5_recuperacion.png){width=15.8cm}

**Paso 1 — Calcular $t/t'$ para cada punto.** $t = t_p + t' = 1440 + t'$:

| $t'$ (min) | 5 | 10 | 20 | 30 | 60 | 120 | 240 | 480 |
|---|---|---|---|---|---|---|---|---|
| $t$ (min) | 1445 | 1450 | 1460 | 1470 | 1500 | 1560 | 1680 | 1920 |
| $t/t'$ | 289 | 145 | 73 | 49 | 25 | 13 | 7 | 4 |

**Paso 2 — Graficar $s'$ contra $\log(t/t')$.** Sale una recta que pasa por el
origen.

**Paso 3 — Medir $\Delta s'$ por ciclo.** Entre $t/t' = 10$ y $t/t' = 100$:
$\Delta s' = 0.92$ m.

**Paso 4 — Calcular.**

$$T = \frac{2.303\,Q}{4\pi\,\Delta s'} = \frac{2.303(1500)}{4\pi(0.92)}
= \boxed{300\ \mathrm{m^2/día}}$$

**Paso 5 — Lo que hay que decir.** Este método da $T$ y **no da $S$**. Además es
el más preciso en la práctica, porque durante la recuperación no hay que mantener
el caudal constante: la bomba está apagada y no puede fluctuar.

## 7.5 Ejemplo resuelto 7.4 — Régimen permanente

**Enunciado (confinado).** $Q = 1500$ m³/día. El abatimiento se estabilizó en
2.80 m a 20 m del pozo y en 1.00 m a 200 m. El acuífero tiene 25 m de espesor.
Hallar $T$ y $K$.

**Solución.**

$$T = \frac{Q\ln(r_2/r_1)}{2\pi(s_1-s_2)}
= \frac{1500\,\ln(200/20)}{2\pi\,(2.80-1.00)}
= \frac{1500\,(2.3026)}{11.31}$$

$$\boxed{T = 305\ \mathrm{m^2/día}}
\qquad
K = \frac{305}{25} = \boxed{12.2\ \mathrm{m/día}}$$

Coincide con los otros tres métodos ✓

**Enunciado (libre).** $Q = 1500$ m³/día en un acuífero libre de 30 m de espesor
inicial. El espesor saturado estabilizado es 27.0 m a 20 m del pozo y 29.2 m a
200 m. Hallar $K$.

**Solución.** Aquí van los **cuadrados**:

$$K = \frac{Q\ln(r_2/r_1)}{\pi(h_2^{2}-h_1^{2})}
= \frac{1500(2.3026)}{\pi\,(29.2^{2}-27.0^{2})}
= \frac{3454}{\pi\,(852.6-729.0)}
= \frac{3454}{388.3}$$

$$\boxed{K = 8.9\ \mathrm{m/día}}$$

**Nota el contraste:** en el confinado el denominador es $2\pi(s_1-s_2)$; en el
libre es $\pi(h_2^2-h_1^2)$. Cambia el factor **y** la variable.

## 7.6 Ejercicios para desarrollar

**P7.1 (el completo).** Prueba de bombeo en un acuífero confinado de 40 m de
espesor. $Q = 2500$ m³/día. Piezómetro a $r = 80$ m. Datos:

| $t$ (min) | $s$ (m) | $t$ (min) | $s$ (m) |
|---|---|---|---|
| 1 | 0.069 | 90 | 1.014 |
| 2 | 0.162 | 120 | 1.085 |
| 3 | 0.233 | 180 | 1.185 |
| 5 | 0.334 | 300 | 1.312 |
| 8 | 0.436 | 480 | 1.429 |
| 12 | 0.528 | 720 | 1.529 |
| 20 | 0.648 | 1080 | 1.630 |
| 30 | 0.746 | 1440 | 1.701 |
| 45 | 0.844 |  |  |
| 60 | 0.915 |  |  |

a. Grafica en papel semilogarítmico y traza la recta.
b. Determina $\Delta s$ y $t_0$.
c. Calcula $T$ y $S$.
d. Verifica la condición $u < 0.01$ e indica desde qué tiempo se cumple.
e. Calcula $K$ en m/día y m/s, y nombra el material probable.

**P7.2** En el mismo acuífero del P7.1 se leen tres piezómetros a $t = 2$ días,
con $Q = 1800$ m³/día:

| $r$ (m) | 25 | 75 | 150 | 250 |
|---|---|---|---|---|
| $s$ (m) | 2.643 | 1.944 | 1.504 | 1.182 |

a. Verifica qué puntos cumplen $u < 0.01$ (usa $T \approx 450$, $S \approx 8\times10^{-4}$ como primera estimación).
b. Determina $\Delta s_r$ y $r_0$.
c. Calcula $T$ y $S$. **Cuidado con el factor del denominador.**

**P7.3** Thiem. $Q = 2200$ m³/día en un acuífero confinado de 30 m de espesor. El
abatimiento estabilizado es 3.40 m a 15 m del pozo y 1.15 m a 150 m.

a. Calcula $T$ y $K$.
b. ¿Por qué no se puede calcular $S$ con estos datos?

*Respuestas en el Anexo C.*

# PARTE 8 — Cálculos en el acuífero

Ya tienes $T$ y $S$. Esta es la segunda mitad del problema y la parte que casi
nadie estudia. Todos los ejemplos usan $T = 300$ m²/día, $S = 10^{-3}$,
$b = 25$ m, $Q = 1500$ m³/día.

## 8.1 Teoría: las cinco herramientas

### 1. Predecir el abatimiento en cualquier punto y tiempo

$$s = \frac{Q}{4\pi T}W(u),\qquad u = \frac{r^{2}S}{4Tt}$$

o, si $u < 0.01$, la versión logarítmica de Cooper-Jacob. **Es la misma fórmula
de la Parte 7, usada al revés:** antes conocías $s$ y buscabas $T$; ahora conoces
$T$ y buscas $s$.

### 2. Superposición

La ecuación de flujo es **lineal**, así que los abatimientos se suman:

$$\boxed{s_{total}(x,y,t) = \sum_{i=1}^{n}\frac{Q_i}{4\pi T}\,W(u_i),
\qquad u_i = \frac{r_i^{2}S}{4Tt}}$$

Y como $s$ es proporcional a $Q$, **duplicar el caudal duplica el abatimiento en
todos los puntos**. Esta linealidad es la propiedad más útil de toda la teoría.

### 3. Radio de influencia

$$\boxed{R_0 = \sqrt{\frac{2.25\,T\,t}{S}} = 1.5\sqrt{\frac{T\,t}{S}}}$$

Es el radio donde la **recta** de Cooper-Jacob da $s = 0$. No es una frontera
física: en rigor el cono es infinito, sólo que inmedible más allá de $R_0$. Crece
con $\sqrt{t}$, así que **cuadruplicar el tiempo sólo duplica el radio**.

### 4. Capacidad específica

$$\text{Capacidad específica} = \frac{Q}{s_w}$$

Se calcula con la misma fórmula de Theis poniendo $r = r_w$ (radio del pozo,
0.1–0.3 m). **No es constante**: disminuye con el tiempo porque $s_w$ crece.
Siempre di a qué tiempo corresponde.

### 5. Fronteras: pozos imagen

Theis supone acuífero infinito. Si hay una frontera, se simula con un pozo
**imagen** reflejado al otro lado, a la misma distancia:

| Frontera | Pozo imagen | Efecto |
|---|---|---|
| **Impermeable** (falla, barrera) | bombea $+Q$ | el abatimiento **aumenta** |
| **Carga constante** (río, lago) | inyecta $-Q$ | el abatimiento **disminuye** |

## 8.2 Ejemplo resuelto 8.1 — Abatimiento y capacidad específica

**Enunciado.** (a) ¿Cuánto baja el nivel a 200 m del pozo después de 30 días?
(b) ¿Cuánto baja en el pozo mismo ($r_w = 0.15$ m) y cuál es la capacidad
específica?

**Solución (a).**

**Paso 1 — Calcular $u$.**

$$u = \frac{r^{2}S}{4Tt} = \frac{(200)^{2}(10^{-3})}{4(300)(30)}
= \frac{40}{36\,000} = 1.11\times10^{-3}$$

**Paso 2 — Buscar $W(u)$.** De la tabla del Anexo A, interpolando entre
$W(10^{-3}) = 6.332$ y $W(2\times10^{-3}) = 5.639$:

$$W(1.11\times10^{-3}) = 6.23$$

O con el atajo: $W \approx -0.5772 - \ln(1.11\times10^{-3}) = -0.5772 + 6.803 = 6.23$ ✓

**Paso 3 — Abatimiento.**

$$s = \frac{Q}{4\pi T}W(u) = \frac{1500}{4\pi(300)}(6.23)
= (0.3979)(6.23) = \boxed{2.48\ \mathrm{m}}$$

**Paso 4 — Verificar con Cooper-Jacob** (válido porque $u < 0.01$):

$$s = \frac{2.303(1500)}{4\pi(300)}\log\frac{2.25(300)(30)}{(200)^{2}(10^{-3})}
= 0.9163\,\log(506.3) = 0.9163(2.704) = 2.48\ \mathrm{m}\ \checkmark$$

**Solución (b).**

$$u = \frac{(0.15)^{2}(10^{-3})}{4(300)(30)} = 6.25\times10^{-10}$$

$$W(u) \approx -0.5772 - \ln(6.25\times10^{-10}) = -0.5772 + 21.193 = 20.62$$

$$s_w = (0.3979)(20.62) = \boxed{8.2\ \mathrm{m}}$$

$$\frac{Q}{s_w} = \frac{1500}{8.2}
= \boxed{183\ \mathrm{m^3/día\ por\ metro\ de\ abatimiento}}$$

> **Fíjate en el salto:** a 200 m el abatimiento es 2.5 m; en el pozo, 8.2 m. El
> cono es muy empinado cerca del pozo porque toda el área de paso se estrecha.
> Matemáticamente, $s$ depende de $\ln r$, que crece muy rápido cuando $r\to 0$.

## 8.3 Ejemplo resuelto 8.2 — Interferencia de tres pozos

**Enunciado.** Tres pozos de 1500 m³/día cada uno, en los vértices de un
triángulo. El punto A está a 173.3 m de cada uno. ¿Cuál es el abatimiento en A a
los 30 días?

![**Figura 20.** Tres pozos a los 30 días. Los conos individuales se suman: en el punto A el abatimiento es el triple del que produciría un pozo aislado a la misma distancia.](fig/fig_b7_superposicion.png){width=15.8cm}

**Solución.**

**Paso 1 — Abatimiento de un pozo a 173.3 m.**

$$u = \frac{(173.3)^{2}(10^{-3})}{4(300)(30)} = \frac{30.03}{36\,000}
= 8.34\times10^{-4}$$

$$W(u) \approx -0.5772 - \ln(8.34\times10^{-4}) = 6.51$$

$$s_i = (0.3979)(6.51) = 2.591\ \mathrm{m}$$

**Paso 2 — Sumar.**

| Aporte | $r_i$ (m) | $s_i$ (m) |
|---|---|---|
| pozo 1 | 173.3 | 2.591 |
| pozo 2 | 173.3 | 2.591 |
| pozo 3 | 173.3 | 2.591 |
| **Total en A** | — | **7.774** |

$$\boxed{s_{total} = 7.77\ \mathrm{m}}$$

**Paso 3 — Interpretar.** Un solo pozo produciría 2.59 m; los tres juntos, 7.77 m.
**La interferencia es lo que limita el espaciamiento de un campo de pozos:** cada
pozo le roba carga al vecino, lo que encarece el bombeo y puede dejar pozos sin
abatimiento disponible.

## 8.4 Ejemplo resuelto 8.3 — Radio de influencia, velocidades, caudal máximo

**Enunciado.** Con el mismo acuífero: (a) radio de influencia a varios tiempos;
(b) velocidad real del agua a 200 m a los 30 días, con $n_e = 0.2$; (c) caudal
máximo si sólo hay 8 m de abatimiento disponible en el pozo y hay que bombear 180
días.

![**Figura 21.** El cono crece indefinidamente: en un acuífero confinado ideal nunca se alcanza el régimen permanente. $R_0 \propto \sqrt{t}$.](fig/fig_b6_cono.png){width=15.8cm}

**(a) Radio de influencia.**

$$R_0 = \sqrt{\frac{2.25\,T\,t}{S}}$$

| $t$ | 1 día | 7 días | 30 días | 1 año |
|---|---|---|---|---|
| $R_0$ | 822 m | 2174 m | 4500 m | 15 700 m |

Ejemplo del cálculo a 30 días:
$R_0 = \sqrt{2.25(300)(30)/10^{-3}} = \sqrt{2.025\times10^{7}} = 4500$ m.

**(b) Velocidades.**

$$K = \frac{T}{b} = \frac{300}{25} = 12\ \mathrm{m/día}$$

Gradiente a $r = 200$ m (derivando la solución,
$\partial s/\partial r \approx Q/2\pi Tr$):

$$i = \frac{Q}{2\pi T r} = \frac{1500}{2\pi(300)(200)} = 3.98\times10^{-3}$$

$$q = K\,i = (12)(3.98\times10^{-3}) = 0.0477\ \mathrm{m/día}$$

$$v = \frac{q}{n_e} = \frac{0.0477}{0.2} = \boxed{0.239\ \mathrm{m/día}}$$

**Verificación por continuidad (gratis, hazla siempre):** todo el caudal cruza el
cilindro de radio 200 m y altura 25 m, así que

$$q = \frac{Q}{2\pi r b} = \frac{1500}{2\pi(200)(25)} = 0.0477\ \mathrm{m/día}\ \checkmark$$

**(c) Caudal máximo.** Como $s$ es proporcional a $Q$, calcula el abatimiento por
unidad de caudal y escala. A 180 días con $r_w = 0.15$ m:

$$s_w\ \text{por}\ 1\ \mathrm{m^3/día} = 5.94\times10^{-3}\ \mathrm{m}$$

$$Q_{max} = \frac{8.00}{5.94\times10^{-3}}
= \boxed{1346\ \mathrm{m^3/día} = 15.6\ \mathrm{L/s}}$$

## 8.5 Ejemplo resuelto 8.4 — Fronteras con pozos imagen

**Enunciado.** Un pozo está a 150 m de una frontera. Calcular el abatimiento a los
30 días en un punto situado a 100 m del pozo, entre el pozo y la frontera,
(a) si la frontera es impermeable y (b) si es un río.

![**Figura 22.** Pozos imagen. Una barrera impermeable casi duplica el abatimiento; un río lo reduce drásticamente porque aporta agua.](fig/fig_b8_imagenes.png){width=15.8cm}

**Solución.**

**Paso 1 — Geometría.** Pozo en $x = 0$, frontera en $x = 150$ m. El pozo imagen
va reflejado a la misma distancia al otro lado: $x = 300$ m. El punto de cálculo
está en $x = 100$ m, de modo que

$$r_{real} = 100\ \mathrm{m}
\qquad\qquad
r_{imagen} = 300 - 100 = 200\ \mathrm{m}$$

**Paso 2 — Abatimientos individuales** (Theis a 30 días):

$$s_{real}(100\ \mathrm{m}) = 3.03\ \mathrm{m}
\qquad
s_{imagen}(200\ \mathrm{m}) = 2.48\ \mathrm{m}$$

**Paso 3 — Combinar según el tipo de frontera.**

| Caso | Cálculo | Resultado |
|---|---|---|
| Sin frontera (acuífero infinito) | $3.03$ | 3.03 m |
| **(a) Frontera impermeable** (imagen bombea $+Q$) | $3.03 + 2.48$ | **5.51 m**  (×1.82) |
| **(b) Río** (imagen inyecta $-Q$) | $3.03 - 2.48$ | **0.55 m**  (×0.18) |

**Paso 4 — Interpretar.** La frontera impermeable casi **duplica** el abatimiento:
el agua que no puede venir de ese lado tiene que venir del otro, con más
gradiente. El río hace lo contrario: aporta agua y **reduce el abatimiento al
18 %** del valor sin frontera. Por eso los pozos se ubican cerca de ríos cuando
se busca caudal, y lejos de fallas impermeables.

## 8.6 Ejercicios para desarrollar

**P8.1** Un acuífero tiene $T = 800$ m²/día y $S = 3\times10^{-4}$. Se bombea un
pozo a $Q = 2500$ m³/día.

a. Calcula el abatimiento a 150 m del pozo después de 60 días.
b. Calcula el abatimiento en el pozo ($r_w = 0.2$ m) a los 60 días y la
   capacidad específica.
c. Calcula el radio de influencia a los 60 días.
d. ¿A qué tiempo el radio de influencia sería el doble?

**P8.2** En el mismo acuífero se instalan **dos** pozos separados 400 m, cada uno
bombeando 2000 m³/día.

a. Calcula el abatimiento en el punto medio entre ambos a los 90 días.
b. ¿Cuánto sería si sólo funcionara un pozo?
c. Calcula el radio de influencia a los 90 días y comenta si los dos conos se
   solapan.
d. Si el abatimiento máximo admisible en el punto medio es 3.0 m, ¿cuál es el
   caudal máximo por pozo?

*Respuestas en el Anexo C.*

# PARTE 9 — Costa y flujo regional

Prioridad baja: probablemente sea una pregunta conceptual corta. No le dediques
más de 25 minutos.

## 9.1 Teoría

### Flujo regional en una cuenca

En una cuenca, el nivel freático replica la topografía y genera **celdas de flujo
anidadas**: sistemas locales someros y rápidos (cada montículo con su depresión
adyacente) dentro de un sistema regional profundo y lento. El resultado depende de
la longitud de onda topográfica y de la heterogeneidad: **una capa profunda de
alta $K$ actúa como un conducto regional** que captura el flujo y lo transporta
decenas de kilómetros.

Condiciones de borde típicas de un modelo de cuenca:
$\partial h/\partial x = 0$ en las divisorias laterales, $\partial h/\partial z = 0$
en la base impermeable, y $h = f(x)$ en el nivel freático. Si el medio está
estratificado hay que añadir, en cada interfaz, la **continuidad del potencial**
($\phi_1 = \phi_2$) y del **flujo normal** ($K_1\partial\phi_1/\partial z = K_2\partial\phi_2/\partial z$).
La segunda produce la **refracción** de las líneas de flujo:

$$\frac{\tan\theta_1}{\tan\theta_2} = \frac{K_1}{K_2}$$

Al pasar a un medio más permeable, las líneas de flujo se tumban; al pasar a uno
menos permeable, se verticalizan. Es la ley de Snell del agua subterránea.

### Relación de Ghyben-Herzberg

El agua dulce flota sobre la salada. El equilibrio de presiones da

$$G = \frac{\Delta\rho}{\rho_f} = \frac{1025-1000}{1000} = 0.025
\qquad\Longrightarrow\qquad
\frac{1}{G} = 40$$

**Cada metro de agua dulce sobre el nivel del mar sostiene 40 m de agua dulce por
debajo.** Esa asimetría es la causa de que bombeos modestos produzcan intrusiones
grandes.

### Upconing (ascenso de la interfaz bajo un pozo)

$$z = \frac{Q}{2\pi K d G}
\qquad\text{con el criterio de estabilidad } z \le 0.3\,d$$

$$\boxed{Q_{max} = 0.6\,\pi\,K\,d^{2}\,G}$$

$d$ = distancia del fondo del pozo a la interfaz. **Dependencia cuadrática:**
duplicar $d$ cuadruplica el caudal admisible.

### Cuña salina (solución de Glover)

$$z^{2} = \frac{2q'x}{KG} + \left(\frac{q'}{KG}\right)^{2}$$

El **pie de la cuña** está donde $z = B$ (base del acuífero):

$$\boxed{x_{toe} = \frac{K\,G\,B^{2}}{2\,q'} - \frac{q'}{2\,K\,G}}$$

Cuando $q'$ es pequeño domina el primer término, de modo que
$x_{toe} \propto 1/q'$: **reducir a la mitad la descarga de agua dulce al mar
duplica la penetración de la cuña.**

## 9.2 Ejemplo resuelto 9.1 — Caudal máximo sin upconing

**Enunciado.** Una interfaz de agua salada es estable a unos 40 ft bajo la base de
un pozo, en una formación con $K = 1\times10^{-1}$ cm/s. Calcular el caudal máximo
de bombeo que no provoque upconing.

*(Es el ejercicio 5 del capítulo 5 del taller.)*

![**Figura 23.** Ascenso del cono salino bajo el pozo y dependencia cuadrática de $Q_{max}$ con la distancia $d$.](fig/fig_5_06_upconing.png){width=15.8cm}

**Solución.**

**Paso 1 — Unidades.** $d = 40\ \mathrm{ft} = 12.192$ m;
$K = 0.1\ \mathrm{cm/s} = 1\times10^{-3}$ m/s.

**Paso 2 — Densidad relativa.** $G = 0.025$ (valor estándar para agua de mar; si
el enunciado no da densidades, úsalo y dilo).

**Paso 3 — Aplicar la fórmula.**

$$Q_{max} = 0.6\pi K d^{2} G
= 0.6\pi\,(1\times10^{-3})(12.192)^{2}(0.025)$$

Paso a paso: $0.6\pi = 1.885$; $(12.192)^2 = 148.6$;
$1.885 \times 10^{-3} \times 148.6 \times 0.025$:

$$\boxed{Q_{max} = 7.0\times10^{-3}\ \mathrm{m^3/s} = 7.0\ \mathrm{L/s}
= 605\ \mathrm{m^3/día} = 111\ \mathrm{gpm}}$$

**Paso 4 — Interpretar.** Bombear por encima de ~7 L/s hace que la interfaz
ascienda más de $0.3 \times 12.19 = 3.7$ m, entre en régimen inestable y colapse
hacia el pozo. La salinización resultante es **prácticamente irreversible**,
porque el agua salada que entró no se va al dejar de bombear.

**Regla de diseño que se deriva:** como $Q_{max} \propto d^2$, en acuíferos
costeros conviene perforar **lo más somero posible** y usar **muchos pozos de bajo
caudal** en lugar de pocos de alto caudal.

## 9.3 Ejemplo resuelto 9.2 — Pie de la cuña salina

**Enunciado.** El flujo de agua dulce hacia el mar es $q'$ por pie de costa, en un
acuífero de 100 ft de espesor con $K = 3.3\times10^{-3}$ ft/s. Calcular la
distancia tierra adentro hasta el pie de la cuña, y la nueva posición si el flujo
se reduce a la mitad.

*(Es el ejercicio 6 del capítulo 5 del taller.)*

![**Figura 24.** Posición de la interfaz según Glover para los dos caudales, y la relación $x_{toe}\propto 1/q'$.](fig/fig_5_06_cuna.png){width=15.8cm}

**Solución.**

**Paso 1 — Calcular $KG$.** $KG = (3.3\times10^{-3})(0.025) = 8.25\times10^{-5}$ ft/s.

**Paso 2 — Verificar la plausibilidad del dato.** El enunciado trae
$q' = 2\times10^{-1}$ ft³/s por pie. Comprueba el gradiente que implica:

$$i = \frac{q'}{K B} = \frac{0.2}{(3.3\times10^{-3})(100)} = 0.61\ \mathrm{m/m}$$

Un gradiente de 0.61 es **físicamente inverosímil** en un acuífero costero (los
reales son $10^{-4}$ a $10^{-3}$). Y en efecto, con ese dato
$q'/KG = 2424$ ft, es decir, la interfaz estaría a 2424 ft de profundidad ya en la
línea de costa, **24 veces más que el espesor del acuífero**:

$$x_{toe} = \frac{(8.25\times10^{-5})(10\,000)}{2(0.2)} - \frac{0.2}{2(8.25\times10^{-5})}
= 2.06 - 1212 = -1210\ \mathrm{ft}$$

$$x_{toe} < 0 \;\Longrightarrow\; \textbf{no existe cuña salina}$$

El agua dulce expulsa por completo al agua de mar. **El exponente del enunciado
está mal transcrito.**

**Paso 3 — Resolver con el valor coherente $q' = 2\times10^{-4}$ ft³/s por pie.**

$$\frac{q'}{KG} = \frac{2\times10^{-4}}{8.25\times10^{-5}} = 2.42\ \mathrm{ft}$$

$$x_{toe} = \frac{(8.25\times10^{-5})(10\,000)}{2(2\times10^{-4})} - 1.21
= 2062.5 - 1.2 = \boxed{2061\ \mathrm{ft} = 0.39\ \mathrm{mi}}$$

**Paso 4 — Con la mitad del caudal** ($q' = 1\times10^{-4}$):

$$x_{toe} = \frac{(8.25\times10^{-5})(10\,000)}{2(1\times10^{-4})} - 0.61
= 4125 - 0.6 = \boxed{4124\ \mathrm{ft} = 0.78\ \mathrm{mi}}$$

**Paso 5 — El resultado conceptual.** Como el segundo término es despreciable,

$$x_{toe} \approx \frac{KGB^{2}}{2q'} \;\propto\; \frac{1}{q'}$$

**Reducir a la mitad la descarga duplica la penetración.** Y la dependencia con
$B^2$: duplicar el espesor del acuífero **cuadruplica** la intrusión.

**La moraleja de gestión:** el caudal que se deja fluir al mar no es "agua
desperdiciada", es la **barrera hidráulica** que protege el acuífero. Sobrebombear
hacia el interior reduce $q'$ y desplaza la cuña linealmente en $1/q'$.

> **Cómo presentar esto en el parcial.** Resuelve con el dato que te dan, muestra
> que es imposible, demuéstralo con el gradiente implicado, y resuelve también con
> el valor coherente. Eso no es corregir al profesor: es **verificar la
> plausibilidad del resultado**, que es lo que define a un ingeniero.

## 9.4 Ejercicios para desarrollar

**P9.1** Un pozo costero tiene su fondo a 25 m sobre la interfaz de agua salada,
en una formación con $K = 5\times10^{-4}$ m/s.

a. Calcula el caudal máximo admisible en m³/s, L/s y m³/día.
b. ¿Cuál sería el ascenso de la interfaz con ese caudal?
c. Si se quisiera bombear el doble, ¿a qué distancia de la interfaz habría que
   subir el fondo del pozo?

**P9.2** En una costa, el flujo de agua dulce hacia el mar es
$q' = 3\times10^{-4}$ ft³/s por pie de costa. El acuífero tiene 120 ft de espesor
y $K = 4\times10^{-3}$ ft/s.

a. Calcula la profundidad de la interfaz en la línea de costa.
b. Calcula la distancia al pie de la cuña.
c. Calcula la nueva posición si el flujo se reduce a la mitad.
d. Verifica el gradiente hidráulico implícito y comenta si es razonable.

*Respuestas en el Anexo C.*

# PARTE 10 — El taller del profesor, resumido

## 10.1 Todas las respuestas en una tabla

Para repasar rápido. Si alguna no te cuadra, el desarrollo completo está en el
documento *Solucionario*.

### Capítulo 3 — Movimiento del agua subterránea

| # | Respuesta |
|---|---|
| 1 | $q = 1.9\times10^{-8}$ m/s |
| 2 | $v = 1.9\times10^{-7}$ m/s ($n_e=0.1$); $1.9\times10^{-4}$ m/s ($n_e=10^{-4}$) |
| 3 | Medio granular frente a roca fracturada |
| 4 | $[P/\rho g] = L$ usando $F = MLT^{-2}$ |
| 5 | $[h]=L$ (energía/peso); $[\phi]=L^2/T^2$ (energía/masa) |
| 6 | $i = 0.141$ m/m, flujo hacia el **S 45° W** |
| 7 | $h$: 300/205/110/15 · $h_p$: 200/190/50/8 · $z$: 100/15/60/7 m |
| 8 | $3.28\times10^{-6}$ ft/s · 2.12 gpd/ft² · $1.02\times10^{-9}$ cm² · 0.103 darcy |
| 9 | Flujo horizontal ($\partial z/\partial x=0$), $\rho$ y $\mu$ constantes |
| 10 | Sólo (a) es correcta; (d) invierte $q$ y $v$; b, c, e, f, g omiten el signo menos |
| 11 | $K_h = 3.70\times10^{-7}$; $K_v = 2.70\times10^{-8}$ m/s; razón 13.7 |
| 12 | $q_x = 1\times10^{-4}$ cm/s (por simetría del tensor) |
| 13 | $K$ más alta: $K_3$ · más baja: $K_2$ · razón ≈ 3–4 |
| 14 | Recarga: equipotenciales se **juntan** · descarga: se **separan** |
| 15 | Mayor velocidad en $h_4$ (el doble); flujo **descendente** en ambas |
| 16 | $q = 5\times10^{-8}$ cm/s, descendente ($\approx1.6$ cm/año) |
| 17 | $Q_{in}=1\times10^{-4}$ cada uno · salidas $1.5\times10^{-4}$ y $5\times10^{-5}$ m³/s · $i$ = 0.15 y 0.05 |

### Capítulo 4 — Ecuaciones, fronteras y redes

| # | Respuesta |
|---|---|
| 1 | (a) $\partial^2h/\partial x^2 = (S_s/K)\partial h/\partial t$ (b) $\nabla^2h=(\rho g\beta_p/K)\partial h/\partial t$ (c) $\nabla^2h=0$ (d) **arcilla** |
| 2 | (a) 300 m³ (b) $S=8.48\times10^{-5}$ (c) $\beta_p=3.66\times10^{-10}$ m²/N |
| 3 | (a) el caudal de bombeo $Q$ (b) el volumen total extraído $Qt$ |
| 4 | (a) 6250/4368/1882 (b) 4998/4368/630 lb/ft² (c) **No**, $FS=0.86$ (d) ≈30.1 ft |
| 5 | $T = Q/(n_f\Delta h) \approx 1.2\times10^{3}$ m²/día |
| 6 | AB y DE: equipotenciales (carga constante) · BC, CD, FG: líneas de flujo (sin flujo) |
| 7 | $Q = KH\,n_f/n_d$: $3.64$ / $5.05$ / $8.73 \times10^{-3}$ m³/s·m (100/139/240 %) |
| 8 | Redes de flujo (ver Parte 5) |
| 9 | Nivel freático: $h=z$, ni equipotencial ni línea de flujo |
| 10 | $x'=0.447x$ · $K_{eq}=\sqrt{K_hK_v}=2.24K_v$ · celdas 2.24:1 |

### Capítulo 5 — El agua en el ciclo hidrológico

| # | Respuesta |
|---|---|
| 1 | 5.5: tres fronteras sin flujo + nivel freático. 5.8 **añade** continuidad de $\phi$ y de $K\partial\phi/\partial z$ (medio estratificado) |
| 2 | Pérdida de simetría y refuerzo del flujo regional (5.4); dominio de celdas locales (5.27) |
| 3 | $h_{canal}=0$ siempre · $h_{divisoria}$ = 12.00/12.00/11.86/10.67 m a 10/20/40/100 años · $q'=1.25\times10^{-2}$ y $3.96\times10^{-3}$ m³/día·m |
| 4 | $FS=\sigma_T/u$; $d_{crit}=(\gamma_{sat}D-\gamma_wh_p)/(\gamma_{sat}-\gamma_w)$ |
| 5 | $Q_{max}=0.6\pi Kd^2G = 7.0\times10^{-3}$ m³/s = 7 L/s = 111 gpm |
| 6 | $x_{toe}=2061$ ft; con la mitad del caudal, 4124 ft. Con el $2\times10^{-1}$ del enunciado **no existe cuña** |

## 10.2 Ejercicio más completo núm. 1 — El sistema de dos acuíferos (3.17)

Este es el ejercicio más integrador del taller: combina Darcy horizontal, Darcy
vertical, dos áreas distintas, balance de masa y dibujo de superficies
piezométricas. Si entiendes este, entiendes el capítulo 3 completo.

**Enunciado.** Un acuífero confinado superior está sobre otro acuífero, separados
por una capa confinante de baja permeabilidad. Además de la geometría de la
figura, se sabe que:

1. La conductividad de ambos acuíferos es del orden de $10^{-6}$ m/s.
2. La conductividad vertical de la capa confinante es del orden de $10^{-9}$ m/s.
3. Las cargas del acuífero **inferior** son unos 10 m **más altas** que las del
   superior.
4. El gradiente hidráulico en las zonas de entrada de ambos acuíferos es del
   orden de $10^{-1}$ m/m.

a. Calcular el caudal de entrada $Q$ a ambos acuíferos.
b. Calcular el caudal de salida de ambos.
c. Calcular el gradiente en las zonas de salida.
d. Dibujar la forma general de las superficies piezométricas.

![**Figura 25.** Geometría del bloque (arriba), balance de masa con la fuga ascendente, y las superficies piezométricas resultantes (abajo).](fig/fig_3_17_sistema.png){width=15.8cm}

### Paso 1 — Extraer la geometría y, sobre todo, las DOS áreas

De la figura: longitud en la dirección del flujo $L = 1000$ m, ancho $W = 100$ m,
acuífero superior 10 m, capa confinante 20 m, acuífero inferior 10 m.

**Aquí está el error que arruina el problema:** hay dos áreas distintas y hay que
no confundirlas.

| Para flujo | Área | Valor |
|---|---|---|
| **Horizontal** (en los acuíferos) | transversal = espesor × ancho | $10\times100 = 1000\ \mathrm{m^2}$ |
| **Vertical** (fuga por la confinante) | en planta = longitud × ancho | $1000\times100 = 10^{5}\ \mathrm{m^2}$ |

### Paso 2 — Inciso (a): caudal de entrada

Darcy horizontal con el gradiente de entrada:

$$Q_{in} = K\,i\,A_{transversal} = (10^{-6})(0.1)(1000)$$

$$\boxed{Q_{in} = 1\times10^{-4}\ \mathrm{m^3/s\ en\ cada\ acuífero}}
\qquad \sum Q_{in} = 2\times10^{-4}\ \mathrm{m^3/s}$$

Son iguales porque ambos acuíferos tienen la misma $K$, el mismo espesor y el
mismo gradiente de entrada.

### Paso 3 — La fuga vertical (la clave de todo)

$$q_{fuga} = K'\frac{\Delta h}{b'} = (10^{-9})\frac{10\ \mathrm{m}}{20\ \mathrm{m}}
= 5\times10^{-10}\ \mathrm{m/s}$$

$$Q_{fuga} = q_{fuga}\times A_{planta} = (5\times10^{-10})(1\times10^{5})
= 5\times10^{-5}\ \mathrm{m^3/s}$$

**Dirección:** el acuífero inferior tiene cargas 10 m **más altas**, así que la
fuga es **ascendente**, del inferior al superior.

> **El detalle que hay que comentar.** $K'$ es **mil veces menor** que $K$, pero
> el área en planta es **cien veces mayor** que la transversal. Esa competencia
> entre una conductividad minúscula y un área enorme hace que la fuga resulte ser
> el **50 %** del caudal de entrada. Por eso la fuga a través de acuitardos nunca
> se puede despreciar a escala regional.

### Paso 4 — Inciso (b): balance de masa en cada acuífero

Escribe el balance **por separado**. Esto es lo que se evalúa:

$$\boxed{Q_{out} = Q_{in} \pm Q_{fuga}}$$

- Acuífero **superior**: **recibe** la fuga →
  $Q_{out} = 1\times10^{-4} + 5\times10^{-5} = \boxed{1.5\times10^{-4}\ \mathrm{m^3/s}}$
- Acuífero **inferior**: **cede** la fuga →
  $Q_{out} = 1\times10^{-4} - 5\times10^{-5} = \boxed{5\times10^{-5}\ \mathrm{m^3/s}}$

**Verificación obligatoria:**

$$1.5\times10^{-4} + 5\times10^{-5} = 2\times10^{-4}\ \mathrm{m^3/s} = \sum Q_{in}\ \checkmark$$

El agua que cambia de acuífero no se pierde del sistema. Si no cierra, hay un
error aritmético.

### Paso 5 — Inciso (c): gradientes de salida

Invierte Darcy, usando de nuevo el área **transversal**:

$$i_{out} = \frac{Q_{out}}{K\,A_{transversal}}$$

$$i_{superior} = \frac{1.5\times10^{-4}}{(10^{-6})(1000)} = \boxed{0.15\ \mathrm{m/m}}$$

$$i_{inferior} = \frac{5\times10^{-5}}{(10^{-6})(1000)} = \boxed{0.05\ \mathrm{m/m}}$$

Tiene sentido inmediato: el acuífero que **gana** agua necesita **más** gradiente
para evacuarla; el que la **pierde**, menos.

### Paso 6 — Inciso (d): el dibujo

Cinco cosas que el dibujo debe mostrar:

1. Ambas superficies empiezan con pendiente 0.10 en la entrada.
2. La del acuífero **inferior se aplana** (0.10 → 0.05): cóncava hacia arriba.
3. La del **superior se empina** (0.10 → 0.15): convexa hacia arriba.
4. **Convergen**: la separación de 10 m se reduce aguas abajo.
5. La inferior queda **siempre por encima** de la superior: es lo que mantiene la
   fuga ascendente.

### El concepto grande

Este es el mecanismo de los **acuíferos semiconfinados** (*leaky aquifers*) y la
base de la teoría de Hantush-Jacob. Nota el **acoplamiento**: al converger las
superficies, $\Delta h$ disminuye y la fuga también. Un cálculo riguroso
requeriría resolver las dos ecuaciones acopladas; el enunciado te autoriza a usar
$\Delta h = 10$ m promedio. **Dilo explícitamente en el examen:** demuestra que
sabes qué estás simplificando, y eso siempre suma.

## 10.3 Ejercicio más completo núm. 2 — El canal a nivel del mar (5.3)

Este es el problema transitorio más completo del taller. Usa la función error y
la longitud de difusión $\sqrt{Tt/S}$, que es **la misma combinación** que aparece
en las pruebas de bombeo. Resolverlo consolida los dos temas a la vez.

**Enunciado.** Un canal a nivel del mar se excava en una zona donde el nivel
freático es plano y está 12 m sobre el nivel del mar. El canal llega a 9 m bajo el
nivel del mar y hay una divisoria de aguas (manantiales) a unas 3 millas del
canal. $K = 8.35$ cm/día y rendimiento específico $S_y = 0.01$.

a. Calcular la carga $h$ en el canal y en la divisoria a los 10, 20, 40 y 100 años.
b. Calcular el caudal $q'$ hacia el canal a los 10 y a los 100 años.

![**Figura 26.** Geometría del canal y descenso progresivo del nivel freático.](fig/fig_5_03_canal.png){width=15.8cm}

### Paso 1 — Declarar las hipótesis (aquí se gana la mitad de la nota)

1. **Datum en el nivel del mar** = nivel de agua en el canal. Entonces $h = 0$ en
   el canal y la carga inicial es $h_0 = 12$ m en todo el dominio.
2. **Base del sistema en el fondo del canal** (9 m bajo el nivel del mar).
3. **Linealización:** el acuífero es libre, así que $T$ depende de $h$ (ecuación
   de Boussinesq, no lineal). Se linealiza con el espesor saturado **medio**:

$$\bar b = \frac{(12+9) + 9}{2} = \frac{21+9}{2} = 15\ \mathrm{m}$$

### Paso 2 — Calcular $T$ y la difusividad

$$T = K\,\bar b = (0.0835\ \mathrm{m/día})(15\ \mathrm{m}) = 1.2525\ \mathrm{m^2/día}$$

$$\nu = \frac{T}{S_y} = \frac{1.2525}{0.01} = 125.25\ \mathrm{m^2/día}$$

$\nu$ es la **difusividad hidráulica** y controla toda la respuesta transitoria.

### Paso 3 — Identificar la solución

**Qué le pasó al acuífero:** se excavó el canal y la carga en $x = 0$ cayó **de
golpe** de 12 m a 0, y se mantiene ahí. Eso es exactamente el problema del medio
semi-infinito con cambio escalón en la frontera, cuya solución (analogía con la
conducción de calor) es

$$\boxed{h(x,t) = h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{\nu t}}\right)
= h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{Tt/S_y}}\right)}$$

**Verifica que cumple las tres condiciones** (hazlo, son tres líneas y blindan la
respuesta):

| Condición | Comprobación |
|---|---|
| $h = 0$ en $x=0$ para todo $t$ | $\mathrm{erf}(0)=0$ ✓ |
| $h = h_0$ en $t=0$ para todo $x>0$ | $t\to0$ ⇒ argumento $\to\infty$ ⇒ $\mathrm{erf}\to1$ ✓ |
| $h \to h_0$ cuando $x\to\infty$ | $\mathrm{erf}(\infty)=1$ ✓ |

**Valores de la función error que conviene memorizar:**
$\mathrm{erf}(0)=0$, $\mathrm{erf}(1)=0.843$, $\mathrm{erf}(2)=0.995$,
$\mathrm{erf}(\infty)=1$. Regla práctica: para argumentos **mayores que 2**,
$\mathrm{erf}\approx1$ y la perturbación **aún no ha llegado**.

### Paso 4 — Inciso (a): las cargas

**En el canal ($x = 0$):** $h = h_0\,\mathrm{erf}(0) = 0$ **para todo $t$**.

> No te confundas al ver un resultado trivial: **es la condición de borde**. El
> canal impone el nivel del mar desde el instante cero, así que el abatimiento
> allí es de 12 m inmediatamente. Escríbelo así y explícalo; es la respuesta
> correcta.

**En la divisoria ($x = L = 3\ \mathrm{mi} = 4828$ m):**

| $t$ (años) | $t$ (días) | $\dfrac{L}{2\sqrt{\nu t}}$ | $\mathrm{erf}$ | $h$ (m) | Abatimiento (m) |
|---|---|---|---|---|---|
| 10 | 3653 | 3.569 | 1.00000 | **12.00** | 0.00 |
| 20 | 7305 | 2.524 | 0.99964 | **12.00** | 0.00 |
| 40 | 14 610 | 1.785 | 0.98839 | **11.86** | 0.14 |
| 100 | 36 525 | 1.129 | 0.88954 | **10.67** | 1.33 |

**Atajo de cálculo:** el argumento sólo depende de $t$ a través de $\sqrt{t}$, así
que calcula el de 10 años y escala: $\mathrm{arg}(100) = \mathrm{arg}(10)/\sqrt{10}$.

**La interpretación, que es la respuesta de verdad.** A los 10 y 20 años el
argumento es mayor que 2.5, de modo que $\mathrm{erf}\approx1$ y **la divisoria no
se ha enterado** de que existe el canal. A los 100 años sólo ha bajado 1.33 m de
los 12 m iniciales. Dos conclusiones: (1) la hipótesis de medio **semi-infinito**
es válida en todo el periodo analizado, porque la perturbación nunca alcanza la
frontera; (2) los **manantiales de la divisoria sobreviven** a escala de décadas,
aunque su caudal disminuya.

![**Figura 27.** Perfiles del nivel freático a los 10, 20, 40 y 100 años, y decaimiento del caudal hacia el canal.](fig/fig_5_03_perfiles.png){width=15.8cm}

### Paso 5 — Inciso (b): el caudal

**Deducción (tres líneas, y es lo más valioso de la respuesta).** El caudal es
Darcy evaluado en la frontera:

$$q' = T\left.\frac{\partial h}{\partial x}\right|_{x=0}$$

Derivando la función error (regla: $\frac{d}{du}\mathrm{erf}(u) = \frac{2}{\sqrt\pi}e^{-u^2}$)
con $u = x/2\sqrt{\nu t}$:

$$\frac{\partial h}{\partial x}
= h_0\frac{2}{\sqrt\pi}e^{-x^{2}/4\nu t}\cdot\frac{1}{2\sqrt{\nu t}}
= \frac{h_0}{\sqrt{\pi\nu t}}\,e^{-x^{2}/4\nu t}$$

En $x=0$ la exponencial vale 1:

$$q' = \frac{T h_0}{\sqrt{\pi\nu t}} = \frac{T h_0}{\sqrt{\pi T t/S_y}}
\qquad\Longrightarrow\qquad
\boxed{q' = h_0\sqrt{\frac{T\,S_y}{\pi\,t}}}$$

**A los 10 años** ($t = 3653$ días):

$$q' = 12\sqrt{\frac{(1.2525)(0.01)}{\pi(3653)}} = 12\sqrt{1.091\times10^{-6}}$$

$$\boxed{q' = 1.25\times10^{-2}\ \mathrm{m^3/día\ por\ metro\ de\ canal}
= 12.5\ \mathrm{L/día\cdot m}}$$

**A los 100 años** ($t = 36\,525$ días):

$$\boxed{q' = 3.96\times10^{-3}\ \mathrm{m^3/día\cdot m} = 4.0\ \mathrm{L/día\cdot m}}$$

Si el canal recibe agua por **ambos flancos**, se duplica. **Dilo
explícitamente.**

### Paso 6 — Las dos propiedades que hay que comentar

**1. $q' \propto t^{-1/2}$.** El caudal decae con la raíz del tiempo: enorme al
principio (infinito en $t=0$, singularidad matemática del escalón) y decreciente
para siempre. **Nunca alcanza régimen permanente** mientras el medio sea
semi-infinito. Verificación gratuita:

$$\frac{q'(10\ \mathrm{a})}{q'(100\ \mathrm{a})} = \sqrt{\frac{100}{10}} = \sqrt{10} = 3.16
\qquad\text{y en efecto}\quad \frac{1.254\times10^{-2}}{3.965\times10^{-3}} = 3.16\ \checkmark$$

**2. $q' \propto \sqrt{T S_y}$.** Depende de la **media geométrica** de
transmisividad y almacenamiento, no de cada uno por separado. Es la misma razón
por la que en una prueba de bombeo no se pueden separar $T$ y $S$ con un solo
dato.

### Paso 7 — Análisis de sensibilidad

La única decisión discutible es $\bar b$. Repítelo con $\bar b = 21$ m (espesor
inicial completo, $T = 1.754$ m²/día): sale $h_{divisoria}(100\ \mathrm{a}) = 9.87$ m
y $q'(10\ \mathrm{a}) = 1.48\times10^{-2}$. Las conclusiones no cambian y $q'$
varía un 18 %. **Declarar la hipótesis y acotar su efecto es lo que hace la
respuesta inatacable.**

### Por qué este ejercicio vale la pena para el parcial

Fíjate en la estructura: $\sqrt{Tt/S}$ aparece aquí y en Cooper-Jacob
($t_0 = r^2S/2.25T$ es la misma combinación despejada), y en el radio de
influencia ($R_0 = \sqrt{2.25Tt/S}$). **Es el mismo grupo adimensional en los tres
sitios.** Si lo reconoces, los tres temas se vuelven uno.

# PARTE 11 — Tus apuntes de clase, explicados y resueltos

Esta parte resume y resuelve todo el contenido de las nueve páginas de tus apuntes. Sus secciones van de 11.A a 11.N, y cuando el texto dice "sección D" se refiere a 11.D.


## 11.A — Qué encontré en tus apuntes y qué faltaba

Revisé las nueve páginas del PDF. Los apuntes son desordenados, pero tienen
**mucho más contenido del que yo había supuesto**: hay temas que no estaban en
esta guía y que además son muy "examinables". Este documento los cubre.

| Tema de los apuntes | ¿Estaba en esta guía? | Dónde está ahora |
|---|---|---|
| $S = S_y + S_s b$ (almacenamiento completo) | **No** | Sección B.1 |
| Teorema de la divergencia aplicado al flujo | **No** | Sección B.2 |
| Difusividad hidráulica | Parcialmente | Sección B.3 |
| **Dupuit-Forchheimer con recarga** | **No** | Secciones B.4 y C |
| **Acuífero costero + cambio climático** | **No** | Sección D |
| **Corrección barométrica y por marea** | **No** | Sección B.5 |
| Funciones de Bessel y transformada de Laplace | **No** | Sección B.6 |
| Thiem con dos piezómetros | Sí | Sección E (con tus datos) |
| Theis por punto de coincidencia | Sí | Sección F (con tus datos) |
| Superposición y pozos imagen | Sí | Sección G (con tus datos) |
| Mapas de isopiezas y gradientes | Parcialmente | Sección H |
| Cargas en una sección de flujo regional | Parcialmente | Sección I |
| Tensión superficial y capilaridad | **No** | Sección B.7 |

**Lo más importante que descubrí:** el curso trabaja **acuíferos libres con el
enfoque de Dupuit** y un **problema costero completo con escenario de cambio
climático**. Eso cambia las prioridades: si el profesor dio ese ejercicio en
clase con datos concretos, es muy probable que caiga algo parecido.

> **Nota sobre los otros archivos de la rama.** Las siete imágenes `1.jpeg` a
> `7.jpeg` son renders de un coliseo y `EJERCICIO.xls` es un presupuesto de obra:
> pertenecen a la propuesta de licitación de Sandoná, no a hidráulica, así que no
> los incluí. Las imágenes de hidráulica están **dentro** del PDF (las fotos de los
> problemas del libro y del tablero), y esas sí están resueltas aquí.

> **Nota sobre los números.** Todos los cálculos de este documento están
> verificados y **reproducen los resultados de tus propios apuntes** (924.4 m,
> 885.2 m, −39.1 m, 0.41 m, $0.503\,Q$, 13 677 ft²/día, 8.4 m, 21 m, 29.4 m).
> Donde encontré un error de transcripción lo señalo en la sección J.

## 11.B — Los temas de teoría que faltaban

### B.1 El almacenamiento completo: $S = S_y + S_s\,b$

En esta guía traté el almacenamiento confinado ($S = S_s b$) y mencioné
$S_y$ como un valor aparte. Tus apuntes traen la **ecuación completa**, que es la
que vale para un acuífero libre:

$$\boxed{S = S_y + S_s\,b}$$

| Término | Mecanismo físico | Qué pasa |
|---|---|---|
| $S_y$ | **drenaje** | los poros se vacían por gravedad al bajar el nivel freático |
| $S_s\,b$ | **descompresión** | la matriz se compacta y el agua se expande |

Y la definición operacional que traen tus apuntes:

$$S_s = \frac{\mathcal{V}_w}{\mathcal{V}_{acu}\,\Delta h}\quad [\mathrm{L^{-1}}]
\qquad\qquad
S = \frac{\mathcal{V}_w}{A_{acu}\,\Delta h}\quad [\text{adimensional}]$$

Nota la diferencia: $S_s$ divide por el **volumen** del acuífero (de ahí las
unidades $\mathrm{m^{-1}}$); $S$ divide por el **área** en planta (y queda
adimensional). Pasar de uno a otro es multiplicar por el espesor.

#### El ejemplo del Valle del Cauca (de tus apuntes)

Con $b = 500$ m y $S_y = 0.27$:

| $S_s$ (1/m) | $S_s\,b$ | $S = S_y + S_s b$ | Aporte de $S_y$ |
|---|---|---|---|
| $10^{-3}$ | 0.500 | 0.770 | 35 % |
| $10^{-5}$ | 0.005 | 0.275 | **98 %** |
| $10^{-6}$ | 0.0005 | 0.2705 | **99.8 %** |

**La conclusión que hay que saber decir:** en un acuífero **libre** el drenaje
($S_y$) domina sobre la descompresión ($S_s b$) por **uno o dos órdenes de
magnitud**, de modo que en la práctica $S \approx S_y$. En un acuífero
**confinado** no hay drenaje ($S_y = 0$) y queda sólo $S = S_s b$, que es
10 000 veces menor. Esa es la razón física de que los conos de abatimiento
confinados sean gigantescos.

> Ojo con el Valle del Cauca: $b = 500$ m es un espesor enorme, así que
> $S_s b$ llega a ser comparable a $S_y$ si $S_s$ está en el extremo alto
> ($10^{-3}$). En acuíferos delgados nunca ocurre.

### B.2 La ecuación de flujo sale del teorema de la divergencia

Tus apuntes traen esta línea, que es la deducción de la ecuación de flujo:

$$\oint_A \mathbf{q}\cdot\mathbf{n}\,dA = \int_V \nabla\cdot\mathbf{q}\,dV
= \text{Flujo neto}$$

**Qué dice en palabras.** El flujo neto que sale por la superficie de un volumen
(integral de la izquierda) es igual a la integral de la divergencia del flujo en
su interior. Es el teorema de la divergencia de Gauss.

**Por qué importa.** Ese flujo neto tiene que igualar al cambio de almacenamiento:

$$\underbrace{\nabla\cdot(K\nabla h)}_{\text{OUTPUT} - \text{INPUT}}
= S_s\frac{\partial h}{\partial t}$$

Y si $K$ es constante, $\nabla\cdot(K\nabla h) = K\nabla^2h$, de donde sale la
forma de acuífero que ya conoces:

$$T\,\nabla^{2}h = S\,\frac{\partial h}{\partial t}$$

**Para el examen:** si te preguntan "¿de dónde sale la ecuación de flujo?", la
respuesta es: **de combinar la ley de Darcy con la conservación de masa aplicada
a un volumen de control**, y el puente matemático es el teorema de la divergencia.

### B.3 Difusividad hidráulica

Tus apuntes definen $D_H$. **Atención, hay una errata ahí** (ver sección J): la
definición correcta es

$$\boxed{D_H = \nu = \frac{T}{S}}\qquad [\mathrm{L^2/T}]$$

y no $S/T$. La forma de comprobarlo es dimensional: una difusividad tiene
unidades de **área sobre tiempo**, y $T/S$ da m²/día dividido por un
adimensional, es decir m²/día ✓. En cambio $S/T$ daría día/m².

**Qué significa.** Es la velocidad con que se propaga una perturbación de carga.
La **longitud de difusión** es

$$\ell(t) = \sqrt{D_H\,t} = \sqrt{\frac{T\,t}{S}}$$

y es **la misma combinación** que aparece en Cooper-Jacob
($t_0 = r^2S/2.25T$), en el radio de influencia ($R_0 = 1.5\sqrt{Tt/S}$) y en el
problema del canal de esta guía. Si reconoces ese grupo, los tres temas son
uno solo.

### B.4 Dupuit-Forchheimer: la hipótesis y las ecuaciones

Tus apuntes lo definen perfectamente:

> «En vez de resolver el flujo en 3 dimensiones, asumimos que el agua se mueve
> horizontalmente.»

**Las dos hipótesis de Dupuit:**

1. Las líneas de flujo son **horizontales** y las equipotenciales **verticales**.
2. El gradiente hidráulico es igual a la **pendiente del nivel freático**, y
   constante en toda la vertical.

**La consecuencia matemática.** En un acuífero libre el espesor saturado es $h$
mismo, de modo que el caudal por unidad de ancho es

$$q' = -K\,h\,\frac{dh}{dx} = -\frac{K}{2}\frac{d(h^{2})}{dx}$$

y por eso **en acuíferos libres todo va con $h^2$**, no con $h$. Esta es la razón
de fondo de la fórmula de Dupuit del régimen permanente que ya viste
($K = Q\ln(r_2/r_1)/[\pi(h_2^2-h_1^2)]$).

#### Flujo entre dos cuerpos de agua con recarga uniforme

Es el caso de tus apuntes. Un acuífero libre de longitud $L$ entre dos cuerpos de
agua con niveles $h_1$ (en $x=0$) y $h_2$ (en $x=L$), con recarga uniforme $W$
(positiva si entra, negativa si hay evapotranspiración neta):

**Perfil del nivel freático:**

$$\boxed{h^{2} = h_1^{2} - \frac{(h_1^{2}-h_2^{2})}{L}\,x + \frac{W}{K}(L-x)\,x}$$

**Caudal por unidad de ancho en cualquier $x$:**

$$\boxed{q'(x) = \frac{K\,(h_1^{2}-h_2^{2})}{2L} - W\left(\frac{L}{2}-x\right)}$$

**Posición de la divisoria de aguas** (donde $q' = 0$ y el nivel freático es
máximo):

$$\boxed{d = \frac{L}{2} - \frac{K}{W}\,\frac{(h_1^{2}-h_2^{2})}{2L}}$$

**Altura máxima:**

$$\boxed{h_{max} = \sqrt{h_1^{2} - \frac{(h_1^{2}-h_2^{2})}{L}\,d
+ \frac{W}{K}(L-d)\,d}}$$

> **La verificación que nadie hace y que vale puntos:** después de calcular $d$
> hay que comprobar que **$0 \le d \le L$**. Si cae fuera, no existe divisoria
> dentro del acuífero y por tanto no existe $h_{max}$ interno: el nivel freático
> crece o decrece monótonamente de un borde al otro. Lo verás en la sección C.

**El criterio físico detrás:** compara los dos términos de $q'$.

$$\left|\frac{K(h_1^{2}-h_2^{2})}{2L}\right|
\quad\text{vs}\quad
\left|\frac{W\,L}{2}\right|$$

Si domina el primero, manda la **diferencia de carga** y no hay divisoria. Si
domina el segundo, manda la **recarga** y se forma un montículo con su divisoria.

### B.5 Correcciones barométrica y por marea

Esto aparece en tus apuntes (página 5) y **no estaba en esta guía**. Es un
tema clásico de preguntas conceptuales.

#### El fenómeno

En un acuífero **confinado**, el nivel de agua de un pozo cambia sin que entre ni
salga agua del acuífero, por dos causas externas:

| Causa | Qué pasa |
|---|---|
| **Presión atmosférica** sube | el nivel en el pozo **baja** |
| **Marea** sube (carga de agua de mar) | el nivel en el pozo **sube** |

**Por qué.** Un aumento de presión atmosférica actúa sobre la superficie libre
del pozo **de inmediato y por completo**, pero sobre el agua del acuífero actúa
sólo en parte, porque los granos del esqueleto absorben una fracción de la carga.
El desbalance hace bajar el nivel del pozo. La marea es lo contrario: la carga
adicional se transmite al acuífero y sube la presión del agua.

#### Eficiencia barométrica

$$\boxed{BE = \frac{|\Delta h_{pozo}|}{\Delta P_{atm}/\gamma_w}}$$

Es adimensional, entre 0 y 1, y típicamente 0.20–0.75. La corrección de los datos
es

$$\boxed{h_{corregido} = h_{medido} + BE\;\frac{P_{atm} - P_{ref}}{\gamma_w}}$$

#### Eficiencia de marea

$$\boxed{TE = \frac{\Delta h_{pozo}}{\Delta h_{marea}}}
\qquad\qquad
\boxed{BE + TE = 1}$$

La suma vale 1 porque las dos reparten la **misma** carga entre el esqueleto y el
agua: lo que una toma, la otra lo deja.

#### Ejemplo numérico

Un acuífero confinado tiene $BE = 0.45$.

**(a) La presión atmosférica sube 1.0 kPa. ¿Cuánto cambia el nivel del pozo?**

Primero, el equivalente en columna de agua:

$$\frac{\Delta P}{\gamma_w} = \frac{1.0\ \mathrm{kPa}}{9.81\ \mathrm{kN/m^3}}
= 0.1019\ \mathrm{m}$$

$$|\Delta h| = BE \times 0.1019 = 0.45\,(0.1019)
= \boxed{0.046\ \mathrm{m} = 4.6\ \mathrm{cm\ de\ BAJADA}}$$

**(b) ¿Cuál es la eficiencia de marea?** $TE = 1 - 0.45 = \boxed{0.55}$

**(c) Con una marea de 1.2 m de amplitud, ¿cuánto oscila el pozo?**

$$\Delta h_{pozo} = TE \times 1.2 = 0.55\,(1.2) = \boxed{0.66\ \mathrm{m}}$$

> **Por qué importa en una prueba de bombeo.** Un abatimiento de pocos
> centímetros medido durante varios días puede estar enteramente contaminado por
> el efecto barométrico. **Antes de graficar $s$ contra $\log t$ hay que corregir
> los datos**, o el $T$ calculado estará mal. Si el profesor pregunta "¿qué
> correcciones hay que aplicar a los datos de una prueba de bombeo?", la
> respuesta es: barométrica, por marea, y por tendencia regional del nivel.

### B.6 Por qué aparecen Bessel y Laplace

Tus apuntes anotan «Repaso: funciones de Bessel, transformada de Laplace». No es
decoración: son las herramientas con que se resuelven las ecuaciones del curso.

| Herramienta | Dónde aparece |
|---|---|
| **Transformada de Laplace** | para resolver $\nabla^2h = (S/T)\partial h/\partial t$ en el tiempo. Es el camino con que Theis obtuvo $W(u)$ |
| **Función de Bessel modificada $K_0$** | en **acuíferos semiconfinados**: la solución de Hantush-Jacob es $s = \frac{Q}{4\pi T}W(u, r/B)$, y en régimen permanente se reduce a $s = \frac{Q}{2\pi T}K_0(r/B)$ (solución de De Glee) |

**Lo que esto te dice sobre el parcial:** si el profesor pidió repasar Bessel, es
porque piensa tocar **acuíferos semiconfinados** (*leaky*). El parámetro clave es
el **factor de goteo**

$$B = \sqrt{\frac{T\,b'}{K'}}$$

donde $b'$ y $K'$ son el espesor y la conductividad vertical del acuitardo. Es la
misma fuga que calculaste en el ejercicio 3.17 del taller, pero ahora en régimen
transitorio alrededor de un pozo. Tus apuntes también mencionan «GOTEO» en la
página 1, lo que lo confirma.

### B.7 Tensión superficial y capilaridad

Primera línea de tus apuntes, y es la base de la **zona no saturada**.

**Tensión superficial** ($\sigma \approx 0.0728$ N/m a 20 °C). Aparece en la
interfaz entre dos fluidos (agua y aire) porque las moléculas del interior se
atraen en todas las direcciones y las de la superficie sólo hacia abajo. El
resultado es una película en tensión.

**Capilaridad.** Es la capacidad del agua de **subir o bajar en contra de la
gravedad** dentro de un tubo o un poro. La altura de ascenso capilar es

$$h_c = \frac{2\sigma\cos\alpha}{\rho_w\,g\,r}$$

con $r$ el radio del poro y $\alpha$ el ángulo de contacto. Lo esencial:
**$h_c$ es inversamente proporcional al radio del poro.**

| Material | Radio de poro | Ascenso capilar |
|---|---|---|
| Grava | grande | centímetros |
| Arena | medio | decenas de cm |
| Limo | pequeño | 1–3 m |
| Arcilla | diminuto | decenas de m |

**Las dos consecuencias que se preguntan:**

1. La **franja capilar** sobre el nivel freático está saturada pero con presión
   **menor que la atmosférica** ($h_p$ negativa). El nivel freático es, por
   definición, donde $h_p = 0$.
2. En la zona no saturada $K$ **depende del contenido de agua**: al secarse, los
   poros grandes se vacían primero y el agua queda en los pequeños, donde circula
   peor. Por eso $K$ no saturada cae varios órdenes de magnitud y la ecuación de
   flujo se vuelve no lineal (Richards).

## 11.C — Dupuit con recarga: el ejemplo de tus apuntes resuelto

**Enunciado (datos de la página 2 de tus apuntes).**
$K = 10$ m/día, $S_y = 0.27$, $b = 30$ m, $h_1 = 15$ m, $h_2 = 18$ m,
$L = 200$ m. Dos casos de recarga: $W = -60$ mm/año y $W = +20$ mm/año.
Calcular $q'_1$, $q'_2$, $d$ y $h_{max}$.

### Paso 1 — Unidades (siempre primero)

$$W_A = -\frac{60\ \mathrm{mm/año}}{1000\times365.25}
= -1.643\times10^{-4}\ \mathrm{m/día}$$

$$W_B = +\frac{20}{1000\times365.25} = +5.476\times10^{-5}\ \mathrm{m/día}$$

El signo negativo del caso A significa **descarga neta** (evapotranspiración
mayor que la lluvia): el acuífero pierde agua por arriba.

### Paso 2 — El término de carga

$$h_1^{2}-h_2^{2} = 225 - 324 = -99\ \mathrm{m^2}$$

Es **negativo** porque $h_2 > h_1$: el nivel es más alto en el borde derecho, así
que el flujo global va de derecha a izquierda.

$$\frac{K(h_1^{2}-h_2^{2})}{2L} = \frac{10\,(-99)}{2(200)}
= -2.475\ \mathrm{m^2/día}$$

### Paso 3 — Caudales en los bordes

$$q'(x) = -2.475 - W\left(100 - x\right)$$

**Caso A** ($W = -1.643\times10^{-4}$):

$$q'_1 = q'(0) = -2.475 - (-1.643\times10^{-4})(100) = \boxed{-2.459\ \mathrm{m^2/día}}$$

$$q'_2 = q'(200) = -2.475 - (-1.643\times10^{-4})(-100) = \boxed{-2.491\ \mathrm{m^2/día}}$$

**Caso B** ($W = +5.476\times10^{-5}$):

$$q'_1 = \boxed{-2.481\ \mathrm{m^2/día}}
\qquad\qquad
q'_2 = \boxed{-2.470\ \mathrm{m^2/día}}$$

**Verificación por balance de masa (hazla siempre):**

$$q'(L) - q'(0) = W\,L$$

Caso A: $-2.491-(-2.459) = -0.0329$ y $W L = -1.643\times10^{-4}(200) = -0.0329$ ✓
Caso B: $-2.470-(-2.481) = +0.0110$ y $WL = +0.0110$ ✓

**Interpretación de los signos:** $q'$ es negativo en todo el dominio, es decir
el flujo va en la dirección $-x$ (de derecha a izquierda, del nivel alto al
bajo) en **ambos** casos. La recarga sólo lo modifica en un 0.7 % y un 0.2 %.

### Paso 4 — La divisoria

$$d = \frac{L}{2} - \frac{K}{W}\frac{(h_1^{2}-h_2^{2})}{2L}$$

**Caso A:** $K/W = 10/(-1.643\times10^{-4}) = -60\,876$

$$d = 100 - (-60\,876)\frac{-99}{400} = 100 - 15\,067 = -14\,967\ \mathrm{m}$$

**Caso B:** $K/W = 182\,648$

$$d = 100 - (182\,648)\frac{-99}{400} = 100 + 45\,200 = +45\,300\ \mathrm{m}$$

$$\boxed{\text{En los dos casos } d \notin [0,\,200]\ \mathrm{m}}$$

### Paso 5 — La conclusión (esto es la respuesta)

$$\boxed{\begin{array}{l}
\text{No existe divisoria de aguas dentro del acuífero, y por tanto}\\
\text{tampoco existe } h_{max}\text{ interno. El nivel freático crece}\\
\text{monótonamente de } h_1=15\text{ m a } h_2=18\text{ m.}
\end{array}}$$

Perfil calculado del caso B:

| $x$ (m) | 0 | 50 | 100 | 150 | 200 |
|---|---|---|---|---|---|
| $h$ (m) | 15.000 | 15.805 | 16.570 | 17.300 | 18.000 |

**Por qué pasa esto.** Compara los dos términos:

| | Caso A | Caso B |
|---|---|---|
| $\left|K(h_1^2-h_2^2)/2L\right|$ | 2.475 | 2.475 |
| $\left|W L/2\right|$ | 0.016 | 0.0055 |
| ¿Quién domina? | **la carga**, 150× | **la carga**, 450× |

La diferencia de carga (3 m sobre 200 m, con $K = 10$ m/día) mueve mucho más agua
que la que aporta una recarga de milímetros al año. **Para que apareciera una
divisoria se necesitaría $|W| \ge 25$ mm/día, es decir unos 9000 mm/año**, que es
físicamente imposible como recarga.

> **Esta es la respuesta correcta y es la que el profesor quiere ver.** La trampa
> del ejercicio no es calcular $h_{max}$: es darse cuenta de que **no existe**.
> Aplicar la fórmula de $h_{max}$ con $d = 45\,300$ m daría un número sin ningún
> significado físico.

### Paso 6 — Variante donde sí hay divisoria (para que practiques $h_{max}$)

Cambio los datos para que domine la recarga: $K = 1$ m/día, $W = 200$ mm/año
$= 5.476\times10^{-4}$ m/día, $L = 1000$ m, $h_1 = 20$ m, $h_2 = 18$ m.

**Comprobación previa:** $|K(h_1^2-h_2^2)/2L| = 0.038$ frente a
$|WL/2| = 0.274$ → **domina la recarga**, debe haber divisoria.

$$d = 500 - \frac{1}{5.476\times10^{-4}}\cdot\frac{76}{2000}
= 500 - 69.4 = \boxed{430.6\ \mathrm{m}}\quad \in[0,1000]\ \checkmark$$

$$h_{max} = \sqrt{400 - \frac{76(430.6)}{1000}
+ \frac{5.476\times10^{-4}}{1}(569.4)(430.6)}$$

$$h_{max} = \sqrt{400 - 32.73 + 134.26} = \sqrt{501.5}
= \boxed{22.40\ \mathrm{m}}$$

El nivel freático sube 2.40 m por encima del borde más alto: se forma un
**montículo de recarga**.

**Caudales de salida:**

$$q'(0) = 0.038 - 0.274 = -0.236\ \mathrm{m^2/día}\ \text{(sale por la izquierda)}$$

$$q'(L) = 0.038 + 0.274 = +0.312\ \mathrm{m^2/día}\ \text{(sale por la derecha)}$$

**Verificación final:** $0.236 + 0.312 = 0.548$ y la recarga total es
$W L = 5.476\times10^{-4}(1000) = 0.548\ \mathrm{m^2/día}$ ✓ **Todo lo que entra
por arriba sale por los dos bordes.** Que el balance cierre es la señal de que el
problema está bien resuelto.

![**Figura C1.** A la izquierda, el ejemplo de clase: las tres curvas casi coinciden y no hay divisoria. A la derecha, la variante del Paso 6, donde domina la recarga y aparece un montículo.](fig/fig_c1_dupuit.png){width=15.8cm}

## 11.D — El acuífero costero con cambio climático

Este es el ejercicio más completo de tus apuntes (páginas 3 y 4) y el que más
probabilidad tiene de caer, porque el profesor lo desarrolló en clase con datos
concretos. Combina Dupuit, Ghyben-Herzberg e intrusión salina.

### D.1 Los datos

**Del ejercicio base (sin cambio climático):**

| Símbolo | Significado | Valor |
|---|---|---|
| $W$ | recarga por lluvia | 500 mm/año |
| $L_0$ | largo inicial del acuífero | 1000 m |
| $K$ | conductividad hidráulica | $1\times10^{-4}$ m/s |
| $n_e$ | porosidad efectiva | 0.35 |
| $\rho_f$ | densidad agua dulce | 1.000 |
| $\rho_s$ | densidad agua salada | 1.025 |
| $\Delta\rho$ | $\rho_s - \rho_f$ | 0.025 |
| $s_0$ | profundidad del fondo del acuífero bajo el nivel del mar | 30 m |

**Del escenario de cambio climático:**

| Símbolo | Significado | Valor |
|---|---|---|
| $\tan\theta$ | pendiente de la playa | 0.02 (2 %) |
| $\Delta S$ | aumento del nivel del mar | 0.6 m |
| $\Delta L_{CE}$ | erosión costera | 3 m |

### D.2 El sistema de coordenadas (si esto se confunde, todo sale mal)

$$x = 0 \;\text{en la divisoria interior}
\qquad\longrightarrow\qquad
x = L \;\text{en la línea de costa}$$

- **Zona interior** (agua dulce en todo el espesor): de $x=0$ a $x=x_T$.
- **Zona de intrusión salina** (cuña salada abajo): de $x=x_T$ a $x=L$.
- $x_T$ = **punta (pie) de la cuña salina**.

De modo que la **longitud invadida** por el agua salada es $L - x_T$. Es
importante: $x_T$ se mide desde el interior, así que un $x_T$ menor **no**
significa automáticamente más intrusión si $L$ también cambió.

![**Figura D1.** Arriba, el acuífero antes (azul) y después (rojo) del cambio climático: la costa retrocede, el mar sube y la interfaz se desplaza. Abajo, las dos lecturas del resultado: la punta se mueve 39.1 m, pero la cuña sólo avanza 6.1 m respecto a la costa.](fig/fig_c2_costa.png){width=15.8cm}

### D.3 Las dos relaciones físicas de fondo

**Ghyben-Herzberg.** El agua salada pesa más, de modo que por cada metro de agua
dulce sobre el nivel del mar hay 40 m de agua dulce por debajo:

$$z = \frac{\rho_f}{\rho_s-\rho_f}\,h = \frac{1.000}{0.025}\,h = 40\,h$$

**Dupuit.** El flujo es horizontal, así que todo va con $h^2$.

Combinando ambas con la recarga uniforme se obtienen las dos fórmulas del curso:

$$\boxed{x_T = \sqrt{L^{2} - \frac{\rho_s\,\Delta\rho\,K}{\rho_f^{2}\,W}\,s^{2}}}$$

$$\boxed{H(x) = \sqrt{\frac{W}{K}\left(L^{2}-x^{2}\right)
+ \frac{\rho_s}{\rho_f}\,s^{2}}}$$

donde $H$ es la carga **medida desde la base del acuífero**. El nivel freático
sobre el nivel del mar es entonces $h = H - s$.

### D.4 Paso 1 — Unidades y la constante $C$

$$W = 500\ \mathrm{mm/año} = 0.5\ \mathrm{m/año}
= \frac{0.5}{365.25\times86\,400} = 1.584\times10^{-8}\ \mathrm{m/s}$$

**Es imprescindible pasar $W$ a m/s**, porque $K$ está en m/s y en la fórmula
aparece el cociente $K/W$, que debe quedar adimensional:

$$\frac{K}{W} = \frac{1\times10^{-4}}{1.584\times10^{-8}} = 6312$$

Ahora la constante que agrupa todo:

$$C = \frac{\rho_s\,\Delta\rho\,K}{\rho_f^{2}\,W}
= \frac{(1.025)(0.025)(1\times10^{-4})}{(1.000)^{2}(1.584\times10^{-8})}
= \frac{2.5625\times10^{-6}}{1.584\times10^{-8}}$$

$$\boxed{C = 161.7\ \text{(adimensional)}}$$

Coincide con el 161.8 de tus apuntes ✓

### D.5 Paso 2 — Cuánto retrocede la costa

Dos efectos que se suman, los dos negativos (el acuífero se acorta):

$$\Delta L = \underbrace{-\frac{\Delta S}{\tan\theta}}_{\text{por subida del mar}}
\;\underbrace{-\;\Delta L_{CE}}_{\text{por erosión}}
= -\frac{0.6}{0.02} - 3 = -30 - 3$$

$$\boxed{\Delta L = -33\ \mathrm{m}}$$

**De dónde sale el $\Delta S/\tan\theta$.** Si el mar sube $\Delta S$ y la playa
tiene pendiente $\tan\theta$, la línea de costa se desplaza horizontalmente
$\Delta S/\tan\theta$ tierra adentro. Con una pendiente del 2 %, **0.6 m de
subida del mar se traducen en 30 m de retroceso horizontal**: el factor de
amplificación es $1/\tan\theta = 50$. Ese es el resultado que asusta del cambio
climático en costas planas.

**Nuevos valores:**

$$L_f = 1000 - 33 = 967\ \mathrm{m}
\qquad\qquad
s_f = 30 + 0.6 = 30.6\ \mathrm{m}$$

### D.6 Pregunta 1 — ¿Cuánto avanza la cuña tierra adentro?

**Antes del cambio climático:**

$$x_{T0} = \sqrt{(1000)^{2} - 161.7\,(30)^{2}}
= \sqrt{1\,000\,000 - 145\,560} = \sqrt{854\,440}$$

$$\boxed{x_{T0} = 924.4\ \mathrm{m}}$$

**Después:**

$$x_{Tf} = \sqrt{(967)^{2} - 161.7\,(30.6)^{2}}
= \sqrt{935\,089 - 151\,440} = \sqrt{783\,649}$$

$$\boxed{x_{Tf} = 885.2\ \mathrm{m}}$$

$$\Delta x_T = 885.2 - 924.4 = \boxed{-39.1\ \mathrm{m}}$$

Los tres números coinciden con tus apuntes ✓

#### Pero cuidado con interpretarlo: hay dos respuestas distintas

| Qué se pregunta | Cálculo | Resultado |
|---|---|---|
| ¿Cuánto se desplaza la punta de la cuña **en el sistema de coordenadas**? | $\Delta x_T$ | **−39.1 m** |
| ¿Cuánto crece la **longitud invadida** por agua salada? | $(L_f-x_{Tf}) - (L_0-x_{T0})$ | **+6.1 m** |

$$L_0 - x_{T0} = 1000 - 924.4 = 75.6\ \mathrm{m}
\qquad
L_f - x_{Tf} = 967 - 885.2 = 81.8\ \mathrm{m}$$

**La explicación.** La punta se mueve 39.1 m hacia el interior, pero **33 de esos
39 metros son simplemente porque la costa se corrió 33 m**. El avance *real* de la
cuña respecto a la costa es sólo $39.1 - 33 = 6.1$ m.

> **Esto es lo que distingue una buena respuesta.** Si contestas sólo "−39.1 m",
> estás mezclando el movimiento de la frontera con el movimiento de la interfaz.
> Di las dos cifras y explica la diferencia.

### D.7 Pregunta 2 — ¿Cuánto sube el nivel freático?

Tus apuntes anotan correctamente las dos causas:

1. **El mar subió** (sube la condición de borde aguas abajo).
2. **El acuífero es más corto ahora**, de modo que la misma recarga se acumula
   sobre menos longitud.

Se evalúa $H(x)$ antes y después. En $x = 10$ m (cerca de la divisoria):

**Antes:**

$$H_0(10) = \sqrt{\frac{1.584\times10^{-8}}{1\times10^{-4}}\left[(1000)^2-(10)^2\right]
+ \frac{1.025}{1.000}(30)^{2}}$$

$$= \sqrt{(1.584\times10^{-4})(999\,900) + 922.5}
= \sqrt{158.4 + 922.5} = \sqrt{1080.9} = 32.877\ \mathrm{m}$$

**Después:**

$$H_f(10) = \sqrt{(1.584\times10^{-4})\left[(967)^2-(10)^2\right]
+ (1.025)(30.6)^{2}}$$

$$= \sqrt{148.1 + 959.8} = \sqrt{1107.9} = 33.285\ \mathrm{m}$$

$$\boxed{\Delta H = 33.285 - 32.877 = +0.41\ \mathrm{m}}$$

Coincide con tus apuntes ✓ Y el resultado es prácticamente el mismo en todo el
dominio:

| $x$ (m) | $H_0$ (m) | $H_f$ (m) | Subida |
|---|---|---|---|
| 10 | 32.877 | 33.285 | +0.408 m |
| 100 | 32.854 | 33.262 | +0.408 m |
| 500 | 32.270 | 32.685 | +0.415 m |

> **El detalle que hay que entender para no equivocarse.** $H$ se mide desde la
> **base del acuífero**, que no se mueve. Por eso $+0.41$ m es la subida
> **absoluta** del nivel freático. Pero medido **respecto al nuevo nivel del
> mar**, el nivel freático queda más bajo: $33.285 - 30.6 = 2.69$ m frente a
> $32.877 - 30 = 2.88$ m antes. Es decir, **el nivel freático sube 0.41 m pero el
> mar sube 0.60 m, así que la "altura de agua dulce disponible" sobre el mar
> disminuye 0.19 m**. Y como Ghyben-Herzberg dice $z = 40h$, esos 0.19 m menos
> equivalen a 7.6 m menos de espesor de agua dulce hacia abajo. Por eso la cuña
> avanza.

### D.8 Verificación independiente (hazla, blinda la respuesta)

**En la punta de la cuña**, la interfaz toca la base del acuífero, así que el
nivel freático sobre el mar debe valer exactamente $s\,\Delta\rho/\rho_f$ por
Ghyben-Herzberg:

$$H(x_{T0}) = \sqrt{(1.584\times10^{-4})\left[1000^2 - 924.4^2\right] + 922.5}
= 30.750\ \mathrm{m}$$

$$h = H - s = 30.750 - 30 = 0.750\ \mathrm{m}$$

$$\text{Teórico: } s\frac{\Delta\rho}{\rho_f} = 30\,(0.025) = 0.750\ \mathrm{m}
\ \checkmark\checkmark$$

**Coincidencia exacta.** Esto confirma que las dos fórmulas son consistentes
entre sí y que usaste bien las unidades.

**En la línea de costa** ($x = L$): $H = \sqrt{0 + 922.5} = 30.373$ m, es decir
el nivel freático está 0.373 m sobre el mar. No es cero porque existe una **cara
de descarga** (*outflow face*) por donde el agua dulce sale al mar.

### D.9 Resumen de respuestas

| Pregunta | Respuesta |
|---|---|
| Retroceso de la costa | $\Delta L = -33$ m (30 m por el mar + 3 m por erosión) |
| Punta de la cuña antes | $x_{T0} = 924.4$ m |
| Punta de la cuña después | $x_{Tf} = 885.2$ m |
| Desplazamiento de la punta | $-39.1$ m |
| **Avance real de la cuña** | **+6.1 m** (de 75.6 a 81.8 m invadidos) |
| Subida absoluta del nivel freático | **+0.41 m** |
| Nivel freático respecto al mar | **baja 0.19 m** |

## 11.E — Thiem con dos piezómetros (página 8)

**Enunciado.** Régimen permanente. $r_1 = 0.8$ m con $s_1 = 2.236$ m;
$r_2 = 30$ m con $s_2 = 1.088$ m. Hallar $T$.

**Solución.**

$$T = \frac{2.303\,Q}{2\pi\,(s_1-s_2)}\log_{10}\!\left(\frac{r_2}{r_1}\right)$$

$$\log_{10}\!\left(\frac{30}{0.8}\right) = \log_{10}(37.5) = 1.5740$$

$$\frac{2.303}{2\pi\,(2.236-1.088)} = \frac{2.303}{2\pi\,(1.148)}
= \frac{2.303}{7.2131} = 0.31928$$

$$T = (0.31928)(1.5740)\,Q = \boxed{0.5026\,Q}$$

Coincide con el $0.503\,Q$ de tus apuntes ✓ Con $Q = 788$ m³/día:

$$T = 0.5026\,(788) = \boxed{396\ \mathrm{m^2/día}}$$

**Equivalencia que conviene notar.** Esta fórmula es **idéntica** a la de Thiem
de esta guía, sólo escrita con logaritmo decimal:

$$T = \frac{Q\ln(r_2/r_1)}{2\pi(s_1-s_2)}
= \frac{788\,(3.6243)}{7.2131} = 396\ \mathrm{m^2/día}\ \checkmark$$

porque $\ln x = 2.303\log_{10}x$. **Si en el parcial te dan una y recuerdas la
otra, da exactamente lo mismo.**

> **Lo que vale comentar:** $r_1 = 0.8$ m es prácticamente el pozo de bombeo, no
> un piezómetro. Usar el pozo como punto de medida es menos confiable porque ahí
> hay **pérdidas de carga propias del pozo** (pérdidas de entrada por la rejilla,
> flujo turbulento), que inflan $s_1$ y por tanto **subestiman** $T$. Si hay dos
> piezómetros de observación verdaderos, se prefieren esos.

## 11.F — Theis por punto de coincidencia (página 8)

**Enunciado.** $Q = 500$ gal/min. Del ajuste de curva patrón se leyó el punto de
coincidencia $W(u) = 1$, $u = 0.1$, $s = 0.56$ ft, $r^2/t = 2.8\times10^{7}$
ft²/día. Hallar $T$ y $S$.

**Paso 1 — Unidades.**

$$Q = 500\ \frac{\mathrm{gal}}{\mathrm{min}}
\times\frac{1440\ \mathrm{min/día}}{7.4805\ \mathrm{gal/ft^3}}
= \boxed{96\,250\ \mathrm{ft^3/día}}$$

**Paso 2 — Transmisividad.**

$$T = \frac{Q\,W(u)}{4\pi\,s} = \frac{(96\,250)(1)}{4\pi\,(0.56)}
= \frac{96\,250}{7.0372}$$

$$\boxed{T = 13\,677\ \mathrm{ft^2/día}}$$

(Tus apuntes traen 13 667: es un error de transcripción de un dígito.)

**Paso 3 — Almacenamiento.**

$$S = \frac{4\,T\,u}{r^{2}/t} = \frac{4\,(13\,677)(0.1)}{2.8\times10^{7}}
= \frac{5471}{2.8\times10^{7}}$$

$$\boxed{S = 1.95\times10^{-4}}$$

Tus apuntes traen 0.00019 ✓ (el factor $4u/(r^2/t) = 1.43\times10^{-8}$ que
anotaste también está bien).

**Paso 4 — Plausibilidad.** $S \approx 2\times10^{-4}$ está en el rango de
acuífero confinado ($10^{-5}$ a $10^{-3}$) ✓. Y
$T = 13\,677\ \mathrm{ft^2/día} = 1271\ \mathrm{m^2/día}$, un acuífero muy
productivo.

**Paso 5 — Radio de influencia a 240 min** ($t = 0.1667$ día):

$$R_0 = 1.5\sqrt{\frac{T\,t}{S}}
= 1.5\sqrt{\frac{13\,677\,(0.1667)}{1.95\times10^{-4}}}
= 1.5\,(3415) = \boxed{5123\ \mathrm{ft}}$$

> **Sobre el "$2\sqrt{Tt/S}$" de tus apuntes.** Aparecen dos versiones en la
> literatura: $R_0 = 1.5\sqrt{Tt/S}$ (que es $\sqrt{2.25\,Tt/S}$, la que sale de
> extrapolar la recta de Cooper-Jacob hasta $s=0$) y $R_0 = 2\sqrt{Tt/S}$ (un
> criterio algo más conservador). Dan 5123 ft y 6831 ft. **Usa la que haya dado
> tu profesor y di cuál usaste**; la diferencia es el criterio, no la física.

## 11.G — Superposición de dos pozos (página 9)

**Enunciado.** $T = 100$ m²/día, $S = 1\times10^{-4}$. Dos pozos:
$Q_1 = 20$ L/s y $Q_2 = 50$ L/s. Punto de observación a $r = 50$ m de cada uno.
$t = 12$ h. Hallar el abatimiento total.

**Paso 1 — Unidades.**

$$t = 12\ \mathrm{h} = 0.5\ \mathrm{día}$$

$$Q_1 = 20\ \mathrm{L/s}\times86.4 = 1728\ \mathrm{m^3/día}
\qquad
Q_2 = 50\times86.4 = 4320\ \mathrm{m^3/día}$$

(El factor 86.4 convierte L/s a m³/día: vale la pena memorizarlo.)

**Paso 2 — El término logarítmico (es el mismo para los dos pozos, porque $r$ es
el mismo).**

$$\Lambda = \ln\!\left(\frac{2.25\,T\,t}{r^{2}S}\right)
= \ln\!\left(\frac{2.25\,(100)(0.5)}{(50)^{2}(1\times10^{-4})}\right)
= \ln\!\left(\frac{112.5}{0.25}\right) = \ln(450)$$

$$\Lambda = 6.109$$

**Paso 3 — El denominador.**

$$4\pi T = 4\pi\,(100) = 1256.6\ \mathrm{m^2/día}$$

**Paso 4 — Abatimiento de cada pozo.**

$$s_1 = \frac{Q_1}{4\pi T}\Lambda = \frac{1728}{1256.6}\,(6.109)
= (1.3752)(6.109) = \boxed{8.40\ \mathrm{m}}$$

$$s_2 = \frac{4320}{1256.6}\,(6.109) = (3.4380)(6.109) = \boxed{21.00\ \mathrm{m}}$$

**Paso 5 — Superposición.**

$$s_{total} = 8.40 + 21.00 = \boxed{29.40\ \mathrm{m}}$$

Los tres números coinciden con tus apuntes ✓

**Paso 6 — Radio de influencia.**

$$R_0 = 1.5\sqrt{\frac{Tt}{S}} = 1.5\sqrt{\frac{100\,(0.5)}{10^{-4}}}
= 1.5\,(707) = \boxed{1061\ \mathrm{m}}$$

### G.1 Los "3 efectos" de tus apuntes

Tus apuntes listan tres cosas que se tratan **todas con superposición**:

| Efecto | Cómo se modela |
|---|---|
| **Otro pozo** | se suma su abatimiento: $s = \sum s_i$ |
| **Carga a nivel constante** (río, lago) | pozo imagen que **inyecta** $-Q$: se **resta** |
| **Barrera impermeable** (falla) | pozo imagen que **bombea** $+Q$: se **suma** |

**Extensión del ejercicio.** Si hay una frontera a $d = 200$ m del punto (ese
parece ser el papel del "d = 200 m" de tus apuntes), el pozo imagen queda a
$2(200) = 400$ m del punto:

$$s_{imagen,1} = \frac{1728}{1256.6}\ln\!\left(\frac{2.25(100)(0.5)}{(400)^2(10^{-4})}\right)
= 2.68\ \mathrm{m}$$

$$s_{imagen,2} = \frac{4320}{1256.6}\,(1.951) = 6.70\ \mathrm{m}$$

| Caso | Cálculo | Resultado |
|---|---|---|
| Sin frontera | 29.40 | **29.40 m** |
| Barrera impermeable | $29.40 + 9.39$ | **38.79 m** |
| Río (carga constante) | $29.40 - 9.39$ | **20.02 m** |

La barrera agrava el abatimiento un 32 %; el río lo alivia un 32 %.

## 11.H — Mapa de isopiezas: elevaciones de pozos y gradientes (Figura 3.31)

**Enunciado (página 6 de tus apuntes).** Los puntos negros de la figura 3.31 son
pozos que llegan al nivel freático. Con las curvas de nivel freático, estimar la
elevación del nivel freático en cada pozo con precisión de 0.1 m. Calcular los
valores mayor y menor del gradiente hidráulico.

![**Figura H1.** Tu mapa con las mediciones que hiciste en clase. En rojo, el gradiente máximo; en verde, el mínimo; en azul, la interpolación de un pozo.](fig/fig_c6_mapa331.png){width=15.8cm}

### Paso 1 — Leer el mapa antes de medir

1. **Las curvas van de 1 en 1 metro**, de 17 m a 23 m. La de **17 m** está junto
   al borde norte, donde sale el río; la de **23 m** es la curva exterior del sur.
2. **El río corre hacia el norte**, hacia la curva más baja.
3. **Las curvas forman una V al cruzar el río, y la V apunta aguas arriba** (hacia
   el sur). Eso indica un **río ganador**: el acuífero le entrega agua (ver
   sección J). El pie de la figura del libro lo dice: las curvas forman una V
   donde cruzan un río.
4. **La 22 m es la curva que rodea toda la cuenca**: baja desde el borde norte por
   la derecha, gira hacia el oeste a lo largo del sur, cruza los dos afluentes y
   sube por la izquierda.

### Paso 2 — Calibrar la escala con la regla

La barra de escala de 0 a 1000 m mide **unos 40 mm** en tu copia. Lo comprobé con
tu propia medición: el espaciamiento que anotaste como 25 mm corresponde en la
figura a la misma distancia que 630 m de la barra.

$$1\ \mathrm{mm} \approx 25\ \mathrm{m}$$

> **Hazlo siempre primero**: mide la barra de escala con la regla. Si tu copia
> está a otra escala (fotocopia ampliada, por ejemplo), el factor cambia, pero el
> método es el mismo.

### Paso 3 — Interpolar la elevación de un pozo

El pozo queda entre dos curvas. Traza por el pozo una línea **perpendicular** a
las curvas y mide dos distancias:

- $d$: del pozo a la curva **inferior**.
- $D$: entre las dos curvas, a lo largo de la misma línea.

$$\boxed{h_{pozo} = h_{inferior} + \Delta h\,\frac{d}{D}}
\qquad \Delta h = 1\ \mathrm{m}$$

**Pozo del sur (el que mediste en clase).** Está entre 22 y 23 m. Medidas: 13 mm
desde la curva de 22 m y 25 mm entre curvas.

$$h = 22 + 1\times\frac{13}{25} = 22 + 0.52 = \boxed{22.5\ \mathrm{m}}$$

**Pozo junto a la curva de 22 m** (el de la nota "25 mm"). Queda casi encima de la
curva, a unos 2 mm por debajo, con 25 mm de separación hasta la de 23 m:

$$h \approx 22 + \frac{2}{25} = \boxed{22.1\ \mathrm{m}}$$

**Pozo del sureste** (tu nota "4 mm / 20 mm"). Está a 4 mm de la curva de 23 m,
con 20 mm entre curvas. Aquí conviene medir desde la curva **superior** y
restar:

$$h = 23 - \frac{4}{20} = 23 - 0.2 = \boxed{22.8\ \mathrm{m}}$$

> **Los demás pozos se hacen igual** sobre tu copia. La foto que me pasaste tiene
> perspectiva, así que no puedo medir 0.1 m con fiabilidad en los otros. Lo que sí
> puedes comprobar sin regla: **cada valor tiene que quedar entre las dos curvas
> que encierran el pozo**. Si un pozo está entre 20 y 21 m y te da 21.3, midiste
> mal.

### Paso 4 — Gradientes mayor y menor

$$i = \frac{\Delta h}{L}$$

con $L$ la distancia **perpendicular** entre dos curvas consecutivas. Como
$\Delta h = 1$ m siempre, el gradiente es mayor donde las curvas están más juntas.

Tus mediciones, convertidas con 1 mm ≈ 25 m:

| Lugar | Separación medida | $L$ (m) | $i$ |
|---|---|---|---|
| **17–18 m, junto a la salida del río** | **4 mm** | **100** | **0.010** |
| 18–19 m | 5 mm | 125 | 0.0080 |
| 19–20 m | 6 mm | 150 | 0.0067 |
| 20–21 m | 12 mm | 300 | 0.0033 |
| 21–22 m | 20 mm | 500 | 0.0020 |
| **22–23 m, al sur** | **25 mm** | **630** | **0.0016** |

$$\boxed{i_{max} \approx 1.0\times10^{-2}}
\qquad\qquad
\boxed{i_{min} \approx 1.6\times10^{-3}}$$

El gradiente máximo es unas **seis veces** el mínimo.

**La explicación física (va en la respuesta).** Todo el flujo de la cuenca
converge hacia el río y sale por el norte. Cerca de la salida, el mismo caudal
tiene que pasar por una sección cada vez más estrecha, así que necesita más
gradiente. Es la misma idea de la Parte 3 de esta guía: curvas juntas
indican gradiente alto; curvas separadas, gradiente bajo. Si el acuífero fuera
heterogéneo, la separación también podría reflejar cambios de $K$, pero aquí la
causa dominante es la geometría del flujo.

## 11.I — Cargas en una sección con río y lago (Figura 7.39)

**Enunciado (página 7 de tus apuntes).** Las líneas discontinuas son
equipotenciales y las cargas están en metros.

a. Completar las cargas en los puntos A a F.
b. Marcar con R un lugar donde haya recarga.
c. Marcar con D un lugar donde haya descarga.
d. Dibujar líneas de flujo que empiecen en X, Y y Z.

![**Figura I1.** La figura 7.39 resuelta: cargas de A a F, zonas de recarga (R) y descarga (D), y las tres líneas de flujo pedidas.](fig/fig_c5_fig739.png){width=15.8cm}

### Paso 1 — Leer bien la figura

**La foto está inclinada unos 3.5°.** Por eso el eje derecho parece desplazado
5 m respecto al izquierdo: los dos ejes son iguales, pero en la foto una línea
horizontal aparece inclinada. **Lee cada punto con el eje que tenga más cerca.**

**La clave del problema:** las equipotenciales no tienen el valor escrito. Se
obtiene con la condición del nivel freático de esta guía:

$$\text{en el nivel freático: } h = z$$

Así que **el valor de cada equipotencial es la elevación del punto donde corta el
nivel freático**. Al leerlas así se ve que van **cada 2.5 m**: 2.5, 5, 7.5, 10,
12.5 y 15 m.

Para cada punto:

$$h_{total} = \text{valor de la equipotencial que pasa por el punto}$$

$$z = \text{elevación del punto}
\qquad\qquad
h_p = h_{total} - z$$

### Paso 2 — La tabla resuelta

| Punto | Elevación $z$ (m) | Presión $h_p$ (m) | Total $h$ (m) | Razonamiento |
|---|---|---|---|---|
| **A** | ≈ 12.5 | **0** | ≈ 12.5 | está sobre el nivel freático: $h_p = 0$ y $h = z$ |
| **B** | ≈ −7.5 | ≈ 10 | ≈ 2.5 | sobre la equipotencial en forma de cuenco bajo el río, que corta el nivel freático a ≈ 2.5 m |
| **C** | ≈ −5 | ≈ 10 | **5** | fondo del lago. El lago está a 5 m y su fondo es equipotencial; $h_p$ es la profundidad del agua |
| **D** | ≈ −7 | ≈ 15 | ≈ 8 | equipotencial que corta el nivel freático justo a la derecha de E, a ≈ 8 m |
| **E** | ≈ 5 | **0** | **5** | orilla del lago: al nivel del lago y a presión atmosférica |
| **F** | ≈ −2 | ≈ 14.5 | ≈ 12.5 | equipotencial que corta el nivel freático en la ladera derecha a ≈ 12.5 m |

Las lecturas sobre la foto tienen una incertidumbre de unos ±0.5 m. En el examen,
escribe que las leíste de la figura.

**Dos comprobaciones rápidas:**

- En C, $h_p = 5 - (-5) = 10$ m, que es **la profundidad del lago en ese punto**.
  Así debe ser, porque dentro del lago la presión es hidrostática.
- En D, $h = 8$ m es **mayor** que el nivel del lago (5 m). El agua bajo el lago
  tiene más carga que el lago, de modo que sube hacia él: **el lago es una zona
  de descarga.** Lo mismo pasa con B bajo el río (2.5 m frente a ≈ 1.7 m del
  río).

### Paso 3 — Recarga (R) y descarga (D)

**El criterio, que es lo que se evalúa:**

| Zona | Cómo se reconoce | En la figura 7.39 |
|---|---|---|
| **Recarga** | la carga **disminuye** con la profundidad; el flujo baja | las cimas: bajo X, la colina central y junto a Z |
| **Descarga** | la carga **aumenta** con la profundidad; el flujo sube | el valle del río y el lago |

Basta con marcar una de cada una, pero marcar todas demuestra que entendiste el
criterio.

### Paso 4 — Líneas de flujo desde X, Y y Z

Las tres reglas de la Parte 5 de esta guía:

1. Las líneas de flujo cortan las equipotenciales **a 90°**.
2. Van de **mayor a menor** carga.
3. Terminan en una zona de **descarga**.

| Desde | Recorrido | Termina en |
|---|---|---|
| **X** | baja casi vertical junto a la divisoria izquierda, gira hacia la derecha por debajo del cuenco de B y sube | el **río** |
| **Y** | Y está en la ladera izquierda de la colina central, a la izquierda de la divisoria (la cima). Baja hacia la izquierda y sube | el **río** (sistema local, recorrido corto) |
| **Z** | baja junto a la divisoria derecha, pasa por debajo de la ladera derecha y sube por debajo del lago | el **lago** (recorrido más largo y profundo) |

> **El detalle que hace la respuesta completa.** Y no va al lago aunque esté en la
> colina que lo separa del río: lo que decide hacia dónde va es **de qué lado de
> la divisoria** está, y Y está del lado del río. Si hubiera un punto a la derecha
> de la cima de esa colina, su línea de flujo iría al lago.

## 11.J — Taller en clase: ríos ganadores y perdedores (página 5)

Tu foto del tablero tiene dos casos rotulados "GANADOR" y "PERDEDOR", con el
perfil y la vista en planta de cada uno.

![**Figura J1.** Lo del tablero, redibujado. Arriba, el perfil; abajo, cómo se ven las curvas en planta.](fig/fig_c3_rios.png){width=15.8cm}

| | **Río ganador** (*gaining*) | **Río perdedor** (*losing*) |
|---|---|---|
| Posición del nivel freático | **por encima** del nivel del río | **por debajo** del nivel del río |
| Sentido del flujo | del acuífero **hacia el río** | del río **hacia el acuífero** |
| Zona | **descarga** | **recarga** |
| Curvas en planta | la V apunta **aguas arriba** | la V apunta **aguas abajo** |
| Clima típico | húmedo; el río sigue corriendo en época seca (flujo base) | árido; el río se seca río abajo |

**La regla de la V, que es lo que se pregunta.** Cerca de un río ganador, el nivel
freático baja hacia el río, de modo que las curvas se "meten" hacia aguas arriba
siguiendo el cauce. En un río perdedor, el río está alto y mantiene el nivel
freático elevado a lo largo del cauce, así que las curvas se doblan hacia aguas
abajo.

**Aplicación directa.** En la figura 3.31 la V apunta aguas arriba, así que el río
es ganador. Eso concuerda con que los gradientes sean máximos cerca del río: todo
el flujo converge a él.

## 11.K — Otros conceptos de tus apuntes

### K.1 La analogía canal–tubería (página 2)

Tus apuntes la anotan en dos líneas:

| | Acuífero **libre** | Acuífero **confinado** |
|---|---|---|
| Analogía | **canal** abierto | **tubería** a presión |
| Carga | $h = z$ (en el nivel freático) | $h = z + p/\gamma$ |
| Almacenamiento | $S_y$, por **drenaje** de poros | $S_s b$, por **compresión** del agua y la matriz |
| Valores típicos | $S_y = 0.05$–$0.30$ | $S = 10^{-5}$–$10^{-3}$ |

En un canal, el agua que sale es la que "se vacía" al bajar el nivel. En una
tubería no se vacía nada: el agua sale porque baja la presión y el sistema se
descomprime. Esa diferencia explica los cuatro órdenes de magnitud entre $S_y$ y
$S$.

### K.2 Recarga, goteo y "agua salta" (página 1)

![**Figura K1.** El dibujo de la página 1 de tus apuntes, redibujado: acuífero confinado que se recarga en su afloramiento, goteo a través de la capa confinante y pozo surgente.](fig/fig_c4_artesiano.png){width=15.8cm}

- **Recarga:** el acuífero confinado se recarga donde **aflora** en superficie,
  aguas arriba.
- **Superficie (nivel) potenciométrica:** la superficie imaginaria hasta donde
  subiría el agua en pozos que llegan al acuífero confinado. Corresponde a la
  carga $h$.
- **"Agua salta" (pozo surgente):** si la superficie potenciométrica está **por
  encima del terreno**, el agua sale sola del pozo, sin bomba. Si está por encima
  del techo del acuífero pero por debajo del terreno, el pozo es artesiano pero no
  surgente.
- **Goteo:** el paso de agua a través de la capa confinante, que no es
  perfectamente impermeable. Es la fuga del ejercicio 3.17 del taller y el
  fenómeno de los **acuíferos semiconfinados** (sección B.6).
- **$S_s \sim 10^{-3}$ a $10^{-6}\ \mathrm{m^{-1}}$**, el rango que anotaste.

### K.3 El tensor de conductividad (página 1)

Tus apuntes escriben $q = -K\nabla h$ con tres componentes $K_{xx}$, $K_{yy}$,
$K_{zz}$, y agrupan $K_{xx}$ y $K_{yy}$ como $K_h$. Es decir, en un medio
estratificado las dos direcciones horizontales se tratan igual ($K_h$) y la
vertical es distinta ($K_v = K_{zz}$). Es exactamente la Parte 3 de la Guía
Maestra: $K_h$ con media aritmética, $K_v$ con media armónica.

## 11.L — Erratas que encontré en tus apuntes

Conviene que las corrijas antes del parcial para no memorizarlas mal.

| Página | Dice | Debe decir | Por qué |
|---|---|---|---|
| 2 | $D_H = S/T$ | $D_H = T/S$ | una difusividad tiene unidades de m²/día; $S/T$ daría día/m² |
| 2 | $q = K\dfrac{d^2h^2}{dx^2} - W = 0$ | $\dfrac{K}{2}\dfrac{d^2(h^2)}{dx^2} + W = 0$ | falta el factor 1/2 y el signo de $W$. La fórmula final de $h^2$ que copiaste sí es correcta |
| 8 | $T = 13\,667$ ft²/día | $T = 13\,677$ ft²/día | error de un dígito al copiar |
| 4 | "la cuña avanza −39.1 m" | la punta se mueve −39.1 m, pero la cuña avanza +6.1 m respecto a la costa | 33 m de los 39 son la costa que retrocede (sección D.6) |

En la página 8 aparece $2\sqrt{Tt/S}$ como radio de influencia y en la página 9
$1.5\sqrt{Tt/S}$. **No es un error**: son dos criterios distintos (sección F).
Usa el que haya usado tu profesor y di cuál.

Y una aclaración sobre el ejemplo de Dupuit: $S_y = 0.27$ y $b = 30$ m **no
intervienen** en el cálculo de régimen permanente. Puede que el profesor los dé
para despistar, o para una pregunta adicional de régimen transitorio.

## 11.M — Ejercicios para practicar los temas nuevos

### M.1 Enunciados

**P11.1 — Dupuit con recarga.** Un acuífero libre de 500 m de longitud está entre
dos canales con niveles $h_1 = 12$ m (en $x = 0$) y $h_2 = 10$ m (en $x = L$).
$K = 5$ m/día y la recarga es $W = 400$ mm/año.

a. Calcula $q'$ en los dos bordes e indica hacia dónde sale el agua.
b. Verifica el balance de masa.
c. ¿Existe divisoria? Calcula $d$ y $h_{max}$.
d. ¿Por debajo de qué recarga desaparece la divisoria?

**P11.2 — Costa con cambio climático.** Usa el acuífero costero de la sección D
($L_0 = 1000$ m, $s_0 = 30$ m, $K = 10^{-4}$ m/s, $W = 500$ mm/año), pero con un
escenario más severo: el mar sube 1.0 m, la pendiente de la playa es del 1 % y la
erosión costera es de 5 m.

a. Calcula el retroceso de la costa y los nuevos $L$ y $s$.
b. Calcula $x_T$ antes y después, y el avance **real** de la cuña.
c. Calcula cuánto sube el nivel freático en $x = 10$ m.
d. ¿Sube o baja el nivel freático **respecto al mar**? ¿Qué implica según
   Ghyben-Herzberg?

**P11.3 — Corrección barométrica.** Un pozo en un acuífero confinado tiene
eficiencia barométrica $BE = 0.6$.

a. Si la presión atmosférica sube 2.5 kPa, ¿cuánto y en qué sentido cambia el
   nivel del pozo?
b. ¿Cuál es la eficiencia de marea?
c. Con una marea de 0.8 m, ¿cuánto oscila el pozo?

**P11.4 — Almacenamiento libre contra confinado.** Un acuífero libre tiene
$S_y = 0.15$, $S_s = 2\times10^{-5}$ m⁻¹ y $b = 80$ m. El nivel baja 2 m en un
área de 3 km².

a. Calcula $S$.
b. Calcula el volumen liberado y separa cuánto viene del drenaje y cuánto de la
   descompresión.
c. Si el acuífero fuera confinado con el mismo $S_s$ y $b$, ¿cuánta agua liberaría?

### M.2 Respuestas

**P11.1**
a. $W = 1.095\times10^{-3}$ m/día. Término de carga $= 0.220$ m²/día;
   $WL/2 = 0.274$ m²/día. $q'(0) = 0.220 - 0.274 = \mathbf{-0.054}$ m²/día
   (sale hacia el canal 1) y $q'(L) = 0.220 + 0.274 = \mathbf{+0.494}$ m²/día
   (sale hacia el canal 2).
b. Salidas $0.054 + 0.494 = 0.548$ m²/día $= WL$ ✓
c. **Sí existe**: domina la recarga (0.274 > 0.220). $d = \mathbf{49.1}$ m, muy
   cerca del canal 1, y $h_{max} = \mathbf{12.02}$ m, apenas 2 cm sobre $h_1$.
d. La divisoria desaparece cuando $|W| < 2\times0.220/500$, es decir por debajo
   de **321 mm/año**.

**P11.2**
a. $\Delta L = -1.0/0.01 - 5 = \mathbf{-105}$ m; $L_f = \mathbf{895}$ m;
   $s_f = \mathbf{31.0}$ m.
b. $C = 161.7$. $x_{T0} = \mathbf{924.4}$ m; $x_{Tf} = \mathbf{803.5}$ m
   ($\Delta x_T = -120.9$ m). Longitud invadida: de 75.6 a 91.5 m, un **avance
   real de 15.9 m**.
c. $H(10)$ pasa de 32.877 a 33.346 m: **sube 0.47 m**.
d. Respecto al mar, el nivel freático **baja** de 2.88 a 2.35 m (0.53 m menos).
   Como el espesor de agua dulce bajo el mar es 40 veces esa altura, se pierden
   unos 21 m de agua dulce en profundidad. Por eso la cuña avanza.

**P11.3**
a. $\Delta P/\gamma_w = 2.5/9.81 = 0.255$ m; $\Delta h = 0.6\times0.255 =$
   **0.153 m de bajada** (15.3 cm).
b. $TE = 1 - 0.6 = \mathbf{0.40}$.
c. $0.40\times0.8 = \mathbf{0.32}$ m.

**P11.4**
a. $S = 0.15 + (2\times10^{-5})(80) = 0.15 + 0.0016 = \mathbf{0.1516}$.
b. $V = 0.1516\times(3\times10^{6})\times2 = \mathbf{909\,600}$ m³: 900 000 m³ por
   drenaje (99 %) y 9 600 m³ por descompresión (1 %).
c. Sólo $S_sb$: **9 600 m³**, unas 94 veces menos.

## 11.N — Qué cambia en tu plan de estudio

Tus apuntes muestran que en clase se trabajaron **Dupuit con recarga** y el
**acuífero costero con cambio climático**, con datos concretos. Eso los vuelve
candidatos fuertes para el parcial, junto con la prueba de bombeo.

| Prioridad | Tema | Tiempo extra | Sección |
|---|---|---|---|
| **Alta** | Acuífero costero con cambio climático | 40 min | D |
| **Alta** | Dupuit con recarga ($q'$, $d$, $h_{max}$) | 30 min | B.4 y C |
| Media | Cargas en una sección (figura 7.39) | 20 min | I |
| Media | Mapa de isopiezas y gradientes (figura 3.31) | 15 min | H |
| Media | $S = S_y + S_sb$, ríos ganadores y perdedores, corrección barométrica | 15 min | B.1, J, B.5 |
| Baja | Bessel, Laplace, capilaridad (lectura) | 10 min | B.6, B.7 |

**Lo que no cambia:** la prueba de bombeo sigue siendo el bloque más probable, y
tus apuntes lo confirman (Thiem, Theis, superposición e imágenes aparecen en las
páginas 8 y 9). Los resultados de tus apuntes en ese tema coinciden con los de la
Guía Maestra.

**Si sólo tienes una hora para este complemento:** haz la sección D completa (el
problema costero) y la sección C hasta el Paso 5. Son los dos ejercicios que
el profesor resolvió en clase.


# ANEXO A — Tabla de la función de pozo $W(u)$

| $u$ | $W(u)$ | $u$ | $W(u)$ | $u$ | $W(u)$ |
|---|---|---|---|---|---|
| $1\times10^{-9}$ | 20.15 | $1\times10^{-6}$ | 13.24 | $1\times10^{-3}$ | 6.332 |
| $2\times10^{-9}$ | 19.45 | $2\times10^{-6}$ | 12.55 | $2\times10^{-3}$ | 5.639 |
| $5\times10^{-9}$ | 18.54 | $5\times10^{-6}$ | 11.63 | $5\times10^{-3}$ | 4.726 |
| $1\times10^{-8}$ | 17.84 | $1\times10^{-5}$ | 10.94 | $1\times10^{-2}$ | 4.038 |
| $2\times10^{-8}$ | 17.15 | $2\times10^{-5}$ | 10.24 | $2\times10^{-2}$ | 3.355 |
| $5\times10^{-8}$ | 16.23 | $5\times10^{-5}$ | 9.326 | $5\times10^{-2}$ | 2.468 |
| $1\times10^{-7}$ | 15.54 | $1\times10^{-4}$ | 8.633 | $1\times10^{-1}$ | 1.823 |
| $2\times10^{-7}$ | 14.85 | $2\times10^{-4}$ | 7.940 | $2\times10^{-1}$ | 1.223 |
| $5\times10^{-7}$ | 13.93 | $5\times10^{-4}$ | 7.024 | $5\times10^{-1}$ | 0.560 |
|  |  |  |  | $1$ | 0.219 |

**Si no tienes la tabla:** para $u < 0.01$,

$$W(u) \approx -0.5772 - \ln u = \ln\frac{0.5615}{u}$$

Con $u = 10^{-3}$ da 6.331 contra 6.332 de la tabla: error del 0.02 %.

# ANEXO B — Las 20 trampas que cuestan el parcial

| # | Error | Cómo evitarlo |
|---|---|---|
| 1 | Mezclar minutos con días | Convierte **todo** a días al principio. $t_0$ en minutos da error de 1440× |
| 2 | Confundir $q$ con $v$ | $q$ = caudal/área total; $v = q/n_e$ es la real. Como $n_e<1$, $v > q$ |
| 3 | Omitir el signo menos de Darcy | El gradiente apunta a carga **creciente**; el flujo va al revés |
| 4 | Dar la dirección de $\nabla h$ como dirección del flujo | Invierte el azimut 180° |
| 5 | Medir $\Delta s$ entre dos puntos cualesquiera | Un **ciclo completo**, o divide por $\log(t_2/t_1)$ |
| 6 | Usar $2\pi$ en tiempo–abatimiento o $4\pi$ en distancia | Tiempo → $4\pi$. Distancia → $2\pi$ |
| 7 | No verificar $u<0.01$ | Si los puntos tardíos no cumplen, usa Theis |
| 8 | Trazar la recta por los puntos iniciales | Los primeros **siempre** se curvan; se descartan |
| 9 | Esperar $S$ de una recuperación | Imposible: la recta pasa por el origen |
| 10 | Esperar $S$ de régimen permanente | Tampoco: sin tiempo no hay almacenamiento |
| 11 | Usar $s$ en acuífero libre | Dupuit va con $h^2$, medido **desde la base** |
| 12 | Confundir $T$ con $K$ | $T = Kb$. Si dan el espesor, casi siempre quieren la conversión |
| 13 | Confundir $K_h$ (aritmética) con $K_v$ (armónica) | $K_h$ la domina la **mejor** capa; $K_v$ la **peor** |
| 14 | Usar $K_h$ en vez de $\sqrt{K_hK_v}$ en red anisótropa | Media **geométrica** |
| 15 | $1\ \mathrm{m^2} = 10^2\ \mathrm{cm^2}$ | Son $10^{4}$: las áreas van al cuadrado |
| 16 | Área transversal frente a área en planta | Horizontal → espesor×ancho. Fuga vertical → longitud×ancho |
| 17 | Calcular $h_p$ sin la parte artesiana | Es la **altura total** de columna sobre el punto |
| 18 | Creer que excavar baja $u$ | $u$ la fija el acuífero, no la excavación |
| 19 | Olvidar la superposición | Si hay más de un pozo, **suma** |
| 20 | Signo del pozo imagen | Impermeable → **suma**. Río → **resta** |

## Rangos para el paso de "¿tiene sentido?"

| Material | $K$ (m/s) | | Parámetro | Rango |
|---|---|---|---|---|
| Grava | $10^{-2}$–1 | | $S$ confinado | $10^{-5}$–$10^{-3}$ |
| Arena limpia | $10^{-5}$–$10^{-2}$ | | $S_y$ libre | 0.05–0.30 |
| Arena fina, limo | $10^{-8}$–$10^{-5}$ | | $n_e$ roca fracturada | $10^{-5}$–$10^{-2}$ |
| Arcilla | $<10^{-8}$ | | Gradiente regional | $10^{-4}$–$10^{-2}$ |

# ANEXO C — Respuestas de los ejercicios propuestos

Compara sólo después de intentarlos.

## P1.1 — Leer una recta

a. $\log_{10}(1000/10) = 2$ ciclos.
b. $\Delta s = (1.55-0.35)/2 = \mathbf{0.60}$ m por ciclo.
c. $t_0 = 10\times10^{-0.35/0.60} = 10\times10^{-0.5833} = \mathbf{2.61}$ min
   $= 1.81\times10^{-3}$ días.
d. $T = 2.303(2000)/(4\pi\cdot0.60) = 4606/7.540 = \mathbf{611}$ m²/día.
   $S = 2.25(611)(1.81\times10^{-3})/60^{2} = 2.488/3600 = \mathbf{6.9\times10^{-4}}$.
e. $K = 611/18 = \mathbf{33.9}$ m/día $= 3.9\times10^{-4}$ m/s → **arena limpia a
   arena gruesa**.

## P1.2 — Escala

a. $100\log_{10}(6.5) = \mathbf{81.3\ \%}$.
b. $1000\times10^{0.25} = \mathbf{1778}$.
c. $\sqrt{100\times1000} = \mathbf{316}$ (media geométrica, no 550).
d. $5\times10^{2.3} = 5\times199.5 = \mathbf{998}$ min.

## P2.1 — Darcy

a. $q = (2.5\times10^{-5})(0.004) = \mathbf{1.0\times10^{-7}}$ m/s $= 8.64\times10^{-3}$ m/día.
b. $Q = qA = \mathbf{1.2\times10^{-5}}$ m³/s $= \mathbf{1.04}$ m³/día.
c. $v = q/n_e = 1.0\times10^{-7}/0.18 = 5.56\times10^{-7}$ m/s $= \mathbf{0.048}$ m/día.
d. $t = 500/0.048 = 10\,417$ días $= \mathbf{28.5}$ años.
e. $2.5\times10^{-5}$ m/s → **arena fina a media**.

## P2.2 — Piezómetro

a. $h = 450 - 12 = \mathbf{438}$ m.
b. $z = 450 - 180 = \mathbf{270}$ m.
c. $h_p = h - z = \mathbf{168}$ m.
d. Columna de agua $= 180 - 12 = 168$ m ✓ coincide.

## P3.1 — Cuatro capas

a. $K_h = [5(3\times10^{-4})+12(5\times10^{-7})+8(2\times10^{-4})+15(8\times10^{-6})]/40$
   $= (1.5\times10^{-3}+6\times10^{-6}+1.6\times10^{-3}+1.2\times10^{-4})/40
   = \mathbf{8.07\times10^{-5}}$ m/s.
   $K_v = 40/[5/3\times10^{-4}+12/5\times10^{-7}+8/2\times10^{-4}+15/8\times10^{-6}]$
   $= 40/(1.667\times10^{4}+2.4\times10^{7}+4\times10^{4}+1.875\times10^{6})
   = \mathbf{1.54\times10^{-6}}$ m/s.
b. $K_h/K_v = \mathbf{52.3}$.
c. $K_h$ la dominan las capas 1 y 3 (las de $10^{-4}$); $K_v$ la domina la capa 2
   (la de $5\times10^{-7}$), que aporta el 93 % de la resistencia vertical.
d. $T = K_h\sum b = (8.07\times10^{-5})(40) = \mathbf{3.23\times10^{-3}}$ m²/s
   $= 279$ m²/día.

## P3.2 — Tensor

a. $K_{yx} = 2\times10^{-4}/0.05 = \mathbf{4\times10^{-3}}$ cm/s.
b. La **simetría** del tensor: $K_{xy} = K_{yx}$.
c. $q_x = (4\times10^{-3})(0.02) = \mathbf{8\times10^{-5}}$ cm/s.
d. Que los ejes de coordenadas **no coinciden** con los ejes principales de
   anisotropía, por lo que $\mathbf{q}$ no es paralelo a $\nabla h$: el flujo se
   desvía respecto a la máxima pendiente.

## P4.1 — Almacenamiento

a. $V = (5\times10^{-4})(2\times10^{6})(1.5) = \mathbf{1500}$ m³.
b. $S = (1000)(9.81)(40)(0.25)(4.8\times10^{-10}) = \mathbf{4.71\times10^{-5}}$,
   el **9.4 %** del real.
c. $\beta_p = 5\times10^{-4}/(9810\cdot40) - (0.25)(4.8\times10^{-10})
   = 1.274\times10^{-9} - 1.20\times10^{-10} = \mathbf{1.15\times10^{-9}}$ m²/N.
   Verificación: $(9810)(40)(1.15\times10^{-9}+1.2\times10^{-10}) = 5.0\times10^{-4}$ ✓
d. El **90.6 %** proviene de la compactación de la matriz.

## P4.2 — Difusividad

a. $\nu = 250/4\times10^{-4} = \mathbf{6.25\times10^{5}}$ m²/día.
b. $t = (1000)^{2}/\nu = \mathbf{1.60}$ días $= 38.4$ horas.
c. 100 m → 0.016 días; 2000 m → 6.40 días. El tiempo escala con el **cuadrado**
   de la distancia.
d. Que el radio de influencia crece con $\sqrt{t}$: cuadruplicar el tiempo sólo
   duplica el radio. El cono se expande cada vez más despacio.

## P5.1 — Red de flujo

a. $Q = (2\times10^{-4})(15)(4/12) = \mathbf{1.0\times10^{-3}}$ m³/s por m.
b. $Q_{total} = (1.0\times10^{-3})(80) = \mathbf{0.080}$ m³/s $= \mathbf{6912}$ m³/día.
c. $i = 15/60 = \mathbf{0.25}$.
d. $Q$ **disminuiría**: al alargar la pantalla aumenta el recorrido, por tanto
   aumenta $n_d$ mientras $n_f$ se mantiene, y $Q = KH\,n_f/n_d$ baja.

## P5.2 — Anisotropía

a. $K_{eq} = \sqrt{(4\times10^{-4})(1\times10^{-5})} = \mathbf{6.32\times10^{-5}}$ m/s.
b. $x' = x\sqrt{K_v/K_h} = \mathbf{0.158}\,x$.
c. $\sqrt{K_h/K_v} = \mathbf{6.32 : 1}$ (rectángulos muy alargados).
d. **No.** La ortogonalidad sólo se cumple en la sección transformada, o cuando el
   flujo coincide con un eje principal de anisotropía.

## P6.1 — Esfuerzo efectivo (unidades inglesas)

a. $h_p = 40+15 = 55$ ft. $\sigma_T = (120)(40) = \mathbf{4800}$ lb/ft².
   $u = (62.4)(55) = \mathbf{3432}$ lb/ft². $\sigma' = \mathbf{1368}$ lb/ft².
   $FS = \mathbf{1.40}$.
b. $d_{crit} = (4800-3432)/(120-62.4) = 1368/57.6 = \mathbf{23.75}$ ft.
c. $d_{crit} = 40 - 3432/120 = 40-28.6 = \mathbf{11.40}$ ft.
d. Con $d=20$ ft en seco, $\sigma_T = (120)(20) = 2400$ lb/ft². Para $FS=1.3$ se
   necesita $u \le 2400/1.3 = 1846$ lb/ft², es decir
   $h_p \le 1846/62.4 = \mathbf{29.6}$ ft. Hay que bajar la carga de 55 a 29.6 ft:
   una despresurización de **25.4 ft**.

## P6.2 — Esfuerzo efectivo (métrico)

a. $h_p = 17$ m. $\sigma_T = (19.5)(12) = \mathbf{234}$ kPa.
   $u = (9.81)(17) = \mathbf{166.8}$ kPa. $\sigma' = \mathbf{67.2}$ kPa.
b. $FS = 234/166.8 = \mathbf{1.40}$.
c. Con agua: $d_{crit} = (234-166.8)/(19.5-9.81) = 67.2/9.69 = \mathbf{6.94}$ m.
   En seco: $d_{crit} = 12 - 166.8/19.5 = 12-8.55 = \mathbf{3.45}$ m.
d. Rellenar de agua **duplica** la profundidad alcanzable (6.94 frente a 3.45 m).
   En obra: excavar con draga o mantener la excavación inundada permite llegar al
   doble de profundidad sin despresurizar el acuífero.

## P7.1 — Cooper-Jacob completo

b. $\Delta s = \mathbf{0.571}$ m por ciclo; $t_0 = \mathbf{1.51}$ min
   $= 1.047\times10^{-3}$ días.
c. $T = 2.303(2500)/(4\pi\cdot0.571) = 5757.5/7.176 = \mathbf{803}$ m²/día.
   $S = 2.25(803)(1.047\times10^{-3})/80^{2} = 1.891/6400 = \mathbf{2.96\times10^{-4}}$.
d. $u = r^2S/4Tt$; con $t = 90$ min $= 0.0625$ d:
   $u = (6400)(2.96\times10^{-4})/(4\cdot803\cdot0.0625) = 9.4\times10^{-3} < 0.01$ ✓.
   Se cumple **desde $t = 90$ min**. Los puntos anteriores tienen $u>0.01$.
e. $K = 803/40 = \mathbf{20.1}$ m/día $= 2.3\times10^{-4}$ m/s → **arena limpia a
   arena gruesa**.

## P7.2 — Distancia–abatimiento

a. $u = r^2S/4Tt$ con $T=450$, $S=8\times10^{-4}$, $t=2$ d:
   $r=25$ → $1.4\times10^{-4}$ ✓; $r=75$ → $1.25\times10^{-3}$ ✓;
   $r=150$ → $5.0\times10^{-3}$ ✓; $r=250$ → $1.39\times10^{-2}$ ✗.
   **Usa los tres primeros.**
b. $\Delta s_r = \mathbf{1.464}$ m por ciclo de $r$; $r_0 = \mathbf{1598}$ m.
c. $T = 2.303(1800)/(2\pi\cdot1.464) = 4145/9.199 = \mathbf{451}$ m²/día.
   $S = 2.25(451)(2)/(1598)^{2} = 2030/2.554\times10^{6} = \mathbf{7.9\times10^{-4}}$.

## P7.3 — Thiem

a. $T = 2200\ln(150/15)/(2\pi(3.40-1.15)) = 2200(2.3026)/14.137 = \mathbf{358}$ m²/día.
   $K = 358/30 = \mathbf{11.9}$ m/día.
b. Porque en régimen permanente $\partial h/\partial t = 0$: **no hay cambio de
   almacenamiento**, así que $S$ no interviene en la ecuación y es imposible
   determinarlo.

## P8.1 — Cálculos en el acuífero

a. $u = (150)^{2}(3\times10^{-4})/(4\cdot800\cdot60) = 6.75/192\,000 = 3.52\times10^{-5}$;
   $W(u) = 9.68$; $s = [2500/(4\pi\cdot800)](9.68) = (0.2487)(9.68) = \mathbf{2.41}$ m.
b. $u = 6.25\times10^{-11}$, $W = 22.9$, $s_w = \mathbf{5.70}$ m.
   Capacidad específica $= 2500/5.70 = \mathbf{439}$ m³/día por m.
c. $R_0 = \sqrt{2.25(800)(60)/3\times10^{-4}} = \sqrt{3.6\times10^{8}} = \mathbf{18\,974}$ m.
d. Como $R_0\propto\sqrt{t}$, hay que **cuadruplicar** el tiempo:
   $t = \mathbf{240}$ días.

## P8.2 — Dos pozos

a. $r = 200$ m para cada uno. $u = (200)^{2}(3\times10^{-4})/(4\cdot800\cdot90)
   = 12/288\,000 = 4.17\times10^{-5}$; $W = 9.51$;
   $s_i = (0.1989)(9.51) = 1.892$ m. **Total $= \mathbf{3.78}$ m.**
   (Nota: $Q/4\pi T = 2000/(4\pi\cdot800) = 0.1989$.)
b. Sólo un pozo: $\mathbf{1.89}$ m. La interferencia **duplica** el abatimiento.
c. $R_0 = \sqrt{2.25(800)(90)/3\times10^{-4}} = \mathbf{23\,238}$ m, muchísimo
   mayor que la separación de 400 m: los conos se solapan **por completo**.
d. Como $s \propto Q$: $Q_{max} = 2000\,(3.0/3.78) = \mathbf{1587}$ m³/día por pozo.

## P9.1 — Upconing

a. $Q_{max} = 0.6\pi(5\times10^{-4})(25)^{2}(0.025) = \mathbf{1.47\times10^{-2}}$ m³/s
   $= \mathbf{14.7}$ L/s $= \mathbf{1272}$ m³/día.
b. El criterio es $z = 0.3d$, así que $z = 0.3(25) = \mathbf{7.5}$ m.
c. Como $Q_{max}\propto d^{2}$, duplicar el caudal exige $d\sqrt{2}$:
   $d = 25\sqrt{2} = \mathbf{35.4}$ m. Es decir, subir el fondo del pozo **10.4 m**.

## P9.2 — Cuña salina

a. $KG = (4\times10^{-3})(0.025) = 1\times10^{-4}$;
   $z(0) = q'/KG = 3\times10^{-4}/1\times10^{-4} = \mathbf{3.0}$ ft.
b. $x_{toe} = (1\times10^{-4})(120)^{2}/(2\cdot3\times10^{-4}) - 1.5
   = 1.44/6\times10^{-4} - 1.5 = 2400 - 1.5 = \mathbf{2398}$ ft.
c. Con $q' = 1.5\times10^{-4}$: $x_{toe} = 4800 - 0.75 = \mathbf{4799}$ ft.
   Se **duplica**, como debe ser.
d. $i = q'/(KB) = 3\times10^{-4}/(4\times10^{-3}\cdot120) = \mathbf{6.3\times10^{-4}}$.
   Está en el rango real de acuíferos costeros ($10^{-4}$–$10^{-3}$): **razonable** ✓

# ANEXO D — Plan de un día

> **Con tus apuntes revisados**, reserva **1 h 30** para la Parte 11, empezando por
> 11.D (costero) y 11.C (Dupuit con recarga). Si el tiempo no alcanza, recorta la
> Parte 9 y la Parte 4, que tienen menos probabilidad.

## Jornada completa (7 horas efectivas)

| Tiempo | Parte | Qué haces |
|---|---|---|
| 0:00–0:20 | 0 | Lee la orientación y el mapa de fórmulas. No memorices: ubícate |
| 0:20–1:10 | 1 | **Papel logarítmico.** Dibuja un papel semilog de 4 ciclos a mano. Haz los 3 ejemplos y P1.1, P1.2 |
| 1:10–2:00 | 2 | **Darcy.** Los 3 ejemplos y P2.1, P2.2 |
| 2:00–2:15 | — | **Descanso** |
| 2:15–3:45 | 7 | **Pruebas de bombeo.** El ejemplo 7.1 **con lápiz y papel**, luego 7.2 a 7.4. Después P7.1 |
| 3:45–4:45 | 8 | **Cálculos en el acuífero.** Los 4 ejemplos y P8.1, P8.2 |
| 4:45–5:00 | — | **Descanso** |
| 5:00–5:40 | 3 y 4 | $K_h/K_v$ y almacenamiento. Ejemplos 3.1, 4.2 y P3.1, P4.1 |
| 5:40–6:20 | 5 | **Redes de flujo.** Memoriza la tabla de las tres fronteras. Ejemplo 5.1 y P5.1 |
| 6:20–6:45 | 6 | **Esfuerzo efectivo.** El ejemplo 6.1 completo |
| 6:45–7:00 | 9, Anexo B | Costa en diagonal + releer las 20 trampas |

## Si sólo tienes 3 horas

| Tiempo | Qué |
|---|---|
| 0:00–0:30 | Parte 0 (las 6 ideas) + Parte 1 (papel semilog), ejemplo 1.2 |
| 0:30–1:45 | Parte 7: ejemplo 7.1 **rehecho a mano**, luego P7.1 |
| 1:45–2:30 | Parte 8: ejemplos 8.1 a 8.4 |
| 2:30–2:50 | Ejemplo 3.1 ($K_h$, $K_v$) + tabla de las tres fronteras |
| 2:50–3:00 | Mapa de fórmulas y Anexo B |

## Si sólo tienes 1 hora

Parte 0 (mapa de fórmulas), ejemplo 1.2 (leer la recta), ejemplo 7.1 (Cooper-Jacob
completo). Y memoriza estas cuatro:

$$q = -K\frac{dh}{dL}
\qquad v = \frac{q}{n_e}
\qquad T = \frac{2.303\,Q}{4\pi\,\Delta s}
\qquad S = \frac{2.25\,T\,t_0}{r^{2}}$$

# ANEXO E — Protocolo para el parcial

## Los primeros dos minutos, antes de escribir nada

1. **Lee todo el examen** y marca el problema de bombeo. Empieza por ese: es el
   que más vale y el que mejor sabes.
2. En el problema de bombeo, mira **qué variable acompaña al abatimiento**:
   ¿tiempo? → Cooper-Jacob. ¿distancia? → distancia–abatimiento ($2\pi$).
   ¿nada, ya estabilizado? → Thiem o Dupuit. ¿después de apagar? → recuperación.
3. **Convierte todos los tiempos a días.**
4. **Escribe las fórmulas antes de meter números.** Si te quedas sin tiempo, la
   fórmula correcta ya vale puntos.

## Veinte segundos de verificación al cerrar cada problema

- ¿Las unidades cuadran?
- ¿$u < 0.01$ si usé Cooper-Jacob?
- ¿$S$ entre $10^{-5}$ y $10^{-3}$ si el acuífero es confinado?
- ¿$K$ corresponde a un material real? **Nómbralo**: "arena limpia", "limo".
- ¿El balance de masa cierra, si había varios flujos?
- ¿El signo tiene sentido físico?

## Qué hacer si te bloqueas

**Dibuja.** El esquema del pozo con su cono te recuerda la geometría. La recta en
papel semilog te recuerda las dos fórmulas de Cooper-Jacob. El bloque de dos
acuíferos te recuerda que hay dos áreas distintas. Casi todo este curso se puede
reconstruir desde un dibujo, y un dibujo bien rotulado **también** vale puntos.

## Lo que siempre conviene escribir, aunque no lo pidan

1. **Las hipótesis** que usaste (temperatura para $\mu$, espesor para linealizar,
   criterio de $u$, conteos de la red).
2. **La verificación** de plausibilidad, con el nombre del material.
3. **El sentido físico** del resultado en una frase.

Una respuesta con hipótesis explícitas, método correcto y verificación vale más
que un número "exacto" sin justificación. Y si el número te sale mal por
aritmética, el método bien planteado te salva la mayor parte de la nota.

---

*Fuentes del material externo recomendado: curso libre de F. Javier Sánchez San
Román, Universidad de Salamanca (hidrologia.usal.es), que incluye vídeos y
ejercicios resueltos en español sobre la ley de Darcy, hidráulica de captaciones
y los métodos de Theis y Jacob. Los enunciados de la Parte 10 provienen de
Domenico & Schwartz,* Physical and Chemical Hydrogeology, *2.ª ed., Wiley (1997),
capítulos 3, 4 y 5.*

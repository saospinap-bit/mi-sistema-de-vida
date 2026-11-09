---
title: "Complemento de la Guía Maestra"
subtitle: "Todo lo que traen tus apuntes de clase, explicado y resuelto"
author: "Hidráulica Subterránea · Preparación para el parcial"
lang: es
toc: true
toc-title: "Contenido"
toc-depth: 2
---

# A — Qué encontré en tus apuntes y qué faltaba

Revisé las nueve páginas del PDF. Los apuntes son desordenados, pero tienen
**mucho más contenido del que yo había supuesto**: hay temas que no estaban en
la Guía Maestra y que además son muy "examinables". Este documento los cubre.

| Tema de los apuntes | ¿Estaba en la Guía Maestra? | Dónde está ahora |
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

# B — Los temas de teoría que faltaban

## B.1 El almacenamiento completo: $S = S_y + S_s\,b$

En la Guía Maestra traté el almacenamiento confinado ($S = S_s b$) y mencioné
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

### El ejemplo del Valle del Cauca (de tus apuntes)

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

## B.2 La ecuación de flujo sale del teorema de la divergencia

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

## B.3 Difusividad hidráulica

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
problema del canal de la Guía Maestra. Si reconoces ese grupo, los tres temas son
uno solo.

## B.4 Dupuit-Forchheimer: la hipótesis y las ecuaciones

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

### Flujo entre dos cuerpos de agua con recarga uniforme

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

## B.5 Correcciones barométrica y por marea

Esto aparece en tus apuntes (página 5) y **no estaba en la Guía Maestra**. Es un
tema clásico de preguntas conceptuales.

### El fenómeno

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

### Eficiencia barométrica

$$\boxed{BE = \frac{|\Delta h_{pozo}|}{\Delta P_{atm}/\gamma_w}}$$

Es adimensional, entre 0 y 1, y típicamente 0.20–0.75. La corrección de los datos
es

$$\boxed{h_{corregido} = h_{medido} + BE\;\frac{P_{atm} - P_{ref}}{\gamma_w}}$$

### Eficiencia de marea

$$\boxed{TE = \frac{\Delta h_{pozo}}{\Delta h_{marea}}}
\qquad\qquad
\boxed{BE + TE = 1}$$

La suma vale 1 porque las dos reparten la **misma** carga entre el esqueleto y el
agua: lo que una toma, la otra lo deja.

### Ejemplo numérico

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

## B.6 Por qué aparecen Bessel y Laplace

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

## B.7 Tensión superficial y capilaridad

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

# C — Dupuit con recarga: el ejemplo de tus apuntes resuelto

**Enunciado (datos de la página 2 de tus apuntes).**
$K = 10$ m/día, $S_y = 0.27$, $b = 30$ m, $h_1 = 15$ m, $h_2 = 18$ m,
$L = 200$ m. Dos casos de recarga: $W = -60$ mm/año y $W = +20$ mm/año.
Calcular $q'_1$, $q'_2$, $d$ y $h_{max}$.

## Paso 1 — Unidades (siempre primero)

$$W_A = -\frac{60\ \mathrm{mm/año}}{1000\times365.25}
= -1.643\times10^{-4}\ \mathrm{m/día}$$

$$W_B = +\frac{20}{1000\times365.25} = +5.476\times10^{-5}\ \mathrm{m/día}$$

El signo negativo del caso A significa **descarga neta** (evapotranspiración
mayor que la lluvia): el acuífero pierde agua por arriba.

## Paso 2 — El término de carga

$$h_1^{2}-h_2^{2} = 225 - 324 = -99\ \mathrm{m^2}$$

Es **negativo** porque $h_2 > h_1$: el nivel es más alto en el borde derecho, así
que el flujo global va de derecha a izquierda.

$$\frac{K(h_1^{2}-h_2^{2})}{2L} = \frac{10\,(-99)}{2(200)}
= -2.475\ \mathrm{m^2/día}$$

## Paso 3 — Caudales en los bordes

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

## Paso 4 — La divisoria

$$d = \frac{L}{2} - \frac{K}{W}\frac{(h_1^{2}-h_2^{2})}{2L}$$

**Caso A:** $K/W = 10/(-1.643\times10^{-4}) = -60\,876$

$$d = 100 - (-60\,876)\frac{-99}{400} = 100 - 15\,067 = -14\,967\ \mathrm{m}$$

**Caso B:** $K/W = 182\,648$

$$d = 100 - (182\,648)\frac{-99}{400} = 100 + 45\,200 = +45\,300\ \mathrm{m}$$

$$\boxed{\text{En los dos casos } d \notin [0,\,200]\ \mathrm{m}}$$

## Paso 5 — La conclusión (esto es la respuesta)

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

## Paso 6 — Variante donde sí hay divisoria (para que practiques $h_{max}$)

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

# D — El acuífero costero con cambio climático

Este es el ejercicio más completo de tus apuntes (páginas 3 y 4) y el que más
probabilidad tiene de caer, porque el profesor lo desarrolló en clase con datos
concretos. Combina Dupuit, Ghyben-Herzberg e intrusión salina.

## D.1 Los datos

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

## D.2 El sistema de coordenadas (si esto se confunde, todo sale mal)

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

## D.3 Las dos relaciones físicas de fondo

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

## D.4 Paso 1 — Unidades y la constante $C$

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

## D.5 Paso 2 — Cuánto retrocede la costa

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

## D.6 Pregunta 1 — ¿Cuánto avanza la cuña tierra adentro?

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

### Pero cuidado con interpretarlo: hay dos respuestas distintas

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

## D.7 Pregunta 2 — ¿Cuánto sube el nivel freático?

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

## D.8 Verificación independiente (hazla, blinda la respuesta)

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

## D.9 Resumen de respuestas

| Pregunta | Respuesta |
|---|---|
| Retroceso de la costa | $\Delta L = -33$ m (30 m por el mar + 3 m por erosión) |
| Punta de la cuña antes | $x_{T0} = 924.4$ m |
| Punta de la cuña después | $x_{Tf} = 885.2$ m |
| Desplazamiento de la punta | $-39.1$ m |
| **Avance real de la cuña** | **+6.1 m** (de 75.6 a 81.8 m invadidos) |
| Subida absoluta del nivel freático | **+0.41 m** |
| Nivel freático respecto al mar | **baja 0.19 m** |

# E — Thiem con dos piezómetros (página 8)

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
de la Guía Maestra, sólo escrita con logaritmo decimal:

$$T = \frac{Q\ln(r_2/r_1)}{2\pi(s_1-s_2)}
= \frac{788\,(3.6243)}{7.2131} = 396\ \mathrm{m^2/día}\ \checkmark$$

porque $\ln x = 2.303\log_{10}x$. **Si en el parcial te dan una y recuerdas la
otra, da exactamente lo mismo.**

> **Lo que vale comentar:** $r_1 = 0.8$ m es prácticamente el pozo de bombeo, no
> un piezómetro. Usar el pozo como punto de medida es menos confiable porque ahí
> hay **pérdidas de carga propias del pozo** (pérdidas de entrada por la rejilla,
> flujo turbulento), que inflan $s_1$ y por tanto **subestiman** $T$. Si hay dos
> piezómetros de observación verdaderos, se prefieren esos.

# F — Theis por punto de coincidencia (página 8)

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

# G — Superposición de dos pozos (página 9)

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

## G.1 Los "3 efectos" de tus apuntes

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

# H — Mapa de isopiezas: elevaciones de pozos y gradientes (Figura 3.31)

**Enunciado (página 6 de tus apuntes).** Los puntos negros de la figura 3.31 son
pozos que llegan al nivel freático. Con las curvas de nivel freático, estimar la
elevación del nivel freático en cada pozo con precisión de 0.1 m. Calcular los
valores mayor y menor del gradiente hidráulico.

![**Figura H1.** Tu mapa con las mediciones que hiciste en clase. En rojo, el gradiente máximo; en verde, el mínimo; en azul, la interpolación de un pozo.](fig/fig_c6_mapa331.png){width=15.8cm}

## Paso 1 — Leer el mapa antes de medir

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

## Paso 2 — Calibrar la escala con la regla

La barra de escala de 0 a 1000 m mide **unos 40 mm** en tu copia. Lo comprobé con
tu propia medición: el espaciamiento que anotaste como 25 mm corresponde en la
figura a la misma distancia que 630 m de la barra.

$$1\ \mathrm{mm} \approx 25\ \mathrm{m}$$

> **Hazlo siempre primero**: mide la barra de escala con la regla. Si tu copia
> está a otra escala (fotocopia ampliada, por ejemplo), el factor cambia, pero el
> método es el mismo.

## Paso 3 — Interpolar la elevación de un pozo

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

## Paso 4 — Gradientes mayor y menor

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
gradiente. Es la misma idea de la Parte 3 de la Guía Maestra: curvas juntas
indican gradiente alto; curvas separadas, gradiente bajo. Si el acuífero fuera
heterogéneo, la separación también podría reflejar cambios de $K$, pero aquí la
causa dominante es la geometría del flujo.

# I — Cargas en una sección con río y lago (Figura 7.39)

**Enunciado (página 7 de tus apuntes).** Las líneas discontinuas son
equipotenciales y las cargas están en metros.

a. Completar las cargas en los puntos A a F.
b. Marcar con R un lugar donde haya recarga.
c. Marcar con D un lugar donde haya descarga.
d. Dibujar líneas de flujo que empiecen en X, Y y Z.

![**Figura I1.** La figura 7.39 resuelta: cargas de A a F, zonas de recarga (R) y descarga (D), y las tres líneas de flujo pedidas.](fig/fig_c5_fig739.png){width=15.8cm}

## Paso 1 — Leer bien la figura

**La foto está inclinada unos 3.5°.** Por eso el eje derecho parece desplazado
5 m respecto al izquierdo: los dos ejes son iguales, pero en la foto una línea
horizontal aparece inclinada. **Lee cada punto con el eje que tenga más cerca.**

**La clave del problema:** las equipotenciales no tienen el valor escrito. Se
obtiene con la condición del nivel freático de la Guía Maestra:

$$\text{en el nivel freático: } h = z$$

Así que **el valor de cada equipotencial es la elevación del punto donde corta el
nivel freático**. Al leerlas así se ve que van **cada 2.5 m**: 2.5, 5, 7.5, 10,
12.5 y 15 m.

Para cada punto:

$$h_{total} = \text{valor de la equipotencial que pasa por el punto}$$

$$z = \text{elevación del punto}
\qquad\qquad
h_p = h_{total} - z$$

## Paso 2 — La tabla resuelta

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

## Paso 3 — Recarga (R) y descarga (D)

**El criterio, que es lo que se evalúa:**

| Zona | Cómo se reconoce | En la figura 7.39 |
|---|---|---|
| **Recarga** | la carga **disminuye** con la profundidad; el flujo baja | las cimas: bajo X, la colina central y junto a Z |
| **Descarga** | la carga **aumenta** con la profundidad; el flujo sube | el valle del río y el lago |

Basta con marcar una de cada una, pero marcar todas demuestra que entendiste el
criterio.

## Paso 4 — Líneas de flujo desde X, Y y Z

Las tres reglas de la Parte 5 de la Guía Maestra:

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

# J — Taller en clase: ríos ganadores y perdedores (página 5)

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

# K — Otros conceptos de tus apuntes

## K.1 La analogía canal–tubería (página 2)

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

## K.2 Recarga, goteo y "agua salta" (página 1)

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

## K.3 El tensor de conductividad (página 1)

Tus apuntes escriben $q = -K\nabla h$ con tres componentes $K_{xx}$, $K_{yy}$,
$K_{zz}$, y agrupan $K_{xx}$ y $K_{yy}$ como $K_h$. Es decir, en un medio
estratificado las dos direcciones horizontales se tratan igual ($K_h$) y la
vertical es distinta ($K_v = K_{zz}$). Es exactamente la Parte 3 de la Guía
Maestra: $K_h$ con media aritmética, $K_v$ con media armónica.

# L — Erratas que encontré en tus apuntes

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

# M — Ejercicios para practicar los temas nuevos

## M.1 Enunciados

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

## M.2 Respuestas

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

# N — Qué cambia en tu plan de estudio

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

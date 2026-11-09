# Chuleta: lo mínimo que tienes que llevar en la cabeza

Si solo te alcanza para memorizar una página, que sea esta.

## Las dos fórmulas que resuelven el 80 % del problema

**Cooper-Jacob** (recta en papel semilogarítmico, $s$ contra $\log t$):

$$\boxed{\;T = \frac{2.303\,Q}{4\pi\,\Delta s}\;}
\qquad\qquad
\boxed{\;S = \frac{2.25\,T\,t_0}{r^{2}}\;}$$

- $\Delta s$ = caída de abatimiento **por ciclo logarítmico** de tiempo (m).
- $t_0$ = tiempo donde la recta extrapolada corta $s = 0$.
- $r$ = distancia del piezómetro al pozo. **Siempre en las mismas unidades que $T$.**

## Las demás, en una tabla

| Qué | Fórmula | Cuándo |
|---|---|---|
| Theis | $s = \dfrac{Q}{4\pi T}\,W(u)$,  $u = \dfrac{r^{2}S}{4Tt}$ | general, cualquier $u$ |
| Cooper-Jacob | $s = \dfrac{2.303\,Q}{4\pi T}\log\dfrac{2.25\,Tt}{r^{2}S}$ | sólo si $u < 0.01$ |
| Distancia–abatimiento | $T = \dfrac{2.303\,Q}{2\pi\,\Delta s_r}$,  $S = \dfrac{2.25\,T\,t}{r_0^{2}}$ | varios piezómetros, un tiempo |
| Recuperación | $T = \dfrac{2.303\,Q}{4\pi\,\Delta s'}$,  $s' = \dfrac{2.303Q}{4\pi T}\log\dfrac{t}{t'}$ | tras parar la bomba |
| Thiem (confinado) | $T = \dfrac{Q\,\ln(r_2/r_1)}{2\pi\,(s_1-s_2)}$ | permanente, confinado |
| Dupuit (libre) | $K = \dfrac{Q\,\ln(r_2/r_1)}{\pi\,(h_2^{2}-h_1^{2})}$ | permanente, libre |
| Radio de influencia | $R_0 = \sqrt{\dfrac{2.25\,T\,t}{S}} = 1.5\sqrt{\dfrac{Tt}{S}}$ | — |
| Superposición | $s_{total} = \sum_i s_i$ | varios pozos |
| Relaciones | $T = Kb$,  $S = S_s b$,  capacidad específica $= Q/s_w$ | — |

## Números que ahorran tiempo

$$\frac{2.303}{4\pi} = 0.1833
\qquad
\frac{2.303}{2\pi} = 0.3665
\qquad
\frac{1}{4\pi} = 0.07958
\qquad
\sqrt{2.25} = 1.5$$

$$1\ \mathrm{L/s} = 86.4\ \mathrm{m^3/día}
\qquad
1\ \mathrm{m^3/día} = 1.157\times10^{-5}\ \mathrm{m^3/s}$$

## La regla de oro de las unidades

Decide **al principio** si trabajas en días o en segundos y no lo cambies. Lo más
cómodo: **$Q$ en m³/día, $r$ en m, $t$ en días, $T$ en m²/día**. Los tiempos de la
tabla de datos casi siempre vienen en minutos: divide por 1440.

# Parte 1 — Qué método usar

No empieces a calcular hasta saber qué método aplica. Esto se decide mirando
**qué datos te dieron**, no qué fórmula recuerdas.

![**Figura 1.** Árbol de decisión. La pregunta que lo define todo es qué variable acompaña al abatimiento en la tabla de datos: tiempo, distancia, o ninguna.](fig/fig_b0_arbol.png){width=15.8cm}

| Si en el enunciado ves… | Usa |
|---|---|
| una tabla de $t$ y $s$ en **un** piezómetro | Cooper-Jacob (o Theis si $u>0.01$) |
| $s$ medido en **varios** piezómetros al **mismo** tiempo | distancia–abatimiento |
| «el abatimiento se estabilizó» y dos piezómetros | Thiem (confinado) o Dupuit (libre) |
| mediciones **después de apagar la bomba** | recuperación de Theis |
| $T$ y $S$ ya dados, y te piden $s$ en algún punto | Theis o Cooper-Jacob directo |

# Parte 2 — Los conceptos, en una página

## Qué es cada cosa

| Símbolo | Nombre | Unidades | Qué significa |
|---|---|---|---|
| $Q$ | caudal de bombeo | m³/día | constante durante la prueba |
| $s$ | abatimiento | m | $s = h_0 - h$, **descenso** respecto al nivel inicial |
| $T$ | transmisividad | m²/día | capacidad de **transmitir** agua, $T = Kb$ |
| $S$ | coeficiente de almacenamiento | adimensional | agua liberada por unidad de área y de descenso |
| $r$ | distancia radial | m | del pozo al punto de observación |
| $b$ | espesor del acuífero | m | — |

![**Figura 2.** Geometría de una prueba de bombeo. El pozo extrae $Q$ constante, el cono de abatimiento crece con el tiempo y el piezómetro a distancia $r$ registra el abatimiento $s$.](fig/fig_b1_esquema.png){width=15.8cm}

## La ecuación que hay detrás

En coordenadas radiales, la ecuación de flujo transitorio es

$$\frac{\partial^{2}s}{\partial r^{2}} + \frac{1}{r}\frac{\partial s}{\partial r}
= \frac{S}{T}\,\frac{\partial s}{\partial t}$$

Theis (1935) la resolvió para un pozo puntual que bombea $Q$ constante en un
acuífero infinito. **Todo lo demás de este documento son casos particulares o
aproximaciones de esa solución.**

## Las hipótesis de Theis (pregunta típica de teoría)

1. Acuífero **confinado**, homogéneo, isótropo y de espesor uniforme.
2. Extensión **infinita** en planta (sin fronteras).
3. Superficie piezométrica inicial **horizontal**.
4. Caudal $Q$ **constante**.
5. El pozo **penetra todo el espesor** del acuífero.
6. Diámetro del pozo **despreciable** (sin almacenamiento en el pozo).
7. El agua se libera **instantáneamente** al bajar la carga.
8. Flujo **radial horizontal** y válido para Darcy (laminar).

Cuando el enunciado dice «acuífero libre» o «semiconfinado», o menciona un río o
una frontera impermeable, está avisando que alguna de estas hipótesis se rompe.

# Parte 3 — Método de Theis

## La solución

$$\boxed{\;s = \frac{Q}{4\pi T}\,W(u)\;}
\qquad\qquad
\boxed{\;u = \frac{r^{2}S}{4Tt}\;}$$

$W(u)$ es la **función de pozo**, que es la integral exponencial:

$$W(u) = \int_u^{\infty}\frac{e^{-y}}{y}\,dy
= -0.5772 - \ln u + u - \frac{u^{2}}{2\cdot 2!} + \frac{u^{3}}{3\cdot 3!} - \cdots$$

## Tabla de $W(u)$

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

**Atajo si no tienes tabla:** para $u < 0.01$,
$W(u) \approx -0.5772 - \ln u = \ln\dfrac{0.5615}{u}$. Con $u = 10^{-3}$ da 6.331
contra 6.332 de la tabla.

## El ajuste de curva patrón

![**Figura 3.** Método de la curva patrón. Se superponen los dos gráficos manteniendo los ejes paralelos, se elige un punto de coincidencia cómodo y se leen sus cuatro coordenadas.](fig/fig_b3_theis.png){width=15.8cm}

**Procedimiento:**

1. Dibuja la curva patrón $W(u)$ contra $1/u$ en papel log-log.
2. Dibuja los datos $s$ contra $t$ en papel log-log **de la misma escala**.
3. Superpón las hojas manteniendo los **ejes paralelos** y desplázalas hasta que
   los datos caigan sobre la curva.
4. Elige un **punto de coincidencia** cómodo (por ejemplo $W=1$, $1/u=10$) y lee
   sus cuatro coordenadas: $W(u)$, $u$, $s$, $t$.
5. Calcula:

$$T = \frac{Q\,W(u)}{4\pi\,s}
\qquad\qquad
S = \frac{4\,T\,t\,u}{r^{2}}$$

**Cuándo lo necesitas de verdad:** cuando los datos son de tiempos cortos o $r$
grande, es decir cuando $u > 0.01$ y la recta de Cooper-Jacob no existe todavía.
En un parcial de 2 horas es más probable que te pidan Cooper-Jacob.

# Parte 4 — Método de Cooper-Jacob

Este es **el** método. Si solo te alcanza para aprender uno, es este.

## De dónde sale

Para $u$ pequeño la serie de $W(u)$ se corta en los dos primeros términos:

$$W(u) \approx -0.5772 - \ln u$$

Sustituyendo $u = r^{2}S/4Tt$ y pasando a logaritmo decimal:

$$s = \frac{2.303\,Q}{4\pi T}\,\log\!\left(\frac{2.25\,T\,t}{r^{2}S}\right)$$

Esto es una **recta** si se grafica $s$ contra $\log t$. Y de una recta se leen dos
cosas: la pendiente y el punto de corte.

**Pendiente** → por cada ciclo logarítmico, $\log t$ aumenta 1, de modo que

$$\Delta s = \frac{2.303\,Q}{4\pi T}
\qquad\Longrightarrow\qquad
\boxed{T = \frac{2.303\,Q}{4\pi\,\Delta s}}$$

**Corte con $s=0$** → ahí el logaritmo vale cero, es decir su argumento vale 1:

$$\frac{2.25\,T\,t_0}{r^{2}S} = 1
\qquad\Longrightarrow\qquad
\boxed{S = \frac{2.25\,T\,t_0}{r^{2}}}$$

## Condición de validez

$$u = \frac{r^{2}S}{4Tt} < 0.01$$

El error que se comete es: 1 % para $u=0.03$, 2 % para $u=0.05$, 5 % para
$u=0.1$. En la práctica se acepta hasta $u \approx 0.05$, pero **declara el
criterio que usaste**.

Leído al revés, la condición dice que hay que esperar lo suficiente:

$$t > \frac{r^{2}S}{0.04\,T}$$

Por eso en el gráfico los puntos iniciales se salen de la recta: no es error de
medición, es que la aproximación todavía no vale.

## Ejemplo completo

**Enunciado.** Prueba de bombeo en un acuífero confinado de 25 m de espesor.
$Q = 1500$ m³/día constante. Piezómetro a $r = 50$ m. Se midió:

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

Calcular $T$, $S$, $K$ y $S_s$.

![**Figura 4.** El ajuste de Cooper-Jacob. Los puntos huecos de tiempo corto no se usan: ahí $u>0.01$. La recta se traza sólo con los puntos llenos, y de ella se leen $\Delta s$ y $t_0$.](fig/fig_b2_cooper_jacob.png){width=15.8cm}

**Paso 1 — Graficar $s$ contra $\log t$** y trazar la recta por los puntos de
tiempo tardío, ignorando la curvatura inicial.

**Paso 2 — Leer la pendiente.** Entre $t = 100$ min y $t = 1000$ min (un ciclo
logarítmico exacto) la recta sube de 1.17 m a 2.08 m:

$$\Delta s = 2.08 - 1.17 = 0.91\ \mathrm{m\ por\ ciclo}$$

**Paso 3 — Leer $t_0$.** La recta extrapolada corta $s = 0$ en

$$t_0 = 5.2\ \mathrm{min} = \frac{5.2}{1440} = 3.61\times10^{-3}\ \mathrm{días}$$

**Paso 4 — Transmisividad.**

$$T = \frac{2.303\,Q}{4\pi\,\Delta s}
= \frac{2.303\,(1500\ \mathrm{m^3/día})}{4\pi\,(0.91\ \mathrm{m})}
= \frac{3454.5}{11.44}$$

$$\boxed{T = 301\ \mathrm{m^2/día}}$$

**Paso 5 — Almacenamiento.**

$$S = \frac{2.25\,T\,t_0}{r^{2}}
= \frac{2.25\,(301)\,(3.61\times10^{-3})}{(50)^{2}}
= \frac{2.445}{2500}$$

$$\boxed{S = 9.8\times10^{-4}}$$

**Paso 6 — Verificar la validez.** Con el $t$ más grande de la tabla ($t = 1440$
min $= 1$ día):

$$u = \frac{r^{2}S}{4Tt} = \frac{(50)^{2}(9.8\times10^{-4})}{4(301)(1)}
= \frac{2.45}{1204} = 2.0\times10^{-3} < 0.01\ \checkmark$$

Y con el primer punto que usé para la recta ($t = 360$ min $= 0.25$ d):
$u = 8.1\times10^{-3} < 0.01$ ✓. Los puntos anteriores tenían $u > 0.01$ y por eso
quedaron fuera.

**Paso 7 — Derivados.**

$$K = \frac{T}{b} = \frac{301}{25} = 12.0\ \mathrm{m/día} = 1.4\times10^{-4}\ \mathrm{m/s}$$

$$S_s = \frac{S}{b} = \frac{9.8\times10^{-4}}{25} = 3.9\times10^{-5}\ \mathrm{m^{-1}}$$

**Paso 8 — ¿Tiene sentido?** $K = 1.4\times10^{-4}$ m/s corresponde a **arena
limpia a arena gruesa**, y $S \approx 10^{-3}$ es el rango típico de un acuífero
confinado ($10^{-5}$ a $10^{-3}$). Coherente. **Haz siempre este paso**: si te
sale $S = 0.2$ en un confinado, o $K$ de grava en una arcilla, hay un error de
unidades.

## Receta de 8 pasos para el parcial

1. Convierte los tiempos a días (divide los minutos por 1440).
2. Grafica $s$ contra $\log t$ en semilog.
3. Traza la recta por los puntos **tardíos**.
4. Mide $\Delta s$ sobre **un ciclo logarítmico completo** (de 10 a 100, de 100 a
   1000…). No midas entre dos puntos cualesquiera.
5. Extrapola hasta $s=0$ y lee $t_0$.
6. $T = 2.303\,Q/(4\pi\,\Delta s)$.
7. $S = 2.25\,T\,t_0/r^{2}$.
8. Comprueba $u < 0.01$ y la plausibilidad del resultado.

# Parte 5 — Método distancia–abatimiento

Cuando hay **varios piezómetros** medidos al **mismo** tiempo, se grafica $s$
contra $\log r$.

![**Figura 5.** Distancia–abatimiento a $t = 1$ día. Ojo con el denominador: aquí es $2\pi$, no $4\pi$, porque al derivar respecto de $\log r$ aparece un factor 2 ($r$ está al cuadrado).](fig/fig_b4_distancia.png){width=15.8cm}

$$\boxed{T = \frac{2.303\,Q}{2\pi\,\Delta s_r}}
\qquad\qquad
\boxed{S = \frac{2.25\,T\,t}{r_0^{2}}}$$

donde $\Delta s_r$ es la caída por ciclo logarítmico de **distancia** y $r_0$ es
la distancia donde la recta corta $s=0$ (el radio de influencia).

## Ejemplo

$Q = 1500$ m³/día, lecturas a $t = 1$ día:

| $r$ (m) | 10 | 30 | 50 | 100 | 200 | 300 |
|---|---|---|---|---|---|---|
| $s$ (m) | 3.508 | 2.634 | 2.228 | 1.679 | 1.137 | 0.830 |

De la recta: $\Delta s_r = 1.83$ m por ciclo y $r_0 = 826$ m.

$$T = \frac{2.303\,(1500)}{2\pi\,(1.83)} = \frac{3454.5}{11.50}
= \boxed{300\ \mathrm{m^2/día}}$$

$$S = \frac{2.25\,(300)\,(1)}{(826)^{2}} = \frac{675}{682\,276}
= \boxed{9.9\times10^{-4}}$$

Idéntico al resultado de Cooper-Jacob, como debe ser: es el mismo acuífero.

> **De dónde sale el factor 2.** En $s = \frac{2.303Q}{4\pi T}\log\frac{2.25Tt}{r^2S}$
> el término $r^2$ está en el denominador y elevado al cuadrado, así que
> $\log(r^{-2}) = -2\log r$. Al derivar respecto de $\log r$ sale $2$, que se
> cancela con el $4\pi$ y deja $2\pi$.

# Parte 6 — Método de recuperación de Theis

Se apaga la bomba y se mide cómo **sube** el nivel. Es la prueba más barata y
precisa porque no hay que mantener $Q$ constante durante la medición.

Definiciones (hay que tenerlas claras o el método falla):

- $t$ = tiempo desde que **arrancó** la bomba.
- $t'$ = tiempo desde que **paró** la bomba.
- $s'$ = **abatimiento residual**: lo que aún falta para recuperar el nivel inicial.

Por superposición (bomba real que sigue bombeando $+Q$ más una bomba imaginaria
que inyecta $-Q$ desde el instante de apagado):

$$\boxed{\;s' = \frac{2.303\,Q}{4\pi T}\,\log\frac{t}{t'}\;}
\qquad\Longrightarrow\qquad
\boxed{\;T = \frac{2.303\,Q}{4\pi\,\Delta s'}\;}$$

![**Figura 6.** Recuperación. Se grafica $s'$ contra $\log(t/t')$ y la recta pasa por el origen. Medida en el propio pozo de bombeo, la aproximación es válida desde el primer instante.](fig/fig_b5_recuperacion.png){width=15.8cm}

## Ejemplo

Se bombeó $Q = 1500$ m³/día durante $t_p = 1440$ min y se mide la recuperación en
el propio pozo:

| $t'$ (min) | 5 | 10 | 20 | 30 | 60 | 120 | 240 | 480 |
|---|---|---|---|---|---|---|---|---|
| $t/t'$ | 289 | 145 | 73 | 49 | 25 | 13 | 7 | 4 |
| $s'$ (m) | 2.255 | 1.980 | 1.707 | 1.549 | 1.281 | 1.021 | 0.774 | 0.552 |

De la recta, $\Delta s' = 0.92$ m por ciclo:

$$T = \frac{2.303\,(1500)}{4\pi\,(0.92)} = \boxed{300\ \mathrm{m^2/día}}$$

> **Lo que hay que decir y casi nadie dice:** la recuperación da $T$ pero **no da
> $S$**, porque la recta pasa obligatoriamente por el origen ($s'=0$ cuando
> $t/t'=1$) y no hay ningún intercepto del que extraer $S$.

# Parte 7 — Régimen permanente: Thiem y Dupuit

Si el enunciado dice que **el abatimiento se estabilizó**, el tiempo desaparece
del problema y ya no se puede obtener $S$ (no hay cambio de almacenamiento).

![**Figura 7.** Régimen permanente. En acuífero confinado se trabaja con los abatimientos; en acuífero libre, con los cuadrados de los espesores saturados.](fig/fig_b9_thiem.png){width=15.8cm}

## Confinado (Thiem)

$$Q = \frac{2\pi T\,(s_1-s_2)}{\ln(r_2/r_1)}
\qquad\Longrightarrow\qquad
\boxed{T = \frac{Q\,\ln(r_2/r_1)}{2\pi\,(s_1-s_2)}}$$

**Ejemplo.** $Q=1500$ m³/día; $r_1=20$ m con $s_1=2.80$ m; $r_2=200$ m con
$s_2=1.00$ m:

$$T = \frac{1500\,\ln(200/20)}{2\pi\,(2.80-1.00)}
= \frac{1500\,(2.3026)}{11.31} = \boxed{305\ \mathrm{m^2/día}}
\qquad K = \frac{305}{25} = 12.2\ \mathrm{m/día}$$

## Libre (Dupuit)

Aquí el espesor saturado **cambia** con $r$, así que aparecen los cuadrados:

$$Q = \frac{\pi K\,(h_2^{2}-h_1^{2})}{\ln(r_2/r_1)}
\qquad\Longrightarrow\qquad
\boxed{K = \frac{Q\,\ln(r_2/r_1)}{\pi\,(h_2^{2}-h_1^{2})}}$$

**Ejemplo.** $Q=1500$ m³/día, acuífero libre de $H=30$ m; $h_1=27.0$ m a 20 m y
$h_2=29.2$ m a 200 m:

$$K = \frac{1500\,(2.3026)}{\pi\,(29.2^{2}-27.0^{2})}
= \frac{3454}{\pi\,(852.6-729.0)} = \frac{3454}{388.3}
= \boxed{8.9\ \mathrm{m/día}}$$

> **La trampa clásica del acuífero libre:** usar $s$ en vez de $h^{2}$. Fíjate en
> que $h$ se mide **desde la base del acuífero**, no desde el nivel inicial.
> Si el enunciado te da abatimientos, convierte: $h = H - s$.

# Parte 8 — Cálculos en el acuífero

Esta es la segunda mitad del problema: ya tienes $T$ y $S$, ahora hay que usarlos.
Todo lo que sigue usa los valores del ejemplo: $T = 300$ m²/día, $S = 10^{-3}$,
$b = 25$ m, $Q = 1500$ m³/día.

## (a) Abatimiento en cualquier punto y cualquier tiempo

**Pregunta.** ¿Cuánto baja el nivel a 200 m del pozo después de 30 días?

$$u = \frac{r^{2}S}{4Tt} = \frac{(200)^{2}(10^{-3})}{4(300)(30)}
= \frac{40}{36\,000} = 1.11\times10^{-3}$$

De la tabla, $W(1.11\times10^{-3}) = 6.23$:

$$s = \frac{Q}{4\pi T}W(u) = \frac{1500}{4\pi(300)}\,(6.23)
= (0.3979)(6.23) = \boxed{2.48\ \mathrm{m}}$$

Como $u < 0.01$, también sirve Cooper-Jacob:

$$s = \frac{2.303(1500)}{4\pi(300)}\log\frac{2.25(300)(30)}{(200)^{2}(10^{-3})}
= 0.9163\log(506.3) = 0.9163(2.704) = 2.48\ \mathrm{m}\ \checkmark$$

## (b) Abatimiento en el pozo y capacidad específica

Se aplica la misma fórmula con $r = r_w$ (radio del pozo, aquí 0.15 m):

$$u = \frac{(0.15)^{2}(10^{-3})}{4(300)(30)} = 6.25\times10^{-10}
\qquad W(u) = 20.6$$

$$s_w = (0.3979)(20.6) = \boxed{8.2\ \mathrm{m}}$$

$$\text{Capacidad específica} = \frac{Q}{s_w} = \frac{1500}{8.2}
= \boxed{183\ \mathrm{m^3/día\ por\ metro\ de\ abatimiento}}$$

> La capacidad específica **no es constante**: disminuye con el tiempo, porque
> $s_w$ crece. Siempre di a qué tiempo corresponde.

## (c) Varios pozos: superposición

La ecuación de flujo es **lineal**, de modo que los abatimientos se suman:

$$\boxed{\;s_{total}(x,y,t) = \sum_{i=1}^{n}\frac{Q_i}{4\pi T}\,W(u_i),
\qquad u_i = \frac{r_i^{2}S}{4Tt}\;}$$

![**Figura 8.** Tres pozos de 1500 m³/día a los 30 días. Los conos individuales se suman: en el punto A el abatimiento es el triple del que produciría un pozo aislado a la misma distancia.](fig/fig_b7_superposicion.png){width=15.8cm}

**Ejemplo.** Tres pozos de 1500 m³/día cada uno, situados en los vértices de un
triángulo. El punto A está a 173.3 m de cada uno. A los 30 días:

| Aporte | $r_i$ (m) | $s_i$ (m) |
|---|---|---|
| pozo 1 | 173.3 | 2.591 |
| pozo 2 | 173.3 | 2.591 |
| pozo 3 | 173.3 | 2.591 |
| **Total** | — | **7.774** |

Un solo pozo produciría 2.59 m; los tres juntos producen 7.77 m. **La
interferencia es lo que limita el espaciamiento de un campo de pozos.**

## (d) Radio de influencia

$$\boxed{R_0 = \sqrt{\frac{2.25\,T\,t}{S}} = 1.5\sqrt{\frac{T\,t}{S}}}$$

| $t$ | 1 día | 7 días | 30 días | 1 año |
|---|---|---|---|---|
| $R_0$ | 822 m | 2174 m | 4500 m | 15 700 m |

![**Figura 9.** El cono crece indefinidamente: en un acuífero confinado ideal **nunca** se alcanza el régimen permanente. $R_0$ crece con $\sqrt{t}$, de modo que cuadruplicar el tiempo sólo duplica el radio.](fig/fig_b6_cono.png){width=15.8cm}

$R_0$ es el radio donde la **recta** de Cooper-Jacob da $s=0$; no es una frontera
física. En rigor el cono es infinito, sólo que inmedible más allá de $R_0$.

## (e) De $T$ a las velocidades

$$K = \frac{T}{b} = \frac{300}{25} = 12\ \mathrm{m/día}$$

Gradiente a $r = 200$ m (derivando la solución, $\partial s/\partial r \approx Q/2\pi Tr$):

$$i = \frac{Q}{2\pi T r} = \frac{1500}{2\pi(300)(200)} = 3.98\times10^{-3}$$

$$q = K\,i = (12)(3.98\times10^{-3}) = 0.0477\ \mathrm{m/día}$$

$$v = \frac{q}{n_e} = \frac{0.0477}{0.2} = \boxed{0.239\ \mathrm{m/día}}$$

**Verificación por continuidad** (hazla, es gratis): todo el caudal cruza el
cilindro de radio 200 m y altura 25 m,

$$q = \frac{Q}{2\pi r b} = \frac{1500}{2\pi(200)(25)} = 0.0477\ \mathrm{m/día}\ \checkmark$$

## (f) Volumen extraído del almacenamiento

$$V = Q\,t = (1500)(30) = \boxed{45\,000\ \mathrm{m^3}}$$

En un acuífero confinado infinito **todo** el agua bombeada sale del
almacenamiento elástico: no hay recarga que la reponga.

## (g) Tiempo para alcanzar un abatimiento dado

**Pregunta.** ¿Cuándo llega el abatimiento a 2.00 m en un piezómetro a 100 m?

Se invierte Cooper-Jacob:

$$t = \frac{r^{2}S}{2.25\,T}\;10^{\,4\pi T s/(2.303\,Q)}$$

$$t = \frac{(100)^{2}(10^{-3})}{2.25(300)}\;
10^{\,4\pi(300)(2.00)/(2.303 \cdot 1500)}
= (0.01481)\,10^{2.183} = \boxed{2.26\ \mathrm{días}}$$

Verificado con Theis: a $t = 2.26$ d, $s = 2.000$ m exactamente.

## (h) Caudal máximo con un abatimiento disponible

**Pregunta.** Si solo se pueden admitir 8 m de abatimiento en el pozo y hay que
bombear 180 días, ¿cuál es el $Q$ máximo?

Como $s$ es **proporcional** a $Q$, basta calcular el abatimiento por unidad de
caudal y escalar:

$$s_w\ \text{por } 1\ \mathrm{m^3/día} = 5.94\times10^{-3}\ \mathrm{m}$$

$$Q_{max} = \frac{8.00}{5.94\times10^{-3}} = \boxed{1346\ \mathrm{m^3/día} = 15.6\ \mathrm{L/s}}$$

La linealidad en $Q$ es la propiedad más útil de toda la teoría: duplicar el
caudal duplica el abatimiento en todos los puntos.

## (i) Fronteras: método de los pozos imagen

Theis supone acuífero infinito. Si hay una frontera, se simula con un **pozo
imagen** reflejado al otro lado, a la misma distancia:

| Tipo de frontera | Pozo imagen | Efecto |
|---|---|---|
| **Impermeable** (barrera, falla) | bombea $+Q$ | el abatimiento **aumenta** |
| **Carga constante** (río, lago) | inyecta $-Q$ | el abatimiento **disminuye** |

![**Figura 10.** Pozos imagen. Una barrera impermeable casi duplica el abatimiento; un río lo reduce drásticamente porque aporta agua al acuífero.](fig/fig_b8_imagenes.png){width=15.8cm}

**Ejemplo.** Pozo en $x=0$, frontera a $L = 150$ m, pozo imagen en $x = 300$ m.
Punto de cálculo en $x = 100$ m, es decir $r_{real} = 100$ m y $r_{imagen} = 200$ m.
A los 30 días:

$$s_{real} = 3.03\ \mathrm{m}
\qquad\qquad
s_{imagen} = 2.48\ \mathrm{m}$$

| Caso | Cálculo | Resultado |
|---|---|---|
| Sin frontera | $3.03$ | 3.03 m |
| Frontera impermeable | $3.03 + 2.48$ | **5.51 m**  (×1.82) |
| Río (carga constante) | $3.03 - 2.48$ | **0.55 m**  (×0.18) |

# Parte 9 — Trampas y errores que cuestan el parcial

| # | Error | Cómo evitarlo |
|---|---|---|
| 1 | Mezclar minutos con días | Convierte **todo** a días al principio. $t_0$ en minutos metido en la fórmula de $S$ da un error de 1440× |
| 2 | Medir $\Delta s$ entre dos puntos cualesquiera | Tiene que ser **un ciclo logarítmico completo**: 1→10, 10→100, 100→1000 |
| 3 | Usar $2\pi$ en tiempo–abatimiento o $4\pi$ en distancia–abatimiento | Tiempo → $4\pi$. Distancia → $2\pi$ |
| 4 | No verificar $u<0.01$ | Si los puntos tardíos no cumplen, hay que usar Theis |
| 5 | Trazar la recta por los puntos iniciales | Los primeros puntos **siempre** se curvan hacia abajo; se descartan |
| 6 | Usar $s$ en un acuífero libre | Dupuit va con $h^{2}$, medido desde la base |
| 7 | Esperar $S$ de una prueba de recuperación | No se puede: la recta pasa por el origen |
| 8 | Esperar $S$ de un ensayo en régimen permanente | Tampoco: sin tiempo no hay almacenamiento |
| 9 | Confundir $T$ con $K$ | $T = Kb$. Si el enunciado da el espesor, casi siempre quiere que hagas la conversión |
| 10 | Olvidar la superposición con varios pozos | Si hay más de un pozo, **suma** |
| 11 | Signo del pozo imagen | Impermeable → suma. Río → resta |
| 12 | $r$ del piezómetro frente a $r_w$ del pozo | Para abatimiento **en el pozo** usa $r_w$, que es ~0.1–0.3 m |
| 13 | No comprobar el orden de magnitud | Confinado: $S = 10^{-5}$ a $10^{-3}$. Libre: $S_y = 0.05$ a 0.3. Si no cae ahí, revisa |

## Rangos de referencia

| Material | $K$ (m/día) | $K$ (m/s) |
|---|---|---|
| Grava | $10^{3}$–$10^{5}$ | $10^{-2}$–1 |
| Arena limpia | 1–$10^{3}$ | $10^{-5}$–$10^{-2}$ |
| Arena fina, limo | $10^{-3}$–1 | $10^{-8}$–$10^{-5}$ |
| Arcilla | $<10^{-3}$ | $<10^{-8}$ |

| Parámetro | Rango |
|---|---|
| $S$ confinado | $10^{-5}$ a $10^{-3}$ |
| $S_y$ libre | 0.05 a 0.30 |
| $T$ acuífero explotable | $>100$ m²/día |

# Parte 10 — Plan para esta noche

Tienes el parcial mañana. Esto es lo que rinde más por hora invertida.

**Primera hora — Cooper-Jacob, y nada más.**
Lee la Parte 4 completa y **rehaz el ejemplo a mano**, con papel semilog si lo
tienes (o dibujando el eje log a mano). El objetivo es que puedas escribir de
memoria $T = 2.303Q/(4\pi\Delta s)$ y $S = 2.25Tt_0/r^{2}$, y que sepas de dónde
sale cada una. Si solo dominas esto ya puedes resolver el problema típico.

**Segunda hora — los cálculos posteriores.**
Parte 8, incisos (a), (b), (c) y (d). Son los que vienen después de hallar $T$:
predecir abatimiento, capacidad específica, superposición y radio de influencia.
Practica la Parte 8(a) cambiando los números de $r$ y $t$.

**Tercera hora — los otros métodos, en diagonal.**
Distancia–abatimiento (sólo recuerda que el denominador cambia a $2\pi$),
recuperación (da $T$, no da $S$) y Thiem/Dupuit (permanente; en libre va con
$h^{2}$). No necesitas deducirlos, sólo reconocerlos y saber qué fórmula aplicar.

**Últimos 20 minutos — la chuleta y las trampas.**
Relee la primera página y la tabla de la Parte 9. Memoriza $2.303/4\pi = 0.1833$
y las hipótesis de Theis, que son pregunta de teoría casi segura.

**Mañana, en los primeros 2 minutos del parcial:**

1. Lee qué te dan: ¿tabla de $t$ y $s$? ¿varios piezómetros? ¿se estabilizó?
2. Convierte los tiempos a días.
3. Escribe las dos fórmulas antes de calcular nada.
4. Grafica, traza la recta, lee $\Delta s$ y $t_0$.
5. Calcula, comprueba $u<0.01$ y di si el resultado es plausible.

Suerte. Si en el parcial te quedas en blanco, dibuja el gráfico: la recta en
semilog te recuerda las dos fórmulas.

# Guía explicada paso a paso

**Cómo se resuelve cada ejercicio** — Capítulos 3, 4 y 5 de Domenico & Schwartz
Documento de preparación para el parcial de Hidráulica Subterránea

> Este documento no repite los números: explica **qué reconocer, qué fórmula usar, por qué, en qué orden y dónde está la trampa**. Los resultados numéricos están en `01_Solucionario_Cap3-4-5.md`.

---

## Índice

- [Parte 0 — El marco conceptual que lo explica todo](#parte-0)
- [Parte I — Capítulo 3: Movimiento del agua subterránea](#parte-i)
- [Parte II — Capítulo 4: Ecuaciones de flujo, fronteras y redes](#parte-ii)
- [Parte III — Capítulo 5: El agua subterránea en el ciclo hidrológico](#parte-iii)
- [Parte IV — Chuleta y errores que cuestan el parcial](#parte-iv)

---

<a name="parte-0"></a>
# Parte 0 — El marco conceptual que lo explica todo

Antes de atacar los ejercicios conviene tener claro que **casi todo el parcial sale de cinco ideas**. Si las dominas, no tienes que memorizar fórmulas sueltas.

## Idea 1 — La carga hidráulica es energía por unidad de peso

$$h = z + \frac{P}{\rho_w g}$$

El agua **no** se mueve de alta a baja presión, ni de arriba hacia abajo: se mueve de **alta a baja carga hidráulica**. Esto es la causa de que el agua pueda fluir hacia arriba (en zonas de descarga) o que un pozo artesiano brote.

Los tres términos y su nombre en el examen:

| Término | Nombre | Cómo se mide en campo |
|---|---|---|
| $h$ | carga total, *total head* | cota del nivel de agua en el piezómetro |
| $z$ | carga de elevación, *elevation head* | cota del **fondo** (punta filtrante) del piezómetro |
| $P/\rho_w g$ | carga de presión, *pressure head* | longitud de la columna de agua dentro del piezómetro |

$$\boxed{h = z + h_p \;\Longleftrightarrow\; h_p = h - z \;\Longleftrightarrow\; z = h - h_p}$$

Con dos de los tres, siempre se obtiene el tercero. El problema 3.7 es exactamente esto.

## Idea 2 — La ley de Darcy, con su signo

$$\boxed{\mathbf{q} = -K\,\nabla h}
\qquad
\boxed{Q = q\,A = -K A \frac{dh}{dL}}$$

- $\mathbf{q}$ es la **descarga específica** o *flujo de Darcy* (también llamada "velocidad de Darcy"). Es un **caudal por unidad de área total**, no una velocidad real. Dimensiones $L/T$.
- El **signo menos** dice que el flujo va en sentido opuesto al gradiente, es decir, de mayor a menor carga. Si lo omites, la respuesta está mal firmada.
- $K$ es la **conductividad hidráulica**: propiedad del medio **y** del fluido.

**La velocidad real** es mucho mayor porque el agua solo circula por los poros conectados:

$$\boxed{v = \frac{q}{n_e}}$$

Mnemotecnia para no invertirla: $n_e < 1$, y la velocidad real tiene que ser **mayor** que $q$; dividir por un número menor que 1 aumenta → correcto.

## Idea 3 — Permeabilidad intrínseca vs. conductividad hidráulica

$$\boxed{K = \frac{k\,\rho_w\,g}{\mu}}$$

| | Símbolo | Dimensiones | Depende de |
|---|---|---|---|
| Permeabilidad intrínseca | $k$ | $L^2$ (m², cm², darcy) | **solo del medio** (tamaño y conexión de poros) |
| Conductividad hidráulica | $K$ | $L/T$ (m/s, m/día) | del medio **y** del fluido ($\rho$, $\mu$) |

Por eso el petróleo usa $k$ (fluidos distintos) y la hidrogeología usa $K$ (siempre agua). Toda conversión de unidades del problema 3.8 cuelga de esta ecuación.

## Idea 4 — La ecuación de flujo es una ecuación de conservación

Combinando Darcy con el balance de masa se obtiene

$$\nabla^2 h = \frac{S_s}{K}\frac{\partial h}{\partial t}
\qquad\text{o, en términos de acuífero,}\qquad
\nabla^2 h = \frac{S}{T}\frac{\partial h}{\partial t}$$

**La lectura correcta es:** "la curvatura espacial de la carga (lo que entra menos lo que sale) iguala la tasa a la que el almacenamiento cambia".

Dos casos límite que debes reconocer al instante:

$$\frac{\partial h}{\partial t} = 0 \;\Longrightarrow\; \boxed{\nabla^2 h = 0} \quad\text{(Laplace: régimen permanente, redes de flujo)}$$

$$S \ne 0 \;\Longrightarrow\; \text{régimen transitorio: aparece } \sqrt{Tt/S} \text{ en todas las soluciones}$$

Esa raíz, $\sqrt{Tt/S}$, es la **longitud de difusión**: la distancia a la que una perturbación de carga se ha propagado en el tiempo $t$. Aparece en el problema 5.3 y en toda la teoría de pruebas de bombeo.

## Idea 5 — Esfuerzo efectivo (principio de Terzaghi)

$$\boxed{\sigma' = \sigma_T - u}$$

El esqueleto del suelo solo soporta carga a través de $\sigma'$. Si la presión de poro $u$ crece hasta igualar el esfuerzo total $\sigma_T$, entonces $\sigma' = 0$ y el suelo **pierde toda resistencia**: licuación, arenas movedizas, reventón del fondo de una excavación.

$$FS = \frac{\sigma_T}{u}$$

Esta única idea resuelve el problema 4.4 y el 5.4.

---

<a name="parte-i"></a>
# Parte I — Capítulo 3: Movimiento del agua subterránea

## 3.1 y 3.2 — Descarga específica y velocidad real

**Qué se evalúa:** que distingas $q$ de $v$. Es el error más común del curso.

**Procedimiento**

1. Identifica $K$ y el gradiente $i = dh/dL$ (adimensional).
2. Aplica Darcy en magnitudes: $q = K\,i$.
3. Solo si piden "velocidad real", "velocidad lineal media" o "tiempo de viaje", divide por $n_e$.

**Por qué funciona.** $q$ reparte el caudal sobre **toda** el área transversal, incluyendo granos sólidos. Pero el agua solo pasa por la fracción $n_e$ de esa área. Para que se conserve el caudal:

$$Q = q\,A = v\,(n_e A) \qquad\Longrightarrow\qquad v = \frac{q}{n_e}$$

**Chequeo de unidades.** $K$ en m/s multiplicado por un gradiente adimensional da m/s. Si te sale otra cosa, el gradiente no era adimensional (p. ej., olvidaste dividir por la distancia).

**Truco útil para el parcial.** Convierte siempre a m/año al final: multiplica m/s por $3.156\times10^{7}$. Así "sientes" si el número es razonable. Un acuitardo da centímetros por año; una grava, decenas de metros por día.

## 3.3 — Interpretar una porosidad efectiva de 0.0001

**Qué se evalúa:** criterio hidrogeológico, no cálculo.

**Razonamiento.** Pregúntate: ¿qué material tiene espacio de flujo que es apenas una diezmilésima del volumen? No existe un medio granular así: hasta una arcilla tiene $n>0.4$ (aunque su $n_e$ sea baja). La única respuesta coherente es **roca fracturada**: granito, basalto, gneis o caliza con fisuras, donde el flujo se concentra en un puñado de planos de fractura.

**Por qué importa (lo que da puntos extra).** El mismo $q$ produce velocidades 1000 veces distintas. En roca fracturada un derrame contaminante puede recorrer kilómetros en el tiempo que en arena tardaría siglos. La porosidad efectiva es el parámetro que controla el **tiempo de tránsito**, no el caudal.

## 3.4 y 3.5 — Análisis dimensional

**Qué se evalúa:** que uses $F = MLT^{-2}$ para mezclar los dos sistemas (gravitacional y absoluto).

**Procedimiento universal para cualquier análisis dimensional**

1. Escribe la definición de la cantidad.
2. Reemplaza cada símbolo por sus dimensiones de la tabla 3.1.
3. Si aparecen $F$ y $M$ mezcladas, usa el puente $F = M L T^{-2}$.
4. Cancela.

**Para la altura de presión** ($h_p = P/\rho g$): el enunciado te da $P$ en $F/L^2$, lo cual mezcla fuerza con la masa de $\rho$. Convierte $F$ a $MLT^{-2}$ primero y todo cancela limpiamente hasta $L$.

**Para la carga hidráulica** el argumento más elegante no es dimensional sino energético:

$$h = \frac{\text{energía mecánica del fluido}}{\text{peso del fluido}} = \frac{F\cdot L}{F} = L$$

Esto explica **por qué** la carga se mide en metros: es energía normalizada por peso. Y el potencial hidráulico $\phi = gh$ es la misma energía normalizada por **masa**, por eso tiene unidades de velocidad al cuadrado:

$$\phi = g h \;\Rightarrow\; [\phi] = \frac{L}{T^2}\cdot L = \frac{L^2}{T^2}$$

**Lo que el profesor quiere ver.** Que señales que $\phi$ es la forma "correcta" para fluidos de densidad variable (agua salada, geotermia), porque $h$ pierde sentido cuando $\rho$ no es constante.

## 3.6 — El problema de los tres puntos

**Qué se evalúa:** determinar dirección y magnitud del gradiente a partir de tres piezómetros. Aparece en prácticamente todos los parciales de hidrogeología.

### Método A — Analítico (más rápido y sin errores de dibujo)

**Recomendado si los puntos forman un triángulo rectángulo**, como en este problema.

1. **Coloca un sistema de coordenadas** con el origen en un vértice; define $x$ = Este, $y$ = Norte.
2. **Calcula las componentes del gradiente** por diferencias finitas a lo largo de los ejes:

$$\frac{\partial h}{\partial x} = \frac{\Delta h}{\Delta x}, \qquad \frac{\partial h}{\partial y} = \frac{\Delta h}{\Delta y}$$

3. **Magnitud** por Pitágoras:

$$|\nabla h| = \sqrt{\left(\frac{\partial h}{\partial x}\right)^2+\left(\frac{\partial h}{\partial y}\right)^2}$$

4. **Dirección** del vector gradiente:

$$\theta = \arctan\!\left(\frac{\partial h/\partial y}{\partial h/\partial x}\right)$$

5. **Invierte el sentido** para dar la dirección del flujo. $\nabla h$ apunta hacia carga **creciente**; el flujo va hacia carga **decreciente**.

> **Aquí está la trampa del ejercicio.** Si respondes "N 45° E" das la dirección en que *sube* la carga, no la del flujo. El signo menos de Darcy es la respuesta.

### Método B — Gráfico (el que hay que saber dibujar)

Funciona para **cualquier** configuración de tres puntos, no solo rectángulos:

1. Identifica los puntos de carga **máxima**, **mínima** e **intermedia**.
2. Sobre el segmento que une el punto de carga máxima con el de carga mínima, **interpola linealmente** para localizar el punto que tiene exactamente la misma carga que el punto intermedio.
3. **Une** ese punto interpolado con el punto intermedio: esa recta es una **equipotencial**.
4. Traza la **perpendicular** a la equipotencial desde el punto restante. Esa perpendicular es la dirección del flujo (apuntando hacia la carga menor).
5. El gradiente es

$$i = \frac{\Delta h}{d_\perp}$$

donde $d_\perp$ es la distancia perpendicular medida y $\Delta h$ la diferencia de carga entre el punto y la equipotencial.

**Para este ejercicio:** la equipotencial de 400 m se encuentra interpolando en el segmento A(500)–B(300), que da el punto medio, y uniéndolo con C(400). Los dos métodos dan 0.141 m/m: usa uno y verifica con el otro.

**Sobre el rótulo de 2062 m.** No cuadra con los catetos de 2000 y 1000 m, que darían 2236 m. Da igual: el método solo usa coordenadas. Menciónalo en el examen — demuestra que estás verificando la geometría y no copiando datos.

## 3.7 — Tabla de piezómetros

**Qué se evalúa:** la descomposición $h = z + h_p$ y el uso del gradiente para propagar cargas.

**Orden de resolución (es fijo, no improvises)**

**Paso 1 — Carga total.** Propaga desde el dato conocido usando el gradiente:

$$\Delta h = i\,\Delta L$$

Con $i = 0.019$ y $\Delta L = 5000$ m, cada piezómetro pierde 95 m respecto al anterior. Esta fila se llena primero porque es la única que se puede calcular sin más información.

**Paso 2 — Carga de presión.** Aquí está la clave que hay que *leer* del enunciado: *"el nivel de agua en todos los piezómetros está en el tope del piezómetro"*. Eso significa que la columna de agua dentro del tubo ocupa toda su longitud. Y como la medida se refiere al fondo del piezómetro:

$$\boxed{h_p = \text{profundidad del piezómetro}}$$

Esa frase del enunciado **es** el dato. Sin ella el problema no tiene solución.

**Paso 3 — Carga de elevación.** Por diferencia:

$$z = h - h_p$$

**Verificación obligatoria.** $z$ debe ser la cota del fondo del piezómetro y debe ser **positiva** (los piezómetros están sobre el nivel del mar según la figura) y **coherente con la topografía descendente** de la figura: el terreno baja de A hacia D. Si te sale $z$ negativo o creciente hacia D, revisa.

**Interpretación física que vale puntos.** Observa que $z$ baja de 100 m (A) a 7 m (D): el sistema descarga hacia el mar. Y que $h_p$ cae de 200 a 8 m: los piezómetros se van haciendo someros porque la superficie piezométrica se aproxima al terreno, típico de una **zona de descarga**.

## 3.8 — Conversiones de conductividad y permeabilidad

**Qué se evalúa:** manejo de unidades, que es puro oficio de ingeniero.

**Factores que conviene llevar memorizados**

$$1\ \mathrm{ft} = 0.3048\ \mathrm{m} \qquad 1\ \mathrm{ft^3} = 7.4805\ \mathrm{gal} \qquad 1\ \mathrm{día} = 86\,400\ \mathrm{s}$$

$$1\ \text{darcy} = 9.87\times10^{-9}\ \mathrm{cm^2} = 9.87\times10^{-13}\ \mathrm{m^2}$$

**(a) m/s → ft/s.** Divide por 0.3048. Nada más.

**(b) ft/s → gpd/ft².** El truco conceptual: $K$ en ft/s **es** un caudal por unidad de área ($\mathrm{ft^3/s}$ por $\mathrm{ft^2}$), porque sus unidades $L/T$ son idénticas a $L^3/T$ por $L^2$. Entonces solo conviertes el volumen a galones y el tiempo a días:

$$K\left[\tfrac{\mathrm{gal}}{\mathrm{d\cdot ft^2}}\right] = K\left[\tfrac{\mathrm{ft}}{\mathrm{s}}\right]\times 7.4805 \times 86\,400$$

**(c) K → k.** Invierte la ecuación de la Idea 3:

$$k = \frac{K\mu}{\rho_w g}$$

Y recuerda que $1\ \mathrm{m^2} = 10^{4}\ \mathrm{cm^2}$ (al cuadrado, no $10^2$ — error clásico).

> **Declara siempre la temperatura.** $\mu$ depende de ella: $1.00\times10^{-3}$ Pa·s a 20 °C, $1.124\times10^{-3}$ a 15.6 °C (60 °F, el estándar antiguo americano). La diferencia en el resultado es del 12 %. Escribe la hipótesis y nadie te la puede objetar.

**(d) cm² → darcy.** Divide por $9.87\times10^{-9}$.

**Verificación independiente (hazla siempre).** Para agua a 20 °C:

$$1\ \text{darcy} \approx 9.66\times10^{-6}\ \mathrm{m/s} \approx 0.83\ \mathrm{m/día}$$

Multiplica tu resultado en darcys por $9.66\times10^{-6}$; debe devolverte la $K$ original.

**Sentido físico del resultado.** $K = 10^{-6}$ m/s $\approx 0.1$ darcy es una **arena fina a limo arenoso**: transmite, pero mal. Da el nombre del material en tu respuesta.

## 3.9 — Darcy en términos de presión

**Qué se evalúa:** que entiendas que la forma "de presión" de Darcy es un **caso particular**, no la ley general.

**Desarrollo (hazlo en tres líneas en el examen)**

1. Parte de la forma general y sustituye la definición de carga:

$$q_x = -K\frac{\partial h}{\partial x} = -\frac{k\rho_w g}{\mu}\frac{\partial}{\partial x}\left(z+\frac{P}{\rho_w g}\right)$$

2. Distribuye la derivada:

$$q_x = -\frac{k\rho_w g}{\mu}\frac{\partial z}{\partial x} - \frac{k}{\mu}\frac{\partial P}{\partial x}$$

3. Anula el primer término imponiendo $\partial z/\partial x = 0$.

**La condición, dicha en palabras:** las dos presiones deben medirse **a la misma elevación**. Si comparas la presión al fondo de dos barrenos de distinta profundidad, la diferencia de presión incluye la columna de agua por diferencia de cota y la fórmula falla.

**Dibujo que debes hacer:**

```
         barreno 1                      barreno 2
            ||                              ||
  ----------||------------------------------||---------  superficie
            ||                              ||
            ||                              ||
            ||          FLUJO ------>       ||
  ==========\/==============================\/=========  misma cota z
            P1                              P2            <- manometros a
                                                             IGUAL elevacion
  ######################################################  base impermeable

  q_x = -(k/mu)(P2 - P1)/L      valido solo si z1 = z2
```

**Condiciones completas para la respuesta:**

1. Flujo horizontal (o presiones medidas a igual cota): $\partial z/\partial x = 0$.
2. Fluido homogéneo, $\rho$ y $\mu$ constantes (isotérmico, salinidad uniforme).
3. Medio con $k$ uniforme en el intervalo considerado.
4. Flujo laminar ($Re < 1$–10), condición de validez de Darcy en general.

## 3.10 — Detectar expresiones incorrectas de Darcy

**Qué se evalúa:** rigor. Hay dos tipos de error en la lista y conviene separarlos explícitamente.

**Estrategia de revisión en tres pasadas**

**Pasada 1 — ¿Dimensiones?** Verifica cada expresión con la tabla 3.1. Sorpresa: todas pasan. Por ejemplo (c), que parece rara:

$$\left[\frac{K}{g}\nabla\phi\right] = \frac{L/T}{L/T^2}\cdot\frac{L^2/T^2}{L} = T\cdot\frac{L}{T^2} = \frac{L}{T}\ \checkmark$$

Como ninguna falla por dimensiones, el error es de otro tipo.

**Pasada 2 — ¿Signo?** La forma vectorial de Darcy **exige** el menos. Marca todas las que lo omitan: b, c, e, f y g.

**Pasada 3 — ¿Relación física invertida?** Busca la que confunde $q$ con $v$. La (d) dice $q = v/n_e$, cuando lo correcto es $v = q/n_e$. Como $n_e<1$, la (d) afirma que la descarga específica es mayor que la velocidad real: físicamente imposible.

**Cómo redactar la respuesta (esto es lo que la hace completa)**

> Con el criterio vectorial estricto, todas excepto (a) son incorrectas: (b), (c), (e), (f) y (g) omiten el signo negativo, y (d) además invierte la relación entre $q$ y $v$. Si se interpretan todas en magnitudes (ignorando signos), la única intrínsecamente errónea es (d).

Declarar el criterio antes de responder es lo que distingue una respuesta de 5.0.

**Nota sobre equivalencias que debes reconocer:** (b), (c) y (g) son **la misma ecuación** escrita de tres formas, porque $\phi = gh$ y $K = k\rho g/\mu$. Igual que (e) y (f). Señalarlo demuestra que entiendes las definiciones y no estás comparando símbolos.

## 3.11 — Capas: conductividad equivalente

**Qué se evalúa:** la analogía eléctrica. Es el ejercicio más mecánico del capítulo si entiendes el concepto.

**La analogía que hay que tener en la cabeza**

| Hidráulica | Electricidad |
|---|---|
| Carga $h$ | Voltaje |
| Caudal $Q$ | Corriente |
| $L/(KA)$ | Resistencia |

**Flujo HORIZONTAL (paralelo a las capas)**

El agua puede escoger por qué capa viajar, y cada capa ve **la misma** pérdida de carga sobre la misma longitud: es un circuito en **paralelo**. Los caudales se suman:

$$Q_{total} = \sum Q_i \;\Longrightarrow\; K_h\left(\sum b_i\right)i = \sum (K_i b_i i)$$

$$\boxed{K_h = \frac{\sum K_i b_i}{\sum b_i}} \qquad\text{media ARITMÉTICA ponderada}$$

**Flujo VERTICAL (perpendicular a las capas)**

El agua está **obligada** a cruzar todas las capas en secuencia: circuito en **serie**. El caudal es el mismo en todas y las pérdidas de carga se suman:

$$\Delta h_{total} = \sum \Delta h_i \;\Longrightarrow\; \frac{\sum b_i}{K_v} = \sum\frac{b_i}{K_i}$$

$$\boxed{K_v = \frac{\sum b_i}{\sum (b_i/K_i)}} \qquad\text{media ARMÓNICA ponderada}$$

**Cómo no confundirlas nunca más**

$$\boxed{K_h \text{ la domina la capa MÁS permeable} \qquad K_v \text{ la domina la capa MENOS permeable}}$$

El flujo horizontal se escapa por la "autopista"; el vertical queda atrapado en el "cuello de botella". Y siempre $K_v \le K_h$.

**Verificación obligatoria.** Comprueba que $K_h$ quede cerca del $K$ mayor ($10^{-6}$) y $K_v$ cerca del menor ($10^{-8}$). En este ejercicio $K_h = 3.7\times10^{-7}$ y $K_v = 2.7\times10^{-8}$: ✓

**Conclusión que debes escribir.** Una secuencia estratificada, aunque cada capa sea isótropa, se comporta a escala macroscópica como un medio **anisótropo** con $K_h/K_v = 13.7$. Esto explica por qué las plumas contaminantes se extienden lateralmente y por qué los acuíferos regionales son "planos".

## 3.12 — Términos cruzados del tensor de conductividad

**Qué se evalúa:** que sepas que en un medio anisótropo $K$ es un **tensor**, de modo que un gradiente en $x$ puede producir flujo en $y$.

**La ley de Darcy completa en 2D**

$$q_x = -\left(K_{xx}\frac{\partial h}{\partial x} + K_{xy}\frac{\partial h}{\partial y}\right)$$

$$q_y = -\left(K_{yx}\frac{\partial h}{\partial x} + K_{yy}\frac{\partial h}{\partial y}\right)$$

**Procedimiento en tres pasos**

**Paso 1 — Usa el primer ensayo para despejar el término cruzado.** El enunciado dice que **no hay gradiente en $y$**, por lo que el segundo término de la ecuación de $q_y$ desaparece y queda un solo incógnito:

$$q_y = K_{yx}\frac{\partial h}{\partial x} \;\Longrightarrow\; K_{yx} = \frac{q_y}{\partial h/\partial x}$$

**Paso 2 — Invoca la simetría del tensor.** Este es el concepto que se está evaluando:

$$\boxed{K_{xy} = K_{yx}}$$

El tensor de conductividad hidráulica es **simétrico** (consecuencia de la reciprocidad de Onsager en la termodinámica de procesos irreversibles). Sin esta propiedad el problema no tendría solución: el primer ensayo mide $K_{yx}$ y el segundo pregunta por $K_{xy}$.

**Paso 3 — Aplica al segundo ensayo.** Ahora no hay gradiente en $x$:

$$q_x = K_{xy}\frac{\partial h}{\partial y}$$

**Verificación de coherencia.** El gradiente del segundo ensayo es 10 veces menor que el del primero (0.01 frente a 0.1), y el flujo cruzado resultante es 10 veces menor ($10^{-4}$ frente a $10^{-3}$). La proporcionalidad directa confirma el resultado.

**Significado físico.** $K_{xy}\ne 0$ significa que **los ejes de coordenadas no coinciden con los ejes principales de anisotropía** del medio (por ejemplo, una estratificación inclinada respecto al sistema x–y). En consecuencia, **$\mathbf{q}$ no es paralelo a $\nabla h$**: el flujo se desvía respecto a la máxima pendiente de la superficie piezométrica. Esta es la razón por la que en medios anisótropos las líneas de flujo **no** cortan a las equipotenciales a 90°.

## 3.13 — Leer conductividades relativas en una red de flujo

**Qué se evalúa:** interpretación de redes de flujo, que es la habilidad central del capítulo 4.

**El razonamiento, paso a paso**

**Paso 1 — Impón continuidad.** El enunciado dice "entrada = salida, no se agrega ni se pierde agua". Por lo tanto el mismo $Q$ cruza **todas** las secciones:

$$Q = K_1 A_1\frac{\Delta h}{L_1} = K_2 A_2\frac{\Delta h}{L_2} = K_3 A_3\frac{\Delta h}{L_3}$$

**Paso 2 — Nota que $\Delta h$ es el mismo.** Las "lines of equal head" de la figura están dibujadas con intervalo constante. Esto es crucial: $\Delta h$ se cancela.

**Paso 3 — Despeja.**

$$\boxed{K_i = \frac{Q\,L_i}{A_i\,\Delta h} \;\Longrightarrow\; K_i \propto \frac{L_i}{A_i}}$$

**Paso 4 — Mide la figura con regla.** $L_i$ = separación entre equipotenciales consecutivas; $A_i = \bar b_i \times$ ancho (el ancho es el mismo, se cancela), con $\bar b_i$ el espesor medio de la franja.

**Paso 5 — Interpreta.**

$$\boxed{\begin{array}{l}
\text{Equipotenciales MUY SEPARADAS} \Rightarrow \text{gradiente pequeño} \Rightarrow K \text{ ALTA}\\
\text{Equipotenciales MUY JUNTAS} \Rightarrow \text{gradiente grande} \Rightarrow K \text{ BAJA}
\end{array}}$$

**La intuición correcta.** Para mover el mismo caudal, un material bueno necesita "poco empujón" (gradiente bajo, equipotenciales separadas) y un material malo necesita "mucho empujón" (gradiente alto, equipotenciales apretadas). Es idéntico a un circuito en serie: la resistencia grande se come la mayor parte del voltaje.

**El factor que no debes olvidar: el espesor.** Si el acuífero se adelgaza, el área disminuye y hace falta más gradiente **aunque $K$ no cambie**. Por eso el criterio completo es $L/A$ y no solo $L$. Un adelgazamiento puede imitar una caída de $K$: ese es exactamente el matiz que el ejercicio quiere que detectes.

**Para el inciso (c)** simplemente divide:

$$\frac{K_{max}}{K_{min}} = \frac{L_{max}/A_{max}}{L_{min}/A_{min}}$$

> Mide tu figura y reporta tus valores. El profesor evalúa el criterio $K\propto L/A$, no el tercer decimal.

## 3.14 — Efecto de la recarga y la descarga en el espaciamiento

**Qué se evalúa:** la ecuación de continuidad aplicada cualitativamente. Es el problema conceptual más bonito del capítulo.

**Caso de referencia.** Si entrada = salida, $Q$ es constante; con $K$ y $A$ constantes, $i = Q/(KA)$ es constante y las equipotenciales están **uniformemente espaciadas**.

**El razonamiento maestro (sirve para los dos incisos)**

$$i = \frac{Q}{K A} \qquad\text{con } K, A \text{ constantes}\qquad\Longrightarrow\qquad i \propto Q$$

Y el espaciamiento entre equipotenciales es **inversamente** proporcional al gradiente:

$$L = \frac{\Delta h}{i}$$

Así que solo hay que preguntarse: **¿qué le pasa a $Q$ en la dirección del flujo?**

**(a) Recarga uniforme** (la pista del enunciado, "inflow ≠ outflow", es que se agrega agua):

$$Q \nearrow \;\Longrightarrow\; i \nearrow \;\Longrightarrow\; L \searrow$$

$$\boxed{\text{Las equipotenciales se JUNTAN progresivamente en la dirección del flujo}}$$

La superficie potenciométrica se vuelve **convexa hacia arriba** (como una loma). Cada metro que avanza el agua, recibe más agua de arriba y necesita más gradiente para evacuarla.

**(b) Descarga natural uniforme** (evapotranspiración, manantiales, goteo ascendente):

$$Q \searrow \;\Longrightarrow\; i \searrow \;\Longrightarrow\; L \nearrow$$

$$\boxed{\text{Las equipotenciales se SEPARAN progresivamente en la dirección del flujo}}$$

La superficie potenciométrica se vuelve **cóncava hacia arriba** (como un cuenco).

**Dibujo para la respuesta:**

```
  (a) RECARGA uniforme                  (b) DESCARGA uniforme
   lluvia  | | | | | | |                  ET  ^ ^ ^ ^ ^ ^ ^
          _v_v_v_v_v_v_                       | | | | | | |
      ___/             \___                __
   __/      convexa        \__            |  \___  concava   ___
  /                           \           |      \_________/
  | |  |  |  | | ||||               | | ||  |  |   |    |     |
  equipotenciales JUNTANDOSE        equipotenciales SEPARANDOSE
  ------ flujo ------>              ------ flujo ------>
```

**Aplicación práctica (añádela y gana puntos).** Este es el criterio de campo para **identificar zonas de recarga y descarga en un mapa potenciométrico real** sin ningún otro dato: contornos que se aprietan en la dirección del flujo indican recarga; contornos que se abren indican descarga o aumento de transmisividad. El reto del hidrogeólogo es precisamente separar ese efecto del de los cambios de $K$ y de espesor (problema 3.13).

## 3.15 — Fuga vertical a través de una arcilla

**Qué se evalúa:** aplicar Darcy en vertical y determinar el sentido correctamente.

**Procedimiento**

**Paso 1 — Calcula el gradiente vertical en cada región.** Como $b'$ (espesor de la arcilla) y $K'$ son los mismos en todo el dominio:

$$q_z = K'\frac{\Delta h}{b'} \;\Longrightarrow\; q_z \propto \Delta h$$

**Paso 2 — Compara las diferencias de carga.** En $h_4$: $70 - 60 = 10$ m. En $h_1$: $30 - 25 = 5$ m.

**Paso 3 — Concluye.** La región de $h_4$ tiene el doble de gradiente, por tanto **el doble de velocidad vertical**.

$$\frac{q_{z,h_4}}{q_{z,h_1}} = \frac{10}{5} = 2$$

**Paso 4 — Determina el sentido.** Regla única: **el flujo va desde donde la carga es mayor hacia donde es menor**.

| Región | Acuífero superior | Acuífero inferior | ¿Cuál es mayor? | Sentido |
|---|---|---|---|---|
| $h_4$ | 70 m | 60 m | superior | **descendente** |
| $h_1$ | 30 m | 25 m | superior | **descendente** |

En **ambas** regiones el flujo es hacia abajo. Hay fuga descendente en todo el dominio.

**El error que hay que evitar.** Mirar las cargas absolutas (70 vs. 30) y concluir que el flujo vertical va "de $h_4$ hacia $h_1$". El flujo horizontal sí va en ese sentido, pero el flujo **vertical** lo controla únicamente la diferencia de carga **entre acuíferos en el mismo punto**. Son dos componentes independientes del mismo vector.

**Interpretación hidrogeológica (vale puntos).** $h_4$ = 70 m es la parte alta del sistema: **zona de recarga**, con componente descendente fuerte. $h_1$ = 30 m es la parte baja: también hay fuga descendente, pero más débil. El sistema inferior está siendo recargado a través del acuitardo en toda su extensión. Si en $h_1$ la carga inferior hubiera sido *mayor* que 30 m, tendríamos una zona de descarga ascendente, que es la situación peligrosa de los problemas 4.4 y 5.4.

## 3.16 — Descarga específica a través de la capa confinante

**Qué se evalúa:** leer cargas de una figura y aplicar Darcy. Es el ejercicio más directo, pero la lectura de la figura es donde se pierden puntos.

**Cómo leer la figura**

```
   ___________        _____________          _____________
  |           |      |      |      |        |             |
  | 10 m  ^   |      |      |      |        | Capa        |   <- espesor de la
  |       |   |      |      |      |        | confinante  |      confinante: 10 m
  |_______v___|______|______|______|________|_____________|
          |                 |
      100 m (nivel          95 m (nivel en el piezometro
      en el piezometro      que penetra el ACUIFERO)
      somero)                            ACUIFERO
  __________________________________________________ Datum
```

**Paso 1 — Identifica las dos cargas y el espesor que las separa.** Carga arriba: 100 m. Carga abajo: 95 m. Espesor de la capa confinante: $b' = 10$ m.

**Paso 2 — Gradiente vertical.**

$$i = \frac{\Delta h}{b'} = \frac{100-95}{10} = 0.5\ \mathrm{m/m}$$

> Un gradiente de 0.5 es enorme comparado con los gradientes horizontales típicos ($10^{-3}$). Esto es normal en acuitardos: concentran casi toda la pérdida de carga del sistema. Si te sale un gradiente vertical pequeño en un acuitardo, revisa que no hayas usado una longitud equivocada.

**Paso 3 — Darcy.** $q = K' i$. Deja el resultado en las unidades que te dan $K'$ (cm/s aquí) para no introducir errores de conversión.

**Paso 4 — Sentido.** De 100 m hacia 95 m: **descendente**.

**Paso 5 — Da perspectiva al número.** Convierte a cm/año: $5\times10^{-8}$ cm/s $\times 3.156\times10^{7}$ s/año $\approx 1.6$ cm/año. Esa cifra, multiplicada por el área en planta, es el agua que el acuífero confinado recibe por fuga: pequeña por unidad de área, pero enorme integrada sobre decenas de km².

## 3.17 — Sistema de dos acuíferos con fuga (el problema integrador)

**Qué se evalúa:** balance de masa combinado con Darcy horizontal y vertical. Es el ejercicio más completo del capítulo y el más probable en un parcial.

**Estrategia: resuélvelo como un balance, no como una fórmula**

### Paso 1 — Extrae la geometría de la figura

```
                                      100 m (ancho)
          1000 m (longitud)      <------------->
    <------------------------->
     ___________________________________
    /                                   /|
   /     ACUIFERO SUPERIOR             / | 10 m   <- A = 10 x 100 = 1000 m2
  /___________________________________/  |
 /     CAPA CONFINANTE  K'=1e-9      /|  | 20 m   <- A_planta = 1000 x 100
/___________________________________/ |  |                    = 1e5 m2
|                                   | |  |
|      ACUIFERO INFERIOR            | | /  10 m   <- A = 1000 m2
|___________________________________|_|/
  --> Inflow (i = 0.1)                      --> Outflow
```

Dos áreas distintas, y confundirlas es el error que arruina el problema:

| Para flujo | Área | Valor |
|---|---|---|
| **Horizontal** (en los acuíferos) | transversal = espesor × ancho | $10\times100 = 1000\ \mathrm{m^2}$ |
| **Vertical** (fuga por la confinante) | en planta = longitud × ancho | $1000\times100 = 10^{5}\ \mathrm{m^2}$ |

### Paso 2 — Caudal de entrada (inciso a)

Darcy horizontal con el gradiente de entrada que da el enunciado:

$$Q_{in} = K\,i\,A_{transversal}$$

Como los dos acuíferos tienen igual $K$, igual espesor e igual gradiente de entrada, entran caudales **idénticos**.

### Paso 3 — Fuga vertical (la clave del inciso b)

$$q_{fuga} = K'\frac{\Delta h}{b'} = K'\frac{10\ \mathrm{m}}{20\ \mathrm{m}}$$

$$Q_{fuga} = q_{fuga}\times A_{planta}$$

**Dirección:** el acuífero inferior tiene cargas 10 m **más altas**, así que la fuga es **ascendente**, del inferior al superior.

> Nota que $K'$ es mil veces menor que $K$, pero el área en planta es **cien veces mayor** que la transversal. Esa competencia entre un $K$ minúsculo y un área enorme es la razón por la que la fuga a través de acuitardos no se puede despreciar: aquí resulta ser el **50 %** del caudal de entrada.

### Paso 4 — Balance de masa en cada acuífero (inciso b)

Escribe el balance por separado. Esto es lo que se evalúa:

$$\boxed{Q_{out} = Q_{in} \pm Q_{fuga}}$$

- Acuífero **superior**: **recibe** la fuga → $Q_{out} = Q_{in} + Q_{fuga}$
- Acuífero **inferior**: **cede** la fuga → $Q_{out} = Q_{in} - Q_{fuga}$

**Verificación obligatoria:** la suma de las dos salidas debe igualar la suma de las dos entradas. El agua que cambia de acuífero no se pierde del sistema. Si no cierra, hay un error aritmético.

### Paso 5 — Gradientes de salida (inciso c)

Invierte Darcy, usando de nuevo el área **transversal**:

$$i_{out} = \frac{Q_{out}}{K\,A_{transversal}}$$

El resultado tiene sentido inmediato: el acuífero que gana agua necesita **más** gradiente para evacuarla (0.15), y el que la pierde necesita **menos** (0.05).

### Paso 6 — Dibujo de las superficies piezométricas (inciso d)

Lo que hay que mostrar:

1. Ambas empiezan con pendiente 0.1 en la entrada.
2. La del acuífero **inferior se aplana** (0.10 → 0.05): cóncava hacia arriba.
3. La del acuífero **superior se empina** (0.10 → 0.15): convexa hacia arriba.
4. **Convergen**: la separación de 10 m se reduce aguas abajo.
5. La inferior siempre queda **por encima** de la superior (es lo que mantiene la fuga ascendente).

```
  carga
    ^
    |  *..                           acuifero INFERIOR
    |     '*...                      (pierde agua -> se APLANA)
    |          '**....                i: 0.10 --> 0.05
    |                '*****.......
    |
    |  o.
    |    'o..                        acuifero SUPERIOR
    |       'oo..                    (gana agua -> se EMPINA)
    |           'oo.                  i: 0.10 --> 0.15
    |              'oo
    +------------------------------------> distancia
       entrada                 salida
```

**El concepto grande.** Este es el mecanismo de los **acuíferos semiconfinados (leaky aquifers)** y la base de la teoría de Hantush-Jacob. Nota el acoplamiento: al converger las superficies, $\Delta h$ disminuye y la fuga también. Un cálculo riguroso requeriría resolver las dos ecuaciones acopladas; el enunciado te permite usar $\Delta h = 10$ m promedio. **Dilo explícitamente en el examen**: demuestra que sabes qué estás simplificando.

---

<a name="parte-ii"></a>
# Parte II — Capítulo 4: Ecuaciones de flujo, fronteras y redes

## 4.1 — Simplificar la ecuación general de flujo

**Qué se evalúa:** que entiendas **de dónde sale cada término** de la ecuación 4.31, no que la memorices.

**Anatomía de la ecuación**

$$\underbrace{\nabla^2 h}_{\text{(1) desbalance de flujo}} = \underbrace{\frac{\rho_w g(\overbrace{\beta_p}^{\text{(2)}} + \overbrace{n\beta_w}^{\text{(3)}})}{K}}_{S_s/K}\ \underbrace{\frac{\partial h}{\partial t}}_{\text{(4) cambio de carga}}$$

| Término | Qué representa |
|---|---|
| (1) $\nabla^2 h$ | lo que entra menos lo que sale en un volumen de control (vía Darcy) |
| (2) $\beta_p$ | compresibilidad de la **matriz** del acuífero: el esqueleto se compacta y expulsa agua |
| (3) $n\beta_w$ | compresibilidad del **agua**: el agua se expande al despresurizarse |
| (4) $\partial h/\partial t$ | tasa de cambio del almacenamiento |

Y el **almacenamiento específico**:

$$S_s = \rho_w g(\beta_p + n\beta_w) \qquad [L^{-1}]
\qquad\qquad
S = S_s\,b \qquad [\text{adimensional}]$$

**Cómo responder cada inciso**

**(a) Unidimensional.** El laplaciano en 1D es simplemente la segunda derivada en una dirección:

$$\nabla^2 h = \frac{\partial^2h}{\partial x^2}+\frac{\partial^2h}{\partial y^2}+\frac{\partial^2h}{\partial z^2} \;\longrightarrow\; \frac{\partial^2 h}{\partial x^2}$$

Nombra la ecuación resultante: es la **ecuación de difusión** (idéntica a la del calor), con difusividad hidráulica $\nu = K/S_s = T/S$.

**(b) Fluido incompresible.** "Incompresible" se traduce matemáticamente en $\beta_w = 0$. Táchalo y queda solo la compresibilidad de la matriz. Interpretación: **todo** el agua que sale del almacenamiento proviene de la compactación del esqueleto.

**(c) Fluido y matriz incompresibles.** $\beta_p = \beta_w = 0$, el lado derecho se anula completo:

$$\nabla^2 h = 0$$

Nómbrala: **ecuación de Laplace**. Y di lo que implica: no hay almacenamiento, de modo que entrada = salida en todo instante, régimen permanente. **Es la ecuación que gobierna todas las redes de flujo** de los problemas 4.6 a 4.10. Esta conexión es lo que el profesor quiere ver.

**(d) ¿Cuándo despreciar $\rho_w g\,n\beta_w$?**

Compara órdenes de magnitud. $n\beta_w \approx 0.3\times4.8\times10^{-10} \approx 1.4\times10^{-10}\ \mathrm{m^2/N}$, un valor **fijo**. Luego el criterio es: ¿en qué material $\beta_p \gg 1.4\times10^{-10}$?

| Material | $\beta_p$ (m²/N) aproximada | ¿Se puede despreciar $n\beta_w$? |
|---|---|---|
| **Arcilla** | $10^{-6}$ a $10^{-8}$ | **Sí**, por 2–4 órdenes de magnitud |
| Arena/limo | $10^{-8}$ a $10^{-9}$ | Sí, con cuidado |
| Grava | $10^{-9}$ a $10^{-10}$ | Marginal |
| Caliza | $10^{-10}$ | No |
| Granito, siltstone cementado | $10^{-10}$ a $10^{-11}$ | **No**, es el término dominante |

$$\boxed{\text{Respuesta: ARCILLA}}$$

**La frase que remata la respuesta:** en materiales rígidos (granito, caliza) ocurre lo **contrario**: la compresibilidad del agua domina y es $\beta_p$ el que se desprecia. Por eso la arcilla y los acuitardos liberan tantísima más agua por unidad de descenso de carga (y por eso se produce la subsidencia del terreno).

## 4.2 — Almacenamiento de un acuífero elástico

**Qué se evalúa:** la ecuación del almacenamiento y la definición operacional de $S$.

**Las dos ecuaciones que necesitas**

$$\boxed{S = \rho_w g\,b\,(\beta_p + n\beta_w)} \qquad\text{(definición física)}$$

$$\boxed{V = S\cdot A\cdot\Delta h} \qquad\text{(definición operacional)}$$

**(a) Volumen extraído.** Aplicación literal de la definición de $S$: *"volumen de agua liberado por unidad de área de acuífero por unidad de descenso de carga"*. Si entiendes la definición, el cálculo es una multiplicación.

Reconstrucción dimensional para no equivocarse:

$$[V] = [\,\cdot\,]\cdot L^2 \cdot L = L^3 \;\Rightarrow\; S \text{ es adimensional}\ \checkmark$$

**Da perspectiva al resultado.** El volumen obtenido equivale a una lámina de agua de solo **0.3 mm** repartida sobre 1 km². Eso es lo asombroso de los acuíferos confinados: para producir volúmenes útiles hay que **bajar muchísimo la carga** sobre áreas enormes. Es la causa física de los conos de abatimiento gigantescos de los acuíferos confinados frente a los libres (donde $S_y \sim 0.2$, cuatro órdenes de magnitud mayor).

**(b) Con matriz incompresible.** Táchale $\beta_p$ a la ecuación de $S$ y calcula el resto.

**Interpreta el resultado:** sale ~28 % del $S$ real. Conclusión para escribir: *el 72 % del agua que produce este acuífero proviene de la compactación del esqueleto, no de la expansión del agua*. Y en consecuencia, bombearlo **produce subsidencia del terreno**.

**(c) Compresibilidad vertical de la matriz.** Despeja $\beta_p$ de la misma ecuación:

$$\beta_p = \frac{S}{\rho_w g\,b} - n\beta_w$$

**Verificación obligatoria.** Sustituye el $\beta_p$ obtenido de vuelta en la ecuación de $S$ y comprueba que recuperas $3\times10^{-4}$. Si $\beta_p$ te sale **negativo**, el enunciado sería físicamente imposible (significaría que la matriz se expande al cargarla); eso indica error aritmético.

**Contexto para la respuesta.** $\beta_p \approx 3.7\times10^{-10}\ \mathrm{m^2/N}$ corresponde a arena o grava densa. Su inverso, el módulo de compresión $1/\beta_p \approx 2.7$ GPa, es del orden del módulo volumétrico del agua ($2.2$ GPa): justamente por eso ambos términos compiten en este acuífero.

## 4.3 — El significado de $S$ en una prueba de bombeo

**Qué se evalúa:** interpretación conceptual. No hay números y se responde en una línea cada inciso, pero hay que entenderlo.

**La lógica.** Parte de la definición operacional, $V = S\,A\,\Delta h$, y pregúntate qué resulta en cada caso.

**(a)** "Tasa de descenso de carga × almacenamiento, integrada sobre el área":

$$\int_A S\,\frac{\partial h}{\partial t}\,dA$$

Dimensionalmente: (adimensional) × ($L/T$) × ($L^2$) = $L^3/T$. Es un **caudal**. Y por conservación de masa, el único caudal que sale del sistema es el del pozo:

$$\boxed{= \text{el caudal de bombeo } Q}$$

**(b)** "Descenso total de carga, integrado sobre el área, × almacenamiento":

$$\int_A S\,\Delta h\,dA$$

Dimensionalmente: (adimensional) × ($L$) × ($L^2$) = $L^3$. Es un **volumen**:

$$\boxed{= \text{el volumen total extraído del almacenamiento hasta ese instante} = Q\,t}$$

**Por qué esto importa.** Es el fundamento de los métodos de **balance volumétrico** para estimar $S$ en campo: si mides el cono de abatimiento completo (su volumen) y conoces el volumen bombeado, obtienes $S$ sin necesidad de la solución de Theis. Y es también la razón de que **todo** el agua bombeada de un acuífero elástico infinito venga del almacenamiento: no existe estado estacionario; el cono crece indefinidamente.

## 4.4 — Esfuerzos totales, neutros y efectivos (problema clave)

**Qué se evalúa:** el principio del esfuerzo efectivo. Este problema, o uno casi idéntico, aparece en el parcial con alta probabilidad.

### El esquema mental

```
  ===== superficie del terreno (nivel freatico aqui) =====
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::
  ::::::::::  ARCILLA  gamma_sat = 125 lb/ft3  ::::::::::   50 ft
  :::::::::::::::::::::::::::::::::::::::::::::::::::::::
  ------------------- base de la arcilla ------------------  <- PUNTO DE ANALISIS
  ooooooooooo ARENA ARTESIANA ooooooooooooooooooooooooooooo

     El piezometro que penetra la arena sube 20 ft SOBRE
     el terreno  ==>  h_p en la base = 50 + 20 = 70 ft
```

### Las tres cantidades, cada una con su regla

**1. Esfuerzo total $\sigma_T$** — el **peso** de todo lo que está encima, por unidad de área:

$$\sigma_T = \sum \gamma_i\,z_i$$

Suma el peso de cada capa (suelo con $\gamma_{sat}$, agua con $\gamma_w$). **Depende de la excavación**: si quitas material, baja.

**2. Presión neutra $u$** (presión de poro) — la presión del **agua** en el punto:

$$u = \gamma_w\,h_p$$

donde $h_p$ es la **carga de presión medida en el piezómetro**. Aquí está el concepto central del problema:

$$\boxed{u \text{ NO depende de la excavación: la controla el acuífero artesiano}}$$

El acuífero está conectado a una zona de recarga lejana. Excavar 20 ft de arcilla no cambia la presión del acuífero. **Esta es la observación que resuelve todo el problema.**

**3. Esfuerzo efectivo $\sigma'$** — lo que realmente soporta el esqueleto:

$$\sigma' = \sigma_T - u$$

### Cómo calcular $h_p$ (donde más se falla)

El piezómetro está en la base de la arcilla (50 ft de profundidad) y el agua sube **20 ft sobre el terreno**. La columna de agua total desde el punto de medida hasta el nivel de agua es:

$$h_p = 50 + 20 = 70\ \mathrm{ft}$$

> Si pones $h_p = 20$ ft estás midiendo solo la parte artesiana. Si pones 50 ft estás ignorando el artesianismo. La carga de presión es la **altura total de la columna de agua por encima del punto**.

### Inciso (a) — Condición original

Aplica las tres fórmulas directamente. Calcula también el factor de seguridad $FS = \sigma_T/u$ aunque no lo pidan: le da sentido al número.

### Inciso (b) — Zanja de 20 ft llena de agua

**Lo que cambia:** solo $\sigma_T$. Ahora encima del punto hay 30 ft de arcilla **más** 20 ft de agua:

$$\sigma_T = \gamma_{sat}(50-20) + \gamma_w(20)$$

**Lo que NO cambia:** $u$, porque sigue siendo 70 ft de carga de presión en el acuífero.

**El resultado interesante:** $\sigma'$ se desploma de 1882 a 630 lb/ft² (un 66 % de pérdida) por excavar solo el 40 % del espesor. La razón: el agua que rellena la zanja pesa la mitad que la arcilla que reemplazó, así que cada pie excavado cuesta $125-62.4 = 62.6$ lb/ft² de esfuerzo efectivo.

### Inciso (c) — ¿Se puede desecar?

**Procedimiento:** recalcula $\sigma_T$ sin la columna de agua y compara con $u$.

$$\sigma_T = \gamma_{sat}(30) = 3750 < u = 4368$$

$$\sigma' = -618\ \mathrm{lb/ft^2} \;\Longrightarrow\; FS = 0.86 < 1$$

**Respuesta: NO.** Y hay que explicar por qué: un esfuerzo efectivo negativo no tiene sentido físico, lo cual indica que **antes de alcanzar ese estado el suelo falla**. La presión artesiana levanta el tapón de arcilla: se produce un **reventón de fondo** (*blowout* o *quick condition*), el agua irrumpe con arena y la excavación se inunda y se desestabiliza.

**Soluciones de ingeniería (incluye esto, es lo que pide un parcial de posgrado):**

1. **Despresurizar el acuífero** con pozos de alivio antes de desecar. La carga máxima admisible para $FS = 1$ es $h_p = \sigma_T/\gamma_w = 3750/62.4 = 60.1$ ft, de modo que hay que bajar la carga **al menos 10 ft** (y más, para $FS\ge1.3$).
2. **Mantener la zanja inundada** y excavar con draga (es lo del inciso b).
3. Dejar un **tapón de arcilla más grueso** o lastrarlo.

### Inciso (d) — Profundidad crítica

**Monta la ecuación de la condición crítica** ($\sigma' = 0$, es decir $\sigma_T = u$) con la profundidad $d$ como incógnita:

$$\gamma_{sat}(D-d) + \gamma_w\,d = \gamma_w\,h_p$$

**Despeja:**

$$\boxed{d_{crit} = \frac{\gamma_{sat}D - \gamma_w h_p}{\gamma_{sat}-\gamma_w} = \frac{\sigma'_{inicial}}{\gamma_{sat}-\gamma_w}}$$

**La forma final es muy elegante y vale la pena memorizarla:** el esfuerzo efectivo inicial dividido por el **peso sumergido** de la arcilla ($\gamma_{sat} - \gamma_w = \gamma'$). Dice: "tengo 1882 lb/ft² de margen y cada pie que excavo me cuesta 62.6 lb/ft²".

**Verifica siempre** sustituyendo $d_{crit}$ en las fórmulas originales y comprobando que $\sigma_T = u$.

**Caso en seco (ejercicio que deberías hacer tú):** si la zanja no se rellena de agua, $\gamma_w d$ desaparece del lado izquierdo y

$$d_{crit} = D - \frac{\gamma_w h_p}{\gamma_{sat}} = 15.1\ \mathrm{ft}$$

¡La mitad! Rellenar la excavación con agua **duplica** la profundidad alcanzable. Esa comparación es el aprendizaje práctico del ejercicio.

## 4.5 — Transmisividad a partir de una red de flujo

**Qué se evalúa:** que sepas que una red de flujo bien trazada **es** un instrumento de medida.

**El concepto fundamental de las redes de flujo cuadradas**

Si las celdas de la red son "cuadrados curvilíneos" (ancho del tubo de flujo $\approx$ separación entre equipotenciales), entonces **cada tubo de flujo transporta exactamente el mismo caudal**, y ese caudal vale:

$$\Delta Q = T\,\Delta h$$

**Demostración en dos líneas** (hazla en el examen, es corta y vale mucho). Para una celda cuadrada de lado $a$, con transmisividad $T$:

$$\Delta Q = T\,(\text{ancho})\frac{\Delta h}{\text{largo}} = T\,a\,\frac{\Delta h}{a} = T\,\Delta h$$

El lado $a$ se cancela. **Ahí está la magia de las celdas cuadradas**: el caudal por tubo no depende del tamaño de la celda, solo de $T$ y del intervalo de carga.

**Procedimiento del problema**

**Paso 1 — Determina $\Delta h$.** Es el intervalo entre curvas equipotenciales de la figura. La leyenda de la figura 4.10 dice "Altitude, in feet below sea level" y las curvas van 20, 30, 40, 50, 60, 70, de modo que $\Delta h = 10$ ft. **Conviértelo a metros** ($3.048$ m), porque $Q$ está en m³/día.

**Paso 2 — Cuenta los tubos de flujo que convergen al centro de bombeo B.** Son los "flow lines" (líneas discontinuas) que terminan en el cono de B. Cuenta los **tubos** (espacios entre líneas), no las líneas.

**Paso 3 — Impón la conservación de masa.** Todo lo que se bombea en B tuvo que entrar por esos tubos:

$$Q = n_f\,\Delta Q = n_f\,T\,\Delta h$$

**Paso 4 — Despeja.**

$$\boxed{T = \frac{Q}{n_f\,\Delta h}}$$

**Paso 5 — Verifica que el resultado sea geológicamente razonable.** Con $T \approx 1200\ \mathrm{m^2/día}$ y un espesor plausible de 30 m para la Formación Patuxent:

$$K = \frac{T}{b} = \frac{1200}{30} = 40\ \mathrm{m/día} = 4.6\times10^{-4}\ \mathrm{m/s}$$

Arena limpia a grava fina: perfectamente coherente con una formación costera del Cretácico. **Esta verificación es lo que convierte un número en un resultado de ingeniería.** Si te hubiera salido $K = 10^{-9}$ m/s, sabrías que contaste mal.

> **Honestidad en el examen.** Escribe explícitamente "contando $n_f = 8$ tubos de flujo convergentes en B de la figura 4.10". Si tu conteo difiere del del profesor, el método queda demostrado y el crédito es el mismo.

## 4.6 — Clasificar las fronteras de una red de flujo

**Qué se evalúa:** las dos condiciones de borde básicas. Esto es la base de los problemas 4.7 a 4.10 y de todo el capítulo 5.

**Las dos reglas, una al lado de la otra**

| | Carga constante (Dirichlet, tipo 1) | Sin flujo (Neumann, tipo 2) |
|---|---|---|
| **Condición** | $h = \text{cte}$ | $\dfrac{\partial h}{\partial n} = 0$ |
| **¿Qué tipo de línea es?** | **Equipotencial** | **Línea de flujo** |
| **Las líneas de flujo la cruzan...** | perpendicularmente | nunca (son paralelas a ella) |
| **Dónde aparece** | fondo de un embalse, lecho de un río, lago, mar, cara de una excavación inundada | contacto con roca impermeable, pantalla o delantal impermeable, base de una presa, divisoria de aguas, eje de simetría |

**Cómo clasificar cualquier frontera en dos preguntas**

> **Pregunta 1: ¿hay un cuerpo de agua libre en contacto con el medio poroso?**
> Sí → carga constante = equipotencial (la carga es la del nivel de ese cuerpo de agua).
>
> **Pregunta 2: ¿hay un material impermeable, o una simetría que impide el paso?**
> Sí → sin flujo = línea de flujo.

**Aplicación a la figura del problema 6**

```
                                  delantal impermeable
      nivel del embalse           (impervious blanket)                nivel aguas abajo
             |                   ############                              |
             v        B ########################## C    /\                v
   A ===================================================/  \====== D ======= E
      \       \         \      |      |      |       | /    \  /   /      /
       \       \         \     |      |      |       |/      \/   /      /
        \       \         \    |      |      |              /    /      /
         \       \         \   |      |      |             /    /      /
   F +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ G
                          base impermeable
```

| Frontera | Pregunta 1 | Pregunta 2 | Clasificación |
|---|---|---|---|
| AB | Sí, el embalse | — | **Equipotencial, carga constante** |
| BC | No | Sí, el delantal | **Línea de flujo, sin flujo** |
| CD | No | Sí, base de la presa | **Línea de flujo, sin flujo** |
| DE | Sí, el agua de descarga | — | **Equipotencial, carga constante** |
| FG | No | Sí, roca impermeable | **Línea de flujo, sin flujo** |

**Observaciones que suben la nota**

- AB y DE son las **únicas** equipotenciales de la frontera; entre ellas se reparte la carga total $H$ del embalse. Son la entrada y la salida del sistema.
- BC, CD y FG forman un contorno continuo de líneas de flujo: son las **paredes** del "tubo" por el que circula el agua.
- La **primera línea de flujo** del dibujo es B-C-D (la más corta) y la **última** es F-G (la más larga). Todas las demás están entre ellas.
- El propósito del delantal es **alargar** el recorrido: obliga al agua a dar un rodeo, aumentando la pérdida de carga por filtración.

## 4.7 — Caudal de filtración y el efecto del delantal

**Qué se evalúa:** la fórmula de la red de flujo y el entendimiento de para qué sirve un delantal impermeable.

**La fórmula y su deducción (dos líneas, hazlas)**

Cada tubo de flujo lleva $\Delta Q = K\,\Delta h$ (por unidad de ancho de presa; $T = Kb$ con $b=1$). La caída de carga por salto es $\Delta h = H/n_d$. Con $n_f$ tubos:

$$Q = n_f\,K\,\frac{H}{n_d}
\qquad\Longrightarrow\qquad
\boxed{Q = K\,H\,\frac{n_f}{n_d}}$$

El cociente $n_f/n_d$ se llama **factor de forma** de la red: es pura geometría, independiente de $K$ y de $H$.

**Procedimiento del problema**

**Paso 1 — Cuenta $n_f$ y $n_d$ en la red original** (problema 6). $n_f$ = canales de flujo (espacios entre líneas de flujo), $n_d$ = saltos de potencial (espacios entre equipotenciales).

**Paso 2 — Redibuja con el delantal a la mitad.** Lo que cambia:

- $n_f$ se mantiene prácticamente igual (la geometría vertical no cambia).
- $n_d$ **disminuye**, porque el recorrido de filtración es más corto y las celdas cuadradas que caben son menos.

**Paso 3 — Redibuja sin delantal.** $n_d$ disminuye aún más.

**Paso 4 — Calcula los tres caudales** con la misma fórmula y compáralos en una tabla.

**El concepto, dicho correctamente**

> El delantal impermeable no reduce la filtración "tapando" nada: **alarga la trayectoria del flujo**. Al forzar un recorrido más largo con la misma carga disponible $H$, el gradiente medio baja ($i = H/L_{recorrido}$) y con él el caudal. En términos de la red: aumenta $n_d$ sin cambiar $n_f$.

**Lo que hay que señalar además del caudal (y casi nadie señala)**

El criterio de diseño real de una presa **no es el caudal de filtración** (unos litros por metro por día son irrelevantes), sino el **gradiente de salida** aguas abajo, que controla la **tubificación** (*piping*). El gradiente en la última celda de la red es:

$$i_{salida} = \frac{\Delta h}{a_{última}}$$

Al eliminar el delantal, las celdas de salida se hacen pequeñas y $i_{salida}$ crece. Si supera el gradiente crítico

$$i_{crit} = \frac{\gamma' }{\gamma_w} = \frac{\gamma_{sat}-\gamma_w}{\gamma_w} \approx 1$$

el suelo de la salida es arrastrado y comienza la erosión regresiva que puede destruir la presa. **Nota la conexión con el problema 4.4:** es el mismo principio de esfuerzo efectivo nulo.

## 4.8 — Dibujar redes de flujo en una sección rectangular

**Qué se evalúa:** si sabes construir una red a mano. Se califica el **dibujo**, así que la técnica importa.

### Las seis reglas de construcción (no son negociables)

1. Las **líneas de flujo** y las **equipotenciales** se cortan siempre a **90°** (en medio isótropo).
2. Las celdas deben ser **cuadrados curvilíneos**: ancho ≈ largo, medidos en el centro de la celda.
3. Las **fronteras de carga constante son equipotenciales**: las líneas de flujo salen de ellas perpendicularmente.
4. Las **fronteras impermeables son líneas de flujo**: las equipotenciales las cortan perpendicularmente.
5. El flujo va **de mayor a menor carga**, siempre.
6. En las **esquinas** y en los puntos donde cambia el tipo de frontera, la red se distorsiona: ahí hay **singularidades** (gradiente infinito en la teoría).

### Técnica recomendada (el orden ahorra borradores)

1. Dibuja la sección a escala y **rotula cada frontera** con su tipo (equipotencial / línea de flujo).
2. Traza **3 o 4 líneas de flujo** tentativas, respetando la perpendicularidad en las fronteras de carga constante y el paralelismo en las impermeables.
3. Traza las equipotenciales **a 90°** de las líneas de flujo, buscando celdas cuadradas.
4. **Corrige iterando**: donde las celdas salgan alargadas, mueve las líneas. Dos o tres iteraciones suelen bastar.
5. Si sobra una celda incompleta al final, está bien: se anota como fracción (p. ej., $n_d = 12.5$).

### Inciso (a) — Salida solo por la mitad izquierda del fondo

```
A ======================================================= B     h = 60 m  (ENTRADA)
| \\    \\    \\     \\      \\       \\       .      .  |
|  \\    \\    \\     \\      \\      \\      .      .   |   AD y BC: impermeables
|   \\    \\    \\     \\     \\     \\      .      .    |   (lineas de flujo)
|    \\    \\    \\     \\    \\     .      .      .     |
|     \\    \\    \\     \\   \\    .      .      .      |
D ===========================+++++++++++++++++++++++++++++ C
   h = 10 m  (SALIDA)         impermeable
   <----- L/2 ----->          <----- L/2 ----->
                              ^ zona casi estancada
                              (celdas grandes, gradiente ~ 0)
```

**Lo que el dibujo debe mostrar:**

- Todo el caudal entra por AB (toda la frontera) y sale **concentrado** por DC-izquierda.
- Las líneas de flujo **convergen** hacia DC-izquierda: allí las celdas son pequeñas y el gradiente máximo.
- La esquina inferior derecha está casi **estancada**: celdas muy grandes, equipotenciales muy separadas.
- En el punto medio de DC (donde la frontera cambia de carga constante a impermeable) hay una **singularidad**: el gradiente tiende a infinito. Se dibuja la última línea de flujo llegando casi vertical justo ahí.
- Las líneas de flujo son **perpendiculares** a AB y a DC-izquierda, y **paralelas** a AD, BC y DC-derecha.

### Inciso (b) — Salida por los segmentos inferiores de los lados

```
A ======================================================= B    h = 60 m (ENTRADA)
|  \                        |                        /   |
|   \                       |                       /    |   mitad superior de
|    \                      |                      /     |   los lados: IMPERMEABLE
+-----\---------------------|---------------------/------+   <- cambio de frontera
|      \                    |                    /       |
| h=10   \                  |                  /   h=10  |   mitad inferior:
| SALIDA  \                 |                 /   SALIDA |   h = 10 m
|          \__              |              __/           |
D +++++++++++++++++++++++++++++++++++++++++++++++++++++++ C
              DC: impermeable (linea de flujo)
                            ^
                 DIVISORIA DE FLUJO (linea de flujo vertical)
```

**Lo que el dibujo debe mostrar:**

- **Simetría especular** respecto al eje vertical central.
- Una **divisoria de flujo** recta y vertical en el eje: es una línea de flujo (igual que las divisorias de la figura 5.5 del capítulo 5). El agua que entra a la izquierda del eje sale por la izquierda.
- En DC (impermeable) el flujo es **horizontal** y tangente a la frontera.
- Las zonas de máximo gradiente son las **esquinas D y C**, donde confluyen una frontera impermeable y una de carga constante.
- Las equipotenciales cortan a 90° a DC y a los segmentos impermeables superiores de los lados.

**Compara los dos incisos en tu respuesta:** el (a) produce un flujo **asimétrico** con una zona muerta; el (b) produce un flujo **simétrico** con dos celdas espejo. El contraste muestra lo decisivas que son las condiciones de borde: el mismo dominio, el mismo material y la misma carga de entrada producen patrones completamente distintos.

## 4.9 — Red de flujo con nivel freático inclinado

**Qué se evalúa:** la condición de borde del nivel freático, que es la más sutil del curso y la base de todo el capítulo 5.

### La condición de borde clave

En el nivel freático la presión es la atmosférica, es decir, $P = 0$. Por lo tanto:

$$h = z + \frac{P}{\rho_w g} = z + 0$$

$$\boxed{h = z \quad \text{en el nivel freático}}$$

**Consecuencia práctica para dibujar** (el punto que hay que entender):

> La equipotencial de valor $h = 50$ m **tiene que** intersecar el nivel freático exactamente en el punto cuya **cota** es 50 m.

Esto obliga a que las equipotenciales lleguen al nivel freático **oblicuamente**, y es lo que distingue a esta frontera de las dos anteriores:

| Frontera | ¿Equipotencial? | ¿Línea de flujo? |
|---|---|---|
| Carga constante | Sí | No |
| Impermeable | No | Sí |
| **Nivel freático inclinado** | **No** | **No** |

El nivel freático es una **frontera de carga variable**: su valor de $h$ cambia punto a punto. No es equipotencial (la carga varía a lo largo de ella) ni línea de flujo (el agua la cruza: entra como recarga y sale como descarga).

### Procedimiento de dibujo

1. Dibuja la sección: BC a la derecha es $1.5\times$ AD; DC horizontal; AB es el nivel freático inclinado (alto en B, bajo en A).
2. **Rotula las cotas** a lo largo de AB. Son los valores de $h$ de las equipotenciales que llegan allí.
3. Marca los puntos de intersección de cada equipotencial con AB usando $h = z$.
4. Traza las equipotenciales desde esos puntos hacia abajo, cortando a **90°** las fronteras impermeables AD, BC y DC.
5. Traza las líneas de flujo **a 90°** de las equipotenciales, buscando celdas cuadradas.
6. Verifica el sentido: el flujo va de B (alto) hacia A (bajo).

```
                                                             B  <- z mas alta
                                               ....'''''''''
                               .....''''''''''                   RECARGA
               .....'''''''''                                    (flujo baja)
A ....''''''''                                                  |  |  |
|  ^  ^  ^      |      |       |        |        |       |       v  v  v
|  |  |  |      |      |       |        |        |       |        |  |  |
| DESCARGA      |  equipotenciales (no son perpendiculares       |  |  |
| (flujo sube)  |   al nivel freatico: lo cortan donde h = z)    |  |  |
|---------------+------+-------+--------+--------+-------+-------+--+--+
|  <-- lineas de flujo: entran en B, salen en A -->                   |
D +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ C
                     DC, AD, BC: impermeables
```

### Lo que debe quedar claro en el dibujo

1. **Zona de recarga en B** (parte alta): las líneas de flujo entran al dominio, con componente **descendente**. Un piezómetro profundo mediría menos carga que uno somero.
2. **Zona de descarga en A** (parte baja): las líneas de flujo salen, con componente **ascendente**. Un piezómetro profundo mediría **más** carga que uno somero (condición artesiana).
3. **Equilibrio de masa:** $\sum Q_{recarga} = \sum Q_{descarga}$. El dominio es cerrado salvo por el nivel freático.
4. Las líneas de flujo **profundas** son largas y lentas (sistema regional); las **someras**, cortas y rápidas (sistema local).
5. Las equipotenciales son **casi verticales** y las líneas de flujo **casi horizontales** en la parte central, porque la sección es ancha y delgada (aproximación de Dupuit).

**La conexión con el capítulo 5.** Esta es exactamente la figura 5.5 y el punto de partida de los modelos de Tóth y de Freeze y Witherspoon. Si dominas este dibujo, los problemas 5.1 y 5.2 son inmediatos.

## 4.10 — La misma red en medio anisótropo

**Qué se evalúa:** el método de la **sección transformada**. Es un procedimiento de cuatro pasos que hay que ejecutar en orden.

**El problema de fondo.** Si $K_h \ne K_v$, la ecuación de flujo no es la de Laplace:

$$K_h\frac{\partial^2h}{\partial x^2} + K_v\frac{\partial^2h}{\partial z^2} = 0$$

Y como las reglas de la red (ortogonalidad y celdas cuadradas) se derivan **de la ecuación de Laplace**, dejan de valer. La solución es cambiar de variable para recuperar Laplace.

### Paso 1 — Transformar la geometría

Define una coordenada nueva:

$$\boxed{x' = x\sqrt{\frac{K_v}{K_h}}}$$

Con $K_h = 5K_v$: $x' = x\sqrt{1/5} = 0.447\,x$. La sección se **contrae horizontalmente** a un 44.7 % de su longitud.

(Alternativa equivalente: expandir la vertical, $z' = z\sqrt{K_h/K_v} = 2.236\,z$. Elige una sola y dilo.)

**Verifica que funciona:** sustituyendo en la ecuación anterior, los coeficientes se igualan y queda

$$\frac{\partial^2h}{\partial x'^2}+\frac{\partial^2h}{\partial z^2} = 0$$

que **es** la ecuación de Laplace. Hacer esta verificación en el examen demuestra que entiendes de dónde sale el factor y no lo estás recitando.

### Paso 2 — Dibujar en la sección transformada

En la sección transformada el medio es **isótropo**, de modo que se aplican todas las reglas del problema 4.9: celdas cuadradas, intersecciones a 90°, $h = z$ en el nivel freático.

### Paso 3 — Destransformar

Devuelve la escala original multiplicando $x'$ por $\sqrt{K_h/K_v} = 2.236$. Las celdas dejan de ser cuadradas y quedan **rectángulos alargados horizontalmente** con relación de lados:

$$\frac{\text{largo}}{\text{ancho}} = \sqrt{\frac{K_h}{K_v}} = \sqrt{5} = 2.24$$

```
   SECCION TRANSFORMADA (x' = 0.447x)        SECCION REAL (destransformada)
   +----+----+----+----+                 +---------+---------+---------+
   |    |    |    |    |                 |         |         |         |
   +----+----+----+----+        ===>     +---------+---------+---------+
   |    |    |    |    |                 |         |         |         |
   +----+----+----+----+                 +---------+---------+---------+
   celdas CUADRADAS                      celdas 2.24 veces mas ANCHAS
   cortes a 90 grados                    los cortes YA NO son a 90 grados
```

### Paso 4 — Conductividad equivalente para el caudal

El caudal se calcula con la **media geométrica**:

$$\boxed{K_{eq} = \sqrt{K_h K_v}} \qquad\Longrightarrow\qquad Q = K_{eq}\,H\,\frac{n_f}{n_d}$$

Con $K_h = 5K_v$: $K_{eq} = \sqrt{5}\,K_v = 2.24\,K_v = 0.447\,K_h$.

> **Error frecuente:** usar $K_h$ (sobreestima el caudal 2.24 veces) o el promedio aritmético. Siempre es la **media geométrica**. Mnemotecnia: media **aritmética** para capas en paralelo (3.11), media **armónica** para capas en serie (3.11), media **geométrica** para la red de flujo en medio anisótropo (4.10).

### Qué cambia físicamente (la parte interpretativa)

1. **Las líneas de flujo se aplanan.** El agua prefiere viajar horizontalmente porque es por donde $K$ es mayor.
2. **Los sistemas de flujo son más someros y más extensos lateralmente.** La penetración vertical desde la divisoria disminuye.
3. **Aumenta la proporción de flujo local** frente al regional.
4. **En la sección real, las líneas de flujo YA NO cortan a las equipotenciales a 90°** (solo lo hacen en la transformada, o cuando coinciden con los ejes principales de anisotropía). Esto hay que decirlo explícitamente: es la pregunta trampa de este problema.
5. Se reconecta con el problema **3.12**: $\mathbf{q}$ no es paralelo a $\nabla h$ en medios anisótropos. Es el mismo fenómeno visto desde la red de flujo.

**Conexión con la realidad.** $K_h/K_v = 5$ es modesto; en sedimentos estratificados reales la relación llega a 100 o 1000 (como en el problema 3.11, que dio 13.7 con solo tres capas). Por eso los acuíferos regionales son "planos" y las plumas de contaminación se extienden lateralmente en lugar de hundirse.

---

<a name="parte-iii"></a>
# Parte III — Capítulo 5: El agua subterránea en el ciclo hidrológico

## 5.1 — Condiciones de borde de los modelos de cuenca

**Qué se evalúa:** que sepas traducir un dibujo de fronteras a su significado físico, y que entiendas **por qué** un medio estratificado necesita condiciones adicionales.

### Primera parte — Figura 5.5

Recorre las cuatro fronteras y traduce cada símbolo matemático a una frase física:

| Lo que dice la figura | Lo que significa |
|---|---|
| $\dfrac{\partial h}{\partial x} = 0$ en los laterales | **Divisorias de agua subterránea** o ejes de simetría de la cuenca. No hay flujo horizontal a través de ellos. Matemáticamente: Neumann homogénea (tipo 2) |
| $\dfrac{\partial h}{\partial z} = 0$ en la base | **Base impermeable** del sistema (basamento, roca fresca). No hay flujo vertical a través de ella |
| $h = f(x)$ en el tope | **Nivel freático especificado** como función de la posición. Se supone que replica la topografía. Matemáticamente: Dirichlet (tipo 1) |

**La frase que completa la respuesta:** las tres primeras fronteras están cerradas al flujo, de modo que el único intercambio del sistema con el exterior ocurre a través del nivel freático. Esto obliga a que **toda la recarga que entra en la parte alta salga como descarga en la parte baja**, y es lo que genera el patrón de celdas de flujo anidadas de Tóth.

### Segunda parte — ¿Qué añade la figura 5.8 y por qué?

**Lo que añade:**

$$\phi_1 = \phi_2, \qquad \phi_2 = \phi_3 \qquad\text{(continuidad del POTENCIAL)}$$

$$K_1\frac{\partial\phi_1}{\partial z} = K_2\frac{\partial\phi_2}{\partial z}, \qquad K_2\frac{\partial\phi_2}{\partial z} = K_3\frac{\partial\phi_3}{\partial z} \qquad\text{(continuidad del FLUJO normal)}$$

Además, el nivel freático se describe como **lineal por tramos** ($C_1, C_2, \dots, C_{k+1}$ sobre los intervalos $x_1, \dots, x_k$), es decir, una topografía con varios quiebres de pendiente, en lugar de una curva suave única.

**Por qué:** porque la figura 5.5 es **homogénea** (un solo material, sin interfaces internas) y la figura 5.8 es **heterogénea** (tres capas con $K_1$, $K_2$, $K_3$). En cada contacto hay que imponer explícitamente las dos leyes de conservación:

1. **El potencial no puede ser discontinuo.** Si $\phi_1 \ne \phi_2$ en un mismo punto, habría una diferencia de carga finita a través de un espesor nulo: gradiente infinito y flujo infinito. Físicamente imposible.
2. **La componente normal del flujo debe conservarse.** No se crea ni se destruye agua en la interfaz: lo que llega por arriba se va por abajo.

**La consecuencia visible (lo que conviene añadir): la refracción.** La segunda condición produce el cambio de dirección de las líneas de flujo al cruzar un contacto, según

$$\frac{\tan\theta_1}{\tan\theta_2} = \frac{K_1}{K_2}$$

con $\theta$ medido respecto a la **normal** a la interfaz.

```
          K1  (baja permeabilidad)
                  |
          \       |  theta_1 pequeno: flujo casi NORMAL a la interfaz
           \      |
  ----------\-----+------------------------- interfaz
              \   |
                \ |  theta_2 grande: flujo casi PARALELO a la interfaz
                  \______________
          K2  (alta permeabilidad)      ley: tan(t1)/tan(t2) = K1/K2
```

Al pasar a un medio **más** permeable las líneas de flujo se **tumban** (se acercan a la interfaz, viajan lateralmente); al pasar a uno **menos** permeable se **verticalizan** (cruzan por el camino más corto). Es el análogo exacto de la ley de Snell en óptica. Por eso una capa profunda de alta $K$ actúa como un **conducto regional** que captura y transporta el flujo decenas de kilómetros, que es precisamente lo que ocurre en la figura 5.27.

## 5.2 — Modificar redes de flujo regionales

**Qué se evalúa:** razonamiento cualitativo sobre sistemas de flujo. No hay cálculos; se califican el dibujo y la explicación.

### Método general: pregúntate siempre estas tres cosas

1. **¿Qué condición de borde cambió, y de qué tipo a qué tipo?**
2. **¿Cómo queda el balance de masa del dominio?**
3. **¿Se conserva o se rompe la simetría?**

### Parte (a) — Figura 5.4 con la frontera izquierda como frontera de flujo

**Situación original.** La figura 5.4 (Tóth, 1962) es un dominio **cerrado y simétrico**: laterales y base sin flujo, nivel freático que replica una topografía ondulada. El resultado son celdas de flujo locales anidadas dentro de un sistema regional.

**El cambio.** La frontera izquierda pasa de $\partial h/\partial x = 0$ (sin flujo, tipo 2) a una **frontera de flujo**: entra agua por el borde.

**Las cinco consecuencias que hay que dibujar y justificar:**

1. **Desaparece la divisoria de flujo izquierda.** En el original, la frontera sin flujo *era* una línea de flujo vertical. Ahora las líneas de flujo **atraviesan** el borde.
2. **Las equipotenciales ya no son perpendiculares a esa frontera.** La perpendicularidad era consecuencia de ser una línea de flujo; al dejar de serlo, llegan oblicuas.
3. **Se rompe la simetría.** La zona de descarga se desplaza y **se amplía** hacia la derecha, porque debe evacuar la recarga propia **más** el caudal importado.
4. **El sistema regional se refuerza a costa de los locales.** El flujo lateral entrante circula por la parte profunda y "arrasa" las celdas locales del lado izquierdo, que se reducen o desaparecen. Las celdas locales de la derecha sobreviven mejor.
5. **Cambia el balance:** ya no es $\sum$recarga $=\sum$descarga, sino

$$\sum Q_{recarga} + Q_{lateral} = \sum Q_{descarga}$$

**Relevancia práctica (añádela).** Este es el problema real de la modelación numérica: elegir una divisoria topográfica como frontera sin flujo es cómodo, pero si en realidad entra flujo regional desde fuera, el modelo subestima la descarga y el balance hídrico de la cuenca queda mal. La frontera lateral es la hipótesis más frágil de cualquier modelo de cuenca.

### Parte (b) — Figura 5.27 con $K_1 = K_2$

**Situación original.** El perfil de pradera de Meyboom (1966) tiene una capa superior de baja $K_1$ (till glaciar) sobre una capa profunda de alta $K_2$ (arena/grava), con $K_2 \gg K_1$. Esa capa profunda es un **conducto regional**: captura el flujo y lo transporta hasta 50 millas, alimentando los *deep-flowing wells* y las áreas de descarga salina lejanas.

**El cambio.** Con $K_1 = K_2$ el medio pasa a ser **homogéneo**.

**Las cinco consecuencias:**

1. **Desaparece la refracción** de las líneas de flujo en el contacto. La red se vuelve continua y suave.
2. **Desaparece el conducto regional.** Sin la capa de alta $K$, el flujo profundo pierde su "autopista" y el sistema regional se **debilita** drásticamente.
3. **Dominan los sistemas locales.** Cada montículo topográfico genera su propia celda cerrada de recarga–descarga, con descarga en la depresión adyacente. El patrón resultante es el de la figura 5.4.
4. **La penetración vertical del flujo** pasa a estar controlada únicamente por la **longitud de onda de la topografía**, no por la estratigrafía (resultado clásico de Tóth: ondulaciones cortas → celdas someras).
5. **Consecuencia hidroquímica:** desaparecen las áreas de descarga salina alejadas alimentadas por flujo regional profundo (de larga residencia y alta mineralización). La salinización queda confinada a las depresiones locales, y el agua es más joven y más dulce.

**La enseñanza general:** la **heterogeneidad** puede dominar sobre la **topografía** en el control del flujo regional. Una sola capa de alta permeabilidad en la profundidad reorganiza por completo el sistema de flujo de una cuenca entera.

## 5.3 — El canal a nivel del mar (el problema estrella del capítulo)

**Qué se evalúa:** aplicación de una solución transitoria con la función error. Es el problema con más pasos y donde más se gana o se pierde.

### Paso 1 — Monta la geometría y elige el datum

```
                                                            DIVISORIA
    CANAL                                                   (manantiales)
      |                                                          |
      |   <------------------ L = 3 mi = 4828 m ---------------->|
 _____|_____                                                     |
      |     '''----___                                           |
      |              '''----____   nivel freatico (t creciente)  |
      |                          '''''----_______________________|______
  ====|================================================================= h0 = 12 m
   ~~~v~~~ nivel del mar  <-- DATUM: h = 0 aqui -->
      |
      | 9 m
   ___v___________________________________________________________________
            base del sistema (fondo del canal)

   Espesor saturado: 9 m en el canal, 21 m en la divisoria  ==>  b_medio = 15 m
```

**Decisiones que debes declarar explícitamente** (son hipótesis, y declararlas es lo que hace defendible la respuesta):

1. **Datum en el nivel del mar** = nivel de agua en el canal. Entonces $h = 0$ en el canal y $h_0 = 12$ m es la carga inicial en todo el dominio.
2. **Base del sistema en el fondo del canal** (9 m bajo el nivel del mar).
3. **Linealización:** el acuífero es libre, así que $T$ depende de $h$ (ecuación de Boussinesq, no lineal). Se linealiza usando el espesor saturado **medio**:

$$\bar b = \frac{21 + 9}{2} = 15\ \mathrm{m} \qquad\Longrightarrow\qquad T = K\bar b$$

### Paso 2 — Calcula la difusividad hidráulica

$$\boxed{\nu = \frac{T}{S_y}} \qquad [L^2/T]$$

Este es el parámetro que controla **toda** la respuesta transitoria. Su interpretación: la "velocidad de propagación" de la perturbación de carga. La longitud de difusión en el tiempo $t$ es

$$\ell(t) = \sqrt{\nu t}$$

**Unidades:** con $K$ en m/día, trabaja todo en días. No mezcles.

### Paso 3 — Identifica la solución correcta

**Qué le pasó al acuífero:** se excavó el canal, y la carga en $x = 0$ cayó **de golpe** de 12 m a 0 y se mantiene ahí. Esto es, matemáticamente, exactamente el problema del **medio semi-infinito con cambio escalón en la frontera**, cuya solución (de la analogía con la conducción de calor) es:

$$\boxed{h(x,t) = h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{\nu t}}\right) = h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{Tt/S_y}}\right)}$$

**Verifica que cumple las condiciones** (hazlo, son tres líneas y blindan la respuesta):

| Condición | Comprobación |
|---|---|
| $h = 0$ en $x=0$, $\forall t$ | $\mathrm{erf}(0) = 0$ ✓ |
| $h = h_0$ en $t=0$, $\forall x>0$ | $t\to0 \Rightarrow$ argumento $\to\infty \Rightarrow \mathrm{erf}\to1$ ✓ |
| $h \to h_0$ cuando $x\to\infty$ | $\mathrm{erf}(\infty)=1$ ✓ |

**La función error** (tenla a mano, memoriza tres valores):

$$\mathrm{erf}(0)=0,\qquad \mathrm{erf}(1)=0.843,\qquad \mathrm{erf}(2)=0.995,\qquad \mathrm{erf}(\infty)=1$$

Regla práctica: para argumentos **mayores que 2**, $\mathrm{erf}\approx1$ y la perturbación **aún no ha llegado** a esa distancia.

### Paso 4 — Inciso (a): cargas en el canal y en la divisoria

**En el canal ($x = 0$):** $h = h_0\,\mathrm{erf}(0) = 0$ **para todo $t$**.

> No te confundas al ver un resultado trivial. **Es la condición de borde**: el canal impone el nivel del mar desde el instante cero. El abatimiento allí es de 12 m inmediatamente. Escríbelo así y explícalo; es la respuesta correcta.

**En la divisoria ($x = L$):** calcula el argumento para cada $t$ y busca $\mathrm{erf}$ en tabla.

**Atajo que ahorra tiempo:** como el argumento es $L/(2\sqrt{\nu t})$ y solo cambia $t$, calcula el argumento para 10 años y luego escala por $\sqrt{t_1/t_2}$:

$$\mathrm{arg}(100\ \mathrm{a}) = \mathrm{arg}(10\ \mathrm{a})\times\sqrt{\frac{10}{100}} = \frac{\mathrm{arg}(10\ \mathrm{a})}{3.162}$$

**La interpretación, que es la respuesta de verdad:**

> A los 10 y 20 años el argumento es mayor que 2.5, de modo que $\mathrm{erf}\approx1$ y **la divisoria no se ha enterado** de que existe el canal. A los 40 años ha bajado 0.14 m y a los 100 años solo 1.33 m de los 12 m iniciales. Dos conclusiones: (1) la hipótesis de medio **semi-infinito** es válida durante todo el periodo analizado, porque la perturbación nunca alcanza la frontera; (2) los **manantiales de la divisoria sobreviven** a escala de décadas, aunque su caudal disminuya.

**Lo que conviene añadir:** una tabla del perfil $h(x,t)$ para varias distancias. Convierte el ejercicio en un gráfico, que es lo que realmente se usa en ingeniería (hasta dónde llega el abatimiento a los 50 años determina qué pozos y humedales se afectan).

### Paso 5 — Inciso (b): caudal hacia el canal

**Deducción (hazla, son tres líneas y es lo más valioso de la respuesta).** El caudal es Darcy evaluado en la frontera:

$$q' = T\left.\frac{\partial h}{\partial x}\right|_{x=0}$$

Derivando la función error (regla: $\dfrac{d}{du}\mathrm{erf}(u) = \dfrac{2}{\sqrt\pi}e^{-u^2}$) con $u = x/(2\sqrt{\nu t})$:

$$\frac{\partial h}{\partial x} = h_0\frac{2}{\sqrt\pi}e^{-x^2/4\nu t}\cdot\frac{1}{2\sqrt{\nu t}} = \frac{h_0}{\sqrt{\pi\nu t}}e^{-x^2/4\nu t}$$

En $x=0$ la exponencial vale 1:

$$q' = \frac{T h_0}{\sqrt{\pi\nu t}} = \frac{T h_0}{\sqrt{\pi T t/S_y}}
\qquad\Longrightarrow\qquad
\boxed{q' = h_0\sqrt{\frac{T\,S_y}{\pi\,t}}}$$

**Unidades:** $\mathrm{m^3/día}$ **por metro de canal** (es un caudal por unidad de longitud, $L^2/T$).

**Las dos propiedades que hay que comentar:**

1. **$q' \propto t^{-1/2}$.** El caudal decae con la raíz del tiempo: enorme al principio (infinito en $t=0$, singularidad matemática del escalón) y decreciente para siempre. **Nunca alcanza un estado estacionario** mientras el medio sea semi-infinito. Verificación gratuita:

$$\frac{q'(10\ \mathrm{a})}{q'(100\ \mathrm{a})} = \sqrt{\frac{100}{10}} = 3.16$$

Comprueba que tus dos números cumplan esta relación: es un control de errores que no cuesta nada.

2. **$q' \propto \sqrt{T S_y}$.** El caudal depende de la **media geométrica** de transmisividad y almacenamiento, no de cada uno por separado. Es la razón de que en una prueba de bombeo no se puedan separar $T$ y $S$ con un solo dato.

**Pregunta que conviene responder antes de que la hagan:** ¿uno o dos flancos? Si el canal tiene acuífero a ambos lados, el caudal total es $2q'$. Dilo explícitamente.

### Paso 6 — Análisis de sensibilidad (lo que distingue una respuesta completa)

La única decisión discutible es $\bar b$. Repite el cálculo con $\bar b = 21$ m (espesor inicial) y muestra que las conclusiones no cambian: la divisoria sigue casi intacta y $q'$ varía un ~18 %. Declarar la hipótesis y acotar su efecto es lo que hace la respuesta inatacable.

## 5.4 — Estabilidad de excavaciones

**Qué se evalúa:** el mismo principio del problema 4.4, aplicado a un caso real de obra. Si dominaste el 4.4, este es gratis.

### Procedimiento de cinco pasos

**Paso 1 — Esfuerzo total en la base del estrato confinante, bajo la excavación.**

$$\sigma_T = \gamma_{sat}(D-d) + \gamma_w\,d_w$$

$D$ = espesor original del confinante; $d$ = profundidad excavada; $d_w$ = profundidad de agua dentro de la excavación.

**Paso 2 — Presión neutra, fijada por el acuífero.**

$$u = \gamma_w\,h_p$$

**Recuerda: $u$ no depende de la excavación.** La controla el acuífero, que está conectado a su zona de recarga.

**Paso 3 — Esfuerzo efectivo.**

$$\sigma' = \sigma_T - u$$

**Paso 4 — Factor de seguridad.**

$$\boxed{FS = \frac{\sigma_T}{u}}$$

| $FS$ | Estado |
|---|---|
| $>1.5$ | Seguro |
| $1.0$–$1.3$ | Marginal: exige instrumentación y monitoreo |
| $=1.0$ | **Crítico**: $\sigma'=0$, condición de arena movediza (*quick condition*) |
| $<1.0$ | **Falla**: reventón del fondo (*blowout*) |

**Paso 5 — Profundidad crítica.** Impón $\sigma_T = u$ y despeja $d$:

$$\boxed{d_{crit} = \frac{\gamma_{sat}D - \gamma_w h_p}{\gamma_{sat}-\gamma_w}} \qquad\text{(excavación llena de agua)}$$

$$\boxed{d_{crit} = D - \frac{\gamma_w h_p}{\gamma_{sat}}} \qquad\text{(excavación en seco)}$$

### Por qué este problema aparece en un libro de hidrogeología

La conexión que el libro quiere que hagas: **las zonas de descarga de agua subterránea son terreno peligroso para excavar**. En una zona de descarga, la carga aumenta con la profundidad (condición artesiana), de modo que cualquier excavación reduce $\sigma_T$ mientras $u$ permanece alto. En una zona de **recarga** ocurre lo contrario y el problema no existe.

**Y aquí se cierra el círculo con el problema 3.15:** identificar si estás en zona de recarga o de descarga (comparando piezómetros someros y profundos) es el **primer** paso de cualquier investigación geotécnica en terreno saturado. Decirlo así es exactamente lo que el autor busca.

### Medidas correctivas (parte de la respuesta esperada)

1. **Despresurizar el acuífero** con pozos de alivio o pozos profundos. Carga máxima admisible:

$$h_{p,adm} = \frac{\sigma_T}{\gamma_w \cdot FS_{req}}$$

2. **Mantener la excavación inundada** y excavar con draga: duplica la profundidad alcanzable.
3. **Dejar un tapón más grueso** o lastrarlo.
4. **Instrumentar con piezómetros** y monitorear $u$ durante la obra: $u$ puede cambiar por estaciones o por recarga.

> Si tienes el libro a mano, sustituye en estas mismas fórmulas los valores del caso histórico de las páginas 99–101. El procedimiento es idéntico.

## 5.5 — Ascenso de la interfaz salina (upconing)

**Qué se evalúa:** la relación de Ghyben-Herzberg aplicada al bombeo y el criterio de estabilidad de la interfaz.

### Concepto: por qué asciende el agua salada

Al bombear agua dulce se reduce la carga sobre la interfaz, y el agua salada, **más densa**, sube para restablecer el equilibrio de presiones. Si sube demasiado, el equilibrio se vuelve **inestable** y la interfaz colapsa hacia el pozo: el pozo se saliniza de forma prácticamente irreversible.

```
       pozo  (Q)
        ||
  ======||==================================== nivel freatico
        ||
        ||  AGUA DULCE  rho_f = 1000 kg/m3
        \/  <- fondo del pozo
        ^
        | ascenso z = Q / (2 pi K d G)
     ___^___  d = 40 ft  (distancia disponible)
    /       \
  _/         \_____________________________
   interfaz (cono de ascenso)
         AGUA SALADA  rho_s = 1025 kg/m3

   Criterio: z <= 0.3 d  (si no, colapso hacia el pozo)
```

### Procedimiento

**Paso 1 — Densidad relativa.**

$$G = \frac{\Delta\rho}{\rho_f} = \frac{\rho_s-\rho_f}{\rho_f} = \frac{1025-1000}{1000} = 0.025$$

Este es el **mismo** 0.025 de la relación de Ghyben-Herzberg ($1/G = 40$: cada metro de agua dulce sobre el nivel del mar sostiene 40 m de agua dulce por debajo). Si el enunciado no da las densidades, usa 0.025: es el valor estándar para agua de mar.

**Paso 2 — Ascenso en estado estacionario** (Dagan y Bear, 1968):

$$z = \frac{Q}{2\pi\,K\,d\,G}$$

**Chequeo dimensional:** $\dfrac{L^3/T}{(L/T)(L)} = L$ ✓

**Paso 3 — Criterio de estabilidad.** La interfaz permanece estable mientras el ascenso no supere aproximadamente un tercio de la distancia disponible:

$$z \le 0.3\,d$$

**Paso 4 — Despeja el caudal admisible.**

$$Q_{max} = 2\pi K d (0.3 d) G
\qquad\Longrightarrow\qquad
\boxed{Q_{max} = 0.6\,\pi\,K\,d^{2}\,G}$$

**Paso 5 — Unidades.** Trabaja en SI ($K$ en m/s, $d$ en m) y convierte al final a L/s, m³/día y gpm. El resultado se lee mejor en L/s.

### Las dos lecciones del resultado

1. **Dependencia cuadrática con $d$.** Duplicar la distancia del pozo a la interfaz **cuadruplica** el caudal admisible. De ahí la regla de diseño de acuíferos costeros: **perforar lo más somero posible** y usar **muchos pozos de bajo caudal** en lugar de pocos de alto caudal.
2. **Es un criterio de estabilidad, no de equilibrio.** Por debajo de $0.3d$ el cono de ascenso es estable y reversible: si dejas de bombear, baja. Por encima, el sistema se vuelve inestable y la salinización es **permanente**, porque el agua salada que entró al acuífero no se va al dejar de bombear.

**El detalle que gana puntos.** La carga de agua dulce es 40 veces más eficaz "sosteniendo" la interfaz que el agua salada en empujarla; esa asimetría ($1/G = 40$) es la razón de que bombeos modestos generen ascensos grandes. En un acuífero costero, un metro de abatimiento del nivel freático desplaza la interfaz unos 40 m hacia arriba.

## 5.6 — Posición del pie de la cuña salina

**Qué se evalúa:** la solución de Glover y, sobre todo, el **juicio crítico** sobre si el resultado es físicamente posible.

### Procedimiento

**Paso 1 — Escribe la solución de Glover (1959)** para la profundidad $z$ de la interfaz bajo el nivel del mar, a una distancia $x$ tierra adentro:

$$z^{2} = \frac{2\,q'\,x}{K\,G} + \left(\frac{q'}{K\,G}\right)^{2}$$

donde $q'$ es el caudal de agua dulce hacia el mar **por unidad de longitud de costa** ($L^2/T$).

**Paso 2 — Interpreta los dos términos.**

- El primero crece con $x$: la interfaz **se hunde** tierra adentro.
- El segundo es el valor de $z$ en $x=0$: la interfaz **no aflora** en la línea de costa, sino que ya está a profundidad $q'/(KG)$. Esa franja es la **cara de descarga** (*outflow face*), por donde el agua dulce sale al mar.

```
  TIERRA                                       MAR
                      linea de costa (x = 0)
                               |
  ====== nivel freatico        |  ~~~~~~~~~~~~~~~~~~~~~~
    \___                       |
        \____  AGUA DULCE      v
             \____          ___ <- cara de descarga, z = q'/(KG)
                  \_____  __/
   PIE (toe)            \/ -----___
      z = B  ^                      ----___  interfaz
  ____________|__________________________  ---___________
  ##### base del acuiferol, B = 100 ft ############
         AGUA SALADA
  <------ x_toe ------>
```

**Paso 3 — El pie de la cuña** es donde la interfaz toca la base del acuífero: $z = B$. Despeja $x$:

$$\boxed{x_{toe} = \frac{K\,G\,B^{2}}{2\,q'} - \frac{q'}{2\,K\,G}}$$

**Paso 4 — Repite con $q'/2$** y compara.

### El paso 5 que es el verdadero contenido del ejercicio: verificar

**Con el valor del enunciado ($q' = 2\times10^{-1}\ \mathrm{ft^3/s}$ por pie) el resultado sale NEGATIVO.** No lo descartes como error de cálculo: **interpreta**.

$$x_{toe} < 0 \;\Longrightarrow\; \text{el pie está mar adentro} \;\Longrightarrow\; \textbf{no hay cuña salina}$$

Lo confirma el segundo término: $q'/(KG) = 2424$ ft es la profundidad de la interfaz en la costa, **24 veces mayor que el espesor del acuífero (100 ft)**. La interfaz está muy por debajo de la base del acuífero ya en la línea de costa: el agua dulce expulsa por completo al agua de mar.

**Verificación independiente con el gradiente** (hazla siempre que un resultado te huela mal):

$$i = \frac{q'}{K\,B} = \frac{0.2}{(3.3\times10^{-3})(100)} = 0.61\ \mathrm{m/m}$$

Un gradiente de 0.61 es físicamente inverosímil en un acuífero costero: los valores reales son $10^{-4}$ a $10^{-3}$. **Conclusión: el exponente del enunciado está mal.**

**Con el valor coherente $q' = 2\times10^{-4}\ \mathrm{ft^3/s}$ por pie** se obtiene $x_{toe} \approx 2061$ ft, y con la mitad del caudal, 4124 ft. Números perfectamente razonables, y además con el gradiente correcto:

$$i = \frac{2\times10^{-4}}{0.33} = 6.1\times10^{-4}\ \mathrm{m/m}\ \checkmark$$

> **Cómo presentar esto en el parcial.** Resuelve con el dato que te dan, muestra que es físicamente imposible, demuéstralo con el gradiente implicado, y resuelve también con el valor coherente. Eso no es "corregir al profesor": es **verificar la plausibilidad del resultado**, que es lo que define a un ingeniero.

### El resultado conceptual que hay que extraer

Cuando $q'$ es pequeño, el segundo término es despreciable y domina

$$x_{toe} \approx \frac{K\,G\,B^{2}}{2\,q'} \;\propto\; \frac{1}{q'}$$

$$\boxed{\text{Reducir a la mitad la descarga de agua dulce DUPLICA la penetración de la cuña salina}}$$

Y la dependencia con $B^2$: duplicar el espesor del acuífero **cuadruplica** la intrusión. Dos acuíferos con el mismo caudal pero distinto espesor tienen cuñas radicalmente distintas.

**La moraleja de gestión del recurso:** la intrusión salina es inversamente proporcional al caudal de agua dulce que se **deja** fluir al mar. Ese caudal no es "agua desperdiciada": es la barrera hidráulica que protege el acuífero. Sobrebombear hacia el interior reduce $q'$ y desplaza la cuña linealmente en $1/q'$. Es el error clásico de gestión en acuíferos costeros.

---

<a name="parte-iv"></a>
# Parte IV — Chuleta y errores que cuestan el parcial

## Las 18 ecuaciones del parcial

### Flujo

$$\mathbf{q} = -K\nabla h \qquad\qquad Q = -KA\frac{dh}{dL} \qquad\qquad v = \frac{q}{n_e}$$

$$h = z + \frac{P}{\rho_w g} \qquad\qquad \phi = g\,h \qquad\qquad K = \frac{k\rho_w g}{\mu}$$

$$T = K\,b \qquad\qquad S = S_s\,b = \rho_w g\,b(\beta_p+n\beta_w) \qquad\qquad \nu = \frac{T}{S}$$

### Medios heterogéneos y anisótropos

$$K_h = \frac{\sum K_ib_i}{\sum b_i} \quad\text{(aritmética, paralelo)}
\qquad
K_v = \frac{\sum b_i}{\sum b_i/K_i} \quad\text{(armónica, serie)}$$

$$K_{eq} = \sqrt{K_hK_v} \quad\text{(geométrica, redes de flujo)}
\qquad
x' = x\sqrt{\frac{K_v}{K_h}} \quad\text{(sección transformada)}$$

### Ecuación de flujo

$$\nabla^2h = \frac{S}{T}\frac{\partial h}{\partial t}
\qquad\qquad
\nabla^2 h = 0 \quad\text{(permanente, Laplace)}$$

### Redes de flujo

$$Q = K\,H\,\frac{n_f}{n_d} \qquad\qquad \Delta Q = T\,\Delta h \qquad\qquad \frac{\tan\theta_1}{\tan\theta_2}=\frac{K_1}{K_2}$$

### Esfuerzos

$$\sigma' = \sigma_T - u \qquad\qquad u = \gamma_w h_p \qquad\qquad FS = \frac{\sigma_T}{u}$$

$$d_{crit} = \frac{\gamma_{sat}D-\gamma_w h_p}{\gamma_{sat}-\gamma_w}$$

### Transitorio y agua salada

$$h = h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{Tt/S}}\right)
\qquad\qquad
q' = h_0\sqrt{\frac{TS}{\pi t}}$$

$$Q_{max} = 0.6\pi K d^2 G \qquad\qquad x_{toe} = \frac{KGB^2}{2q'}-\frac{q'}{2KG} \qquad\qquad G = \frac{\Delta\rho}{\rho_f}=0.025$$

## Los 15 errores que más cuestan

| # | Error | Cómo evitarlo |
|---|---|---|
| 1 | Confundir $q$ con $v$ | $q$ = caudal/área total; $v = q/n_e$ es la velocidad real. Si piden "tiempo de viaje", es $v$ |
| 2 | Omitir el signo menos de Darcy | El gradiente apunta hacia carga **creciente**; el flujo va al contrario |
| 3 | Dar la dirección de $\nabla h$ como dirección del flujo | Invierte el azimut 180° antes de responder |
| 4 | Confundir $K_h$ (aritmética) con $K_v$ (armónica) | $K_h$ la domina la capa **mejor**; $K_v$ la domina la **peor**. Siempre $K_v \le K_h$ |
| 5 | Usar $K_h$ en vez de $\sqrt{K_hK_v}$ en una red anisótropa | Media geométrica, siempre |
| 6 | $1\ \mathrm{m^2} = 10^2\ \mathrm{cm^2}$ | Son $10^{4}$. Las áreas van al cuadrado |
| 7 | Área transversal vs. área en planta | Flujo horizontal → espesor × ancho. Fuga vertical → longitud × ancho |
| 8 | Calcular $h_p$ sin la parte artesiana | $h_p$ = altura **total** de la columna de agua sobre el punto de medida |
| 9 | Creer que excavar baja $u$ | $u$ la fija el acuífero, no la excavación. Es el núcleo de 4.4 y 5.4 |
| 10 | Olvidar el peso del agua en una zanja inundada | Aporta $\gamma_w d_w$ al esfuerzo total y duplica la profundidad crítica |
| 11 | Decir que las líneas de flujo cortan a 90° en medio anisótropo | Solo en la **sección transformada** |
| 12 | Tratar el nivel freático como equipotencial | Es frontera de **carga variable**: $h = z$, ni equipotencial ni línea de flujo |
| 13 | Mezclar unidades de tiempo en problemas transitorios | Si $K$ está en m/día, trabaja **todo** en días |
| 14 | No verificar que un resultado sea plausible | Convierte a m/año, calcula el gradiente implicado, nombra el material. Ver 5.6 |
| 15 | No declarar las hipótesis | Temperatura para $\mu$, espesor para linealizar, conteos de la red. Declararlas es inatacable |

## Gradientes y conductividades de referencia

| Magnitud | Rango típico |
|---|---|
| Gradiente horizontal regional | $10^{-4}$ a $10^{-2}$ |
| Gradiente vertical en un acuitardo | $10^{-1}$ a 1 |
| $K$ grava | $10^{-2}$ a 1 m/s |
| $K$ arena limpia | $10^{-5}$ a $10^{-2}$ m/s |
| $K$ arena fina / limo | $10^{-8}$ a $10^{-5}$ m/s |
| $K$ arcilla | $10^{-11}$ a $10^{-8}$ m/s |
| $S$ acuífero confinado | $10^{-5}$ a $10^{-3}$ |
| $S_y$ acuífero libre | 0.05 a 0.30 |
| $n_e$ roca fracturada | $10^{-5}$ a $10^{-2}$ |

## Cómo abordar cualquier problema en el parcial (rutina de 6 pasos)

1. **Dibuja** el sistema y rotula las fronteras con su tipo (carga constante / sin flujo / carga variable).
2. **Identifica el régimen:** ¿permanente ($\nabla^2h=0$) o transitorio (aparece $\sqrt{Tt/S}$)?
3. **Identifica la dirección del flujo:** ¿horizontal (usa $T$, área transversal) o vertical (usa $K'$, área en planta)?
4. **Escribe el balance de masa** antes de meter números. En sistemas acoplados (3.17) es lo que resuelve el problema.
5. **Calcula con unidades explícitas** en cada paso, no solo al final.
6. **Verifica:** convierte a unidades intuitivas (m/año, L/s), nombra el material correspondiente, comprueba que el balance cierre y que el signo tenga sentido físico.

**Y declara tus hipótesis.** Temperatura para $\mu$, espesor para linealizar $T$, conteos de la red de flujo, densidad del agua de mar. Una respuesta con hipótesis explícitas y método correcto vale más que un número "exacto" sin justificación.

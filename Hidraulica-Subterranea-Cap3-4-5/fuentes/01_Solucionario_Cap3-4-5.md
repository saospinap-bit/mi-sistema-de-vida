# Solucionario

Ejercicios de los capítulos 3, 4 y 5
Domenico, P. A. & Schwartz, F. W., *Physical and Chemical Hydrogeology*, 2.ª ed., Wiley, 1997
(páginas 55–57, 73–74 y 102)

**Constantes usadas en todo el documento**

$$\rho_w = 1000\ \mathrm{kg/m^3},\qquad g = 9.81\ \mathrm{m/s^2},\qquad \gamma_w = \rho_w g = 9810\ \mathrm{N/m^3} = 62.4\ \mathrm{lb/ft^3}$$

$$\mu = 1.0\times10^{-3}\ \mathrm{Pa\cdot s}\ (20^\circ\mathrm{C}),\qquad 1\ \text{darcy} = 9.87\times10^{-9}\ \mathrm{cm^2}$$

---

# CAPÍTULO 3 — Ground Water Movement

## 3.1 Descarga específica

$$q = K\,i = \left(10^{-6}\ \tfrac{\mathrm{m}}{\mathrm{s}}\right)(0.019)$$

$$\boxed{q = 1.9\times10^{-8}\ \mathrm{m/s}}$$

Equivale a $0.60\ \mathrm{m/año}$.

## 3.2 Velocidad real (velocidad lineal media)

$$v = \frac{q}{n_e}$$

| $n_e$ | $v$ (m/s) | $v$ (m/año) |
|---|---|---|
| 0.1 | $\boxed{1.9\times10^{-7}}$ | 6.0 |
| 0.0001 | $\boxed{1.9\times10^{-4}}$ | $5.99\times10^{3}$ |

La velocidad real es **1000 veces mayor** en el segundo caso, aunque el caudal por unidad de área es idéntico.

## 3.3 Razón de la diferencia en $n_e$

Se trata de **medios con geometría de poro radicalmente distinta**:

- $n_e = 0.1$ → medio **granular poroso** (arena, grava): el flujo ocurre por todo el espacio intergranular interconectado.
- $n_e = 0.0001$ → **roca fracturada** (cristalina, ígnea o metamórfica, o caliza con fisuras): el agua circula únicamente por un conjunto escaso de fracturas que representa una fracción diminuta del volumen total.

Consecuencia práctica: en roca fracturada un contaminante viaja miles de veces más rápido que lo que sugeriría el gradiente y la $K$ por sí solos.

## 3.4 Análisis dimensional de la altura de presión

$$h_p = \frac{P}{\rho_w g}$$

Con $F = M\,L\,T^{-2}$ (segunda ley de Newton):

$$[P] = \frac{F}{L^2} = \frac{M L T^{-2}}{L^2} = \frac{M}{L\,T^{2}}$$

$$[\rho g] = \frac{M}{L^3}\cdot\frac{L}{T^2} = \frac{M}{L^{2}T^{2}}$$

$$[h_p] = \frac{M/(L\,T^{2})}{M/(L^{2}T^{2})} = \frac{M}{L\,T^{2}}\cdot\frac{L^{2}T^{2}}{M} = \boxed{L}$$

## 3.5 Altura hidráulica y potencial hidráulico

**Altura hidráulica** $h = z + \dfrac{P}{\rho_w g}$ — energía por unidad de **peso**:

$$\frac{\text{Energía}}{\text{Peso}} = \frac{F\cdot L}{F} = \boxed{L}$$

**Potencial hidráulico** $\phi = g\,h$ — energía por unidad de **masa**:

$$\frac{\text{Energía}}{\text{Masa}} = \frac{F\cdot L}{M} = \frac{(M L T^{-2})\,L}{M} = \boxed{\frac{L^{2}}{T^{2}}}$$

Verificación cruzada: $[\phi] = [g][h] = \dfrac{L}{T^{2}}\cdot L = \dfrac{L^{2}}{T^{2}}$ ✓

## 3.6 Problema de los tres puntos

Sistema de coordenadas: $x$ hacia el Este, $y$ hacia el Norte, origen en el vértice inferior izquierdo.

| Punto | Coordenadas (m) | $h$ (m) |
|---|---|---|
| B (inferior izq.) | $(0,\,0)$ | 300 |
| C (inferior der.) | $(1000,\,0)$ | 400 |
| A (superior) | $(0,\,2000)$ | 500 |

**Componentes del gradiente**

$$\frac{\partial h}{\partial x} = \frac{400-300}{1000} = 0.100\ \mathrm{m/m}
\qquad
\frac{\partial h}{\partial y} = \frac{500-300}{2000} = 0.100\ \mathrm{m/m}$$

**Magnitud**

$$|\nabla h| = \sqrt{(0.100)^2+(0.100)^2} = \boxed{0.141\ \mathrm{m/m}}$$

**Dirección**

$$\theta = \arctan\!\left(\frac{\partial h/\partial y}{\partial h/\partial x}\right) = \arctan(1) = 45^\circ$$

$\nabla h$ apunta hacia el **N 45° E** (hacia carga creciente). Como $\mathbf{q} = -K\nabla h$:

$$\boxed{\text{El flujo se dirige hacia el S 45° W (suroeste), con } i = 0.141\ \mathrm{m/m}}$$

**Comprobación por el método gráfico.** Sobre AB, $h = 400$ m en el punto medio $P(0,1000)$. La equipotencial de 400 m es la recta $PC$: $x + y = 1000$. Distancia perpendicular de B a esa recta:

$$d = \frac{|0+0-1000|}{\sqrt{2}} = 707.1\ \mathrm{m}
\qquad\Rightarrow\qquad
i = \frac{400-300}{707.1} = 0.141\ \mathrm{m/m}\ \checkmark$$

> **Nota sobre la figura.** El rótulo de la hipotenusa (2062 m) es inconsistente con los catetos de 2000 m y 1000 m, que darían $\sqrt{2000^2+1000^2}=2236$ m. El método de los tres puntos solo necesita las coordenadas de los puntos, de modo que el resultado no se ve afectado.

## 3.7 Piezómetros A, B, C, D

Separación $\Delta L = 5000$ m, gradiente $i = 0.019$ m/m. Pérdida de carga entre piezómetros consecutivos:

$$\Delta h = i\,\Delta L = 0.019 \times 5000 = 95\ \mathrm{m}$$

Como el nivel de agua está **en el tope de cada piezómetro**, la altura de presión en el fondo (punto de medida) es igual a la longitud de la columna de agua, es decir, igual a la profundidad del piezómetro. Y $z = h - h_p$.

| Piezómetro | A | B | C | D |
|---|---|---|---|---|
| Profundidad (m) | 200 | 190 | 50 | 8 |
| **Carga total $h$ (m)** | **300** | **205** | **110** | **15** |
| **Altura de presión $h_p$ (m)** | **200** | **190** | **50** | **8** |
| **Altura de elevación $z$ (m)** | **100** | **15** | **60** | **7** |

Cálculos de la fila de carga total:

$$h_B = 300-95 = 205\ \mathrm{m};\quad h_C = 205-95 = 110\ \mathrm{m};\quad h_D = 110-95 = 15\ \mathrm{m}$$

## 3.8 Conversiones de $K = 10^{-6}$ m/s

**(a) pies por segundo**

$$K = \frac{10^{-6}\ \mathrm{m/s}}{0.3048\ \mathrm{m/ft}} = \boxed{3.28\times10^{-6}\ \mathrm{ft/s}}$$

**(b) galones por día por $\mathrm{ft^2}$**

$$K = \left(3.28\times10^{-6}\ \tfrac{\mathrm{ft^3}}{\mathrm{s\cdot ft^2}}\right)\left(7.4805\ \tfrac{\mathrm{gal}}{\mathrm{ft^3}}\right)\left(86\,400\ \tfrac{\mathrm{s}}{\mathrm{d}}\right)$$

$$\boxed{K = 2.12\ \mathrm{gpd/ft^2}}$$

**(c) permeabilidad intrínseca en $\mathrm{cm^2}$**

$$k = \frac{K\mu}{\rho_w g} = \frac{(10^{-6})(1.0\times10^{-3})}{(1000)(9.81)} = 1.019\times10^{-13}\ \mathrm{m^2}$$

$$\boxed{k = 1.02\times10^{-9}\ \mathrm{cm^2}}$$

(Con $\mu = 1.124\times10^{-3}$ Pa·s, a 15.6 °C, se obtiene $1.15\times10^{-9}\ \mathrm{cm^2}$.)

**(d) permeabilidad en darcys**

$$k = \frac{1.019\times10^{-9}\ \mathrm{cm^2}}{9.87\times10^{-9}\ \mathrm{cm^2/darcy}} = \boxed{0.103\ \text{darcy} \approx 103\ \mathrm{md}}$$

Regla de verificación rápida: para agua a 20 °C, $1\ \text{darcy}\approx 9.66\times10^{-6}$ m/s; $0.103 \times 9.66\times10^{-6} = 1.0\times10^{-6}$ m/s ✓

## 3.9 Condiciones para $q_x = (k/\mu)(\partial P/\partial x)$

Se parte de la ley de Darcy en términos de carga y se sustituye $h = z + P/\rho_w g$ y $K = k\rho_w g/\mu$:

$$q_x = -K\frac{\partial h}{\partial x} = -\frac{k\rho_w g}{\mu}\frac{\partial}{\partial x}\!\left(z + \frac{P}{\rho_w g}\right)$$

$$q_x = -\underbrace{\frac{k\rho_w g}{\mu}\frac{\partial z}{\partial x}}_{\text{término gravitatorio}} \;-\; \frac{k}{\mu}\frac{\partial P}{\partial x}$$

La expresión pedida se obtiene **solo si $\partial z/\partial x = 0$**, es decir:

$$\boxed{q_x = -\frac{k}{\mu}\frac{\partial P}{\partial x}}$$

**Condiciones requeridas:**

1. **Flujo horizontal**: las dos presiones se miden a la *misma* elevación (fondos de barreno a igual cota), de modo que el término de elevación desaparece.
2. Fluido **homogéneo** de $\rho$ y $\mu$ constantes (isotérmico, no salino).
3. Medio con $k$ constante en el intervalo y flujo laminar (Re < 1–10).

El signo negativo es obligatorio: el flujo va de mayor a menor presión.

## 3.10 Expresiones incorrectas de la ley de Darcy

| | Expresión | Veredicto |
|---|---|---|
| a | $Q = KiA$ | **Correcta** (escrita en magnitudes, $i$ = magnitud del gradiente) |
| b | $q = K\,\mathrm{grad}\,h$ | **Incorrecta** — falta el signo menos |
| c | $q = (K/g)\,\mathrm{grad}\,\phi$ | **Incorrecta** — falta el signo menos (dimensionalmente correcta: $\phi = gh \Rightarrow (K/g)\nabla\phi = K\nabla h$) |
| d | $q = v/n_e$ | **Incorrecta** — la relación está invertida: $v = q/n_e$, luego $q = v\,n_e$ |
| e | $v = (K/n_e)\,\mathrm{grad}\,h$ | **Incorrecta** — falta el signo menos |
| f | $v = (k\rho g/\mu n_e)\,\mathrm{grad}\,h$ | **Incorrecta** — falta el signo menos (por lo demás idéntica a (e), ya que $K = k\rho g/\mu$) |
| g | $q = (k\rho g/\mu)\,\mathrm{grad}\,h$ | **Incorrecta** — falta el signo menos (por lo demás idéntica a (b)) |

**Resumen.** Si el criterio es la forma vectorial estricta, **todas excepto (a) son incorrectas**: b, c, e, f y g omiten el signo negativo y (d) además invierte la relación entre $q$ y $v$.

Si se ignoran los signos (interpretando todo en magnitudes), **la única realmente errónea es (d)**.

## 3.11 Conductividad equivalente de tres capas

Datos: $b_1=b_2=b_3=20$ m; $K_1=10^{-6}$, $K_2=10^{-7}$, $K_3=10^{-8}$ m/s; $\sum b = 60$ m.

**Horizontal (media aritmética ponderada — resistencias en paralelo)**

$$K_h = \frac{\sum K_i b_i}{\sum b_i} = \frac{20(10^{-6}+10^{-7}+10^{-8})}{60} = \frac{2.22\times10^{-5}}{60}$$

$$\boxed{K_h = 3.70\times10^{-7}\ \mathrm{m/s}}$$

**Vertical (media armónica ponderada — resistencias en serie)**

$$K_v = \frac{\sum b_i}{\sum (b_i/K_i)} = \frac{60}{\dfrac{20}{10^{-6}}+\dfrac{20}{10^{-7}}+\dfrac{20}{10^{-8}}} = \frac{60}{2.22\times10^{9}}$$

$$\boxed{K_v = 2.70\times10^{-8}\ \mathrm{m/s}}$$

**Anisotropía**

$$\frac{K_h}{K_v} = \frac{3.70\times10^{-7}}{2.70\times10^{-8}} = \boxed{13.7}$$

Observación: $K_h$ está dominada por la capa **más permeable** y $K_v$ por la **menos permeable**. Siempre $K_v \le K_h$.

## 3.12 Medio anisótropo: términos cruzados

Ley de Darcy tensorial (en magnitudes):

$$q_y = K_{yx}\frac{\partial h}{\partial x} + K_{yy}\frac{\partial h}{\partial y}$$

Primer ensayo: $\partial h/\partial y = 0$, $\partial h/\partial x = 0.1$ cm/cm, $q_y = 0.001$ cm/s:

$$K_{yx} = \frac{q_y}{\partial h/\partial x} = \frac{0.001}{0.1} = 0.01\ \mathrm{cm/s}$$

El tensor de conductividad hidráulica es **simétrico** ($K_{xy} = K_{yx}$), por lo que en el segundo ensayo ($\partial h/\partial x = 0$, $\partial h/\partial y = 0.01$ cm/cm):

$$q_x = K_{xy}\frac{\partial h}{\partial y} = (0.01)(0.01)$$

$$\boxed{q_x = 1\times10^{-4}\ \mathrm{cm/s}}$$

## 3.13 Conductividades relativas en la figura 3.E4

Con entrada = salida, $Q$ es constante a través de cada sección. Entre dos equipotenciales separadas $L_i$ con la misma caída de carga $\Delta h$:

$$Q = K_i A_i \frac{\Delta h}{L_i} = \text{cte}
\qquad\Longrightarrow\qquad
\boxed{K_i \propto \frac{L_i}{A_i}}$$

donde $A_i$ es el área transversal media de la franja ($A_i \approx \bar{b}_i \times$ ancho unitario).

**Criterio de lectura:** a igual espesor, mayor separación entre equipotenciales ⇒ menor gradiente ⇒ se necesita **mayor** $K$ para transmitir el mismo $Q$.

| | Respuesta |
|---|---|
| **(a) $K$ más alta** | La región **$K_3$** (la de la derecha): equipotenciales más separadas y espesor menor |
| **(b) $K$ más baja** | La región **$K_2$** (la central): equipotenciales más próximas con espesor intermedio |
| **(c) Relación** | $\dfrac{K_3}{K_2} = \dfrac{L_3/A_3}{L_2/A_2} \approx \mathbf{3\ a\ 4\ veces}$ |

> **Importante.** $L_i$ y $b_i$ deben escalarse con regla sobre la figura del libro. Con la lectura relativa $L_1:L_2:L_3 \approx 0.20:0.15:0.45$ y $\bar b_1:\bar b_2:\bar b_3 \approx 0.93:0.80:0.65$ se obtiene $K_1:K_2:K_3 \approx 0.22:0.19:0.69$, es decir $K_3/K_2 \approx 3.7$. **Mide tú la figura de tu edición y reemplaza**; el criterio y la fórmula son lo evaluable.

## 3.14 Espaciamiento de equipotenciales con recarga y descarga

El caso de referencia (entrada = salida, medio homogéneo e isótropo) tiene espaciamiento **uniforme**.

**(a) Recarga uniforme sobre todo el campo de flujo**

El caudal $Q$ **aumenta** en la dirección del flujo porque se agrega agua en cada tramo. Con $K$ y $A$ constantes, $i = Q/(KA)$ debe crecer:

$$\boxed{\text{Las equipotenciales se van } \textbf{juntando} \text{ (acercando) en la dirección del flujo}}$$

La superficie potenciométrica se vuelve **convexa hacia arriba**.

**(b) Descarga natural uniforme sobre todo el campo de flujo**

El caudal **disminuye** en la dirección del flujo (evapotranspiración, manantiales, goteo ascendente), de modo que $i$ decrece:

$$\boxed{\text{Las equipotenciales se van } \textbf{separando} \text{ en la dirección del flujo}}$$

La superficie potenciométrica se vuelve **cóncava hacia arriba**.

## 3.15 Dirección y magnitud del flujo vertical a través de la arcilla

Capa de arcilla de espesor uniforme $b'$ y conductividad vertical $K'$ constante. La ley de Darcy vertical da:

$$q_z = K'\frac{\Delta h}{b'}$$

| Región | $h$ acuífero superior | $h$ acuífero inferior | $\Delta h$ |
|---|---|---|---|
| Cerca de $h_4$ | 70 m | 60 m | **10 m** |
| Cerca de $h_1$ | 30 m | 25 m | **5 m** |

$$\frac{q_{z,(h_4)}}{q_{z,(h_1)}} = \frac{\Delta h_4}{\Delta h_1} = \frac{10}{5} = 2$$

**Respuestas:**

- La velocidad vertical es **mayor en la región de $h_4$**, exactamente **el doble**, porque con $K'$ y $b'$ idénticos el gradiente vertical es el doble ($0.5\,b'^{-1}\cdot$ ... en términos de $\Delta h$: 10 m frente a 5 m).
- En **ambas** regiones el flujo es **descendente**, porque la carga del acuífero superior supera la del inferior (70 > 60 y 30 > 25). Hay fuga (*leakage*) hacia abajo en todo el dominio.

## 3.16 Descarga específica a través de la capa confinante

De la figura: carga en la unidad superior = 100 m, carga en el acuífero inferior = 95 m, espesor de la capa confinante $b' = 10$ m.

$$i = \frac{100 - 95}{10} = 0.5\ \mathrm{m/m}$$

$$q = K'\,i = (10^{-7}\ \mathrm{cm/s})(0.5)$$

$$\boxed{q = 5\times10^{-8}\ \mathrm{cm/s}\ \ \text{(descendente)}}$$

En otras unidades: $5\times10^{-10}$ m/s $= 1.58\times10^{-2}$ m/año $\approx 1.6$ cm/año.

El flujo es **hacia abajo**, de la zona de 100 m de carga a la de 95 m.

## 3.17 Sistema de dos acuíferos con fuga

Geometría (de la figura): longitud en dirección del flujo $L = 1000$ m, ancho $W = 100$ m, acuífero superior 10 m, capa confinante 20 m, acuífero inferior 10 m.

Datos: $K_{ac} = 10^{-6}$ m/s, $K' = 10^{-9}$ m/s, $\Delta h$ entre acuíferos $= 10$ m (inferior más alto), $i_{entrada} = 10^{-1}$ m/m.

**(a) Caudal de entrada**

Área transversal de cada acuífero: $A = 10\ \mathrm{m}\times100\ \mathrm{m} = 1000\ \mathrm{m^2}$

$$Q_{in} = K\,i\,A = (10^{-6})(0.1)(1000)$$

$$\boxed{Q_{in} = 1\times10^{-4}\ \mathrm{m^3/s\ \ en\ cada\ acuífero};\qquad \sum Q_{in} = 2\times10^{-4}\ \mathrm{m^3/s}}$$

**(b) Caudal de salida**

Fuga vertical ascendente a través de la capa confinante (del inferior, de mayor carga, al superior):

$$q_{fuga} = K'\frac{\Delta h}{b'} = 10^{-9}\cdot\frac{10}{20} = 5\times10^{-10}\ \mathrm{m/s}$$

Área en planta: $A_{planta} = 1000 \times 100 = 1\times10^{5}\ \mathrm{m^2}$

$$Q_{fuga} = (5\times10^{-10})(1\times10^{5}) = 5\times10^{-5}\ \mathrm{m^3/s}$$

Balance de masa en cada acuífero:

$$\boxed{Q_{out,\,superior} = 1\times10^{-4} + 5\times10^{-5} = 1.5\times10^{-4}\ \mathrm{m^3/s}}$$

$$\boxed{Q_{out,\,inferior} = 1\times10^{-4} - 5\times10^{-5} = 5\times10^{-5}\ \mathrm{m^3/s}}$$

Verificación global: $1.5\times10^{-4}+5\times10^{-5} = 2\times10^{-4}\ \mathrm{m^3/s} = \sum Q_{in}$ ✓

**(c) Gradientes en la zona de salida**

$$i = \frac{Q_{out}}{K A}$$

$$i_{superior} = \frac{1.5\times10^{-4}}{(10^{-6})(1000)} = \boxed{0.15\ \mathrm{m/m}}
\qquad
i_{inferior} = \frac{5\times10^{-5}}{(10^{-6})(1000)} = \boxed{0.05\ \mathrm{m/m}}$$

**(d) Forma de las superficies piezométricas**

```
  carga
    ^
    |  inferior (entra con i=0.1, pierde agua por fuga)
    |  *.
    |    '*..                    <- se APLANA: 0.10 -> 0.05
    |        '**..
    |             '***....
    |                    '*****......
    |  superior (entra con i=0.1, recibe agua por fuga)
    |  o.
    |    'o..
    |       'oo.                 <- se EMPINA: 0.10 -> 0.15
    |          'oo.
    |             'oo
    |               'o
    +--------------------------------------> distancia (0 -> 1000 m)
        entrada                    salida
```

- **Acuífero inferior:** la superficie piezométrica **se aplana** progresivamente (gradiente de 0.10 a 0.05 m/m) porque va perdiendo caudal hacia arriba.
- **Acuífero superior:** la superficie piezométrica **se empina** progresivamente (gradiente de 0.10 a 0.15 m/m) porque va ganando caudal.
- Las dos superficies **convergen** hacia la salida: la diferencia de 10 m se reduce aguas abajo, y con ella la tasa de fuga (en un cálculo riguroso, no uniforme).

---

# CAPÍTULO 4 — Main Equations of Flow, Boundary Conditions, and Flow Nets

Ecuación de partida (Ec. 4.31):

$$\nabla^2 h = \frac{\rho_w g\,(\beta_p + n\beta_w)}{K}\,\frac{\partial h}{\partial t} \;\approx\; \frac{S_s}{K}\,\frac{\partial h}{\partial t}$$

## 4.1 Formas particulares de la ecuación 4.31

**(a) Flujo unidimensional**

$$\boxed{\frac{\partial^2 h}{\partial x^2} = \frac{\rho_w g(\beta_p + n\beta_w)}{K}\,\frac{\partial h}{\partial t} = \frac{S_s}{K}\frac{\partial h}{\partial t}}$$

En términos de acuífero (multiplicando por el espesor $b$): $\dfrac{\partial^2 h}{\partial x^2} = \dfrac{S}{T}\dfrac{\partial h}{\partial t}$

**(b) Fluido incompresible** → $\beta_w = 0$

$$\boxed{\nabla^2 h = \frac{\rho_w g\,\beta_p}{K}\,\frac{\partial h}{\partial t}}$$

Todo el agua liberada del almacenamiento proviene de la **compactación de la matriz**.

**(c) Fluido y matriz incompresibles** → $\beta_w = \beta_p = 0$

$$\boxed{\nabla^2 h = 0}$$

Ecuación de **Laplace**: flujo en régimen permanente, sin almacenamiento. Es la base de todas las redes de flujo.

**(d) ¿Dónde se puede despreciar $\rho_w g\,n\beta_w$?**

El término $n\beta_w$ (compresibilidad del agua) es despreciable frente a $\beta_p$ cuando la matriz es muy compresible:

$$\boxed{\text{En la ARCILLA}}$$

Para arcilla, $\beta_p \sim 10^{-6}$–$10^{-8}\ \mathrm{m^2/N}$, mientras que $n\beta_w \sim 1.4\times10^{-10}\ \mathrm{m^2/N}$: hay 2 a 4 órdenes de magnitud de diferencia. En el extremo opuesto (granito, caliza densa, siltstone muy cementado) $\beta_p$ es tan pequeña que el término del agua es el dominante y **no** puede despreciarse.

Orden creciente de importancia relativa de $n\beta_w$: arcilla < limo/arena < grava < caliza < granito.

## 4.2 Almacenamiento de un acuífero elástico

Datos: $S = 3\times10^{-4}$, $n = 0.3$, $\beta_w = 4.8\times10^{-10}\ \mathrm{m^2/N}$, $b = 60$ m.

**(a) Volumen extraído del almacenamiento**

$$V = S\cdot A\cdot \Delta h = (3\times10^{-4})(1\times10^{6}\ \mathrm{m^2})(1\ \mathrm{m})$$

$$\boxed{V = 300\ \mathrm{m^3}}$$

**(b) Almacenamiento con matriz incompresible ($\beta_p = 0$)**

$$S = \rho_w g\,b\,(\beta_p + n\beta_w) \;\to\; S = \rho_w g\,b\,n\beta_w$$

$$S = (1000)(9.81)(60)(0.3)(4.8\times10^{-10})$$

$$\boxed{S = 8.48\times10^{-5}}$$

Es decir, solo el **28 %** del almacenamiento real ($8.48\times10^{-5}/3\times10^{-4}$); el 72 % restante proviene de la compresión de la matriz.

**(c) Compresibilidad vertical del acuífero $\beta_p$**

$$\beta_p = \frac{S}{\rho_w g\,b} - n\beta_w = \frac{3\times10^{-4}}{(1000)(9.81)(60)} - (0.3)(4.8\times10^{-10})$$

$$\beta_p = 5.097\times10^{-10} - 1.44\times10^{-10}$$

$$\boxed{\beta_p = 3.66\times10^{-10}\ \mathrm{m^2/N}}$$

Valor típico de arena/grava densa. Comprobación: $S = (9810)(60)(3.657\times10^{-10}+1.44\times10^{-10}) = 3.0\times10^{-4}$ ✓

## 4.3 Significado físico del almacenamiento

**(a)** La tasa de descenso de carga multiplicada por el almacenamiento, integrada sobre el área afectada, equivale al

$$\boxed{\text{caudal de bombeo } Q\ \ \mathrm{[L^3/T]}}$$

$$Q = \int_A S\,\frac{\partial h}{\partial t}\,dA$$

**(b)** El descenso total de carga, integrado sobre el área afectada, multiplicado por el almacenamiento, equivale al

$$\boxed{\text{volumen total de agua extraída del almacenamiento hasta ese instante, } V = Qt\ \ \mathrm{[L^3]}}$$

$$V = \int_A S\,\Delta h\,dA = Q\,t$$

## 4.4 Esfuerzos en una excavación en arcilla sobre un acuífero artesiano

Datos: arcilla de 0 a 50 ft, $\gamma_{sat} = 125\ \mathrm{lb/ft^3}$, $\gamma_w = 62.4\ \mathrm{lb/ft^3}$, nivel freático en superficie, carga artesiana en el techo del acuífero = 20 ft **sobre** la superficie del terreno.

La carga de presión en la base de la arcilla (a 50 ft de profundidad) es:

$$h_p = 50 + 20 = 70\ \mathrm{ft}$$

**(a) Condición original (sin excavación), en la base de la arcilla**

$$\sigma_T = \gamma_{sat}\,z = (125)(50) = \boxed{6250\ \mathrm{lb/ft^2}}$$

$$u = \gamma_w\,h_p = (62.4)(70) = \boxed{4368\ \mathrm{lb/ft^2}}$$

$$\sigma' = \sigma_T - u = 6250 - 4368 = \boxed{1882\ \mathrm{lb/ft^2}}$$

Factor de seguridad frente a levantamiento: $FS = \sigma_T/u = 6250/4368 = 1.43$

**(b) Zanja de 20 ft llena de agua hasta la superficie**

Debajo de la zanja quedan $50-20 = 30$ ft de arcilla, más 20 ft de agua:

$$\sigma_T = (125)(30) + (62.4)(20) = 3750 + 1248 = \boxed{4998\ \mathrm{lb/ft^2}}$$

$$u = 4368\ \mathrm{lb/ft^2}\ \ \text{(no cambia: la controla el acuífero)}$$

$$\sigma' = 4998 - 4368 = \boxed{630\ \mathrm{lb/ft^2}}$$

$FS = 4998/4368 = 1.14$. Estable, pero con margen escaso.

**(c) ¿Es estable si se deseca la zanja?**

Al retirar los 20 ft de agua se pierde la contrapresión de 1248 lb/ft²:

$$\sigma_T = (125)(30) = 3750\ \mathrm{lb/ft^2} \;<\; u = 4368\ \mathrm{lb/ft^2}$$

$$\sigma' = 3750 - 4368 = \boxed{-618\ \mathrm{lb/ft^2}}$$

$$\boxed{\textbf{NO.}\ \ FS = 3750/4368 = 0.86 < 1 \Rightarrow \text{el fondo falla (reventón / arena movediza)}}$$

El esfuerzo efectivo negativo significa que la presión artesiana levanta el tapón de arcilla. Para excavar en seco hay que **despresurizar el acuífero** (pozos de alivio) hasta bajar la carga al menos a $3750/62.4 = 60.1$ ft, es decir, reducir la carga artesiana en más de 10 ft.

**(d) Profundidad crítica de zanja (llena de agua)**

Sea $d$ la profundidad excavada. Quedan $(50-d)$ ft de arcilla más $d$ ft de agua. La condición de falla es $\sigma_T = u$:

$$\gamma_{sat}(50-d) + \gamma_w d = \gamma_w(70)$$

$$125(50) - 125d + 62.4d = 4368$$

$$6250 - 62.6\,d = 4368 \qquad\Longrightarrow\qquad d = \frac{1882}{62.6}$$

$$\boxed{d_{crit} \approx 30.1\ \mathrm{ft}}$$

Forma general útil:

$$d_{crit} = \frac{\gamma_{sat} D - \gamma_w h_p}{\gamma_{sat} - \gamma_w} = \frac{\sigma'_{inicial}}{\gamma_{sat}-\gamma_w}$$

Comprobación: con $d = 30.1$ ft, $\sigma_T = 125(19.9)+62.4(30.1) = 2487+1878 = 4365 \approx 4368$ ✓

## 4.5 Transmisividad en el centro de bombeo B (figura 4.10)

Para una red de flujo en planta con celdas cuadradas, cada tubo de flujo transporta

$$\Delta Q = T\,\Delta h$$

donde $\Delta h$ es la caída de carga entre equipotenciales consecutivas. Todo el caudal bombeado en B entra por los $n_f$ tubos de flujo que convergen al cono:

$$Q = n_f\,T\,\Delta h
\qquad\Longrightarrow\qquad
\boxed{T = \frac{Q}{n_f\,\Delta h}}$$

Datos: $Q = 3\times10^{4}\ \mathrm{m^3/día}$; intervalo entre curvas de la figura 4.10 $= 10\ \mathrm{ft} = 3.048$ m.

| $n_f$ (tubos contados hacia B) | $T$ (m²/día) |
|---|---|
| 6 | 1640 |
| **8** | **1230** |
| 10 | 984 |

$$\boxed{T \approx 1.2\times10^{3}\ \mathrm{m^2/día} \quad (\text{con } n_f = 8)}$$

Equivalente: $T \approx 1.4\times10^{-2}\ \mathrm{m^2/s}$; si $b \approx 30$ m, $K \approx 41$ m/día $= 4.7\times10^{-4}$ m/s (arena limpia, coherente con la Formación Patuxent).

> **Importante.** $n_f$ se obtiene **contando sobre la figura 4.10** los tubos de flujo que descargan en B. Cuenta tú los de tu copia y reemplaza en la fórmula; el rango razonable es $T \approx 1000$–$1600\ \mathrm{m^2/día}$. Lo evaluable es la relación $T = Q/(n_f\Delta h)$.

## 4.6 Clasificación de las fronteras (figura del problema 6)

Presa con delantal impermeable (*impervious blanket*) sobre una cimentación permeable.

| Frontera | Tipo de línea | Tipo de condición de borde |
|---|---|---|
| **AB** | **Equipotencial** | **Carga constante** ($h$ = nivel del embalse aguas arriba) |
| **BC** | **Línea de flujo** | **Impermeable / sin flujo** (es el delantal impermeable) |
| **CD** | **Línea de flujo** | **Impermeable / sin flujo** (base de la presa) |
| **DE** | **Equipotencial** | **Carga constante** ($h$ = nivel aguas abajo) |
| **FG** | **Línea de flujo** | **Impermeable / sin flujo** (base impermeable del estrato permeable) |

Reglas aplicadas:

$$\text{Carga constante: } h = \text{cte} \;\Rightarrow\; \text{equipotencial; las líneas de flujo la cruzan a }90^\circ$$

$$\text{Sin flujo: } \frac{\partial h}{\partial n} = 0 \;\Rightarrow\; \text{línea de flujo; las equipotenciales la cruzan a }90^\circ$$

## 4.7 Caudal de filtración con y sin delantal

Para una red de flujo con celdas cuadradas, por unidad de ancho de presa:

$$\boxed{Q = K\,H\,\frac{n_f}{n_d}}$$

$n_f$ = número de canales (tubos) de flujo, $n_d$ = número de saltos de potencial, $H$ = carga total disponible.

Datos: $H = 20$ m, $K = 5\times10^{-4}$ m/s.

| Caso | $n_f$ | $n_d$ | $Q$ (m³/s por m) | % respecto al caso base |
|---|---|---|---|---|
| Delantal completo (problema 6) | 5 | 15 | $3.33\times10^{-3}$ | 100 % |
| Delantal a la mitad (a) | 5 | 12 | $4.17\times10^{-3}$ | 125 % |
| Sin delantal (b) | 5 | 9 | $5.56\times10^{-3}$ | 167 % |

Ejemplo de cálculo (caso base):

$$Q = (5\times10^{-4})(20)\left(\frac{5}{15}\right) = 3.33\times10^{-3}\ \mathrm{m^3/s\ por\ m} = 288\ \mathrm{m^3/día\ por\ m}$$

**Conclusión física.** El delantal impermeable **alarga la trayectoria de filtración** (aumenta $n_d$, es decir, consume más saltos de potencial) sin cambiar el número de canales de flujo. Al acortarlo a la mitad la filtración sube ~25 %; al eliminarlo, ~67 %. Además, al desaparecer el delantal **aumenta el gradiente de salida** aguas abajo, lo que es el verdadero riesgo (tubificación / *piping*).

> Los valores de $n_f$ y $n_d$ dependen de tu propio trazado. Mantén $n_f$ constante entre los tres casos y ajusta $n_d$; lo que se evalúa es la **tendencia** y el uso correcto de $Q = KH\,n_f/n_d$.

## 4.8 Redes de flujo en la sección ABCD

Sección rectangular: AB arriba, DC abajo, AD izquierda, BC derecha; lados $=\tfrac12$ de la longitud de AB.

**(a) AB carga constante 60 m; AD y BC impermeables; DC mitad izquierda con carga 10 m, mitad derecha impermeable**

```
A ======================================================= B     h = 60 m (equipotencial)
| \   \    \     \      \       \        \       \      . |
|  \   \    \     \      \       \       \      .       . |
|   \   \    \     \      \      \      .      .       .  |   AD, BC: sin flujo
|    \   \    \     \      \     \     .      .       .   |   (lineas de flujo)
|     \   \    \     \     \     \    .      .       .    |
D ================================+++++++++++++++++++++++ C
   h = 10 m (equipotencial)        DC derecha: impermeable
   SALIDA de todo el caudal        (linea de flujo)
```

Características a reproducir en el dibujo:
- Todo el caudal entra por AB y sale **solo por la mitad izquierda de DC**.
- Las líneas de flujo **convergen** hacia DC-izquierda; allí el espaciamiento de equipotenciales es mínimo (gradiente máximo).
- En la esquina inferior derecha el agua está prácticamente **estancada**: celdas muy grandes, gradiente casi nulo.
- En el punto de transición de DC (de carga constante a impermeable) hay una **singularidad**: el gradiente tiende a infinito; se dibuja la última línea de flujo entrando casi vertical.
- Las líneas de flujo son perpendiculares a AB y a DC-izquierda; son **paralelas** a AD, BC y DC-derecha.

**(b) AB carga 60 m; DC impermeable; en AD y BC: segmento superior impermeable y segmento inferior con carga 10 m**

```
A ======================================================= B    h = 60 m
|  .                                                  .  |
|   .                                                .   |   mitad superior de los
|    .                                              .    |   lados: impermeable
+~~~~~.                                          .~~~~~~ +   <- cambio de condicion
|      '.                                      .'        |
| h=10   '..                                ..'   h=10   |   mitad inferior:
|  (salida)  '''...................''''      (salida)    |   carga constante 10 m
D +++++++++++++++++++++++++++++++++++++++++++++++++++++++ C
                  DC: impermeable (linea de flujo)
```

Características:
- El flujo entra por AB y **se divide simétricamente** hacia los dos lados.
- Hay una **divisoria vertical de flujo** en el eje central de la sección (línea de flujo recta vertical), igual que en la figura 5.5 del capítulo 5.
- En el fondo DC el flujo es **horizontal** (DC es línea de flujo).
- Las zonas de mayor gradiente son las esquinas D y C, donde confluyen la frontera impermeable y la de carga constante.

## 4.9 Red de flujo con nivel freático inclinado

Sección modificada: BC (derecha) es $1.5\times$ AD (izquierda); DC permanece horizontal; AB es un nivel freático **inclinado** (de B, más alto a la derecha, hacia A). AD, BC y DC son impermeables; AB es frontera de carga variable con $h = z$ (en el nivel freático la presión es atmosférica).

```
                                                      B
                                       ....'''''''''  |
                      ....''''''''''                  |
A ....''''''''                                        |
|   |   |    |    |     |     |      |      |     |   |   <- equipotenciales
| 1 | 2 |  3 |  4 |  5  |  6  |  7   |  8   |  9  | 10|      (casi verticales)
|---+---+----+----+-----+-----+------+------+-----+---|   <- lineas de flujo
|   |   |    |    |     |     |      |      |     |   |      (casi horizontales)
D +++++++++++++++++++++++++++++++++++++++++++++++++++++ C
```

Reglas de construcción:
1. En AB: $h = z$. Por eso las equipotenciales **intersecan el nivel freático en el punto cuya cota es igual al valor de la equipotencial**. Esto obliga a que las equipotenciales lleguen inclinadas, no perpendiculares, al nivel freático (AB no es equipotencial).
2. En AD, BC y DC: $\partial h/\partial n = 0$, por lo que son líneas de flujo. Las equipotenciales las cortan a 90°.
3. El flujo va de B (zona alta, **recarga**, flujo descendente) hacia A (zona baja, **descarga**, flujo ascendente).
4. Las celdas deben ser aproximadamente cuadradas ("curvilinear squares").
5. Como todo el dominio es cerrado salvo el nivel freático, $\sum Q_{\text{recarga}} = \sum Q_{\text{descarga}}$: las áreas de entrada y salida sobre AB son comparables.
6. Las líneas de flujo más profundas son las de recorrido más largo y lento (sistema regional); las superficiales, cortas y rápidas (sistema local).

## 4.10 La misma red en medio anisótropo ($K_h = 5K_v$)

Las celdas cuadradas **solo son válidas en medio isótropo**. El procedimiento es el de la **sección transformada**:

**Paso 1 — Transformar.** Se contrae la escala horizontal:

$$x' = x\sqrt{\frac{K_v}{K_h}} = x\sqrt{\frac{1}{5}} = 0.447\,x$$

(equivalentemente, se puede expandir la vertical: $z' = z\sqrt{K_h/K_v} = 2.236\,z$).

**Paso 2 — Dibujar.** En la sección transformada el medio es isótropo, de modo que se traza una red de **celdas cuadradas** normal, con las mismas reglas del problema 4.9.

**Paso 3 — Destransformar.** Se devuelve la escala original multiplicando $x$ por $\sqrt{K_h/K_v}=2.236$. Las celdas dejan de ser cuadradas: quedan **rectángulos alargados horizontalmente** con relación de lados

$$\frac{\text{largo}}{\text{ancho}} = \sqrt{\frac{K_h}{K_v}} = \sqrt{5} = 2.24$$

**Paso 4 — Conductividad equivalente para el caudal.**

$$\boxed{K_{eq} = \sqrt{K_h K_v} = \sqrt{5}\,K_v = 2.24\,K_v = 0.447\,K_h}$$

$$Q = K_{eq}\,H\,\frac{n_f}{n_d}$$

**Diferencias visibles respecto al problema 4.9:**

```
   ISOTROPO (prob. 9)            ANISOTROPO Kh=5Kv (prob. 10)
  +---+---+---+---+            +-------+-------+-------+
  |   |   |   |   |            |       |       |       |
  +---+---+---+---+            +-------+-------+-------+
  |   |   |   |   |            |       |       |       |
  +---+---+---+---+            +-------+-------+-------+
  celdas cuadradas             celdas 2.24 veces mas anchas
  flujo oblicuo                flujo refractado hacia la horizontal
```

- Las líneas de flujo se **aplanan**: el agua prefiere viajar horizontalmente, y los sistemas de flujo son **más someros y más extensos** lateralmente.
- En el medio original **las líneas de flujo ya no cortan a las equipotenciales a 90°** (solo lo hacen en la sección transformada), salvo cuando coinciden con los ejes principales de anisotropía.
- La penetración vertical del flujo desde la divisoria es menor; aumenta la proporción de flujo local frente al regional.

---

# CAPÍTULO 5 — Ground Water in the Basin Hydrologic Cycle

## 5.1 Condiciones de borde de las figuras 5.5 y 5.8

**Figura 5.5** — región bidimensional homogénea e isótropa, flujo regional en el plano $x$–$z$:

| Frontera | Condición | Significado físico |
|---|---|---|
| Lateral izquierda | $\dfrac{\partial h}{\partial x} = 0$ | **Divisoria de aguas subterráneas**: no hay flujo horizontal a través del eje de simetría (plano de simetría de la cuenca) |
| Lateral derecha | $\dfrac{\partial h}{\partial x} = 0$ | Ídem (eje del valle o divisoria opuesta) |
| Base | $\dfrac{\partial h}{\partial z} = 0$ | **Base impermeable** del sistema (basamento): no hay flujo vertical |
| Tope | $h = f(x)$ | **Nivel freático conocido** como función de la posición; se supone que replica la topografía |

Las tres primeras son condiciones de **Neumann** homogéneas (tipo 2, sin flujo); la cuarta es una condición de **Dirichlet** (tipo 1, carga especificada). Juntas definen un problema cerrado: todo el agua que entra como recarga en la parte alta del nivel freático sale como descarga en la parte baja.

**Figura 5.8** — modelo no confinado con $n$ capas homogéneas e isótropas ($K_1$, $K_2$, $K_3$). Incluye **todo lo anterior**, y añade:

$$\boxed{\phi_1 = \phi_2 \quad\text{y}\quad \phi_2 = \phi_3} \qquad \text{(continuidad del potencial en las interfaces)}$$

$$\boxed{K_1\frac{\partial \phi_1}{\partial z} = K_2\frac{\partial \phi_2}{\partial z} \quad\text{y}\quad K_2\frac{\partial \phi_2}{\partial z} = K_3\frac{\partial \phi_3}{\partial z}} \qquad \text{(continuidad del flujo normal)}$$

Además, el nivel freático se especifica como una función **lineal por tramos** ($C_1$, $C_2$, …, $C_{k+1}$ sobre los intervalos $x_1$, $x_2$, …, $x_k$), es decir, una topografía escalonada con varias pendientes, en lugar de una única función suave.

**¿Por qué aparecen estas condiciones y en 5.5 no?**

Porque la figura 5.5 es un medio **homogéneo**: no hay interfaces internas. En la figura 5.8 el dominio es **heterogéneo** (estratificado), y en cada contacto entre capas hay que imponer explícitamente las dos leyes de conservación:

1. La **carga (potencial) no puede ser discontinua** — si lo fuera, habría un gradiente infinito y un flujo infinito.
2. La **componente normal del flujo debe conservarse** — no se crea ni se destruye agua en la interfaz.

La segunda condición produce la **refracción de las líneas de flujo** en el contacto, que sigue la ley

$$\frac{\tan\theta_1}{\tan\theta_2} = \frac{K_1}{K_2}$$

(con $\theta$ medido respecto a la normal a la interfaz). Al pasar a una capa más permeable, las líneas de flujo se acercan a la interfaz (se "aplanan"); al pasar a una menos permeable, se verticalizan.

## 5.2 Construcción de redes de flujo (figuras 5.4 y 5.27)

**(a) Figura 5.4 (Tóth, 1962) con la frontera izquierda como frontera de FLUJO**

Original (figura 5.4): dominio simétrico cerrado, divisoria en el centro, laterales y base sin flujo. Resultado: celdas de flujo locales anidadas dentro del sistema regional, con descarga en el centro del valle.

Modificado (frontera izquierda permite flujo entrante):

```
   ORIGINAL (5.4): laterales sin flujo        MODIFICADO: izquierda = frontera de flujo
   __                                 __         __
  /  \_        nivel freatico       _/  \       /  \_                          __
 |  recarga                 recarga   |        | recarga                     _/  \
 | | | |                     | | | |  |        |  | | |                       | | |
 |-v-v-v-------- descarga ---v-v-v----|     -->|--v-v-v--------------- descarga ----
 |  \    \    /   ^ ^ ^   \    /   /  |     -->|   \   \    \     ^ ^ ^    /    /
 |   \    \  /    | | |    \  /   /   |     -->|    \   \    \    | | |   /    /
 |    \____\/_____|_|_|_____\/___/    |     -->|_____\___\____\___|_|_|__/____/
 |                                    |     -->|
 +====== base impermeable =============+        +====== base impermeable ========+
   ^                        ^                     ^
   divisoria (sin flujo)    divisoria              ENTRA flujo lateral
```

Cambios a dibujar:

1. **Desaparece la divisoria de flujo del lado izquierdo.** Ya no hay una línea de flujo vertical pegada a la frontera; las líneas de flujo **atraviesan** el borde izquierdo.
2. Sobre esa frontera las **equipotenciales llegan oblicuas o perpendiculares** (ya no son perpendiculares a ella como exige una frontera sin flujo).
3. El sistema **pierde la simetría**: la zona de descarga se desplaza y se amplía hacia la derecha, porque debe evacuar la recarga propia **más** el caudal que entra por la izquierda.
4. El **sistema regional se refuerza** a costa de los sistemas locales: las celdas locales del lado izquierdo se reducen o desaparecen, absorbidas por el flujo profundo que viene de fuera.
5. El balance ya no es $\sum$recarga $=\sum$descarga en el dominio, sino $\sum$recarga $+\,Q_{lateral} = \sum$descarga.

**(b) Figura 5.27 (perfil de pradera, Meyboom 1966) con $K_1 = K_2$**

El perfil original tiene una capa superior $K_1$ sobre una inferior $K_2$, con $K_2 \gg K_1$ (arena/grava bajo till glaciar de baja permeabilidad). Con $K_1 = K_2$ el medio pasa a ser **homogéneo**:

1. **Desaparece la refracción** de las líneas de flujo en el contacto entre $K_1$ y $K_2$: la red se vuelve continua y suave.
2. La capa inferior **deja de actuar como un "drenaje" preferencial**. En el original, la capa profunda de alta $K$ captura el flujo y lo conduce lateralmente hasta 50 millas (de ahí los *deep-flowing wells*).
3. Al eliminar ese conducto, el flujo **regional profundo se debilita** notablemente y los **sistemas locales dominan**: cada montículo topográfico genera su propia celda de recarga–descarga, con descarga en la depresión inmediata.
4. El patrón resultante es el de la figura 5.4 (Tóth): celdas locales anidadas controladas por la topografía, con penetración vertical proporcional a la longitud de onda topográfica.
5. Consecuencias hidroquímicas: **desaparece el área de descarga salina lejana** alimentada por el flujo regional; la salinización se concentra en las depresiones locales.

## 5.3 El canal a nivel del mar

**Planteamiento y datos**

| Parámetro | Valor |
|---|---|
| Nivel freático inicial, plano | $h_0 = 12$ m sobre el nivel del mar |
| Profundidad del canal | 9 m bajo el nivel del mar |
| Distancia a la divisoria (manantiales) | $L = 3\ \mathrm{mi} = 4828$ m |
| Conductividad hidráulica | $K = 8.35\ \mathrm{cm/día} = 0.0835\ \mathrm{m/día}$ |
| Rendimiento específico | $S_y = 0.01$ |

Se toma el **datum en el nivel del mar** (= nivel de agua en el canal) y la base del sistema en el fondo del canal. Espesor saturado: 21 m en la divisoria y 9 m en el canal, de modo que se linealiza con el valor medio

$$\bar b = \frac{21+9}{2} = 15\ \mathrm{m}$$

$$T = K\bar b = (0.0835)(15) = 1.2525\ \mathrm{m^2/día}$$

$$\nu = \frac{T}{S_y} = \frac{1.2525}{0.01} = 125.25\ \mathrm{m^2/día} \qquad \text{(difusividad hidráulica)}$$

**Solución (analogía con la conducción de calor en un medio semi-infinito)**

Al excavar el canal, la carga en $x=0$ cae instantáneamente de $h_0$ a 0 y se mantiene allí:

$$\boxed{h(x,t) = h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{\nu t}}\right) = h_0\,\mathrm{erf}\!\left(\frac{x}{2\sqrt{Tt/S_y}}\right)}$$

### (a) Carga en el canal y en la divisoria

**En el canal ($x = 0$):** $\mathrm{erf}(0)=0$, por lo tanto

$$\boxed{h_{canal} = 0\ \mathrm{m\ (nivel\ del\ mar)\ \ para\ \ \textit{todo}\ \ t}}$$

Es la condición de borde impuesta por el canal: el abatimiento allí es de 12 m desde el primer momento.

**En la divisoria ($x = L = 4828$ m):**

| $t$ (años) | $t$ (días) | $\dfrac{L}{2\sqrt{\nu t}}$ | $\mathrm{erf}(\cdot)$ | $h_{divisoria}$ (m) | Abatimiento (m) |
|---|---|---|---|---|---|
| 10 | 3 653 | 3.569 | 1.00000 | **12.00** | 0.00 |
| 20 | 7 305 | 2.524 | 0.99964 | **12.00** | 0.00 |
| 40 | 14 610 | 1.785 | 0.98839 | **11.86** | 0.14 |
| 100 | 36 525 | 1.129 | 0.88954 | **10.67** | 1.33 |

**Perfil completo del nivel freático** $h(x,t)$ en metros sobre el nivel del mar:

| $x$ (m) | 0 | 250 | 500 | 1000 | 2000 | 3000 | 4000 | 4828 |
|---|---|---|---|---|---|---|---|---|
| **10 años** | 0.00 | 2.47 | 4.79 | 8.45 | 11.56 | 11.98 | 12.00 | 12.00 |
| **20 años** | 0.00 | 1.76 | 3.46 | 6.48 | 10.33 | 11.68 | 11.96 | 12.00 |
| **40 años** | 0.00 | 1.25 | 2.47 | 4.79 | 8.45 | 10.60 | 11.56 | 11.86 |
| **100 años** | 0.00 | 0.79 | 1.58 | 3.11 | 5.90 | 8.14 | 9.77 | 10.67 |

**Interpretación.** El cono de abatimiento tarda **más de 40 años** en "sentir" la divisoria y a los 100 años solo la ha bajado 1.3 m de 12 m. La hipótesis de medio semi-infinito ($L\to\infty$) es por tanto válida durante todo el periodo analizado. La divisoria (los manantiales) persiste a escala de décadas, aunque su caudal disminuye.

### (b) Caudal de entrada al canal $q'$

Derivando la solución y evaluando en $x=0$:

$$q' = T\left.\frac{\partial h}{\partial x}\right|_{x=0} = \frac{T h_0}{\sqrt{\pi\nu t}}
\qquad\Longrightarrow\qquad
\boxed{q' = h_0\sqrt{\frac{T S_y}{\pi t}}}$$

**A 10 años ($t = 3653$ días):**

$$q' = 12\sqrt{\frac{(1.2525)(0.01)}{\pi\,(3653)}} = 12\sqrt{1.091\times10^{-6}}$$

$$\boxed{q' = 1.25\times10^{-2}\ \mathrm{m^3/día\ por\ metro\ de\ canal} = 12.5\ \mathrm{L/día\cdot m}}$$

**A 100 años ($t = 36\,525$ días):**

$$q' = 12\sqrt{\frac{(1.2525)(0.01)}{\pi\,(36\,525)}}$$

$$\boxed{q' = 3.96\times10^{-3}\ \mathrm{m^3/día\ por\ metro\ de\ canal} = 4.0\ \mathrm{L/día\cdot m}}$$

Si el canal recibe agua por **ambos flancos**, se duplica: $2.51\times10^{-2}$ y $7.93\times10^{-3}$ m³/día·m respectivamente.

**Verificación de la dependencia temporal.** Como $q' \propto t^{-1/2}$:

$$\frac{q'(10\ \mathrm{a})}{q'(100\ \mathrm{a})} = \sqrt{\frac{100}{10}} = \sqrt{10} = 3.16
\qquad\text{y en efecto}\qquad
\frac{1.254\times10^{-2}}{3.965\times10^{-3}} = 3.16\ \checkmark$$

> **Sensibilidad al espesor elegido.** Si en lugar de $\bar b = 15$ m se usa el espesor inicial completo $\bar b = 21$ m ($T = 1.754\ \mathrm{m^2/día}$), se obtiene $h_{divisoria}(100\ \mathrm{a}) = 9.87$ m, $q'(10\ \mathrm{a}) = 1.48\times10^{-2}$ y $q'(100\ \mathrm{a}) = 4.69\times10^{-3}\ \mathrm{m^3/día\cdot m}$. Las conclusiones no cambian; declara siempre el espesor que usaste.

## 5.4 Estabilidad de excavaciones — procedimiento del caso histórico

Este problema remite a los datos numéricos del caso histórico de las páginas 99–101 del libro (*The Stability of Excavations in Ground-Water Discharge Areas*). **No tengo acceso a esas páginas**, de modo que a continuación se da el procedimiento completo y se ejecuta con el conjunto de datos equivalente del problema 4.4, que es el mismo tipo de cálculo. Sustituye los valores de tu edición en las mismas fórmulas.

**Procedimiento (5 pasos)**

**Paso 1 — Esfuerzo total en la base del estrato confinante, bajo la excavación.**

$$\sigma_T = \gamma_{sat}\,(D - d) + \gamma_w\,d_w$$

donde $D$ = espesor original del confinante, $d$ = profundidad excavada, $d_w$ = profundidad de agua dentro de la excavación.

**Paso 2 — Presión neutra (de poro), fijada por el acuífero artesiano.**

$$u = \gamma_w\,h_p$$

$h_p$ = carga de presión en la base del confinante, medida en piezómetro. **No depende de la excavación.**

**Paso 3 — Esfuerzo efectivo.**

$$\sigma' = \sigma_T - u$$

**Paso 4 — Factor de seguridad frente a levantamiento / reventón del fondo.**

$$\boxed{FS = \frac{\sigma_T}{u} = \frac{\gamma_{sat}(D-d)+\gamma_w d_w}{\gamma_w h_p}}$$

$FS > 1$: estable. $FS = 1$: condición crítica ($\sigma'=0$, condición de arena movediza, *quick condition*). $FS < 1$: reventón del fondo. En la práctica se exige $FS \ge 1.3$–$1.5$.

**Paso 5 — Profundidad crítica.** Se impone $\sigma_T = u$ y se despeja $d$:

$$\boxed{d_{crit} = \frac{\gamma_{sat}D - \gamma_w h_p}{\gamma_{sat}-\gamma_w}}\qquad\text{(excavación llena de agua, } d_w=d)$$

$$\boxed{d_{crit} = D - \frac{\gamma_w h_p}{\gamma_{sat}}}\qquad\text{(excavación en seco, } d_w=0)$$

**Ejecución con el conjunto de datos equivalente** ($D = 50$ ft, $\gamma_{sat} = 125\ \mathrm{lb/ft^3}$, $h_p = 70$ ft, $\gamma_w = 62.4\ \mathrm{lb/ft^3}$):

| Caso | $\sigma_T$ (lb/ft²) | $u$ (lb/ft²) | $\sigma'$ (lb/ft²) | $FS$ | Estado |
|---|---|---|---|---|---|
| Sin excavar | 6250 | 4368 | 1882 | 1.43 | Estable |
| Zanja 20 ft con agua | 4998 | 4368 | 630 | 1.14 | Marginal |
| Zanja 20 ft en seco | 3750 | 4368 | −618 | 0.86 | **Falla** |
| Zanja 30.1 ft con agua | 4368 | 4368 | 0 | 1.00 | **Crítico** |

Profundidades críticas:

$$d_{crit}\ (\text{con agua}) = \frac{(125)(50)-(62.4)(70)}{125-62.4} = \frac{1882}{62.6} = 30.1\ \mathrm{ft}$$

$$d_{crit}\ (\text{en seco}) = 50 - \frac{(62.4)(70)}{125} = 50 - 34.9 = 15.1\ \mathrm{ft}$$

**Medidas correctivas** (lo que el caso histórico concluye):

1. **Despresurizar el acuífero** con pozos de alivio o pozos profundos de bombeo (*deep wells*) hasta que $u$ baje lo suficiente. Carga admisible: $h_p \le \sigma_T/(\gamma_w \cdot FS_{req})$.
2. **Mantener la excavación inundada** durante el avance (contrapresión de agua), excavando con draga.
3. **Dejar un tapón de arcilla más grueso** (reducir $d$) o lastrarlo.
4. **Nunca** desecar una excavación en zona de descarga sin verificar antes el $FS$ con los piezómetros instalados.

## 5.5 Caudal máximo de bombeo sin ascenso de la interfaz (upconing)

Datos: distancia del fondo del pozo a la interfaz $d = 40\ \mathrm{ft} = 12.192$ m; $K = 1\times10^{-1}\ \mathrm{cm/s} = 1\times10^{-3}\ \mathrm{m/s}$.

Densidad relativa del agua salada:

$$G = \frac{\Delta\rho}{\rho_f} = \frac{1025-1000}{1000} = 0.025$$

**Ascenso de la interfaz en estado estacionario** (Dagan y Bear, 1968; Schmorak y Mercado):

$$z = \frac{Q}{2\pi\,K\,d\,G}$$

**Criterio de estabilidad:** la interfaz es estable mientras el ascenso no supere aproximadamente $\tfrac13$ de la distancia disponible:

$$z \le 0.3\,d$$

Sustituyendo:

$$Q_{max} = 2\pi K d\,(0.3\,d)\,G
\qquad\Longrightarrow\qquad
\boxed{Q_{max} = 0.6\,\pi\,K\,d^{2}\,G}$$

$$Q_{max} = 0.6\pi\,(1\times10^{-3}\ \mathrm{m/s})\,(12.192\ \mathrm{m})^{2}\,(0.025)$$

$$Q_{max} = 0.6\pi\,(1\times10^{-3})(148.6)(0.025)$$

$$\boxed{Q_{max} = 7.0\times10^{-3}\ \mathrm{m^3/s} = 7.0\ \mathrm{L/s} = 605\ \mathrm{m^3/día} = 111\ \mathrm{gpm} = 0.247\ \mathrm{ft^3/s}}$$

**Lectura del resultado.** Bombear por encima de ~7 L/s hace que la interfaz ascienda más de 3.7 m (12 ft), entre en el régimen inestable y colapse hacia el pozo, salinizándolo de forma prácticamente irreversible. Nótese la dependencia **cuadrática** con $d$: duplicar la separación del pozo respecto a la interfaz **cuadruplica** el caudal admisible. De ahí la regla de diseño de perforar lo más somero posible en acuíferos costeros.

## 5.6 Posición del pie de la cuña de agua salada

Datos: espesor del acuífero $B = 100$ ft; $K = 3.3\times10^{-3}\ \mathrm{ft/s}$; $G = 0.025$.

**Solución de Glover (1959)** para la profundidad $z$ de la interfaz bajo el nivel del mar a una distancia $x$ tierra adentro de la línea de costa:

$$z^{2} = \frac{2\,q'\,x}{K\,G} + \left(\frac{q'}{K\,G}\right)^{2}$$

El **pie de la cuña** (*toe*) es el punto donde la interfaz alcanza la base del acuífero, $z = B$. Despejando:

$$\boxed{x_{toe} = \frac{K\,G\,B^{2}}{2\,q'} - \frac{q'}{2\,K\,G}}$$

con $KG = (3.3\times10^{-3})(0.025) = 8.25\times10^{-5}\ \mathrm{ft/s}$.

### Con el dato del enunciado, $q' = 2\times10^{-1}\ \mathrm{ft^3/s}$ por pie de costa

$$\frac{q'}{KG} = \frac{0.2}{8.25\times10^{-5}} = 2424\ \mathrm{ft}$$

Este término es la profundidad de la interfaz **en la propia línea de costa** ($x=0$): 2424 ft, es decir, **24 veces más que el espesor del acuífero (100 ft)**.

$$x_{toe} = \frac{(8.25\times10^{-5})(100)^2}{2(0.2)} - \frac{0.2}{2(8.25\times10^{-5})} = 2.06 - 1212 = -1210\ \mathrm{ft}$$

$$\boxed{x_{toe} < 0 \;\Longrightarrow\; \textbf{no existe cuña de agua salada}}$$

Con ese caudal de descarga la interfaz está muy por debajo de la base del acuífero ya en la costa: **el agua dulce expulsa por completo al agua de mar** y la cuña queda mar adentro. Verificación independiente del gradiente implicado:

$$i = \frac{q'}{KB} = \frac{0.2}{(3.3\times10^{-3})(100)} = 0.61\ \mathrm{m/m}$$

Un gradiente de 0.61 es físicamente inverosímil en un acuífero costero (los valores reales son $10^{-4}$–$10^{-3}$), lo que confirma que **el exponente del enunciado está mal transcrito**.

### Con el valor coherente $q' = 2\times10^{-4}\ \mathrm{ft^3/s}$ por pie de costa

$$\frac{q'}{KG} = \frac{2\times10^{-4}}{8.25\times10^{-5}} = 2.42\ \mathrm{ft}$$

$$x_{toe} = \frac{(8.25\times10^{-5})(10\,000)}{2(2\times10^{-4})} - \frac{2\times10^{-4}}{2(8.25\times10^{-5})} = 2062.5 - 1.2$$

$$\boxed{x_{toe} = 2.06\times10^{3}\ \mathrm{ft} \approx 2061\ \mathrm{ft} = 0.39\ \mathrm{mi}}$$

**Si el flujo hacia el mar se reduce a la mitad** ($q' = 1\times10^{-4}\ \mathrm{ft^3/s}$ por pie):

$$x_{toe} = \frac{(8.25\times10^{-5})(10\,000)}{2(1\times10^{-4})} - \frac{1\times10^{-4}}{2(8.25\times10^{-5})} = 4125 - 0.6$$

$$\boxed{x_{toe} = 4.12\times10^{3}\ \mathrm{ft} \approx 4124\ \mathrm{ft} = 0.78\ \mathrm{mi}}$$

**Conclusión.** Como el segundo término es despreciable cuando $q'$ es pequeño, domina la relación

$$x_{toe} \approx \frac{K\,G\,B^{2}}{2\,q'} \;\propto\; \frac{1}{q'}$$

de modo que **reducir a la mitad la descarga de agua dulce duplica la penetración de la cuña salina** (de 2061 a 4124 ft, +2063 ft tierra adentro). Es el resultado central del problema: la intrusión salina es inversamente proporcional al caudal de agua dulce que se deja fluir al mar, razón por la cual el sobrebombeo de acuíferos costeros desplaza la cuña de forma lineal en el inverso del caudal.

---

## Resumen de resultados

### Capítulo 3

| # | Resultado |
|---|---|
| 1 | $q = 1.9\times10^{-8}$ m/s |
| 2 | $v = 1.9\times10^{-7}$ m/s ($n_e=0.1$); $1.9\times10^{-4}$ m/s ($n_e=10^{-4}$) |
| 3 | Medio granular vs. roca fracturada |
| 4 | $[P/\rho g] = L$ |
| 5 | $[h]=L$ (energía/peso); $[\phi]=L^2/T^2$ (energía/masa) |
| 6 | $i = 0.141$ m/m, flujo hacia el S 45° W |
| 7 | $h$: 300 / 205 / 110 / 15 m; $h_p$: 200 / 190 / 50 / 8 m; $z$: 100 / 15 / 60 / 7 m |
| 8 | (a) $3.28\times10^{-6}$ ft/s (b) 2.12 gpd/ft² (c) $1.02\times10^{-9}$ cm² (d) 0.103 darcy |
| 9 | Flujo horizontal ($\partial z/\partial x = 0$), $\rho$ y $\mu$ constantes |
| 10 | Solo (a) es correcta; (d) invierte $q$ y $v$; b, c, e, f, g omiten el signo menos |
| 11 | $K_h = 3.70\times10^{-7}$ m/s; $K_v = 2.70\times10^{-8}$ m/s; $K_h/K_v = 13.7$ |
| 12 | $q_x = 1\times10^{-4}$ cm/s |
| 13 | (a) $K_3$ (b) $K_2$ (c) ≈ 3–4 veces |
| 14 | (a) equipotenciales se juntan (b) se separan |
| 15 | Mayor velocidad en $h_4$ (doble); flujo descendente en ambas |
| 16 | $q = 5\times10^{-8}$ cm/s, descendente |
| 17 | (a) $1\times10^{-4}$ m³/s cada uno (b) sup. $1.5\times10^{-4}$, inf. $5\times10^{-5}$ m³/s (c) $i$ = 0.15 y 0.05 m/m |

### Capítulo 4

| # | Resultado |
|---|---|
| 1 | (a) $\partial^2h/\partial x^2 = (S_s/K)\partial h/\partial t$ (b) $\nabla^2h = (\rho g\beta_p/K)\partial h/\partial t$ (c) $\nabla^2h=0$ (d) arcilla |
| 2 | (a) 300 m³ (b) $S = 8.48\times10^{-5}$ (c) $\beta_p = 3.66\times10^{-10}$ m²/N |
| 3 | (a) caudal de bombeo $Q$ (b) volumen total extraído $Qt$ |
| 4 | (a) 6250 / 4368 / 1882 lb/ft² (b) 4998 / 4368 / 630 lb/ft² (c) No, $FS=0.86$ (d) ≈ 30.1 ft |
| 5 | $T = Q/(n_f\Delta h) \approx 1.2\times10^{3}$ m²/día |
| 6 | AB y DE: equipotenciales, carga constante. BC, CD y FG: líneas de flujo, sin flujo |
| 7 | $Q = KH\,n_f/n_d$: $3.33\times10^{-3}$ / $4.17\times10^{-3}$ / $5.56\times10^{-3}$ m³/s·m |
| 8–9 | Redes de flujo (ver esquemas y reglas) |
| 10 | Sección transformada: $x' = 0.447x$; $K_{eq} = \sqrt{K_hK_v} = 2.24K_v$; celdas 2.24:1 |

### Capítulo 5

| # | Resultado |
|---|---|
| 1 | 5.5: tres fronteras sin flujo + nivel freático $h=f(x)$. 5.8 añade continuidad de $\phi$ y de $K\partial\phi/\partial z$ en las interfaces (medio estratificado) |
| 2 | Pérdida de simetría y refuerzo del flujo regional (5.4); dominio de celdas locales (5.27) |
| 3 | (a) $h_{canal}=0$ siempre; $h_{divisoria}$ = 12.00 / 12.00 / 11.86 / 10.67 m a 10 / 20 / 40 / 100 años (b) $q' = 1.25\times10^{-2}$ y $3.96\times10^{-3}$ m³/día·m |
| 4 | $FS = \sigma_T/u$; $d_{crit} = (\gamma_{sat}D-\gamma_w h_p)/(\gamma_{sat}-\gamma_w)$ |
| 5 | $Q_{max} = 0.6\pi K d^2 G = 7.0\times10^{-3}$ m³/s = 7 L/s = 111 gpm |
| 6 | Con $q'=2\times10^{-4}$: $x_{toe} = 2061$ ft; con la mitad del caudal, 4124 ft (se duplica). Con el $2\times10^{-1}$ del enunciado no existe cuña |

---

## Advertencias sobre datos que dependen de las figuras del libro

Estos tres puntos **no se pueden cerrar numéricamente sin medir sobre las figuras de tu edición**. En todos ellos la fórmula y el criterio están completos; solo falta sustituir tu lectura:

1. **Cap. 3, problema 13** — $K_i \propto L_i/A_i$. Hay que escalar con regla $L_1,L_2,L_3$ y $b_1,\dots,b_4$ en la figura 3.E4.
2. **Cap. 4, problema 5** — $T = Q/(n_f\Delta h)$. Hay que contar los tubos de flujo que convergen en el centro de bombeo B en la figura 4.10.
3. **Cap. 4, problema 7** — $Q = KH\,n_f/n_d$. Los conteos dependen de tu propio trazado; lo evaluable es que $n_d$ disminuya al acortar el delantal.

Adicionalmente, el **Cap. 5, problema 4** remite a los datos del caso histórico de las páginas 99–101, que aquí se sustituyeron por el conjunto equivalente del Cap. 4, problema 4.

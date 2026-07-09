# Simulacro de Parcial – Diseño Estructural

> Practica primero **sin mirar las respuestas**. Las soluciones están al final de cada bloque.
> Mezcla preguntas conceptuales (teoría) y problemas (cálculo).

---

## BLOQUE A – Columnas (concepto)

**A1.** ¿Cuál es la diferencia fundamental entre una columna **corta** y una **esbelta**?

**A2.** Escribe la fórmula de la resistencia a compresión pura `Po` e indica qué representa cada término.

**A3.** ¿Por qué el código multiplica `Po` por 0.80 (estribos) o 0.85 (espiral)?

**A4.** En el diagrama de interacción, ¿qué separa el **punto balanceado**?

**A5.** ¿Cuándo uso la fórmula de **Bresler** y cuál es su limitación?

**A6.** ¿Qué diferencia hay entre el efecto **P-Δ** y el efecto **P-δ**?

<details><summary>✅ Respuestas A</summary>

- **A1.** La corta falla por resistencia del material (aplastamiento/fluencia); la esbelta falla
  por efectos de segundo orden (pandeo, momentos P-Δ y P-δ amplificados).
- **A2.** `Po = 0.85f'c(Ag−Ast) + fy·Ast`. Primer término: aporte del concreto sobre el área neta;
  segundo: aporte del acero longitudinal en fluencia.
- **A3.** Para considerar la **excentricidad accidental mínima** (nunca hay compresión perfectamente
  axial) y dar seguridad adicional.
- **A4.** Separa la zona de **falla por compresión** (arriba, el acero a tracción no fluye) de la
  de **falla por tracción** (abajo, el acero fluye primero). Es el punto de máximo momento.
- **A5.** Para **flexión biaxial** (Mx y My simultáneos): `1/Pn = 1/Pnx + 1/Pny − 1/Po`.
  No es válida cuando φPnx y φPny son menores que φPb (zona de tracción).
- **A6.** **P-Δ:** efecto global por desplazamiento lateral de piso (estructuras no arriostradas).
  **P-δ:** efecto local sobre el eje deformado del propio miembro (estructuras arriostradas).
</details>

---

## BLOQUE B – Columnas (cálculo)

**B1.** Columna **400×400 mm**, 8#7, `f'c=28 MPa`, `fy=420 MPa`. Halla `Po` y `φPn,max` (estribos).

**B2.** Una columna arriostrada tiene `k=0.85`, `Lu=3.2 m`, sección 0.35×0.50 (flexión en h=0.50),
`M1/M2 = +0.4`. ¿Es corta o esbelta?

<details><summary>✅ Respuestas B</summary>

- **B1.** `Ast = 8(387) = 3096 mm²`; `Ag = 160 000 mm²`.
  `Po = 0.85(28)(160000−3096) + 420(3096) = 23.8(156904) + 1 300 320 = 3 734 315 + 1 300 320 =
  5 034 635 N ≈ 5035 kN`.
  `φPn,max = 0.80(0.65)(5035) = 2618 kN`.
- **B2.** `r = 0.3(0.50) = 0.15 m`; `kLu/r = 0.85(3.2)/0.15 = 18.1`.
  Límite (arriostrada): `34 − 12(0.4) = 29.2` (≤40). Como `18.1 < 29.2` → **columna corta**.
</details>

---

## BLOQUE C – Provisiones sísmicas (C.21)

**C1.** Dimensión mínima de columna en **DMO** y en **DES**.

**C2.** ¿Entre qué valores debe estar la cuantía de refuerzo longitudinal `Ast`?

**C3.** Enuncia el principio de **columna fuerte – viga débil** y su ecuación.

**C4.** En DMO, ¿cuáles son los 4 límites para la separación `s₀` del confinamiento?

<details><summary>✅ Respuestas C</summary>

- **C1.** DMO: ≥ **250 mm**; DES: ≥ **300 mm**.
- **C2.** `0.01 Ag ≤ Ast ≤ 0.04 Ag` (entre 1 % y 4 %).
- **C3.** En cada nudo `ΣMnc ≥ 1.2 ΣMnb` (las columnas más fuertes que las vigas) para que las
  rótulas plásticas se formen en las vigas y no se desplome el piso.
- **C4.** `s₀ ≤` menor de: 8·db(long.), 16·db(estribo), ⅓ de la dimensión menor, y 150 mm.
</details>

---

## BLOQUE D – Escaleras

**D1.** ¿Como qué elemento estructural se modela una escalera de un tramo?

**D2.** Regla de comodidad de huella/contrahuella (Título K).

**D3.** Escalera de un tramo, luz `L = 3.6 m`, `e = L/20`, `wu = 14 kN/m` (por metro de ancho).
Halla `Mu` y `Vu` (apoyo simple).

<details><summary>✅ Respuestas D</summary>

- **D1.** Como una **losa maciza unidireccional** apoyada en sus extremos.
- **D2.** `600 mm ≤ 2·(contrahuella) + 1·(huella) ≤ 640 mm`. Huella ≥ 280 mm; contrahuella 100–180 mm.
- **D3.** `Mu = wuL²/8 = 14(3.6²)/8 = 22.7 kN·m`; `Vu = wuL/2 = 14(3.6)/2 = 25.2 kN`.
  (Espesor `e = 3.6/20 = 0.18 m`.)
</details>

---

## BLOQUE E – Zapatas

**E1.** ¿Qué cargas se usan para **dimensionar** y cuáles para **diseñar** una zapata?

**E2.** ¿Dónde está la sección crítica para (a) flexión, (b) cortante como viga, (c) punzonamiento?

**E3.** Zapata cuadrada, columna 0.50×0.50, `PD=900 kN`, `PL=300 kN`, `σadm=200 kN/m²`.
Halla el lado **B** y la presión de diseño `qu`.

**E4.** Para la misma zapata, si `B=2.50 m` y el voladizo es 1.0 m, halla `Mu` en la cara de la
columna (usa el `qu` de E3).

<details><summary>✅ Respuestas E</summary>

- **E1.** Dimensionar: **cargas de servicio** (sin mayorar) + `σadm`. Diseñar: **cargas mayoradas**
  → presión de diseño `qu = Pu/A`.
- **E2.** (a) Flexión: en la **cara de la columna**. (b) Cortante viga: a **`d`** de la cara.
  (c) Punzonamiento: a **`d/2`** de la cara (perímetro `bo`).
- **E3.** `P_serv = 1200 kN` → `A = 1200/200 = 6.0 m²` → `B = 2.45 m` (usar 2.50, A=6.25).
  `Pu = 1.2(900)+1.6(300) = 1080+480 = 1560 kN`; `qu = 1560/6.25 = 249.6 kN/m²`.
- **E4.** `Mu = qu·B·Lvol²/2 = 249.6(2.50)(1.0²/2) = 312 kN·m`.
</details>

---

## BLOQUE F – Vigas de amarre

**F1.** Menciona 3 funciones de una viga de amarre.

**F2.** Fórmula de la fuerza de **amarre sísmico**.

**F3.** Viga de amarre que conecta columnas de 3000 kN y 4500 kN, `Aa=0.20`.
Halla la fuerza de amarre y el acero requerido (`fy=420`, φ=0.90).

<details><summary>✅ Respuestas F</summary>

- **F1.** (cualquiera 3): contrapeso de zapatas excéntricas; amarre sísmico; control de
  asentamientos diferenciales; reacción del terreno; soportar cargas directas (escaleras/rampas);
  tomar momentos de empotramiento de columnas.
- **F2.** `T = 0.25·Aa·(carga del elemento más cargado)`.
- **F3.** `T = 0.25(0.20)(4500) = 225 kN`. `As = T/(φfy) = 225000/(0.9·420) = 595 mm²`
  → con 2#7 (774 mm²) sobra; gobiernan los mínimos de sección de C.15.13.
</details>

---

## Consejos finales para el parcial
- Lleva **claras las fórmulas** del [formulario](GUIA-PARCIAL.md#6-formulario-rapido).
- En zapatas, **siempre** separa servicio (dimensionar) de mayorado (diseñar).
- En columnas, no olvides el **tope φPn,max** y el cambio de **φ** (0.65 ↔ 0.90).
- En sísmica (C.21), memoriza dimensiones mínimas, cuantías y "columna fuerte–viga débil".
- Revisa **unidades**: trabaja en N y mm (MPa) o en kN y m de forma consistente.

¡Éxitos! 💪

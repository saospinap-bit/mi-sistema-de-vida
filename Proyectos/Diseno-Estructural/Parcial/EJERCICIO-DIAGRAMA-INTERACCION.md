# Ejercicio resuelto: Diagrama de interacción completo (Columna 500 × 400)

> Solución numérica completa del ejercicio de la presentación 13-COLUMNAS (diapositiva 23).
> `f'c = 21 MPa`, `fy = 420 MPa`, `Es = 200 000 MPa`, `β1 = 0.85`.

## 1. Definición de la sección

Sección **b = 400 mm**, **h = 500 mm** (la flexión se evalúa en el plano de h).
Refuerzo: **3#8 + 3#8** en las caras superior/inferior **+ 4#7** repartidas en las caras de 500 mm.

Como h = 500 mm es alta, las 4#7 forman **2 capas intermedias** (2 barras cada una). Quedan
**4 capas de acero**. Tomando recubrimiento al centroide de la barra ≈ **62 mm**:

| Capa | Barras | As (mm²) | dᵢ desde fibra sup. (mm) |
|------|--------|----------|--------------------------|
| 1 (comp.) | 3#8 | 1530 | 62 |
| 2 | 2#7 | 774 | 187 |
| 3 | 2#7 | 774 | 313 |
| 4 (tracc.) | 3#8 | 1530 | 438 |

`Ast = 1530+774+774+1530 = 4608 mm²` ✔ | `Ag = 200 000 mm²` | `ρ = 2.3 %`

## 2. Ecuaciones de equilibrio (para cada profundidad de eje neutro c)

- `a = β1·c = 0.85 c`
- Concreto: `Cc = 0.85 f'c · a · b = 0.85(21)(a)(400) = 7140·a` (N), aplicado a `a/2` de la fibra sup.
- Cada capa: `εsᵢ = 0.003 (c − dᵢ)/c` (compresión +)
  - `fsᵢ = Es·εsᵢ`, limitado a ±fy (±420)
  - `Fsᵢ = Asᵢ·fsᵢ`; a las **barras en compresión** se les resta el concreto desplazado `0.85f'c·Asᵢ`
- `Pn = Cc + ΣFsᵢ`
- `Mn = Cc(h/2 − a/2) + ΣFsᵢ(h/2 − dᵢ)` (momentos respecto al centroide, h/2 = 250 mm)

## 3. Puntos calculados

### (A) Compresión pura
`Po = 0.85f'c(Ag−Ast) + fy·Ast = 5423 kN`, `M = 0`.
**Tope de diseño** (estribos): `φPn,max = 0.80(0.65)(5423) = 2820 kN`.

### (B) c = 350 mm (zona de falla por compresión)
`a = 297.5 mm`, `Cc = 2124 kN`.

| Capa | εsᵢ | fsᵢ (MPa) | Fsᵢ (kN) |
|------|-----|-----------|----------|
| 1 | +0.00247 | +420 | +615 |
| 2 | +0.00140 | +279 | +202 |
| 3 | +0.00032 | +64  | +36  |
| 4 | −0.00075 | −151 | −231 |

`Pn = 2124+615+202+36−231 = 2746 kN` | `Mn ≈ 385 kN·m` | φ = 0.65 (controlada por compresión)
→ **φPn ≈ 1785 kN, φMn ≈ 250 kN·m**

### (C) Punto BALANCEADO  (el acero a tracción fluye al tiempo que ε_c = 0.003)
`c_b = 0.003/(0.003+εy)·d = 0.003/0.0051 · 438 = 257.6 mm`, `a = 219 mm`, `Cc = 1564 kN`.

| Capa | εsᵢ | fsᵢ (MPa) | Fsᵢ (kN) |
|------|-----|-----------|----------|
| 1 | +0.00228 | +420 | +615 |
| 2 | +0.00082 | +164 | +113 |
| 3 | −0.00064 | −128 | −99  |
| 4 | −0.00210 | −420 | −643 |

`Pb = 1564+615+113−99−643 = 1550 kN` | `Mb ≈ 470 kN·m` (máximo momento) | φ = 0.65
→ **φPb ≈ 1007 kN, φMb ≈ 305 kN·m**

### (D) Flexión pura  (P = 0)
Iterando se obtiene `c ≈ 125.5 mm`, `a = 106 mm`, `Cc = 759 kN`.

| Capa | εsᵢ | fsᵢ (MPa) | Fsᵢ (kN) |
|------|-----|-----------|----------|
| 1 | +0.00151 | +302 | +435 |
| 2 | −0.00150 | −299 | −231 |
| 3 | −0.00449 | −420 | −325 |
| 4 | −0.00747 | −420 | −643 |

`Pn = 759+435−231−325−643 ≈ 0` ✔ | `Mn ≈ 358 kN·m`
`εt = 0.0075 > 0.005` → tracción controlada, **φ = 0.90** → **φMn ≈ 322 kN·m**

### (E) Tracción pura
`Tn = Ast·fy = 4608(420) = 1935 kN`, `M = 0`. φ = 0.90 → **φTn ≈ 1742 kN**

## 4. Resumen del diagrama

| Punto | Pn (kN) | Mn (kN·m) | φ | φPn (kN) | φMn (kN·m) |
|-------|---------|-----------|------|----------|------------|
| A Compresión pura | 5423 | 0 | 0.65 | 2820 (tope) | 0 |
| B c=350 | 2746 | 385 | 0.65 | 1785 | 250 |
| C Balanceado | 1550 | 470 | 0.65 | 1007 | 305 |
| D Flexión pura | 0 | 358 | 0.90 | 0 | 322 |
| E Tracción pura | −1935 | 0 | 0.90 | −1742 | 0 |

**Forma del diagrama** (φPn en el eje vertical vs φMn en el horizontal):

```
 φPn (kN)
 2820 |■■■■■■  ← tope plano φPn,max (estribos)
      |      \
 1785 |        ● B (250, 1785)
      |          \
 1007 |            ● C balanceado (305, 1007)   ← punto de máximo momento
      |           /
    0 |________●_________________ φMn (kN·m)
      |     D (322, 0)
-1742 |  ● E tracción pura
```

- **Por encima del balanceado (C):** falla por **compresión** (φ = 0.65).
- **Por debajo del balanceado:** falla por **tracción**; φ sube de 0.65 a 0.90 en la transición
  (entre εt = 0.0021 y 0.005).
- Toda combinación **(Pu, Mu)** que caiga **dentro** de la curva es segura; si cae **fuera**, falla.

## 5. Cómo usarlo en el parcial
1. Calcula los puntos A, C y D (son los obligatorios) y, si piden más detalle, B y un punto en
   la transición.
2. Recuerda aplicar el **tope** `φPn,max` (línea horizontal) y el cambio de **φ** según εt.
3. Para verificar una columna: ubica el par `(Mu, Pu)` mayorado y comprueba que quede dentro.

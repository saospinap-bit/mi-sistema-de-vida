# PLAN DE ESTUDIO — TERCER PARCIAL (Diseño Estructural)
### Videos + ejercicios + horario del día completo · Meta: **5.0**

---

## A. VIDEOS POR TEMA

> Consejo: en YouTube pega la búsqueda tal cual, ordena por relevancia y elige videos con muchas
> vistas y buenos comentarios (idealmente basados en ACI 318 / NSR-10). Canales latinos confiables
> para concreto reforzado: **Genner Villarreal**, **Ingeniería Fácil**, **SkyCiv** (diagramas de
> interacción), **412 Estructuras / canales de estructuras NSR-10**. Verifica siempre la norma.

**1. Columnas cortas — capacidad axial y flexocompresión**
- `columna corta concreto reforzado carga axial fluencia ejemplo`
- `flexocompresión columna concreto reforzado explicación`

**2. Diagrama de interacción P–M**
- `diagrama de interacción columna concreto reforzado ejercicio resuelto`
- `interaction diagram column ACI 318 balanced point example`
- `punto balanceado columna compresión tracción pura diagrama`

**3. Esbeltez y magnificación de momentos (2° orden)**
- `esbeltez columna concreto klu/r ejemplo`
- `magnificación de momentos delta ns Cm carga crítica Euler ACI`
- `momento magnificado columna esbelta ejercicio resuelto`

**4. Provisiones sísmicas de columnas (NSR-10 C.21 / ACI 318 Cap. 18)**
- `confinamiento columnas NSR-10 estribos Ash s0 l0`
- `columna fuerte viga débil ACI 318 nudo`
- `cortante por capacidad columna Mpr diseño sísmico`

**5. Zapatas (cuadrada, rectangular, con momento)**
- `diseño zapata aislada concreto punzonamiento cortante flexión ejemplo`
- `zapata con carga axial y momento excentricidad presión trapezoidal ejercicio`
- `zapata rectangular concreto reforzado diseño refuerzo banda central`

**6. Escaleras**
- `diseño escalera concreto reforzado losa maciza ejemplo`
- `carga muerta viva escalera tramo inclinado descanso diseño`

**7. Vigas de amarre / riostras**
- `viga de amarre cimentación NSR-10 amarre sísmico refuerzo`
- `viga riostra diseño concreto 0.25 Aa`

---

## B. EJERCICIOS DE INTERNET (enlaces reales)

- Zapata aislada — solucionario de examen (udocz):
  https://www.udocz.com/apuntes/128586/solucionario-de-examen-parcial-de-zapata-aislada
- Hoja Excel — diagramas de interacción de columnas (udocz):
  https://www.udocz.com/apuntes/171189/hoja-excel-de-calculo-de-diagramas-de-interaccion-de-columnas
- Chequeo de columna con P y M — ejemplo (Scribd):
  https://www.scribd.com/document/482315882/columna-25-x-30-pdf
- Ejercicios resueltos de diseño de zapatas (Scribd):
  https://www.scribd.com/document/434889011/Ejercicios-Resueltos-de-Disenos-de-Zapatas
- Zapatas aisladas con carga axial y momentos — artículo académico (Redalyc):
  https://www.redalyc.org/journal/496/49645153020/html/
- SkyCiv — qué es una curva de interacción de columna (teoría, inglés):
  https://skyciv.com/docs/tutorials/reinforced-concrete-tutorials/what-is-a-column-interaction-curve/

*Nota: parte del contenido fue reformulado; consulta siempre la fuente original.*

---

## C. EJERCICIOS DE PRÁCTICA (con respuesta — tápalas y resuélvelos tú)

**P1. Capacidad axial.** Columna 400×400, 8#7, f'c=28, fy=420. Halla Po y φPn,máx (estribos).
> **R:** Ast=3096 mm²; Po=**5035 kN**; φPn,máx=0.65·0.80·Po=**2618 kN**

**P2. Zapata cuadrada.** Col 0.45×0.45, PD=900, PL=350, σadm=200. Dimensiona y halla qu.
> **R:** A=6.25 m² → B=**2.5 m**; Pu=1640 kN; qu=**262 kPa** (luego revisa punzonamiento para h)

**P3. Esbeltez.** Col 40×40, lu=3.6 m, k=1.0 (arriostrada), r=0.3h. ¿Es esbelta si M1/M2=0?
> **R:** r=0.12; klu/r=**30.0**; límite=34−12(0)=34 → **30<34: NO esbelta (corta)**

**P4. Magnificación.** Pu=1200 kN, Pc=6000 kN, Cm=0.85. Halla δns.
> **R:** δns=0.85/(1−1200/(0.75·6000))=**1.16** → Mc=1.16·M2

**P5. Zapata con momento.** P=800, M=120, B=2.4, L=2.8. e, ¿trapezoidal?, qmáx/qmín.
> **R:** e=**0.15 m** ≤ L/6=0.467 → trapezoidal; qmáx=**157.3**, qmín=**80.8 kPa**

**P6. Viga de amarre.** Aa=0.25, carga mayor=6000 kN, fy=420. T y As.
> **R:** T=0.25·0.25·6000=**375 kN**; As=T/(0.9·fy)=**992 mm²** (≈ 2#8+... o 5#5)

**P7. Escalera.** Luz L=3.5 m. Predimensiona el espesor.
> **R:** e=L/20=0.175 → adopta **e=0.18–0.20 m**

---

## D. HORARIO DEL DÍA COMPLETO (tu día dedicado antes del parcial)

| Hora | Bloque | Qué hacer |
|------|--------|-----------|
| 7:00–7:30 | ☕ Arranque | Desayuno + repasar el FORMULARIO del solucionario (visión global) |
| 7:30–9:00 | **Columnas 1** | Ver video interacción + rehacer Ejemplo 1 y 2 del solucionario SIN mirar |
| 9:00–9:15 | Descanso | Estírate, agua |
| 9:15–10:45 | **Columnas 2 (esbeltez)** | Video magnificación + Punto 3 del Taller + P3 y P4 de práctica |
| 10:45–11:00 | Descanso | |
| 11:00–12:30 | **Provisiones sísmicas** | Confinamiento (so, ℓo, Ash), columna fuerte-viga débil, cortante capacidad |
| 12:30–13:30 | 🍽️ Almuerzo | Desconexión real |
| 13:30–15:00 | **Zapatas** | Cuadrada + rectangular + con momento (Punto 1 del Taller) + P2 y P5 |
| 15:00–15:15 | Descanso | |
| 15:15–16:15 | **Escaleras + vigas de amarre** | Método + P6 y P7 de práctica |
| 16:15–16:30 | Descanso | |
| 16:30–18:00 | **Simulacro** | Rehacer el TALLER 3 completo cronometrado, como si fuera el parcial |
| 18:00–19:00 | 🍽️ Cena | |
| 19:00–20:30 | **Repaso de errores** | Corrige lo que fallaste en el simulacro; relee solo esos temas |
| 20:30–21:00 | Cierre | Repaso rápido del formulario + prepara calculadora, lápiz, tablas NSR-10 |
| 21:00 | 😴 A dormir | Descansar es parte de estudiar. Nada nuevo a esta hora |

**Reglas de oro del día**
1. **Resuelve con lápiz, no solo leas.** Se aprende haciendo, no viendo.
2. Técnica **Pomodoro**: ~50 min enfocado + 10 de descanso.
3. Prioriza por peso: **Columnas + Zapatas** suelen valer más → dales las mejores horas.
4. Ten a mano: formulario, tablas de áreas de barras, Fa/Fv (suelo), factores φ.
5. Lleva **el formulario resumen** ya interiorizado (Po, balanceado, klu/r, δns, qmáx/mín, Ash).

**Checklist para el parcial ✅**
- [ ] Sé calcular Po, Pn,máx y φPn,máx
- [ ] Sé ubicar compresión pura, balanceado, flexión pura y tracción pura en el diagrama
- [ ] Sé calcular klu/r y decidir si es esbelta (límites 22 / 34−12M1/M2)
- [ ] Sé calcular Cm, Pc y δns → Mc
- [ ] Sé dimensionar zapata (servicio) y revisar punzonamiento (mayorado)
- [ ] Sé zapata con momento: e≤L/6, qmáx≤qadm, qmín≥0
- [ ] Sé confinamiento: so, ℓo, Ash y columna fuerte-viga débil
- [ ] Sé el amarre sísmico: T=0.25·Aa·P

**¡Tú puedes con ese 5! 💪**

# Cómo se calculó todo — Metodología del Proyecto PEPI

Este documento explica, paso a paso, cómo se construyó cada parte del informe para que puedas **sustentarlo y defenderlo** o **adaptarlo** a otro proyecto.

> Proyecto desarrollado: **Construcción de PTAP (120 L/s) + ampliación del sistema de acueducto** del municipio de El Progreso. Es un proyecto de ejemplo coherente con la guía del PDF (que solo lista entregables, no un caso concreto).

---

## 1. Punto de partida: la guía del PDF

El archivo `PROYECTO PEPI.pdf` (en la raíz de la carpeta) **no es un enunciado**, sino una **lista de entregables**. Pide 8 componentes:

1. Resumen ejecutivo (máx. 1 página)
2. Árbol de problemas (1 gráfica)
3. Árbol de objetivos (1 gráfica)
4. Matriz de Marco Lógico (MML) — 4 filas y 4 columnas
5. Solución de ingeniería (máx. 1 página)
6. Análisis financiero: CAPEX/OPEX, Deuda+Equity, WACC, TIR, VPN, flujos (proyecto, banco, inversionista)
7. Matriz de 20 riesgos calificados
8. Intervención de 10 riesgos (5 ambientales) + recalificación

Informe máximo de 10 páginas.

---

## 2. Las secciones cualitativas (1 a 5, 7 y 8)

Estas se redactaron a partir de un **caso realista de acueducto**:

- **Árbol de problemas/objetivos:** se parte de un problema central ("deficiente prestación del servicio de acueducto") y se derivan **causas** (PTAP obsoleta, pérdidas IANC 48 %, redes viejas) y **consecuencias** (enfermedades, sobrecostos). El árbol de objetivos es el "espejo en positivo" del de problemas (cada causa → un medio, cada consecuencia → un fin).
- **MML:** se llenó la matriz 4×4 (Fin, Propósito, Componentes, Actividades) × (Resumen, Indicadores, Medios de verificación, Supuestos). Los indicadores son los típicos del sector agua: cobertura, continuidad, IRCA (calidad), IANC (pérdidas).
- **Riesgos:** se listaron 20 riesgos reales del sector (financieros, ambientales, operativos, sociales). Cada uno se califica con **Probabilidad (P) × Impacto (I)**, ambos de 1 a 5. El producto P×I da el nivel: Bajo (1–6), Medio (8–12), Alto (15–25).
- **Intervención:** se eligieron los 10 más críticos (asegurando que 5 fueran ambientales) y se definió una medida de control para cada uno, recalificando el riesgo **residual** (la P y/o la I bajan tras aplicar la medida).

---

## 3. El análisis financiero (el corazón numérico)

Aquí está la parte importante: **nada se inventó "a mano"**. Todo se calculó con el script `modelo_financiero.py`, lo que garantiza que WACC, TIR, VPN y los tres flujos sean **matemáticamente consistentes** entre sí.

### 3.1 Supuestos de entrada (los que puedes cambiar)

| Variable | Valor usado | Significado |
|---|---|---|
| `CAPEX` | 14.000 (COP MM) | Inversión total inicial |
| `PCT_DEUDA` / `PCT_EQUITY` | 60 % / 40 % | Estructura de financiación |
| `KD` | 12,5 % | Costo de la deuda (interés del crédito) |
| `KE` | 15,5 % | Costo del equity (rentabilidad exigida por el inversionista) |
| `TASA_IMPUESTOS` | 35 % | Impuesto de renta |
| `PLAZO_DEUDA` | 10 años | Años para pagar el crédito |
| `INGRESO_ANIO1` | 5.200 | Ingreso por tarifa el primer año |
| `OPEX_ANIO1` | 2.350 | Costo de operación el primer año |
| `HORIZONTE` | 20 años | Periodo de evaluación |

### 3.2 WACC (Costo Promedio Ponderado de Capital)

Fórmula:

> **WACC = (E/V)·Ke + (D/V)·Kd·(1 − t)**

Reemplazando:

> WACC = (0,40 × 0,155) + (0,60 × 0,125 × (1 − 0,35)) = 0,0620 + 0,04875 = **11,07 %**

El `(1 − t)` aplica el **escudo fiscal**: los intereses de la deuda son deducibles de impuestos, por eso la deuda "cuesta menos" en términos netos.

### 3.3 Tabla de amortización de la deuda

La deuda (8.400) se paga con **cuota fija (sistema francés)** durante 10 años. La cuota se calcula con:

> Cuota = P · i / (1 − (1 + i)^(−n)) = 8.400 × 0,125 / (1 − 1,125^(−10)) = **1.517,2 COP MM/año**

Cada año, parte de la cuota es **interés** (decreciente) y parte es **abono a capital** (creciente). Esto alimenta los flujos.

### 3.4 Los tres flujos de caja

- **Flujo del Proyecto (FCLP):** mide la rentabilidad de la inversión *sin importar cómo se financie*.
  `FCLP = EBIT × (1 − t) + Depreciación`. Se descuenta al **WACC**.
- **Flujo del Inversionista (FCLA):** lo que le queda al dueño del equity *después* de pagarle al banco.
  `FCLA = Utilidad neta + Depreciación − Abono a capital`. Se descuenta al **Ke**.
- **Flujo del Banco:** entrega 8.400 en el año 0 y recibe la cuota fija 10 años. Su rentabilidad es el Kd (12,5 %).

### 3.5 VPN y TIR

- **VPN (Valor Presente Neto):** se traen todos los flujos futuros a "hoy" con la tasa de descuento y se restan de la inversión. Si VPN > 0, el proyecto crea valor.
- **TIR (Tasa Interna de Retorno):** es la tasa que hace VPN = 0. En el script se calcula por **bisección** (un método numérico robusto). Si TIR > tasa de descuento, el proyecto es viable.

---

## 4. Resultados obtenidos

| Indicador | Valor | Lectura |
|---|---|---|
| **WACC** | 11,07 % | Costo de financiar el proyecto |
| **VPN proyecto** | COP 8.376 MM | > 0 → crea valor |
| **TIR proyecto** | 18,13 % | > WACC (11,07 %) → viable |
| **VPN inversionista** | COP 4.698 MM | > 0 → atractivo para el dueño |
| **TIR inversionista** | 24,78 % | > Ke (15,5 %) → viable |

**Conclusión financiera:** el proyecto es viable por ambas ópticas, y el apalancamiento (usar deuda) sube la rentabilidad del inversionista del 18,13 % al 24,78 %.

---

## 5. Cómo recalcular todo si cambias los supuestos

1. Abre `modelo_financiero.py` y edita los valores de la sección de parámetros (CAPEX, tasas, ingresos, etc.).
2. Ejecuta:
   ```bash
   python3 modelo_financiero.py
   ```
   Esto imprime los nuevos indicadores y regenera `resultados_modelo.csv`.
3. Actualiza los números en `INFORME_PEPI.md` y, si quieres el Word nuevo:
   ```bash
   python3 generar_word.py
   ```

Así, si tu profesor pide otros valores o un proyecto distinto, solo cambias las entradas y todo se recalcula solo.

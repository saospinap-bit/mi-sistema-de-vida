# Cómo se calculó todo — Metodología del Proyecto PEPI (Acueducto de Tadó, Chocó)

Este documento explica, paso a paso, cómo se construyó cada parte del informe para que puedas **sustentarlo y defenderlo** o **adaptarlo**.

> Proyecto desarrollado: **Optimización y ampliación del sistema de acueducto del municipio de Tadó (Chocó)**, con una **PTAP de 45 L/s**. Es un **caso real**: se usan datos verificables de Tadó (DANE, río San Juan, clima, proyecto real de MinVivienda). Los parámetros sin fuente oficial específica (desglose del presupuesto, tarifas, IANC, beneficios sociales) son **estimaciones razonables** señaladas.

---

## 1. Punto de partida: la guía del PDF

El archivo `PROYECTO PEPI.pdf` (en la carpeta de arriba) **no es un enunciado**, sino una **lista de entregables**: resumen ejecutivo, árbol de problemas, árbol de objetivos, MML, solución de ingeniería, análisis financiero (CAPEX/OPEX, Deuda+Equity, WACC, TIR, VPN, flujos), matriz de 20 riesgos e intervención de 10 (5 ambientales). Sobre esa estructura se desarrolló el caso de Tadó.

---

## 2. Por qué Tadó y qué datos son reales

| Dato | ¿Real? | Fuente |
|---|---|---|
| Municipio de Tadó (Chocó), sobre el río San Juan | ✅ Real | DANE / Wikipedia |
| Población 17.000 hab (CNPV 2018) | ✅ Real | DANE |
| Lluvia ~7.921 mm/año (de las más altas del planeta) | ✅ Real | Wikipedia (datos climáticos) |
| Proyecto real de acueducto: COP 19.971 MM, meta 24 h y 98 % cobertura | ✅ Real | Agencia Anadolu (MinVivienda + cooperación española) |
| Presencia de grupos armados en la región | ✅ Real | El Ciudadano |
| Desglose del presupuesto por capítulos | ⚠️ Estimado | Coherente con el total real |
| Tarifas, IANC, beneficios sociales | ⚠️ Estimado | Valores típicos del sector |

La **paradoja** que estructura el problema es real y poderosa: Tadó es uno de los lugares más lluviosos del mundo, pero su población ha carecido de agua **potable** continua.

---

## 3. Las secciones cualitativas (árboles, MML, riesgos)

- **Árbol de problemas/objetivos:** el problema central es "servicio de acueducto deficiente, discontinuo y con agua no apta". Las **causas** (PTAP insuficiente, alta turbiedad del agua cruda, redes deterioradas, baja cobertura) y los **efectos** (EDA, gasto en agua embotellada, freno económico) se dibujan como **esquema visual de árbol** (cajas conectadas), no como listas. El árbol de objetivos es el "espejo positivo".
- **MML:** matriz 4×4 (Fin, Propósito, Componentes, Actividades) × (Resumen, Indicadores, Medios de verificación, Supuestos). Indicadores del sector agua: cobertura, continuidad, IRCA (calidad), IANC (pérdidas).
- **Riesgos:** 20 riesgos calificados con **P × I** (1 a 5). Nivel: Bajo (1–6), Medio (8–12), Alto (15–25). Los más críticos en Tadó son **ambientales** (turbiedad del río, minería ilegal con mercurio, inundaciones) y de **seguridad** e **institucionales** (desembolsos).
- **Intervención:** 10 riesgos prioritarios (5 ambientales) con su medida de control y **recalificación residual**.

---

## 4. Diseño de caudal (Resolución 0330 de 2017 — RAS)

Esta es la parte de **ingeniería** que sustenta el tamaño de la PTAP. Se calcula en `modelo_financiero.py` (sección A) y se reproduce en la hoja **"Diseno de Caudal"** del Excel.

| Paso | Cálculo | Resultado |
|---|---|---|
| Población de diseño (geométrico, 25 años) | 10.957 · (1,012)^25 | **14.764 hab** |
| Dotación neta (clima cálido < 1.000 m, Art. 43) | — | **140 L/hab·día** |
| Dotación bruta (pérdidas 25 %, Art. 44) | 140 / (1 − 0,25) | **186,7 L/hab·día** |
| Caudal medio diario (Qmd) | Pob · Dot.bruta / 86.400 | **31,9 L/s** |
| Caudal máximo diario (QMD), k1 = 1,30 | Qmd · 1,30 | **41,5 L/s** |
| Caudal máximo horario (QMH), k2 = 1,60 | QMD · 1,60 | **66,4 L/s** |
| **Capacidad PTAP** | se diseña para el QMD | **45 L/s** |

---

## 5. El análisis financiero (el corazón numérico)

Todo se calcula con `modelo_financiero.py`, y el Excel `MODELO FINANCIERO PEPI.xlsx` lo replica con **fórmulas vivas** (se verificó que dan exactamente lo mismo).

### 5.1 Supuestos de entrada (los que puedes cambiar)

| Variable | Valor | Significado |
|---|---|---|
| `CAPEX` | 19.971 (COP MM) | Inversión total (anclada a la inversión real) |
| `PCT_PUBLICO` | 80 % | Aporte público no reembolsable (SGR/PDA/cooperación) |
| `PCT_DEUDA` / `PCT_EQUITY` | 10 % / 10 % | Deuda y equity |
| `KD` | 11 % | Costo de la deuda |
| `KE` | 14 % | Costo del equity |
| `TASA_SOCIAL` | 9 % | Tasa social de descuento (DNP) |
| `TASA_IMPUESTOS` | 35 % | Impuesto de renta |
| `INGRESO_ANIO1` / `OPEX_ANIO1` | 1.500 / 1.150 | Ingreso por tarifa y OPEX año 1 |
| `BEN_*` (agua alterna, salud, tiempo) | 2.800 / 900 / 450 | Beneficios sociales año 1 |
| `HORIZONTE` | 25 años | Periodo de evaluación |

### 5.2 WACC (con aporte público)

A diferencia de un proyecto privado, aquí el 80 % es **aporte público**, cuyo costo de oportunidad es la **tasa social (9 %)**:

> **WACC = %Público·TasaSocial + %Equity·Ke + %Deuda·Kd·(1 − t)**
> WACC = 0,80·9 % + 0,10·14 % + 0,10·11 %·(1 − 0,35) = **9,31 %**

### 5.3 Las TRES evaluaciones (clave para entender el resultado)

1. **Financiera del proyecto (solo tarifas):** ¿se paga el acueducto con lo que cobra a los usuarios? → **VPN = −15.487 MM, TIR = −2,45 %**. **NO.** Esto es normal en acueductos del Pacífico.
2. **Del inversionista (con aporte público):** con 80 % de aporte, la TIR sube a **10,46 %**, aún por debajo del 14 % que exige un privado → conviene un **operador público/comunitario**.
3. **Socioeconómica (tasa social 9 %):** suma los **beneficios sociales** (ahorro en agua embotellada, salud por EDA evitada, tiempo) menos OPEX → **VPN = +19.626 MM, B/C = 1,56**. **Aquí está la justificación real del proyecto.**

### 5.4 Análisis de sensibilidad

Se calcula la TIR del inversionista variando el % de aporte público (0 % → 90 %). Muestra que el proyecto solo es atractivo para un privado con aporte ≥ 85–90 %, lo que confirma su naturaleza de **bien público**.

---

## 6. Resultados obtenidos (resumen)

| Indicador | Valor | Lectura |
|---|---|---|
| **QMD (diseño)** | 41,5 L/s | Tamaño de la PTAP (45 L/s) |
| **WACC** | 9,31 % | Costo de financiar (con aporte público) |
| **VPN proyecto** | −15.487 MM | < 0 → no rentable solo con tarifas |
| **TIR inversionista** | 10,46 % | < Ke → requiere operador público |
| **VPN social** | +19.626 MM | > 0 → socialmente rentable |
| **B/C** | 1,56 | > 1 → justifica la inversión pública |

**Conclusión:** el proyecto es **técnicamente viable** y **socialmente rentable**, pero **no se financia solo con tarifas**: requiere cofinanciación pública, exactamente como ocurrió en la realidad (MinVivienda + cooperación).

---

## 7. Cómo recalcular todo si cambias los supuestos

```bash
cd Solucion
python3 modelo_financiero.py   # imprime indicadores y regenera resultados_modelo.csv
python3 generar_arboles.py     # regenera los árboles (PNG)
python3 generar_excel.py       # regenera el Excel con fórmulas vivas
python3 generar_word.py        # regenera el Word (lee el CSV para los flujos)
```

Cambia los valores en la sección de parámetros de `modelo_financiero.py` (y/o en la hoja **Supuestos** del Excel) y todo se recalcula solo.

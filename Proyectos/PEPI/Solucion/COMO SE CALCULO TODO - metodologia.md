# Cómo se calculó todo — Metodología (Proyecto PEPI · Acueducto de Tadó, Chocó)

Este documento explica, paso a paso, cómo se construyó cada parte del informe, **con fuentes reales**, para que puedas sustentarlo o adaptarlo.

> Caso: **optimización y ampliación del acueducto de Tadó (Chocó)**. Municipio real; los datos de población, geografía y normativa son reales (ver fuentes al final).

---

## 1. La guía (PDF) y los entregables

El `PROYECTO PEPI.pdf` lista los entregables: resumen ejecutivo, árbol de problemas, árbol de objetivos, MML, solución de ingeniería, análisis financiero (CAPEX/OPEX, Deuda+Equity, WACC, TIR, VPN, flujos), matriz de 20 riesgos e intervención de 10 (5 ambientales). Informe máx. 10 páginas.

## 2. Datos del municipio (REALES — DANE)

- Población total 2025 (proyección DANE): **20.476 hab**.
- **Cabecera urbana: 11.917 hab** (es la que sirve el acueducto urbano).
- Altitud **75 m s. n. m.**; río **San Juan**; clima de selva tropical húmeda (de los más lluviosos del mundo); economía minera (oro/platino).

## 3. Caudal de diseño — Resolución 0330 de 2017 (RAS)

1. **Proyección de población** a 25 años (horizonte de diseño), método geométrico con tasa 0,8 %:
   `Pf = 11.917 × (1 + 0,008)^25 = 14.544 hab`.
2. **Dotación neta**: 140 L/hab·día (altitud < 1.000 m, Art. 43 de la Res 0330).
3. **Pérdidas** máximas admisibles 25 % → **dotación bruta** = 140 / (1 − 0,25) = **186,7 L/hab·día**.
4. **Caudal medio diario** `Qmd = dotación bruta × población / 86.400 = 31,4 L/s`.
5. **Caudal máximo diario** `QMD = Qmd × k₁ (1,30) = 40,8 L/s` → **es el caudal de diseño de la PTAP**.
6. **Caudal máximo horario** `QMH = QMD × k₂ (1,60) = 65,4 L/s` → diseño de redes.
7. Se adopta una **PTAP de 45 L/s** (holgura sobre el QMD).

## 4. CAPEX — Presupuesto de obra

Se arma un **presupuesto por capítulos** (captación, aducción, PTAP, tanque, bombeo, redes, micromedición, estudios) que suma **COP 13.470 MM**. Los precios son **de referencia de mercado** (con sobrecosto por la logística del Chocó) y **deben validarse con un APU (Análisis de Precios Unitarios)** actualizado y la lista de precios regional. Esto se dice explícitamente en la Sección 10 del informe (transparencia).

## 5. Estructura financiera y WACC

- Realidad de los acueductos municipales pequeños y pobres: se cofinancian casi en su totalidad con **recursos públicos no reembolsables** (SGR, PDA, SGP, cooperación). Caso base: **90 % aporte público / 5 % deuda / 5 % equity**.
- **WACC** sobre el capital remunerado (deuda+equity, 50/50):
  `WACC = 0,5×Ke + 0,5×Kd×(1−t) = 0,5×0,14 + 0,5×0,11×0,65 = 10,58 %`.
- Coherente con el orden de magnitud de la **tasa de descuento regulatoria de la CRA** (Res CRA 943 de 2021).

## 6. Flujos, VPN y TIR (tres ópticas)

- **Flujo del Proyecto (FCLP)** = EBIT×(1−t) + Depreciación; se descuenta al WACC.
- **Flujo del Inversionista (FCLA)** = (EBIT − intereses)×(1−t) + Depreciación − abono de capital; se descuenta al Ke.
- **Flujo del Banco** = desembolsa la deuda y recibe la cuota fija (sistema francés).
- Se calculan **VPN** (trae los flujos a hoy) y **TIR** (tasa que hace VPN = 0; en el código por bisección).

**Resultados (Python y Excel coinciden):**

| Óptica | VPN (COP MM) | TIR | Lectura |
|---|---:|---:|---|
| Proyecto "puro" (@WACC 10,58 %) | −10.523 | −1,58 % | No rentable solo con tarifas (típico) |
| Inversionista (@Ke 14 %) | +1.064 | 30,2 % | Viable con 90 % de aporte público |

## 7. Evaluación socioeconómica (lo que justifica la inversión pública)

Con la **tasa social de descuento del DNP (9 %)** y beneficios sociales (ahorro de los hogares en agua, reducción de costos en salud por EDA/vectores, tiempo):
- **VPN económico = +COP 5.123 MM**, **TIRE = 13,7 %**, **B/C = 1,18**.
- Conclusión: aunque no sea rentable financieramente por sí solo, **es socialmente rentable** → se justifica la cofinanciación pública.

## 8. Análisis de sensibilidad

Se varió el % de aporte público (70 %–95 %): el inversionista pasa de inviable (TIR 7,5 % con 70 %) a muy atractivo (TIR 66 % con 95 %). **Punto de equilibrio ≈ 81 % de aporte público**.

## 9. Recalcular todo si cambias supuestos

1. Edita `modelo_financiero.py` (o la hoja **Supuestos** del Excel) y ejecuta:
   ```bash
   python3 modelo_financiero.py
   python3 generar_excel.py
   python3 generar_arboles.py
   python3 generar_word.py
   ```
2. El Excel tiene **fórmulas vivas**: cambia un supuesto y todo se recalcula.

## 10. Fuentes
DANE (CNPV 2018 y proyecciones), Resolución 0330 de 2017, Resolución 2115 de 2007, Resolución CRA 943 de 2021, Ley 142 de 1994, tasa social de descuento del DNP, Decreto 1072 de 2015 y NSR-10. Ver Sección 10 del informe para el detalle y las notas de transparencia.

# 📘 PEPI — Proyecto

## Estructura
- `PROYECTO PEPI.pdf` — Guía/enunciado de entregables (original).
- **`Solucion/`** — Solución desarrollada (informe, modelo financiero y documentos de apoyo).

## Qué hay en `Solucion/`
| Archivo | Qué es |
|---|---|
| `INFORME_PEPI.docx` | **Informe completo en Word (entregable principal)** con árboles incrustados |
| `MODELO FINANCIERO PEPI.xlsx` | **Excel con TODOS los cálculos** (fórmulas vivas: diseño de caudal, WACC, TIR, VPN, flujos, amortización, riesgos) |
| `INFORME_PEPI.md` | Mismo informe en Markdown (árboles como imagen) |
| `arbol_problemas.png` / `arbol_objetivos.png` | Árboles como esquema visual |
| `modelo_financiero.py` | Modelo de cálculo en Python (diseño de caudal Res. 0330 + WACC, TIR, VPN, flujos, evaluación social) |
| `resultados_modelo.csv` | Resultados y flujos exportados |
| `generar_word.py` | Script que genera el Word |
| `generar_excel.py` | Script que genera el Excel |
| `generar_arboles.py` | Script que genera los árboles (PNG) |
| `COMO SE CALCULO TODO - metodologia.md` | Explicación de cada cálculo (para sustentar) |
| `PASO A PASO - como usar y entregar.md` | Guía de uso y entrega |

## Datos clave del proyecto desarrollado
- **Tema:** Optimización y ampliación del sistema de acueducto del municipio de **Tadó (Chocó)** — PTAP de **45 L/s** (caso real).
- **Contexto:** Tadó tiene 17.000 hab (CNPV 2018, DANE), está sobre el río San Juan y es uno de los lugares más lluviosos del planeta (~7.900 mm/año); aun así carecía de agua potable continua. Proyecto real ejecutado por MinVivienda + cooperación española (inversión COP 19.971 MM).
- **Diseño de caudal (Res. 0330/2017):** QMD = 41,5 L/s → PTAP de 45 L/s.
- **Resultados:** WACC 9,31 % · VPN proyecto **−15.487 MM** (no rentable solo con tarifas) · TIR inversionista 10,46 % · **VPN social +19.626 MM** · **B/C 1,56** (socialmente rentable).

> **Conclusión:** el proyecto NO se financia solo con tarifas (norma en acueductos del Pacífico); su justificación es **socioeconómica** y requiere **cofinanciación pública** (SGR/PDA/cooperación), tal como ocurrió en la realidad.

## Reproducir el modelo
```bash
cd Solucion
python3 modelo_financiero.py   # imprime indicadores y genera resultados_modelo.csv
python3 generar_arboles.py     # genera arbol_problemas.png y arbol_objetivos.png
python3 generar_excel.py       # genera "MODELO FINANCIERO PEPI.xlsx" (fórmulas vivas)
python3 generar_word.py        # regenera INFORME_PEPI.docx con los árboles incrustados
```

> Nota de transparencia: los datos de Tadó (población, fuente, clima, inversión real) son **verificables**; los parámetros sin fuente oficial específica (desglose del presupuesto, tarifas, IANC, beneficios sociales) son **estimaciones razonables** señaladas en el informe. Las fuentes se listan en la sección 10 del informe.

# 📘 PEPI — Proyecto

## Estructura
- `PROYECTO PEPI.pdf` — Guía/enunciado de entregables (original).
- **`Solucion/`** — Solución desarrollada (informe, modelo financiero y documentos de apoyo).

## Qué hay en `Solucion/`
| Archivo | Qué es |
|---|---|
| `INFORME_PEPI.docx` | **Informe completo en Word (entregable principal)** con árboles incrustados |
| `MODELO FINANCIERO PEPI.xlsx` | **Excel con TODOS los cálculos** (fórmulas vivas: WACC, TIR, VPN, flujos, amortización, riesgos) |
| `INFORME_PEPI.md` | Mismo informe en Markdown (árboles como imagen + diagrama) |
| `arbol_problemas.png` / `arbol_objetivos.png` | Árboles como esquema visual |
| `modelo_financiero.py` | Modelo de cálculo en Python (WACC, TIR, VPN, flujos) |
| `resultados_modelo.csv` | Resultados y flujos exportados |
| `generar_word.py` | Script que genera el Word |
| `generar_excel.py` | Script que genera el Excel |
| `generar_arboles.py` | Script que genera los árboles (PNG) |
| `COMO SE CALCULO TODO - metodologia.md` | Explicación de cada cálculo (para sustentar) |
| `PASO A PASO - como usar y entregar.md` | Guía de uso y entrega |

## Datos clave del proyecto desarrollado
- **Tema:** Construcción de PTAP (120 L/s) y ampliación del sistema de acueducto — Municipio de El Progreso.
- **Resultados financieros:** WACC 11,07 % · VPN proyecto COP 8.376 MM · TIR proyecto 18,13 % · TIR inversionista 24,78 %.

## Reproducir el modelo
```bash
cd Solucion
python3 modelo_financiero.py   # imprime indicadores y genera resultados_modelo.csv
python3 generar_arboles.py     # genera arbol_problemas.png y arbol_objetivos.png
python3 generar_excel.py       # genera "MODELO FINANCIERO PEPI.xlsx" (fórmulas vivas)
python3 generar_word.py        # regenera INFORME_PEPI.docx con los árboles incrustados
```

> Nota: el enunciado (PDF) es una guía de otro proyecto; esta solución es un desarrollo de ejemplo
> completo y consistente, útil como plantilla para adaptar al proyecto real.

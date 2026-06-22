# 📘 PEPI — Proyecto

## Estructura
- `PROYECTO PEPI.pdf` — Guía/enunciado de entregables (original).
- **`Solucion/`** — Solución desarrollada (informe, modelo financiero y documentos de apoyo).

## Caso desarrollado
**Optimización y ampliación del sistema de acueducto del municipio de Tadó (Chocó).**
Municipio real (DANE CNPV 2018: 20.476 hab. total, 11.917 en la cabecera), sobre el río San Juan.

## Qué hay en `Solucion/`
| Archivo | Qué es |
|---|---|
| `INFORME_PEPI.docx` | **Informe completo en Word (entregable principal)** con árboles incrustados |
| `MODELO FINANCIERO PEPI.xlsx` | **Excel con TODOS los cálculos** (fórmulas vivas; verificado contra Python) |
| `INFORME_PEPI.md` | Mismo informe en Markdown (árboles como imagen) |
| `arbol_problemas.png` / `arbol_objetivos.png` | Árboles como esquema visual |
| `modelo_financiero.py` | Modelo técnico-financiero (diseño Res 0330 + WACC/TIR/VPN/flujos + socioeconómico) |
| `resultados_modelo.csv` | Resultados y flujos exportados |
| `generar_excel.py` / `generar_word.py` / `generar_arboles.py` | Scripts generadores |
| `COMO SE CALCULO TODO - metodologia.md` | Explicación de cada cálculo (para sustentar) |
| `PASO A PASO - como usar y entregar.md` | Guía de uso y entrega |

## Datos clave (verificados Python = Excel)
- **Caudal de diseño (Res 0330/2017):** QMD = 40,8 L/s → PTAP de 45 L/s.
- **CAPEX:** COP 13.470 MM (presupuesto por capítulos).
- **Estructura:** 90 % aporte público + 5 % deuda + 5 % equity (realista para Chocó).
- **WACC:** 10,58 %.
- **VPN proyecto "puro":** −COP 10.523 MM (no rentable solo con tarifas — típico).
- **VPN/TIR inversionista:** +COP 1.064 MM / 30,2 % (viable con cofinanciación).
- **VPN socioeconómico (DNP 9 %):** +COP 5.123 MM · B/C = 1,18 (socialmente justificado).

## Reproducir el modelo
```bash
cd Solucion
python3 modelo_financiero.py   # imprime indicadores y genera resultados_modelo.csv
python3 generar_arboles.py     # genera arbol_problemas.png y arbol_objetivos.png
python3 generar_excel.py       # genera "MODELO FINANCIERO PEPI.xlsx" (fórmulas vivas)
python3 generar_word.py        # convierte INFORME_PEPI.md -> INFORME_PEPI.docx
```

> Fuentes y notas de transparencia: ver Sección 10 del informe. Los datos de población, geografía
> y normativa (DANE, Res 0330/2017, Res 2115/2007, CRA 943/2021, tasa social DNP) son reales; el CAPEX,
> tarifas y OPEX son estimaciones de referencia a validar con APU y el PDA del Chocó.

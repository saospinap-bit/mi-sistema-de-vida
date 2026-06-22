# Paso a paso — Cómo usar y entregar el Proyecto PEPI (Acueducto de Tadó, Chocó)

## 1. ¿Qué entrego?

| Archivo | ¿Se entrega? |
|---|---|
| **`INFORME_PEPI.docx`** | ✅ **ESTE es el entregable principal** (Word con árboles y tablas) |
| `MODELO FINANCIERO PEPI.xlsx` | ✅ Anexo: el modelo con todos los cálculos (fórmulas vivas) |
| `INFORME_PEPI.md` | Referencia (mismo contenido, se ve en GitHub) |
| `modelo_financiero.py`, `resultados_modelo.csv` | Soporte / anexos técnicos |
| `arbol_*.png`, `generar_*.py` | Insumos y scripts |
| `COMO SE CALCULO TODO - metodologia.md` | Para estudiar y sustentar |

## 2. Cómo descargar el Word

En GitHub, abre `Proyectos/PEPI/Solucion/INFORME_PEPI.docx` y dale a **"Download raw file"** (icono ⬇). Ábrelo en Word/Google Docs.

## 3. Antes de entregar — checklist
- [ ] Pon **tu nombre, código, materia y profesor** en la portada.
- [ ] Verifica que **no pase de 10 páginas** (límite del enunciado).
- [ ] Revisa que los **árboles** se vean bien.
- [ ] Si tu profesor exige fuentes oficiales del déficit/costos, reemplaza las estimaciones por el **PDA del Chocó**, el **SUI–Superservicios** y un **APU** real (ver Sección 10 del informe).

## 4. Cómo defenderlo (puntos clave)
1. **Tadó es real** (DANE: 20.476 hab.; cabecera 11.917; río San Juan; Chocó, alta pobreza).
2. **Caudal de diseño por la Res 0330/2017** → QMD 40,8 L/s → PTAP 45 L/s.
3. **WACC 10,58 %** (deuda+equity 50/50); el aporte público no exige retorno.
4. **Tres evaluaciones:** proyecto "puro" (no rentable, −10.523), inversionista (viable, TIR 30,2 %) y **socioeconómica** (VPN +5.123, B/C 1,18). La clave: estos acueductos **se justifican por el beneficio social** y se financian con recursos públicos.
5. **Riesgos:** 20 calificados con P×I; intervención de 10 (5 ambientales: turbiedad/mercurio del San Juan, inundaciones, lodos, vertimientos, fauna/flora).

## 5. ¿Quieres cambiar algo?
- Cambiar supuestos (CAPEX, tarifas, % aporte): edita la hoja **Supuestos** del Excel (todo se recalcula) o `modelo_financiero.py`.
- Cambiar de municipio: se ajustan población y fuente, y el diseño/financiero se recalcula.

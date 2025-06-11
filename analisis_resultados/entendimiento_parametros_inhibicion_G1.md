# Entendimiento del Impacto de Parámetros de Inhibición en la Selectividad de Detectores G1

Fecha: 2025-06-08

## 1. Introducción

Este documento resume los hallazgos obtenidos a través de una serie de experimentos (ver `analisis_selectividad_ruido_G1_exp1.md`) enfocados en mejorar la selectividad de las neuronas detectoras de secuencias del Grupo 1 (G1), especialmente `N_Detector_Secuencia123`, bajo condiciones de ruido. El objetivo principal era reducir los Falsos Positivos (FPs) sin sacrificar los Verdaderos Positivos (TPs).

Se investigaron principalmente tres parámetros:
- `AJUSTE_SELECTIVIDAD_PRUEBA`: Modifica el umbral de disparo de las neuronas detectoras durante la fase de prueba.
- `PESO_EXCITATORIO_A_INHIBIDORA_BASE`: Controla la fuerza de la conexión desde las neuronas presinápticas (N_Pre) hacia la neurona inhibitoria `N_INHIB1_ID`. Un valor más alto hace a `N_INHIB1_ID` más sensible.
- `PESO_INHIBITORIO_BASE`: Controla la fuerza de la conexión inhibitoria desde `N_INHIB1_ID` hacia las neuronas detectoras G1. Un valor más alto implica una inhibición más fuerte.

## 2. Parámetros Investigados y Hallazgos Clave

### 2.1. `AJUSTE_SELECTIVIDAD_PRUEBA`

Este parámetro incrementa el umbral de disparo de las neuronas detectoras durante las pruebas. Un valor más alto significa que se necesita más excitación acumulada para que un detector dispare.

- **Línea Base (`1.65 mV`):**
    - `N_Detector_Secuencia123`: 1 FP.
    - Red G1 Total: 6 FPs.
- **Experimento 1 (`1.80 mV`):**
    - `N_Detector_Secuencia123`: 2 FPs (empeoró).
    - Red G1 Total: 4 FPs (mejoró globalmente, pero no para el detector objetivo).

**Conclusión sobre `AJUSTE_SELECTIVIDAD_PRUEBA`:**
Incrementar este parámetro puede reducir FPs globalmente al hacer los detectores menos propensos a disparar. Sin embargo, un valor demasiado alto puede ser contraproducente para detectores específicos (como `N_Detector_Secuencia123` en este caso) o incluso afectar TPs (aunque no se observó pérdida de TPs en estos experimentos). El valor base de `1.65 mV` pareció más adecuado para `N_Detector_Secuencia123` en combinación con otros ajustes.

### 2.2. `PESO_EXCITATORIO_A_INHIBIDORA_BASE`

Este parámetro determina cuán fácilmente se activa la neurona inhibitoria `N_INHIB1_ID` por la actividad de las neuronas de entrada.

- **Línea Base (`0.3`), con `PESO_INHIBITORIO_BASE = 0.3`:**
    - `N_Detector_Secuencia123`: 1 FP.
- **Experimento 2 (`0.25`), con `PESO_INHIBITORIO_BASE = 0.3`:**
    - `N_Detector_Secuencia123`: 1 FP (sin cambios, pero cambió la secuencia del FP).
    - Red G1 Total: 8 FPs (empeoró).
- **Experimento 3 (`0.35`), con `PESO_INHIBITORIO_BASE = 0.3`:**
    - `N_Detector_Secuencia123`: **0 FPs (¡Éxito!)**.
    - Red G1 Total: 6 FPs.

**Conclusión sobre `PESO_EXCITATORIO_A_INHIBIDORA_BASE`:**
- Reducir la sensibilidad de `N_INHIB1_ID` (valor de 0.25) fue perjudicial, aumentando los FPs totales.
- Incrementar la sensibilidad de `N_INHIB1_ID` (valor de 0.35) fue **crucial y muy beneficioso** para `N_Detector_Secuencia123`, logrando eliminar sus FPs. Esto sugiere que para `N_Detector_Secuencia123`, una activación más robusta y oportuna de la inhibición es clave para su selectividad.

### 2.3. `PESO_INHIBITORIO_BASE`

Este parámetro ajusta la magnitud del efecto inhibitorio que `N_INHIB1_ID` ejerce sobre los detectores G1.

- **Referencia (Configuración del Experimento 3: `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`, `PESO_INHIBITORIO_BASE = 0.3`):**
    - `N_Detector_Secuencia123`: 0 FPs.
    - Red G1 Total: 6 FPs.
- **Experimento 4 (`PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`, `PESO_INHIBITORIO_BASE = 0.35`):**
    - `N_Detector_Secuencia123`: 4 FPs (empeoró drásticamente).
    - Red G1 Total: 10 FPs (empeoró).

**Conclusión sobre `PESO_INHIBITORIO_BASE`:**
Manteniendo `N_INHIB1_ID` más sensible (con `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`), un incremento adicional en la fuerza directa de la inhibición (`PESO_INHIBITORIO_BASE` de 0.3 a 0.35) resultó ser excesivo. Esto degradó severamente la selectividad de `N_Detector_Secuencia123` y de la red en general. Parece que una inhibición demasiado fuerte puede desestabilizar el reconocimiento de secuencias o interferir de forma no deseada.

## 3. Interrelación de Parámetros y Funcionamiento Óptimo

Los experimentos demuestran una interdependencia entre `PESO_EXCITATORIO_A_INHIBIDORA_BASE` y `PESO_INHIBITORIO_BASE`:
- Primero, es necesario que la neurona inhibitoria `N_INHIB1_ID` se active de manera adecuada y oportuna en respuesta a los estímulos de entrada. Esto se logra ajustando `PESO_EXCITATORIO_A_INHIBIDORA_BASE`. Para `N_Detector_Secuencia123`, un valor de `0.35` fue óptimo.
- Segundo, una vez que `N_INHIB1_ID` se activa, la fuerza de su inhibición sobre los detectores G1 debe ser suficiente para suprimir FPs, pero no tan fuerte como para causar nuevos problemas o suprimir TPs. Esto se controla con `PESO_INHIBITORIO_BASE`. Para `N_Detector_Secuencia123` (con la sensibilidad de `N_INHIB1_ID` ya optimizada), un valor de `0.3` fue óptimo.

Es importante recordar que `N_Detector_Secuencia123` mostró ser particularmente sensible a la inhibición durante su fase de aprendizaje (ver memoria `f546ada3-37b8-4eef-9701-6a2fa8c5926d`). Aunque estos experimentos se centran en la selectividad durante la *prueba*, esta sensibilidad subyacente podría explicar por qué el ajuste fino de los parámetros de inhibición es tan crítico para su correcto desempeño.

## 4. Configuración Óptima Identificada (para `N_Detector_Secuencia123`)

Basado en los experimentos realizados, la configuración que proporcionó el mejor rendimiento (0 Falsos Positivos) para `N_Detector_Secuencia123` es:

- **`AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV`** (valor base)
- **`PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`**
- **`PESO_INHIBITORIO_BASE = 0.3`**

Esta configuración se encuentra actualmente activa en `configuracion/parametros_simulacion.py`.

## 5. Impacto en la Red General y Consideraciones Finales

Si bien la configuración óptima para `N_Detector_Secuencia123` eliminó sus Falsos Positivos, la red G1 en su conjunto todavía presenta 6 FPs (distribuidos entre los otros 5 detectores). Esto es el mismo número total de FPs que en la línea base, aunque la distribución ha cambiado.

Lograr una selectividad perfecta para todos los detectores simultáneamente es un desafío complejo. Optimizar un detector puede, en ocasiones, afectar a otros. Los resultados actuales representan un buen compromiso, especialmente si el detector `N_Detector_Secuencia123` es de particular interés.

Futuros trabajos podrían enfocarse en estrategias de inhibición más selectivas o en ajustes de parámetros individuales para los detectores que aún presentan FPs, teniendo cuidado de no degradar el rendimiento ya logrado para `N_Detector_Secuencia123`.

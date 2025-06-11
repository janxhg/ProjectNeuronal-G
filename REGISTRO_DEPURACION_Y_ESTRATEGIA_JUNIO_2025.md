# Registro de Depuración y Estrategia de Avance - Junio 2025

## 1. Contexto Inicial y Objetivo

El objetivo principal es refinar el proyecto NeuroBiologico, actualmente en el directorio `d:\NeuronalLikes\EXP\NeuroBiologico\`, para que utilice de manera efectiva solo tres neuronas detectoras de secuencias del Grupo 1 (G1):
*   `N_Detector_Secuencia123` (con `tau_m = 10 ms`)
*   `N_Detector_Secuencia321` (con `tau_m = 7 ms`)
*   `N_Detector_Secuencia132` (con `tau_m = 7 ms`)

Se busca que estas neuronas aprendan y detecten sus secuencias objetivo con alta precisión, tanto en ausencia como en presencia de ruido.

## 2. Problemas Encontrados (Principios de Junio 2025)

Las versiones de trabajo más recientes en el directorio `EXP` (por ejemplo, `NeuroBiologico_18_semi_semi` y las configuraciones que generaron logs como `simulacion_log_20250608_134729.txt` y `simulacion_log_20250608_134811.txt`) presentaron una falla crítica:
*   **Los detectores G1 no disparaban en absoluto.** Esto se observó consistentemente, resultando en múltiples Falsos Negativos incluso para sus secuencias objetivo y en ausencia de ruido.
*   Este comportamiento impedía cualquier evaluación de rendimiento o avance en la optimización de los parámetros específicos para los tres detectores.

## 3. Análisis de Versiones de Respaldo Funcionales

Para encontrar una base estable, se revisaron los logs de versiones anteriores del proyecto que se sabía que eran funcionales con 6 detectores G1:
*   `NeuroBiologico_15_configuración_optima` (log de referencia: `log15.txt`)
*   `NeuroBiologico_16_documentado_full` (log de referencia: `simulacion_log_20250608_134518.txt`)

Ambas versiones mostraron un rendimiento base correcto y muy similar para los 6 detectores G1:
*   **SIN RUIDO:** 0 Falsos Positivos, 0 Falsos Negativos.
*   **CON RUIDO:** Aproximadamente 6 Falsos Positivos, 0 Falsos Negativos.

Esto confirmó que existían configuraciones previas donde el mecanismo de detección y aprendizaje G1 funcionaba correctamente.

## 4. Decisión Estratégica (8 de Junio de 2025)

Debido a la persistente falla de los detectores G1 en las versiones recientes del directorio `EXP` y la dificultad para diagnosticar la causa raíz en ese contexto modificado, se tomó la siguiente decisión:
*   **Volver a una base de código conocida y funcional.**
*   Se ha optado por utilizar una **copia de `NeuroBiologico_16_documentado_full`** como el nuevo punto de partida para el desarrollo activo. Esta copia se encuentra ahora en `D:\NeuronalLikes\NeuroBiologico_16_documentado_full\` (o la ruta donde el USER haya colocado la copia de trabajo).
*   El `README.md` de esta versión ha sido actualizado para reflejar su estado y estructura.

## 5. Próximos Pasos (Sobre la Nueva Base Funcional)

El plan para avanzar desde esta base funcional (`NeuroBiologico_16_documentado_full`) es el siguiente:

1.  **Comparación de Configuraciones:**
    *   Revisar y comparar exhaustivamente los archivos `parametros_simulacion.py` y `src/main_parts/setup_network.py` de esta base funcional con los de las versiones `EXP` que no funcionaban. El objetivo es identificar las diferencias críticas que podrían haber causado el no disparo de los detectores (ej. pesos iniciales, conexiones, parámetros `tau_m` incorrectamente aplicados, lógica de inhibición).

2.  **Modificación Incremental de `setup_network.py`:**
    *   **Reducir Detectores G1:** Modificar `initialize_network` para crear únicamente los tres detectores G1 deseados: `N_Detector_Secuencia123`, `N_Detector_Secuencia321`, y `N_Detector_Secuencia132`.
    *   **Asignación de `tau_m`:**
        *   Asegurar que `N_Detector_Secuencia123` se inicialice con `tau_m = 10 ms` (utilizando `ps.TAU_M_DETECTOR_SEC123` si está definido, o un valor directo).
        *   Asegurar que `N_Detector_Secuencia321` y `N_Detector_Secuencia132` se inicialicen con `tau_m = 7 ms` (utilizando `ps.TAU_M_DETECTOR_BASE` si este es 7ms, o un valor directo).
    *   **Pesos Sinápticos Iniciales:** Verificar que `ps.PESO_INICIAL_SINAPSIS_BASE` esté en un valor adecuado (ej. ~0.5) para permitir el aprendizaje.
    *   **Conexiones e Inhibición:**
        *   Confirmar que las conexiones desde las neuronas presinápticas (P1, P2, P3) a los tres detectores G1 sean correctas.
        *   Revisar la lógica de inhibición. Si es necesario, asegurar que `N_Detector_Secuencia123` esté excluida de la inhibición general (ej. de `N_INHIB1_ID`), según los hallazgos de optimizaciones previas.

3.  **Ajustes en `main_simulador.py`:**
    *   Modificar las listas de detectores utilizadas en las fases de prueba y en la generación de gráficos para que solo incluyan los tres detectores G1 activos.
    *   Asegurar que los escenarios de prueba (`escenarios_G1_sin_ruido`, `escenarios_G1_con_ruido`) se definan y utilicen correctamente para evaluar los tres detectores.

4.  **Pruebas y Validación:**
    *   Ejecutar la simulación después de cada cambio significativo.
    *   Verificar en los logs que los tres detectores G1 disparen para sus secuencias objetivo y no para otras (evaluar TP y FP).
    *   Monitorear el aprendizaje de los pesos sinápticos.

5.  **Integración de Métricas Detalladas (Opcional pero Recomendado):**
    *   Considerar portar la lógica de cálculo de métricas detalladas (TP, FP, FN, Precisión, Recall, F1-Score) desde `testing_phase.py` de las versiones `EXP` a la nueva base funcional para un análisis de rendimiento más riguroso.

Este registro servirá para documentar el progreso y las decisiones tomadas durante este proceso de refactorización y depuración.

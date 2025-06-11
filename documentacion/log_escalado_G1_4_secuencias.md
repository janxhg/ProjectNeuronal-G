# Log de Escalado del Grupo 1 (G1) a 4 Secuencias

**Fecha de Inicio:** 2025-06-07

## 1. Objetivo Principal

El objetivo de esta fase es escalar la capacidad del Grupo 1 (G1) de neuronas detectoras para que pueda aprender y distinguir cuatro secuencias de estímulos distintas, en lugar de las tres actuales. Esto servirá como un primer paso para aumentar la capacidad representacional del sistema.

Adicionalmente, se investigará la hipótesis del USER sobre el parámetro `AJUSTE_SELECTIVIDAD_PRUEBA`.

## 2. Configuración de Partida (G1 con 3 Secuencias)

Nos basamos en la configuración exitosa donde `N_Detector_Secuencia123` y otras dos neuronas detectoras aprenden sus respectivas secuencias perfectamente. Los parámetros clave incluyen:

*   `NUM_NEURONAS_DETECTORAS_G1 = 3` (implícito o explícito en la configuración actual).
*   `N_Detector_Secuencia123` excluida de inhibición por `N_INHIB1_ID`.
*   `TAU_M_DETECTOR_SEC123 = 10.0 ms`, `TAU_M_DETECTOR_BASE = 7.0 ms` para las otras.
*   `PESO_INICIAL_SINAPSIS_BASE = 0.5`.
*   `DT_ENTRENAMIENTO_ESTIMULO = 1 ms`.
*   `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV`.

## 3. Hipótesis del USER sobre `AJUSTE_SELECTIVIDAD_PRUEBA`

El USER teoriza que el valor actual de `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV` podría estar relacionado con el número de neuronas detectoras, específicamente `0.55 mV` por cada neurona (0.55 mV * 3 neuronas = 1.65 mV).
Si esta hipótesis es correcta, al escalar a 4 neuronas detectoras, el nuevo valor debería ser `0.55 mV * 4 = 2.20 mV` para mantener una selectividad comparable durante la fase de prueba.

## 4. Plan de Acción Inicial

1.  **Modificar Parámetros:**
    *   Actualizar `NUM_NEURONAS_DETECTORAS_G1` (si existe como variable explícita, o asegurar que la lógica maneje 4) en `configuracion/parametros_simulacion.py`.
    *   Definir el patrón de estímulos para la cuarta secuencia (ej. P10-P11-P12).
2.  **Actualizar Creación de Red (`setup_network.py`):**
    *   Asegurar que se cree una cuarta neurona detectora (`N_Detector_Secuencia4`).
    *   Asignarle los parámetros correspondientes (ej. `tau_m` base, a menos que requiera uno específico).
    *   Establecer las conexiones sinápticas desde las neuronas de entrada (`Pre`) correspondientes al nuevo patrón hacia `N_Detector_Secuencia4`.
    *   Decidir si esta nueva neurona estará sujeta a la inhibición de `N_INHIB1_ID` o si también será excluida (para empezar, podríamos mantenerla inhibida como las otras detectoras base, a menos que la secuencia sea particularmente difícil de aprender).
3.  **Actualizar Lógica de Simulación (`main_simulador.py`):**
    *   Asegurar que la nueva secuencia se incluya en los ciclos de entrenamiento.
    *   Asegurar que la nueva secuencia se presente durante la fase de prueba.
    *   Adaptar la lógica de evaluación de resultados para incluir la cuarta neurona detectora.
4.  **Pruebas Iniciales:**
    *   Ejecutar la simulación con el valor actual de `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV`.
    *   Analizar si las cuatro neuronas aprenden correctamente sus secuencias y si la selectividad en la fase de prueba es adecuada (es decir, si cada neurona responde preferentemente a su secuencia y no a las otras).
5.  **Probar Hipótesis (si es necesario):**
    *   Si la selectividad no es óptima con `1.65 mV`, o si se observan problemas, modificar `AJUSTE_SELECTIVIDAD_PRUEBA` a `2.20 mV` (según la hipótesis) y re-evaluar.

## 5. Log de Experimentos y Observaciones

*(Esta sección se llenará a medida que realicemos los experimentos)*

---

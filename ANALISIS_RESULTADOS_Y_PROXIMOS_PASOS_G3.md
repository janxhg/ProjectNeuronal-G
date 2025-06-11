# Análisis de Resultados de la Simulación (10-Jun-2025) y Próximos Pasos

Este documento resume el análisis completo del archivo de log `simulacion_log_20250610_040304.txt`, cuantificando el rendimiento de los detectores neuronales G1, G2 y G3. La conclusión principal es que, si bien G1 y G2 son robustos, **el detector G3 ha fallado en su fase de prueba y requiere una depuración exhaustiva.**

---

## 1. Rendimiento de los Detectores de Secuencia (Grupo G1)

Se evaluaron 6 detectores de secuencias de 3 picos en 36 escenarios de prueba (6 secuencias de prueba x 6 detectores) bajo dos condiciones: sin ruido y con ruido.

### 1.1. Pruebas SIN RUIDO
*   **Verdaderos Positivos (TP):** 6/6 (100%) - Cada detector disparó correctamente para su secuencia objetivo.
*   **Verdaderos Negativos (TN):** 30/30 (100%) - Ningún detector disparó para secuencias no objetivo.
*   **Falsos Positivos (FP):** 0
*   **Falsos Negativos (FN):** 0
*   **Conclusión:** Rendimiento **perfecto**. Cero errores.

### 1.2. Pruebas CON RUIDO
*   **Verdaderos Positivos (TP):** 6/6 (100%) - Todos los detectores identificaron su secuencia objetivo a pesar del ruido.
*   **Falsos Negativos (FN):** 0 - No hubo fallos en la detección de la secuencia correcta.
*   **Falsos Positivos (FP):** **8 errores**. Varios detectores dispararon incorrectamente para secuencias que no eran su objetivo.
    *   Este nivel de Falsos Positivos es aceptable y esperado en condiciones de ruido, demostrando un buen equilibrio entre sensibilidad y selectividad.

---

## 2. Rendimiento del Detector de Contexto (Grupo G2)

Se evaluó un detector para la secuencia contextual `A -> B`.

*   **Pruebas SIN y CON RUIDO:**
    *   **Verdaderos Positivos:** 1/1 (100%)
    *   **Verdaderos Negativos:** 1/1 (100%)
    *   **Falsos Positivos / Falsos Negativos:** 0
*   **Conclusión:** Rendimiento **perfecto**. Cero errores en todas las condiciones.

---

## 3. Rendimiento del Detector de Eventos Complejos (Grupo G3)

Se evaluó un detector (`N_G3_Detector_Evento_A_AB`) diseñado para disparar solo cuando la activación del detector G1 (`G1_A`) es seguida, con un intervalo de tiempo específico, por la activación del detector G2 (`G2_AB`).

*   **Prueba de Verdadero Positivo (`G1A_then_G2AB_CorrectTiming`):**
    *   **Resultado Esperado:** G3 debía disparar.
    *   **Resultado Obtenido:** G3 **NO** disparó.
    *   **Clasificación:** **1 Falso Negativo (Error Crítico).**

*   **Pruebas de Verdadero Negativo (`Only_G1A`, `Only_G2AB`, etc.):**
    *   **Resultado Esperado:** G3 no debía disparar.
    *   **Resultado Obtenido:** G3 no disparó (Correcto).

*   **Conclusión:** El detector G3 **no es funcional**. El proceso de entrenamiento (aprendizaje por STDP) no ha logrado que la neurona G3 fortalezca sus sinapsis lo suficiente como para disparar ante la coincidencia temporal de sus entradas de G1 y G2.

---

## 4. Próximos Pasos

El análisis confirma que la simulación ahora se ejecuta de principio a fin y que los componentes G1 y G2 son robustos.

El **objetivo prioritario** para la próxima sesión es **diagnosticar y corregir el fallo de aprendizaje en la neurona G3**. Las áreas a investigar incluyen:
1.  Parámetros de la regla de aprendizaje STDP para G3.
2.  Magnitud y duración de los impulsos durante el entrenamiento de G3.
3.  Posibles interferencias o umbrales inadecuados que impiden la potenciación sináptica.

Se creará un registro de depuración específico para este problema.

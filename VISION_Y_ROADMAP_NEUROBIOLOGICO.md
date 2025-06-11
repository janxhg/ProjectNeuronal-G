# Visión del Proyecto NeuroBiologico y Alineación con el Roadmap de Cerebro Artificial

## 1. Introducción al Proyecto NeuroBiologico

El proyecto `NeuroBiologico` tiene como objetivo principal desarrollar y simular redes neuronales de spiking (SNNs) biológicamente plausibles, capaces de realizar tareas de detección de secuencias temporales y reconocimiento de patrones contextuales. Se enfoca en la implementación de mecanismos de aprendizaje local, como la Plasticidad Dependiente del Tiempo de Disparo (STDP), y en la exploración de dinámicas neuronales como la Adaptación de la Frecuencia de Disparo (SFA).

Actualmente, el sistema se centra en:
*   **Neuronas Detectoras de Secuencia (Grupo 1 - G1):** Neuronas que aprenden a reconocer secuencias temporales específicas de eventos de entrada (ej., P1->P2->P3).
*   **Neuronas Detectoras de Patrones Contextuales (Grupo 2 - G2):** Neuronas que aprenden a reconocer la co-ocurrencia de patrones de entrada, representando un contexto.
*   **Mecanismos de Inhibición:** Para refinar la selectividad y eficiencia de la red.
*   **Parámetros Neuronales Específicos:** Como la constante de tiempo de membrana (`tau_m`), que se ha demostrado crucial para la detección de secuencias específicas.

## 2. Alineación con el Roadmap General de Cerebro Artificial

El proyecto `NeuroBiologico` se enmarca principalmente dentro de la **Fase 0: Fundamentos y Herramientas** del `ROADMAP_CEREBRO_ARTIFICIAL.md`, sentando las bases para fases más avanzadas. Específicamente, contribuye a los siguientes puntos:

### Fase 0: Fundamentos y Herramientas

*   **1. Modelado Neuronal Básico:**
    *   **Modelos de Neuronas Individuales:** `NeuroBiologico` utiliza un modelo de neurona Leaky Integrate-and-Fire (LIF), que es un primer paso fundamental. La implementación de SFA añade una dinámica más rica. El trabajo actual con `tau_m` variables para diferentes detectores G1 es un refinamiento de estos modelos individuales para tareas específicas.
    *   **Mecanismos de Plasticidad a Largo Plazo:**
        *   **STDP (Spike-Timing-Dependent Plasticity):** Es el mecanismo de aprendizaje primario en `NeuroBiologico` para las sinapsis excitatorias hacia las neuronas detectoras G1 y G2. Esto es crucial para que las neuronas aprendan las secuencias y patrones.

*   **2. Simulador de Redes Neuronales Eficiente:**
    *   Aunque `NeuroBiologico` es actualmente un simulador a pequeña escala, su desarrollo (incluyendo la modularidad del código, la gestión de parámetros y las funciones de visualización) contribuye a la experiencia necesaria para construir simuladores más grandes y eficientes. Las herramientas de logging y visualización de pesos son un embrión de las herramientas de análisis mencionadas en el roadmap.

### Hacia la Fase 1: Módulos Cerebrales y Microcircuitos Funcionales

`NeuroBiologico` también comienza a tocar aspectos de la **Fase 1**:

*   **4. Modelado de Microcircuitos Canónicos:**
    *   Los ensamblajes de neuronas presinápticas, detectoras (G1, G2) e inhibitorias en `NeuroBiologico` pueden considerarse implementaciones tempranas de **microcircuitos funcionales**. Están diseñados para realizar tareas específicas (detección de secuencias, detección de co-ocurrencias) que son fundamentales para procesamientos más complejos.
    *   La lógica de inhibición selectiva (ej., `N_Detector_Secuencia123` siendo exenta de cierta inhibición) es un ejemplo de diseño de conectividad específica dentro de un microcircuito.

## 3. Objetivos de NeuroBiologico a Corto y Medio Plazo (dentro del Roadmap)

Los próximos pasos para `NeuroBiologico` se centran en solidificar y expandir sus contribuciones a la Fase 0 y comenzar a abordar más robustamente la Fase 1:

*   **Refinar Modelos Neuronales y Sinápticos (Fase 0.1):**
    *   Continuar investigando el impacto de parámetros como `tau_m` y umbrales de disparo en la selectividad y robustez.
    *   Explorar variantes de STDP o reglas de aprendizaje adicionales si es necesario.
    *   Considerar la implementación de plasticidad homeostática básica para mejorar la estabilidad de la red a medida que crece en complejidad.
*   **Mejorar Robustez y Escalabilidad de Microcircuitos (Fase 0.2, Fase 1.4):**
    *   Asegurar que los detectores G1 y G2 funcionen de manera fiable bajo diversas condiciones (ej., ruido, variaciones temporales).
    *   Investigar cómo escalar el número de secuencias y patrones que la red puede manejar.
*   **Integración de Módulos (Fase 1.4):**
    *   Explorar cómo los detectores G1 (secuencias) y G2 (contexto) pueden interactuar de manera más profunda. Por ejemplo, ¿puede la activación de un detector de contexto G2 modular el umbral o la plasticidad de los detectores de secuencia G1?

## 4. Visión a Largo Plazo

`NeuroBiologico` sirve como un banco de pruebas esencial. Las lecciones aprendidas sobre cómo las neuronas individuales y los pequeños circuitos pueden aprender y procesar información temporal y contextual son cruciales. A largo plazo, los principios y módulos desarrollados en `NeuroBiologico` podrían integrarse en arquitecturas más grandes que aborden:

*   Sistemas sensoriales primarios (Fase 1.5).
*   Módulos de memoria más complejos (Fase 2).
*   Funciones cognitivas superiores (Fases 3 y 4).

El enfoque en la plausibilidad biológica y el aprendizaje local en `NeuroBiologico` es fundamental para la visión de construir una AGI que no solo sea inteligente, sino que también opere bajo principios similares a los del cerebro, permitiendo una mayor comprensión tanto de la inteligencia artificial como de la natural.

## 5. Jerarquía de Detectores: G1 y G2

Una capacidad fundamental del sistema `NeuroBiologico` es su habilidad para aprender y detectar patrones jerárquicos, comenzando con secuencias simples y progresando hacia combinaciones más complejas de estas secuencias. Esto se logra a través de dos grupos principales de neuronas detectoras: G1 y G2.

### 5.1. Detectores de Grupo 1 (G1): Detectores de Secuencias Primarias

*   **Función:** Las neuronas del Grupo 1 (G1) están diseñadas para aprender y detectar secuencias temporales específicas de eventos de entrada discretos. Por ejemplo, una neurona G1 puede aprender a disparar selectivamente en respuesta a la secuencia de estímulos P1 -> P2 -> P3.
*   **Mecanismo de Aprendizaje:** El aprendizaje en las neuronas G1 se basa principalmente en la Plasticidad Dependiente del Tiempo de Disparo (STDP). Las sinapsis desde las neuronas de entrada (N_Pre) hacia las neuronas G1 se fortalecen o debilitan según el orden temporal preciso de los disparos presinápticos y postsinápticos.
*   **Inhibición:** Se utiliza una neurona inhibitoria (`N_INHIB1_ID`) para mejorar la selectividad de los detectores G1, ayudando a suprimir disparos ante secuencias no objetivo, especialmente bajo condiciones de ruido. Se ha demostrado que el ajuste fino de los pesos excitatorios hacia esta neurona inhibitoria (`PESO_EXCITATORIO_A_INHIBIDORA_BASE`) y los pesos inhibitorios desde esta hacia los detectores G1 (`PESO_INHIBITORIO_BASE`), junto con el umbral de prueba (`AJUSTE_SELECTIVIDAD_PRUEBA`), es crucial para optimizar la selectividad (ver `analisis_resultados/analisis_selectividad_ruido_G1_exp1.md` y `analisis_resultados/entendimiento_parametros_inhibicion_G1.md`).
*   **Ejemplo de Éxito:** Se logró una selectividad perfecta (0 Falsos Positivos con ruido) para `N_Detector_Secuencia123` con la configuración: `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV`, `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`, `PESO_INHIBITORIO_BASE = 0.3`.

### 5.2. Detectores de Grupo 2 (G2): Detectores de Secuencias de Detectores G1

*   **Función:** Las neuronas del Grupo 2 (G2) representan un nivel superior en la jerarquía de detección. Están diseñadas para aprender y detectar secuencias de activación de las neuronas del Grupo 1. Es decir, un detector G2 aprende a reconocer cuándo un detector G1 específico dispara, seguido por el disparo de otro detector G1 específico.
*   **Mecanismo de Aprendizaje:** Al igual que los G1, los detectores G2 utilizan STDP para aprender. Las sinapsis hacia una neurona G2 provienen de las neuronas G1, y su peso se ajusta en función de la temporización relativa de las activaciones de estas neuronas G1 y la activación de la propia neurona G2.
*   **Ejemplo de Éxito (Simulación `simulacion_log_20250608_154603.txt`):**
    *   Se configuró un detector G2, `N_G2_DetectorAB`, para aprender la secuencia donde `N_Detector_Secuencia123` (actuando como neurona 'A' para G2) se activa, seguida por la activación de `N_Detector_Secuencia321` (actuando como neurona 'B' para G2).
    *   **Resultados:** `N_G2_DetectorAB` demostró un **rendimiento perfecto**:
        *   **SIN RUIDO:** Disparó correctamente para la secuencia objetivo (A->B) y no disparó para la secuencia no objetivo (B->A).
        *   **CON RUIDO:** Mantuvo el rendimiento perfecto, disparando para A->B y no para B->A, demostrando robustez.
    *   Esto confirma que la arquitectura puede aprender exitosamente secuencias de segundo orden.

Esta capacidad de construir detectores jerárquicos (G1 aprendiendo secuencias de entradas, G2 aprendiendo secuencias de G1) es un paso fundamental hacia el reconocimiento de patrones más abstractos y complejos.

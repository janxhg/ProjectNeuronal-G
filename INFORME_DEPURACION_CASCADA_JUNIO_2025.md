# Informe de Depuración y Validación: Cascada G1->G2->G3

**Fecha:** 11 de Junio, 2025

## 1. Objetivo

El propósito de este documento es detallar el proceso de diagnóstico, depuración y validación final de la cascada de activación neuronal `G1 -> G2 -> G3` en la nueva arquitectura orientada a objetos del simulador. El objetivo era resolver un fallo crítico donde la neurona `G2` no lograba disparar en presencia de `G3` y confirmar que la red dinámica funciona según lo diseñado.

## 2. Problema Inicial

Tras la refactorización a una arquitectura orientada a objetos, se detectó un comportamiento anómalo:

- La neurona `G1` disparaba correctamente al recibir su secuencia de estímulos.
- La neurona `G2` no llegaba a disparar si la neurona `G3` estaba presente en la simulación.
- La sospecha inicial apuntaba a una "interferencia" por parte de `G3`, que podría estar reseteando el estado de `G2` de forma prematura.

## 3. Estrategia de Depuración y Pasos Realizados

Se adoptó un enfoque metódico y por capas para aislar y resolver el problema:

1.  **Aislamiento de la Cascada G1->G2:**
    - Se modificó temporalmente `main_simulador.py` para deshabilitar la creación y actualización de la neurona `G3`.
    - **Resultado:** En aislamiento, la cascada `G1 -> G2` funcionó perfectamente. `G2` disparaba al recibir la secuencia correcta de impulsos de dos neuronas `G1` distintas, validando su lógica interna.

2.  **Corrección del Bucle de Simulación:**
    - Se identificó que el bucle principal de la simulación no contenía pasos explícitos para la propagación de impulsos. La simulación avanzaba sin dar tiempo a que un disparo se transmitiera y fuera procesado por la siguiente neurona en la cadena.
    - **Acción:** Se refactorizó `run_simulation` para incluir "pasos de propagación" explícitos, que actualizan la red repetidamente hasta que todos los disparos se han resuelto.

3.  **Instrumentación con Logging Detallado:**
    - Para obtener visibilidad completa del estado interno, se añadieron registros de `logging` de nivel `DEBUG` en los métodos clave (`__init__`, `recibir_impulso`, `actualizar_estado`, `resetear_estado`) de las clases `NeuronaBase`, `NeuronaG2` y `NeuronaG3`.
    - Estos logs permitieron trazar el potencial de membrana, el estado de espera y los contadores de ventana temporal de cada neurona en cada paso de la simulación.

4.  **Análisis de Logs y Validación Final:**
    - Se reintrodujo la neurona `G3` en la simulación, ahora con el `logging` activado y el bucle de propagación corregido.
    - Se ejecutó el escenario de prueba completo y se analizó el archivo de log resultante (`simulacion_log_20250611_000524.txt`).

## 4. Hallazgos y Conclusión

El análisis del log final reveló la verdad:

- **No existía una interferencia directa.** La neurona `G3` no modificaba el estado de `G2`.
- El problema raíz era la **falta de pasos de propagación** en el simulador. `G2` nunca tenía la oportunidad de disparar y propagar su señal a `G3` antes de que la simulación avanzara.
- El log confirmó la secuencia correcta de eventos:
    1.  `G1` dispara.
    2.  `G2` y `G3` reciben el impulso y entran en estado de espera.
    3.  Otra `G1` dispara, completando la secuencia para `G2`.
    4.  **`G2` dispara exitosamente.**
    5.  `G3` recibe el impulso de `G2` dentro de su ventana temporal.
    6.  **`G3` dispara exitosamente, completando la detección del evento complejo.**

## 5. Limpieza de Código

Una vez validado el correcto funcionamiento, se procedió a una fase de limpieza para profesionalizar el código:

- Se eliminaron todas las sentencias `logging.debug` añadidas durante la depuración en los archivos:
    - `src/core/elementos_neuronales.py`
    - `src/core/neurona_g2.py`
    - `src/core/neurona_g3.py`
- Se conservaron únicamente los logs de nivel `INFO` que marcan eventos importantes (disparos, inicio/fin de simulación), resultando en una salida de log limpia y legible.

## 6. Estado Actual y Próximos Pasos

**Misión Cumplida.** El núcleo del simulador neuronal es ahora **estable, robusto y ha sido completamente validado**. La arquitectura dinámica no solo es funcional, sino que se ha demostrado su capacidad para gestionar secuencias de eventos complejos en cascada.

El proyecto está oficialmente listo para avanzar hacia la **Fase 3: Implementación de Plasticidad Sináptica**, incluyendo:

- **Aprendizaje Hebbiano:** Refuerzo de conexiones sinápticas activas.
- **Poda Sináptica:** Debilitamiento de conexiones sinápticas en desuso.

---

## Sesión de Depuración: 11 de Junio de 2025 - Validación del Aprendizaje Jerárquico

### Objetivo
El objetivo de esta sesión fue depurar y validar el ciclo completo de aprendizaje jerárquico (G1 -> G2 -> G3), asegurando que el simulador pudiera:
1.  Crear dinámicamente neuronas conceptuales (G2) a partir de estímulos sensoriales (G1).
2.  Identificar de forma fiable las neuronas G2 representativas de cada concepto.
3.  Formar neuronas de abstracción (G3) a partir de la co-activación de neuronas G2.

### Diagnóstico Inicial
La simulación se ejecutaba pero no completaba el aprendizaje jerárquico. El análisis de los logs reveló dos problemas críticos:
1.  **`TypeError` en `NeuronaG3`:** El `GestorPlasticidad` intentaba crear neuronas G3 pasando los argumentos `id_input_A` e `id_input_B`, pero el constructor de `NeuronaG3` esperaba `id_input_g1` e `id_input_g2`.
2.  **Fallo Lógico en la Identificación de Conceptos:** Tras corregir el `TypeError`, un nuevo análisis de logs mostró un `ERROR` que indicaba que el sistema no podía identificar las neuronas G2 distintas para 'Gato' y 'Perro', abortando la fase final de abstracción.

### Proceso de Depuración y Soluciones

**Paso 1: Refactorización de `NeuronaG3`**
- **Acción:** Se modificó el constructor de `src/core/neurona_g3.py` para aceptar los parámetros genéricos `id_input_A` e `id_input_B`.
- **Resultado:** Esto resolvió el `TypeError` y convirtió a `NeuronaG3` en un detector de secuencias genérico, permitiendo al `GestorPlasticidad` crear instancias correctamente.

**Paso 2: Corrección de la Lógica de Identificación de Conceptos**
- **Análisis:** Se localizó la función anidada `_identificar_neurona_concepto` dentro de `demostrar_aprendizaje_jerarquico` en `main_simulador.py`. Se descubrió que su lógica era demasiado simplista: seleccionaba la neurona G2 basándose únicamente en el *número* de conexiones entrantes y usaba un umbral estricto que causaba el fallo.
- **Acción:** Se refactorizó por completo la función `_identificar_neurona_concepto`. La nueva lógica es más robusta y coherente con los principios de aprendizaje Hebbiano:
    1.  Filtra las neuronas G2 candidatas, requiriendo un mínimo de 2 conexiones desde el grupo de neuronas G1 de origen.
    2.  Selecciona como "ganadora" a la candidata cuya **suma de pesos de conexión** sea la más alta.
- **Resultado:** Este cambio prioriza a las neuronas cuyas conexiones han sido más reforzadas, asegurando que se elija a la representante más fuerte y fiable del concepto.

### Validación y Conclusión
Tras aplicar la corrección final, se ejecutó de nuevo la simulación (`demostrar_aprendizaje_jerarquico`). El análisis del último log (`simulacion_log_20250611_013230.txt`) confirmó el **éxito total**:

- El error de identificación desapareció.
- Las neuronas `G2_Concepto_1` ('Gato') y `G2_Concepto_4` ('Perro') fueron identificadas correctamente.
- La simulación avanzó a la FASE 2 y creó con éxito la neurona de abstracción `G3_Abstraccion_7` para representar el concepto 'Animal' a partir de la co-activación de las neuronas de 'Gato' y 'Perro'.

**La misión se ha completado con éxito.** El núcleo del simulador ahora funciona como se esperaba, demostrando un aprendizaje jerárquico autónomo y dinámico.

---

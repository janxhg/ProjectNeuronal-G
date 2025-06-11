# Informe de Depuración y Desarrollo del Simulador Neuronal

**Fecha:** 10 de Junio de 2025

## Resumen Ejecutivo

El objetivo de esta sesión de trabajo fue diagnosticar y resolver una serie de problemas críticos que impedían la ejecución completa del simulador de red neuronal. La simulación terminaba prematuramente durante la fase de entrenamiento del Grupo 1 (G1) sin generar errores explícitos, lo que dificultaba el diagnóstico. A través de un proceso iterativo de formulación de hipótesis, instrumentación del código con logs y análisis de resultados, se identificaron y corrigieron múltiples fallos en cascada. Los problemas iban desde errores de lógica en el algoritmo de entrenamiento hasta funciones incompletas y un manejo inadecuado del estado de los archivos. El resultado final es un simulador robusto y estable que completa todas las fases de entrenamiento y prueba (G1, G2, G3 y SFA) según lo diseñado, con un sistema de logging mejorado que permite una trazabilidad clara del flujo de ejecución.

---

## 1. Problema Inicial Identificado

La simulación se detenía de forma abrupta y silenciosa durante la fase de entrenamiento de G1. No se registraban excepciones ni mensajes de error en la consola o en los archivos de log, lo que sugería un cierre no gestionado del proceso.

---

## 2. Proceso de Diagnóstico y Depuración (Iterativo)

Se siguió un enfoque metódico para aislar y resolver el problema.

### Iteración 1: El Crash Silencioso

*   **Síntoma:** La ejecución del script `main_simulador.py` finalizaba sin completar el entrenamiento de G1 y sin ningún tipo de output de error.
*   **Hipótesis Inicial:** Existía un error lógico severo dentro de la función `entrenar_detector_secuencia` (en `logica_entrenamiento.py`), que es el núcleo del entrenamiento de G1. Este tipo de error (posiblemente un bucle infinito con una condición de salida errónea o un acceso inválido no protegido) podría estar causando que el intérprete de Python se cerrara sin pasar por el manejador de excepciones principal.
*   **Acción:** Se realizó una revisión exhaustiva de la función `entrenar_detector_secuencia`.
*   **Descubrimiento:** Se confirmó que la lógica para aplicar los estímulos y contar los pasos de la simulación era defectuosa, lo que llevaba a un estado inconsistente y al cierre inesperado.
*   **Solución:** Se reemplazó por completo el contenido de la función `entrenar_detector_secuencia` con una versión previamente validada, más robusta y con una lógica de simulación correcta.
*   **Resultado Parcial:** La simulación dejó de "crashear". Sin embargo, surgió un nuevo problema: ahora terminaba prematuramente pero de forma "limpia", justo después de entrenar al primer detector de secuencia.

### Iteración 2: La Terminación Prematura

*   **Síntoma:** La ejecución corría el entrenamiento para el primer detector de G1 (`N_Detector_Secuencia123`) y luego se detenía. No se ejecutaba el entrenamiento para los otros 5 detectores de G1 ni se pasaba a las fases de prueba o a las fases de G2/G3.
*   **Hipótesis:** La función orquestadora `run_training_phase` (en `training_phase.py`) estaba incompleta o contenía una declaración `return` prematura.
*   **Acción:** Se analizó el código de `run_training_phase`.
*   **Descubrimiento:** La función efectivamente estaba incompleta. Solo contenía el código para entrenar al primer detector y carecía de la lógica para los cinco restantes, además de no tener una declaración `return` explícita al final del flujo previsto. En Python, una función sin `return` devuelve `None`, lo que causaba que el programa principal dejara de ejecutarse correctamente.
*   **Solución:** Se reemplazó la función `run_training_phase` por su versión completa, que incluye los bucles de entrenamiento para los seis detectores de secuencia y una declaración `return` final que devuelve el estado actualizado de la simulación.

### Iteración 3: El Misterio del Log Faltante y el Estado Inconsistente

*   **Síntoma:** A pesar de la corrección anterior, un mensaje de log de diagnóstico que habíamos añadido en `main_simulador.py` (específicamente `"--- run_training_phase (G1) ha retornado... ---"`) seguía sin aparecer. Esto indicaba que, por alguna razón, el control no volvía correctamente desde `run_training_phase`.
*   **Hipótesis 1:** El programa terminaba tan rápido después de la función que el búfer del logger no tenía tiempo de escribir los últimos mensajes en el archivo.
*   **Hipótesis 2:** La función `run_training_phase` todavía tenía un problema lógico que impedía que llegara a su `return` final.
*   **Acción (para Hipótesis 1):** Se modificó `main_simulador.py` para incluir un bloque `try...finally` que asegurara la llamada a `logging.shutdown()`. Esta función fuerza el vaciado de todos los búferes de logging.
*   **Resultado:** El problema persistía. El log seguía sin aparecer, lo que debilitaba la Hipótesis 1 y reforzaba la Hipótesis 2.
*   **Acción (para Hipótesis 2):** Se decidió añadir un log de depuración (`logging.debug`) justo antes de la línea `return` dentro de `run_training_phase.py` para confirmar de manera inequívoca si se alcanzaba ese punto.
*   **Descubrimiento Crítico:** Al intentar aplicar este último cambio, se detectó que el archivo `training_phase.py` se encontraba en un estado inconsistente. Una edición anterior había fallado, resultando en código duplicado y la lógica de los detectores 4, 5 y 6 ubicada *después* de la declaración `return`, haciéndola inalcanzable.
*   **Solución Final:** Se realizó un reemplazo completo del archivo `src/main_parts/training_phase.py` con una versión final, limpia y verificada. Esta versión corregía el orden del código, importaba el módulo `logging` necesario y contenía el mensaje de depuración en la ubicación correcta.

---

## 3. Ejecución Final y Verificación

*   **Acción:** Se ejecutó el script `main_simulador.py` por última vez tras aplicar todas las correcciones.
*   **Resultado:** **Éxito total.** La simulación se ejecutó de principio a fin, completando todas las fases (Entrenamiento G1, Pruebas G1, Entrenamiento G2/G3, Pruebas G2/G3, Test de Inhibición y Test de SFA) y finalizando con un código de salida 0. Los logs generados mostraron todos los mensajes de diagnóstico esperados, incluyendo el `"--- A punto de retornar desde run_training_phase. ---"` y el `"--- run_training_phase (G1) ha retornado... ---"`, confirmando que el flujo de ejecución era el correcto.

---

## 4. Confirmación de la Lógica de Integración (G1, G2 -> G3)

Posterior a la depuración, se verificó la lógica de la neurona G3.

*   **Pregunta:** ¿Recibe la neurona G3 señales de G1 y G2?
*   **Análisis:** Se revisaron las llamadas a las funciones `run_training_phase_g3` y `run_testing_phase_g3` en `main_simulador.py`, y el contenido de dichas funciones en sus respectivos módulos.
*   **Conclusión:** Se confirmó que la arquitectura está diseñada explícitamente para que G3 integre señales de G1 y G2. El entrenamiento de G3 consiste en presentar una secuencia `Activación G1 -> Pausa -> Activación G2` para fortalecer, mediante STDP, las sinapsis de G1->G3 y G2->G3, haciendo que G3 se convierta en un detector de coincidencias temporales de alto nivel.

---

## 5. Lecciones Aprendidas

1.  **Depuración Sistemática:** La estrategia de formular hipótesis claras y realizar cambios pequeños y controlados para verificarlas fue fundamental para no perderse en la complejidad del problema.
2.  **Valor del Logging:** Los fallos silenciosos son de los más difíciles de depurar. El uso estratégico de mensajes de log en puntos clave del flujo de ejecución fue la herramienta principal para entender el comportamiento real del programa.
3.  **Gestión de Búferes:** En programas que pueden terminar abruptamente, es crucial asegurarse de que los búferes de E/S (como los de `logging`) se vacíen (`flush`/`shutdown`) para no perder información de diagnóstico vital.
4.  **Verificación de Estado:** Es importante verificar el estado de un archivo antes y después de realizar modificaciones programáticas para evitar introducir errores por un estado inconsistente.

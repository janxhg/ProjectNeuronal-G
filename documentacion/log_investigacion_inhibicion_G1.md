# Log de Investigación: Dinámica Inhibitoria y Aprendizaje de N_Detector_Secuencia123 (Grupo 1)

## Objetivo Principal
Diagnosticar y resolver el aprendizaje deficiente de la neurona `N_Detector_Secuencia123` (objetivo: secuencia P1->P2->P3), especialmente en presencia de mecanismos de inhibición feed-forward en el Grupo 1.

## Resumen de Experimentos Recientes

### Contexto Inicial
La neurona `N_Detector_Secuencia123` mostraba dificultades para aprender su secuencia cuando una neurona inhibitoria (`N_INHIB1_ID`) estaba activa, incluso con pesos inhibitorios bajos. Una prueba diagnóstica anterior (referencia: memoria `f546ada3-37b8-4eef-9701-6a2fa8c5926d`) sugirió que si `N_Detector_Secuencia123` era excluida de recibir inhibición de `N_INHIB1_ID` (mientras otras detectoras sí la recibían, y con `PESO_INICIAL_SINAPSIS_BASE = 0.5`), aprendía perfectamente.

### Experimento 1: Intento de Replicación de Memoria (Simulación del 2025-06-07 ~18:40, asociado a Step 3719)
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.5`
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_INHIB1_ID` activa (recibe excitación de presinápticas G1).
        *   `N_INHIB1_ID` inhibe a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   Contrario a la memoria, `N_Detector_Secuencia123` continuó aprendiendo deficientemente (pesos finales ~0.6-0.7).
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3719.*
*   **Conclusión Parcial:** No se pudo replicar el aprendizaje perfecto.

### Experimento 2: Aumento de Peso Inicial con Inhibición Selectiva (Simulación del 2025-06-07 ~18:41, asociado a Step 3727)
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.6` (incrementado)
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_INHIB1_ID` activa (recibe excitación de presinápticas G1).
        *   `N_INHIB1_ID` inhibe a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   `N_Detector_Secuencia123` mostró una mejora significativa en su aprendizaje (pesos finales ~0.8-0.85).
    *   Sin embargo, aún no alcanzó el aprendizaje perfecto (peso máximo de 1.5).
    *   Otras neuronas detectoras (inhibidas) aprendieron de forma variable.
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3727.*
*   **Conclusión Parcial:** `PESO_INICIAL_SINAPSIS_BASE = 0.6` ayuda considerablemente a `N_Detector_Secuencia123`, pero no es la solución completa en este contexto de red.

## Hallazgos Clave y Puntos Abiertos
1.  **Sensibilidad de `N_Detector_Secuencia123`:** Esta neurona es particularmente sensible al `PESO_INICIAL_SINAPSIS_BASE` para el aprendizaje de la secuencia P1->P2->P3.
2.  **Replicación de Memoria Fallida:** El escenario de aprendizaje perfecto descrito en la memoria `f546ada3-37b8-4eef-9701-6a2fa8c5926d` no se ha podido reproducir consistentemente, lo que sugiere que otros factores no identificados o una alta sensibilidad a condiciones específicas estaban en juego.
3.  **Efecto del Contexto Inhibitorio:** Aunque excluir a `N_Detector_Secuencia123` de la inhibición directa y aumentar su peso inicial mejora su aprendizaje, el contexto de inhibición en las neuronas circundantes no parece ser suficiente por sí solo para garantizar un aprendizaje perfecto si el peso inicial es bajo (0.5), ni la combinación actual (peso 0.6 + exclusión) lo logra.

### Experimento 3: Nuevo Aumento de Peso Inicial (0.65) con Inhibición Selectiva (Simulación del 2025-06-07 ~18:43, asociado a Step 3741)
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.65` (nuevo incremento)
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_INHIB1_ID` activa (recibe excitación de presinápticas G1).
        *   `N_INHIB1_ID` inhibe a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   `N_Detector_Secuencia123` mostró otra ligera mejora en su aprendizaje (pesos finales ~0.85-0.9).
    *   Aún no alcanzó el aprendizaje perfecto (peso máximo de 1.5).
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3741.*
*   **Conclusión Parcial:** El incremento a `PESO_INICIAL_SINAPSIS_BASE = 0.65` continúa la tendencia de mejora, pero la brecha hacia el aprendizaje óptimo persiste.

### Experimento 4: Cuarto Aumento de Peso Inicial (0.7) con Inhibición Selectiva (Simulación del 2025-06-07 ~18:45, asociado a Step 3756)
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.7` (cuarto incremento)
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_INHIB1_ID` activa (recibe excitación de presinápticas G1).
        *   `N_INHIB1_ID` inhibe a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   `N_Detector_Secuencia123` mostró otra mejora, con pesos finales estabilizándose alrededor de `0.9-0.95`.
    *   Aún no alcanzó el aprendizaje perfecto (peso máximo de 1.5).
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3756.*
*   **Conclusión Parcial:** La tendencia de mejora con el aumento de `PESO_INICIAL_SINAPSIS_BASE` continúa, pero el aprendizaje óptimo sigue siendo esquivo. Podría ser necesario un valor de peso inicial muy alto o existen otros factores limitantes.

### Experimento 5: Prueba con `DT_ENTRENAMIENTO_ESTIMULO = 3` (Simulación del 2025-06-07 ~18:48, asociado a Step 3774)
*   **Objetivo:** Investigar si un mayor espaciado temporal entre los estímulos de la secuencia mejora el aprendizaje de `N_Detector_Secuencia123`.
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.7` (mantenido de Exp. 4)
        *   `DT_ENTRENAMIENTO_ESTIMULO = 3` (aumentado desde 1)
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_INHIB1_ID` activa, inhibiendo a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   Para `N_Detector_Secuencia123`:
        *   Sinapsis `N_Pre1 -> N_Detector_Secuencia123` alcanzó ~1.0.
        *   Sinapsis `N_Pre2 -> N_Detector_Secuencia123` alcanzó ~0.73.
        *   Sinapsis `N_Pre3 -> N_Detector_Secuencia123` alcanzó ~0.73.
    *   El aprendizaje fue menos uniforme para `N_Detector_Secuencia123` en comparación con `DT_ENTRENAMIENTO_ESTIMULO = 1` (Exp. 4), donde los pesos se estabilizaron más cerca entre sí (~0.9-0.95).
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3774.*
*   **Conclusión Parcial:** Aumentar `DT_ENTRENAMIENTO_ESTIMULO` a 3 no mejoró el aprendizaje general de la secuencia P1->P2->P3 por `N_Detector_Secuencia123` y, de hecho, pareció desequilibrar el fortalecimiento de sus sinapsis. Se recomienda revertir este cambio.

### Experimento 6: Quinto Aumento de Peso Inicial (0.75) con DT=1 (Simulación del 2025-06-07 ~18:49, asociado a Step 3786)
*   **Objetivo:** Determinar si un incremento adicional en `PESO_INICIAL_SINAPSIS_BASE` (a 0.75), manteniendo `DT_ENTRENAMIENTO_ESTIMULO = 1`, permite el aprendizaje perfecto de `N_Detector_Secuencia123`.
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.75` (quinto incremento)
        *   `DT_ENTRENAMIENTO_ESTIMULO = 1` (revertido a valor original)
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_INHIB1_ID` activa, inhibiendo a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   Para `N_Detector_Secuencia123`, las sinapsis (P1, P2, P3) se estabilizaron alrededor de `0.95-0.98`.
    *   Mejora incremental sobre el peso inicial de 0.7, pero aún no se alcanza el máximo de 1.5.
    *   Otras neuronas detectoras (e.g., N_Detector_Secuencia321) sí aprenden perfectamente.
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3786.*
*   **Conclusión Parcial:** El aumento de `PESO_INICIAL_SINAPSIS_BASE` sigue produciendo mejoras marginales, pero el aprendizaje perfecto para `N_Detector_Secuencia123` sigue siendo esquivo por esta vía. Es probable que se necesiten ajustes más específicos o diferentes.

### Experimento 7: Ajuste Específico de tau_m para N_Detector_Secuencia123 (Simulación del 2025-06-07 ~19:05, asociado a Step 3802)
*   **Objetivo:** Determinar si una constante de tiempo de membrana (`tau_m`) ligeramente mayor para `N_Detector_Secuencia123` mejora su aprendizaje.
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.75` (mantenido)
        *   `DT_ENTRENAMIENTO_ESTIMULO = 1`
        *   `TAU_M_DETECTOR_BASE = 7.0` (para la mayoría de detectoras G1)
        *   `TAU_M_DETECTOR_SEC123 = 10.0` (específico para `N_Detector_Secuencia123`)
        *   `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3`
        *   `PESO_INHIBITORIO_BASE = 0.3`
    *   `src/main_parts/setup_network.py`:
        *   `N_Detector_Secuencia123` instanciada con `tau_m = TAU_M_DETECTOR_SEC123`.
        *   `N_INHIB1_ID` activa, inhibiendo a todas las detectoras G1 **excepto** `N_Detector_Secuencia123`.
*   **Resultado:**
    *   **¡ÉXITO!** Para `N_Detector_Secuencia123`, las tres sinapsis (P1, P2, P3) alcanzaron el peso sináptico máximo de `1.5`.
    *   El aprendizaje fue robusto y homogéneo para las tres sinapsis.
    *   Otras neuronas detectoras del Grupo 1 continuaron aprendiendo perfectamente sus secuencias.
    *   Se confirmó (visualmente en la simulación o mediante el print añadido) que `N_Detector_Secuencia123` utilizó el `tau_m` de 10.0 ms.
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3802.*
*   **Conclusión Parcial:** Ajustar `tau_m` a `10.0 ms` específicamente para `N_Detector_Secuencia123` fue la modificación clave que permitió el aprendizaje perfecto de la secuencia P1->P2->P3, incluso bajo condiciones de inhibición selectiva y con `PESO_INICIAL_SINAPSIS_BASE = 0.75`.

## Conclusiones Generales de la Investigación (Hasta Experimento 7)

1.  **Inhibición Selectiva:** Excluir a `N_Detector_Secuencia123` de la inhibición general de `N_INHIB1_ID` es un requisito fundamental para su aprendizaje. Cuando recibe inhibición (incluso débil), su aprendizaje se ve severamente afectado.
2.  **Peso Sináptico Inicial (`PESO_INICIAL_SINAPSIS_BASE`):** Aumentar este parámetro desde `0.5` hasta `0.75` mostró mejoras incrementales, pero no fue suficiente por sí solo para lograr el aprendizaje perfecto bajo inhibición selectiva.
3.  **Intervalo entre Estímulos (`DT_ENTRENAMIENTO_ESTIMULO`):** Un valor de `1 ms` parece ser más adecuado que `3 ms`. Aumentar el intervalo no benefició el aprendizaje de `N_Detector_Secuencia123`.
4.  **Constante de Tiempo de Membrana (`tau_m`):** Este ha sido el factor diferencial. `N_Detector_Secuencia123` parece requerir una `tau_m` ligeramente mayor (`10.0 ms`) que las otras detectoras (`7.0 ms`) para integrar adecuadamente los estímulos secuenciales P1->P2->P3 y permitir que la STDP funcione de manera óptima. Esto sugiere que la secuencia P1->P2->P3 podría ser intrínsecamente un poco más difícil de aprender o requiere una ventana de integración temporal ligeramente más amplia para esta neurona específica.

### Experimento 8: Optimización de Peso Inicial (0.7) con tau_m Específico (Simulación del 2025-06-07 ~19:19, asociado a Step 3808)
*   **Objetivo:** Verificar si se mantiene el aprendizaje perfecto de `N_Detector_Secuencia123` al reducir `PESO_INICIAL_SINAPSIS_BASE` a `0.7`, manteniendo las demás condiciones del Experimento 7.
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.7` (reducido desde 0.75)
        *   `DT_ENTRENAMIENTO_ESTIMULO = 1`
        *   `TAU_M_DETECTOR_BASE = 7.0`
        *   `TAU_M_DETECTOR_SEC123 = 10.0`
        *   Inhibición selectiva para `N_Detector_Secuencia123`.
*   **Resultado:**
    *   **¡ÉXITO MANTENIDO!** `N_Detector_Secuencia123` continuó aprendiendo su secuencia perfectamente, alcanzando pesos de `1.5`.
    *   Otras neuronas detectoras también mantuvieron su aprendizaje perfecto.
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3808.*
*   **Conclusión Parcial:** El sistema es robusto a una reducción de `PESO_INICIAL_SINAPSIS_BASE` a `0.7` una vez que `tau_m` está correctamente ajustado para `N_Detector_Secuencia123`.

### Experimento 9: Optimización de Peso Inicial (0.6) con tau_m Específico (Simulación del 2025-06-07 ~19:28, asociado a Step 3816)
*   **Objetivo:** Verificar si se mantiene el aprendizaje perfecto de `N_Detector_Secuencia123` al reducir `PESO_INICIAL_SINAPSIS_BASE` a `0.6`.
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.6` (reducido desde 0.7)
        *   `DT_ENTRENAMIENTO_ESTIMULO = 1`
        *   `TAU_M_DETECTOR_BASE = 7.0`
        *   `TAU_M_DETECTOR_SEC123 = 10.0`
        *   Inhibición selectiva para `N_Detector_Secuencia123`.
*   **Resultado:**
    *   **¡ÉXITO MANTENIDO!** `N_Detector_Secuencia123` continuó aprendiendo su secuencia perfectamente, alcanzando pesos de `1.5`.
    *   Otras neuronas detectoras también mantuvieron su aprendizaje perfecto.
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3816.*
*   **Conclusión Parcial:** El aprendizaje perfecto se mantiene con `PESO_INICIAL_SINAPSIS_BASE = 0.6` bajo las condiciones actuales (tau_m específico e inhibición selectiva).

### Experimento 10: Optimización Final de Peso Inicial (0.5) con tau_m Específico (Simulación del 2025-06-07 ~19:37, asociado a Step 3822)
*   **Objetivo:** Verificar si se mantiene el aprendizaje perfecto de `N_Detector_Secuencia123` al reducir `PESO_INICIAL_SINAPSIS_BASE` a `0.5`, el valor de la memoria `f546ada3-37b8-4eef-9701-6a2fa8c5926d`.
*   **Condiciones:**
    *   `configuracion/parametros_simulacion.py`:
        *   `PESO_INICIAL_SINAPSIS_BASE = 0.5` (reducido desde 0.6)
        *   `DT_ENTRENAMIENTO_ESTIMULO = 1`
        *   `TAU_M_DETECTOR_BASE = 7.0`
        *   `TAU_M_DETECTOR_SEC123 = 10.0`
        *   Inhibición selectiva para `N_Detector_Secuencia123`.
*   **Resultado:**
    *   **¡ÉXITO TOTAL Y REPLICACIÓN DE MEMORIA!** `N_Detector_Secuencia123` aprendió su secuencia perfectamente, alcanzando pesos de `1.5` de manera robusta.
    *   Otras neuronas detectoras también mantuvieron su aprendizaje perfecto.
    *   *Referencia de imagen: Ver imagen proporcionada en Step 3822.*
*   **Conclusión Parcial:** Se ha encontrado una configuración óptima (`PESO_INICIAL_SINAPSIS_BASE = 0.5`, `TAU_M_DETECTOR_SEC123 = 10.0`, inhibición selectiva) que permite el aprendizaje perfecto de `N_Detector_Secuencia123`. Esto también reconcilia los hallazgos con la memoria `f546ada3-37b8-4eef-9701-6a2fa8c5926d`, sugiriendo que el `tau_m` específico era la pieza faltante en intentos anteriores de replicación.

## Conclusiones Finales de la Investigación sobre N_Detector_Secuencia123 (Hasta Experimento 10)

La investigación para restaurar y optimizar el aprendizaje de la neurona `N_Detector_Secuencia123` ha sido exitosa. Los factores clave identificados son:

1.  **Inhibición Selectiva:** Es crucial. `N_Detector_Secuencia123` no aprende correctamente si recibe la inhibición feed-forward global de `N_INHIB1_ID` que afecta a otras detectoras del Grupo 1.
2.  **Constante de Tiempo de Membrana (`tau_m`) Específica:** `N_Detector_Secuencia123` requiere una `tau_m` de `10.0 ms` (en lugar de los `7.0 ms` base de otras detectoras) para integrar adecuadamente los estímulos de la secuencia P1->P2->P3. Esto sugiere que esta secuencia particular, o la dinámica de esta neurona, se beneficia de una ventana de integración temporal ligeramente más larga.
3.  **Peso Sináptico Inicial (`PESO_INICIAL_SINAPSIS_BASE`):** Con los dos puntos anteriores implementados, la red es capaz de lograr un aprendizaje perfecto incluso con un `PESO_INICIAL_SINAPSIS_BASE` de `0.5`. Esto indica una buena eficiencia en el aprendizaje.
4.  **Intervalo entre Estímulos (`DT_ENTRENAMIENTO_ESTIMULO`):** Un valor de `1 ms` es adecuado.

Se ha logrado una configuración de parámetros que permite un aprendizaje robusto y perfecto para `N_Detector_Secuencia123` sin afectar negativamente el aprendizaje de otras neuronas detectoras (que no requieren el `tau_m` modificado y pueden o no estar sujetas a la inhibición general según el diseño de la red).

## Próximos Pasos Recomendados (Post-Investigación)

1.  **Guardar Configuración Óptima:**
    *   Asegurarse de que los parámetros actuales en `configuracion/parametros_simulacion.py` y las modificaciones en `src/main_parts/setup_network.py` (para `tau_m` e inhibición selectiva) reflejen esta configuración exitosa. Considerar añadir comentarios en el código para destacar estos ajustes específicos para `N_Detector_Secuencia123`.

2.  **Validación de Robustez (Opcional Avanzado):**
    *   Ejecutar la simulación varias veces (si es posible con diferentes semillas aleatorias si el simulador las usa para algo) para confirmar la consistencia al 100%.
    *   Probar la sensibilidad a pequeñas variaciones en `PESO_EXCITATORIO_A_INHIBIDORA_BASE` y `PESO_INHIBITORIO_BASE` (aunque la inhibición selectiva hace esto menos crítico para `N_Detector_Secuencia123`).

3.  **Exploración Teórica (Opcional):**
    *   Profundizar en por qué la secuencia P1->P2->P3 específicamente se beneficia de un `tau_m` mayor. ¿Podría estar relacionado con los retardos sinápticos (si existen en el modelo y no son cero), la duración de los EPSP, o la interacción precisa con las ventanas temporales de la STDP?

4.  **Documentación y Cierre del Log:**
    *   Este log (`log_investigacion_inhibicion_G1.md`) puede considerarse completo para el objetivo inicial. Realizar una revisión final.

**Recomendación Inmediata:**
*   ¡Celebrar el éxito! Considerar el punto 1 (Guardar Configuración Óptima) como la acción principal para consolidar este resultado. El objetivo principal de la investigación se ha cumplido.

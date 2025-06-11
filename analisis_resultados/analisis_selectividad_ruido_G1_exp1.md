# Análisis de Selectividad de Detectores G1 Bajo Ruido (N_Detector_Secuencia123)

Fecha de Análisis: 2025-06-08

## 1. Objetivo

El objetivo principal de este análisis es investigar y mejorar la robustez y selectividad del detector de secuencias `N_Detector_Secuencia123` (objetivo: P1->P2->P3) bajo condiciones de entrada con ruido. Se busca reducir los falsos positivos (disparos para secuencias no objetivo) manteniendo una alta tasa de verdaderos positivos (disparos para su secuencia objetivo).

## 2. Rendimiento de Línea Base (Pre-Ajustes)

Los parámetros de simulación iniciales relevantes para la selectividad en la fase de prueba eran:
- `DELTA_UMBRAL_PRUEBA_BASE = 2.60 mV`
- `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV`

El rendimiento de los detectores G1 con estos parámetros, según el análisis del log `simulacion_log_20250608_142735.txt` (referencia: Memoria Cascade ID `4ea0f096-72eb-4969-8c7e-ea3bacdac6d0`), fue el siguiente en las pruebas CON RUIDO:

| Detector                | Sec. Objetivo | TP | FP | FN | TN | Falsos Positivos Específicos (Secuencia -> Disparo) |
|-------------------------|---------------|----|----|----|----|---------------------------------------------------|
| N_Detector_Secuencia123 | 1->2->3       | 1  | 1  | 0  | 4  | 3->1->2                                           |
| N_Detector_Secuencia321 | 3->2->1       | 1  | 1  | 0  | 4  | (FP presente)                                     |
| N_Detector_Secuencia132 | 1->3->2       | 1  | 1  | 0  | 4  | (FP presente)                                     |
| N_Detector_Secuencia213 | 2->1->3       | 1  | 2  | 0  | 3  | (FPs presentes)                                   |
| N_Detector_Secuencia231 | 2->3->1       | 1  | 0  | 0  | 5  | Ninguno (Perfecto)                                |
| N_Detector_Secuencia312 | 3->1->2       | 1  | 1  | 0  | 4  | (FP presente)                                     |

**Foco:** `N_Detector_Secuencia123` presentaba 1 falso positivo para la secuencia 3->1->2.

## 3. Experimento 1: Incremento de `AJUSTE_SELECTIVIDAD_PRUEBA`

Fecha del Experimento: 2025-06-08

### 3.1. Hipótesis
Incrementar el parámetro `AJUSTE_SELECTIVIDAD_PRUEBA` aumentaría el umbral de disparo para secuencias no objetivo, reduciendo así los falsos positivos de `N_Detector_Secuencia123` sin afectar su capacidad de detectar la secuencia correcta.

### 3.2. Cambio Realizado
- `AJUSTE_SELECTIVIDAD_PRUEBA` se modificó de `1.65 mV` a `1.80 mV` en `configuracion/parametros_simulacion.py`.

### 3.3. Simulación y Log
Se ejecutó una nueva simulación, generando el log: `logs/simulacion_log_20250608_143407.txt`.

### 3.4. Resultados (CON RUIDO)
El análisis del resumen "CON RUIDO" del log `simulacion_log_20250608_143407.txt` arrojó los siguientes resultados:

| Detector                | Sec. Objetivo | TP | FP | FN | TN | Falsos Positivos Específicos (Secuencia -> Disparo) |
|-------------------------|---------------|----|----|----|----|---------------------------------------------------|
| N_Detector_Secuencia123 | 1->2->3       | 1  | 2  | 0  | 3  | 3->2->1, 2->3->1                                  |
| N_Detector_Secuencia321 | 3->2->1       | 1  | 1  | 0  | 4  | 1->2->3                                           |
| N_Detector_Secuencia132 | 1->3->2       | 1  | 0  | 0  | 5  | Ninguno                                           |
| N_Detector_Secuencia213 | 2->1->3       | 1  | 0  | 0  | 5  | Ninguno                                           |
| N_Detector_Secuencia231 | 2->3->1       | 1  | 1  | 0  | 4  | 3->1->2                                           |
| N_Detector_Secuencia312 | 3->1->2       | 1  | 0  | 0  | 5  | Ninguno                                           |

*(Nota: TP=Verdadero Positivo, FP=Falso Positivo, FN=Falso Negativo, TN=Verdadero Negativo. Cada detector se prueba contra 6 secuencias distintas; 1 objetivo y 5 no objetivo).*

### 3.5. Conclusión del Experimento 1
- Para `N_Detector_Secuencia123`: El incremento de `AJUSTE_SELECTIVIDAD_PRUEBA` fue contraproducente. El número de falsos positivos aumentó de 1 a 2.
- Para otros detectores:
    - `N_Detector_Secuencia132`, `N_Detector_Secuencia213`, `N_Detector_Secuencia312`: Mejoraron, reduciendo sus FPs a 0.
    - `N_Detector_Secuencia321`: Mantuvo 1 FP.
    - `N_Detector_Secuencia231`: Empeoró, pasando de 0 FPs a 1 FP.

El ajuste global de este parámetro no es una solución selectiva para `N_Detector_Secuencia123` y tiene efectos mixtos en la red.

### 3.6. Reversión del Cambio (Post-Experimento 1)
Debido a los resultados negativos para `N_Detector_Secuencia123`, el parámetro `AJUSTE_SELECTIVIDAD_PRUEBA` fue revertido a su valor original de `1.65 mV` (confirmado el 2025-06-08).

## 4. Experimento 2: Reducción de `PESO_EXCITATORIO_A_INHIBIDORA_BASE`

Fecha del Experimento: 2025-06-08

### 4.1. Hipótesis
Reducir `PESO_EXCITATORIO_A_INHIBIDORA_BASE` (de `0.3` a `0.25`) haría que la neurona inhibitoria `N_INHIB1_ID` sea menos sensible a la actividad de las neuronas presinápticas. Esto podría llevar a una menor activación de `N_INHIB1_ID` durante la presentación de secuencias con ruido, alterando la dinámica de inhibición sobre las otras neuronas detectoras G1. Este cambio en la actividad inhibitoria podría, indirectamente, mejorar la selectividad de `N_Detector_Secuencia123`.

### 4.2. Parámetros Clave al Inicio del Experimento
- `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV` (valor base)
- `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3` (valor base antes de este experimento)
- `PESO_INHIBITORIO_BASE = 0.3`

### 4.3. Cambio Realizado
- `PESO_EXCITATORIO_A_INHIBIDORA_BASE` se modificó de `0.3` a `0.25` en `configuracion/parametros_simulacion.py`.

### 4.4. Simulación y Log
Se ejecutó una nueva simulación, generando el log: `logs/simulacion_log_20250608_144204.txt`.

### 4.5. Resultados (CON RUIDO)
El análisis del resumen "CON RUIDO" del log `simulacion_log_20250608_144204.txt` arrojó los siguientes resultados:

| Detector                | Sec. Objetivo | TP | FP | FN | TN | Falsos Positivos Específicos (Secuencia -> Disparo) |
|-------------------------|---------------|----|----|----|----|---------------------------------------------------|
| N_Detector_Secuencia123 | 1->2->3       | 1  | 1  | 0  | 4  | 3->2->1                                           |
| N_Detector_Secuencia321 | 3->2->1       | 1  | 1  | 0  | 4  | 1->2->3                                           |
| N_Detector_Secuencia132 | 1->3->2       | 1  | 2  | 0  | 3  | (FPs presentes)                                   |
| N_Detector_Secuencia213 | 2->1->3       | 1  | 1  | 0  | 4  | (FP presente)                                     |
| N_Detector_Secuencia231 | 2->3->1       | 1  | 2  | 0  | 3  | (FPs presentes)                                   |
| N_Detector_Secuencia312 | 3->1->2       | 1  | 1  | 0  | 4  | (FP presente)                                     |

### 4.6. Conclusión del Experimento 2
- Para `N_Detector_Secuencia123`: El número de falsos positivos se mantuvo en 1, pero la secuencia específica que lo causa cambió de 3->1->2 (línea base) a 3->2->1. El cambio no eliminó el problema.
- Para otros detectores:
    - `N_Detector_Secuencia132`: Empeoró (1 FP a 2 FPs).
    - `N_Detector_Secuencia213`: Mejoró (2 FPs a 1 FP).
    - `N_Detector_Secuencia231`: Empeoró significativamente (0 FPs a 2 FPs).
    - `N_Detector_Secuencia321` y `N_Detector_Secuencia312`: Mantuvieron 1 FP.

Reducir la sensibilidad de `N_INHIB1_ID` no mejoró la selectividad de `N_Detector_Secuencia123` y tuvo efectos mixtos/negativos en el resto de la red.

### 4.7. Reversión del Cambio (Post-Experimento 2)
Debido a los resultados, el parámetro `PESO_EXCITATORIO_A_INHIBIDORA_BASE` fue revertido a su valor original de `0.3` (confirmado el 2025-06-08).

## 5. Experimento 3: Incremento de `PESO_EXCITATORIO_A_INHIBIDORA_BASE`

Fecha del Experimento: 2025-06-08

### 5.1. Hipótesis
Incrementar `PESO_EXCITATORIO_A_INHIBIDORA_BASE` (de `0.3` a `0.35`) haría que la neurona inhibitoria `N_INHIB1_ID` sea *más* sensible a la actividad de las neuronas presinápticas. Una mayor activación de `N_INHIB1_ID` podría resultar en una inhibición más fuerte o más oportuna sobre las neuronas detectoras G1, lo que podría ayudar a suprimir los disparos para secuencias no objetivo (falsos positivos), especialmente para `N_Detector_Secuencia123`.

### 5.2. Parámetros Clave al Inicio del Experimento
- `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV` (valor base)
- `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.3` (valor base antes de este experimento)
- `PESO_INHIBITORIO_BASE = 0.3`

### 5.3. Cambio Realizado
- `PESO_EXCITATORIO_A_INHIBIDORA_BASE` se modificó de `0.3` a `0.35` en `configuracion/parametros_simulacion.py`.

### 5.4. Simulación y Log
Se ejecutó una nueva simulación, generando el log: `logs/simulacion_log_20250608_144758.txt`.

### 5.5. Resultados (CON RUIDO)
El análisis del resumen "CON RUIDO" del log `simulacion_log_20250608_144758.txt` arrojó los siguientes resultados:

| Detector                | Sec. Objetivo | TP | FP | FN | TN | Falsos Positivos Específicos (Secuencia -> Disparo) |
|-------------------------|---------------|----|----|----|----|---------------------------------------------------|
| N_Detector_Secuencia123 | 1->2->3       | 1  | 0  | 0  | 5  | Ninguno (Perfecto)                                |
| N_Detector_Secuencia321 | 3->2->1       | 1  | 2  | 0  | 3  | 1->2->3, 2->1->3                                  |
| N_Detector_Secuencia132 | 1->3->2       | 1  | 1  | 0  | 4  | 2->3->1                                           |
| N_Detector_Secuencia213 | 2->1->3       | 1  | 3  | 0  | 2  | 3->2->1, 1->3->2, 3->1->2                         |
| N_Detector_Secuencia231 | 2->3->1       | 1  | 0  | 0  | 5  | Ninguno (Perfecto)                                |
| N_Detector_Secuencia312 | 3->1->2       | 1  | 0  | 0  | 5  | Ninguno (Perfecto)                                |

### 5.6. Conclusión del Experimento 3
- Para `N_Detector_Secuencia123`: **Éxito**. El número de falsos positivos se redujo de 1 a 0. El detector ahora muestra un rendimiento perfecto (1 TP, 0 FP) bajo ruido.
- Para otros detectores:
    - `N_Detector_Secuencia231` y `N_Detector_Secuencia312`: También alcanzaron un rendimiento perfecto (0 FPs).
    - `N_Detector_Secuencia321`: Empeoró, pasando de 1 FP (línea base) a 2 FPs.
    - `N_Detector_Secuencia132`: Se mantuvo con 1 FP (igual que la línea base).
    - `N_Detector_Secuencia213`: Empeoró significativamente, pasando de 2 FPs (línea base) a 3 FPs.

Aumentar la sensibilidad de `N_INHIB1_ID` (vía `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`) fue altamente efectivo para `N_Detector_Secuencia123` y benefició a otros dos detectores. Sin embargo, degradó el rendimiento de dos detectores. El número total de FPs en la red (6) se mantuvo igual que la línea base, pero la distribución cambió, favoreciendo al detector objetivo.

### 5.7. Consideraciones y Próximos Pasos (Post-Experimento 3)
Dado el éxito con `N_Detector_Secuencia123`, este ajuste de `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35` es un candidato fuerte para ser mantenido si el foco principal es ese detector.

Próximos pasos podrían incluir:
1.  Mantener `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35` y ahora experimentar con `PESO_INHIBITORIO_BASE` (actualmente `0.3`) para ver si se puede mejorar la selectividad de los detectores que empeoraron (`N_Detector_Secuencia321`, `N_Detector_Secuencia213`) sin afectar negativamente a los que mejoraron.
2.  Considerar si el rendimiento global de la red (6 FPs totales) es aceptable, o si se necesita un ajuste más fino o un enfoque diferente para los detectores problemáticos.


## 6. Experimento 4: Incremento de `PESO_INHIBITORIO_BASE` (manteniendo `PESO_EXCITATORIO_A_INHIBIDORA_BASE`)

Fecha del Experimento: 2025-06-08

### 6.1. Hipótesis
Incrementar `PESO_INHIBITORIO_BASE` (de `0.3` a `0.35`), manteniendo `PESO_EXCITATORIO_A_INHIBIDORA_BASE` en `0.35` (del Experimento 3), aumentaría la fuerza de la inhibición desde `N_INHIB1_ID` hacia las neuronas detectoras G1. Esto podría suprimir aún más los falsos positivos, idealmente mejorando la selectividad de los detectores que empeoraron en el Experimento 3 (`N_Detector_Secuencia321`, `N_Detector_Secuencia213`) sin afectar negativamente a `N_Detector_Secuencia123`.

### 6.2. Parámetros Clave al Inicio del Experimento
- `AJUSTE_SELECTIVIDAD_PRUEBA = 1.65 mV` (valor base)
- `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35` (mantenido del Experimento 3)
- `PESO_INHIBITORIO_BASE = 0.3` (antes de este experimento)

### 6.3. Cambio Realizado
- `PESO_INHIBITORIO_BASE` se modificó de `0.3` a `0.35` en `configuracion/parametros_simulacion.py`.

### 6.4. Simulación y Log
Se ejecutó una nueva simulación, generando el log: `logs/simulacion_log_20250608_151009.txt`.

### 6.5. Resultados (CON RUIDO)
El análisis del resumen "CON RUIDO" del log `simulacion_log_20250608_151009.txt` arrojó los siguientes resultados:

| Detector                | Sec. Objetivo | TP | FP | FN | TN | Falsos Positivos Específicos (Secuencia -> Disparo) |
|-------------------------|---------------|----|----|----|----|---------------------------------------------------|
| N_Detector_Secuencia123 | 1->2->3       | 1  | 4  | 0  | 1  | 3->2->1, 1->3->2, 2->3->1, 3->1->2                  |
| N_Detector_Secuencia321 | 3->2->1       | 1  | 2  | 0  | 3  | 1->3->2, 2->3->1                                  |
| N_Detector_Secuencia132 | 1->3->2       | 1  | 2  | 0  | 3  | 2->3->1, 3->1->2                                  |
| N_Detector_Secuencia213 | 2->1->3       | 1  | 1  | 0  | 4  | 1->3->2                                           |
| N_Detector_Secuencia231 | 2->3->1       | 1  | 1  | 0  | 4  | 1->2->3                                           |
| N_Detector_Secuencia312 | 3->1->2       | 1  | 0  | 0  | 5  | Ninguno (Perfecto)                                |

### 6.6. Conclusión del Experimento 4
- Para `N_Detector_Secuencia123`: **Empeoró drásticamente**. El número de falsos positivos aumentó de 0 (en Experimento 3) a 4.
- Para otros detectores:
    - `N_Detector_Secuencia321`: Se mantuvo con 2 FPs (igual que Experimento 3).
    - `N_Detector_Secuencia132`: Empeoró, pasando de 1 FP (Experimento 3) a 2 FPs.
    - `N_Detector_Secuencia213`: Mejoró, pasando de 3 FPs (Experimento 3) a 1 FP.
    - `N_Detector_Secuencia231`: Empeoró, pasando de 0 FPs (Experimento 3) a 1 FP.
    - `N_Detector_Secuencia312`: Mantuvo su rendimiento perfecto (0 FPs).
- El número total de FPs en la red aumentó de 6 (en Experimento 3) a 10.
- Incrementar `PESO_INHIBITORIO_BASE` a `0.35` (con `PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`) fue perjudicial para la selectividad general y especialmente para `N_Detector_Secuencia123`.

### 6.7. Consideraciones y Próximos Pasos (Post-Experimento 4)
- Debido a los resultados negativos, el parámetro `PESO_INHIBITORIO_BASE` debería ser revertido a `0.3` en `configuracion/parametros_simulacion.py`.
- Los parámetros del Experimento 3 (`PESO_EXCITATORIO_A_INHIBIDORA_BASE = 0.35`, `PESO_INHIBITORIO_BASE = 0.3`) parecen ser los mejores hasta ahora para `N_Detector_Secuencia123` (0 FPs) y ofrecen un total de 6 FPs en la red.
- Se debe decidir si se revierte a la configuración del Experimento 3 y se considera finalizada esta línea de ajuste, o si se exploran otros parámetros (ej. `AJUSTE_SELECTIVIDAD_PRUEBA`) o estrategias para los detectores que aún presentan FPs en la configuración del Experimento 3.


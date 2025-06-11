# Plan de Implementación: Generalización y Autoorganización Neuronal

## 1. Objetivo

Evolucionar el simulador de una red que aprende patrones fijos a una que puede **generalizar**, creando **conceptos abstractos** a partir de la estadística de sus entradas. El objetivo es que la red se organice a sí misma, decidiendo cuándo y cómo crear nuevas neuronas para representar conocimiento de nivel superior.

## 2. Mecanismo Propuesto: El "Gestor de Plasticidad"

Se creará una nueva clase, `GestorPlasticidad`, que operará a nivel de toda la red (`RedDinamica`). Este gestor no es una neurona, sino un supervisor que monitorea la actividad y aplica reglas de desarrollo.

### Fase 1: El Observador - Registro de Actividad

- **Tarea:** El `GestorPlasticidad` registrará cada vez que una neurona de tipo `G1` dispare.
- **Implementación:** Mantendrá un diccionario donde las claves son los IDs de las neuronas `G1` y los valores son listas de timestamps de sus disparos.
  ```python
  # Ejemplo de estado interno del Gestor
  self.historial_disparos_g1 = {
      'G1_A_hola': [10, 25, 60],
      'G1_B_que_tal': [11, 26, 62],
      'G1_C_adios': [45, 80]
  }
  ```

### Fase 2: El Analista - Detección de Co-ocurrencias

- **Tarea:** Periódicamente, el `Gestor` analizará su historial para encontrar pares de neuronas `G1` que tienden a disparar juntas en una ventana de tiempo.
- **Implementación:** Se definirá un `UMBRAL_COOCURRENCIA` (ej. 3 veces) y una `VENTANA_TEMPORAL_ASOCIACION` (ej. 5 pasos de tiempo). Si dos neuronas `G1` cumplen esta condición, se consideran candidatas para la generalización.

### Fase 3: El Creador - Nacimiento de una Neurona Conceptual (G2)

- **Tarea:** Cuando se detecta un par de `G1`s fuertemente correlacionadas, el `Gestor` creará una nueva neurona `G2`.
- **Implementación:**
    1. Se instancia una nueva `NeuronaG2` con un ID único (ej. `G2_Concepto_1`).
    2. Se agrega esta neurona a la `RedDinamica`.
    3. El `Gestor` ordena a la `RedDinamica` que cree conexiones desde las `G1`s originales hacia la nueva `G2`.
    4. **Resultado:** Esta `G2` ahora representa el concepto abstracto que une a las `G1`s. Disparará si cualquiera de ellas dispara, logrando la generalización.

### Fase 4: Optimización y Limpieza (Avanzado)

- **Poda de Memoria:** El `Gestor` limpiará su propio historial de disparos periódicamente para mantenerse eficiente.
- **Poda de Conexiones (Opcional):** Se podría experimentar con debilitar ligeramente las conexiones directas que las `G1` tenían a otras partes de la red, favoreciendo el nuevo camino a través de la `G2` conceptual.

## 3. Parámetros a Añadir en `parametros_simulacion.py`

- `ACTIVAR_GESTION_PLASTICIDAD` (bool)
- `UMBRAL_COOCURRENCIA` (int)
- `VENTANA_TEMPORAL_ASOCIACION` (int)

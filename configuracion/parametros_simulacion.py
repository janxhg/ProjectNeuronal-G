# -*- coding: utf-8 -*-
"""
Archivo de configuración centralizado para todos los parámetros del simulador.
Esto permite un ajuste fácil y rápido del comportamiento de la red sin
modificar el código fuente principal.
"""

# --- Parámetros de Plasticidad Sináptica ---

# Factor para el ajuste de pesos sinápticos según la regla de Hebb.
# Un valor positivo refuerza la conexión que contribuyó a un disparo.
FACTOR_APRENDIZAJE_HEBBIANO = 0.1

# Activa o desactiva la poda sináptica (debilitamiento pasivo de conexiones).
ACTIVAR_PODA_SINAPTICA = True

# Factor de decaimiento pasivo. Se aplica a todas las sinapsis en cada paso.
# Debe ser un valor negativo pequeño para un olvido gradual.
FACTOR_PODA_SINAPTICA = -0.005

# El peso mínimo que puede tener una sinapsis. Evita que se borren por completo,
# permitiendo que el conocimiento quede latente.
PESO_MINIMO_SINAPTICO = 0.01

# El peso máximo que puede alcanzar una sinapsis. Limita el crecimiento para
# mantener la estabilidad de la red.
PESO_MAXIMO_SINAPTICO = 5.0


# --- Parámetros de Autoorganización y Generalización ---

# Activa/desactiva el Gestor de Plasticidad que crea neuronas dinámicamente.
ACTIVAR_GESTION_PLASTICIDAD = True

# Número de veces que dos neuronas G1 deben disparar juntas (en una ventana de tiempo)
# para ser consideradas un concepto y generar una neurona G2 que las represente.
UMBRAL_COOCURRENCIA = 2

# Ventana de tiempo (en pasos de simulación) para considerar que dos disparos son "juntos".
VENTANA_TEMPORAL_ASOCIACION = 5


# --- Parámetros de la Arquitectura de Neuronas Especializadas ---

# Ventana temporal para que una NeuronaG2 detecte la co-ocurrencia de sus dos inputs.
TIEMPO_ENTRE_EVENTOS_G2 = 5

# Ventana temporal para que una NeuronaG3 detecte la activación de sus inputs (G1 y G2).
TIEMPO_ENTRE_EVENTOS_G3 = 10


# --- Parámetros de las Demostraciones y Experimentos ---

# Intensidad base para los impulsos externos aplicados a las neuronas.
INTENSIDAD_ESTIMULO = 1.0

# Frecuencia de actualización del gráfico (cada N pasos de simulación).
VISUALIZADOR_FRECUENCIA_ACTUALIZACION = 5

# Tiempo de espera (en segundos) antes de cerrar la ventana de visualización al final.
TIEMPO_CIERRE_VISUALIZADOR = 15

# Pasos de simulación para permitir que la red se estabilice después de un estímulo.
PASOS_ESTABILIZACION = 10

# Pasos de simulación para permitir que el Gestor de Plasticidad actúe (período de "reflexión").
PASOS_REFLEXION = 20

# --- Demo: Auto-organización ---
DEMO_AUTO_NUM_ESTIMULOS = 4 # Número de veces que se presenta el estímulo 'pájaro'.

# --- Demo: Red Compleja ---
DEMO_COMPLEJA_NUM_PASOS_SIMULACION = 200
DEMO_COMPLEJA_PROBABILIDAD_EXPERIENCIA = 0.2 # Probabilidad en cada paso de que ocurra una experiencia.

# --- Demo: Aprendizaje Jerárquico ---
DEMO_JERARQUICO_NUM_CICLOS_G2 = 8
DEMO_JERARQUICO_NUM_CICLOS_G3 = 8
DEMO_JERARQUICO_PASOS_SIMULACION_POR_CICLO = 15
DEMO_JERARQUICO_PASOS_CONSOLIDACION_G2 = 30

# Mínimo de conexiones que debe tener una neurona G2 candidata para ser considerada
# la representante de un concepto.
MIN_CONEXIONES_REQUERIDAS_G2 = 1

# --- Demo: Recurrencia y Memoria ---
DEMO_RECURRENCIA_PESO_ENTRANTE = 1.5
DEMO_RECURRENCIA_PESO_RECURRENTE = 1.1
DEMO_RECURRENCIA_PASOS_SIMULACION = 20
DEMO_RECURRENCIA_TIEMPO_ESPERA_INICIAL_S = 2
DEMO_RECURRENCIA_TIEMPO_ESPERA_PASO_S = 0.2

# --- Simulación General (Función run_simulation) ---
SIMULACION_GENERAL_PASOS_PODA = 100
# -*- coding: utf-8 -*-
"""
Archivo de configuración para el entorno 2D.
"""

# --- Configuración de la Ventana ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TITULO_VENTANA = "Entorno de Aprendizaje para Agente Neuronal"
FPS = 30  # Fotogramas por segundo

# Constantes de la simulación
TASA_APRENDIZAJE = 0.4 # Aumentamos para que aprenda más rápido
PROBABILIDAD_EXPLORACION = 0.1 # 10% de probabilidad de moverse al azar para desatascarse
UMBRAL_PARED = 5 # Distancia en píxeles para detectar una pared
PESO_INICIAL_SINAPSIS = 0.1 # Peso inicial para las conexiones que pueden aprender
PESO_MAXIMO_SINAPSIS = 5.0 # El peso máximo que puede alcanzar una sinapsis
PESO_MINIMO_SINAPTICO = 0.01 # El peso mínimo para que el conocimiento quede latente
VENTANA_TEMPORAL_ASOCIACION = 5 # Ventana de tiempo (en pasos) para asociar eventos

# --- Colores (formato RGB) ---
COLOR_FONDO = (25, 25, 25)      # Gris oscuro
COLOR_AGENTE = (50, 150, 255)   # Azul
COLOR_COMIDA = (50, 205, 50)    # Verde lima
COLOR_PARED = (139, 69, 19)     # Marrón

# --- Configuración del Mundo ---
TAMANO_CELDA = 20

# --- Configuración del Agente ---
VELOCIDAD_AGENTE = 5 # Píxeles por fotograma

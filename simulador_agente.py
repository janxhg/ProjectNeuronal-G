# -*- coding: utf-8 -*-
"""
Archivo principal para la simulación del agente en el entorno 2D.
Conecta la RedDinamica con el entorno de Pygame para crear un ciclo de
percepción-acción-aprendizaje.
"""

import pygame
import sys
import os
import datetime
import random
import logging

# --- Importaciones del Entorno ---
from entorno_2d import config_entorno as config_env
from entorno_2d import entidades

# --- Importaciones de la Red Neuronal ---
from src.core.red_dinamica import RedDinamica
from src.core.neurona_g1 import NeuronaG1
import matplotlib.pyplot as plt
from src.visualizacion.visualizador_dinamico import VisualizadorDinamico
from configuracion import parametros_simulacion as ps

# --- Configuración del Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_agent_simulation():
    """Función principal que integra la red neuronal con el entorno 2D."""
    logging.info("Iniciando simulación del agente...")

    # --- 1. Inicialización del Entorno (Pygame) ---
    pygame.init()
    pantalla = pygame.display.set_mode((config_env.ANCHO_VENTANA, config_env.ALTO_VENTANA))
    pygame.display.set_caption(config_env.TITULO_VENTANA)
    reloj = pygame.time.Clock()

    # --- 2. Inicialización de la Red Neuronal ---
    red = RedDinamica()
    # El Gestor de Plasticidad ahora está ACTIVO por defecto en la RedDinamica.
    logging.info("Red neuronal creada con Gestor de Plasticidad ACTIVO.")

    # --- 3. Creación de Entidades y Neuronas ---
    agente = entidades.Agente(config_env.ANCHO_VENTANA // 2, config_env.ALTO_VENTANA // 2)
    comida = entidades.Comida(random.randint(0, config_env.ANCHO_VENTANA - config_env.TAMANO_CELDA),
                              random.randint(0, config_env.ALTO_VENTANA - config_env.TAMANO_CELDA))
    
    logging.info("Entidades del entorno creadas.")

    # IDs para las neuronas
    neuronas_sensoriales_comida_ids = [
        "S_Comida_Arriba", "S_Comida_Abajo", "S_Comida_Izquierda", "S_Comida_Derecha"
    ]
    neuronas_sensoriales_pared_ids = [
        "S_Pared_Arriba", "S_Pared_Abajo", "S_Pared_Izquierda", "S_Pared_Derecha"
    ]
    neuronas_motoras_ids = [
        "M_Mover_Arriba", "M_Mover_Abajo", "M_Mover_Izquierda", "M_Mover_Derecha"
    ]

    # Crear las neuronas sensoriales (comida y paredes)
    for nid in neuronas_sensoriales_comida_ids + neuronas_sensoriales_pared_ids:
        red.agregar_neurona(NeuronaG1(nid))
    
    # Crear las neuronas motoras
    for nid in neuronas_motoras_ids:
        red.agregar_neurona(NeuronaG1(nid))
    
    # Conectar cada neurona sensorial a cada neurona motora
    peso_inicial = 0.1 # Un peso bajo pero no nulo para permitir el aprendizaje
    for s_id in neuronas_sensoriales_comida_ids:
        for m_id in neuronas_motoras_ids:
            red.conectar_neuronas(s_id, m_id, peso_inicial=config_env.PESO_INICIAL_SINAPSIS)

    # Conectar las neuronas de PARED para que inhiban el movimiento (reflejo)
    # Estas conexiones son FIJAS (no plásticas) para que no se puedan desaprender.
    peso_inhibitorio_fuerte = -10.0 # Un valor muy negativo para asegurar la inhibición
    red.conectar_neuronas("S_Pared_Arriba", "M_Mover_Arriba", peso_inhibitorio_fuerte, plastica=False)
    red.conectar_neuronas("S_Pared_Abajo", "M_Mover_Abajo", peso_inhibitorio_fuerte, plastica=False)
    red.conectar_neuronas("S_Pared_Izquierda", "M_Mover_Izquierda", peso_inhibitorio_fuerte, plastica=False)
    red.conectar_neuronas("S_Pared_Derecha", "M_Mover_Derecha", peso_inhibitorio_fuerte, plastica=False)
    
    logging.info(f"Creadas {len(neuronas_sensoriales_comida_ids + neuronas_sensoriales_pared_ids)} neuronas sensoriales y {len(neuronas_motoras_ids)} motoras.")
    logging.info("Conexiones iniciales sensorio-motoras establecidas.")

    # --- Bucle Principal ---
    ejecutando = True
    ultima_neurona_sensorial_activa = None
    ultima_neurona_motora_activa = None

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                ejecutando = False

        # --- 4. Ciclo de Percepción-Acción-Aprendizaje ---

        # a) Percepción
        # a.1) Sentido del Tacto (Paredes): Activa reflejos inhibitorios
        if agente.rect.top <= config_env.UMBRAL_PARED:
            red.aplicar_impulso_externo("S_Pared_Arriba", 1.0)
        if agente.rect.bottom >= config_env.ALTO_VENTANA - config_env.UMBRAL_PARED:
            red.aplicar_impulso_externo("S_Pared_Abajo", 1.0)
        if agente.rect.left <= config_env.UMBRAL_PARED:
            red.aplicar_impulso_externo("S_Pared_Izquierda", 1.0)
        if agente.rect.right >= config_env.ANCHO_VENTANA - config_env.UMBRAL_PARED:
            red.aplicar_impulso_externo("S_Pared_Derecha", 1.0)

        # a.2) Sentido de la Vista (Comida): Guía el aprendizaje
        dx = comida.rect.x - agente.rect.x
        dy = comida.rect.y - agente.rect.y
        neurona_sensorial_activa = None

        if abs(dx) > abs(dy): # Movimiento horizontal es prioritario
            if dx > 0:
                neurona_sensorial_activa = "S_Comida_Derecha"
            else:
                neurona_sensorial_activa = "S_Comida_Izquierda"
        else: # Movimiento vertical
            if dy > 0:
                neurona_sensorial_activa = "S_Comida_Abajo"
            else:
                neurona_sensorial_activa = "S_Comida_Arriba"
        
        if neurona_sensorial_activa:
            red.aplicar_impulso_externo(neurona_sensorial_activa, 1.0)
            # Solo guardamos la última neurona de COMIDA para el aprendizaje
            ultima_neurona_sensorial_activa = neurona_sensorial_activa

        # b) Exploración Aleatoria: Añadir ruido para fomentar el descubrimiento
        if random.random() < config_env.PROBABILIDAD_EXPLORACION:
            neurona_motora_aleatoria = random.choice(neuronas_motoras_ids)
            red.aplicar_impulso_externo(neurona_motora_aleatoria, 1.0) # Impulso suficiente para disparar
            logging.info(f"--- Exploración: Activando {neurona_motora_aleatoria} ---")

        # c) Simulación de la Red: Dejar que el "cerebro" piense
        neuronas_disparadas = red.simular_paso()

        # d) Acción: Traducir disparos de neuronas motoras en movimiento
        posicion_anterior = agente.rect.copy()
        movimiento_realizado = False
        for nid in neuronas_disparadas:
            if nid in neuronas_motoras_ids and not movimiento_realizado:
                if nid == "M_Mover_Arriba":
                    agente.mover(0, -config_env.VELOCIDAD_AGENTE)
                elif nid == "M_Mover_Abajo":
                    agente.mover(0, config_env.VELOCIDAD_AGENTE)
                elif nid == "M_Mover_Izquierda":
                    agente.mover(-config_env.VELOCIDAD_AGENTE, 0)
                elif nid == "M_Mover_Derecha":
                    agente.mover(config_env.VELOCIDAD_AGENTE, 0)
                
                ultima_neurona_motora_activa = nid
                movimiento_realizado = True # Solo procesamos una acción por ciclo
        
        agente.mantener_en_pantalla(config_env.ANCHO_VENTANA, config_env.ALTO_VENTANA)

        # e) Castigo (LTD): Comprobar si el agente está atascado
        if movimiento_realizado and agente.rect == posicion_anterior:
            if ultima_neurona_sensorial_activa and ultima_neurona_motora_activa:
                try:
                    clave_conexion = (ultima_neurona_sensorial_activa, ultima_neurona_motora_activa)
                    conexion = red.conexiones[clave_conexion]
                    peso_actual = conexion.peso
                    # Debilitamos la conexión, asegurando que no baje de cero
                    nuevo_peso = max(0, peso_actual - config_env.TASA_APRENDIZAJE)
                    conexion.peso = nuevo_peso
                    logging.warning(f"¡CASTIGO! Movimiento bloqueado. Debilitando '{ultima_neurona_sensorial_activa}' -> '{ultima_neurona_motora_activa}'. Peso: {peso_actual:.2f} -> {nuevo_peso:.2f}")
                except KeyError:
                    pass # No hacemos nada si la conexión no existe

        # d) Recompensa: Comprobar si el agente ha alcanzado la comida
        if agente.rect.colliderect(comida.rect):
            # f) Recompensa y Aprendizaje (LTP)
            if ultima_neurona_sensorial_activa and ultima_neurona_motora_activa:
                try:
                    clave_conexion = (ultima_neurona_sensorial_activa, ultima_neurona_motora_activa)
                    conexion = red.conexiones[clave_conexion]
                    peso_actual = conexion.peso
                    nuevo_peso = min(config_env.PESO_MAXIMO_SINAPSIS, peso_actual + config_env.TASA_APRENDIZAJE)
                    conexion.peso = nuevo_peso
                    
                    logging.info(f"¡RECOMPENSA! Reforzando '{ultima_neurona_sensorial_activa}' -> '{ultima_neurona_motora_activa}'. Peso: {peso_actual:.2f} -> {nuevo_peso:.2f}")

                except KeyError:
                    logging.error("Error al intentar reforzar una sinapsis inexistente.")

            # Resetear para el próximo ciclo de aprendizaje
            ultima_neurona_sensorial_activa = None
            ultima_neurona_motora_activa = None
            
            # Mover la comida a una nueva posición
            comida.rect.x = random.randint(0, config_env.ANCHO_VENTANA - config_env.TAMANO_CELDA)
            comida.rect.y = random.randint(0, config_env.ALTO_VENTANA - config_env.TAMANO_CELDA)

        # Dibujado
        pantalla.fill(config_env.COLOR_FONDO)
        agente.dibujar(pantalla)
        comida.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(config_env.FPS)

    # --- Finalización ---
    pygame.quit()
    logging.info("Simulación finalizada.")

    # --- 5. Visualización Final de la Red --- 
    logging.info("Generando visualización final de la estructura de la red...")
    visualizador = VisualizadorDinamico(red)
    visualizador.actualizar_grafico() # Dibuja el estado final de la red
    visualizador.ax.set_title("Estado Final de la Red del Agente", fontsize=16) # Establece un título personalizado

    # --- Guardar el gráfico en un archivo ---
    graficos_dir = "graficos_red"
    os.makedirs(graficos_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(graficos_dir, f"red_agente_{timestamp}.png")
    
    # Usar la figura del visualizador para guardar
    visualizador.fig.savefig(filepath)
    logging.info(f"Gráfico de la red guardado en: {filepath}")

    plt.close(visualizador.fig) # Cierra la figura para liberar memoria
    sys.exit()

if __name__ == '__main__':
    run_agent_simulation()

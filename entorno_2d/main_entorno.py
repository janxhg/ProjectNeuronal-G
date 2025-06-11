# -*- coding: utf-8 -*-
"""
Archivo principal que ejecuta el entorno 2D y el bucle de simulación.
"""

import pygame
import sys
import random

# Hacemos una importación relativa para que funcione dentro del paquete 'entorno_2d'
from . import config_entorno as config
from . import entidades

def run_entorno():
    """Función principal para inicializar y correr el entorno."""
    pygame.init()

    # Configuración de la ventana
    pantalla = pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
    pygame.display.set_caption(config.TITULO_VENTANA)
    reloj = pygame.time.Clock()

    # Creación de las entidades
    agente = entidades.Agente(config.ANCHO_VENTANA // 2, config.ALTO_VENTANA // 2)
    comida = entidades.Comida(random.randint(0, config.ANCHO_VENTANA - config.TAMANO_CELDA),
                              random.randint(0, config.ALTO_VENTANA - config.TAMANO_CELDA))

    # Bucle principal de la simulación
    ejecutando = True
    while ejecutando:
        # 1. Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        # 2. Lógica de la simulación (Control por teclado y colisiones)
        
        # Control por teclado
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            agente.mover(-config.VELOCIDAD_AGENTE, 0)
        if teclas[pygame.K_RIGHT]:
            agente.mover(config.VELOCIDAD_AGENTE, 0)
        if teclas[pygame.K_UP]:
            agente.mover(0, -config.VELOCIDAD_AGENTE)
        if teclas[pygame.K_DOWN]:
            agente.mover(0, config.VELOCIDAD_AGENTE)
        
        # Mantener al agente en pantalla
        agente.mantener_en_pantalla(config.ANCHO_VENTANA, config.ALTO_VENTANA)

        # Lógica de colisión con la comida
        if agente.rect.colliderect(comida.rect):
            print("Agente ha recogido la comida.") # Esto será la señal de recompensa para la red
            # Mover la comida a una nueva posición aleatoria
            comida.rect.x = random.randint(0, config.ANCHO_VENTANA - config.TAMANO_CELDA)
            comida.rect.y = random.randint(0, config.ALTO_VENTANA - config.TAMANO_CELDA)

        # 3. Dibujado en pantalla
        pantalla.fill(config.COLOR_FONDO)
        agente.dibujar(pantalla)
        comida.dibujar(pantalla)

        # 4. Actualización de la pantalla
        pygame.display.flip()

        # Controlar los FPS
        reloj.tick(config.FPS)

    # Salir de Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # Este bloque permite ejecutar el entorno de forma independiente para pruebas
    run_entorno()

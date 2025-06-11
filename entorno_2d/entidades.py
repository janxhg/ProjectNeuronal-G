# -*- coding: utf-8 -*-
"""
Define las entidades que existen en el entorno 2D, como el Agente y la Comida.
"""

import pygame
from . import config_entorno as config

class Agente:
    def __init__(self, x, y):
        """Inicializa el agente en una posición específica."""
        self.rect = pygame.Rect(x, y, config.TAMANO_CELDA, config.TAMANO_CELDA)
        self.color = config.COLOR_AGENTE

    def mover(self, dx, dy):
        """Mueve el agente una cantidad delta en x e y."""
        self.rect.x += dx
        self.rect.y += dy

    def dibujar(self, superficie):
        """Dibuja el agente en la superficie de Pygame."""
        pygame.draw.rect(superficie, self.color, self.rect)

    def mantener_en_pantalla(self, ancho_pantalla, alto_pantalla):
        """Asegura que el agente no se salga de los límites de la pantalla."""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho_pantalla:
            self.rect.right = ancho_pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > alto_pantalla:
            self.rect.bottom = alto_pantalla

class Comida:
    def __init__(self, x, y):
        """Inicializa un objeto de comida en una posición específica."""
        self.rect = pygame.Rect(x, y, config.TAMANO_CELDA, config.TAMANO_CELDA)
        self.color = config.COLOR_COMIDA

    def dibujar(self, superficie):
        """Dibuja la comida en la superficie de Pygame."""
        pygame.draw.rect(superficie, self.color, self.rect)

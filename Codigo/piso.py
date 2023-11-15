import pygame
from personaje import *
from constantes import *
from cajas import *
from paredes import *
from niveles import *
from objetivo import *

class Piso:
    def __init__(self, x, y):
        self.image = pygame.image.load("imagenes/floor.png")
        self.image = pygame.transform.scale(self.image, (70,70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.rect_pared = pygame.Rect(self.rect.x, self.rect.y, 70, 70)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

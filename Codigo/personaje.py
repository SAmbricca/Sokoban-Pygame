import pygame
from constantes import *
from cajas import *
from objetivo import *
from paredes import *

pygame.mixer.init()
sonido_caminar = pygame.mixer.Sound("sonidos/caminar.flac")
sonido_caminar.set_volume(0.03)

class Personaje:
    def __init__(self, x, y) -> None:
        self.caminar_d = pygame.image.load("imagenes/d.png")
        self.caminar_d = pygame.transform.scale(self.caminar_d, (70,70))
        self.caminar_i = pygame.image.load("imagenes/i.png")
        self.caminar_i = pygame.transform.scale(self.caminar_i, (70,70))
        self.caminar_up = pygame.image.load("imagenes/up.png")
        self.caminar_up = pygame.transform.scale(self.caminar_up, (70,70))
        self.caminar_down = pygame.image.load("imagenes/down.png")
        self.caminar_down = pygame.transform.scale(self.caminar_down, (70,70))

        self.mover_x = 0
        self.mover_y = 0

        self.imagen = self.caminar_d

        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mirando = DIRECCION_R

        self.movimientos = 150
    
    def caminar(self, direccion, lista_cajas, lista_paredes):
        self.mirando = direccion
        self.mover_x = 0
        self.mover_y = 0

        if direccion == DIRECCION_R:
            self.mover_x = 70
            self.imagen = self.caminar_d
        elif direccion == DIRECCION_L:
            self.mover_x = -70
            self.imagen = self.caminar_i
        elif direccion == DIRECCION_UP:
            self.mover_y = -70
            self.imagen = self.caminar_up
        elif direccion == DIRECCION_DOWN:
            self.mover_y = 70
            self.imagen = self.caminar_down

        if not (self.colision_caja(lista_cajas, lista_paredes, self.mirando) or self.colision_pared(lista_paredes)):
            self.rect.x += self.mover_x
            self.rect.y += self.mover_y
            self.movimientos -= 1
            sonido_caminar.play()
    
    def parado(self):
        self.mover_x = 0
        self.mover_y = 0


    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
    
    def colision_caja(self, lista_cajas, lista_paredes, direccion):
        nuevo_rect = pygame.Rect(self.rect)
        nuevo_rect.x += self.mover_x
        nuevo_rect.y += self.mover_y
        colision = False

        for caja in lista_cajas:
            if nuevo_rect.colliderect(caja.rect_caja):
                colision = True
                self.movimientos -= 1
                if direccion == DIRECCION_R:
                    caja.mover_caja(DIRECCION_R, lista_cajas, lista_paredes)
                elif direccion == DIRECCION_L:
                    caja.mover_caja(DIRECCION_L, lista_cajas, lista_paredes)
                elif direccion == DIRECCION_UP:
                    caja.mover_caja(DIRECCION_UP, lista_cajas, lista_paredes)
                elif direccion == DIRECCION_DOWN:
                    caja.mover_caja(DIRECCION_DOWN, lista_cajas, lista_paredes)
                break
        return colision

    def colision_pared(self, lista_paredes):
        nuevo_rect = pygame.Rect(self.rect)
        nuevo_rect.x += self.mover_x
        nuevo_rect.y += self.mover_y
        colision = False
        for pared in lista_paredes:
            if nuevo_rect.colliderect(pared.rect_pared):
                colision = True
                break
        return colision

import pygame
from constantes import *
from paredes import *
from objetivo import *

pygame.mixer.init()
sonido_caja = pygame.mixer.Sound("sonidos/mover_caja.flac")
sonido_caja.set_volume(0.1)

class Caja:
    def __init__(self, x, y):
        self.image = pygame.image.load("imagenes/box.png")
        self.image = pygame.transform.scale(self.image, (70,70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.rect_caja = pygame.Rect(self.rect.x, self.rect.y, 70,70)

    def mover_caja(self, direccion, lista_cajas, lista_paredes):
        # Primero calculo las futuras posiciones, para luego comprobar si habrá colisión
        nuevo_rect_x = self.rect.x
        nuevo_rect_y = self.rect.y
        nuevo_rect_caja_x = self.rect_caja.x
        nuevo_rect_caja_y = self.rect_caja.y

        if direccion == DIRECCION_R:
            nuevo_rect_x += 70
            nuevo_rect_caja_x += 70
        elif direccion == DIRECCION_L:
            nuevo_rect_x -= 70
            nuevo_rect_caja_x -= 70
        elif direccion == DIRECCION_UP:
            nuevo_rect_y -= 70
            nuevo_rect_caja_y -= 70
        elif direccion == DIRECCION_DOWN:
            nuevo_rect_y += 70
            nuevo_rect_caja_y += 70

        # Compruebo si habrá colisión con alguna pared o caja
        # Si no habrá colisión, realiza el movimiento.
        nuevo_caja_rect = pygame.Rect(nuevo_rect_caja_x, nuevo_rect_caja_y, self.rect_caja.width, self.rect_caja.height)
        if not self.colision_caja_pared(lista_cajas, lista_paredes, nuevo_caja_rect):
            self.rect.x = nuevo_rect_x
            self.rect.y = nuevo_rect_y
            self.rect_caja.x = nuevo_rect_caja_x
            self.rect_caja.y = nuevo_rect_caja_y
            sonido_caja.play()
            
    
    def colision_caja_pared(self, lista_cajas, lista_paredes, nuevo_caja_rect):
        colision = False
        for pared in lista_paredes:
            if nuevo_caja_rect.colliderect(pared.rect_pared):
                colision = True
        for caja in lista_cajas:
            if nuevo_caja_rect.colliderect(caja.rect_caja):
                colision = True
        return colision

    def colision_objetivo(self, lista_objetivos):
        colision = False
        for objetivo in lista_objetivos:
            if self.rect_caja.colliderect(objetivo.rect_objetivo):
                colision = True

        if colision == True:
            self.image = pygame.image.load("imagenes/box_docked.png")
            self.image = pygame.transform.scale(self.image, (70,70))
        else:
            self.image = pygame.image.load("imagenes/box.png")
            self.image = pygame.transform.scale(self.image, (70,70))
        
    def todas_en_objetivo(self, lista_cajas, lista_objetivos):
        nivel_terminado = True  # Inicializamos nivel_terminado en True
        for objetivo in lista_objetivos:
            colisiona_con_objetivo = any(caja.rect_caja.colliderect(objetivo.rect_objetivo) for caja in lista_cajas)
            if not colisiona_con_objetivo:
                nivel_terminado = False
                break
        return nivel_terminado

    
    def dibujar(self, pantalla, lista_objetivos):
        self.colision_objetivo(lista_objetivos)
        pantalla.blit(self.image, self.rect)


        

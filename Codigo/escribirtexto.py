import pygame
import sys
from constantes import *
from personaje import *
from cajas import *
from paredes import *
from mapa import *
from niveles import *
from objetivo import *
from ventanas import *

class Escribir:
    def __init__(self, x , y) -> None:
        self.lineas = 0
        self.caracteres = []
        self.fuente = pygame.font.Font(None, 70)

        self.distancia_letras = 20
        self.x = x
        self.y = y

    def numero_nivel(self, evento, numero_nivel, ventana_activa, bandera_seleccion_nivel):
        ventana_activa = "titulo principal"
        bandera_seleccion_nivel = bandera_seleccion_nivel
        for accion in evento:
            if accion.type == pygame.KEYDOWN:
                if accion.key == pygame.K_RETURN:
                    if len(self.caracteres[self.lineas]) > 0:
                        numero_nivel = int(''.join(self.caracteres))
                        self.caracteres = ['']  # Reiniciar la lista de caracteres
                        self.lineas = 0
                        if numero_nivel >= 0 and numero_nivel < 10:
                            ventana_activa = "nivel"
                            bandera_seleccion_nivel = True
                            return numero_nivel, ventana_activa, bandera_seleccion_nivel
                elif accion.key == pygame.K_BACKSPACE:
                    if len(self.caracteres[self.lineas]) > 0:
                        self.caracteres[self.lineas] = self.caracteres[self.lineas][:-1]
                    elif self.lineas > 0:
                        self.lineas -= 1
                        self.caracteres = self.caracteres[0:self.lineas] + [self.caracteres[self.lineas][:-1]]
                    
                elif accion.unicode.isdigit():
                    if len(self.caracteres) > 0:
                        self.caracteres[self.lineas] = str(self.caracteres[self.lineas] + accion.unicode)
                    else:
                        self.caracteres.append(accion.unicode)
                        self.lineas = 1
        self.lineas = 0
        return numero_nivel, ventana_activa, bandera_seleccion_nivel
    

    def nombre_usuario(self, evento):
        nombre_usuario_final = ""
        for accion in evento:
            if accion.type == pygame.KEYDOWN:
                if accion.key == pygame.K_RETURN:
                    nombre_usuario_final = str(''.join(self.caracteres))
                elif accion.key == pygame.K_BACKSPACE:
                    if len(self.caracteres[self.lineas]) > 0:
                        self.caracteres[self.lineas] = self.caracteres[self.lineas][:-1]
                    elif self.lineas > 0:
                        self.lineas -= 1
                        self.caracteres = self.caracteres[0:self.lineas] + [self.caracteres[self.lineas][:-1]]
                else:
                    if len(self.caracteres) > 0:
                        self.caracteres[self.lineas] = str(self.caracteres[self.lineas] + accion.unicode)
                    else:
                        self.caracteres.append(accion.unicode)
                        self.lineas = 1

        return nombre_usuario_final

    
    def mensaje(self, pantalla, tipo):
        if len(self.caracteres) > 0:
            if tipo == "numero_nivel":
                for self.lineas in range(len(self.caracteres)):
                    imagen_letra = self.fuente.render(self.caracteres[self.lineas], True, (COLOR_ROSA))
            else:
                for self.lineas in range(len(self.caracteres)):
                    imagen_letra = self.fuente.render(self.caracteres[self.lineas], True, (COLOR_VERDE))
            pantalla.blit(imagen_letra, (self.x, self.y))


import pygame
from personaje import *
from constantes import *
from cajas import *
from paredes import *
from niveles import *
from objetivo import *
from piso import *

class Mapa:
    def __init__(self):
        self.nivel_actual = None
    
    def crear_mapa_nivel(self, numero_nivel):
        
        nivel = lista_niveles[numero_nivel]
        lista_cajas = []
        lista_paredes = []
        lista_objetivos = []
        lista_pisos = []
        
        fila_numero = 0  #Para rastrear el número de fila
        for fila in nivel:
            columna_numero = 0  #Para rastrear el número de columna
            for simbolo in fila:
                if len(nivel) == 7:
                    x = 450 +(columna_numero * 70)
                    y = 150 +(fila_numero * 70)
                elif len(nivel) == 8:
                    x = 400 +(columna_numero * 70)
                    y = 150 +(fila_numero * 70)
                elif len(nivel) == 9:
                    x = 320 +(columna_numero * 70)
                    y = 100 +(fila_numero * 70)
                elif len(nivel) == 10:
                    x = 320 +(columna_numero * 70)
                    y = 100 +(fila_numero * 70)
                elif len(nivel) == 11:
                    x = 300 +(columna_numero * 70)
                    y = 100 +(fila_numero * 70)
                else:
                    x = 100 + (columna_numero * 70)
                    y = 20 + (fila_numero * 70)

                if simbolo != "-":
                    lista_pisos.append(Piso(x,y))

                if simbolo == '+':
                    lista_objetivos.append(Objetivo(x,y))
                    personaje = Personaje(x, y)
                elif simbolo == '#':
                    lista_paredes.append(Pared(x,y))
                elif simbolo == '@':
                    personaje = Personaje(x, y)
                elif simbolo == '.':
                    lista_objetivos.append(Objetivo(x,y))
                elif simbolo == '*':
                    lista_cajas.append(Caja(x,y))
                    lista_objetivos.append(Objetivo(x,y))
                elif simbolo == '$':
                    lista_cajas.append(Caja(x,y))
                else:
                    pass
                
                columna_numero += 1
            fila_numero += 1

        return personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos
        '''
        simbolo == ' '  #piso
        simbolo == '#'  #pared
        simbolo == '@'  #pj sobre el piso
        simbolo == '.'  #objetivo
        simbolo == '*'  #caja en objetivo
        simbolo == '$'  #caja
        simbolo == '+'  #pj en objetivo
        '''

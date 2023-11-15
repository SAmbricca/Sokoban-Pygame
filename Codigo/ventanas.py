import pygame
import sys
from constantes import *
from personaje import *
from cajas import *
from paredes import *
from mapa import *
from niveles import *
from objetivo import *
import codecs

fondo_principal = pygame.image.load("imagenes/fondo.jpg")
fondo_principal = pygame.transform.scale(fondo_principal, (ANCHO_VENTANA, ALTO_VENTANA))
fondo_nivel_ranking = pygame.image.load("imagenes/fondo_nivel.png")
fondo_nivel_ranking = pygame.transform.scale(fondo_nivel_ranking, (ANCHO_VENTANA, ALTO_VENTANA))

class Ventana:
    dict_ventana_activa = {}    #creo un diccionario antes de crear el constructor. Ahora todas las clases van a compartir este diccionario en el mismo espacio de memoria
    def __init__(self):
        self.fuente = pygame.font.SysFont("8-bit-pusab.ttf", 80)
        self.fuente_pausa = pygame.font.SysFont("8-bit-pusab.ttf", 170)
        self.fuente_barra_datos = pygame.font.SysFont("8-bit-pusab.ttf", 50)

        self.superficie_transparente = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        self.rect_transparente = self.superficie_transparente.get_rect()

class Ventana_principal(Ventana):
    def __init__(self) -> None:
        super().__init__()
        self.texto_titulo_elegir_nivel = self.fuente.render('Elegir nivel (0-9)', True, COLOR_ROSA)
        self.rect_texto_titulo_elegir_nivel = pygame.Rect((50, 820), (290,35))

        self.texto_titulo_ranking = self.fuente.render('Ranking', True, COLOR_ROSA)
        self.rect_texto_titulo_ranking = pygame.Rect((600, 820), (290,35))

        self.texto_titulo_salir = self.fuente.render('Salir', True, COLOR_ROSA)
        self.rect_texto_titulo_salir = pygame.Rect((1050, 820), (290,35))
        

    def dibujar(self, pantalla):
        pantalla.blit(fondo_principal, (0,0))

        pantalla.blit(self.texto_titulo_elegir_nivel,(50, 820))
        pantalla.blit(self.texto_titulo_ranking,(620, 820))
        pantalla.blit(self.texto_titulo_salir,(1050, 820))

class Ventana_nivel(Ventana):
    def __init__(self) -> None:
        super().__init__() 

        
         
    def dibujar(self, personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos, pantalla, ventana_activa, contador_segundos):
        pantalla.fill(COLOR_NEGRO)
        pantalla.blit(fondo_nivel_ranking, (0,0))
        ventana_activa = ventana_activa
        for piso in lista_pisos:
            piso.dibujar(pantalla)

        for objetivo in lista_objetivos:
            objetivo.dibujar(pantalla)

        for pared in lista_paredes:
            pared.dibujar(pantalla)

        for caja in lista_cajas:
            caja.dibujar(pantalla, lista_objetivos)

        personaje.dibujar(pantalla)
        pygame.draw.rect(pantalla, COLOR_BLANCO, (0, 890, 1360, 70))
        texto_movimientos = self.fuente_barra_datos.render(str(f'Movimientos: {personaje.movimientos}'), True, COLOR_NEGRO)
        pantalla.blit(texto_movimientos, (30, 910))
        texto_timer = self.fuente_barra_datos.render(str(f'Tiempo: {contador_segundos}'), True, COLOR_NEGRO)
        pantalla.blit(texto_timer, (610, 910))
        self.puntaje_movimientos = (personaje.movimientos)
        self.puntaje_tiempo = (500 - contador_segundos)
        self.puntaje_total = int(self.puntaje_movimientos + self.puntaje_tiempo)
        texto_puntaje = self.fuente_barra_datos.render(str(f'Score: {self.puntaje_total}'), True, COLOR_NEGRO)
        pantalla.blit(texto_puntaje, (1100, 910))
        
        if caja.todas_en_objetivo(lista_cajas, lista_objetivos):
            ventana_activa = "nivel_completado"
        return ventana_activa


class Ventana_nivel_completado(Ventana):
    def __init__(self, personaje, contador_segundos):
        super().__init__()
        self.puntaje_movimientos = (personaje.movimientos)
        self.puntaje_tiempo = (500 - contador_segundos)
        self.puntaje_total = int(self.puntaje_movimientos + self.puntaje_tiempo)

        self.texto_nivel_completado = self.fuente_pausa.render('NIVEL COMPLETADO', True, COLOR_VERDE)
        self.texto_movimientos = self.fuente.render(f'Movimientos: {personaje.movimientos}', True, COLOR_VERDE)
        self.texto_tiempo = self.fuente.render(f'Tiempo: {contador_segundos}', True, COLOR_VERDE)
        self.texto_puntaje = self.fuente.render(f'Score: {self.puntaje_total}', True, COLOR_VERDE)
        self.texto_usuario = self.fuente.render(f'Nombre:', True, COLOR_VERDE)

        self.texto_siguiente_nivel = self.fuente.render(f'Siguiente nivel', True, COLOR_VERDE)
        self.rect_texto_siguiente_nivel = pygame.Rect((450, 650), (350, 45))

        self.texto_volver_al_menu = self.fuente.render('VOLVER AL MENU PRINCIPAL', True, COLOR_VERDE)
        self.rect_texto_volver_al_menu = pygame.Rect((270, 830), (900, 45))

    def guardar_puntaje(self, nombre_usuario, numero_nivel):
        with codecs.open(f'ranking/puntajes{numero_nivel}.txt', 'r', encoding='UTF-8') as archivo:
            lineas = archivo.readlines()
            if any(nombre_usuario in linea for linea in lineas):
                return

        with codecs.open(f'ranking/puntajes{numero_nivel}.txt', 'a', encoding = 'UTF-8') as archivo:
            escritura = f'{nombre_usuario}: {self.puntaje_total}\n'
            archivo.write(escritura)

    def dibujar(self, pantalla):
        pygame.draw.rect(self.superficie_transparente, (128, 128, 128, 200), self.rect_transparente)
        pantalla.blit(self.superficie_transparente, (0,0))
        
        pantalla.blit(self.texto_nivel_completado,(70, 100))
        pantalla.blit(self.texto_movimientos,(70, 500))
        pantalla.blit(self.texto_tiempo,(750, 500))
        pantalla.blit(self.texto_puntaje,(70, 350))
        pantalla.blit(self.texto_usuario,(750, 350))
        pantalla.blit(self.texto_siguiente_nivel,(450, 650))
        pantalla.blit(self.texto_volver_al_menu,(270, 830))

class Ventana_pausa(Ventana):
    def __init__(self) -> None:
        super().__init__()
        self.texto_pausa = self.fuente_pausa.render('PAUSA', True, COLOR_VERDE)

        self.texto_continuar = self.fuente.render('CONTINUAR', True, COLOR_VERDE)
        self.rect_texto_continuar = pygame.Rect((500, 450), (350, 45))

        self.texto_volver_al_menu = self.fuente.render('VOLVER AL MENU PRINCIPAL', True, COLOR_VERDE)
        self.rect_texto_volver_al_menu = pygame.Rect((270, 650), (900, 45))
    
    def dibujar(self, pantalla):
        pygame.draw.rect(self.superficie_transparente, (128, 128, 128, 200), self.rect_transparente)
        pantalla.blit(self.superficie_transparente, (0,0))
        
        pantalla.blit(self.texto_pausa,(480, 200))
        pantalla.blit(self.texto_continuar,(500, 450))
        pantalla.blit(self.texto_volver_al_menu,(270, 650))

class Ventana_ranking(Ventana):
    def __init__(self):
        super().__init__()

        self.texto_ranking = self.fuente_pausa.render('RANKING', True, COLOR_ROSA)
        self.texto_volver = self.fuente_barra_datos.render('Volver', True, COLOR_ROSA)
        self.rect_texto_volver = pygame.Rect((1200, 900), (100, 50))

    def obtener_mejores_puntajes(self):
        mejores_jugadores_por_nivel = []
        for i in range(10):
            datos = []
            with open(f'ranking/puntajes{i}.txt', 'r', encoding='UTF-8') as archivo:
                for linea in archivo:
                    partes = linea.strip().split(': ')
                    if len(partes) == 2:
                        nombre_usuario = partes[0]
                        puntaje = float(partes[1])
                        datos.append((nombre_usuario, puntaje))
            if datos:
                datos_ordenados = sorted(datos, key=lambda x: x[1], reverse=True)
                mejor_jugador = datos_ordenados[0]
                mejores_jugadores_por_nivel.append(mejor_jugador)
        return mejores_jugadores_por_nivel

    def dibujar(self, pantalla, lista_mejores_jugadores):
        pantalla.blit(fondo_nivel_ranking, (0,0))
        pantalla.blit(self.texto_ranking, (420, 20))
        pantalla.blit(self.texto_volver, (1200, 900))
        for i, jugador in enumerate(lista_mejores_jugadores):
            nombre, puntaje = jugador
            texto_nivel = self.fuente_barra_datos.render(f'Nivel {i + 1}:         Usuario - {nombre}         Score - {puntaje}', True, COLOR_ROSA)
            x = 50
            y = 170 + (i * 80)
            pantalla.blit(texto_nivel, (x, y))




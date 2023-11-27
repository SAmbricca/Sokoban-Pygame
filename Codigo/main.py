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
from escribirtexto import *

pygame.init()
pygame.mixer.init()
pantalla = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Sokoban by Santiago Ambricca")
pygame.font.init
nombre_usuario = Escribir(1000, 355)
nombre_usuario_final = ""

#Reloj para controlar la frecuencia de actualización del bucle principal
reloj = pygame.time.Clock()
tiempo_inicial = pygame.time.get_ticks()
contador_segundos = 0

mapa = Mapa()
numero_nivel = 0
(personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos) = mapa.crear_mapa_nivel(numero_nivel)

ventana = Ventana()
ventana_principal = Ventana_principal()
ventana_seleccion_nivel = Ventana_seleccion_nivel()
ventana_pausa = Ventana_pausa()
ventana_nivel = Ventana_nivel()
ventana_game_over = Ventana_game_over()
ventana_ranking = Ventana_ranking()

pygame.mixer.music.load("sonidos/puzzlemenu.ogg")
sonido_nivel_completado = pygame.mixer.Sound("sonidos/nivel_completo.wav")
sonido_nivel_completado.set_volume(0.01)
musica_reproducida = False
bandera_elegir_nivel = False
tiempo_pausado = False

ventana_activa = "titulo principal"

while True:
    if not tiempo_pausado:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido_segundos = (tiempo_actual - tiempo_inicial) // 1000
        if tiempo_transcurrido_segundos > contador_segundos:
            contador_segundos = tiempo_transcurrido_segundos

    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if ventana_activa == "nivel":
                    tiempo_pausado = True
                    ventana_activa = "pausa"
                elif ventana_activa == "pausa":
                    tiempo_pausado = False
                    ventana_activa = "nivel"
                    
            elif ventana_activa == "nivel_completado":
                nombre_usuario_final = nombre_usuario.nombre_usuario(eventos)

            elif not tiempo_pausado:
                if event.key == pygame.K_RIGHT:
                    personaje.caminar(DIRECCION_R, lista_cajas, lista_paredes)
                elif event.key == pygame.K_LEFT:
                    personaje.caminar(DIRECCION_L, lista_cajas, lista_paredes)
                elif event.key == pygame.K_UP:
                    personaje.caminar(DIRECCION_UP, lista_cajas, lista_paredes)
                elif event.key == pygame.K_DOWN:
                    personaje.caminar(DIRECCION_DOWN, lista_cajas, lista_paredes)
                elif event.key == pygame.K_r:  #boton de reseteo de nivel
                    (personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos) = mapa.crear_mapa_nivel(numero_nivel)
                    tiempo_inicial = pygame.time.get_ticks()
                    contador_segundos = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            posicion_click = list(event.pos)
            if ventana_activa == "titulo principal":
                if ventana_principal.rect_texto_titulo_seleccionar_nivel.collidepoint(posicion_click):
                    ventana_activa = "seleccion nivel"

                elif ventana_principal.rect_texto_titulo_ranking.collidepoint(posicion_click):
                    ventana_activa = "ranking"
            
                elif ventana_principal.rect_texto_titulo_salir.collidepoint(posicion_click):
                    pygame.quit()
                    sys.exit()

            elif ventana_activa == "seleccion nivel":
                if ventana_seleccion_nivel.rect_texto_volver.collidepoint(posicion_click):
                    ventana_activa = "titulo principal"

                for i in range(len(ventana_seleccion_nivel.lista_rects)):
                    if ventana_seleccion_nivel.lista_rects[i].collidepoint(posicion_click):
                        contador_segundos = 0
                        tiempo_inicial = pygame.time.get_ticks()
                        numero_nivel = i
                        (personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos) = mapa.crear_mapa_nivel(numero_nivel)
                        ventana_activa = "nivel"
                        tiempo_pausado = False
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sonidos/nivel.mp3")
                        musica_reproducida = False
                        break

            elif ventana_activa == "pausa":
                if ventana_pausa.rect_texto_continuar.collidepoint(posicion_click):
                    ventana_activa = "nivel"
                elif ventana_pausa.rect_texto_volver_al_menu.collidepoint(posicion_click):
                    ventana_activa = "titulo principal"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sonidos/puzzlemenu.ogg")
                    musica_reproducida = False

            elif ventana_activa == "ranking":
                if ventana_ranking.rect_texto_volver.collidepoint(posicion_click):
                    ventana_activa = "titulo principal"

            elif ventana_activa == "nivel_completado":
                if ventana_nivel_completado.rect_texto_siguiente_nivel.collidepoint(posicion_click):
                    contador_segundos = 0
                    tiempo_inicial = pygame.time.get_ticks()
                    numero_nivel += 1
                    (personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos) = mapa.crear_mapa_nivel(numero_nivel)
                    ventana_activa = "nivel"
                    tiempo_pausado = False
                    musica_reproducida = False

                elif ventana_nivel_completado.rect_texto_volver_al_menu.collidepoint(posicion_click):
                    ventana_activa = "titulo principal"
                    musica_reproducida = False
                    pygame.mixer.music.load("sonidos/puzzlemenu.ogg")
            
            elif ventana_activa == "game over":
                if ventana_game_over.rect_texto_reintentar.collidepoint(posicion_click):
                    contador_segundos = 0
                    tiempo_inicial = pygame.time.get_ticks()
                    (personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos) = mapa.crear_mapa_nivel(numero_nivel)
                    ventana_activa = "nivel"
                    tiempo_pausado = False
                    musica_reproducida = False

                elif ventana_game_over.rect_texto_volver_al_menu.collidepoint(posicion_click):
                    ventana_activa = "titulo principal"
                    musica_reproducida = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sonidos/puzzlemenu.ogg")

    reloj.tick(FPS)
    if personaje.movimientos == 0:
        personaje.movimientos = 150
        ventana_activa = "game over"

    if ventana_activa == "titulo principal":
        ventana_principal.dibujar(pantalla)

    elif ventana_activa == "seleccion nivel":
        ventana_seleccion_nivel.dibujar(pantalla)

    elif ventana_activa == "nivel":
        ventana_activa = ventana_nivel.dibujar(personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos, pantalla, ventana_activa, contador_segundos)

    elif ventana_activa == "pausa":
        ventana_nivel.dibujar(personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos, pantalla, ventana_activa, contador_segundos)
        ventana_pausa.dibujar(pantalla)

    elif ventana_activa == "ranking":
        lista_ranking_por_nivel = ventana_ranking.obtener_mejores_puntajes()
        ventana_ranking.dibujar(pantalla, lista_ranking_por_nivel)

    elif ventana_activa == "nivel_completado":
        sonido_nivel_completado.play()
        pygame.mixer.music.stop()
        tiempo_pausado = True
        ventana_nivel_completado = Ventana_nivel_completado(personaje, contador_segundos)
        ventana_activa = ventana_nivel.dibujar(personaje, lista_cajas, lista_paredes, lista_objetivos, lista_pisos, pantalla, ventana_activa, contador_segundos)
        ventana_nivel_completado.dibujar(pantalla)
        nombre_usuario.mensaje(pantalla, "nombre_usuario")
        ventana_nivel_completado.guardar_puntaje(nombre_usuario_final, numero_nivel)
    
    elif ventana_activa == "game over":
        pygame.mixer.music.stop()
        tiempo_pausado = True
        ventana_game_over.dibujar(pantalla)
    
    if not musica_reproducida:
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play()
        musica_reproducida = True

    pygame.display.flip() #pasar lo que programamos a la pantalla

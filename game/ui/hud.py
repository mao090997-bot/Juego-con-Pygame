import pygame
from config import ANCHO, ALTO, MAX_ENERGIA_DASH


def dibujar_hud(pantalla, jugador, puntuacion, tiempo_transcurrido_ms,
                fuente_ppal, fuente_hit, corazon_img, hits):
    segundos_totales = tiempo_transcurrido_ms // 1000
    minutos = segundos_totales // 60
    segundos = segundos_totales % 60

    # Vidas (corazones)
    for i in range(jugador.vidas):
        pantalla.blit(corazon_img, (10 + i * 40, 10))

    # Puntuacion
    texto_puntos = fuente_ppal.render(f"Puntos: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (ANCHO - texto_puntos.get_width() - 20, 15))

    # Cronometro
    texto_crono = fuente_ppal.render(f"{minutos}:{segundos:02d}", True, (255, 255, 255))
    pantalla.blit(texto_crono, (ANCHO // 2 - texto_crono.get_width() // 2, 15))

    # Hit popups
    for h in hits:
        h.dibujar(pantalla, fuente_hit)

    # Barra de energia (dash)
    ancho_barra = 80
    pygame.draw.rect(pantalla, (60, 60, 60), (10, 60, ancho_barra, 8))
    ancho_lleno = int(ancho_barra * (jugador.energia_dash / MAX_ENERGIA_DASH))
    color_dash = (0, 200, 255) if jugador.energia_dash > 30 else (255, 100, 0)
    pygame.draw.rect(pantalla, color_dash, (10, 60, ancho_lleno, 8))


def dibujar_game_over(pantalla, puntuacion, tiempo_sobrevivido_ms):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(160)
    overlay.fill((0, 0, 0))
    pantalla.blit(overlay, (0, 0))

    fuente_titulo = pygame.font.Font(None, 74)
    titulo = fuente_titulo.render("GAME OVER", True, (255, 0, 0))
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 250))

    fuente_info = pygame.font.Font(None, 48)
    puntaje = fuente_info.render(f"Puntaje final: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(puntaje, (ANCHO // 2 - puntaje.get_width() // 2, 330))

    segs = tiempo_sobrevivido_ms // 1000
    tiempo = fuente_info.render(f"Tiempo: {segs // 60}m {segs % 60}s", True, (255, 255, 255))
    pantalla.blit(tiempo, (ANCHO // 2 - tiempo.get_width() // 2, 390))

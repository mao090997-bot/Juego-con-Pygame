import pygame
from config import ANCHO, ALTO, INTERVALO_INVULNERABILIDAD


class Repartidor:
    def __init__(self, img):
        self.img = img
        self.x = 368
        self.y = 450
        self.cambio_x = 0
        self.cambio_y = 0
        self.vidas = 4
        self.ultimo_dano = 0
        self.energia_dash = 100

    def mover(self, multiplicador):
        self.x += self.cambio_x * multiplicador
        self.y += self.cambio_y * multiplicador
        if self.x < 0:
            self.x = 0
        elif self.x > ANCHO - 64:
            self.x = ANCHO - 64
        if self.y < 0:
            self.y = 0
        elif self.y > ALTO - 108:
            self.y = ALTO - 108

    def get_rect(self):
        return pygame.Rect(self.x + 12, self.y + 20, 40, 70)

    def esta_invulnerable(self, tiempo_actual):
        return tiempo_actual - self.ultimo_dano < INTERVALO_INVULNERABILIDAD

    def dibujar(self, pantalla):
        pantalla.blit(self.img, (self.x, self.y))

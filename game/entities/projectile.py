import pygame
from config import ANCHO, ALTO


class Pizza:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def mover(self):
        self.x += self.dx
        self.y += self.dy

    def esta_fuera(self):
        return (self.x < -32 or self.x > ANCHO or
                self.y < -32 or self.y > ALTO)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 32, 32)

    def dibujar(self, pantalla, img):
        pantalla.blit(img, (self.x, self.y))

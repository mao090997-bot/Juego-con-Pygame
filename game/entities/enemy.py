import math
import random
import pygame
from config import GATO_ANCHO, GATO_ALTO, GATO_AMPLITUD, GATO_FRECUENCIA
from utils.helpers import distancia


class Perro:
    def __init__(self, x, y, vel, modo):
        self.tipo = "perro"
        self.x = x
        self.y = y
        self.vel = vel
        self.modo = modo

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 58, 72)

    def get_centro(self):
        return (self.x + 29, self.y + 36)

    def perseguir(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distancia(self.x, self.y, target_x, target_y)
        if dist == 0:
            return
        if self.modo != 0 and dist > 120:
            nx = dx / dist
            ny = dy / dist
            lado = -1 if self.modo == 1 else 1
            flanco_x = target_x + (-ny * lado) * 100
            flanco_y = target_y + (nx * lado) * 100
            fdx = flanco_x - self.x
            fdy = flanco_y - self.y
            fdist = distancia(self.x, self.y, flanco_x, flanco_y)
            if fdist > 0:
                self.x += (fdx / fdist) * self.vel
                self.y += (fdy / fdist) * self.vel
        else:
            self.x += (dx / dist) * self.vel
            self.y += (dy / dist) * self.vel

    def dibujar(self, pantalla, img):
        pantalla.blit(img, (self.x, self.y))


class Gato(Perro):
    def __init__(self, x, y, vel, img):
        super().__init__(x, y, vel, modo=0)
        self.tipo = "gato"
        self.img = img
        self.amplitud = GATO_AMPLITUD
        self.frecuencia = GATO_FRECUENCIA
        self.tiempo_vida = 0
        self.zigzag_contador = random.randint(30, 90)
        self.zigzag_fase = random.uniform(0, math.pi * 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, GATO_ANCHO, GATO_ALTO)

    def get_centro(self):
        return (self.x + GATO_ANCHO // 2, self.y + GATO_ALTO // 2)

    def perseguir(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = distancia(self.x, self.y, target_x, target_y)
        if dist == 0:
            return

        nx = dx / dist
        ny = dy / dist
        perpx = -ny
        perpy = nx

        self.tiempo_vida += 1
        self.zigzag_contador -= 1
        if self.zigzag_contador <= 0:
            self.zigzag_fase = random.uniform(0, math.pi * 2)
            self.zigzag_contador = random.randint(30, 90)

        offset = math.sin(self.tiempo_vida * self.frecuencia + self.zigzag_fase) * self.amplitud

        self.x += (nx * self.vel) + (perpx * offset)
        self.y += (ny * self.vel) + (perpy * offset)

    def dibujar(self, pantalla, img=None):
        pantalla.blit(self.img, (self.x, self.y))

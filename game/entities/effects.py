import pygame


class Particula:
    def __init__(self, x, y, vx, vy, vida, tam):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.vida = vida
        self.tam = tam

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1

    def dibujar(self, pantalla):
        vida_ratio = self.vida / 40
        color = (255, 200, 0) if vida_ratio > 0.5 else (255, 100, 0)
        pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), int(self.tam))


class HitPopup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 30

    def actualizar(self):
        self.timer -= 1
        self.y -= 1

    def dibujar(self, pantalla, fuente):
        texto = fuente.render("+10", True, (255, 255, 100))
        pantalla.blit(texto, (self.x + 10, self.y))

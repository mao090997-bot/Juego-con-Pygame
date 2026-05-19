import math
import pygame
from config import ANCHO, ALTO, CAJA_VIDA_ANCHO, CAJA_VIDA_ALTO


class CajaVida:
    def __init__(self, x, y, img, tiempo_aparicion):
        self.x = x
        self.y = y
        self.ancho = CAJA_VIDA_ANCHO
        self.alto = CAJA_VIDA_ALTO
        self.img = img
        self.tiempo_aparicion = tiempo_aparicion

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def ha_expirado(self, tiempo_actual):
        return tiempo_actual - self.tiempo_aparicion >= 6000

    def dibujar(self, pantalla, tiempo_actual):
        tiempo_vivo = tiempo_actual - self.tiempo_aparicion
        pulse = math.sin(tiempo_vivo * 0.008) * 0.15 + 1.0

        # Centro de la caja
        cx = self.x + self.ancho // 2
        cy = self.y + self.alto // 2

        # Brillo pulsante detrás
        radio_brillo = int(self.ancho * 0.7 * pulse) + 6
        brillo_alpha = int(160 + math.sin(tiempo_vivo * 0.01) * 80)
        brillo_alpha = max(0, min(255, brillo_alpha))
        surf_brillo = pygame.Surface((radio_brillo * 2, radio_brillo * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf_brillo, (255, 220, 50, brillo_alpha),
                           (radio_brillo, radio_brillo), radio_brillo)
        pantalla.blit(surf_brillo, (cx - radio_brillo, cy - radio_brillo))

        # Caja escalada con pulso
        escala_w = max(4, int(self.ancho * pulse))
        escala_h = max(4, int(self.alto * pulse))
        img_scaled = pygame.transform.scale(self.img, (escala_w, escala_h))
        bx = self.x + (self.ancho - escala_w) // 2
        by = self.y + (self.alto - escala_h) // 2
        pantalla.blit(img_scaled, (bx, by))

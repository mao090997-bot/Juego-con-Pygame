import os
import pygame
from config import RUTA_IMAGENES, RUTA_SONIDOS


def cargar_imagen(nombre, ancho, alto):
    ruta = os.path.join(RUTA_IMAGENES, nombre)
    img = pygame.image.load(ruta)
    return pygame.transform.scale(img, (ancho, alto))


def cargar_sonido(nombre, volumen=1.0):
    ruta = os.path.join(RUTA_SONIDOS, nombre)
    s = pygame.mixer.Sound(ruta)
    s.set_volume(volumen)
    return s


def cargar_spritesheet_repartidor():
    ruta = os.path.join(RUTA_IMAGENES, "Reparte.png")
    ss = pygame.image.load(ruta)
    ss = ss.subsurface((179, 25, 221, 374))
    return pygame.transform.scale(ss, (64, 108))

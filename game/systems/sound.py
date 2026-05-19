import pygame
from config import RUTA_SONIDOS, VOL_DISPARO, VOL_GOLPE, VOL_VIDA, VOL_MUSICA
from utils.loaders import cargar_sonido


class SoundManager:
    def __init__(self):
        self.disparo = cargar_sonido("disparo.mp3", VOL_DISPARO)
        self.golpe = cargar_sonido("golpe.mp3", VOL_GOLPE)
        self.vida = cargar_sonido("vida_perdida.mp3", VOL_VIDA)

        pygame.mixer.music.load(self._ruta("MusicaFondo.mp3"))
        pygame.mixer.music.set_volume(VOL_MUSICA)

    def _ruta(self, nombre):
        import os
        return os.path.join(RUTA_SONIDOS, nombre)

    def play_disparo(self):
        self.disparo.play()

    def play_golpe(self):
        self.golpe.play()

    def play_vida(self):
        self.vida.play()

    def iniciar_musica(self):
        pygame.mixer.music.play(-1)

    def stop_musica(self):
        pygame.mixer.music.stop()

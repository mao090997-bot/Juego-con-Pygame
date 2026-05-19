import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.game import Juego

if __name__ == "__main__":
    Juego().ejecutar()

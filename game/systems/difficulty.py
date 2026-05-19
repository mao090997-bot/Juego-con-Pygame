import random
from config import ANCHO, ALTO, INTERVALO_APARICION_INICIAL, INTERVALO_APARICION_MINIMO, \
    VEL_GATO_MULTIPLICADOR, GATO_APARICION_INICIAL_SEG, GATO_ANCHO, GATO_ALTO
from entities.enemy import Perro, Gato
from entities.effects import Particula


def calcular(tiempo_transcurrido):
    segundos = tiempo_transcurrido / 1000.0
    vel_perro = min(2.5 + (segundos / 60.0) * 2.5, 5)
    intervalo = max(INTERVALO_APARICION_INICIAL - segundos * 8,
                    INTERVALO_APARICION_MINIMO)
    return vel_perro, int(intervalo)


def generar_apariciones(tiempo_transcurrido, vel_base):
    segundos = tiempo_transcurrido / 1000
    if segundos < 30:
        cantidad = 1
    elif segundos < 60:
        cantidad = random.randint(1, 2)
    else:
        cantidad = random.randint(2, 3)

    perros = []
    for _ in range(cantidad):
        borde = random.randint(0, 3)
        if borde == 0:
            x, y = random.randint(0, ANCHO), -72
        elif borde == 1:
            x, y = random.randint(0, ANCHO), ALTO
        elif borde == 2:
            x, y = -58, random.randint(0, ALTO)
        else:
            x, y = ANCHO, random.randint(0, ALTO)
        vel = random.uniform(vel_base * 0.8, vel_base * 1.2)
        r = random.random()
        modo = 0 if r < 0.85 else (1 if r < 0.93 else 2)
        perros.append(Perro(x, y, vel, modo))
    return perros


def generar_apariciones_gatos(tiempo_transcurrido, vel_base, gato_img):
    segundos = tiempo_transcurrido / 1000
    if segundos < GATO_APARICION_INICIAL_SEG:
        return []
    if random.random() > 0.25:
        return []

    borde = random.randint(0, 3)
    if borde == 0:
        x, y = random.randint(0, ANCHO), -GATO_ALTO
    elif borde == 1:
        x, y = random.randint(0, ANCHO), ALTO
    elif borde == 2:
        x, y = -GATO_ANCHO, random.randint(0, ALTO)
    else:
        x, y = ANCHO, random.randint(0, ALTO)

    vel = vel_base * VEL_GATO_MULTIPLICADOR * random.uniform(0.9, 1.1)
    return [Gato(x, y, vel, gato_img)]


def crear_explosion(x, y):
    particulas = []
    for _ in range(12):
        particulas.append(Particula(
            x, y,
            random.uniform(-4, 4),
            random.uniform(-4, 4),
            random.randint(20, 40),
            random.randint(3, 6)
        ))
    return particulas

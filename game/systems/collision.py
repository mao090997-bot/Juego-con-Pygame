from utils.helpers import distancia
from entities.effects import HitPopup
from systems.difficulty import crear_explosion as crear_explosion_particulas


def separar_enemigos(enemigos):
    for i in range(len(enemigos)):
        for j in range(i + 1, len(enemigos)):
            dx = enemigos[i].x - enemigos[j].x
            dy = enemigos[i].y - enemigos[j].y
            dist = distancia(enemigos[i].x, enemigos[i].y,
                             enemigos[j].x, enemigos[j].y)
            if 0 < dist < 50:
                separacion = (50 - dist) / 2
                enemigos[i].x += (dx / dist) * separacion
                enemigos[i].y += (dy / dist) * separacion
                enemigos[j].x -= (dx / dist) * separacion
                enemigos[j].y -= (dy / dist) * separacion
    return enemigos


def jugador_con_enemigos(jugador, enemigos, tiempo_actual):
    if jugador.esta_invulnerable(tiempo_actual):
        return enemigos, False

    player_rect = jugador.get_rect()
    for i, enemigo in enumerate(enemigos):
        if player_rect.colliderect(enemigo.get_rect()):
            enemigos.pop(i)
            jugador.vidas -= 1
            jugador.ultimo_dano = tiempo_actual
            game_over = jugador.vidas <= 0
            return enemigos, game_over
    return enemigos, False


def pizzas_con_enemigos(pizzas, enemigos):
    nueva_puntuacion = 0
    hits = []
    particulas = []
    pizzas_restantes = list(pizzas)
    enemigos_restantes = list(enemigos)

    i = 0
    while i < len(pizzas_restantes):
        pizza_rect = pizzas_restantes[i].get_rect()
        eliminar = False
        j = 0
        while j < len(enemigos_restantes):
            if pizza_rect.colliderect(enemigos_restantes[j].get_rect()):
                cx, cy = enemigos_restantes[j].get_centro()
                particulas.extend(crear_explosion_particulas(cx, cy))
                hits.append(HitPopup(enemigos_restantes[j].x, enemigos_restantes[j].y))
                enemigos_restantes.pop(j)
                nueva_puntuacion += 10
                eliminar = True
                break
            else:
                j += 1
        if eliminar:
            pizzas_restantes.pop(i)
        else:
            i += 1

    return pizzas_restantes, enemigos_restantes, nueva_puntuacion, hits, particulas

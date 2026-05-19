import random
import pygame
from config import ANCHO, ALTO, FPS, VEL_REPARTIDOR, VEL_PIZZA, \
    COOLDOWN_DISPARO, MAX_ENERGIA_DASH, GATO_ANCHO, GATO_ALTO, \
    INTERVALO_APARICION_GATO, CAJA_VIDA_INTERVALO_MIN, \
    CAJA_VIDA_INTERVALO_MAX, CAJA_VIDA_MAX_VIDAS, \
    CAJA_VIDA_ANCHO, CAJA_VIDA_ALTO
from core.states import ESTADO_JUGANDO, ESTADO_GAME_OVER
from entities.player import Repartidor
from entities.enemy import Perro, Gato
from entities.projectile import Pizza
from entities.powerup import CajaVida
from systems.sound import SoundManager
from systems.difficulty import calcular as calcular_dificultad, \
    generar_apariciones, generar_apariciones_gatos, crear_explosion
from systems.collision import separar_enemigos, jugador_con_enemigos, \
    pizzas_con_enemigos
from ui.hud import dibujar_hud, dibujar_game_over
from utils.loaders import cargar_imagen, cargar_spritesheet_repartidor
from utils.helpers import distancia


class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Future Pizza")
        icono = cargar_imagen("Piz.png", 32, 32)
        pygame.display.set_icon(icono)

        # Assets
        self.fondo = cargar_imagen("FONDO.png", 1160, 700)
        repartidor_img = cargar_spritesheet_repartidor()
        self.perro_img = cargar_imagen("Perros.png", 58, 72)
        self.gato_img = cargar_imagen("gato.png", GATO_ANCHO, GATO_ALTO)
        self.pizza_img = cargar_imagen("Piz.png", 32, 32)
        self.corazon_img = cargar_imagen("corazon.png", 32, 32)
        self.caja_img = cargar_imagen("caja_pizza.png", CAJA_VIDA_ANCHO, CAJA_VIDA_ALTO)

        # Audio
        self.sound = SoundManager()
        self.sound.iniciar_musica()

        # Entidades
        self.player = Repartidor(repartidor_img)
        self.perros = []
        self.gatos = []
        self.pizzas = []
        self.particulas = []
        self.hits = []
        self.cajas_vida = []

        # Estado
        self.puntuacion = 0
        self.tiempo_inicio = 0
        self.tiempo_transcurrido = 0
        self.estado_juego = ESTADO_JUGANDO
        self.tiempo_sobrevivido = 0
        self.ultimo_disparo = 0
        self.ultima_aparicion = 0
        self.ultima_aparicion_gato = 0
        self.proxima_caja = random.randint(CAJA_VIDA_INTERVALO_MIN, CAJA_VIDA_INTERVALO_MAX)

        # Fuentes (creadas una vez, no cada frame)
        self.fuente_ppal = pygame.font.Font(None, 48)
        self.fuente_hit = pygame.font.Font(None, 28)

        self.reloj = pygame.time.Clock()
        self.se_ejecuta = True

    def ejecutar(self):
        while self.se_ejecuta:
            self.reloj.tick(FPS)
            tiempo_actual = pygame.time.get_ticks()

            if self.tiempo_inicio == 0:
                self.tiempo_inicio = tiempo_actual

            self._manejar_eventos(tiempo_actual)
            if self.estado_juego == ESTADO_JUGANDO:
                self._actualizar(tiempo_actual)
            self._dibujar(tiempo_actual)
            pygame.display.update()
        pygame.quit()

    def _manejar_eventos(self, tiempo_actual):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.se_ejecuta = False

            if self.estado_juego != ESTADO_JUGANDO:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.cambio_x = -VEL_REPARTIDOR
                if event.key == pygame.K_RIGHT:
                    self.player.cambio_x = VEL_REPARTIDOR
                if event.key == pygame.K_UP:
                    self.player.cambio_y = -VEL_REPARTIDOR
                if event.key == pygame.K_DOWN:
                    self.player.cambio_y = VEL_REPARTIDOR
                if event.key == pygame.K_SPACE:
                    self._intentar_disparar(tiempo_actual)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._intentar_disparar(tiempo_actual)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.cambio_x = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.player.cambio_y = 0

    def _actualizar(self, tiempo_actual):
        self.tiempo_transcurrido = tiempo_actual - self.tiempo_inicio

        # Dash
        teclas = pygame.key.get_pressed()
        dash_activo = teclas[pygame.K_RCTRL]
        if dash_activo and self.player.energia_dash > 0:
            multiplicador = 2.5
            self.player.energia_dash -= 1
        else:
            multiplicador = 1
        if not dash_activo and self.player.energia_dash < MAX_ENERGIA_DASH:
            self.player.energia_dash += 0.5
        self.player.mover(multiplicador)

        # Dificultad
        vel_base, intervalo = calcular_dificultad(self.tiempo_transcurrido)

        # Combinar todos los enemigos para procesarlos juntos
        todos = self.perros + self.gatos

        # Todos persiguen al jugador
        for e in todos:
            e.perseguir(self.player.x, self.player.y)

        # Separacion entre enemigos
        todos = separar_enemigos(todos)

        # Colision jugador ↔ enemigos
        todos, game_over = jugador_con_enemigos(
            self.player, todos, tiempo_actual)
        if game_over:
            self.estado_juego = ESTADO_GAME_OVER
            self.tiempo_sobrevivido = self.tiempo_transcurrido
            self.sound.stop_musica()
            return

        # Separar en listas por tipo
        self.perros = [e for e in todos if e.tipo == "perro"]
        self.gatos = [e for e in todos if e.tipo == "gato"]

        # Spawn de perros
        if tiempo_actual - self.ultima_aparicion >= intervalo:
            nuevos = generar_apariciones(self.tiempo_transcurrido, vel_base)
            self.perros.extend(nuevos)
            self.ultima_aparicion = tiempo_actual

        # Spawn de gatos
        if tiempo_actual - self.ultima_aparicion_gato >= INTERVALO_APARICION_GATO:
            nuevos_gatos = generar_apariciones_gatos(
                self.tiempo_transcurrido, vel_base, self.gato_img)
            self.gatos.extend(nuevos_gatos)
            self.ultima_aparicion_gato = tiempo_actual

        # Spawn de caja de vida
        if tiempo_actual >= self.proxima_caja + self.tiempo_inicio:
            x = random.randint(0, ANCHO - 32)
            y = random.randint(0, ALTO - 32)
            self.cajas_vida.append(CajaVida(x, y, self.caja_img, tiempo_actual))
            self.proxima_caja = tiempo_actual + random.randint(
                CAJA_VIDA_INTERVALO_MIN, CAJA_VIDA_INTERVALO_MAX)

        # Colision jugador ↔ caja de vida
        player_rect = self.player.get_rect()
        self.cajas_vida = [c for c in self.cajas_vida
                           if not c.ha_expirado(tiempo_actual)]
        for c in self.cajas_vida[:]:
            if player_rect.colliderect(c.get_rect()):
                if self.player.vidas < CAJA_VIDA_MAX_VIDAS:
                    self.player.vidas += 1
                self.cajas_vida.remove(c)

        # Pizzas: mover + eliminar fuera de pantalla
        for p in self.pizzas:
            p.mover()
        self.pizzas = [p for p in self.pizzas if not p.esta_fuera()]

        # Colision pizza ↔ enemigos (usando lista combinada)
        todos = self.perros + self.gatos
        self.pizzas, todos, pts, nuevos_hits, nuevas_particulas = \
            pizzas_con_enemigos(self.pizzas, todos)
        self.puntuacion += pts
        self.hits.extend(nuevos_hits)
        self.particulas.extend(nuevas_particulas)
        if pts > 0:
            self.sound.play_golpe()

        # Separar de vuelta
        self.perros = [e for e in todos if e.tipo == "perro"]
        self.gatos = [e for e in todos if e.tipo == "gato"]

        # Particulas y hits
        for p in self.particulas:
            p.actualizar()
        self.particulas = [p for p in self.particulas if p.vida > 0]

        for h in self.hits:
            h.actualizar()
        self.hits = [h for h in self.hits if h.timer > 0]

    def _dibujar(self, tiempo_actual):
        self.pantalla.blit(self.fondo, (0, 0))

        # Entidades
        self.player.dibujar(self.pantalla)
        for perro in self.perros:
            perro.dibujar(self.pantalla, self.perro_img)
        for gato in self.gatos:
            gato.dibujar(self.pantalla)
        for c in self.cajas_vida:
            c.dibujar(self.pantalla, tiempo_actual)
        for p in self.pizzas:
            p.dibujar(self.pantalla, self.pizza_img)
        for p in self.particulas:
            p.dibujar(self.pantalla)

        # HUD
        dibujar_hud(self.pantalla, self.player, self.puntuacion,
                    self.tiempo_transcurrido, self.fuente_ppal,
                    self.fuente_hit, self.corazon_img, self.hits)

        # Game over
        if self.estado_juego == ESTADO_GAME_OVER:
            dibujar_game_over(self.pantalla, self.puntuacion,
                              self.tiempo_sobrevivido)

    def _intentar_disparar(self, tiempo_actual):
        if tiempo_actual - self.ultimo_disparo < COOLDOWN_DISPARO:
            return
        self.ultimo_disparo = tiempo_actual

        mouse_x, mouse_y = pygame.mouse.get_pos()
        origen_x = self.player.x + 16
        origen_y = self.player.y + 38
        dx = mouse_x - origen_x
        dy = mouse_y - origen_y
        d = distancia(0, 0, dx, dy)
        if d == 0:
            return
        self.pizzas.append(Pizza(origen_x, origen_y,
                                 (dx / d) * VEL_PIZZA,
                                 (dy / d) * VEL_PIZZA))
        self.sound.play_disparo()

import pygame  # Importa la libreria pygame (community edition)
import random  # Importa random (para posiciones aleatorias del perro)

# ─────────────────────────────────────────────────────────
# INICIALIZACION DE PYGAME
# ─────────────────────────────────────────────────────────
pygame.init()  # Enciende todos los modulos de pygame (video, sonido, eventos, etc.)
pygame.mixer.init()  # Inicializa el modulo de sonido

# ─────────────────────────────────────────────────────────
# VENTANA DEL JUEGO
# ─────────────────────────────────────────────────────────
pantalla = pygame.display.set_mode((1100, 700))  # Crea la ventana de 1100x700 pixeles
pygame.display.set_caption("Future Pizza")      # Texto que aparece en la barra de titulo
icono = pygame.image.load("./Recursos/Piz.png") # Carga la imagen del icono de la ventana
pygame.display.set_icon(icono)                  # Asigna esa imagen como icono de la ventana

# ─────────────────────────────────────────────────────────
# FONDO
# ─────────────────────────────────────────────────────────
fondo = pygame.image.load("./Recursos/FONDO.png")  # Carga la imagen de fondo
fondo = pygame.transform.scale(fondo, (1160, 700))   # Escala el fondo a 1160x700

# ─────────────────────────────────────────────────────────
# REPARTIDOR (jugador)
# ─────────────────────────────────────────────────────────
repartidor_img = pygame.image.load("./Recursos/Reparte.png")           # Carga el spritesheet del repartidor
repartidor_img = repartidor_img.subsurface((179, 25, 221, 374))        # Recorta un rectangulo del spritesheet: (x, y, ancho, alto) -> obtiene solo la imagen del repartidor
repartidor_img = pygame.transform.scale(repartidor_img, (64, 108))     # Escala el recorte a 64x108 pixeles
repartidor_x = 368          # Posicion X inicial del repartidor (centro aproximado de la pantalla)
repartidor_y = 450          # Posicion Y inicial del repartidor (cerca del borde inferior)
repartidor_cambio_x = 0     # Velocidad horizontal actual del repartidor (0 = quieto)
repartidor_cambio_y = 0     # Velocidad vertical actual del repartidor (0 = quieto)
velocidad_repartidor = 4    # Pixeles que avanza el repartidor por frame cuando se mueve

# ─────────────────────────────────────────────────────────
# PERROS (enemigos)
# ─────────────────────────────────────────────────────────
perro_img = pygame.image.load("./Recursos/Perros.png")             # Carga el spritesheet del perro
perro_img = pygame.transform.scale(perro_img, (58, 72))            # Escala la imagen del perro a 58x72 pixeles
velocidad_perro = 4            # Pixeles que avanza cada perro por frame hacia el repartidor
perros = []                    # Lista de perros, cada perro es [x, y]

# ─────────────────────────────────────────────────────────
# PARTICULAS (efectos visuales)
# ─────────────────────────────────────────────────────────
particulas = []                # Lista de particulas: [x, y, vx, vy, vida, tamaño]

# ─────────────────────────────────────────────────────────
# PIZZAS (proyectiles)
# ─────────────────────────────────────────────────────────
pizza_img = pygame.image.load("./Recursos/Piz.png")   # Carga la imagen de la pizza
pizza_img = pygame.transform.scale(pizza_img, (32, 32))  # Escala la pizza a 32x32 pixeles

# ─────────────────────────────────────────────────────────
# CORAZONES (VIDAS DEL JUGADOR)
# ─────────────────────────────────────────────────────────
# Se dibujarán como círculos en lugar de importar una imagen que no existe

velocidad_pizza = 11   # Pixeles que avanza CADA pizza por frame en la direccion en que fue lanzada

pizzas_x  = []  # Lista: coordenada X de cada pizza activa
pizzas_y  = []  # Lista: coordenada Y de cada pizza activa
pizzas_dx = []  # Lista: velocidad X (direccion X * velocidad_pizza) de cada pizza
pizzas_dy = []  # Lista: velocidad Y (direccion Y * velocidad_pizza) de cada pizza
# Las 4 listas tienen el mismo largo. pizzas_x[i], pizzas_y[i], pizzas_dx[i], pizzas_dy[i]
# representan una sola pizza. Se agregan y eliminan en simultaneo.

# ─────────────────────────────────────────────────────────
# PUNTUACION Y PROGRESION
# ─────────────────────────────────────────────────────────
puntuacion = 0              # Puntos por eliminar perros
tiempo_inicio = 0           # Momento en que comenzo el juego

# ─────────────────────────────────────────────────────────
# CONTROL DE FPS Y TEMPORIZADOR DE DISPARO
# ─────────────────────────────────────────────────────────
reloj = pygame.time.Clock()  # Reloj que limita los FPS del juego
FPS = 60                     # El juego correra a 60 cuadros por segundo
# El disparo ahora es manual (clic izquierdo)
ultimo_disparo = 0           # Momento del ultimo disparo (para cooldown)
cooldown_disparo = 180       # Milisegundos entre disparos
ultima_aparicion = 0         # Momento (en ms) de la ultima aparicion de un perro
intervalo_aparicion = 2000   # Aparece un nuevo perro cada 2000 ms (= 2 segundos)
intervalo_aparicion_minimo = 800  # Minimo intervalo entre apariciones (800ms)

# ─────────────────────────────────────────────────────────
# VIDAS
# ─────────────────────────────────────────────────────────
vidas = 3                  # El jugador comienza con 3 vidas
ultimo_dano = 0            # Momento del ultimo dano recibido (en ms)
intervalo_invulnerabilidad = 1000  # 1 segundo de invulnerabilidad tras ser golpeado
game_over = False

# ─────────────────────────────────────────────────────────
# SONIDOS
# ─────────────────────────────────────────────────────────
sonido_disparo = pygame.mixer.Sound("./Music/disparo.mp3")
sonido_golpe = pygame.mixer.Sound("./Music/golpe.mp3")
sonido_vida = pygame.mixer.Sound("./Music/vida_perdida.mp3")
sonido_disparo.set_volume(0.4)
sonido_golpe.set_volume(0.6)
sonido_vida.set_volume(0.8)
musica_fondo = "./Music/MusicaFondo.mp3"

pygame.mixer.music.load(musica_fondo)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ─────────────────────────────────────────────────────────
# DASH (stamina)
# ─────────────────────────────────────────────────────────
energia_dash = 100          # 0-100, se gasta al hacer dash
MAX_ENERGIA_DASH = 100

# ─────────────────────────────────────────────────────────
# SCORE POPUPS (texto +10 flotante)
# ─────────────────────────────────────────────────────────
hits = []  # [x, y, timer]

# ─────────────────────────────────────────────────────────
# FUNCIONES DE DIBUJADO
# ─────────────────────────────────────────────────────────
def repartidor(x, y):
    """Dibuja al repartidor en la posicion (x, y) de la pantalla."""
    pantalla.blit(repartidor_img, (x, y))  # blit = pegar una imagen sobre la superficie de la pantalla


def perro(x, y):
    """Dibuja al perro en la posicion (x, y) de la pantalla."""
    pantalla.blit(perro_img, (x, y))


def pizza(x, y):
    """Dibuja una pizza en la posicion (x, y) de la pantalla."""
    pantalla.blit(pizza_img, (x, y))



# ─────────────────────────────────────────────────────────
# FUNCION: ENCONTRAR AL PERRO MAS CERCANO
# ─────────────────────────────────────────────────────────
def encontrar_perro_mas_cercano(origen_x, origen_y):
    """
    Recorre la lista global 'perros' y devuelve la posicion (x, y)
    y la distancia del perro mas cercano a (origen_x, origen_y).
    Devuelve: (x_del_perro, y_del_perro, distancia_euclidea)
    Si no hay perros devuelve (origen_x, origen_y, 0).
    """
    global perros
    if len(perros) == 0:
        return origen_x, origen_y, 0

    mejor_x = perros[0][0]
    mejor_y = perros[0][1]
    mejor_dist = (mejor_x - origen_x) ** 2 + (mejor_y - origen_y) ** 2

    for i in range(1, len(perros)):
        dx = perros[i][0] - origen_x
        dy = perros[i][1] - origen_y
        dist_cuad = dx ** 2 + dy ** 2
        if dist_cuad < mejor_dist:
            mejor_dist = dist_cuad
            mejor_x = perros[i][0]
            mejor_y = perros[i][1]

    return mejor_x, mejor_y, mejor_dist ** 0.5


# ─────────────────────────────────────────────────────────
# FUNCION: DISPARAR UNA PIZZA
# ─────────────────────────────────────────────────────────
def disparar_pizza(origen_x, origen_y):
    """
    Crea una nueva pizza en la posicion (origen_x, origen_y) que viajara
    en linea recta hacia la posicion del mouse a velocidad_pizza pixeles/frame.
    """
    global pizzas_x, pizzas_y, pizzas_dx, pizzas_dy  # Vamos a MODIFICAR las listas de pizzas

    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - origen_x
    dy = mouse_y - origen_y
    dist = (dx ** 2 + dy ** 2) ** 0.5

    if dist == 0:   # Si el mouse esta exactamente encima del origen
        return      # No dispara, evitaria division por cero

    norm_x = dx / dist  # Vector unitario X
    norm_y = dy / dist  # Vector unitario Y

    pizzas_x.append(origen_x + 16)   # Agrega una pizza centrada en X respecto al repartidor (64/2 = 32, 32/2 = 16 de offset)
    pizzas_y.append(origen_y + 38)   # Agrega una pizza centrada en Y respecto al repartidor (108/2 = 54, 32/2 = 16, offset ~38)
    pizzas_dx.append(norm_x * velocidad_pizza)  # Velocidad X de esta pizza: direccion * rapidez constante
    pizzas_dy.append(norm_y * velocidad_pizza)  # Velocidad Y de esta pizza: direccion * rapidez constante


# ─────────────────────────────────────────────────────────
# FUNCION: ACTUALIZAR POSICION DE TODAS LAS PIZZAS
# ─────────────────────────────────────────────────────────
def actualizar_pizzas():
    """
    Mueve todas las pizzas activas una posicion hacia adelante (segun su dx/dy).
    Elimina aquellas que se salen completamente de la pantalla.
    """
    global pizzas_x, pizzas_y, pizzas_dx, pizzas_dy  # Vamos a MODIFICAR las listas

    i = 0  # Indice para recorrer la lista manualmente (usamos while porque la lista cambia de tamaño al hacer pop)
    while i < len(pizzas_x):
        pizzas_x[i] += pizzas_dx[i]  # Avanza la pizza en X segun su velocidad
        pizzas_y[i] += pizzas_dy[i]  # Avanza la pizza en Y segun su velocidad

        # Verifica si la pizza salio de la pantalla (con un margen de 32px = su propio tamaño)
        if (pizzas_x[i] < -32 or pizzas_x[i] > 1100 or   # Fuera de los bordes izquierdo o derecho
            pizzas_y[i] < -32 or pizzas_y[i] > 700):    # Fuera de los bordes superior o inferior
            # Elimina la pizza de las 4 listas simultaneamente
            pizzas_x.pop(i)
            pizzas_y.pop(i)
            pizzas_dx.pop(i)
            pizzas_dy.pop(i)
            # NO incrementamos i porque al eliminar, el elemento que estaba en i+1 ahora esta en i
        else:
            i += 1  # Solo avanzamos si no eliminamos, para no saltarnos ninguna pizza


# ─────────────────────────────────────────────────────────
# FUNCION: DIBUJAR TODAS LAS PIZZAS EN PANTALLA
# ─────────────────────────────────────────────────────────
def dibujar_pizzas():
    """Recorre la lista de pizzas activas y dibuja cada una en su posicion."""
    for i in range(len(pizzas_x)):
        pizza(pizzas_x[i], pizzas_y[i])  # Llama a la funcion pizza() que hace blit de la imagen


def dibujar_vidas():
    """Dibuja los corazones de vidas restantes en la esquina superior izquierda."""
    for i in range(vidas):
        pygame.draw.circle(pantalla, (255, 0, 0), (25 + i * 40, 25), 12)


def calcular_dificultad(tiempo_transcurrido):
    """
    Calcula parametros de dificultad segun el tiempo de juego.
    A mayor tiempo, mas veloces los perros y mas frecuentes las apariciones.
    """
    segundos = tiempo_transcurrido / 1000.0
    
    # Velocidad de perros: aumenta gradualmente (2.5 -> 5 max)
    vel_perro = 2.5 + (segundos / 60.0) * 2.5
    vel_perro = min(vel_perro, 5)
    
    # Intervalo de aparicion: decrece (2000ms -> 800ms)
    inter_aparicion = max(2000 - segundos * 8, intervalo_aparicion_minimo)
    
    return vel_perro, inter_aparicion


def dibujar_puntuacion():
    """Dibuja la puntuación en la esquina superior derecha."""
    fuente = pygame.font.Font(None, 48)
    texto = fuente.render(f"Puntos: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (1100 - texto.get_width() - 20, 15))


def crear_explosion(x, y):
    """Crea particulas en la posicion (x, y) simulando una explosion."""
    global particulas
    for _ in range(12):
        vx = random.uniform(-4, 4)
        vy = random.uniform(-4, 4)
        vida = random.randint(20, 40)
        tamaño = random.randint(3, 6)
        particulas.append([x, y, vx, vy, vida, tamaño])


def actualizar_particulas():
    """Mueve las particulas y elimina las que se apagaron."""
    global particulas
    i = 0
    while i < len(particulas):
        particulas[i][0] += particulas[i][2]  # x += vx
        particulas[i][1] += particulas[i][3]  # y += vy
        particulas[i][4] -= 1                 # vida -= 1
        if particulas[i][4] <= 0:
            particulas.pop(i)
        else:
            i += 1


def dibujar_particulas():
    """Dibuja las particulas activas como circulos de colores."""
    for p in particulas:
        vida_ratio = p[4] / 40
        if vida_ratio > 0.5:
            color = (255, 200, 0)  # amarillo
        else:
            color = (255, 100, 0)  # naranja
        pygame.draw.circle(pantalla, color, (int(p[0]), int(p[1])), int(p[5]))


# ─────────────────────────────────────────────────────────
# FUNCION: DIBUJAR TODOS LOS PERROS
# ─────────────────────────────────────────────────────────
def dibujar_perros():
    """Recorre la lista de perros y dibuja cada uno en su posicion."""
    for i in range(len(perros)):
        perro(perros[i][0], perros[i][1])


# ─────────────────────────────────────────────────────────
# FUNCION: APARECER UN NUEVO PERRO
# ─────────────────────────────────────────────────────────
def aparecer_perro():
    """
    Crea un nuevo perro en un borde aleatorio de la pantalla.
    Bordes: arriba, abajo, izquierda, derecha (justo fuera de la pantalla).
    """
    global perros
    borde = random.randint(0, 3)
    if borde == 0:  # Arriba
        x = random.randint(0, 1100)
        y = -72
    elif borde == 1:  # Abajo
        x = random.randint(0, 1100)
        y = 700
    elif borde == 2:  # Izquierda
        x = -58
        y = random.randint(0, 700)
    else:  # Derecha
        x = 1100
        y = random.randint(0, 700)
    tipo = random.randint(1, 10)
    if tipo <= 7:
        velocidad = random.uniform(2.2, 3.2)
    else:
        velocidad = random.uniform(4, 5)
    r = random.random()
    if r < 0.85:
        modo = 0      # directo
    elif r < 0.93:
        modo = 1      # flanqueo izquierda
    else:
        modo = 2      # flanqueo derecha
    perros.append([x, y, velocidad, modo])

def detectar_colisiones():
    global pizzas_x, pizzas_y, pizzas_dx, pizzas_dy, perros, puntuacion

    i = 0
    while i < len(pizzas_x):
        pizza_rect = pygame.Rect(pizzas_x[i], pizzas_y[i], 32, 32)
        eliminar_pizza = False
        j = 0
        while j < len(perros):
            perro_rect = pygame.Rect(perros[j][0], perros[j][1], 58, 72)
            if pizza_rect.colliderect(perro_rect):
                crear_explosion(perros[j][0] + 29, perros[j][1] + 36)
                hits.append([perros[j][0], perros[j][1], 30])
                sonido_golpe.play()
                perros.pop(j)
                puntuacion += 10  # +10 puntos por cada perro eliminado
                eliminar_pizza = True
                break
            else:
                j += 1
        if eliminar_pizza:
            pizzas_x.pop(i)
            pizzas_y.pop(i)
            pizzas_dx.pop(i)
            pizzas_dy.pop(i)
        else:
            i += 1

# ─────────────────────────────────────────────────────────
# BUCLE PRINCIPAL DEL JUEGO
# ─────────────────────────────────────────────────────────
se_ejecuta = True  # Bandera que controla si el juego sigue corriendo. Se pone False al cerrar la ventana.

while se_ejecuta:

    # ── CONTROL DE FPS Y TIEMPO ──
    reloj.tick(FPS)                     # Pausa el bucle lo necesario para que solo se ejecute 60 veces por segundo
    tiempo_actual = pygame.time.get_ticks()  # Obtiene los milisegundos transcurridos desde que se llamo a pygame.init()
    
    if tiempo_inicio == 0:
        tiempo_inicio = tiempo_actual

    # ── MANEJO DE EVENTOS (teclado, cierre de ventana) ──
    for event in pygame.event.get():     # Obtiene TODOS los eventos ocurridos desde el ultimo frame

        if event.type == pygame.QUIT:    # Si el usuario hizo clic en la X de la ventana
            se_ejecuta = False           # Termina el bucle principal

        if event.type == pygame.KEYDOWN:  # Cuando se PRESIONA una tecla
            if event.key == pygame.K_LEFT:    # Flecha izquierda
                repartidor_cambio_x = -velocidad_repartidor  # Empieza a moverse a la izquierda (negativo)
            if event.key == pygame.K_RIGHT:   # Flecha derecha
                repartidor_cambio_x = velocidad_repartidor   # Empieza a moverse a la derecha (positivo)
            if event.key == pygame.K_UP:      # Flecha arriba
                repartidor_cambio_y = -velocidad_repartidor  # Empieza a moverse hacia arriba (negativo)
            if event.key == pygame.K_DOWN:    # Flecha abajo
                repartidor_cambio_y = velocidad_repartidor   # Empieza a moverse hacia abajo (positivo)
            if event.key == pygame.K_SPACE:   # Barra espaciadora
                if not game_over and tiempo_actual - ultimo_disparo >= cooldown_disparo:
                    disparar_pizza(repartidor_x, repartidor_y)
                    sonido_disparo.play()
                    ultimo_disparo = tiempo_actual

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo
            if not game_over and tiempo_actual - ultimo_disparo >= cooldown_disparo:
                disparar_pizza(repartidor_x, repartidor_y)
                sonido_disparo.play()
                ultimo_disparo = tiempo_actual

        if event.type == pygame.KEYUP:    # Cuando se SUELTA una tecla
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):  # Si era izquierda o derecha
                repartidor_cambio_x = 0    # Detiene el movimiento horizontal
            if event.key in (pygame.K_UP, pygame.K_DOWN):     # Si era arriba o abajo
                repartidor_cambio_y = 0    # Detiene el movimiento vertical

    # ── MOVIMIENTO DEL REPARTIDOR ──
    teclas = pygame.key.get_pressed()
    dash_activo = teclas[pygame.K_RCTRL]
    if dash_activo and energia_dash > 0:
        multiplicador_dash = 2.5
        energia_dash -= 1
    else:
        multiplicador_dash = 1
    if not dash_activo and energia_dash < MAX_ENERGIA_DASH:
        energia_dash += 0.5
    repartidor_x += repartidor_cambio_x * multiplicador_dash  # Actualiza posicion X sumando la velocidad actual
    repartidor_y += repartidor_cambio_y * multiplicador_dash  # Actualiza posicion Y sumando la velocidad actual

    # ── LIMITES DE PANTALLA PARA EL REPARTIDOR ──
    if repartidor_x < 0:        # Si se sale por el borde izquierdo
        repartidor_x = 0        # Lo fija en el borde
    elif repartidor_x > 1036:   # Si se sale por el borde derecho (1100 - 64)
        repartidor_x = 1036     # Lo fija en el borde
    if repartidor_y < 0:        # Si se sale por el borde superior
        repartidor_y = 0        # Lo fija en el borde
    elif repartidor_y > 592:    # Si se sale por el borde inferior (700 - 108)
        repartidor_y = 592      # Lo fija en el borde

    # ── CALCULAR DIFICULTAD ACTUAL ──
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    vel_perro_actual, intervalo_aparicion_actual = calcular_dificultad(tiempo_transcurrido)
    # ── MOVIMIENTO DE LOS PERROS (PERSIGUEN AL REPARTIDOR) ──
    for i in range(len(perros)):
        dx = repartidor_x - perros[i][0]  # Diferencia en X entre repartidor y este perro
        dy = repartidor_y - perros[i][1]  # Diferencia en Y entre repartidor y este perro
        distancia = (dx ** 2 + dy ** 2) ** 0.5  # Distancia euclidea entre ambos
        if distancia > 0:  # Si la distancia es mayor a 0 (no estan exactamente en el mismo pixel)
            velocidad_final = perros[i][2]
            modo = perros[i][3]
            if modo != 0 and distancia > 120:
                nx = dx / distancia
                ny = dy / distancia
                lado = -1 if modo == 1 else 1
                flanco_x = repartidor_x + (-ny * lado) * 100
                flanco_y = repartidor_y + (nx * lado) * 100
                fdx = flanco_x - perros[i][0]
                fdy = flanco_y - perros[i][1]
                fdist = (fdx ** 2 + fdy ** 2) ** 0.5
                if fdist > 0:
                    perros[i][0] += (fdx / fdist) * velocidad_final
                    perros[i][1] += (fdy / fdist) * velocidad_final
            else:
                perros[i][0] += (dx / distancia) * velocidad_final
                perros[i][1] += (dy / distancia) * velocidad_final

    # ── COLISION PERRO ↔ PERRO (SE EMPUJAN) ──
    for i in range(len(perros)):
        for j in range(i + 1, len(perros)):
            dx = perros[i][0] - perros[j][0]
            dy = perros[i][1] - perros[j][1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < 50 and dist > 0:
                separacion = (50 - dist) / 2
                perros[i][0] += (dx / dist) * separacion
                perros[i][1] += (dy / dist) * separacion
                perros[j][0] -= (dx / dist) * separacion
                perros[j][1] -= (dy / dist) * separacion

    # ── COLISION REPARTIDOR ↔ PERROS (PIERDE VIDA) ──
    if tiempo_actual - ultimo_dano >= intervalo_invulnerabilidad:
        repartidor_rect = pygame.Rect(repartidor_x + 12, repartidor_y + 20, 40, 70)
        i = 0
        while i < len(perros):
            perro_rect = pygame.Rect(perros[i][0], perros[i][1], 58, 72)
            if repartidor_rect.colliderect(perro_rect):
                    perros.pop(i)
                    vidas -= 1
                    sonido_vida.play()
                    ultimo_dano = tiempo_actual
                    if vidas <= 0:
                        game_over = True
                    break
            else:
                i += 1

    # ── APARICION DE NUEVOS PERROS (GRUPOS) ──
    if tiempo_actual - ultima_aparicion >= intervalo_aparicion_actual:
        segundos = tiempo_transcurrido / 1000
        if segundos < 30:
            cantidad = 1
        elif segundos < 60:
            cantidad = random.randint(1, 2)
        else:
            cantidad = random.randint(2, 3)
        for _ in range(cantidad):
            aparecer_perro()
        ultima_aparicion = tiempo_actual

    # ── ACTUALIZAR POSICION DE LAS PIZZAS ──
    actualizar_pizzas()  # Mueve todas las pizzas y elimina las que salieron de pantalla

    detectar_colisiones()

    actualizar_particulas()

    # ── ACTUALIZAR SCORE POPUPS ──
    i = 0
    while i < len(hits):
        hits[i][2] -= 1
        hits[i][1] -= 1  # flota hacia arriba
        if hits[i][2] <= 0:
            hits.pop(i)
        else:
            i += 1

    # ── DIBUJADO DE TODO EL CUADRO ──
    pantalla.blit(fondo, (0, 0))        # Dibuja el fondo primero (debajo de todo)
    repartidor(repartidor_x, repartidor_y)  # Dibuja al repartidor encima del fondo
    dibujar_perros()                    # Dibuja todos los perros
    dibujar_pizzas()                    # Dibuja todas las pizzas activas
    dibujar_vidas()                     # Dibuja los corazones de vidas restantes
    dibujar_puntuacion()                # Dibuja la puntuación en la esquina superior derecha
    # ── DIBUJAR SCORE POPUPS (+10 flotante) ──
    fuente_hit = pygame.font.Font(None, 28)
    for h in hits:
        texto_hit = fuente_hit.render("+10", True, (255, 255, 100))
        pantalla.blit(texto_hit, (h[0] + 10, h[1]))
    # ── DIBUJAR BARRA DE DASH ──
    ancho_barra = 80
    alto_barra = 8
    x_barra = 10
    y_barra = 60
    pygame.draw.rect(pantalla, (60, 60, 60), (x_barra, y_barra, ancho_barra, alto_barra))
    ancho_lleno = int(ancho_barra * (energia_dash / MAX_ENERGIA_DASH))
    color_dash = (0, 200, 255) if energia_dash > 30 else (255, 100, 0)
    pygame.draw.rect(pantalla, color_dash, (x_barra, y_barra, ancho_lleno, alto_barra))
    dibujar_particulas()                # Dibuja las particulas de explosion

    if game_over:
        pygame.mixer.music.stop()
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("GAME OVER", True, (255, 0, 0))
        pantalla.blit(texto, (550 - texto.get_width() // 2, 350 - texto.get_height() // 2))

    pygame.display.update()             # Actualiza la pantalla para que se vea todo lo dibujado

# ── SALIDA DEL JUEGO ──
pygame.quit()  # Apaga todos los modulos de pygame y cierra la ventana

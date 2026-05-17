import pygame  # Importa la libreria pygame (community edition)
import random  # Importa random (para posiciones aleatorias del perro)

# ─────────────────────────────────────────────────────────
# INICIALIZACION DE PYGAME
# ─────────────────────────────────────────────────────────
pygame.init()  # Enciende todos los modulos de pygame (video, sonido, eventos, etc.)

# ─────────────────────────────────────────────────────────
# VENTANA DEL JUEGO
# ─────────────────────────────────────────────────────────
pantalla = pygame.display.set_mode((800, 600))  # Crea la ventana de 800x600 pixeles
pygame.display.set_caption("Future Pizza")      # Texto que aparece en la barra de titulo
icono = pygame.image.load("./Recursos/Piz.png") # Carga la imagen del icono de la ventana
pygame.display.set_icon(icono)                  # Asigna esa imagen como icono de la ventana

# ─────────────────────────────────────────────────────────
# FONDO
# ─────────────────────────────────────────────────────────
fondo = pygame.image.load("./Recursos/FONDO.png")  # Carga la imagen de fondo
fondo = pygame.transform.scale(fondo, (860, 600))   # Escala el fondo a 860x600 (un poco mas ancho que la pantalla para cubrir bordes)

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
velocidad_repartidor = 3    # Pixeles que avanza el repartidor por frame cuando se mueve

# ─────────────────────────────────────────────────────────
# PERROS (enemigos)
# ─────────────────────────────────────────────────────────
perro_img = pygame.image.load("./Recursos/Perros.png")             # Carga el spritesheet del perro
perro_img = pygame.transform.scale(perro_img, (58, 72))            # Escala la imagen del perro a 58x72 pixeles
velocidad_perro = 2            # Pixeles que avanza cada perro por frame hacia el repartidor
perros = []                    # Lista de perros, cada perro es [x, y]

# ─────────────────────────────────────────────────────────
# PIZZAS (proyectiles)
# ─────────────────────────────────────────────────────────
pizza_img = pygame.image.load("./Recursos/Piz.png")   # Carga la imagen de la pizza
pizza_img = pygame.transform.scale(pizza_img, (32, 32))  # Escala la pizza a 32x32 pixeles
velocidad_pizza = 8   # Pixeles que avanza CADA pizza por frame en la direccion en que fue lanzada

pizzas_x  = []  # Lista: coordenada X de cada pizza activa
pizzas_y  = []  # Lista: coordenada Y de cada pizza activa
pizzas_dx = []  # Lista: velocidad X (direccion X * velocidad_pizza) de cada pizza
pizzas_dy = []  # Lista: velocidad Y (direccion Y * velocidad_pizza) de cada pizza
# Las 4 listas tienen el mismo largo. pizzas_x[i], pizzas_y[i], pizzas_dx[i], pizzas_dy[i]
# representan una sola pizza. Se agregan y eliminan en simultaneo.

# ─────────────────────────────────────────────────────────
# CONTROL DE FPS Y TEMPORIZADOR DE DISPARO
# ─────────────────────────────────────────────────────────
reloj = pygame.time.Clock()  # Reloj que limita los FPS del juego
FPS = 60                     # El juego correra a 60 cuadros por segundo
ultimo_disparo = 0           # Momento (en milisegundos) del ultimo disparo de pizza
intervalo_disparo = 1000     # Se dispara una pizza cada 1000 ms (= 1 segundo)
ultima_aparicion = 0         # Momento (en ms) de la ultima aparicion de un perro
intervalo_aparicion = 3000   # Aparece un nuevo perro cada 3000 ms (= 3 segundos)


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
    en linea recta hacia el perro mas cercano a velocidad_pizza pixeles/frame.
    """
    global pizzas_x, pizzas_y, pizzas_dx, pizzas_dy  # Vamos a MODIFICAR las listas de pizzas

    dest_x, dest_y, dist = encontrar_perro_mas_cercano(origen_x, origen_y)  # Obtiene el objetivo

    if dist == 0:   # Si la distancia es 0 (el perro esta exactamente encima del origen)
        return      # No dispara, evitaria division por cero

    norm_x = (dest_x - origen_x) / dist  # Vector unitario X: componente X de la direccion normalizada (valor entre -1 y 1)
    norm_y = (dest_y - origen_y) / dist  # Vector unitario Y: componente Y de la direccion normalizada (valor entre -1 y 1)
    # norm_x y norm_y forman un vector de longitud 1 que apunta hacia el perro

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
        if (pizzas_x[i] < -32 or pizzas_x[i] > 800 or   # Fuera de los bordes izquierdo o derecho
            pizzas_y[i] < -32 or pizzas_y[i] > 600):    # Fuera de los bordes superior o inferior
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
        x = random.randint(0, 800)
        y = -72
    elif borde == 1:  # Abajo
        x = random.randint(0, 800)
        y = 600
    elif borde == 2:  # Izquierda
        x = -58
        y = random.randint(0, 600)
    else:  # Derecha
        x = 800
        y = random.randint(0, 600)
    perros.append([x, y])


# ─────────────────────────────────────────────────────────
# BUCLE PRINCIPAL DEL JUEGO
# ─────────────────────────────────────────────────────────
se_ejecuta = True  # Bandera que controla si el juego sigue corriendo. Se pone False al cerrar la ventana.

while se_ejecuta:

    # ── CONTROL DE FPS Y TIEMPO ──
    reloj.tick(FPS)                     # Pausa el bucle lo necesario para que solo se ejecute 60 veces por segundo
    tiempo_actual = pygame.time.get_ticks()  # Obtiene los milisegundos transcurridos desde que se llamo a pygame.init()

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

        if event.type == pygame.KEYUP:    # Cuando se SUELTA una tecla
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):  # Si era izquierda o derecha
                repartidor_cambio_x = 0    # Detiene el movimiento horizontal
            if event.key in (pygame.K_UP, pygame.K_DOWN):     # Si era arriba o abajo
                repartidor_cambio_y = 0    # Detiene el movimiento vertical

    # ── MOVIMIENTO DEL REPARTIDOR ──
    repartidor_x += repartidor_cambio_x  # Actualiza posicion X sumando la velocidad actual
    repartidor_y += repartidor_cambio_y  # Actualiza posicion Y sumando la velocidad actual

    # ── LIMITES DE PANTALLA PARA EL REPARTIDOR ──
    if repartidor_x < 0:        # Si se sale por el borde izquierdo
        repartidor_x = 0        # Lo fija en el borde
    elif repartidor_x > 736:    # Si se sale por el borde derecho (800 - 64 = 736)
        repartidor_x = 736      # Lo fija en el borde
    if repartidor_y < 0:        # Si se sale por el borde superior
        repartidor_y = 0        # Lo fija en el borde
    elif repartidor_y > 492:    # Si se sale por el borde inferior (600 - 108 = 492)
        repartidor_y = 492      # Lo fija en el borde
    # 736 y 492 son 800-64 y 600-108 respectivamente (tamaño del sprite del repartidor)

    # ── MOVIMIENTO DE LOS PERROS (PERSIGUEN AL REPARTIDOR) ──
    for i in range(len(perros)):
        dx = repartidor_x - perros[i][0]  # Diferencia en X entre repartidor y este perro
        dy = repartidor_y - perros[i][1]  # Diferencia en Y entre repartidor y este perro
        distancia = (dx ** 2 + dy ** 2) ** 0.5  # Distancia euclidea entre ambos
        if distancia > 0:  # Si la distancia es mayor a 0 (no estan exactamente en el mismo pixel)
            perros[i][0] += (dx / distancia) * velocidad_perro  # mueve al perro hacia el repartidor en X
            perros[i][1] += (dy / distancia) * velocidad_perro  # mueve al perro hacia el repartidor en Y

    # ── APARICION DE NUEVOS PERROS (CADA 3 SEGUNDOS) ──
    if tiempo_actual - ultima_aparicion >= intervalo_aparicion:
        aparecer_perro()
        ultima_aparicion = tiempo_actual

    # ── DISPARO AUTOMATICO DE PIZZA (CADA 1 SEGUNDO) ──
    if tiempo_actual - ultimo_disparo >= intervalo_disparo:  # Si paso al menos 1 segundo desde el ultimo disparo
        disparar_pizza(repartidor_x, repartidor_y)  # Crea una nueva pizza desde la posicion del repartidor
        ultimo_disparo = tiempo_actual              # Reinicia el contador para el proximo disparo

    # ── ACTUALIZAR POSICION DE LAS PIZZAS ──
    actualizar_pizzas()  # Mueve todas las pizzas y elimina las que salieron de pantalla

    # ── DIBUJADO DE TODO EL CUADRO ──
    pantalla.blit(fondo, (0, 0))        # Dibuja el fondo primero (debajo de todo)
    repartidor(repartidor_x, repartidor_y)  # Dibuja al repartidor encima del fondo
    dibujar_perros()                    # Dibuja todos los perros
    dibujar_pizzas()                    # Dibuja todas las pizzas activas
    pygame.display.update()             # Actualiza la pantalla para que se vea todo lo dibujado

# ── SALIDA DEL JUEGO ──
pygame.quit()  # Apaga todos los modulos de pygame y cierra la ventana

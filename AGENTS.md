# AGENTS.md — Future Pizza (Pygame)

**Contexto para asistentes de IA:** Este es un juego de acción hecho con Pygame donde el jugador controla a un repartidor de pizzas que se defiende de perros atacantes usando pizzas como proyectiles. **Todo el código está en `game/` — arquitectura modular.**

## Inicio rápido

```bash
pip install pygame-ce   # Community Edition, NO "pygame"
python game/main.py
```

Ventana: **1100×700 píxeles**
FPS: **60 (fijados con Clock)**

---

## Estructura del proyecto

```
/game
├── main.py                     # Entry point: python game/main.py
├── config.py                   # Todas las constantes y rutas de assets
│
├── core/
│   ├── game.py                 # class Juego — orquestador y game loop
│   └── states.py               # ESTADO_JUGANDO, ESTADO_GAME_OVER
│
├── entities/
│   ├── player.py               # class Repartidor
│   ├── enemy.py                # class Perro (IA de persecución + flanqueo)
│   ├── projectile.py           # class Pizza
│   └── effects.py              # class Particula, class HitPopup
│
├── systems/
│   ├── collision.py            # Funciones de colisión puras (sin mutación)
│   ├── difficulty.py           # Cálculo de dificultad, spawn de enemigos, explosiones
│   └── sound.py                # class SoundManager
│
├── ui/
│   └── hud.py                  # dibujar_hud(), dibujar_game_over()
│
├── utils/
│   ├── helpers.py              # distancia(x1,y1,x2,y2)
│   └── loaders.py              # cargar_imagen(), cargar_sonido(), spritesheet
│
└── assets/
    ├── images/                 # Sprites PNG (antes Recursos/)
    │   ├── FONDO.png           # fondo (escalado 1160×700)
    │   ├── Reparte.png         # spritesheet; subsurface(179,25,221,374)→64×108
    │   ├── Perros.png          # sprite del perro (escalado 58×72)
    │   ├── Piz.png             # sprite de pizza (32×32; también ícono de ventana)
    │   └── corazon.png         # ícono de corazón para vidas (32×32)
    └── sounds/                 # Audio MP3 (antes Music/)
        ├── disparo.mp3         # volumen 0.4 — sonido al disparar
        ├── golpe.mp3           # volumen 0.6 — sonido al golpear
        ├── vida_perdida.mp3    # volumen 0.8 — sonido al perder vida
        └── MusicaFondo.mp3     # volumen 0.5 — música de fondo en bucle
```

---

## Mecánicas principales del juego

### **Jugador: Repartidor**
- **Sprite:** 64×108 píxeles, aparece en (368, 450)
- **Controles:** Flechas del teclado (movimiento de 4px/frame)
  - `VEL_REPARTIDOR = 4`
  - Posición/velocidad en el objeto `Repartidor`
- **Vidas:** Empieza con `vidas = 3`
- **Invencibilidad:** 1 segundo (`INTERVALO_INVULNERABILIDAD = 1000`) después de recibir daño
- **Dash/Energía:** `energia_dash` (0–100, se recarga con el tiempo), se activa con Ctrl Derecho

### **Enemigos: Perros**
- **Sprite:** 58×72 píxeles
- **Comportamiento:** Persiguen al repartidor con flanqueo opcional (modo 1/2)
- **Dificultad dinámica:**
  - Velocidad aumenta de 2.5 a 5 px/frame mediante `systems/difficulty.calcular()`
  - Intervalo de aparición disminuye de 2000ms a 800ms (mínimo)
- **Aparición:** Bordes aleatorios de la pantalla cada intervalo (controlado por dificultad)
- **Colisión:** Usa `colliderect` basado en `get_rect()`

### **Armas: Pizzas (Proyectiles)**
- **Sprite:** 32×32 píxeles
- **Velocidad:** `VEL_PIZZA = 11` px/frame
- **Dirección:** Hacia la posición actual del mouse
- **Disparo:** Click izquierdo o ESPACIO; enfriamiento `COOLDOWN_DISPARO = 180` ms
- **Eliminación:** Las pizzas se eliminan automáticamente cuando están a más de 32px fuera de la pantalla
- **Colisión:** Pizza golpea perro → partículas de explosión + popup + sonido + 10 puntos

### **Estado del juego y progresión**
- **Puntuación:** `puntuacion` (aumenta en 10 por cada perro golpeado)
- **Game Over:** `estado_juego` cambia a `ESTADO_GAME_OVER`
- **Seguimiento de tiempo:** `tiempo_inicio` (ms cuando comenzó el juego), `tiempo_transcurrido`
- **Escalado de dificultad:** Ligado al tiempo transcurrido, no a la puntuación

### **Efectos visuales**
- **Partículas:** Lista de `Particula` al golpear un perro mediante `difficulty.crear_explosion()`
  - Colores: amarillo → naranja a medida que disminuye la vida
- **Interfaz:**
  - Vidas (arriba a la izquierda): Íconos de corazón desde `corazon.png`
  - Puntuación (arriba a la derecha): "Puntos: {puntuacion}" en blanco
  - Temporizador (arriba al centro): Formato "m:ss"
  - Barra de dash (debajo de las vidas): Barra de energía cian/naranja
  - Popups de golpe: Texto "+10" flotante

---

## Arquitectura del código y clases principales

### **core/game.py — class Juego (Orquestador)**
```python
def ejecutar(self):             # Bucle principal: eventos → actualizar → dibujar
def _manejar_eventos(t):        # Teclado, mouse, cerrar ventana
def _actualizar(t):             # Lógica del juego (delega en systems/)
def _dibujar(t):                # Renderizado (delega en ui/hud.py)
def _intentar_disparar(t):      # Disparar pizza hacia el mouse
```

### **entities/ — Objetos del juego**
```python
Repartidor.mover(multiplicador)     # Aplicar velocidad + limitar a la pantalla
Perro.perseguir(target_x, target_y) # Perseguir con comportamiento de flanqueo opcional
Pizza.mover()                       # Mover proyectil
Particula.actualizar()              # Mover partícula, disminuir vida
HitPopup.actualizar()               # Flotar hacia arriba, disminuir temporizador
```

### **systems/ — Sistemas del juego**
```python
collision.separar_perros(perros)           # Separar perros entre sí (pura)
collision.jugador_con_perros(jug, perros)  # Colisión jugador-perro (pura)
collision.pizzas_con_perros(pizz, perros)  # Colisión pizza-perro (pura)
difficulty.calcular(tiempo)                # Devuelve (vel_perro, intervalo)
difficulty.generar_apariciones(t, vel)     # Devuelve lista[Perro]
difficulty.crear_explosion(x, y)           # Devuelve lista[Particula]
sound.SoundManager                         # Audio centralizado
```

### **ui/hud.py — Funciones del HUD**
```python
dibujar_hud(pantalla, jugador, puntuacion, tiempo, fuente_ppal, fuente_hit, corazon_img, hits)
dibujar_game_over(pantalla, puntuacion, tiempo_sobrevivido_ms)
```

### **Bucle principal (en game.py)**
1. **Límite de frames** — `reloj.tick(FPS)` a 60 FPS
2. **Manejo de eventos** — Flechas del teclado, clicks del mouse, ESPACIO, cerrar ventana
3. **Actualización** — Dash, movimiento, dificultad, IA de perros, apariciones, movimiento de proyectiles, colisiones (3 tipos), partículas, popups
4. **Renderizado** — Fondo, todas las entidades, HUD, superposición de game over
5. **Volcado de pantalla** — `pygame.display.update()`

---

## Grafo de dependencias

```
main.py
  └── core/game.py
        ├── config.py              ← constantes de solo lectura
        ├── core/states.py         ← enumeraciones de estado
        ├── entities/player.py     ← config
        ├── entities/enemy.py      ← config, utils/helpers
        ├── entities/projectile.py ← config
        ├── entities/effects.py    ← (solo pygame)
        ├── systems/collision.py   ← entities/*, utils/helpers, systems/difficulty
        ├── systems/difficulty.py  ← config, entities/enemy, entities/effects
        ├── systems/sound.py       ← config, utils/loaders
        └── ui/hud.py              ← config
        └── utils/loaders.py       ← config
        └── utils/helpers.py       ← (sin dependencias)
```

Sin dependencias circulares.

---

## Detalles de implementación conocidos

- **POO en todo:** Los objetos del juego son clases con estado interno
- **Sistema de coordenadas:** (0,0) arriba a la izquierda; X→derecha, Y→abajo (estándar de Pygame)
- **Detección de colisiones:** Usa `Rect.colliderect()` con `get_rect()` en todas las entidades
- **Desplazamiento de sprites:** Las pizzas aparecen en `(origen_x + 16, origen_y + 38)` para centrarse en el jugador
- **Sin pausa/menú:** El juego se ejecuta continuamente hasta que se cierra la ventana
- **Sin oleadas/jefes:** Solo escalado lineal de dificultad
- **Funciones de colisión puras:** Reciben listas y devuelven listas modificadas; sin mutación in-place
- **Fuentes creadas una vez** en `Juego.__init__()`, reutilizadas en cada frame
- **SoundManager** está centralizado; `Juego` invoca los sonidos en los eventos, las entidades no conocen el audio

---

## Guía de tareas para asistentes de IA

Al trabajar en este juego, sigue este flujo:

1. **Lee el módulo relevante** — cada módulo tiene una única responsabilidad
   - Añadir nueva entidad → `entities/`
   - Añadir nuevo sistema → `systems/`
   - Cambiar interfaz → `ui/hud.py`
   - Cambiar dificultad → `systems/difficulty.py`
   - Cambiar constantes → `config.py`
   - Cambiar lógica del bucle principal → `core/game.py`
2. **Comprende el orden de dependencias** — `core/` importa todo lo demás; `entities/` solo importa `config`/`utils`
3. **Añadir un nuevo tipo de enemigo** → crear nueva clase en `entities/`, implementar `get_rect()`, `perseguir()`, `dibujar()`, luego integrar en `core/game.py`
4. **Mantener funciones de colisión puras** — nunca mutar listas in-place dentro de `systems/collision.py`
5. **Probar con `python game/main.py`** para verificar que los cambios funcionan
6. **Verificar rutas de assets** — todas las referencias mediante `config.RUTA_IMAGENES` / `RUTA_SONIDOS`

### Tareas comunes

- **Añadir una nueva mecánica** (ej. powerup, jefe, oleadas) → Crear clase de entidad + función de sistema + integrar en `game.py`
- **Ajustar dificultad** → Modificar `systems/difficulty.py` o `config.py`
- **Corregir errores** → Rastrear `Juego._actualizar()`; revisar el flujo de colisiones
- **Ajustes visuales** → Modificar tamaños/posiciones de sprites en `config.py` o `entities/`

---

## Peculiaridades y restricciones conocidas

- Usa **pygame-ce** (fork comunitario), **NO** el `pygame` oficial
- Toda la configuración en `config.py` — sin archivos de configuración externos
- Sin manejo de errores — la falta de assets causa un crash inmediato
- Invencibilidad después de ser golpeado — evita pérdida rápida de vidas al colisionar con múltiples perros
- Apuntado de pizzas basado en el mouse — las pizzas siempre se disparan hacia la posición actual del mouse

# AGENTS.md — Future Pizza (Pygame)

**Context for AI assistants:** This is a Pygame-based action game where the player controls a pizza delivery person defending against attacking dogs using pizza projectiles. **All game logic is in `juego.py`—this is the only file to modify.**

## Quick start

```bash
pip install pygame-ce   # Community Edition, NOT "pygame"
python juego.py
```

Window size: **1100×700 pixels**  
FPS: **60 (locked with Clock)**

---

## Project structure

- **`juego.py`** — Single-file game (only file to edit). ~800 lines, organized in sections with clear dividers.
- **`Recursos/`** — 4 PNG sprite sheets (paths are relative `"./Recursos/..."`):
  - `FONDO.png` — background (scaled 1160×700)
  - `Reparte.png` — spritesheet for repartidor (delivery person); code extracts subsurface (179, 25, 221, 374) then scales to 64×108
  - `Perros.png` — dog sprite (scaled 58×72)
  - `Piz.png` — pizza sprite (scaled 32×32; also used as window icon)
- **`Music/`** — Audio files (all must exist or game crashes):
  - `disparo.mp3` (volume 0.4) — pizza fire sound
  - `golpe.mp3` (volume 0.6) — collision/hit sound
  - `vida_perdida.mp3` (volume 0.8) — life lost sound
  - `MusicaFondo.mp3` (volume 0.5, looped) — background music

---

## Core Game Mechanics

### **Player: Repartidor (Delivery Person)**
- **Sprite:** 64×108 pixels, spawns at (368, 450)
- **Controls:** Arrow keys (4px/frame movement)
  - `velocidad_repartidor = 4`
  - Position: `repartidor_x`, `repartidor_y`
  - Velocity: `repartidor_cambio_x`, `repartidor_cambio_y`
- **Lives:** Starts with `vidas = 3`
- **Invulnerability:** 1 second (`intervalo_invulnerabilidad = 1000`) after being hit
- **Dash/Stamina:** `energia_dash` (0–100, replenishes over time)

### **Enemies: Perros (Dogs)**
- **Sprite:** 58×72 pixels
- **Behavior:** Chase the repartidor at `velocidad_perro` px/frame
- **Dynamic Difficulty:**
  - Velocity increases from 2.5–5 px/frame as game progresses
  - Spawn interval decreases from 2000ms to 800ms (min)
  - Function: `calcular_dificultad(tiempo_transcurrido)` computes speed & spawn rate based on elapsed time
- **Spawn:** Random screen edges every `intervalo_aparicion` ms (controlled by difficulty)
- **Data Structure:** `perros = []` where each dog is `[x, y]`
- **Collision Detection:** Uses distance calculation from repartidor center

### **Weapons: Pizzas (Projectiles)**
- **Sprite:** 32×32 pixels
- **Speed:** `velocidad_pizza = 11` px/frame
- **Direction:** Toward nearest dog via `encontrar_perro_mas_cercano()`
- **Firing:** Manual (left mouse click), cooldown `cooldown_disparo = 180` ms
- **Data Structure:** 4 parallel lists (all same length):
  - `pizzas_x`, `pizzas_y` — current positions
  - `pizzas_dx`, `pizzas_dy` — velocity vectors (pre-normalized × speed)
- **Removal:** Pizzas auto-despawn when > 32px outside screen bounds
- **Collision:** Pizza hits dog → explosion effect + sound + points

### **Game State & Progression**
- **Score:** `puntuacion` (increments when pizza hits dog)
- **Game Over:** `game_over = False` (can be set to True to end)
- **Time Tracking:** `tiempo_inicio` (ms when game started)
- **Difficulty Scaling:** Tied to elapsed time, not score

### **Visual Effects**
- **Particles:** `particulas` list stores explosion effects (position, velocity, lifespan, size)
  - Created on dog collision via `crear_explosion(x, y)`
  - Colors: yellow → orange as lifespan decreases
  - Updated/drawn each frame
- **UI:**
  - Lives (top-left): Red circles, 1 circle per life
  - Score (top-right): "Puntos: {puntuacion}" in white
  - Energy bar (not yet drawn, but `energia_dash` exists for future use)

---

## Code Structure & Key Functions

### **Drawing Functions**
```python
repartidor(x, y)              # Render player sprite
perro(x, y)                   # Render dog sprite
pizza(x, y)                   # Render pizza sprite
dibujar_pizzas()              # Loop through all active pizzas
dibujar_vidas()               # Draw life circles (top-left)
dibujar_puntuacion()          # Draw score text (top-right)
dibujar_particulas()          # Render all particles
```

### **Game Logic Functions**
```python
encontrar_perro_mas_cercano(origen_x, origen_y)  # Returns (x, y, distance) of nearest dog
disparar_pizza(origen_x, origen_y)               # Fire pizza toward mouse from origin
actualizar_pizzas()                              # Move all pizzas, remove off-screen
calcular_dificultad(tiempo_transcurrido)         # Return (velocity, spawn_interval) tuple
crear_explosion(x, y)                            # Spawn particles at position
actualizar_particulas()                          # Move particles, remove dead ones
```

### **Main Loop (Loop Sections in juego.py)**
1. **Event Handling** — Arrow keys, mouse clicks, window close
2. **Update Player** — Apply `repartidor_cambio_x/y` velocities, clamp to screen
3. **Spawn Dogs** — If time since last spawn > `intervalo_aparicion`, add new dog
4. **Update Dogs** — Chase repartidor; check collision with player
5. **Fire Pizzas** — On mouse click + cooldown met
6. **Update Pizzas** — Move and remove off-screen
7. **Collision Detection** — Pizza ∩ dog → eliminate dog, create explosion, add score
8. **Update Particles** — Move and fade explosions
9. **Render Everything** — Background, all sprites, UI, particles
10. **Frame Limit** — `reloj.tick(FPS)` at 60 FPS

---

## Known Implementation Details

- **No Classes:** Uses globals + parallel lists (open to refactoring, but works fine)
- **Coordinate System:** (0,0) is top-left; X increases right, Y increases down (standard Pygame)
- **Collision Detection:** Currently uses squared distance (Euclidean) for dog-pizza
- **Sprite Offsets:**
  - Pizzas spawn at `(origen_x + 16, origen_y + 38)` to center on player
  - Sprite centers are approximated, not pixel-perfect
- **No Pause/Menu:** Game runs continuously until window closes
- **No Waves/Bosses:** Linear difficulty scaling only

---

## AI Assistant Task Guide

When working on this game, follow this flow:

1. **Read `juego.py` thoroughly** to understand the current implementation
2. **Identify the section** (event handling, update loop, collision, rendering, etc.)
3. **Make surgical changes** — avoid refactoring unless explicitly requested
4. **Test with `python juego.py`** to verify changes work
5. **Preserve parallel list consistency** — if you add/remove dogs or pizzas, maintain all 4 pizza lists in sync
6. **Check asset paths** — all `./Recursos/` and `./Music/` files must exist
7. **Document large changes** — add comments in the code for clarity

### Common Tasks

- **Add a new mechanic** (e.g., powerup, boss, waves) → Insert function + integrate into main loop
- **Adjust difficulty** → Modify `calcular_dificultad()` or spawn/speed constants
- **Fix bugs** → Trace through main loop; check collision logic, boundary conditions
- **Optimize** → Profile first (FPS counter?), then refactor if needed
- **Visual tweaks** → Adjust sprite sizes, positions, particle effects; test rendering

---

## Known Quirks & Constraints

- Uses **pygame-ce** (community fork), **not** upstream `pygame`
- **Hard-coded constants** — window size, sprite positions, speeds all set at module level
- **Single commit** on `main` — no version history
- **No external config** — all settings in code
- **No error handling** — missing assets cause immediate crash
- **Invulnerability after hit** — prevents rapid life loss when colliding with multiple dogs
- **Mouse-based pizza aiming** — pizzas always fire toward current mouse position

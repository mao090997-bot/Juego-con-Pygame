# AGENTS.md — Future Pizza (Pygame)

## Quick start

```bash
python juego.py
```

Requires Python 3.14+ and `pygame-ce` (Community Edition, not `pygame`):

```bash
pip install pygame-ce   # NOT "pygame"
```

## Project structure

- `juego.py` — single-file game, the only source to edit.
- `Recursos/` — 4 PNG assets (`FONDO.png`, `Perros.png`, `Piz.png`, `Reparte.png`). All paths in the code are relative `"./Recursos/..."`.

## Gameplay

- **Arrow keys** move the repartidor (delivery person) around the screen.
- **Perros** (dogs) spawn from random screen edges every 3 seconds and chase the repartidor.
- **Pizzas** are auto-fired every 1 second toward the nearest dog. They travel in a straight line and disappear off-screen.
- No scoring, lives, or game-over logic yet.

## Known quirks

- Uses **pygame-ce** (community fork), **not** the upstream `pygame` package.
- Hard-coded window size (800×600) and sprite positions — no config or constants file.
- Single commit on `main`; no tests, no CI, no linting, no type checking.
- `Recursos/` images must exist on disk; the game crashes on missing assets.
- Uses parallel lists (`perros`, `pizzas_x/y/dx/dy`) instead of classes.
- `encontrar_perro_mas_cercano()` already iterates a list — ready for multi-dog from the start.

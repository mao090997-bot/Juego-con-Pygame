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

## Known quirks

- Uses **pygame-ce** (community fork), **not** the upstream `pygame` package.
- Hard-coded window size (800×600) and sprite positions — no config or constants file.
- Single commit on `main`; no tests, no CI, no linting, no type checking.
- `Recursos/` images must exist on disk; the game crashes on missing assets.
- Arrow keys move the "repartidor" (delivery person) character; game loop has no scoring or game-over logic.

# Multi-Mine

Multi-Mine is a local two-player Minesweeper-style game built with Python and Pygame. Two players move around the same board in real time, reveal tiles for points, place flags, and compete for the best score when the field is cleared.

## Features

- Local multiplayer on a shared minefield
- Main menu with `Start Game`, `Settings`, `Rules`, and `Quit`
- Three board sizes:
  - `Small`: 12 columns x 9 rows, 20 mines
  - `Medium`: 16 columns x 12 rows, 30 mines
  - `Large`: 20 columns x 15 rows, 45 mines
- Safe first reveal: the first tile revealed is never a mine
- Flood reveal for empty tiles
- Chord reveal on numbered tiles when nearby flags match the number
- Competitive scoring:
  - Safe reveal: `+1`
  - Mine hit: `-5`
- Game-over screen with replay or return-to-menu options

## Requirements

- Python 3.11 or newer
- `pygame`

Install the dependency:

```bash
pip install pygame
```

## Run

From the project root:

```bash
python main.py
```

## Controls

### Menu

- `Up / Down`: navigate
- `Enter`: select
- `Esc`: quit from the main menu

### Settings and Rules

- `Left / Right`: change map size in `Settings`
- `Esc` or `Backspace`: return to the main menu

### In Game

- Player 1:
  - Move: `W A S D`
  - Reveal tile: `E`
  - Toggle flag: `Q`
- Player 2:
  - Move: arrow keys
  - Reveal tile: `Enter`
  - Toggle flag: `Right Shift`
- Global:
  - Reset the current minefield: `R`
  - Return to menu: `Esc`

### Game Over

- `Up / Down` or `W / S`: change selection
- `Enter`: confirm selection
- `Esc` or `Backspace`: return to the main menu

## Gameplay Notes

- Players move freely and interact with the tile under their character.
- Revealing a safe tile adds points; revealing a mine subtracts points.
- Flagging is used for mine tracking and can also satisfy the win condition.
- The game is won when every mine has either been flagged or revealed.
- Final victory is decided by score, so a player can still win after hitting mines if they reveal more safe tiles overall.

## Testing

This project includes unit tests for mine placement and minefield behavior.

Run the test suite with:

```bash
python -m unittest -q
```

## Project Structure

```text
.
|- README.md
|- config.py
|- main.py
|- assets/
|  |- BlueMan.png
|  `- RedMan.png
|- src/
|  |- __init__.py
|  `- game/
|     |- __init.py
|     |- effects/
|     |  |- __init__.py
|     |  `- status.py
|     |- grid/
|     |  |- __init__.py
|     |  `- tiles.py
|     |- logic/
|     |  |- __init__.py
|     |  `- minesweeper.py
|     |- players/
|     |  |- __init__.py
|     |  `- player.py
|     `- scoring/
|        |- __init__.py
|        `- scoreboard.py
`- tests/
   |- __init__.py
   |- test__grid_tiles.py
   `- test_minesweeper_logic.py
```

## Notes

- `src/game/effects/status.py` and `src/game/scoring/scoreboard.py` are currently empty placeholders.
- The package file at `src/game/__init.py` is named without the usual trailing underscore pair. The project still runs because imports target submodules directly.

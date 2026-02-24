# Multi-mine
Multi-mine is a local 2-player Minesweeper-style game built with Python and Pygame.

## Features
- Local multiplayer with two on-screen players
- Menu system (`Start Game`, `Settings`, `Rules`, `Quit`)
- Three map sizes:
  - `Small`: 12x9 with 20 mines
  - `Medium`: 16x12 with 30 mines
  - `Large`: 20x15 with 45 mines
- Safe first reveal (the first revealed tile cannot be a mine)
- Flagging and chord reveal behavior
- Point-based scoring:
  - Safe reveal: `+1`
  - Mine hit: `-5`
- Win state when all mines are either flagged or revealed

## Requirements
- Python 3.11+ (3.12 works)
- `pygame`

Install dependency:

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
- `Up / Down`: Navigate menu
- `Enter`: Select
- `Esc`: Quit (from menu) or return to menu (from game)

### Settings
- `Left / Right`: Change map size
- `Esc` or `Backspace`: Return to menu

### In Game
- Player 1:
  - Move: `W A S D`
  - Reveal tile under player: `E`
  - Toggle flag under player: `Q`
- Player 2:
  - Move: Arrow keys
  - Reveal tile under player: `Enter`
  - Toggle flag under player: `Right Shift`
- Global:
  - Reset minefield: `R`
  - Return to menu: `Esc`

## Project Structure
```text
.
|- README.md
|- config.py
|- main.py
|- assets/
|  `- .gitkeep
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
- `tests/` and some modules (`effects/status.py`, `scoring/scoreboard.py`) are currently placeholders.
- If `pytest` is not installed in your environment, test commands will fail until it is installed.

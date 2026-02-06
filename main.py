# main.py
import pygame

from config import (
    COLOR_BG,
    COLOR_PANEL,
    COLOR_TEXT,
    FPS,
    GRID_OFFSET_X,
    GRID_OFFSET_Y,
    MINE_PENALTY_POINTS,
    SAFE_REVEAL_POINTS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)
from src.game.grid.tiles import Minefield
from src.game.players.player import Player, PlayerConfig

MAP_SIZES = [
    ("Small", 12, 9, 20),
    ("Medium", 16, 12, 30),
    ("Large", 20, 15, 45),
]


def _map_config(name: str) -> tuple[int, int, int]:
    for label, cols, rows, mines in MAP_SIZES:
        if label == name:
            return rows, cols, mines
    return MAP_SIZES[1][2], MAP_SIZES[1][1], MAP_SIZES[1][3]


def _change_map_size(current: str, direction: int) -> str:
    labels = [label for label, _, _, _ in MAP_SIZES]
    if current not in labels:
        return labels[0]
    idx = labels.index(current)
    idx = (idx + direction) % len(labels)
    return labels[idx]


def _player_grid_pos(player: Player, offset_x: int, offset_y: int, tile_size: int) -> tuple[int, int] | None:
    cx, cy = player.rect.center
    gx = int((cx - offset_x) // tile_size)
    gy = int((cy - offset_y) // tile_size)
    if gx < 0 or gy < 0:
        return None
    return (gy, gx)


def _setup_game(rows: int, cols: int, mine_count: int) -> tuple[Player, Player, Minefield]:
    # Create players
    p1_config = PlayerConfig(name="Player 1")
    p2_config = PlayerConfig(name="Player 2")

    player1 = Player(
        config=p1_config,
        start_pos=(GRID_OFFSET_X + 10, GRID_OFFSET_Y + 10),
        color=(0, 200, 255),
    )

    player2 = Player(
        config=p2_config,
        start_pos=(GRID_OFFSET_X + 200, GRID_OFFSET_Y + 10),
        color=(255, 100, 100),
    )

    minefield = Minefield(
        rows=rows,
        cols=cols,
        tile_size=TILE_SIZE,
        mine_count=mine_count,
        offset=(GRID_OFFSET_X, GRID_OFFSET_Y),
    )

    return player1, player2, minefield


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multi-Mine")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 48)
    menu_font = pygame.font.SysFont(None, 30)
    menu_font_selected = pygame.font.SysFont(None, 36)

    # Screen bounds for clamping players
    screen_rect = screen.get_rect()

    player1: Player | None = None
    player2: Player | None = None
    minefield: Minefield | None = None

    state = "menu"
    menu_items = ["Start Game", "Settings", "Rules", "Quit"]
    menu_index = 0
    map_size_name = "Medium"

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if state == "menu":
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        menu_index = (menu_index - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        menu_index = (menu_index + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        selection = menu_items[menu_index]
                        if selection == "Start Game":
                            rows, cols, mines = _map_config(map_size_name)
                            player1, player2, minefield = _setup_game(rows, cols, mines)
                            state = "game"
                        elif selection == "Settings":
                            state = "settings"
                        elif selection == "Rules":
                            state = "rules"
                        elif selection == "Quit":
                            running = False
                elif state == "settings":
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        state = "menu"
                    elif event.key == pygame.K_LEFT:
                        map_size_name = _change_map_size(map_size_name, -1)
                    elif event.key == pygame.K_RIGHT:
                        map_size_name = _change_map_size(map_size_name, 1)
                elif state == "rules":
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        state = "menu"
                elif state == "game":
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"
                    if event.key == pygame.K_r and minefield is not None:
                        minefield.reset()
                    if event.key == pygame.K_e and player1 is not None and minefield is not None:
                        pos = _player_grid_pos(player1, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                        if pos is not None:
                            result = minefield.reveal_tile(*pos)
                            if result == "safe":
                                player1.add_score(SAFE_REVEAL_POINTS)
                            elif result == "mine":
                                player1.add_score(-MINE_PENALTY_POINTS)
                    if event.key == pygame.K_q and player1 is not None and minefield is not None:
                        pos = _player_grid_pos(player1, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                        if pos is not None:
                            minefield.toggle_flag(*pos)
                    if event.key == pygame.K_RETURN and player2 is not None and minefield is not None:
                        pos = _player_grid_pos(player2, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                        if pos is not None:
                            result = minefield.reveal_tile(*pos)
                            if result == "safe":
                                player2.add_score(SAFE_REVEAL_POINTS)
                            elif result == "mine":
                                player2.add_score(-MINE_PENALTY_POINTS)
                    if event.key == pygame.K_RSHIFT and player2 is not None and minefield is not None:
                        pos = _player_grid_pos(player2, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                        if pos is not None:
                            minefield.toggle_flag(*pos)

        keys = pygame.key.get_pressed()

        screen.fill(COLOR_BG)

        if state == "menu":
            title = title_font.render("Multi-Mine", True, COLOR_TEXT)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

            for idx, label in enumerate(menu_items):
                is_selected = idx == menu_index
                color = (255, 255, 255) if is_selected else COLOR_TEXT
                font_to_use = menu_font_selected if is_selected else menu_font
                text = font_to_use.render(label, True, color)
                x = SCREEN_WIDTH // 2 - text.get_width() // 2
                y = 260 + idx * 40

                if is_selected:
                    highlight_rect = pygame.Rect(x - 80, y - 8, text.get_width() + 160, text.get_height() + 16)
                    pygame.draw.rect(screen, COLOR_PANEL, highlight_rect, border_radius=6)
                    pygame.draw.rect(screen, (90, 110, 140), highlight_rect, 2, border_radius=6)

                screen.blit(text, (x, y))

            hint = font.render("Use Up/Down + Enter. Esc to quit.", True, COLOR_TEXT)
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 420))

        elif state == "settings":
            title = title_font.render("Settings", True, COLOR_TEXT)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

            label = font.render("Map Size", True, COLOR_TEXT)
            screen.blit(label, (240, 260))

            value = menu_font.render(map_size_name, True, (255, 255, 255))
            screen.blit(value, (520, 252))

            hint = font.render("Left/Right to change. Esc/Backspace to return.", True, COLOR_TEXT)
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 620))

        elif state == "rules":
            title = title_font.render("Rules / Features", True, COLOR_TEXT)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

            rules = [
                "Two local players with separate controls (WASD/E/Q and Arrows/Enter/RShift).",
                "Random minefield with safe first reveal (first click is never a mine).",
                "Reveal tiles to score: +1 for safe, -5 for mine hits.",
                "Empty tiles auto-flood reveal connected safe areas.",
                "Flag tiles to mark suspected mines.",
                "Chord reveal: click a revealed number to open neighbors if flags match.",
                "Numbers show adjacent mine counts.",
                "Win when all safe tiles are revealed; loss shows all mines.",
                "Press R during a game to reset the field.",
            ]

            y = 160
            for line in rules:
                text = font.render(f"- {line}", True, COLOR_TEXT)
                screen.blit(text, (80, y))
                y += 26

            hint = font.render("Esc or Backspace to return to menu.", True, COLOR_TEXT)
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 620))

        elif state == "game" and player1 is not None and player2 is not None and minefield is not None:
            # Player 1 movement (WASD)
            dir1 = pygame.Vector2(0, 0)
            if keys[pygame.K_w]:
                dir1.y -= 1
            if keys[pygame.K_s]:
                dir1.y += 1
            if keys[pygame.K_a]:
                dir1.x -= 1
            if keys[pygame.K_d]:
                dir1.x += 1

            # Player 2 movement (Arrow keys)
            dir2 = pygame.Vector2(0, 0)
            if keys[pygame.K_UP]:
                dir2.y -= 1
            if keys[pygame.K_DOWN]:
                dir2.y += 1
            if keys[pygame.K_LEFT]:
                dir2.x -= 1
            if keys[pygame.K_RIGHT]:
                dir2.x += 1

            player1.move(dir1, dt)
            player2.move(dir2, dt)

            player1.clamp_to_rect(screen_rect)
            player2.clamp_to_rect(screen_rect)

            panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH, GRID_OFFSET_Y)
            pygame.draw.rect(screen, COLOR_PANEL, panel_rect)

            score_text = font.render(
                f"P1: {player1.score}   P2: {player2.score}",
                True,
                COLOR_TEXT,
            )
            screen.blit(score_text, (20, 20))

            controls_text = font.render(
                "P1: WASD + E reveal + Q flag | P2: Arrows + Enter reveal + RShift flag | R reset | Esc menu",
                True,
                COLOR_TEXT,
            )
            screen.blit(controls_text, (20, 45))

            if minefield.state == "won":
                status_text = font.render("All safe tiles revealed! Press R to restart.", True, COLOR_TEXT)
                screen.blit(status_text, (20, 60))
            elif minefield.state == "lost":
                status_text = font.render("Mine hit! Press R to restart.", True, COLOR_TEXT)
                screen.blit(status_text, (20, 60))

            minefield.draw(screen, font=font)

            p1_pos = _player_grid_pos(player1, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
            if p1_pos is not None:
                minefield.draw_highlight(screen, *p1_pos)
            p2_pos = _player_grid_pos(player2, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
            if p2_pos is not None:
                minefield.draw_highlight(screen, *p2_pos)

            player1.draw(screen)
            player2.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

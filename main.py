# main.py
import pygame

from config import (
    COLOR_BG,
    COLOR_PANEL,
    COLOR_TEXT,
    FPS,
    GRID_COLS,
    GRID_OFFSET_X,
    GRID_OFFSET_Y,
    GRID_ROWS,
    MINE_COUNT,
    MINE_PENALTY_POINTS,
    SAFE_REVEAL_POINTS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)
from src.game.grid.tiles import Minefield
from src.game.players.player import Player, PlayerConfig


def _player_grid_pos(player: Player, offset_x: int, offset_y: int, tile_size: int) -> tuple[int, int] | None:
    cx, cy = player.rect.center
    gx = int((cx - offset_x) // tile_size)
    gy = int((cy - offset_y) // tile_size)
    if gx < 0 or gy < 0:
        return None
    return (gy, gx)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multi-Mine")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)

    # Screen bounds for clamping players
    screen_rect = screen.get_rect()

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
        rows=GRID_ROWS,
        cols=GRID_COLS,
        tile_size=TILE_SIZE,
        mine_count=MINE_COUNT,
        offset=(GRID_OFFSET_X, GRID_OFFSET_Y),
    )

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    minefield.reset()
                if event.key == pygame.K_e:
                    pos = _player_grid_pos(player1, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                    if pos is not None:
                        result = minefield.reveal_tile(*pos)
                        if result == "safe":
                            player1.add_score(SAFE_REVEAL_POINTS)
                        elif result == "mine":
                            player1.add_score(-MINE_PENALTY_POINTS)
                if event.key == pygame.K_q:
                    pos = _player_grid_pos(player1, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                    if pos is not None:
                        minefield.toggle_flag(*pos)
                if event.key == pygame.K_RETURN:
                    pos = _player_grid_pos(player2, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                    if pos is not None:
                        result = minefield.reveal_tile(*pos)
                        if result == "safe":
                            player2.add_score(SAFE_REVEAL_POINTS)
                        elif result == "mine":
                            player2.add_score(-MINE_PENALTY_POINTS)
                if event.key == pygame.K_RSHIFT:
                    pos = _player_grid_pos(player2, GRID_OFFSET_X, GRID_OFFSET_Y, TILE_SIZE)
                    if pos is not None:
                        minefield.toggle_flag(*pos)

        keys = pygame.key.get_pressed()

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

        screen.fill(COLOR_BG)

        panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH, GRID_OFFSET_Y)
        pygame.draw.rect(screen, COLOR_PANEL, panel_rect)

        score_text = font.render(
            f"P1: {player1.score}   P2: {player2.score}",
            True,
            COLOR_TEXT,
        )
        screen.blit(score_text, (20, 20))

        controls_text = font.render(
            "P1: WASD + E reveal + Q flag | P2: Arrows + Enter reveal + RShift flag | R reset",
            True,
            COLOR_TEXT,
        )
        screen.blit(controls_text, (20, 45))

        minefield.draw(screen)

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
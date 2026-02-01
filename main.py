# main.py
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game.players.player import Player, PlayerConfig


MENU_ITEMS = ["Start Game", "Settings", "Quit"]


class ScreenState:
    MENU = "menu"
    GAME = "game"
    SETTINGS = "settings"


def _draw_centered_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    y: int,
) -> None:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(rendered, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multi-Mine")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 28)
    title_font = pygame.font.SysFont("consolas", 48, bold=True)

    # Screen bounds for clamping players
    screen_rect = screen.get_rect()

    # Create players
    p1_config = PlayerConfig(name="Player 1")
    p2_config = PlayerConfig(name="Player 2")

    player1 = Player(
        config=p1_config,
        start_pos=(100, 100),
        color=(0, 200, 255),  # blue
    )

    player2 = Player(
        config=p2_config,
        start_pos=(600, 400),
        color=(255, 100, 100),  # red
    )

    state = ScreenState.MENU
    menu_index = 0

    running = True
    while running:
        # Delta time (seconds)
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state == ScreenState.MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_index = (menu_index - 1) % len(MENU_ITEMS)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_index = (menu_index + 1) % len(MENU_ITEMS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        selected = MENU_ITEMS[menu_index]
                        if selected == "Start Game":
                            state = ScreenState.GAME
                        elif selected == "Settings":
                            state = ScreenState.SETTINGS
                        elif selected == "Quit":
                            running = False
                elif event.key == pygame.K_ESCAPE:
                    state = ScreenState.MENU

        # ----------------------------
        # Update
        # ----------------------------
        if state == ScreenState.GAME:
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

        # ----------------------------
        # Rendering
        # ----------------------------
        screen.fill((30, 30, 30))

        if state == ScreenState.MENU:
            _draw_centered_text(screen, "Multi-Mine", title_font, (240, 240, 240), 140)
            start_y = 260
            for i, item in enumerate(MENU_ITEMS):
                color = (255, 220, 100) if i == menu_index else (200, 200, 200)
                _draw_centered_text(screen, item, font, color, start_y + i * 50)
            _draw_centered_text(
                screen,
                "Use arrows/W-S and Enter. Esc returns to menu.",
                pygame.font.SysFont("consolas", 20),
                (140, 140, 140),
                SCREEN_HEIGHT - 40,
            )
        elif state == ScreenState.SETTINGS:
            _draw_centered_text(screen, "Settings", title_font, (240, 240, 240), 160)
            _draw_centered_text(
                screen,
                "Settings screen placeholder.",
                font,
                (200, 200, 200),
                260,
            )
            _draw_centered_text(
                screen,
                "Press Esc to return to menu.",
                pygame.font.SysFont("consolas", 20),
                (140, 140, 140),
                SCREEN_HEIGHT - 40,
            )
        else:
            player1.draw(screen)
            player2.draw(screen)
            _draw_centered_text(
                screen,
                "Press Esc to return to menu.",
                pygame.font.SysFont("consolas", 20),
                (140, 140, 140),
                SCREEN_HEIGHT - 40,
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

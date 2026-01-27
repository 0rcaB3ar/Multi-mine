# main.py
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.game.players.player import Player, PlayerConfig


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Multi-Mine")
    clock = pygame.time.Clock()

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

    running = True
    while running:
        # Delta time (seconds)
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ----------------------------
        # Input handling
        # ----------------------------
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

        # ----------------------------
        # Update players
        # ----------------------------
        player1.move(dir1, dt)
        player2.move(dir2, dt)

        player1.clamp_to_rect(screen_rect)
        player2.clamp_to_rect(screen_rect)

        # ----------------------------
        # Rendering
        # ----------------------------
        screen.fill((30, 30, 30))

        player1.draw(screen)
        player2.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

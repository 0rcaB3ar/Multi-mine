# src/game/players/player.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

import pygame


@dataclass
class PlayerConfig:
    """Configuration for a player."""
    name: str
    size: Tuple[int, int] = (28, 28)   # width, height in pixels
    speed: float = 200.0              # pixels per second


class Player:
    """
    Top-down player entity.

    Responsibilities:
    - Store player state (position, score)
    - Apply movement input (pixels, not tiles)
    - Clamp to bounds
    - Provide helpers like "which tile am I standing on?"
    """

    def __init__(
        self,
        config: PlayerConfig,
        start_pos: Tuple[float, float],
        color: Tuple[int, int, int],
    ) -> None:
        self.config = config
        self.x: float = float(start_pos[0])
        self.y: float = float(start_pos[1])
        self.color = color

        self.score: int = 0
        self._last_tile: Tuple[int, int] | None = None  # initialize this

    def move(self, direction: pygame.Vector2, dt: float) -> None:
        """Move using a direction vector; normalized automatically."""
        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.x += direction.x * self.config.speed * dt
        self.y += direction.y * self.config.speed * dt

    def clamp_to_rect(self, bounds: pygame.Rect) -> None:
        """Keep the player inside the given rectangle bounds."""
        r = self.rect
        if r.left < bounds.left:
            self.x = bounds.left
        if r.top < bounds.top:
            self.y = bounds.top
        if r.right > bounds.right:
            self.x = bounds.right - r.width
        if r.bottom > bounds.bottom:
            self.y = bounds.bottom - r.height

    def add_score(self, points: int) -> None:
        self.score += points

    @property
    def rect(self) -> pygame.Rect:
        w, h = self.config.size
        return pygame.Rect(int(self.x), int(self.y), w, h)

    def tile_pos(self, tile_size: int) -> Tuple[int, int]:
        cx, cy = self.rect.center
        return (cx // tile_size, cy // tile_size)

    def set_last_tile(self, tile_xy: Tuple[int, int]) -> None:
        self._last_tile = tile_xy

    def get_last_tile(self) -> Tuple[int, int] | None:
        return self._last_tile

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

# src/game/grid/tiles.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Tuple

import pygame

from config import (
    COLOR_GRID_BG,
    COLOR_TILE_FLAG,
    COLOR_TILE_HIDDEN,
    COLOR_TILE_HIGHLIGHT,
    COLOR_TILE_MINE,
    COLOR_TILE_REVEALED,
)
from src.game.logic.minesweeper import count_adjacent_mines, generate_mine_positions


@dataclass
class Tile:
    row: int
    col: int
    is_mine: bool = False
    adjacent_mines: int = 0
    revealed: bool = False
    flagged: bool = False


class Minefield:
    def __init__(
        self,
        rows: int,
        cols: int,
        tile_size: int,
        mine_count: int,
        offset: Tuple[int, int],
    ) -> None:
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.mine_count = mine_count
        self.offset_x, self.offset_y = offset

        self.tiles: List[List[Tile]] = [
            [Tile(r, c) for c in range(cols)] for r in range(rows)
        ]

        self.state: str = "playing"
        self.revealed_safe_count: int = 0
        self.first_reveal_done: bool = False

        self._place_mines_and_counts()

    def _clear_mines_and_counts(self) -> None:
        for row in self.tiles:
            for tile in row:
                tile.is_mine = False
                tile.adjacent_mines = 0

    def _place_mines_and_counts(self, exclude: Iterable[Tuple[int, int]] | None = None) -> None:
        self._clear_mines_and_counts()
        mine_positions = generate_mine_positions(
            self.rows,
            self.cols,
            self.mine_count,
            exclude=exclude,
        )
        for r, c in mine_positions:
            self.tiles[r][c].is_mine = True

        for r in range(self.rows):
            for c in range(self.cols):
                if not self.tiles[r][c].is_mine:
                    self.tiles[r][c].adjacent_mines = count_adjacent_mines(
                        r,
                        c,
                        mine_positions,
                        self.rows,
                        self.cols,
                    )

    def reset(self) -> None:
        for row in self.tiles:
            for tile in row:
                tile.revealed = False
                tile.flagged = False
        self.state = "playing"
        self.revealed_safe_count = 0
        self.first_reveal_done = False
        self._place_mines_and_counts()

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def tile_at_grid(self, row: int, col: int) -> Tile | None:
        if not self.in_bounds(row, col):
            return None
        return self.tiles[row][col]

    def grid_from_pixel(self, x: float, y: float) -> Tuple[int, int] | None:
        gx = int((x - self.offset_x) // self.tile_size)
        gy = int((y - self.offset_y) // self.tile_size)
        if not self.in_bounds(gy, gx):
            return None
        return (gy, gx)

    def reveal_tile(self, row: int, col: int) -> str:
        if self.state != "playing":
            return "blocked"
        tile = self.tile_at_grid(row, col)
        if tile is None:
            return "out"
        if tile.flagged:
            return "blocked"

        if not self.first_reveal_done:
            self._place_mines_and_counts(exclude={(row, col)})
            self.first_reveal_done = True
            tile = self.tiles[row][col]

        if tile.revealed:
            return self._chord_reveal(row, col)

        hit_mine, newly_revealed = self._reveal_from_click(row, col)
        if hit_mine:
            self.state = "lost"
            self._reveal_all_mines()
            return "mine"

        self.revealed_safe_count += newly_revealed
        self._check_win()
        return "safe"

    def _reveal_from_click(self, row: int, col: int) -> Tuple[bool, int]:
        tile = self.tiles[row][col]
        if tile.revealed or tile.flagged:
            return (False, 0)

        tile.revealed = True
        if tile.is_mine:
            return (True, 0)

        newly_revealed = 1
        if tile.adjacent_mines == 0:
            newly_revealed += self._flood_reveal(row, col)

        return (False, newly_revealed)

    def _flood_reveal(self, row: int, col: int) -> int:
        stack = [(row, col)]
        visited = set(stack)
        revealed_count = 0

        while stack:
            cr, cc = stack.pop()
            for nr in (cr - 1, cr, cr + 1):
                for nc in (cc - 1, cc, cc + 1):
                    if not self.in_bounds(nr, nc):
                        continue
                    if (nr, nc) in visited:
                        continue
                    neighbor = self.tiles[nr][nc]
                    if neighbor.flagged or neighbor.is_mine:
                        continue
                    if neighbor.revealed:
                        continue
                    neighbor.revealed = True
                    revealed_count += 1
                    visited.add((nr, nc))
                    if neighbor.adjacent_mines == 0:
                        stack.append((nr, nc))

        return revealed_count

    def _chord_reveal(self, row: int, col: int) -> str:
        tile = self.tiles[row][col]
        if tile.adjacent_mines <= 0:
            return "blocked"

        flag_count = 0
        for nr in (row - 1, row, row + 1):
            for nc in (col - 1, col, col + 1):
                if not self.in_bounds(nr, nc):
                    continue
                if self.tiles[nr][nc].flagged:
                    flag_count += 1

        if flag_count != tile.adjacent_mines:
            return "blocked"

        hit_mine = False
        newly_revealed = 0
        for nr in (row - 1, row, row + 1):
            for nc in (col - 1, col, col + 1):
                if not self.in_bounds(nr, nc):
                    continue
                if nr == row and nc == col:
                    continue
                revealed_mine, count = self._reveal_from_click(nr, nc)
                newly_revealed += count
                if revealed_mine:
                    hit_mine = True

        if hit_mine:
            self.state = "lost"
            self._reveal_all_mines()
            return "mine"

        if newly_revealed:
            self.revealed_safe_count += newly_revealed
            self._check_win()

        return "safe"

    def _reveal_all_mines(self) -> None:
        for row in self.tiles:
            for tile in row:
                if tile.is_mine:
                    tile.revealed = True

    def _check_win(self) -> None:
        if self.revealed_safe_count >= (self.rows * self.cols - self.mine_count):
            self.state = "won"

    def toggle_flag(self, row: int, col: int) -> bool:
        tile = self.tile_at_grid(row, col)
        if tile is None or tile.revealed:
            return False
        tile.flagged = not tile.flagged
        return True

    def draw(self, surface: pygame.Surface, font: pygame.font.Font | None = None) -> None:
        grid_rect = pygame.Rect(
            self.offset_x,
            self.offset_y,
            self.cols * self.tile_size,
            self.rows * self.tile_size,
        )
        pygame.draw.rect(surface, COLOR_GRID_BG, grid_rect)

        for row in self.tiles:
            for tile in row:
                x = self.offset_x + tile.col * self.tile_size
                y = self.offset_y + tile.row * self.tile_size
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                if tile.revealed:
                    if tile.is_mine:
                        color = COLOR_TILE_MINE
                    else:
                        color = COLOR_TILE_REVEALED
                else:
                    color = COLOR_TILE_HIDDEN

                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (0, 0, 0), rect, 1)

                if tile.revealed and not tile.is_mine and tile.adjacent_mines > 0 and font:
                    label = font.render(str(tile.adjacent_mines), True, (20, 20, 20))
                    label_rect = label.get_rect(center=rect.center)
                    surface.blit(label, label_rect)

                if tile.flagged and not tile.revealed:
                    flag_rect = rect.inflate(-self.tile_size * 0.4, -self.tile_size * 0.4)
                    pygame.draw.rect(surface, COLOR_TILE_FLAG, flag_rect)

    def draw_highlight(self, surface: pygame.Surface, row: int, col: int) -> None:
        if not self.in_bounds(row, col):
            return
        x = self.offset_x + col * self.tile_size
        y = self.offset_y + row * self.tile_size
        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        pygame.draw.rect(surface, COLOR_TILE_HIGHLIGHT, rect, 2)

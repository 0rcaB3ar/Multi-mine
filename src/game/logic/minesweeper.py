# src/game/logic/minesweeper.py
from __future__ import annotations

import random
from typing import Iterable, Set, Tuple


def generate_mine_positions(
    rows: int,
    cols: int,
    mine_count: int,
    rng: random.Random | None = None,
) -> Set[Tuple[int, int]]:
    if mine_count <= 0:
        return set()
    if mine_count >= rows * cols:
        raise ValueError("mine_count must be less than rows * cols")

    rng = rng or random.Random()
    positions: Set[Tuple[int, int]] = set()

    while len(positions) < mine_count:
        positions.add((rng.randrange(rows), rng.randrange(cols)))

    return positions


def count_adjacent_mines(
    row: int,
    col: int,
    mine_positions: Iterable[Tuple[int, int]],
    rows: int,
    cols: int,
) -> int:
    mines = set(mine_positions)
    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in mines:
                count += 1

    return count
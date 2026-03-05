import unittest

from src.game.grid.tiles import Minefield


class TestMinefieldFlagsAndWin(unittest.TestCase):
    def _fresh_field(self) -> Minefield:
        field = Minefield(rows=2, cols=2, tile_size=16, mine_count=1, offset=(0, 0))
        for row in field.tiles:
            for tile in row:
                tile.is_mine = False
                tile.revealed = False
                tile.flagged = False
                tile.adjacent_mines = 0
        field.tiles[0][0].is_mine = True
        field.state = "playing"
        return field

    def test_flagging_last_mine_sets_won(self) -> None:
        field = self._fresh_field()

        changed = field.toggle_flag(0, 0)

        self.assertTrue(changed)
        self.assertEqual(field.state, "won")

    def test_toggle_flag_blocked_when_not_playing(self) -> None:
        field = self._fresh_field()
        field.state = "won"

        changed = field.toggle_flag(0, 0)

        self.assertFalse(changed)
        self.assertFalse(field.tiles[0][0].flagged)

    def test_flag_count_and_remaining_mines_estimate(self) -> None:
        field = self._fresh_field()

        field.toggle_flag(0, 0)

        self.assertEqual(field.flagged_count, 1)
        self.assertEqual(field.remaining_mines_estimate, 0)


if __name__ == "__main__":
    unittest.main()

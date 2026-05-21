import random
import unittest

from minesweeper.models import Board


class BoardTests(unittest.TestCase):
    def test_first_click_is_safe(self):
        board = Board(rows=9, cols=9, mines=10, rng=random.Random(1))

        result = board.reveal(4, 4)

        self.assertNotEqual(result, "lost")
        self.assertFalse(board.grid[4][4].is_mine)

    def test_flagged_cell_cannot_be_revealed(self):
        board = Board(rows=9, cols=9, mines=10, rng=random.Random(2))

        board.toggle_flag(0, 0)
        result = board.reveal(0, 0)

        self.assertEqual(result, "ignored")
        self.assertFalse(board.grid[0][0].is_revealed)

    def test_revealing_all_safe_cells_wins(self):
        board = Board(rows=4, cols=4, mines=1, rng=random.Random(3))

        board.reveal(0, 0)
        for row in range(board.rows):
            for col in range(board.cols):
                if not board.grid[row][col].is_mine:
                    board.reveal(row, col)

        self.assertEqual(board.state, "won")


if __name__ == "__main__":
    unittest.main()

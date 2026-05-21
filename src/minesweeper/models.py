from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random
from typing import Iterable


@dataclass
class Cell:
    row: int
    col: int
    is_mine: bool = False
    is_revealed: bool = False
    is_flagged: bool = False
    adjacent_mines: int = 0


class Board:
    """Pure game logic for Minesweeper."""

    def __init__(
        self,
        rows: int,
        cols: int,
        mines: int,
        rng: random.Random | None = None,
    ) -> None:
        if rows < 4 or cols < 4:
            raise ValueError("Board must be at least 4x4.")
        if mines < 1 or mines >= rows * cols:
            raise ValueError("Mine count must be between 1 and cells - 1.")

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self._rng = rng or random.Random()
        self._mine_positions: set[tuple[int, int]] = set()
        self._mines_placed = False
        self.state = "playing"
        self.grid: list[list[Cell]] = []
        self.reset()

    def reset(self) -> None:
        self.state = "playing"
        self._mine_positions = set()
        self._mines_placed = False
        self.grid = [
            [Cell(row=row, col=col) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    @property
    def flagged_count(self) -> int:
        return sum(cell.is_flagged for row in self.grid for cell in row)

    @property
    def remaining_flags(self) -> int:
        return self.mines - self.flagged_count

    @property
    def revealed_count(self) -> int:
        return sum(cell.is_revealed for row in self.grid for cell in row)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbors(self, row: int, col: int) -> Iterable[Cell]:
        for row_offset in (-1, 0, 1):
            for col_offset in (-1, 0, 1):
                if row_offset == 0 and col_offset == 0:
                    continue
                next_row = row + row_offset
                next_col = col + col_offset
                if self.in_bounds(next_row, next_col):
                    yield self.grid[next_row][next_col]

    def toggle_flag(self, row: int, col: int) -> bool:
        if self.state != "playing" or not self.in_bounds(row, col):
            return False

        cell = self.grid[row][col]
        if cell.is_revealed:
            return False

        cell.is_flagged = not cell.is_flagged
        return True

    def reveal(self, row: int, col: int) -> str:
        if self.state != "playing" or not self.in_bounds(row, col):
            return "ignored"

        if not self._mines_placed:
            self._place_mines(first_click=(row, col))

        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return "ignored"

        if cell.is_mine:
            cell.is_revealed = True
            self.state = "lost"
            self.reveal_all_mines()
            return "lost"

        self._reveal_area(row, col)
        if self._all_safe_cells_revealed():
            self.state = "won"
            self._flag_all_mines()
            return "won"

        return "revealed"

    def reveal_all_mines(self) -> None:
        for mine_row, mine_col in self._mine_positions:
            self.grid[mine_row][mine_col].is_revealed = True

    def _place_mines(self, first_click: tuple[int, int]) -> None:
        protected = {first_click}
        protected.update((cell.row, cell.col) for cell in self.neighbors(*first_click))

        candidates = [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if (row, col) not in protected
        ]
        if len(candidates) < self.mines:
            candidates = [
                (row, col)
                for row in range(self.rows)
                for col in range(self.cols)
                if (row, col) != first_click
            ]

        self._mine_positions = set(self._rng.sample(candidates, self.mines))
        for mine_row, mine_col in self._mine_positions:
            self.grid[mine_row][mine_col].is_mine = True

        for row in self.grid:
            for cell in row:
                cell.adjacent_mines = sum(neighbor.is_mine for neighbor in self.neighbors(cell.row, cell.col))

        self._mines_placed = True

    def _reveal_area(self, start_row: int, start_col: int) -> None:
        queue: deque[tuple[int, int]] = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            cell = self.grid[row][col]
            if cell.is_revealed or cell.is_flagged:
                continue

            cell.is_revealed = True
            if cell.adjacent_mines != 0:
                continue

            for neighbor in self.neighbors(row, col):
                if not neighbor.is_revealed and not neighbor.is_flagged and not neighbor.is_mine:
                    queue.append((neighbor.row, neighbor.col))

    def _all_safe_cells_revealed(self) -> bool:
        safe_cells = self.rows * self.cols - self.mines
        return self.revealed_count == safe_cells

    def _flag_all_mines(self) -> None:
        for mine_row, mine_col in self._mine_positions:
            self.grid[mine_row][mine_col].is_flagged = True

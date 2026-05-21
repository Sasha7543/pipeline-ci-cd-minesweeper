from __future__ import annotations

from dataclasses import dataclass

from .models import Board, Cell


NUMBER_COLORS = {
    1: (25, 93, 190),
    2: (30, 130, 76),
    3: (196, 55, 45),
    4: (100, 65, 165),
    5: (145, 74, 28),
    6: (34, 140, 145),
    7: (30, 30, 30),
    8: (105, 105, 105),
}


@dataclass(frozen=True)
class GameSettings:
    rows: int
    cols: int
    mines: int
    cell_size: int
    background: tuple[int, int, int]


class MinesweeperApp:
    def __init__(self, settings: GameSettings) -> None:
        import pygame

        pygame.init()
        self.pygame = pygame
        self.settings = settings
        self.header_height = 56
        self.width = settings.cols * settings.cell_size
        self.height = settings.rows * settings.cell_size + self.header_height
        self.board = Board(settings.rows, settings.cols, settings.mines)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper - CI/CD Lab")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", max(16, settings.cell_size // 2), bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 22, bold=True)

    def run(self) -> None:
        running = True
        while running:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                elif event.type == self.pygame.KEYDOWN:
                    running = self._handle_key(event.key)
                elif event.type == self.pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse(event.button, event.pos)

            self._draw()
            self.clock.tick(60)

        self.pygame.quit()

    def _handle_key(self, key: int) -> bool:
        if key == self.pygame.K_ESCAPE:
            return False
        if key == self.pygame.K_r:
            self.board.reset()
        return True

    def _handle_mouse(self, button: int, pos: tuple[int, int]) -> None:
        x, y = pos
        if y < self.header_height:
            if button == 1:
                self.board.reset()
            return

        row = (y - self.header_height) // self.settings.cell_size
        col = x // self.settings.cell_size
        if button == 1:
            self.board.reveal(row, col)
        elif button == 3:
            self.board.toggle_flag(row, col)

    def _draw(self) -> None:
        self.screen.fill(self.settings.background)
        self._draw_header()
        self._draw_board()
        self.pygame.display.flip()

    def _draw_header(self) -> None:
        pygame = self.pygame
        pygame.draw.rect(self.screen, (37, 47, 59), (0, 0, self.width, self.header_height))

        status = {
            "playing": "Playing",
            "won": "You won!",
            "lost": "Game over",
        }[self.board.state]
        info = f"Mines: {self.board.remaining_flags}   Status: {status}"
        info_surface = self.title_font.render(info, True, (244, 247, 250))
        self.screen.blit(info_surface, (14, 8))

        hint = "Left click: open | Right click: flag | R/header: restart | Esc: quit"
        hint_surface = self.small_font.render(hint, True, (190, 201, 214))
        self.screen.blit(hint_surface, (14, 32))

    def _draw_board(self) -> None:
        for row in self.board.grid:
            for cell in row:
                self._draw_cell(cell)

    def _draw_cell(self, cell: Cell) -> None:
        pygame = self.pygame
        size = self.settings.cell_size
        x = cell.col * size
        y = self.header_height + cell.row * size
        rect = pygame.Rect(x, y, size, size)

        if cell.is_revealed:
            fill = (214, 219, 225) if not cell.is_mine else (210, 70, 60)
            pygame.draw.rect(self.screen, fill, rect)
            pygame.draw.rect(self.screen, (158, 169, 181), rect, 1)
            self._draw_revealed_content(cell, rect)
            return

        pygame.draw.rect(self.screen, (73, 133, 94), rect)
        pygame.draw.rect(self.screen, (96, 159, 115), rect.inflate(-4, -4))
        pygame.draw.rect(self.screen, (45, 89, 63), rect, 1)

        if cell.is_flagged:
            self._draw_flag(rect)

    def _draw_revealed_content(self, cell: Cell, rect) -> None:
        if cell.is_mine:
            self.pygame.draw.circle(self.screen, (38, 38, 42), rect.center, max(5, rect.width // 4))
            return

        if cell.adjacent_mines:
            color = NUMBER_COLORS.get(cell.adjacent_mines, (40, 40, 40))
            label = self.font.render(str(cell.adjacent_mines), True, color)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

    def _draw_flag(self, rect) -> None:
        pygame = self.pygame
        pole_x = rect.left + rect.width // 3
        top_y = rect.top + rect.height // 4
        bottom_y = rect.bottom - rect.height // 4
        pygame.draw.line(self.screen, (245, 245, 245), (pole_x, top_y), (pole_x, bottom_y), 3)
        points = [
            (pole_x, top_y),
            (rect.right - rect.width // 4, top_y + rect.height // 8),
            (pole_x, rect.top + rect.height // 2),
        ]
        pygame.draw.polygon(self.screen, (220, 55, 55), points)

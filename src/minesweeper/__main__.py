from __future__ import annotations

import argparse

from .game import GameSettings, MinesweeperApp


DIFFICULTIES = {
    "easy": (9, 9, 10),
    "normal": (12, 16, 30),
    "hard": (16, 24, 72),
}


def parse_color(value: str) -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise argparse.ArgumentTypeError("Color must use HEX format, for example #1f2937.")

    try:
        red = int(raw[0:2], 16)
        green = int(raw[2:4], 16)
        blue = int(raw[4:6], 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Color contains invalid HEX symbols.") from exc

    return red, green, blue


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Minesweeper with pygame.")
    parser.add_argument(
        "--difficulty",
        choices=DIFFICULTIES,
        default="normal",
        help="Game difficulty preset.",
    )
    parser.add_argument("--rows", type=int, help="Custom number of rows.")
    parser.add_argument("--cols", type=int, help="Custom number of columns.")
    parser.add_argument("--mines", type=int, help="Custom number of mines.")
    parser.add_argument("--cell-size", type=int, default=32, help="Cell size in pixels.")
    parser.add_argument(
        "--background",
        type=parse_color,
        default=parse_color("#f4f7fb"),
        help="Window background color in HEX format.",
    )
    return parser


def settings_from_args(args: argparse.Namespace) -> GameSettings:
    rows, cols, mines = DIFFICULTIES[args.difficulty]
    rows = args.rows or rows
    cols = args.cols or cols
    mines = args.mines or mines

    return GameSettings(
        rows=rows,
        cols=cols,
        mines=mines,
        cell_size=max(22, args.cell_size),
        background=args.background,
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    settings = settings_from_args(args)
    app = MinesweeperApp(settings)
    app.run()


if __name__ == "__main__":
    main()

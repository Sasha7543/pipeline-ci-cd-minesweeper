# UML-діаграми

Діаграми записані у форматі Mermaid. Їх можна переглянути безпосередньо на GitHub або вставити у звіт.

## Діаграма варіантів використання

```mermaid
flowchart LR
    player["Гравець"]
    start(("Запустити гру"))
    choose(("Обрати складність"))
    open(("Відкрити клітинку"))
    flag(("Поставити/прибрати прапорець"))
    restart(("Перезапустити гру"))
    win(("Побачити перемогу"))
    lose(("Побачити поразку"))

    player --> start
    player --> choose
    player --> open
    player --> flag
    player --> restart
    open --> win
    open --> lose
```

## Діаграма діяльності

```mermaid
flowchart TD
    a([Старт])
    b[Прочитати аргументи командного рядка]
    c[Створити вікно Pygame]
    d[Створити ігрове поле]
    e{Подія користувача}
    f[Відкрити клітинку]
    g[Поставити або прибрати прапорець]
    h[Перезапустити гру]
    i{Клітинка містить міну?}
    j[Показати всі міни]
    k{Відкриті всі безпечні клітинки?}
    l[Показати перемогу]
    m[Оновити екран]
    n([Кінець])

    a --> b --> c --> d --> e
    e -->|Лівий клік| f --> i
    e -->|Правий клік| g --> m
    e -->|R або клік по панелі| h --> d
    e -->|Закрити вікно| n
    i -->|Так| j --> m
    i -->|Ні| k
    k -->|Так| l --> m
    k -->|Ні| m
    m --> e
```

## Діаграма класів

```mermaid
classDiagram
    class Cell {
        +int row
        +int col
        +bool is_mine
        +bool is_revealed
        +bool is_flagged
        +int adjacent_mines
    }

    class Board {
        +int rows
        +int cols
        +int mines
        +str state
        +reset()
        +toggle_flag(row, col)
        +reveal(row, col)
        +neighbors(row, col)
        +reveal_all_mines()
    }

    class GameSettings {
        +int rows
        +int cols
        +int mines
        +int cell_size
        +tuple background
    }

    class MinesweeperApp {
        +run()
        -_handle_key(key)
        -_handle_mouse(button, pos)
        -_draw()
        -_draw_cell(cell)
    }

    Board "1" *-- "*" Cell
    MinesweeperApp "1" --> "1" Board
    MinesweeperApp "1" --> "1" GameSettings
```

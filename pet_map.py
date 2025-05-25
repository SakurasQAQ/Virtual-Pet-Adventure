# pet_map.py — Virtual Pet Map Module
from emoji_map import emoji_dict

from emoji_map import emoji_dict

def create_map(rows: int, cols: int) -> list[list[str]]:
    placeholder = emoji_dict["Floor"]  # assume you added a "Floor" key in emoji_map
    # initialize every cell with the floor emoji
    return [[placeholder for _ in range(cols)] for _ in range(rows)]


def display_map(grid_net: list[list[str]]) -> None:
    placeholder = emoji_dict["Floor"]
    for row in grid_net:
        for cell in row:
            if cell == ' ':
                cell = placeholder
            print(f'| {cell:^2}', end='')
        print('|')


def place_pet(grid: list[list[str]], position: tuple[int, int], symbol: str = 'P') -> None:
    r, c = position
    grid[r][c] = symbol


def place_item(grid_net: list[list[str]], symbol: str, position: tuple[int, int]) -> None:

    r, c = position
    grid_net[r][c] = symbol


def move_pet(grid: list[list[str]], old_pos: tuple[int, int], direction: str, symbol: str) -> tuple[int, int]:

    # Move pet one step using WASD: 'w', 'a', 's', 'd'.
    rows, cols = len(grid), len(grid[0])
    r, c = old_pos
    grid[r][c] = ' '  # clear old position

    if direction == 'w' and r > 0:
        r -= 1
    elif direction == 's' and r < rows - 1:
        r += 1
    elif direction == 'a' and c > 0:
        c -= 1
    elif direction == 'd' and c < cols - 1:
        c += 1
    else:
        grid[old_pos[0]][old_pos[1]] = symbol
        return old_pos

    grid[r][c] = symbol
    return r, c

def place_exit(grid):
    grid[0][0] = emoji_dict["Exit"]
    print("An exit has appeared at (0, 0)!")

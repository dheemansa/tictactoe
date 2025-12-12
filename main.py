"""
index: 0 1 2  -> top row
       3 4 5  -> middle row
       6 7 8  -> bottom row

values: 1 = player1, 2 = player2, 0 = empty
"""

import os

RED = "\033[1;31m"
BLUE = "\033[1;34m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

CROSS = RED + "✕" + RESET
TICK = BLUE + "◯" + RESET

VALID_POSITIONS = range(1, 10)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def show_grid(grid_list: list):
    final = []
    for i in grid_list:
        if i == 1:
            final.append(CROSS)
        elif i == 2:
            final.append(TICK)
        else:
            final.append(" ")

    print(grid_structure(*final))


def grid_structure(*pos: str):
    return f"""
    ┌───┬───┬───┐
    │ {pos[0]} │ {pos[1]} │ {pos[2]} │
    ├───┼───┼───┤
    │ {pos[3]} │ {pos[4]} │ {pos[5]} │
    ├───┼───┼───┤
    │ {pos[6]} │ {pos[7]} │ {pos[8]} │
    └───┴───┴───┘
    """


def check_winner(grid_list: list):
    def check_lines(*lines: list):
        """
        Returns the winner's value (1 or 2).
        If there is no winner, returns None.
        Each line must be a list of three cell values.
        """
        for line in lines:
            if 0 in line:
                continue

            if line[0] == line[1] == line[2]:
                return line[0]

        return None

    # check diagonal
    row_1 = grid_list[0:3]
    row_2 = grid_list[3:6]
    row_3 = grid_list[6:9]

    col_1 = grid_list[0::3]
    col_2 = grid_list[1::3]
    col_3 = grid_list[2::3]

    dia_1 = [grid_list[0], grid_list[4], grid_list[8]]
    dia_2 = [grid_list[2], grid_list[4], grid_list[6]]

    return check_lines(
        row_1,
        row_2,
        row_3,
        col_1,
        col_2,
        col_3,
        dia_1,
        dia_2,
    )


def main():
    grid = [0] * 9  # initialise with empty grid

    turn_counter = 1
    while True:
        if turn_counter % 2 == 1:
            player = RED + "Player 1" + RESET
            value = 1
            symbol = CROSS
        else:
            player = BLUE + "Player 2" + RESET
            value = 2
            symbol = TICK

        available_positions = [
            index + 1 for index, value in enumerate(grid) if value == 0
        ]  # + 1 for game index adjustment

        # show the grid with available positions
        helper_index = [
            str(x) if x in available_positions else " " for x in VALID_POSITIONS
        ]

        while True:  # loop to iterate till a correct input is received
            print(YELLOW, "Use this index numbers to choose your position", RESET)
            print(YELLOW, grid_structure(*helper_index), RESET)

            print(f"{player} ({symbol}) turn ")
            show_grid(grid)
            try:
                pos = int(input("Choose your position: "))
            except ValueError:
                clear()
                print(
                    f"{RED}Invalid position, valid positions are {', '.join(str(x) for x in available_positions)}{RESET}"
                )
                print(f"{RED}Try again{RESET}")
                continue

            if pos not in available_positions:
                clear()
                print(
                    f"{RED}{pos} is not a valid position, valid positions are {', '.join(str(x) for x in available_positions)}{RESET}"
                )
                print(f"{RED}Try again{RESET}")
            else:
                grid[pos - 1] = value  # -1 for the list index adjustment
                break

        clear()
        winner = check_winner(grid)
        if winner:
            show_grid(grid)
            print(f"{player} has won the game")
            break

        # check for tie
        elif all(cell != 0 for cell in grid):
            show_grid(grid)
            print("This game was a Tie")
            break

        else:
            turn_counter += 1


if __name__ == "__main__":
    main()

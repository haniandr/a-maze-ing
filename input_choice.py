import os
import sys
from mazegen.maze_generator import MazeGenerator
from maze_display.ascii_renderer import ASCIIRenderer
from a_maze_ing import a_maze_ing

"""
Option for maniputaling the maze:
    - 1: re-generate a new maze: it's recall the a_maze_ing function
    - 2: show or hide the path from entry to exit: call the display_solution
    and display_maze functions
    - 3: rotate maze colors: it can change the color of maze into purple or
    yellow or blue or green
    - 4: quit the program
"""


def input_choices(
    maze: MazeGenerator,
    renderer: ASCIIRenderer,
    solution: list[tuple[int, int]],
    file_name: str,
) -> None:
    """
Handle the user's menu choices.

The user can regenerate the maze, toggle the solution display,
change the color theme, or quit the program.

Args:
    maze: The maze currently displayed.
    renderer: The ASCII renderer used to display the maze.
    solution: The path from the maze entry to its exit.
    file_name: Name of the maze configuration file.
"""

    # When the menu closed, it's totally deseapear
    renderer.print_menu()
    choice = input("Choice? (1-4): ")
    os.system("clear")

    if choice == "1":
        a_maze_ing(file_name)

    elif choice == "2":
        renderer.display_solution = not renderer.display_solution
        renderer.display_maze(maze, solution)
        input_choices(maze, renderer, solution, file_name)

    elif choice == "3":
        renderer.next_color()
        renderer.display_maze(maze, solution)
        input_choices(maze, renderer, solution, file_name)

    elif choice == "4":
        sys.exit(0)

    # Return the menu
    else:
        renderer.display_maze(maze, solution)
        input_choices(maze, renderer, solution, file_name)

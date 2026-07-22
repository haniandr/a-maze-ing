"""
Entry point script for the A-Maze-Ing project.
This module parses a configuration file describing a maze, generates the
maze using a depth-first search algorithm, solves it, renders it as ASCII
art, and optionally saves it to an output file. It also hands off control
to an interactive input-choice loop once the maze has been displayed.
"""

import sys
from parsing.parsing_file import parse_input_file
from mazegen.algo_dfs import DepthFirstSearch
from maze_display.ascii_renderer import ASCIIRenderer


def a_maze_ing(file_name: str) -> int:
    """
    Generate, solve, render, and save a maze from a config file.
    This is the main orchestration function of the program. It performs,
    in order:
        1. Parsing of the input configuration file.
        2. Maze generation via depth-first search.
        3. Maze solving (pathfinding from entry to exit).
        4. Conversion of the solution path into cardinal directions and
           saving of the maze to an output file.
        5. ASCII rendering of the maze and its solution to the terminal.
        6. Handing off control to an interactive input-choice loop.
    Args:
        file_name: Path to the configuration file describing the maze
            (dimensions, entry/exit points, seed, perfect/imperfect flag,
            output filename, etc.).
    Returns:
        int: 0 on success, -1 if an error occurred at any stage
        (parsing, maze construction, pathfinding, or file saving).
    """
    # Local import to avoid a circular import with input_choice at module
    # load time (input_choice likely imports back from this module).
    from input_choice import input_choices

    # parse the configuration file into a maze_setting object.
    try:
        maze_setting = parse_input_file(file_name)
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1

    # build the maze generator and the ASCII renderer from the
    # parsed settings.
    try:
        maze = DepthFirstSearch(
            width=maze_setting.width,
            height=maze_setting.height,
            entry=(maze_setting.entry_x, maze_setting.entry_y),
            exit=(maze_setting.exit_x, maze_setting.exit_y),
            perfect=maze_setting.is_perfect,
            seed=maze_setting.seed,
        )
        renderer = ASCIIRenderer(
            display_solution=maze_setting.display_solution,
        )
    except Exception as e:
        print(e, file=sys.stderr)
        return -1

    # generate the maze structure (carve walls) and build its
    # hexadecimal (bitmask) representation.
    maze.generate()
    hexa_maze = maze.create_hexa_maze()

    # solve the maze once to get the raw path, then convert that
    # path into a sequence of cardinal directions (N/E/S/W) for saving.
    perfect_maze_path = maze.solver()
    try:
        cardinal_path = maze.find_cardinal_path(perfect_maze_path)
        maze.print_maze_to_file(
            maze_setting.output_filename, hexa_maze, cardinal_path
        )
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1

    # solve the maze again (fresh solution) for display purposes.
    solution = maze.solver()
    if not solution:
        print("Couldn't find the maze's solution.", file=sys.stderr)
        return -1

    # render the maze (and its solution, if enabled) to the
    # terminal as ASCII art.
    renderer.display_maze(maze, solution)

    # enter the interactive menu/input loop, letting the user
    # explore further options (e.g., regenerate, replay solution, etc.).
    try:
        input_choices(maze, renderer, solution, file_name)
    except (KeyboardInterrupt, EOFError):
        # Gracefully exit on Ctrl+C or Ctrl+D without treating it as an
        # error.
        return 0
    return 0


if __name__ == "__main__":
    # Enforce exactly one command-line argument: the config file path.
    if len(sys.argv) > 2:
        print("You can't have more than 1 argument.\n", file=sys.stderr)
        sys.exit(-1)

    if len(sys.argv) == 1:
        print("You can't have no argument.", file=sys.stderr)
        sys.exit(-1)

    a_maze_ing(sys.argv[1])

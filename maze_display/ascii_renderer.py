from mazegen.maze_generator import MazeGenerator
from mazegen.grid import Grid

"""
All colors into ascii colors code
"""
RESET = "\033[0m"

COLOR_SETS = [
    # Default Color
    {
        "wall": "\033[38;5;250m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;46m",
        "exit": "\033[38;5;196m",
        "logo": "\033[38;5;208m",
        "solution": "\033[38;5;51m",
    },
    # Purple Color
    {
        "wall": "\033[38;5;99m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;226m",
        "exit": "\033[38;5;201m",
        "logo": "\033[38;5;39m",
        "solution": "\033[38;5;82m",
    },
    # Blue Color
    {
        "wall": "\033[38;5;214m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;27m",
        "exit": "\033[38;5;160m",
        "logo": "\033[38;5;129m",
        "solution": "\033[38;5;190m",
    },
    # Yellow Color
    {
        "wall": "\033[38;5;33m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;202m",
        "exit": "\033[38;5;118m",
        "logo": "\033[38;5;199m",
        "solution": "\033[38;5;229m",
    },
    # Green Color
    {
        "wall": "\033[38;5;244m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;45m",
        "exit": "\033[38;5;220m",
        "logo": "\033[38;5;93m",
        "solution": "\033[38;5;154m",
    },
]

"""
Regroups all function to print all result:
    - maze generated
    - maze solved
    - menu
"""


class ASCIIRenderer:
    """
    Render a maze in the terminal using ASCII characters and colors.

    The renderer can display the maze solution path and switch between
    different color themes.
    """
    def __init__(
        self, display_solution: bool, color_index: int = 0
    ) -> None:
        self.display_solution = display_solution
        self.color_index = color_index

    # Apply the color into the grid
    @property
    def colors(self) -> dict[str, str]:
        """
        Return the currently selected color set.
        """
        return COLOR_SETS[self.color_index]

    # Apply the next color when the choice is 3 in the menu (change maze color)
    def next_color(self) -> None:
        """
        Switch to the next available color theme.
        """
        self.color_index = (self.color_index + 1) % len(COLOR_SETS)

    def _c(self, key: str, text: str) -> str:
        """
        Apply a color to the given text and reset the terminal color.
        """
        return self.colors[key] + text + RESET

    # Display the grid into ascii format
    def display_maze(
        self,
        maze: MazeGenerator,
        solution: list[tuple[int, int]],
    ) -> None:
        """
        Display the maze in the terminal.

        Args:
            maze: The maze to render.
            solution: The path from the entry to the exit.
        """
        solution_set: set[tuple[int, int]] = set(solution)
        logo_set: set[tuple[int, int]] = set(maze.logo)

        for y in range(maze.height):
            self._print_top_border(maze, y)
            self._print_cell_row(maze, y, solution_set, logo_set)

        self._print_bottom_border(maze)

        print(f"\nSeed: {maze.seed}")
        if not maze.logo:
            print("Can't print 42 logo : the maze is too small")

    # Print the format of top border
    def _print_top_border(self, maze: MazeGenerator, y: int) -> None:
        """
        Print the north walls of a maze row.
        """
        row = self._c("wall", "▪")
        for x in range(maze.width):
            has_north = bool(maze.grid.cells[y][x] & Grid.NORTH)
            seg = "━━━" if has_north else "   "
            row += self._c("wall", seg) + self._c("wall", "▪")
        print(row)

    # Print the format of wall border
    def _print_cell_row(
        self,
        maze: MazeGenerator,
        y: int,
        solution_set: set[tuple[int, int]],
        logo_set: set[tuple[int, int]],
    ) -> None:
        """
        Print the contents of a maze row and its east walls.
        """
        row = self._c("wall", "┃")
        for x in range(maze.width):
            color_key, char = self._get_cell(
                maze, x, y, solution_set, logo_set
            )
            has_east = bool(maze.grid.cells[y][x] & Grid.EAST)
            row += self._c(color_key, f" {char} ")
            row += self._c("wall", "┃") if has_east else "   "[1]
        print(row)

    # Print the format of entry, exit, path and pattern
    def _get_cell(
        self,
        maze: MazeGenerator,
        x: int,
        y: int,
        solution_set: set[tuple[int, int]],
        logo_set: set[tuple[int, int]],
    ) -> tuple[str, str]:
        """
        Determine the character and color used to represent a cell.
        """
        if (x, y) in logo_set:
            return "logo", "█"
        if (x, y) == maze.entry:
            return "entry", "■"
        if (x, y) == maze.exit:
            return "exit", "■"
        if self.display_solution and (x, y) in solution_set:
            return "solution", "●"
        return "tunnel", " "

    # Print the format of bottom border
    def _print_bottom_border(self, maze: MazeGenerator) -> None:
        """
        Print the south walls of the last maze row.
        """
        row = self._c("wall", "▪")
        for x in range(maze.width):
            last_y = maze.height - 1
            has_south = bool(maze.grid.cells[last_y][x] & Grid.SOUTH)
            seg = "━━━" if has_south else "   "
            row += self._c("wall", seg) + self._c("wall", "▪")
        print(row)

    # Print the menu
    def print_menu(self) -> None:
        """
        Display the interactive menu options.
        """
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

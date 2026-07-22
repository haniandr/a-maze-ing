from mazegen.grid import Grid
from abc import ABC, abstractmethod
from typing import Any
import sys


class MazeGenerator(ABC):
    """
    Abstract base class for maze generation algorithms.

    This class stores common maze generation data and provides
    shared utilities such as hexadecimal conversion,
    path formatting, logo placement, and maze output handling.
    """
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int] | None,
        perfect: bool,
        seed: int,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = Grid(width, height)
        self.logo = self.get_logo()

    @abstractmethod
    def generate(self) -> Any: ...

    @abstractmethod
    def solver(self) -> Any: ...

    # Necessary for the imperfect maze
    def verif_3x3(self, nx: int, ny: int) -> bool:
        """
        Check if a 3x3 area contains a valid hole position.

        Returns:
            True if a hole exists in the area, otherwise False.
        """
        for ty in range(-2, 1):
            for tx in range(-2, 1):
                x = nx + tx
                y = ny + ty
                if (
                    self.grid.is_valid(x, y)
                    and self.grid.is_valid(x + 2, y + 2)
                ):
                    if self.is_there_hole(x, y):
                        return True
        return False

    # Check if is there a hole
    def is_there_hole(self, nx: int, ny: int) -> bool:
        """
        Check whether a 3x3 section of the maze is empty.

        Returns:
            True if no walls divide the area , otherwise False.
        """
        for y in range(3):
            for x in range(2):
                if self.grid.cells[ny + y][nx + x] & self.grid.EAST:
                    return False

        for y in range(2):
            for x in range(3):
                if self.grid.cells[ny + y][nx + x] & self.grid.SOUTH:
                    return False
        return True

    # Convert the path into hexadecimal
    def create_hexa_maze(self) -> list[str]:
        """
        Converts the path into hexadecimal

        Returns:
            Stores the result in a list and return
        it in format hexadecimal
        """
        hexa_maze: list[str] = []
        hexa = "0123456789ABCDEF"

        for lines in self.grid.cells:
            new_line: list[str] = []
            for cells in lines:
                new_cell = hexa[cells]
                new_line.append(new_cell)
            hexa_maze.append("".join(new_line))

        return hexa_maze

    # Write the hexadecimale maze into the file.txt (OUTPUT_FILE)
    def print_maze_to_file(
        self,
        file_name: str,
        hexa_maze: list[str],
        entry_to_exit_path: str,
    ) -> None:
        """
        Write the maze in hexadecimal in the file.txt(OUTPU_FILE)

        Args:
            -name of the file to write the maze
            -the maze hexa
        """
        if self.exit is None:
            raise ValueError("Can't print the maze : there is no exit")

        x, y = self.entry
        x2, y2 = self.exit

        try:
            with open(file_name, "w") as file:
                file.write("\n".join(hexa_maze))
                file.write("\n\n")
                file.write(f"{x},{y}\n")
                file.write(f"{x2},{y2}\n")
                file.write(entry_to_exit_path + "\n")
        except OSError as e:
            print(e, file=sys.stderr)
            sys.exit(-1)

    # Convert the path (solver) into coordinate symbol
    def find_cardinal_path(
        self, path: list[tuple[int, int]] | None
    ) -> str:
        if path is None:
            raise ValueError(
                "Can't create a cardinal path : there is no path solution"
            )

        cardinal_path: list[str] = []
        for cell, next_cell in zip(path, path[1:]):
            x, y = cell
            x2, y2 = next_cell
            if x > x2:
                cardinal_path.append("W")
            if x2 > x:
                cardinal_path.append("E")
            if y > y2:
                cardinal_path.append("N")
            if y2 > y:
                cardinal_path.append("S")

        return "".join(cardinal_path)

    """
    Default = center but if entry is in the default coordinate for
    pattern so pattern move
    """
    def get_logo(self) -> list[tuple[int, int]]:
        width = self.width
        while width > 9:
            height = self.height
            while height > 7:
                possible_logo = self.create_logo(width, height)
                if self.is_logo_valid(possible_logo):
                    return possible_logo
                height -= 1
            width -= 1
        return []

    # Check if the cell is logo
    def is_logo_valid(self, logo: list[tuple[int, int]]) -> bool:
        return self.entry not in logo and self.exit not in logo

    # Create the pattern, default = 42
    @staticmethod
    def create_logo(width: int, height: int) -> list[tuple[int, int]]:
        x = (width - 1) // 2
        y = (height - 1) // 2

        logo: list[tuple[int, int]] = [
            (x - 3, y - 2),
            (x - 3, y - 1),
            (x - 3, y),
            (x - 2, y),
            (x - 1, y),
            (x - 1, y + 1),
            (x - 1, y + 2),
            (x + 1, y - 2),
            (x + 2, y - 2),
            (x + 3, y - 2),
            (x + 3, y - 1),
            (x + 3, y),
            (x + 2, y),
            (x + 1, y),
            (x + 1, y + 1),
            (x + 1, y + 2),
            (x + 2, y + 2),
            (x + 3, y + 2),
        ]
        return logo

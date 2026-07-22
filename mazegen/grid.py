class Grid:
    """
    Direction must be defined by their coordonate follow axe(x) and axe(y)
    """
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000

    OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
    DELTA = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: list[list[int]] = []
        self.create_grid()

    # Full width and height by cells
    def create_grid(self) -> None:
        """
        Initialize the grid with all walls present.

        Each cells starts with a value 0xF,
        meaning that the four walls(N,E,S,W) are closed.
        """
        self.cells = []
        for _ in range(self.height):
            line: list[int] = []
            for _ in range(self.width):
                line.append(0xF)
            self.cells.append(line)

    # Break the wall for creating a path.
    def remove_wall(self, x: int, y: int, direction: int) -> None:
        """
        Remove a wall between a cell and its neighbor.

        The opposite wall of the neighboring cell
        is also removed to keep the grid consistent.
        """
        dx, dy = self.DELTA[direction]
        nx = x + dx
        ny = y + dy

        if not self.is_valid(nx, ny):
            return

        self.cells[y][x] &= ~direction
        self.cells[ny][nx] &= ~self.OPPOSITE[direction]

    # Opposite of remove_wall, it add wall
    def add_wall(self, x: int, y: int, direction: int) -> None:
        """
        Add a wall between a cell and its neighbor.
        """
        dx, dy = self.DELTA[direction]
        nx = x + dx
        ny = y + dy

        if not self.is_valid(nx, ny):
            return

        self.cells[y][x] |= direction
        self.cells[ny][nx] |= self.OPPOSITE[direction]

    # Check if cell is not overflowed the grid
    def is_valid(self, x: int, y: int) -> bool:
        """
        Check if a cell is inside the grid or not.
        """
        return 0 <= x < self.width and 0 <= y < self.height

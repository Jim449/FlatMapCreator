from cell import Cell


class Grid():
    """Represents a square area"""

    def __init__(self, length: int, height: int):
        """Creates a new grid containing given amount of cells
        horizontally and vertically"""
        self.content: dict[tuple, Cell] = {}
        self.length = length
        self.height = height
        self.ix: int = 0
        self.iy: int = 0

        for x in range(length):
            for y in range(height):
                self.add(x, y, 10)

    def add(self, x: int, y: int, terrain: int) -> None:
        """Creates a new cell at (x, y)"""
        self.content[(x, y)] = Cell(x, y, terrain)

    def get(self, x: int, y: int) -> Cell:
        """Returns the cell at (x, y)

        Throws:
            KeyError"""
        return self.content[(x, y)]

    def get_all(self, positions: list[tuple[int]]) -> list[Cell]:
        """Returns a list of cells corresponding to a list of coordinates (x, y).
        If any coordinate is out-of-bounds, None is placed on that index."""
        result = []

        for coordinates in positions:
            try:
                result.append(self.content[coordinates])
            except KeyError:
                result.append(None)
        return result

    def get_square(self, x: int, y: int, offset: int) -> list[Cell]:
        """Returns 10x10 cells, where the northwest cell has coordinates (x - offset, y - offset).
        Out-of-bound cells are skipped."""
        result = []

        for sub_x in range(x*10 - offset, (x + 1)*10 - offset):
            for sub_y in range(y*10 - offset, (y + 1)*10 - offset):
                try:
                    result.append(self.get(sub_x, sub_y))
                except KeyError:
                    pass
        return result

    def get_main_terrain(self, x: int, y: int) -> int:
        """Returns the most common terrain in the square area given by get_square(x, y, 0)"""
        terrain_count = dict[int, int] = {}
        main_terrain: int = 0
        main_count: int = 0

        for cell in self.get_square(x, y, 0):
            if cell.terrain in terrain_count:
                terrain_count[cell.terrain] += 1
            else:
                terrain_count[cell.terrain] = 1

        for terrain, count in terrain_count.items():
            if count > main_count:
                main_terrain = terrain
                main_count = count
        return main_terrain

    def get_unique_terrain(self) -> list[int]:
        """Returns a list of all terrain types in this grid"""
        result = set()

        for cell in self.content.values():
            result.add(cell.terrain)

    def filter_terrain(self, terrain: int) -> list[Cell]:
        """Returns a list of cells with the given terrain type"""
        result = []

        for cell in self.content.values():
            if cell.terrain == terrain:
                result.append(cell)

    def __iter__(self):
        self.ix = 0
        self.iy = 0
        return self

    def __next__(self) -> Cell:
        if self.ix == self.length:
            self.ix = 0

            if self.iy == self.height - 1:
                raise StopIteration
            else:
                self.iy += 1
        item = self.get(self.ix, self.iy)
        self.ix += 1
        return item

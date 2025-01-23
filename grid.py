from cell import Cell
from typing import Self
import constants as c


class Grid():
    """Represents a square area"""

    def __init__(self, length: int, height: int,
                 start_x: int = 0, start_y: int = 0):
        """Creates a new grid containing given amount of cells
        horizontally and vertically"""
        self.content: dict[tuple, Cell] = {}
        self.length = length
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.ix: int = 0
        self.iy: int = 0

        for x in range(start_x, start_x + length):
            for y in range(start_y, start_y + height):
                self.add(x, y, 10)

    def add(self, x: int, y: int, terrain: int) -> None:
        """Creates a new cell at (x, y)"""
        self.content[(x, y)] = Cell(x, y, terrain)

    def add_cell(self, x: int, y: int, cell: Cell) -> None:
        """Adds a cell at (x, y)"""
        self.content[(x, y)] = cell

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

    def get_close_surroundings(self, x: int, y: int) -> list[Cell]:
        return self.get_all(c.get_close_surroundings(x, y))

    def get_area(self, x: int, y: int, length: int = 10, height: int = 10) -> list[Cell]:
        """Returns a list of cells, occupying a rectangular area.
        Out of bound cells are ignored"""
        result = []

        for sub_x in range(x, x + length):
            for sub_y in range(y, y + height):
                try:
                    result.append(self.get(sub_x, sub_y))
                except KeyError:
                    pass
        return result

    def _get_horizontal_edge(self, start_x: int, start_y: int, direction: int,
                             length: int, height: int) -> list[Cell]:
        """Returns the horizontal edge on the north or south side of a rectangle"""
        result = []
        y = start_y if direction == c.NORTH else start_y + height - 1

        for x in range(start_x, start_x + length):
            try:
                result.append(self.get(x, y))
            except KeyError:
                pass
        return result

    def _get_vertical_edge(self, start_x: int, start_y: int, direction: int,
                           length: int, height: int) -> list[Cell]:
        """Returns a vertical edge on the west or east side of a rectangle"""
        result = []
        x = start_x if direction == c.WEST else start_x + length - 1

        for y in range(start_y, start_y + height):
            try:
                result.append(self.get(x, y))
            except KeyError:
                pass
        return result

    def get_edge(self, x: int, y: int, direction: int,
                 length: int = 10, height: int = 10) -> list[Cell]:
        """Returns a list of cells, occupying the edge of a rectangular area.
        Out of bound cells are ignored"""
        if direction in (c.NORTH, c.SOUTH):
            return self._get_horizontal_edge(x, y, direction, length, height)
        elif direction in (c.WEST, c.EAST):
            return self._get_vertical_edge(x, y, direction, length, height)

    def get_subgrid(self, x: int, y: int, length: int, height: int) -> Self:
        """Creates a new grid, containing a rectangular subset of this grid.
        Changing cells in the new grid will affect this grid"""
        result = Grid(length, height, x, y)

        for sub_x in range(x, x + length):
            for sub_y in range(y, y + height):
                try:
                    result.add_cell(sub_x, sub_y, self.get(sub_x, sub_y))
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
            if c.is_terrain(cell.terrain, terrain):
                result.append(cell)
        return result

    def __iter__(self):
        self.ix = self.start_x
        self.iy = self.start_y
        return self

    def __next__(self) -> Cell:
        if self.ix == self.start_x + self.length:
            self.ix = self.start_x

            if self.iy == self.start_y + self.height - 1:
                raise StopIteration
            else:
                self.iy += 1
        item = self.get(self.ix, self.iy)
        self.ix += 1
        return item

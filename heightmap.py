from grid import Grid
from cell import Cell
import random
import constants as c


class Heightmap():
    def __init__(self, grid: Grid, start_x: int, start_y: int,
                 min_random: int = -1, max_random: int = 3):
        """Generates a heightmap on an area of size 9x9.
        Uses the diamond square algorithm.
        Heightmaps should be applied on steps of 8 cells.
        This will cause heightmaps to slightly overlap.
        The heightmap doesn't have to be entirely within grid bounds.
        Non-mountainous cells will get minimum elevation.
        A cell will only be given a new elevation if it's current elevation is None. 
        """
        self._generate_heights(grid, start_x, start_y,
                               3, min_random, max_random)

    def _randomize_elevation(self, grid: Grid, x: int, y: int) -> None:
        """Generates a random starting elevation for a cell.
        The value is chosen from 0 to twice the mountain depth.
        If elevation is not None, the cell retains its current elevation."""
        try:
            cell = grid.get(x, y)

            if cell.elevation == None and c.is_terrain(cell.terrain, c.MOUNTAIN):
                cell.elevation = random.randrange(
                    0, 1 + cell.mountain_depth * 2)
            elif cell.elevation == None:
                cell.elevation = 0
        except KeyError as e:
            pass

    def _set_flatlands(self, grid: Grid, x: int, y: int) -> None:
        """If the cell is not mountainous, its elevation is set to 0
        and will not change."""
        try:
            cell = grid.get(x, y)

            if c.is_terrain(cell.terrain, c.MOUNTAIN) == False:
                cell.elevation = 0
        except KeyError:
            pass

    def _set_flat_edges(self, grid: Grid, start_x: int, start_y: int, size: int) -> None:
        """Checks the edges of the heightmap for any non-mountainous cells.
        Sets the elevation of those cells to 0."""
        for x in range(start_x, start_x + size):
            self._set_flatlands(grid, x, start_y)
            self._set_flatlands(grid, x, start_y + size - 1)

        for y in range(start_y + 1, start_y + size - 1):
            self._set_flatlands(grid, start_x, y)
            self._set_flatlands(grid, start_x + size - 1, y)

    def _set_elevation(self, cell: Cell, elevation: int) -> None:
        """Sets elevation of a cell. Only applies if the cells elevation is None.
        Changes cell terrain as needed"""
        if cell.elevation == None:
            cell.elevation = elevation

            if elevation > 0:
                cell.set_terrain(c.MOUNTAIN)
            elif elevation < 0:
                cell.set_terrain(c.WATER)
            elif c.is_terrain(cell.terrain, c.MOUNTAIN):
                cell.set_terrain(c.LAND)

    def _get_elevation(self, grid: Grid, x: int, y: int) -> int:
        """Returns the elevation of a cell. Returns 0 if elevation is None
        or if there's no cell at the coordinate"""
        try:
            cell = grid.get(x, y)
            if cell.elevation == None:
                return 0
            else:
                return cell.elevation
        except KeyError as e:
            pass
            return 0

    def _get_random(self, min_random: float, max_random: float) -> float:
        """Returns a random value from min_random to max_random"""
        return min_random + random.random() * (max_random - min_random)

    def _diamond_step(self, grid: Grid, start_x: int, start_y: int, size: int,
                      step: int, min_random: float, max_random: float) -> None:
        half = step // 2

        for x in range(start_x + half, start_x + size, step):
            for y in range(start_y + half, start_y + size, step):
                try:
                    cell = grid.get(x, y)
                except KeyError as e:
                    continue

                northeast = self._get_elevation(grid, x + half, y - half)
                southeast = self._get_elevation(grid, x + half, y + half)
                southwest = self._get_elevation(grid, x - half, y + half)
                northwest = self._get_elevation(grid, x - half, y - half)
                value = (northeast + southeast + southwest + northwest) / 4

                if cell.terrain == c.MOUNTAIN:
                    result = round(
                        value + self._get_random(min_random, max_random))
                else:
                    result = round(value)

                self._set_elevation(cell, result)

    def _square_step(self, grid: Grid, start_x: int, start_y: int, size: int,
                     step: int, min_random: float, max_random: float) -> None:
        half = step // 2

        for x in range(start_x, start_x + size, half):
            for y in range(start_y + (x + half) % step, start_y + size, step):
                try:
                    cell = grid.get(x, y)
                except KeyError as e:
                    continue

                north = self._get_elevation(grid, x, y - half)
                east = self._get_elevation(grid, x + half, y)
                south = self._get_elevation(grid, x, y + half)
                west = self._get_elevation(grid, x - half, y)
                value = (north + east + south + west) / 4

                if cell.terrain == c.MOUNTAIN:
                    result = round(
                        value + self._get_random(min_random, max_random))
                else:
                    result = round(value)
                self._set_elevation(cell, result)

    def _generate_heights(self, grid: Grid, start_x: int, start_y: int,
                          exponent: int, min_random: int, max_random) -> None:
        """Generates a heightmap on an area of size 2^exponent + 1.
        Uses the diamond square algorithm"""
        size = 2 ** exponent + 1

        self._set_flat_edges(grid, start_x, start_y, size)
        self._randomize_elevation(grid, start_x, start_y)
        self._randomize_elevation(grid, start_x + size - 1, start_y)
        self._randomize_elevation(grid, start_x, start_y + size - 1)
        self._randomize_elevation(grid, start_x + size - 1,
                                  start_y + size - 1)

        step = 2 ** exponent

        while (step > 1):
            self._diamond_step(grid, start_x, start_y,
                               size, step, min_random, max_random)
            self._square_step(grid, start_x, start_y,
                              size, step, min_random, max_random)
            min_random = min_random / 2
            max_random = max_random / 2
            step = step // 2


# Testing!
if __name__ == "__main__":
    grid: Grid = Grid(9, 9)

    for cell in grid:
        cell.set_terrain(c.MOUNTAIN)
        cell.mountain_depth = 1

    for x in range(9):
        grid.get(x, 0).set_terrain(c.LAND)
        grid.get(x, 0).mountain_depth = 0
        grid.get(x, 1).set_terrain(c.LAND)
        grid.get(x, 1).mountain_depth = 0

    heightmap: Heightmap = Heightmap(grid, 0, 0, -1, 3)

    for y in range(9):
        print()
        for x in range(9):
            print(grid.get(x, y).elevation, end=" ")
    print()
    print()

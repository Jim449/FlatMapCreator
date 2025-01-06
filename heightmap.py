from grid import Grid
from cell import Cell
import random
import constants as c


class Heightmap():
    def __init__(self, grid: Grid, start_x: int, start_y: int):
        """Generates a heightmap on an area of size 9x9.
        Uses the diamond square algorithm"""

        self._generate_heights(grid, start_x, start_y, 3)

        # I thought about generating a heightmap of size 11x11
        # but that won't go as smoothly
        # for step in range(0, 7, 2):
        #     self._generate_heights(grid, start_x + 8, start_y + step, 1)
        #     self._generate_heights(grid, start_x + step, start_y + 8, 1)

        # self._generate_heights(grid, start_x + 8, start_y + 8, 1)

    def _randomize_elevation(self, cell: Cell, maximum: int = 1) -> None:
        # Sets a random elevation
        # If the cell is not mountainous, it should have elevation 0
        # If it is mountainous, I can set a higher elevation
        # Maybe I should account for depth
        # Setting a high elevation on a cell close to the mountain edge
        # may lead to problems
        # On the other hand, it could force the creation
        # of more interesting mountain borders

        if cell.elevation == None and c.is_terrain(cell.terrain, c.MOUNTAIN):
            cell.elevation = random.randrange(1, maximum + 1)
        elif cell.elevation == None:
            cell.elevation = 0

    def _set_elevation(self, cell: Cell, elevation: int) -> None:
        if cell.elevation == None:
            cell.elevation = elevation

            if elevation == 0:
                cell.terrain = c.LAND
            else:
                cell.terrain = c.MOUNTAIN

    def _diamond_step(self, grid: Grid, start_x: int, start_y: int, size: int,
                      step: int, random_scale: float) -> None:
        half = step // 2

        for x in range(start_x + half, start_x + size, step):
            for y in range(start_y + half, start_y + size, step):
                northeast = grid.get(x + half, y - half).elevation
                southeast = grid.get(x + half, y + half).elevation
                southwest = grid.get(x - half, y + half).elevation
                northwest = grid.get(x - half, y - half).elevation
                value = (northeast + southeast + southwest + northwest) / 4

                # If it's not a mountain, I want to limit the size
                # Hopefully, removing the random addition will do that
                if grid.get(x, y).terrain == c.MOUNTAIN:
                    result = round(value + random.random() * random_scale)
                    # try maximizing
                    # result = round(value + random_scale)
                else:
                    result = round(value)

                self._set_elevation(grid.get(x, y), result)
                # print(f"Diamond step on ({x}, {y}) yielding average {
                #       value} and elevation {result}")

    def _get_elevation_or_zero(self, grid: Grid, x: int, y: int) -> int:
        try:
            elevation = grid.get(x, y).elevation

            if elevation == None:
                return 0
            else:
                return elevation
        except KeyError:
            return 0

    def _square_step(self, grid: Grid, start_x: int, start_y: int, size: int,
                     step: int, random_scale: float) -> None:
        half = step // 2

        for x in range(start_x, start_x + size, half):
            for y in range(start_y + (x + half) % step, start_y + size, step):
                north = self._get_elevation_or_zero(grid, x, y - half)
                east = self._get_elevation_or_zero(grid, x + half, y)
                south = self._get_elevation_or_zero(grid, x, y + half)
                west = self._get_elevation_or_zero(grid, x - half, y)
                value = (north + east + south + west) / 4

                if grid.get(x, y).terrain == c.MOUNTAIN:
                    result = round(value + random.random() * random_scale)
                    # try maximizing
                    # result = round(value + random_scale)
                else:
                    result = round(value)
                # print(f"Square step on ({x}, {y}) yielding average {
                #       value} and elevation {result}")
                self._set_elevation(grid.get(x, y), result)

    def _generate_heights(self, grid: Grid, start_x: int, start_y: int,
                          exponent: int) -> None:
        """Generates a heightmap on an area of size 2^exponent + 1.
        Uses the diamond square algorithm"""
        size = 2 ** exponent + 1

        print(f"Generating heightmap of size {size} at ({start_x}, {start_y})")

        self._randomize_elevation(grid.get(start_x, start_y), 1)
        self._randomize_elevation(grid.get(start_x + size - 1, start_y), 1)
        self._randomize_elevation(grid.get(start_x, start_y + size - 1), 1)
        self._randomize_elevation(
            grid.get(start_x + size - 1, start_y + size - 1), 1)

        step = 2 ** exponent
        random_scale = 3

        while (step > 1):
            self._diamond_step(grid, start_x, start_y,
                               size, step, random_scale)
            self._square_step(grid, start_x, start_y,
                              size, step, random_scale)
            random_scale = random_scale / 2
            step = step // 2


# Testing!
if __name__ == "__main__":
    grid: Grid = Grid(9, 9)

    for cell in grid:
        cell.set_terrain(c.MOUNTAIN)

    # Try non-mountainous terrain to the west
    # Can I get a slope?
    # for y in range(8):
    #     grid.get(0, y).terrain = c.LAND

    # Set elevation in the corners
    grid.get(0, 0).elevation = 1
    grid.get(8, 0).elevation = 1
    grid.get(0, 8).elevation = 1
    grid.get(8, 8).elevation = 1

    heightmap: Heightmap = Heightmap(grid, 0, 0)

    for y in range(9):
        print()
        for x in range(9):
            print(grid.get(x, y).elevation, end=" ")
    print()

    # Yeah, that's fine.
    # However!
    # I need a guideline for determining acceptable initial elevation
    # One possibility would be to calculate depth of mountain areas
    # So the border would have depth 1
    # Then I raise depth as I go towards the mountain ranges center
    # Moreover, I want to limit the height of cells
    # which have non-mountain cells as neighbors
    # I don't want to check more neighbors than necessary,
    # since I'm already doing something similar in the algorithm

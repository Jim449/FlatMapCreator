from cell import Cell
from grid import Grid
import constants as c


class OffsetGrid():
    def __init__(self, grid: Grid, fine_grid: Grid):
        self.grid: Grid = grid
        self.fine_grid: Grid = fine_grid

    def get(self, x: int, y: int) -> list[Cell]:
        return self.grid.get_all(c.get_square(x, y, c.SOUTHWEST))

    def get_details(self, x: int, y: int) -> list[Cell]:
        self.fine_grid.get_square(x, y, 5)

    def get_entrance(self, x: int, y: int, inner_terrain: int) -> int | None:
        pass

    def get_exit(self, x: int, y: int, inner_terrain: int) -> int | None:
        pass

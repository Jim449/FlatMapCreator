from grid import Grid
from area import Area
from random import randrange
import constants as c


class World():
    def __init__(self, regions: int):
        self.square_regions: Grid = Grid(regions, regions)
        self.square_miles: Grid = Grid(regions * 10, regions * 10)
        self.square_kilometers: Grid = None
        self.areas: list[Area] = []
        self.regions = regions
        self.fixed_growth = False

    def create_areas(self, total_amount: int, sea_amount: int, land_amount: int,
                     sea_margin: float = 0.25, fixed_growth: bool = False) -> None:
        """Creates areas on random starting points"""
        self.fixed_growth = fixed_growth

        for i in range(total_amount):
            while True:
                start_x = randrange(self.regions * 10)
                start_y = randrange(self.regions * 10)
                origin = self.square_miles.get(start_x, start_y)

                if origin.area == -1:
                    break

            if land_amount > 0:
                type = c.LAND
                land_amount -= 1
            elif sea_amount > 0:
                type = c.WATER
                sea_amount -= 1
            else:
                type = randrange(8)

            self.areas.append(Area(id=i,
                                   grid=self.square_miles,
                                   start_x=start_x,
                                   start_y=start_y,
                                   type=type,
                                   sea_margin=sea_margin))

    def expand_areas(self) -> bool:
        """Expands all areas once.
        Returns true if areas cover the entire map"""
        finished = True

        for area in self.areas:
            if area.alive:
                finished = False
            else:
                continue

            if self.fixed_growth:
                area.expand()
            else:
                area.expand_blindly()

        return finished

    def build_areas(self) -> None:
        """Expands all areas until the entire world is covered"""
        while True:
            if self.expand_areas():
                break

    def create_land(self) -> None:
        """Creates land and water on all areas"""
        for area in self.areas:
            area.create_land()

    def find_boundaries(self, grid: Grid):
        for y in range(1, grid.height):
            cell = grid.get(0, y)

            for x in range(1, grid.length):
                previous = cell
                cell = grid.get(x, y)

                if previous.area != cell.area:
                    previous.east_boundary = True
                    cell.west_boundary = True

        for x in range(grid.length):
            cell = grid.get(x, 0)

            for y in range(grid.height):
                previous = cell
                cell = grid.get(x, y)

                if previous.area != cell.area:
                    previous.south_boundary = True
                    cell.north_boundary = True

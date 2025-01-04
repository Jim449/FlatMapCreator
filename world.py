from grid import Grid
from cell import Cell
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

    def get_area(self, id: int) -> None:
        """Returns an area"""
        return self.areas[id]

    def create_land(self) -> None:
        """Creates land and water on all areas"""
        for area in self.areas:
            area.create_land()

    def create_coastline(self, cell_1: Cell, cell_2: Cell):
        if cell_1.terrain == cell_2.terrain:
            return
        elif cell_1.terrain in (c.WATER, c.SHALLOWS) and cell_2.terrain == c.LAND:
            cell_1.terrain = c.SHORE
        elif cell_1.terrain == c.LAND and cell_2.terrain in (c.WATER, c.SHALLOWS):
            cell_2.terrain = c.SHORE

    def find_boundaries(self, grid: Grid):
        for y in range(1, grid.height):
            cell = grid.get(0, y)

            for x in range(1, grid.length):
                previous = cell
                cell = grid.get(x, y)

                if previous.area != cell.area:
                    previous.east_boundary = True
                    cell.west_boundary = True

                # Do a coastline check while I'm at it
                # That should improve the graphics
                # Not yet. Maybe if I have a better LAND / WATER check
                # Simply adding shallows doesn't do much
                # It adds some smoothness but I can do without that
                # I could try lengthening the shallows by 1
                # But then I have to consider diagonals as well
                # What if I do a shallows check similar to the land check
                # That could be nice...
                # Adding a shore isn't too bad
                # It looks a bit thin in some places and edgier in others
                # It's too thin. It has to occupy 2 cells!
                # I know one thing which would probably look really nice...
                # doing a depth search and painting the far inland in a lighter hue
                # do the same thing for water in order to create long shallows
                # and some dark depths
                self.create_coastline(cell, previous)

        for x in range(grid.length):
            cell = grid.get(x, 0)

            for y in range(grid.height):
                previous = cell
                cell = grid.get(x, y)

                if previous.area != cell.area:
                    previous.south_boundary = True
                    cell.north_boundary = True

                # Another coastline check
                # self.create_coastline(cell, previous)

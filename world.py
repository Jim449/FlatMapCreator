from grid import Grid
from cell import Cell
from area import Area
from heightmap import Heightmap
from boundary import Boundary
from random import randrange, shuffle
import constants as c


class World():
    def __init__(self, regions: int):
        self.square_regions: Grid = Grid(regions, regions)
        self.square_miles: Grid = Grid(regions * 10, regions * 10)
        self.square_kilometers: Grid = None
        self.zoomed_square_miles: Grid = None
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

    def create_coastline(self, center: Cell, outskirts: list[Cell]):
        """Changes cell terrain to SHORE if it has LAND terrain
        and at least one surrounding cell has WATER terrain"""
        # Skip shore for now. Coastal areas will probably look better in a brighter color
        # if center.terrain == c.SHORE:
        #     center.set_terrain(c.LAND)
        if center.terrain == c.SHALLOWS:
            center.set_terrain(c.WATER)

        # if center.terrain == c.LAND:
        #     for cell in outskirts:
        #         if cell != None and c.is_terrain(cell.terrain, c.WATER):
        #             center.set_terrain(c.SHORE)
        #             return
        if center.terrain == c.WATER:
            for cell in outskirts:
                if cell != None and c.is_terrain(cell.terrain, c.LAND):
                    center.set_terrain(c.SHALLOWS)
                    return

    def update_coastlines(self, grid: Grid) -> None:
        """Finds cell located by the coast and changes
        their terrain to SHORE"""
        for cell in grid:
            surroundings = c.get_surroundings(cell.x, cell.y)
            outskirts = grid.get_all(surroundings)
            self.create_coastline(cell, outskirts)

    def find_boundaries(self, grid: Grid) -> None:
        """Finds all cells which are situated by area borders.
        Set cell variables to indicate border direction"""
        for y in range(1, grid.height):
            cell = grid.get(0, y)

            for x in range(1, grid.length):
                previous = cell
                cell = grid.get(x, y)

                if previous.area != cell.area:
                    previous.east_boundary = True
                    cell.west_boundary = True
                else:
                    previous.east_boundary = False
                    cell.west_boundary = False

        for x in range(grid.length):
            cell = grid.get(x, 0)

            for y in range(grid.height):
                previous = cell
                cell = grid.get(x, y)

                if previous.area != cell.area:
                    previous.south_boundary = True
                    cell.north_boundary = True
                else:
                    previous.south_boundary = False
                    cell.north_boundary = False

    def _square_mile_to_heightmap(self, value: int, last: bool = False) -> int:
        if last:
            value = value * 10 + 9
        else:
            value = value * 10
        # Try using 16 instead of 8. Larger heightmaps might look smoother
        return value - value % 16

    def get_heightmap_coordinates(self, square_miles: Grid) -> set[tuple[int]]:
        """For each mountainous square_mile cell in the given grid,
        finds starting coordinates for heightmaps.
        Together, those heightmaps will cover all of the square mile cells.
        Returns a set of coordinates."""
        result = set()

        for cell in square_miles:
            # Translate from 10-cell grid to 8-cell grid
            # A square of 10x10 may overlap at most 9 squares of 8x8
            # But as long as both grids start from 0,
            # there are only 4 possible overlaps
            if c.is_terrain(cell.terrain, c.MOUNTAIN):
                result.add((self._square_mile_to_heightmap(cell.x),
                            self._square_mile_to_heightmap(cell.y)))
                result.add((self._square_mile_to_heightmap(cell.x, True),
                            self._square_mile_to_heightmap(cell.y)))
                result.add((self._square_mile_to_heightmap(cell.x),
                            self._square_mile_to_heightmap(cell.y, True)))
                result.add((self._square_mile_to_heightmap(cell.x, True),
                            self._square_mile_to_heightmap(cell.y, True)))

                # Try creating more heightmaps for smoother transitions
                # I want to to the northwest, since some heightmaps may end abruptly there
                result.add((self._square_mile_to_heightmap(cell.x - 1),
                            self._square_mile_to_heightmap(cell.y)))
                result.add((self._square_mile_to_heightmap(cell.x),
                            self._square_mile_to_heightmap(cell.y - 1)))
                result.add((self._square_mile_to_heightmap(cell.x - 1),
                            self._square_mile_to_heightmap(cell.y - 1)))
        return result

    def _sort_heightmaps(self, heightmaps: list[Heightmap]) -> None:
        for i in range(len(heightmaps) - 1):
            for j in range(1, len(heightmaps)):
                heightmap = heightmaps[i]

                if heightmaps[j].start_y < heightmap.start_y:
                    heightmaps[i] = heightmaps[j]
                    heightmaps[j] = heightmap

    def create_heightmaps(self, square_miles: Grid) -> None:
        """Generates heightmap on areas of 8x8 square miles,
        so that all the given mountainous cells are covered.
        The resulting heightmaps will be 9x9 square miles,
        overlapping neighboring cells slightly"""
        starting_points = self.get_heightmap_coordinates(square_miles)
        heightmaps: list[Heightmap] = []
        coordinates = list(starting_points)
        shuffle(coordinates)
        finished = False

        for x, y in coordinates:
            heightmaps.append(Heightmap(self.square_kilometers, x, y,
                                        min_random=-2, max_random=6, exponent=4))

        while not finished:
            for heightmap in heightmaps:
                finished = heightmap.next_iteration()

        # I shouldn't need this. Maybe after I've improved the algorithm
        # self._sort_heightmaps(heightmaps)

        # for heightmap in heightmaps:
        #     heightmap.tilt()

    def zoom_in(self, start_x: int, start_y: int) -> Grid:
        """Generates a square kilometer grid representing
        a zoomed-in area on the square mile grid"""

        self.square_kilometers = Grid(400, 400, start_x * 100, start_y * 100)
        self.zoomed_square_miles = self.square_miles.get_subgrid(
            start_x * 10, start_y * 10, 40, 40)

        for mile_cell in self.zoomed_square_miles:
            mile_x = mile_cell.x * 10
            mile_y = mile_cell.y * 10

            for kilometer_cell in self.square_kilometers.get_area(mile_x, mile_y, 10, 10):
                kilometer_cell.inherit(mile_cell)

        # self.create_heightmaps(self.zoomed_square_miles)
        boundary = Boundary()
        boundary.find_from_sqare_miles(self.square_kilometers, self.zoomed_square_miles,
                                       c.LAND, c.WATER)
        # Decent
        # Wobble that line! Repetitions at 2
        # Looks blocky but if I overdo it, it gets really blurry
        # Consider tweaking the algorithm
        # Try selecting lines of land/water
        # It might lead to a smoother result
        # Try making newly turned cells unturnable for a short while
        # In that case, I'd need to lower quota to less than 0.5
        boundary.wobble(self.square_kilometers, 0.5, 2)
        boundary.set_exterior_terrain(c.SHALLOWS)
        return self.square_kilometers

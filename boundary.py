from grid import Grid
from cell import Cell
from random import choice
import constants as c


class Boundary():
    """Represents the border between two terrain types or an area border"""

    def __init__(self):
        """Creates an empty boundary"""
        self.interior: list[list[Cell]] = []
        self.exterior: list[Cell] = []
        self.discovered: set[Cell] = set()
        self.interior_terrain: int = 0
        self.exterior_terrain: int = 0

    def _add(self, cell: Cell, cells: list[Cell]) -> bool:
        """Adds a cell to a list of cells and the set of discovered cells"""
        if cell not in self.discovered:
            cells.append(cell)
            self.discovered.add(cell)
            return True
        else:
            return False

    def _add_all(self, cells: list[Cell], destination: list[Cell]) -> None:
        for cell in cells:
            self._add(cell, destination)

    def find_terrain_boundary(self, grid: Grid, interior_terrain: int,
                              exterior_terrain: int) -> None:
        """Finds any terrain boundary.
        TODO: consider replacing this method with more precise methods"""
        self.interior = [[]]
        self.exterior = []
        self.discovered = set()
        self.interior_terrain = interior_terrain
        self.exterior_terrain = exterior_terrain

        for cell in grid.filter_terrain(exterior_terrain):
            for neighbor in grid.get_close_surroundings(cell.x, cell.y):
                if c.is_terrain(neighbor.terrain, interior_terrain):
                    self._add(cell, self.exterior)
                    self._add(neighbor, self.interior[0])

    def find_from_sqare_miles(self, grid: Grid, square_miles: Grid,
                              interior_terrain: int, exterior_terrain: int) -> None:
        """Finds all terrain boundaries on a square kilometer level
        only when all terrain borders are set on a square mile level.
        This is useful when constructing the square kilometer grid"""
        self.interior = [[]]
        self.exterior = []
        self.discovered = set()
        self.interior_terrain = interior_terrain
        self.exterior_terrain = exterior_terrain

        for square_mile in square_miles.filter_terrain(exterior_terrain):
            for direction, neighbor in enumerate(square_miles.get_close_surroundings(
                    square_mile.x, square_mile.y)):
                if neighbor != None and c.is_terrain(neighbor.terrain, interior_terrain):
                    exterior = grid.get_edge(square_mile.x * 10, square_mile.y * 10,
                                             direction * 2)
                    interior = grid.get_edge(neighbor.x * 10, neighbor.y * 10,
                                             c.flip_direction(direction * 2))
                    self._add_all(exterior, self.exterior)
                    self._add_all(interior, self.interior[0])

    def get_sample(self, cells: list[Cell], quota: float) -> list[Cell]:
        """Returns a sample of cells from a list"""
        amount = int(len(cells) * quota)
        result = []

        while amount > 0:
            result.append(choice(cells))
            amount -= 1

        return result

    def _check_exclusion(self, grid: Grid, cell: Cell, neighboring_terrain: int) -> bool:
        """Checks if the cell has any neighbors of the given terrain.
        If it has no neighbors but exist in the set of discovered cells,
        returns true to signal that the cell should be excluded from the boundary.
        Otherwise, returns false"""
        if cell not in self.discovered:
            return False

        surroundings = grid.get_close_surroundings(cell.x, cell.y)

        for neighbor in surroundings:
            if c.is_terrain(neighbor.terrain, neighboring_terrain):
                return False
        return True

    def turn_to_interior(self, grid: Grid, quota: float):
        """Selects a sample of cells of the exterior terrain
        and turns them into cells of the interior terrain,
        effectively eroding the boundary in a random manner.
        The boundary is then updated"""
        turned = self.get_sample(self.exterior, quota)

        for cell in turned:
            cell.set_terrain(self.interior)
            self.exterior.remove(cell)
            self.interior.append(cell)
            surroundings = grid.get_close_surroundings(cell.x, cell.y)

            for neighbor in surroundings:
                if neighbor == None:
                    continue
                elif c.is_terrain(neighbor.terrain, self.interior_terrain):
                    self._add(neighbor, self.interior)
                elif c.is_terrain(neighbor, self.exterior_terrain):
                    if self._check_exclusion(grid, neighbor, self.interior_terrain):
                        self.exterior.remove(neighbor)
                        self.discovered.remove(neighbor)

    def turn_to_exterior(self, grid: Grid, quota: float):
        """Selects a sample of cells of the interior terrain
        and turns them into cells of the exterior terrain,
        effectively expanding the boundary in a random manner.
        The boundary is then updated"""
        turned = self.get_sample(self.interior, quota)

        for cell in turned:
            cell.set_terrain(self.exterior)
            self.interior.remove(cell)
            self.exterior.append(cell)
            surroundings = grid.get_close_surroundings(cell.x, cell.y)

            for neighbor in surroundings:
                if neighbor == None:
                    continue
                elif c.is_terrain(neighbor.terrain, self.exterior_terrain):
                    self._add(neighbor, self.exterior)
                elif c.is_terrain(neighbor, self.interior_terrain):
                    if self._check_exclusion(grid, neighbor, self.exterior_terrain):
                        self.interior.remove(neighbor)
                        self.discovered.remove(neighbor)

    def wobble(self, grid: Grid, quota: float, repetitions: int) -> None:
        """Randomizes the boundary by shifting the terrain of random cells

        Args:
            grid: relevant grid
            quota: percentage 0 to 1, determining amount of cells affected
            repetitions: value over 1, determining how many times the cells are shifted
        """
        for rep in repetitions:
            self.turn_to_interior(grid, quota)
            self.turn_to_exterior(grid, quota)

    def set_exterior_terrain(self, terrain: int) -> None:
        for cell in self.exterior:
            cell.set_terrain(terrain)

    def set_interior_terrain(self, terrain: int) -> None:
        for depth in self.interior:
            for cell in depth:
                cell.set_terrain(terrain)

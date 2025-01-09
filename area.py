from grid import Grid
from cell import Cell
import random
import math
import constants as c


class Area():
    def __init__(self, id: int, grid: Grid, start_x: int, start_y: int,
                 type: int = c.CENTER, sea_margin: float = 0.25,
                 growth: int = 20, relative_growth: float = 0.3):
        self.id: int = id
        self.grid: Grid = grid
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.type: int = type
        self.sea_margin: float = sea_margin
        self.growth: int = growth
        self.relative_growth = relative_growth
        self.currency: int = growth
        self.alive: bool = True
        self.area: int = 0
        self.land_area: int = 0
        self.sea_area: int = 0
        self.claimed_cells: list[Cell] = []
        self.queued_cells: list[Cell] = []

        self.west_end: dict[int, int] = {start_y: start_x}
        self.east_end: dict[int, int] = {start_y: start_x}
        self.north_end: dict[int, int] = {start_x: start_y}
        self.south_end: dict[int, int] = {start_x: start_y}

        self.horizontal_distance: dict[int, int] = {}
        self.vertical_distance: dict[int, int] = {}
        self.ascending_distance: dict[int, int] = {}
        self.descending_distance: dict[int, int] = {}

        self.claim_cell(start_x, start_y)

    def _set_boundary(self, minimum: dict[int, int], maximum: dict[int, int],
                      key: int, value: int) -> None:
        """Updates boundaries

        Arguments:
            self.west_end, self.east_end, y, x
        Or:
            self.north_end, self.south_end, x, y"""
        if key in minimum:
            if value < minimum[key]:
                minimum[key] = value
            elif value > maximum[key]:
                maximum[key] = value
        else:
            minimum[key] = value
            maximum[key] = value

    def _add_or_set(self, dictionary: dict[int, int], key: int):
        """Adds value by 1 if key exists, otherwise, sets value to 1"""
        if key in dictionary:
            dictionary[key] += 1
        else:
            dictionary[key] = 1

    def _add_distance(self, x: int, y: int) -> None:
        """Increases appropriate horizontal and vertical distances by 1,
        based on claiming the cell at (x, y)"""

        # Find the x-value when y = 0 and use that as key for diagonal distance
        asc_key = x - y
        des_key = x + y

        self._add_or_set(self.ascending_distance, asc_key)
        self._add_or_set(self.descending_distance, des_key)
        self._add_or_set(self.horizontal_distance, y)
        self._add_or_set(self.vertical_distance, x)

    def claim_cell(self, x: int, y: int) -> None:
        """Claims a cell. Updates boundaries and pays cell cost"""
        cell = self.grid.get(x, y)
        cell.area = self.id
        cell.active = False
        self.area += 100
        self.currency -= 1
        self.queued_cells.append(cell)
        self._set_boundary(self.west_end, self.east_end, y, x)
        self._set_boundary(self.north_end, self.south_end, x, y)
        self._add_distance(x, y)

    def _awaken_cells(self) -> int:
        """Counts amount of cells which the area can expand from"""
        amount = 0
        for cell in self.queued_cells:
            cell.active = True
            amount += 1
        return amount

    def expand(self) -> int:
        """Expands the area in random directions. Returns remaining growth currency.
        Areas will expand no faster than 1 cell per method call in any direction.
        Areas will expand efficiently into vacant spaces.
        If a plate has little space to expand, it will expand with greater focus
        to claim the vacant spaces.
        """
        active_cells = self._awaken_cells()
        limit = math.ceil(active_cells * 0.5)
        self.currency += self.growth

        if active_cells == 0:
            self.alive = False
            return 0

        random.shuffle(self.queued_cells)

        while limit > 0 and self.currency > 0:
            cell = self.queued_cells[0]
            if not cell.active:
                break

            for dir in range(0, 8, 2):
                x, y = c.get_next_coordinates(cell.x, cell.y, dir)

                try:
                    if self.grid.get(x, y).area == -1:
                        self.claim_cell(x, y)
                except KeyError:
                    pass

            cell.active = False
            limit -= 1
            self.claimed_cells.append(cell)
            self.queued_cells.remove(cell)
        return self.currency

    def expand_blindly(self) -> int:
        """Expands the area in random directions. Returns remaining growth currency.
        Areas will expand no faster than 1 cell per method call in any direction.
        Areas expansion should not speed up even if expansion choices are limited"""
        active_cells = self._awaken_cells()
        limit = math.ceil(active_cells * 0.5)
        self.currency += active_cells * self.relative_growth

        if active_cells == 0:
            self.alive = False
            return 0

        random.shuffle(self.queued_cells)

        while limit > 0 and self.currency > 0:
            cell = self.queued_cells[0]
            if not cell.active:
                break

            for dir in range(0, 8, 2):
                x, y = c.get_next_coordinates(
                    cell.x, cell.y, dir)

                try:
                    if self.grid.get(x, y).area == -1:
                        self.claim_cell(x, y)
                except KeyError:
                    pass

            cell.active = False
            self.claimed_cells.append(cell)
            self.queued_cells.remove(cell)
            limit -= 1
        return self.currency

    def _horizontal_land_scan(self, type: int, sea_margin: float, coastal_scan: bool = False) -> None:
        """Scans the area horizontally, finding valid land positions on each vertical"""
        if type in (c.WEST, c.CENTER, c.EAST):
            north_margin = sea_margin
            south_margin = sea_margin
        elif type in (c.NORTHWEST, c.NORTH, c.NORTHEAST):
            north_margin = 0
            south_margin = sea_margin * 2
        elif type in (c.SOUTHWEST, c.SOUTH, c.SOUTHEAST):
            north_margin = sea_margin * 2
            south_margin = 0

        for x in self.north_end.keys():
            length = self.vertical_distance[x]
            start = self.north_end[x]
            end = self.south_end[x]

            first_skip = int(length * north_margin)
            second_skip = int(length * south_margin)
            include = length - first_skip - second_skip

            for y in range(start, end + 1):
                if self.grid.get(x, y).area == self.id:
                    if first_skip > 0:
                        first_skip -= 1
                    elif include > 0:
                        if coastal_scan:
                            self.grid.get(x, y).horizontal_coastal_check = True
                        else:
                            self.grid.get(x, y).horizontal_land_check = True
                        include -= 1
                    else:
                        break

    def _vertical_land_scan(self, type: int, sea_margin: float, coastal_scan: bool = False) -> None:
        """Scans the area vertically, finding valid land positions on each horizontal"""
        if type in (c.NORTH, c.CENTER, c.SOUTH):
            west_margin = sea_margin
            east_margin = sea_margin
        elif type in (c.NORTHWEST, c.WEST, c.SOUTHWEST):
            west_margin = 0
            east_margin = sea_margin * 2
        elif type in (c.NORTHEAST, c.EAST, c.SOUTHEAST):
            west_margin = sea_margin * 2
            east_margin = 0

        for y in self.west_end.keys():
            length = self.horizontal_distance[y]
            start = self.west_end[y]
            end = self.east_end[y]

            first_skip = int(length * west_margin)
            second_skip = int(length * east_margin)
            include = length - first_skip - second_skip

            for x in range(start, end + 1):
                if self.grid.get(x, y).area == self.id:
                    if first_skip > 0:
                        first_skip -= 1
                    elif include > 0:
                        if coastal_scan:
                            self.grid.get(x, y).vertical_coastal_check = True
                        else:
                            self.grid.get(x, y).vertical_land_check = True
                        include -= 1
                    else:
                        break

    def _ascending_land_scan(self, type: int, sea_margin: float, coastal_scan: bool = False) -> None:
        """Scans the area diagonally, finding valid land position in northwest to southeast diagonal"""
        if type in (c.NORTH, c.WEST, c.NORTHWEST):
            northwest_margin = 0
            southeast_margin = sea_margin * 2
        elif type in (c.CENTER, c.NORTHEAST, c.SOUTHWEST):
            northwest_margin = sea_margin
            southeast_margin = sea_margin
        elif type in (c.EAST, c.SOUTHEAST, c.SOUTH):
            northwest_margin = sea_margin * 2
            southeast_margin = 0

        for start_x, length in self.ascending_distance.items():
            first_skip = int(length * northwest_margin)
            second_skip = int(length * southeast_margin)
            include = length - first_skip - second_skip

            if start_x < 0:
                y = - start_x
                start_x = 0
            else:
                y = 0

            for x in range(start_x, self.grid.length):
                if y == self.grid.height:
                    break
                elif self.grid.get(x, y).area == self.id:
                    if first_skip > 0:
                        first_skip -= 1
                    elif include > 0:
                        if coastal_scan:
                            self.grid.get(x, y).ascending_coastal_check = True
                        else:
                            self.grid.get(x, y).ascending_land_check = True
                        include -= 1
                    else:
                        break
                y += 1

    def _descending_land_scan(self, type: int, sea_margin: float, coastal_scan: bool = False) -> None:
        """Scans the area diagonally, finding valid land positions in northeast to southwest diagonal"""
        if type in (c.NORTH, c.NORTHEAST, c.EAST):
            northeast_margin = 0
            southwest_margin = sea_margin * 2
        elif type in (c.CENTER, c.SOUTHEAST, c.NORTHWEST):
            northeast_margin = sea_margin
            southwest_margin = sea_margin
        elif type in (c.SOUTH, c.SOUTHWEST, c.WEST):
            northeast_margin = sea_margin * 2
            southwest_margin = 0

        for start_x, length in self.descending_distance.items():
            first_skip = int(length * northeast_margin)
            second_skip = int(length * southwest_margin)
            include = length - first_skip - second_skip

            if start_x >= self.grid.length:
                y = start_x - self.grid.length + 1
                start_x = self.grid.length - 1
            else:
                y = 0

            for x in range(start_x, -1, -1):
                if y == self.grid.height:
                    break
                if self.grid.get(x, y).area == self.id:
                    if first_skip > 0:
                        first_skip -= 1
                    elif include > 0:
                        if coastal_scan:
                            self.grid.get(x, y).descending_coastal_check = True
                        else:
                            self.grid.get(x, y).descending_land_check = True
                        include -= 1
                    else:
                        break
                y += 1

    def create_land(self) -> None:
        """Creates land or sea on this area, depending on area type"""
        self.land_area = 0
        self.sea_area = 0

        if self.type == c.LAND:
            for cell in self.claimed_cells:
                cell.set_terrain(c.LAND)
                self.land_area += 100
        elif self.type == c.WATER:
            for cell in self.claimed_cells:
                cell.set_terrain(c.WATER)
                self.sea_area += 100
        else:
            if self.type in (
                    c.CENTER, c.NORTHEAST, c.SOUTHEAST,
                    c.SOUTHWEST, c.NORTHWEST):
                self._horizontal_land_scan(self.type, self.sea_margin)
                self._vertical_land_scan(self.type, self.sea_margin)
            else:
                self._ascending_land_scan(self.type, self.sea_margin)
                self._descending_land_scan(self.type, self.sea_margin)

            for cell in self.claimed_cells:
                if cell.passes_land_scan():
                    cell.set_terrain(c.LAND)
                    self.land_area += 100
                else:
                    cell.set_terrain(c.WATER)
                    self.sea_area += 100

    def convert_to_coastal(self, cell: Cell, water_rate: float) -> bool:
        if c.is_terrain(cell.terrain, c.WATER) or random.random() > water_rate:
            return False

        surroundings = c.get_surroundings(cell.x, cell.y)
        outskirts = self.grid.get_all(surroundings)

        for neighbor in outskirts:
            if neighbor != None and c.is_terrain(neighbor.terrain, c.WATER):
                cell.set_terrain(c.WATER)
                return True
        return False

    def create_coastal_landscape(self, type: int,
                                 coastal_margin: float, water_rate: float) -> None:
        if type in (c.CENTER, c.NORTHEAST, c.SOUTHEAST,
                    c.SOUTHWEST, c.NORTHWEST):
            self._horizontal_land_scan(type, coastal_margin, True)
            self._vertical_land_scan(type, coastal_margin, True)
        elif type in (c.NORTH, c.EAST, c.SOUTH, c.WEST):
            self._ascending_land_scan(type, coastal_margin, True)
            self._descending_land_scan(type, coastal_margin, True)

        coastal_cells = []

        for cell in self.claimed_cells:
            if c.is_terrain(cell.terrain, c.WATER) and cell.passes_coastal_scan():
                cell.set_terrain(c.LAND)
                coastal_cells.append(cell)

        amount = int(len(coastal_cells) * water_rate)
        random.shuffle(coastal_cells)

        while amount > 0:
            for cell in coastal_cells:
                if self.convert_to_coastal(cell, water_rate):
                    amount -= 1

    def sink(self) -> None:
        """Clears all land from this plate. Clears land and sea area calculations"""
        self.land_area = 0
        self.sea_area = 0

        for cell in self.claimed_cells:
            cell.set_terrain(c.WATER)
            cell.horizontal_land_check = False
            cell.vertical_land_check = False
            cell.ascending_land_check = False
            cell.descending_land_check = False

    def find_border_of_terrain(self, external_terrain: int) -> list[Cell]:
        """Returns a list of cells at the area border,
        so that the terrain beyond the area border equals the given terrain
        (for at least one cell immediately beyond the border)"""
        border = []

        for cell in self.claimed_cells:
            for dir in range(8):
                x, y = c.get_next_coordinates(cell.x, cell.y, dir)

                try:
                    neighbor: Cell = self.grid.get(x, y)
                except KeyError:
                    continue

                if neighbor.area != self.id \
                    and c.is_terrain(neighbor.terrain, external_terrain) \
                        and neighbor not in border:
                    cell.set_depth(1)
                    border.append(cell)
        return border

    def find_border_distance(self, external_terrain: int, max_distance: int = 100) -> list[list[Cell]]:
        """Returns a two-dimensional list of cells,
        where list at index i respresents cells with distance i+1
        to an out-of-area cell with terrain equal to the given external terrain.
        Sets the depth value of the cells to equal this distance.
        The algorithm terminates at max distance or when all cells have been found.
        """
        for cell in self.claimed_cells:
            cell.set_depth()

        circles = []
        current_circle = self.find_border_of_terrain(external_terrain)
        circles.append(current_circle)

        if max_distance == 1:
            return circles

        for distance in range(2, max_distance + 1):
            previous_circle = current_circle
            current_circle = []

            for cell in previous_circle:
                for dir in range(8):
                    x, y = c.get_next_coordinates(cell.x, cell.y, dir)
                    try:
                        neighbor: Cell = self.grid.get(x, y)
                    except KeyError:
                        continue

                    if neighbor.area == self.id and neighbor.has_depth() == False:
                        neighbor.set_depth(distance)
                        current_circle.append(neighbor)

            if len(current_circle) > 0:
                circles.append(current_circle)
            else:
                return circles
        return circles

    def find_border_offset(self, internal_terrain: int, external_terrain: int,
                           min_distance: int, max_distance: int) -> list[Cell]:
        """Returns a list of cells, so that the distance to a
        out-of-area cell of given external terrain is between
        min distance and max distance, and the resulting cells terrain
        equals the internal terrain.
        (only out-of-plate cells next to the plate border are considered)"""
        result = []
        circles = self.find_border_distance(external_terrain, max_distance)

        distance = 1

        for circle in circles:
            if distance >= min_distance:
                for cell in circle:
                    if c.is_terrain(cell.terrain, internal_terrain):
                        result.append(cell)
            distance += 1

        return result

    def get_info(self) -> str:
        """Returns plate information"""
        west = min(self.west_end.values()) * 10
        east = max(self.east_end.values()) * 10
        north = min(self.north_end.values()) * 10
        south = max(self.south_end.values()) * 10

        text = f"""Plate {self.id}
Type: {c.get_type(self.type)}
Area: {self.area:,} km2
Land area: {self.land_area:,} km2
Sea area {self.sea_area:,} km2
Sea percentage: {self.sea_area / self.area:.0%}
x: {west} to {east}
y: {south} to {north}
Sea margin: {self.sea_margin:.0%}"""
        return text

from typing import Self


class Cell():
    """Represents a space in a rectangular grid"""

    def __init__(self, x: int, y: int, terrain: int):
        """Creates a cell with the given coordinates and terrain"""
        self.x: int = x
        self.y: int = y
        self.terrain: int = terrain
        self.elevation: int = None
        self.depth: int = None
        self.mountain_depth: int = None
        self.area: int = -1
        self.active: bool = True

        self.horizontal_land_check: bool = False
        self.vertical_land_check: bool = False
        self.ascending_land_check: bool = False
        self.descending_land_check: bool = False

        self.horizontal_coastal_check: bool = False
        self.vertical_coastal_check: bool = False
        self.ascending_coastal_check: bool = False
        self.descending_coastal_check: bool = False

        self.north_boundary: bool = False
        self.east_boundary: bool = False
        self.south_boundary: bool = False
        self.west_boundary: bool = False

    def set_terrain(self, terrain: int) -> None:
        """Sets the terrain"""
        self.terrain = terrain

    def set_depth(self, depth: int = None) -> None:
        """Sets the depth. This represents the minimum distance
        to some other type of terrain, like the distance to a coast or shore.
        Exact usage may vary"""
        self.depth = depth

    def has_depth(self) -> bool:
        """Returns true if depth has not been calculated"""
        return self.depth != None

    def calculate_mountain_depth(self, mountain_start: int, mountain_end: int) -> int:
        """Sets the mountain depth. Assumes the cell has a depth
        which describes its distance to the coast.
        Assumes mountains are placed based on distance to coast.
        Mountain depth describes the cells distance to non-mountainous terrain"""
        forward_depth = 1 + self.depth - mountain_start
        backward_depth = 1 + mountain_end - self.depth
        self.mountain_depth = min(forward_depth, backward_depth)

    def has_boundary(self) -> bool:
        """Returns true if this cell is at the boundary of an Area.
        Before using this, world.find_boundaries should be called"""
        return (self.north_boundary or self.east_boundary
                or self.south_boundary or self.west_boundary)

    def passes_land_scan(self) -> bool:
        """Returns true if land can be generated on this cell,
        based on the settings of its Area"""
        return (self.horizontal_land_check and self.vertical_land_check) \
            or (self.ascending_land_check and self.descending_land_check)

    def passes_coastal_scan(self) -> bool:
        """Returns true if this cell is a suitable location for either land or water,
        based on the settings of its Area"""
        return (self.horizontal_coastal_check and self.vertical_coastal_check) \
            or (self.ascending_coastal_check and self.descending_coastal_check)

    def inherit(self, cell: Self) -> None:
        """Sets cell variables based on a another cell"""
        self.set_terrain(cell.terrain)
        self.mountain_depth = cell.mountain_depth
        self.area = cell.area

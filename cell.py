class Cell():
    def __init__(self, x: int, y: int, terrain: int):
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
        self.terrain = terrain

    def set_depth(self, depth: int = None) -> None:
        self.depth = depth

    def has_depth(self) -> bool:
        return self.depth != None

    def set_mountain_depth(self, mountain_start: int, mountain_end: int) -> int:
        forward_depth = 1 + self.depth - mountain_start
        backward_depth = 1 + mountain_end - self.depth
        self.mountain_depth = min(forward_depth, backward_depth)

    def has_boundary(self) -> bool:
        return (self.north_boundary or self.east_boundary
                or self.south_boundary or self.west_boundary)

    def passes_land_scan(self) -> bool:
        return (self.horizontal_land_check and self.vertical_land_check) \
            or (self.ascending_land_check and self.descending_land_check)

    def passes_coastal_scan(self) -> bool:
        return (self.horizontal_coastal_check and self.vertical_coastal_check) \
            or (self.ascending_coastal_check and self.descending_coastal_check)

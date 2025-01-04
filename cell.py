class Cell():
    def __init__(self, x: int, y: int, terrain: int):
        self.x: int = x
        self.y: int = y
        self.terrain: int = terrain
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

        self.border_distance: int = -1

    def set_terrain(self, terrain: int) -> None:
        self.terrain = terrain

    def has_boundary(self) -> bool:
        return (self.north_boundary or self.east_boundary
                or self.south_boundary or self.west_boundary)

    def passes_land_scan(self) -> bool:
        return (self.horizontal_land_check and self.vertical_land_check) \
            or (self.ascending_land_check and self.descending_land_check)

    def passes_coastal_scan(self) -> bool:
        return (self.horizontal_coastal_check and self.vertical_coastal_check) \
            or (self.ascending_coastal_check and self.descending_coastal_check)

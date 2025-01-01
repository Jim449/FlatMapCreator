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

        self.border_distance: int = -1

    def set_terrain(self, terrain: int) -> None:
        self.terrain = terrain

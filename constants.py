from PyQt5.QtGui import QColor

NORTH = 0
NORTHEAST = 1
EAST = 2
SOUTHEAST = 3
SOUTH = 4
SOUTHWEST = 5
WEST = 6
NORTHWEST = 7
CENTER = 8
LAND = 9
WATER = 10
MOUNTAIN = 11
SHALLOWS = 12
SHORE = 13
DEPTHS = 14
CLIFFS = 15
FLATLAND = 16

BORDER_COLOR = QColor(120, 90, 90)
GRID_COLOR = QColor(150, 150, 180)
LINE_COLOR = QColor(90, 90, 120)
BLACK = QColor(0, 0, 0)
EMPTY_COLOR = QColor(0, 0, 0, 0)

COLORS = {WATER: QColor(22, 134, 174), LAND: QColor(189, 171, 123), MOUNTAIN: QColor(118, 108, 93),
          SHALLOWS: QColor(110, 154, 174), SHORE: QColor(162, 139, 100), DEPTHS: QColor(11, 117, 156),
          CLIFFS: QColor(144, 128, 100)}

REGION = "Region"
SQUARE_MILE = "Square mile"
SQUARE_KILOMETER = "Square kilometer"


def get_color(terrain: int) -> QColor:
    return COLORS[terrain]

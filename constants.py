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

AREA = "Area"
SQUARE_REGION = "Square region"
SQUARE_MILE = "Square mile"
SQUARE_KILOMETER = "Square kilometer"


def get_color(terrain: int) -> QColor:
    """Retreives the color of the given terrain"""
    return COLORS[terrain]


def get_next_coordinates(x: int, y: int, dir: int) -> tuple[int]:
    """Returns new coordinates (x,y) after travelling once in a direction."""
    nx = x
    ny = y

    if dir in (NORTH, NORTHEAST, NORTHWEST):
        ny -= 1
    elif dir in (SOUTH, SOUTHEAST, SOUTHWEST):
        ny += 1

    if dir in (EAST, NORTHEAST, SOUTHEAST):
        nx += 1
    elif dir in (WEST, NORTHWEST, SOUTHWEST):
        nx -= 1

    return (nx, ny)


def flip_direction(dir: int) -> int:
    """Returns the opposite direction"""
    dir += 4
    if dir > 8:
        dir -= 8
    return dir


def angle_direction(dir: int, steps_of_eight: int) -> int:
    """Rotates a direction in clockwise steps of an eight circle. Returns the new direction"""
    dir += steps_of_eight
    if dir > 8:
        dir -= 8
    return dir


def get_surroundings(x: int, y: int) -> list[tuple[int]]:
    """Returns coordinates representing the surroundings of point (x,y) in all eight directions."""
    result = []

    for dir in range(8):
        result.append(get_next_coordinates(x, y, dir))
    return result


def get_close_surroundings(x: int, y: int) -> list[tuple[int]]:
    """Returns coordinates representing the surroundings of point (x,y) in four directions.
    Returns a list of coordinates, corresponding to directions north, east, south, west,
    in that order"""
    result = []

    for dir in range(0, 8, 2):
        result.append(get_next_coordinates(x, y, dir))

    return result


def get_square(x: int, y: int, dir: int) -> list[tuple[int]]:
    """Returns a list of coordinates in order NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST.
    Provide one of these coordinates and the relative position of those coordinates."""
    result = [None, None, None, None]

    if dir == NORTHEAST:
        result[0] = (x, y)
        result[1] = get_next_coordinates(x, y, SOUTH)
        result[2] = get_next_coordinates(x, y, SOUTHWEST)
        result[3] = get_next_coordinates(x, y, WEST)
    elif dir == SOUTHEAST:
        result[0] = get_next_coordinates(x, y, NORTH)
        result[1] = (x, y)
        result[2] = get_next_coordinates(x, y, WEST)
        result[3] = get_next_coordinates(x, y, NORTHWEST)
    elif dir == SOUTHWEST:
        result[0] = get_next_coordinates(x, y, NORTHEAST)
        result[1] = get_next_coordinates(x, y, EAST)
        result[2] = (x, y)
        result[3] = get_next_coordinates(x, y, NORTH)
    elif dir == NORTHWEST:
        result[0] = get_next_coordinates(x, y, EAST)
        result[1] = get_next_coordinates(x, y, SOUTHEAST)
        result[2] = get_next_coordinates(x, y, SOUTH)
        result[3] = (x, y)
    return result

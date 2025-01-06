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
# No, randomly alternating between this and LAND just looks messy
# But this lighter hue is a bit superior than the original I think
LAND_2 = 17

BORDER_COLOR = QColor(120, 90, 90)
GRID_COLOR = QColor(150, 150, 180)
LINE_COLOR = QColor(90, 90, 120)
BLACK = QColor(0, 0, 0)
EMPTY_COLOR = QColor(0, 0, 0, 0)

COLORS = {WATER: QColor(22, 134, 174), LAND: QColor(196, 179, 136), MOUNTAIN: QColor(155, 135, 95),
          SHALLOWS: QColor(110, 154, 174), SHORE: QColor(162, 139, 100), DEPTHS: QColor(11, 117, 156),
          CLIFFS: QColor(144, 128, 100), LAND_2: QColor(189, 171, 123)}

MOUNTAIN_COLORS = [QColor(155, 135, 95), QColor(160, 141, 103), QColor(165, 147, 111),
                   QColor(170, 153, 119), QColor(
                       175, 159, 127), QColor(180, 165, 135),
                   QColor(185, 171, 143), QColor(
                       190, 177, 151), QColor(195, 183, 159),
                   QColor(200, 189, 167), QColor(
                       205, 195, 175), QColor(210, 201, 183),
                   QColor(215, 207, 191), QColor(
                       220, 213, 199), QColor(225, 219, 207),
                   QColor(230, 225, 215), QColor(
                       235, 231, 223), QColor(240, 237, 231),
                   QColor(245, 243, 239), QColor(250, 249, 247), QColor(255, 255, 255)]
# 255 - 100 = 155; 255 - 20*5 = 155
# 255 - 120 = 135; 255 - 20*6 = 135
# 255 - 160 = 95; 255 - 20*8 = 95
# Include 16 colors, where each signifies a difference of 500m
# The maximum height will be 8000m

AREA = "Area"
SQUARE_REGION = "Square region"
SQUARE_MILE = "Square mile"
SQUARE_KILOMETER = "Square kilometer"


def get_color(terrain: int, elevation: int = None) -> QColor:
    """Retreives the color of the given terrain"""
    if elevation == None:
        return COLORS[terrain]
    elif terrain == MOUNTAIN:
        return MOUNTAIN_COLORS[(elevation - 1)]


def get_type(type: int) -> str:
    """Translates an integer constant into a string type"""
    type_names = {0: "north", 1: "northeast", 2: "east", 3: "southeast",
                  4: "south", 5: "southwest", 6: "west", 7: "northwest",
                  8: "center", 9: "land", 10: "water", 11: "mountain"}
    return type_names[type]


def get_type_value(type: str) -> int:
    """Translates a string type into an integer constant"""
    type_values = {"north": 0, "northeast": 1, "east": 2, "southeast": 3,
                   "south": 4, "southwest": 5, "west": 6, "northwest": 7,
                   "center": 8, "land": 9, "water": 10, "mountain": 11}
    return type_values[type.lower()]


def is_terrain(type: int, category: int):
    """Returns true if type belongs to the given terrain category"""
    if type == category:
        return True
    elif category == LAND:
        return type in (MOUNTAIN, CLIFFS, SHORE)
    elif category == WATER:
        return type in (SHALLOWS, DEPTHS)
    elif category == FLATLAND:
        return type in (LAND, SHORE)
    else:
        return False


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

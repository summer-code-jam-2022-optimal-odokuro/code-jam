import random

MAP_HORIZONTAL = 5
MAP_VERTICAL = 5

ROOM_HORIZONTAL = 80
ROOM_VERTICAL = 80
ROCK_CHAR = '#'
NONE_CHAR = ' '

DOOR_FRAMES = [4]


def get_interior_sides(room_horizontal: int, room_vertical: int, horizontal: int = MAP_HORIZONTAL,
                       vertical: int = MAP_VERTICAL) -> dict[str:bool]:
    """
    Get the interior corners of the room in terms of the map
    :param room_horizontal: The horizontal position of the room in the map
    :param room_vertical: The vertical position of the room in the map
    :param horizontal: The number of rows of rooms on the map
    :param vertical: The number of columns of rooms on the map
    :return: An ordered list of bool determining whether the sides (north, east, west, south) are interior
    """
    interior_sides = {"north": True, "east": True, "west": True, "south": True}

    if room_horizontal == 0:
        interior_sides["north"] = False
    if room_horizontal == horizontal - 1:
        interior_sides["south"] = False
    if room_vertical == 0:
        interior_sides["west"] = False
    if room_vertical == vertical - 1:
        interior_sides["east"] = False

    return interior_sides


def generate_room(door_sides: dict[str:bool], rows: int = ROOM_HORIZONTAL,
                  columns: int = ROOM_VERTICAL) -> list[list[str]]:
    """
    Generate a room with the given number of rows and columns.
    :param columns: The amount of columns of the room
    :param rows: The amount of rows of the room
    :param door_sides: A dictionary of the sides of the room that are to have a door generated on them
    """
    room = [[NONE_CHAR for _ in range(columns)] for _ in range(rows)]

    # Generate the room's walls

    for row in range(rows):
        for column in range(columns):
            if row == 0 or row == rows - 1 or column == 0 or column == columns - 1:
                room[row][column] = ROCK_CHAR

    # Generate the room's doors
    # Todo: remove magic numbers

    for direction, door in door_sides.items():
        if door:
            match direction: # noqa: E999
                case 'north':
                    room[38][0] = NONE_CHAR
                    room[39][0] = NONE_CHAR
                    room[40][0] = NONE_CHAR
                    room[41][0] = NONE_CHAR
                case 'east':
                    room[79][39] = NONE_CHAR
                    room[79][40] = NONE_CHAR
                    room[79][41] = NONE_CHAR
                    room[79][42] = NONE_CHAR
                case 'west':
                    room[0][38] = NONE_CHAR
                    room[0][39] = NONE_CHAR
                    room[0][40] = NONE_CHAR
                    room[0][41] = NONE_CHAR
                case 'south':
                    room[39][79] = NONE_CHAR
                    room[40][79] = NONE_CHAR
                    room[41][79] = NONE_CHAR
                    room[42][79] = NONE_CHAR

    # Generate the room's interior
    # Todo: clean up

    g = random.randint(25, 30)
    while g > 0:
        rocksize = random.randint(5, 7)
        rocklocx = random.randint(0, 70)
        rocklocy = random.randint(0, 70)
        while rocklocy < 3 and 41 > rocklocx > 32 or rocklocy > 70 and 41 > rocklocx > 32 \
                or rocklocx > 65 and 41 > rocklocy > 32 or rocklocx > 65 and 41 > rocklocy > 32:
            rocklocx = random.randint(0, 70)
            rocklocy = random.randint(0, 70)
        for v in range(0, rocksize):
            for t in range(0, random.randint((rocksize - 2), (rocksize + 2))):
                (room[rocklocy + v])[rocklocx + t] = '#'
        g -= 1

    return room


def generate_map(map_width: int = MAP_HORIZONTAL, map_height: int = MAP_VERTICAL) -> list[list[list[list[str]]]]:
    new_map = []
    for row in range(map_height):
        new_map.append([])
        for column in range(map_width):
            new_map[row].append(generate_room(door_sides=get_interior_sides(column, row, map_width, map_height)))

    return new_map


for a in generate_map():
    for b in a:
        for c in b:
            print(c)
        print()

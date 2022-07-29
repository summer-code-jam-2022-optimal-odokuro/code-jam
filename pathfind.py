import random

MAP_HORIZONTAL = 5
MAP_VERTICAL = 5

ROOM_HORIZONTAL = 80
ROOM_VERTICAL = 80
DOOR_CHAR = 3
WALL_CHAR = 2
ROCK_CHAR = 1
NONE_CHAR = 0

DOOR_FRAMES = [38, 39, 40, 41]


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


def generate_room_sides(room: list[list[int]], rows: int = ROOM_HORIZONTAL,
                        columns: int = ROOM_VERTICAL) -> list[list[int]]:
    """
    Generate sides of a room
    :param room: The room to generate sides in
    :param columns: The amount of columns of the room
    :param rows: The amount of rows of the room
    """

    # Generate the room's walls

    for row in range(rows):
        for column in range(columns):
            if row == 0 or row == rows - 1 or column == 0 or column == columns - 1:
                room[row][column] = WALL_CHAR

    return room


def generate_room_doors(room: list[list[int]], door_sides: dict[str:bool], frames=None, rows: int = ROOM_HORIZONTAL,
                        columns: int = ROOM_VERTICAL) -> list[list[int]]:
    """
    Generate doors in a room
    :param rows: The amount of rows of the room
    :param columns: The amount of columns of the room
    :param room: The room to generate doors in
    :param door_sides: A dictionary of the sides of the room that are to have a door generated on them
    :param frames: A list of the frames tiles indices to use for the doors
    :return: The room with doors in it
    """

    if frames is None:
        frames = DOOR_FRAMES

    for direction, door in door_sides.items():
        if door:
            match direction:  # noqa: E999
                case 'north':
                    for frame in frames:
                        room[frame][0] = DOOR_CHAR

                case 'east':
                    for frame in frames:
                        room[rows - 1][frame] = DOOR_CHAR

                case 'west':
                    for frame in frames:
                        room[0][frame] = DOOR_CHAR

                case 'south':
                    for frame in frames:
                        room[frame][columns - 1] = DOOR_CHAR

                case _:
                    continue

    return room


def generate_room_rocks(room: list[list[int]]) -> list[list[int]]:
    """
    Generate rocks in the given room. Note that this function may override other structures in the room
    :param room: The room to generate rocks in
    :return: Room with rocks in it
    """
    # Todo: As much as possible cut down on the amount of magic numbers and instead use constants, parameters, etc.

    for _ in range(random.randint(25, 30)):
        rocksize = random.randint(5, 7)
        rocklocx = random.randint(0, 70)
        rocklocy = random.randint(0, 70)

        while rocklocy < 3 and 41 > rocklocx > 32 or rocklocy > 70 and 41 > rocklocx > 32 \
                or rocklocx > 65 and 41 > rocklocy > 32 or rocklocx > 65 and 41 > rocklocy > 32:
            rocklocx = random.randint(0, 70)
            rocklocy = random.randint(0, 70)

        for v in range(0, rocksize):
            for t in range(0, random.randint((rocksize - 2), (rocksize + 2))):
                (room[rocklocy + v])[rocklocx + t] = ROCK_CHAR

    return room


def generate_map(map_width: int = MAP_HORIZONTAL, map_height: int = MAP_VERTICAL,
                 room_width: int = ROOM_HORIZONTAL, room_height: int = ROOM_VERTICAL, generate_rocks: bool = True) \
        -> list[list[list[list[int]]]]:
    """
    Generate a rectangular map with the given number of rooms
    :param room_width: The width of the rooms
    :param room_height: The height of the rooms
    :param map_width: Width of the map
    :param map_height: Height of the map
    :param generate_rocks: Boolean determining whether rocks should be generated
    :return: 2d list of rooms, each room is a 2d list of characters
    """
    new_map = [[[[NONE_CHAR for _ in range(room_height)] for _ in range(room_width)] for _ in range(map_height)] for _
               in range(map_width)]
    for row in range(map_height):
        for column in range(map_width):
            new_map[row][column] = generate_room_sides(new_map[row][column], room_width, room_height)
            new_map[row][column] = generate_room_doors(new_map[row][column],
                                                       get_interior_sides(column, row, map_width, map_height),
                                                       rows=room_height, columns=room_width)

            if generate_rocks:
                new_map[row][column] = generate_room_rocks(new_map[row][column])

    return new_map


class Node:
    """Node used for pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.pos = position

        self.h = 0
        self.f = 0
        self.g = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def __str__(self):
        return str(self.pos)


def pathfind(maze: list, start: tuple[int, int], end: tuple[int, int]) -> list[list[int, int]]:
    """
    Find a path to a location.
    :param maze: The maze
    :param start: Starting coordinate (x, y)
    :param end:
    :return: List of points to move to
    """

    # Setup
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []
    open_list.append(start_node)

    # Loop until success
    while len(open_list) > 0:

        # Get the current node
        cur_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < cur_node.f:
                cur_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(cur_node)

        # If we succeeded
        if cur_node == end_node:
            path = []
            current = cur_node
            while current is not None:
                path.append(current.pos)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_pos in ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                        (1, 1)):  # Adjacent squares

            # Get node position
            node_pos = (cur_node.pos[0] + new_pos[0], cur_node.pos[1] + new_pos[1])

            # Make sure within range
            if node_pos[0] > (len(maze) - 1) or node_pos[0] < 0 or node_pos[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_pos[1] < 0:
                continue

            # Make sure we can walk on terrain
            if maze[node_pos[0]][node_pos[1]] != 0:
                continue

            new_node = Node(cur_node, node_pos)
            children.append(new_node)

        # Loop through em all
        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = cur_node.g + 1
            child.h = ((child.pos[0] - end_node.pos[0]) ** 2) + (
                    (child.pos[1] - end_node.pos[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    maze = generate_map()[0]

    start = (1, 1)
    end = (23, 10)

    for b in maze[0]:
        print(b)
    print()

    path = pathfind(maze[0], start, end)
    print(path)


if __name__ == '__main__':
    main()

from mapgen import generate_map
import mapgen as mg


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


async def pathfind(maze: list, start: tuple[int, int], end: tuple[int, int]) -> list[list[int, int]]:
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
            if maze[node_pos[0]][node_pos[1]] != mg.NONE_CHAR:
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

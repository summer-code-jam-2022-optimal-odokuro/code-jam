from code_jam_site.bug_game.mapgen import generate_map
import random

def initialize_game(player_ids):
    MAP_HORIZONTAL = 5
    MAP_VERTICAL = 5

    ROOM_HORIZONTAL = 80
    ROOM_VERTICAL = 80
    DOOR_CHAR = 3
    WALL_CHAR = 2
    ROCK_CHAR = 1
    NONE_CHAR = 0

    DOOR_FRAMES = [38, 39, 40, 41]
    map=generate_map()

    for player in player_ids:
        random


def player_input_handler(id,input):
    


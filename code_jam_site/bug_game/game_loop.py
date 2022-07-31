import json
from dataclasses import dataclass

from . import mapgen as mg
from . import pathfind as pf
import random
from channels.layers import get_channel_layer

from .mapgen import generate_map
from .models import MapModel

from .pathfind import pathfind


@dataclass(init=True)
class Player:
    map_x: int
    map_y: int
    room_x: int
    room_y: int


@dataclass(init=True)
class Entity:
    map_x: int
    map_y: int
    room_x: int
    room_y: int
    texture_type: str


class GameWrapper:
    game_id: int
    game_map: list[list[list[list[int]]]]
    player_locations: dict[str, Player]
    enemy_locations: dict[str, Entity]


def initialize_game(player_ids, game_id):
    game_exists = False

    if MapModel.objects.filter(game_id=game_id, game_exists=True).exists():
        game_map = json.loads(MapModel.objects.filter(game_id=game_id)[0].map)
        game_exists = True

        # If the game already exists

    elif MapModel.objects.filter(game_id=game_id).exists:
        map_object = MapModel.objects.filter(game_id=game_id)[0]
        map_object.exists = True
        game_map = json.loads(map_object.map)

        # If the game does not yet exist but has existed before

    else:
        game_map = generate_map(game_id)
        MapModel.objects.create(map=json.dumps(game_map), game_id=game_id, game_exists=True)

        # The game does not yet exist

    if not game_exists:

        enemy_count = 200
        enemylocs = {}

        for enemy_id in range(1, enemy_count):
            spawnlocx = random.randint(16, 1248)
            spanwlocy = random.randint(16, 1248)
            roomx = random.randint(0, 5)
            roomy = random.randint(0, 5)
            while ((((game_map[roomx])[roomy])[spawnlocx // 16])[spanwlocy // 16]) != 0:
                spawnlocx = random.randint(16, 1248)
                spanwlocy = random.randint(16, 1248)
                roomx = random.randint(0, 5)
                roomy = random.randint(0, 5)
            location = [roomx, roomy, spawnlocx, spanwlocy]
            enemylocs[str(enemy_id)] = location

        return game_map


def player_input_handler(player_id, player_input, playerlocs, enemylocs, map):
    playerloc = playerlocs[player_id]

    ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2] // 16)])[((playerloc[3]) // 16)])

    if player_input == 'up':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2] // 16)])[((playerloc[3]) // 16) - 1]) != 0:
            return playerlocs
        elif playerloc[3] < 16:
            newplayerloc = ((((map[playerloc[0]])[(playerloc[1] - 1)])[(playerloc[2])])[(playerloc[3] + 1248)])
        else:
            newplayerloc = ((((map[playerloc[0]])[(playerloc[1] - 1)])[(playerloc[2])])[(playerloc[3] - 16)])
    elif player_input == 'down':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2] // 16)])[((playerloc[3]) // 16) + 1]) != 0:
            return playerlocs
        elif playerloc[3] > 1248:
            newplayerloc = ((((map[playerloc[0]])[(playerloc[1] + 1)])[(playerloc[2])])[(playerloc[3] - 1248)])
        else:
            newplayerloc = ((((map[playerloc[0]])[(playerloc[1] + 1)])[(playerloc[2])])[(playerloc[3] + 16)])
    elif player_input == 'left':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2] // 16) - 1])[((playerloc[3]) // 16)]) != 0:
            return playerlocs
        elif playerloc[2] < 16:
            newplayerloc = ((((map[(playerloc[0] - 1)])[(playerloc[1])])[(playerloc[2] + 1248)])[(playerloc[3])])
        else:
            newplayerloc = ((((map[(playerloc[0] - 1)])[(playerloc[1])])[(playerloc[2] - 16)])[(playerloc[3])])
    elif player_input == 'right':
        if ((((map[playerloc[0]])[playerloc[1]])[(playerloc[2] // 16) + 1])[((playerloc[3]) // 16) - 1]) != 0:
            return playerlocs
        elif playerloc[2] > 1248:
            newplayerloc = ((((map[(playerloc[0] + 1)])[(playerloc[1] - 1)])[(playerloc[2] - 1248)])[(playerloc[3])])
        else:
            newplayerloc = ((((map[(playerloc[0] + 1)])[(playerloc[1] - 1)])[(playerloc[2] - 1248)])[(playerloc[3])])
    elif player_input == 'attack':
        for key in enemylocs.keys():
            if (enemylocs[key])[0] == playerloc[0] and (enemylocs[key])[1] == playerloc[1] and (enemylocs[key])[
                2] in range((playerloc[2] - 20, (playerloc[2] + 20))) and (enemylocs[key])[2] in range(
                (playerloc[3] - 20, (playerloc[3] + 20))):
                enemylocs = enemylocs.pop(key)


def enemy_actions(playerlocs, enemylocs, enemy, map):
    for player in playerlocs.keys():
        if (playerlocs[player])[0] == (enemylocs[enemy])[0] and (playerlocs[player])[1] == (enemylocs[enemy])[1]:
            room = (map[(enemylocs[enemy])[0]])[(enemylocs[enemy])[1]]
            enemypos = ((enemylocs[enemy])[2], (enemylocs[enemy])[3])
            playerpos = ((playerlocs[player])[2], (playerlocs[player])[3])
            path = pathfind(room, enemypos, playerpos)
            newenemypos = path[1]
            (enemylocs[enemy])[2] = newenemypos[0]
            (enemylocs[enemy])[3] = newenemypos[1]


async def new_player(playerid, playerlocs, game_map):
    spawnlocx = random.randint(16, 1248)
    spanwlocy = random.randint(16, 1248)
    while ((((game_map[0])[0])[spawnlocx // 16])[spanwlocy // 16]) != 0:
        spawnlocx = random.randint(16, 1248)
        spanwlocy = random.randint(16, 1248)
    location = [0, 0, spawnlocx, spanwlocy]
    playerlocs[playerid] = location

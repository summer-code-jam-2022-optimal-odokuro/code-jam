from . import mapgen as mg
from . import pathfind as pf
import random
from channels.layers import get_channel_layer


def initialize_game(player_ids):

    enemy_count = 200
    game_map = mg.generate_map()
    playerlocs = {}
    enemylocs = {}
    for player in player_ids:
        spawnlocx = random.randint(16, 1248)
        spanwlocy = random.randint(16, 1248)
        while ((((game_map[0])[0])[spawnlocx // 16])[spanwlocy // 16]) != 0:
            spawnlocx = random.randint(16, 1248)
            spanwlocy = random.randint(16, 1248)
        location = [0, 0, spawnlocx, spanwlocy]
        playerlocs[player] = location
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

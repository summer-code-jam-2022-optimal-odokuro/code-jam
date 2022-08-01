import asyncio
import json
from dataclasses import dataclass

from . import mapgen as mg
import random
from channels.layers import get_channel_layer

from .mapgen import generate_map
from .models import MapModel

from .pathfind import pathfind

import threading

PLAYER_RANGE = 2
ENTRANCE_BUFFER = 2


@dataclass(init=True)
class GameEntity:
    map_x: int
    map_y: int
    room_x: int
    room_y: int
    texture_type: str = 'None'

    def tile_x(self):
        return self.room_x // mg.PIXELS_TILE

    def tile_y(self):
        return self.room_y // mg.PIXELS_TILE


class Player(GameEntity):
    kills: int = 0


class Enemy(GameEntity):
    path: list[list[int, int]] = None


@dataclass(init=True)
class GameWrapper:

    has_players: bool
    game_id: str
    game_map: list[list[list[list[int]]]]
    player_locations: dict[str, Player]
    enemy_locations: dict[str, Enemy]

    async def room_players(self, map_x: int, map_y: int):
        items: dict[str, Player] = {}

        for k, v in self.player_locations.items():
            if v.map_x is map_x and v.map_y is map_y:
                items[k] = v

        return items

    async def room_enemies(self, map_x: int, map_y: int):
        items: dict[str, Enemy] = {}

        for k, v in self.enemy_locations.items():
            if v.map_x is map_x and v.map_y is map_y:
                items[k] = v

        return items

    async def loaded_rooms(self):

        rooms: list[list[int]] = []
        for k, v in self.player_locations.items():
            room = [v.map_x, v.map_y]
            if room not in rooms:
                rooms.append(room)

        return rooms

    async def loaded_enemies(self):
        items: dict[str, Enemy] = {}
        rooms = await self.loaded_rooms()

        for k, v in self.enemy_locations.items():
            if [v.map_x, v.map_y] in rooms:
                items[k] = v

        return items

    async def nearest_player(self, map_x: int, map_y: int, tile_x: int, tile_y: int):
        dist = [mg.ROOM_VERTICAL * mg.ROOM_HORIZONTAL, str]

        for k, v in (await self.room_players(map_x, map_y)).items():
            temp_dist = abs(tile_x - v.tile_x()) + abs(tile_y - v.tile_y())
            if temp_dist < dist[0]:
                dist = [temp_dist, k]

        return dist[1]

    async def update_clients(self):

        channel_layer = get_channel_layer()
        serial: dict[str, {list[list[list[list[int]]]] | dict[str, {str: int | str}]}] = {
            'map': self.game_map,
            'players': {},
            'enemies': {},
        }

        for k, v in self.player_locations.items():
            serial['players'][k] = {
                'map_x': v.map_x,
                'map_y': v.map_y,
                'room_x': v.room_x,
                'room_y': v.room_y,
                'texture_type': v.texture_type,
                'kills': v.kills,
            }

        for k, v in self.enemy_locations.items():
            serial['enemies'][k] = {
                'map_x': v.map_x,
                'map_y': v.map_y,
                'room_x': v.room_x,
                'room_y': v.room_y,
                'texture_type': v.texture_type,
            }

        await channel_layer.group_send(
            str.format('ingame_{}', self.game_id),
            {
                "type": "message",
                "game_wrapper": serial,
            },
        )

    async def enemy_actions(self, enemy_id: str):
        return
        # TODO FIX (type errors, out of bounds errors, ect)

        ref_enemy = self.enemy_locations[enemy_id]

        while (ref_enemy.path is None) or (not ref_enemy.path):
            target = self.player_locations[await self.nearest_player(
                ref_enemy.map_x, ref_enemy.map_y, ref_enemy.tile_x(), ref_enemy.tile_y())]

            path = await pathfind(maze=self.game_map[ref_enemy.map_x][ref_enemy.map_y],
                                  start=(ref_enemy.tile_x(), ref_enemy.tile_y()),
                                  end=(target.tile_x(), target.tile_y()))
            if path is None:
                return

            ref_enemy.path = path

        ref_enemy.room_x = ref_enemy.path[1][0] * mg.PIXELS_TILE
        ref_enemy.room_y = ref_enemy.path[1][1] * mg.PIXELS_TILE
        ref_enemy.path = ref_enemy.path.pop()

        self.enemy_locations[enemy_id] = ref_enemy

    async def player_input_handler(self, channel_name: str, player_input: str):
        player = self.player_locations[channel_name]
        room = self.game_map[player.map_x][player.map_y]
        newpos = [player.tile_x(), player.tile_y()]
        no_move = False

        match player_input:
            case 'up':
                newpos = [player.tile_x(), player.tile_y() + 1]

            case 'down':
                newpos = [player.tile_x(), player.tile_y() - 1]

            case 'left':
                newpos = [player.tile_x() - 1, player.tile_y()]

            case 'right:':
                newpos = [player.tile_x() + 1, player.tile_y()]

            case 'attack':
                no_move = True
                for k, v in (await self.room_enemies(player.map_x, player.map_y)).items():
                    if v.tile_x() in range(newpos[0] - PLAYER_RANGE, newpos[0] + PLAYER_RANGE) \
                            and v.tile_y() in range(newpos[1] - PLAYER_RANGE, newpos[1] + PLAYER_RANGE):
                        self.enemy_locations.pop(k)
                        player.kills += 1

            case _:
                no_move = True

        if not no_move:
            match room[newpos[0]][newpos[1]]:
                case mg.NONE_CHAR:
                    self.player_locations[channel_name].room_x = newpos[0] * mg.PIXELS_TILE
                    self.player_locations[channel_name].room_y = newpos[1] * mg.PIXELS_TILE
                    # Move player

                case mg.DOOR_CHAR:
                    enterpos = [int, int]
                    newroom = [int, int]
                    match player_input:
                        case 'up':
                            enterpos = [player.room_x, mg.PIXELS_TILE * ENTRANCE_BUFFER]
                            newroom = [player.map_x, player.map_y - 1]

                        case 'down':
                            enterpos = [player.room_x, (mg.MAP_VERTICAL - ENTRANCE_BUFFER) * mg.PIXELS_TILE]
                            newroom = [player.map_x, player.map_y + 1]

                        case 'left':
                            enterpos = [mg.PIXELS_TILE * ENTRANCE_BUFFER, player.room_y]
                            newroom = [player.map_x + 1, player.map_y]

                        case 'right:':
                            enterpos = [(mg.MAP_HORIZONTAL - ENTRANCE_BUFFER) * mg.PIXELS_TILE, player.room_y]
                            newroom = [player.map_x - 1, player.map_y]

                    self.player_locations[channel_name].room_x = enterpos[0]
                    self.player_locations[channel_name].room_y = enterpos[1]
                    self.player_locations[channel_name].map_x = newpos[0]
                    self.player_locations[channel_name].map_y = newroom[1]

                case _:
                    pass
                    # Nothing else can be moved into so there is no change in position

    async def new_player(self, playerid: str):
        # TODO FIX (main thing is use of magic numbers)
        spawnlocx = random.randint(mg.PIXELS_TILE, (mg.ROOM_HORIZONTAL - 1) * mg.PIXELS_TILE)
        spanwlocy = random.randint(mg.PIXELS_TILE, (mg.ROOM_VERTICAL - 1) * mg.PIXELS_TILE)
        while ((((self.game_map[0])[0])[spawnlocx // 16])[spanwlocy // 16]) != mg.NONE_CHAR:
            spawnlocx = random.randint(mg.PIXELS_TILE, (mg.ROOM_HORIZONTAL - 1) * mg.PIXELS_TILE)
            spanwlocy = random.randint(mg.PIXELS_TILE, (mg.ROOM_VERTICAL - 1) * mg.PIXELS_TILE)

        player = Player(map_x=0, map_y=0, room_x=spawnlocx, room_y=spanwlocy)
        self.player_locations[playerid] = player
        self.has_players = True

    async def del_player(self, playerid: str):
        self.player_locations.pop(playerid)
        if len(self.player_locations) == 0:
            self.has_players = False

    async def call_loaded_actions(self):
        for k, v in (await self.loaded_enemies()).items():
            await self.enemy_actions(k)


GameWrappers_Global_Dict: dict[str, GameWrapper] = {}
# TODO FIX (implement caching)
# This code is only here due to a lack of foresight and time. I will commit seppuku for my actions


async def game_thread(game_id):

    # This function will runforever in a thread
    while GameWrappers_Global_Dict[game_id].has_players:
        # All the game events that run some amount of time?
        # TODO implement gameticks
        # (idk how much they are supposed to run lol)
        await GameWrappers_Global_Dict[game_id].call_loaded_actions()
        await GameWrappers_Global_Dict[game_id].update_clients()
        await asyncio.sleep(1)

    # When the game no longer has any players, we can remove it from the dict
    GameWrappers_Global_Dict.pop(game_id)


def initialize_game(game_id):

    if game_id in GameWrappers_Global_Dict:
        return
        # If the game already exists (already in mem)

    map_obj = MapModel.objects.get_or_create(
        game_id=game_id,
        defaults={'map': generate_map()}
    )[0]

    game_wrapper = GameWrapper(
        game_id=str(game_id),
        game_map=map_obj.map,
        player_locations={},
        enemy_locations={},
        has_players=True
    )

    enemy_count = 200

    for enemy_id in range(1, enemy_count):
        roomx = 0
        roomy = 0
        spawnlocx = 0
        spawnlocy = 0
        while game_wrapper.game_map[roomx][roomy][spawnlocx // mg.PIXELS_TILE][spawnlocy // mg.PIXELS_TILE] \
                != mg.ROCK_CHAR:
            spawnlocx = random.randint(mg.PIXELS_TILE, (mg.ROOM_HORIZONTAL - 1) * mg.PIXELS_TILE)
            spawnlocy = random.randint(mg.PIXELS_TILE, (mg.ROOM_VERTICAL - 1) * mg.PIXELS_TILE)
            roomx = random.randint(0, mg.MAP_HORIZONTAL - 1)
            roomy = random.randint(0, mg.MAP_VERTICAL - 1)

        game_wrapper.enemy_locations[str(enemy_id)] = \
            Enemy(map_x=roomx, map_y=roomy, room_x=spawnlocx, room_y=spawnlocy)

    GameWrappers_Global_Dict[str(game_id)] = game_wrapper

    # Starts the game process to run in the background while players are connected
    thread = threading.Thread(target=asyncio.run, args=(game_thread(str(game_id)),), daemon=True)
    thread.start()



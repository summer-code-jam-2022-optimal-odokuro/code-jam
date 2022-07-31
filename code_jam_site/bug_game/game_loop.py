import json
from dataclasses import dataclass

from . import mapgen as mg
import random
from channels.layers import get_channel_layer

from .mapgen import generate_map
from .models import MapModel

from .pathfind import pathfind

PLAYER_RANGE = 2


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
    pass


class Enemy(GameEntity):
    path: list[list[int, int]] = None

    pass


@dataclass(init=True)
class GameWrapper:
    game_id: int
    game_map: list[list[list[list[int]]]]
    player_locations: dict[str, Player]
    enemy_locations: dict[str, Enemy]

    async def room_players(self, map_x: int, map_y: int):
        items = dict[str, Player]

        for k, v in self.player_locations.items():
            if v.map_x is map_x and v.map_y is map_y:
                items[k] = v

        return items

    async def room_enemies(self, map_x: int, map_y: int):
        items = dict[str, Enemy]

        for k, v in self.enemy_locations.items():
            if v.map_x is map_x and v.map_y is map_y:
                items[k] = v

        return items

    async def loaded_rooms(self):

        rooms = list[int, int]
        for k, v in self.player_locations.items():
            room = [v.map_x, v.map_y]
            if room not in rooms:
                rooms.append(room)

        return rooms

    async def loaded_enemies(self):
        items = dict[str, Enemy]
        rooms = await self.loaded_rooms()

        for k, v in self.enemy_locations.items():
            if [v.map_x, v.map_y] in rooms:
                items[k] = v

        return items

    async def nearest_player(self, map_x: int, map_y: int, tile_x: int, tile_y: int):
        dist = [mg.ROOM_VERTICAL * mg.ROOM_HORIZONTAL, str]

        for k, v in (await self.room_players(map_x, map_y)).items():
            temp_dist = abs(tile_x - v.tile_x) + abs(tile_y - v.tile_y)
            if temp_dist < dist[0]:
                dist = [temp_dist, k]

        return dist[1]

    async def player_update(self):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            str(self.game_id),
            {
                "type": "ingame.message",
                "map": self.game_map,
                "players": self.player_locations,
                "enemies": self.enemy_locations
            },
        )

    async def enemy_actions(self, enemy_id: str):
        ref_enemy = self.enemy_locations[enemy_id]

        if ref_enemy.path is not None and ref_enemy.path is not []:
            pass

        else:
            target = self.player_locations[await self.nearest_player(
                ref_enemy.map_x, ref_enemy.map_y, ref_enemy.tile_x(), ref_enemy.tile_y())]
            ref_enemy.path = await pathfind(maze=self.game_map[ref_enemy.map_x][ref_enemy.map_y],
                                            start=(ref_enemy.tile_x(), ref_enemy.tile_y()),
                                            end=(target.tile_x(), target.tile_y()))

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

            case _:
                no_move = True

        if not no_move:
            match room[newpos[0]][newpos[1]]:
                case mg.NONE_CHAR:
                    self.player_locations[channel_name].room_x = newpos[0] * mg.PIXELS_TILE
                    self.player_locations[channel_name].room_y = newpos[1] * mg.PIXELS_TILE
                    # Move player

                case mg.DOOR_CHAR:
                    pass
                # TODO

                case _:
                    pass
                    # Nothing else can be moved into so there is no change in position

    async def new_player(self, playerid: str):
        spawnlocx = random.randint(mg.PIXELS_TILE, (mg.ROOM_HORIZONTAL - 1) * mg.PIXELS_TILE)
        spanwlocy = random.randint(mg.PIXELS_TILE, (mg.ROOM_VERTICAL - 1) * mg.PIXELS_TILE)
        while ((((self.game_map[0])[0])[spawnlocx // 16])[spanwlocy // 16]) != mg.NONE_CHAR:
            spawnlocx = random.randint(mg.PIXELS_TILE, (mg.ROOM_HORIZONTAL - 1) * mg.PIXELS_TILE)
            spanwlocy = random.randint(mg.PIXELS_TILE, (mg.ROOM_VERTICAL - 1) * mg.PIXELS_TILE)

        player = Player(map_x=0, map_y=0, room_x=spawnlocx, room_y=spanwlocy)
        self.player_locations[playerid] = player


def initialize_game(game_id):
    game_exists = False
    game_wrapper = None

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

        game_wrapper = GameWrapper(game_id=game_id, game_map=game_map, player_locations={}, enemy_locations={})

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
                roomx = random.randint(0, mg.MAP_HORIZONTAL)
                roomy = random.randint(0, mg.MAP_VERTICAL)

            game_wrapper.enemy_locations[str(enemy_id)] = \
                Enemy(map_x=roomx, map_y=roomy, room_x=spawnlocx, room_y=spawnlocy)

    return game_map, game_wrapper

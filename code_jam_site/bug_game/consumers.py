from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .game_loop import GameWrapper, Player, GameWrappers_Global_Dict


class GameConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = str.format('ingame_{}', self.room_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # TODO: get the game wrapper to call new player on

        await GameWrappers_Global_Dict[self.room_name].new_player(self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await GameWrappers_Global_Dict[self.room_name].del_player(self.channel_name)

        pass

    async def receive_json(self, content, **kwargs):
        print("received json")

        # content is a dict representing player input

        await GameWrappers_Global_Dict[self.room_name].player_input_handler(
            channel_name=self.channel_name,
            player_input=content['input'])

        # TODO: get the game wrapper to call player input on

        pass

    async def message(self, event):
        print("sending json")

        # send event to self after parsing

        to_send = {}
        game_wrapper: GameWrapper = event["game_wrapper"]
        player: Player = game_wrapper.player_locations[self.channel_name]
        players = await game_wrapper.room_players(player.map_x, player.map_y)
        enemies = await game_wrapper.room_enemies(player.map_x, player.map_y)
        send_players = {}
        send_enemies = {}

        for k, v in players:
            send_players[k] = [v.room_x, v.room_y]
            # only send the room specific positional coordinates over

        for k, v in enemies:
            send_enemies[k] = [v.room_x, v.room_y]

        to_send['room'] = game_wrapper.game_map[player.map_x][player.map_y]
        to_send['players'] = send_players
        to_send['enemies'] = send_enemies

        await self.send_json(to_send)

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .game_loop import GameWrappers_Global_Dict


class GameConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = str.format('ingame_{}', self.room_name)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await GameWrappers_Global_Dict[self.room_name].new_player(self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        #TODO: this call gives a keyError sometimes, fix
        await GameWrappers_Global_Dict[self.room_name].del_player(self.channel_name)

    async def receive_json(self, content, **kwargs):
        # content is a dict representing player input

        await GameWrappers_Global_Dict[self.room_name].player_input_handler(
            channel_name=self.channel_name,
            player_input=content['input'])

    async def message(self, event):

        # send event to self after parsing

        to_send = {}
        serial: dict[str, {list[list[list[list[int]]]] | dict[str, {str: int | str}]}] = event["game_wrapper"]

        player: dict[str, {str: int | str}] = serial['players'][self.channel_name]
        room = [player['map_x'], player['map_y']]

        send_players = {}
        send_enemies = {}

        for k, v in serial['players'].items():
            if room == [v['map_x'], v['map_y']]:
                send_players[k] = v

            # only send the room specific positional coordinates over

        for k, v in serial['enemies'].items():
            if room == [v['map_x'], v['map_y']]:
                send_enemies[k] = v

        to_send['room']: list[list[list[list[int]]]] = serial['map'][room[0]][room[1]]
        to_send['players'] = send_players
        to_send['enemies'] = send_enemies
        to_send['room_index'] = room
        to_send['player_key'] = self.channel_name

        await self.send_json(to_send)

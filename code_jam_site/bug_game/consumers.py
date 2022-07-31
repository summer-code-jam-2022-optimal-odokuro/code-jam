from channels.generic.websocket import AsyncJsonWebsocketConsumer
from game_loop import GameWrapper, Player, GameWrappers_Global_Dict


class GameConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = 'ingame_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # TODO: get the game wrapper to call new player on

        await GameWrappers_Global_Dict[self.room_name].new_player(self.room_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await GameWrappers_Global_Dict[self.room_name].del_player(self.room_name)

        pass

    async def receive_json(self, content, **kwargs):
        # content is a dict representing player input

        await GameWrappers_Global_Dict[self.room_name].player_input_handler(content)

        # TODO: get the game wrapper to call player input on

        pass

    async def ingame_message(self, event):
        # send event to self after parsing
        # TODO: modify event before sending

        await self.send_json(event)

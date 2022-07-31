from channels.generic.websocket import AsyncJsonWebsocketConsumer
from game_loop import new_player


class GameConsumer(AsyncJsonWebsocketConsumer):
    map_x: int
    map_y: int
    room_x: int
    room_y: int

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = 'ingame_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)



        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        pass

    async def receive_json(self, content, **kwargs):
        # content is a dict representing player input
        # TODO: get the game wrapper

        await new_player(self.room_name, )

        pass

    async def ingame_message(self, event):
        # send event to self after parsing
        # TODO: modify event before sending

        await self.send_json(event)

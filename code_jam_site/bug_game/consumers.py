import json

from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer

class ClientConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


class GameConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'ingame_%s' % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        pass

    async def receive_json(self, content, **kwargs):
        # content is a dict representing player input

        # call player with input

        pass

    async def ingame_message(self, event):
        # send event to self after parsing

        pass

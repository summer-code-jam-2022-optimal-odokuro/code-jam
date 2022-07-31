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

        await self.accept()

    async def disconnect(self, code):

        pass

    async def receive_json(self, content, **kwargs):

        # content is a tuple? of decoded json object item

        await self.send_json(content={'message': 'among'})


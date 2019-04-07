
# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class YtdlConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "ytdl-{}".format(user_id)
        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data = None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        user = text_data_json["user"]
        reci = text_data_json['reci']
        ytTime = text_data_json["time"]
        video_id = text_data_json['video_id']
        video_state = text_data_json['video_state']
        if user >reci:
            group_name = user+reci
        else:
            group_name = reci+user

        if group_name != self.group_name:
            self.group_name = group_name
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        #Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'recieve_group_message',
                'ytTime': ytTime,
                'video_id':video_id,
                'video_state':video_state

            }
        )

    async def recieve_group_message(self, event):
        ytTime = event['ytTime']
        video_id = event['video_id']
        video_state = event['video_state']

        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'ytTime': ytTime,
                 'video_id': video_id,
                 'video_state': video_state

             }))





class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "{}".format(user_id)
        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data = None):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message
            }
        )

    async def recieve_group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'message': message
        }))
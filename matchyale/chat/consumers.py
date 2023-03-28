import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage
from django.contrib.auth.models import User
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        me = self.scope['user'].id
        print(self.scope)
        receiver = self.scope['url_route']['kwargs']['room_name']
        #self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        if int(me) > int(receiver):
            self.room_name = f'{me}-{receiver}'
        else:
            self.room_name = f'{receiver}-{me}'
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("Haha", text_data_json)
        message = text_data_json["message"]
        username = text_data_json['username']
        receiver = text_data_json['receiver']
        await self.save_msg(username, self.room_group_name, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {"type": "chat_message", 
             "message": message,
             'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {"type": "chat_message", 
             "message": message,
             'username': username,}))
    
    
    @sync_to_async
    def save_msg(self, username, room, content):
        ChatMessage.objects.create(username=username, room_name=room, content=content)
    
    
class PublicChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % 'public'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
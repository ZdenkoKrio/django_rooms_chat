import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.db import models
from .models import *
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
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
        message = text_data_json["message"]
        username = text_data_json['username']
        room_name = self.room_name

        print(f"NAME: {username}")

        # Uloženie správy do DB asynchrónne
        await self.save_message_to_db(username, message, room_name)

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'username': username,
        })

    # Asynchrónna funkcia na uloženie správy do databázy
    @database_sync_to_async
    def save_message_to_db(self, username, message, room_name):
        try:
            user = User.objects.get(username=username)
            chatroom = Chatroom.objects.get(name=room_name)
            Message.objects.create(sender=user, content=message, chatroom=chatroom)
        except User.DoesNotExist:
            # Handle user not found case if needed
            pass
        except models.Chatroom.DoesNotExist:
            # Handle chatroom not found case if needed
            pass

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Získanie mena odosielateľa

        # Debugging výpis pre kontrolu, či sa meno správne posiela späť
        print(f"Sending back: {username}, {message}")

        # Poslanie správy naspäť do WebSocketu
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username  # Poslanie používateľského mena
        }))
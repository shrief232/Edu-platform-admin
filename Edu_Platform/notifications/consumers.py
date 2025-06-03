from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('=')[1]
        
        try:
            access_token = AccessToken(token)
            self.user = access_token.payload.get('user_id')
        except:
            self.user = AnonymousUser()
        
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": message
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class ReceptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.hospital_id = self.scope['url_route']['kwargs']['hospital_id']
            self.room_group_name = f'hospital_{self.hospital_id}'

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # Agar operator chiqib ketsa, uni offlayn qilish mantiqi shu yerda bo'ladi

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'request_call':
            # Bemor qo'ng'iroq so'radi
            await self.handle_call_request()
            
        elif action == 'operator_free':
            # Operator suhbatni tugatdi va bo'shadi
            await self.notify_next_patient()

    @database_sync_to_async
    def handle_call_request(self):
        # Bo'sh operatorni tekshirish va navbatga qo'shish mantiqi (DB amallari)
        pass # Bu yerda utils.py dagi mantiq chaqiriladi

    async def notify_next_patient(self):
        """Navbatdagi bemorga operator bo'shaganini xabar qilish"""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'queue_update',
                'message': 'Operator bo\'shadi, navbatdagi bemor ulanmoqda...'
            }
        )

    async def queue_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message']
        }))

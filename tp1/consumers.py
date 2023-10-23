from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'tp1'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        sender = data['sender']
        message = data['message']
        encryption = data['encryption']
        print(encryption)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": sender,
                "message": message,
                "encryption": encryption
            }
        )

    def chat_message(self, event):
        sender = event['sender']
        message = event['message']
        encryption = event['encryption']
        
        self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "message": message,
                    "encryption": encryption
                }
            )
        )

from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .encryptions import *
from .serializers import *

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

        serializer = DefaultEncryptionSerializer(data=data)
        if serializer.is_valid():
            match data['encryption_type']:
                case "rotation":
                    if serializer.is_valid():
                        data['type'] = "rotation_message"
                    else:
                        raise Exception()
                case "caesar":
                    serializer = CaesarEncryptionSerializer(data=data)
                    if serializer.is_valid():
                        data['type'] = "caesar_message"
                    else:
                        raise Exception()
                case _:
                    self.send(serializer.errors)
                    return
                
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                data
            )
        else:
            self.send(json.dumps(serializer.errors))
    
    def rotation_message(self, event):
        sender = event['sender']
        message = event['message']
        direction = event['direction']
        date = event['date']
        
        self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "message": left_rotation(text=message) if direction == 'left' else right_rotation(text=message),
                    "direction": direction,
                    "encryption_type":"rotation",
                    "date": date
                }
            )
        )
    
    def caesar_message(self, event):
        sender = event['sender']
        message = event['message']
        caesar_value = event['caesar_value']
        direction = event['direction']
        date = event['date']
        
        self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "message": left_caesar(text=message, shift=caesar_value) if direction == 'left' else right_caesar(text=message, shift=caesar_value),
                    "direction": direction,
                    "caesar_value": caesar_value,
                    "encryption_type":"caesar",
                    "date": date
                }
            )
        )
    

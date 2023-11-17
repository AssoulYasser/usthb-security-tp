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
                    serializer = RotationEncryptionSerializer(data=data)
                    if serializer.is_valid():
                        serializer.validated_data['type'] = "rotation_message"
                    else:
                        self.send(json.dumps(serializer.errors))
                        return
                case "caesar":
                    serializer = CaesarEncryptionSerializer(data=data)
                    if serializer.is_valid():
                        serializer.validated_data['type'] = "caesar_message"
                    else:
                        self.send(json.dumps(serializer.errors))
                        return
                case "mirror":
                    serializer = MirrorEncryptionSerializer(data=data)
                    if serializer.is_valid():
                        serializer.validated_data['type'] = "mirror_message"
                    else:
                        self.send(json.dumps(serializer.errors))
                        return
                case "affine":
                    serializer = AffineEncryptionSerializer(data=data)
                    if serializer.is_valid():
                        serializer.validated_data['type'] = "affine_meesage"
                    else:
                        self.send(json.dumps(serializer.errors))
                        return
                case _:
                    self.send(json.dumps(serializer.errors))
                    return
                
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                serializer.validated_data
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
                    "message": cryptage_rotation(message, direction),
                    "encryption_type":"rotation",
                    "date": str(date),
                    "extra_char": None,
                    "direction": direction,
                    "caesar_value": None,
                    "extra_char": None,
                    "a": None,
                    "b": None,
                    "error": None
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
                    "message": caesar_encrypt(message, caesar_value, direction),
                    "encryption_type":"caesar",
                    "date": str(date),
                    "extra_char": None,
                    "direction": direction,
                    "caesar_value": caesar_value,
                    "extra_char": None,
                    "a": None,
                    "b": None,
                    "error": None
                }
            )
        )
    
    def mirror_message(self, event):
        sender = event['sender']
        message = event['message']
        date = event['date']
        extra_char = event['extra_char']
        mirror_encryption = mirror_encrypt_phrase(phrase=message, extra_char=extra_char)

        self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "message": mirror_encryption,
                    "encryption_type":"mirror",
                    "date": str(date),
                    "direction": None,
                    "caesar_value": None,
                    "extra_char": extra_char,
                    "a": None,
                    "b": None,
                    "error": None
                }
            )
        )

    def affine_meesage(self, event):
        sender = event['sender']
        message = event['message']
        date = event['date']
        a = event['a']
        b = event['b']
        try:
            affine_result = affine_encryption(text=message, a=a, b=b)
            self.send(
                text_data=json.dumps(
                    {
                        "sender": sender,
                        "message": affine_result,
                        "encryption_type":"affine",
                        "date": str(date),
                        "extra_char": None,
                        "direction": None,
                        "caesar_value": None,
                        "extra_char": None,
                        "a": a,
                        "b": b,
                        "error": None
                    }
                )
            )
        except Exception as e:
            self.send(
                text_data=json.dumps(
                    {
                        "sender": sender,
                        "message": None,
                        "encryption_type":"affine",
                        "date": str(date),
                        "extra_char": None,
                        "direction": None,
                        "caesar_value": None,
                        "extra_char": None,
                        "a": a,
                        "b": b,
                        "error": str(e)
                    }
                )
            )
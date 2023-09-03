import json 
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import base64 

class ProcessConsunmer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'progress_{self.room_name}'
       
        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            if "fps" in message:
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'realtime_message',
                    'message': message,
                }
            )
            else:
                # send chat message event to the room
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'text_message',
                        'message': message,
                    }
                )
        except:
            # Convert back to binary
            jpg_original = base64.b64decode(bytes_data)
            data = {"type": "update_frame", "data" : jpg_original}
            # Write to a file to show conversion worked
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'byte_message',
                    'message': data,
                }
            )
    def text_message(self, event):
        self.send(text_data=json.dumps(event))
    
    def byte_message(self, event):
        self.send(bytes_data=event['message']['data'])

    def realtime_message(self, event):
        self.send(text_data=json.dumps(event))
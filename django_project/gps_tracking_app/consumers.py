import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GpsLogConsumer(WebsocketConsumer):
    """
        Synchronous WebSocket consumer that accepts all connections,
        receives messages from its client, and echos those messages
        back to the same client
    """

    def connect(self):
        self.serial_number = self.scope['url_route']['kwargs']['serial_number']
        self.group_name = 'device_{sn}'.format(sn=self.serial_number)

        # Join group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'location_update',
                'message': message
            }
        )

    def location_update(self, data):
        # Send message to WebSocket
        self.send(text_data=data['message'])

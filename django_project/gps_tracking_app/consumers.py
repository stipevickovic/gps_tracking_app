import json
import sys
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer, SyncConsumer
from channels.layers import get_channel_layer
from django.contrib.gis.geos import GEOSGeometry

from gps_tracking_app.models import GeofenceZone, GPSDevice


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


class PositionCheckConsumer(SyncConsumer):

    def position_check(self, message):
        """
        Check if there are zones in wich GPS device is not
        located and send those location on websocket
        """

        # Creating POINT object out of longitude and latitude information
        last_location = GEOSGeometry('POINT({}  {})'.format(message['long'], message['lat']),
                                     srid=4326)

        try:
            gps_device = GPSDevice.objects.get(serial_number=message['gps_serial'])
        except GPSDevice.DoesNotExist:
            sys.stderr.write('GPS device with serial number {} does not exist!\n'.format(message['gps_serial']))
            return

        # Filter associated Geofence zones in which device is not located
        exclude_zones = GeofenceZone.objects.filter(gps=gps_device).exclude(geom__contains=last_location)

        # If there are zones without GPS signal, send their ID via websocket
        if exclude_zones.exists():
            # Send payload to websocket
            channel_layer = get_channel_layer()
            group_name = 'device_{}'.format(message['gps_serial'])
            data = {'type': 'zone warning', 'long': message['long'],
                    'lat': message['lat'], 'zone': [zone.id for zone in exclude_zones]}
            async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type': 'location_update',
                        'message': json.dumps(data)
                    }
                    )

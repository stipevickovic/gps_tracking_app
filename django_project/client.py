import django
import json
import paho.mqtt.client as mqtt
import os
import sys
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Setup django instance
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from django.conf import settings # noqa
from django.db import connection # noqa

from gps_tracking_app.models import GPSDevice # noqa


def on_connect(client, userdata, flags, rc):
    client.subscribe('{}/devices/{}/up'.format(settings.MQTT_TTN['user'],
                                               settings.MQTT_TTN['device']))
    sys.stdout.write('Connected with result code {} \n'.format(rc))


def on_message(client, userdata, message):
    """Save recived payload in database and send it on websocket """

    SQL = """INSERT INTO gps_tracking_app_log(gps_id, location, date_time)
    VALUES (%s, ST_GeometryFromText('POINT(%s %s)', 4326), %s);"""

    # Extracting from payload
    gps_payload = json.loads(message.payload.decode())
    gps_serial = gps_payload['hardware_serial']
    gps_lat = gps_payload['payload_fields']['gps']['latitude']
    gps_long = gps_payload['payload_fields']['gps']['longitude']
    gps_time = gps_payload['metadata']['time']

    try:
        gps_device = GPSDevice.objects.get(serial_number=gps_serial)
    except GPSDevice.DoesNotExist:
        sys.stderr.write('GPS device with serial number {} does not exist!\n'.format(gps_serial))
        return

    # Connecting to database and executing SQL
    cur = connection.cursor()
    cur.execute(SQL, (gps_device.id, gps_long, gps_lat, gps_time))
    connection.commit()
    cur.close()

    # Send payload to websocket
    channel_layer = get_channel_layer()
    group_name = 'device_1'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'location_update',
            'message': json.dumps(gps_lat)
        }
        )


client = mqtt.Client()
client.username_pw_set(settings.MQTT_TTN['user'], password=settings.MQTT_TTN['password'])
client.on_connect = on_connect
client.on_message = on_message


client.connect(settings.MQTT_TTN['broker_address'], port=settings.MQTT_TTN['port'])

client.loop_forever()

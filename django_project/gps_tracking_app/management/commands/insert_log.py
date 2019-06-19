import json
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from random import randrange
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import connection


def random_date(start, end):
    """
    Return a random datetime between two datetime objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_log_data():
    """
    Generate and insert 100 test objects in Log.
    """
    SQL = """INSERT INTO gps_tracking_app_log(gps_id, location, date_time)
    VALUES (%s, ST_GeometryFromText('POINT(%s %s)', 4326), %s);"""

    for i in range(100):
        a = random.randint(1, 2)
        blong = random.uniform(6.5, 9.5)
        blat = random.uniform(46, 47.5)
        start = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
        end = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')
        c = '{} +2:00'.format(random_date(start, end))
        cur = connection.cursor()
        # execute the INSERT statement
        cur.execute(SQL, (a, blong, blat, c))
        # commit the changes to the database
        connection.commit()
        # close communication with the database
        cur.close()
        data = {'gps_serial_no': a, 'long': blong, 'lat': blat, 'timestamp': c}
        channel_layer = get_channel_layer()
        group_name = 'device_1'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'location_update',
                'message': json.dumps(data)
            }
            )


class Command(BaseCommand):
    help = """
      Generate 100 random log objects.
      """

    def handle(self, *args, **options):
        generate_log_data()

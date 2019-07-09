from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer

from gps_tracking_app.models import GPSDevice, Log, GeofenceZone


class GPSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSDevice
        fields = ('id', 'serial_number', 'terryx_station_id')


class LogSerializer(GeoModelSerializer):
    gps_id = serializers.PrimaryKeyRelatedField(queryset=GPSDevice.objects.all(), write_only=True)
    gps_sn = serializers.ReadOnlyField(source='gps.serial_number')

    class Meta:
        model = Log
        geo_field = 'location'
        fields = ('gps_id', 'gps_sn', 'date_time', 'location')


class GeofenceZoneSerializer(GeoModelSerializer):
    gps = serializers.PrimaryKeyRelatedField(queryset=GPSDevice.objects.all())
    gps_sn = serializers.ReadOnlyField(source='gps.serial_number')

    class Meta:
        model = GeofenceZone
        geo_field = 'geom'
        fields = ('id', 'gps', 'gps_sn', 'geom')

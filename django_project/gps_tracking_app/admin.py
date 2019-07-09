from django.conf import settings
import django.contrib.gis.admin as admin

from gps_tracking_app.models import GPSDevice, Log, GeofenceZone


@admin.register(GPSDevice)
class GPSDeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'id')


@admin.register(Log)
class LogAdmin(admin.GeoModelAdmin):
    list_display = ('gps', 'date_time')
    default_lon = 8
    default_lat = 45
    openlayers_url = settings.OPENLAYERS_URL


@admin.register(GeofenceZone)
class GeofenceZoneAdmin(admin.GeoModelAdmin):
    list_display = ('id', 'gps')
    default_lon = 8
    default_lat = 45
    openlayers_url = settings.OPENLAYERS_URL

from django.conf import settings
import django.contrib.gis.admin as admin

from gps_tracking_app.models import GPSDevice, Log


@admin.register(GPSDevice)
class GPSDeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'id')


@admin.register(Log)
class LogAdmin(admin.GeoModelAdmin):
    list_display = ('gps', 'date_time')
    default_lon = 8
    default_lat = 45
    openlayers_url = settings.OPENLAYERS_URL

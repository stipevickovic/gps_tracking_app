from django.shortcuts import render, get_object_or_404
from rest_framework import filters, generics

from gps_tracking_app.models import GPSDevice, Log, GeofenceZone
from gps_tracking_app.serializers import GPSDeviceSerializer, LogSerializer, GeofenceZoneSerializer


def index(request):
    location_object = Log.objects.order_by('-date_time').first()
    location_dict = {"location": location_object}
    return render(request, 'gps_tracking_app/index.html', location_dict)


class DeviceList(generics.ListCreateAPIView):
    """
    get: List all the devices.
    post: Create a new device.
    """

    queryset = GPSDevice.objects.all()
    serializer_class = GPSDeviceSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('id', 'serial_number',)
    search_fields = ('id', 'serial_number',)
    ordering_fields = ('id', 'serial_number',)
    ordering = ('id', 'serial_number',)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: Get a device instance.
    put: Updates device instace
    patch: Partially update device instance.
    delete: Delete a device instance.
    """
    serializer_class = GPSDeviceSerializer

    def get_object(self):
        """ Return GPS device for current sn"""
        return get_object_or_404(GPSDevice, serial_number=self.kwargs['sn'])


class LogList(generics.ListAPIView):
    """
    get: List all the logs for specific device.
    """
    serializer_class = LogSerializer

    def get_queryset(self):
        """ Return logs for current gps device"""
        serial_number = self.kwargs['sn']
        gps_device = get_object_or_404(GPSDevice, serial_number=serial_number)
        return Log.objects.filter(gps=gps_device)


class GeofenceZoneList(generics.ListCreateAPIView):
    """
    get: List all the zones for specific device.
    post: Create a new zone.
    """
    serializer_class = GeofenceZoneSerializer

    def get_queryset(self):
        """ Returning geofence zones for current gps device"""
        serial_number = self.kwargs['sn']
        gps_device = get_object_or_404(GPSDevice, serial_number=serial_number)
        return GeofenceZone.objects.filter(gps=gps_device)

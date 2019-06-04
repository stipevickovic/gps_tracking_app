from django.contrib.gis.db.models import PointField
from django.db import models


class GPSDevice(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    terryx_station_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.id


class MyQuerySet(models.query.QuerySet):
    def delete(self):
        raise NotImplementedError('RawData queryset delete is not supported')


class RawDataManager(models.Manager):

    def get_queryset(self):
        return MyQuerySet(self.model, using=self._db)


class Log(models.Model):
    gps = models.ForeignKey(GPSDevice, on_delete=models.CASCADE)
    date_time = models.DateTimeField(primary_key=True)
    location = PointField(srid=4326, null=True, blank=True)

    class Meta:
        # This table is managed manually, as it's a Timescale table
        managed = False

    objects = RawDataManager()

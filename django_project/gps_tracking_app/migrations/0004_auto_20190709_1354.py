# Generated by Django 2.2.3 on 2019-07-09 11:54

import django.contrib.gis.db.models.fields
from django.db import migrations
from django.contrib.gis.geos import Polygon


class Migration(migrations.Migration):

    dependencies = [
        ('gps_tracking_app', '0003_auto_20190703_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geofencezone',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(default=Polygon(((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), srid=4326),
            preserve_default=False,
        ),
    ]

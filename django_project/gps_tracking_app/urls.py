from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from gps_tracking_app import views

# @permission_classes((AllowedAny, ))
schema_view = get_swagger_view(title="GPS_Tracking API")

urlpatterns = [
    url(r'gps-devices/$', views.DeviceList.as_view(), name='device-list'),
    url(r'gps-devices/(?P<sn>[-\w]+)/$', views.DeviceDetail.as_view(), name='device-detail'),
    url(r'gps-devices/(?P<sn>[-\w]+)/data/$', views.LogList.as_view(), name='log-list'),
    url(r'gps-devices/(?P<sn>[-\w]+)/geofence-areas/$', views.GeofenceZoneList.as_view(),
        name='geofence-areas-detail'),
    url(r'^$', views.index, name='index'),
    url(r'^schema$', schema_view),
]

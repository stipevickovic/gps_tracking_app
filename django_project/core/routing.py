from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from gps_tracking_app. consumers import PositionCheckConsumer, GpsLogConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/gps/(?P<serial_number>[-\w]+)/$', GpsLogConsumer)
        ])
    ),
    'channel': ChannelNameRouter({
        'location-check': PositionCheckConsumer,
    })
})

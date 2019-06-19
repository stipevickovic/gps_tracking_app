from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from gps_tracking_app. consumers import GpsLogConsumer
from django.conf.urls import url


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/gps/(?P<serial_number>[0-9]+)/$', GpsLogConsumer)
        ])
    )
})

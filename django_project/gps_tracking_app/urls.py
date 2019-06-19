from django.conf.urls import url

from gps_tracking_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

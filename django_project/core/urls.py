from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls)
]

urlpatterns = format_suffix_patterns(urlpatterns)

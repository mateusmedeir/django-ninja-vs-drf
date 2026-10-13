from django.contrib import admin
from django.urls import include, path

from config.api_ninja import api as ninja_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ninja/v1/', ninja_api.urls),
    path('drf/v1/', include('config.api_drf')),
]

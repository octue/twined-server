from django.urls import path

from . import consumers


# from django.urls import path, re_path

websocket_urlpatterns = [
    path("ws/twined/<uuid:room_name>/", consumers.TwinedConsumer),
]

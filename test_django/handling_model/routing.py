from django.urls import path,re_path

#
# websocket_urlpatterns = [
#     path(r'ws/webcam/', consumers.WebcamConsumer.as_asgi()),
# ]

from django.urls import path
from .consumers import WebcamConsumer

websocket_urlpatterns = [
    path('ws/webcam/', WebcamConsumer.as_asgi()),
]

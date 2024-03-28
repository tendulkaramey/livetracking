from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/test/<str:name>/', consumers.TestConsumer.as_asgi()),
]
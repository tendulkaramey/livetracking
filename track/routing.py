from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/test/<str:name>/', consumers.TestConsumer.as_asgi()),
    path('ws/test-group/<str:name>/', consumers.TestConsumerGroupPeriodic.as_asgi()),
    path('ws/test-basic/<str:name>/', consumers.TestConsumerBasic.as_asgi()),
]
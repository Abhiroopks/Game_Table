from django.urls import re_path

from games import consumers

websocket_urlpatterns = [
    re_path("mlb_data", consumers.MLBConsumer.as_asgi()),
]

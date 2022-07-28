from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bug_game/(?P<game_id>\w+)/$', consumers.ClientConsumer.as_asgi()),
]

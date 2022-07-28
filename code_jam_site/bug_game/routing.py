from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'bug_game/ingame/(?P<game_id>\w+)/$', consumers.ClientConsumer.as_asgi()),
]

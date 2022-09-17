from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/join/(?P<match_id>\w+)/$', consumers.JoinConsumer.as_asgi()),
    re_path(r'ws/move/(?P<match_id>\w+)/$', consumers.MoveConsumer.as_asgi()),
    re_path(r'ws/resign/(?P<match_id>\w+)/$', consumers.ResignConsumer.as_asgi()),
]
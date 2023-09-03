from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumer
from django.conf.urls import url

websocket_urlpatterns = [

    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumer.ProcessConsunmer.as_asgi()),
]
application = ProtocolTypeRouter( 
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)
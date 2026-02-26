from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://localhost:8000/ws/reception/<hospital_id>/
    re_path(r'ws/reception/(?P<hospital_id>\d+)/$', consumers.ReceptionConsumer.as_asgi()),
]

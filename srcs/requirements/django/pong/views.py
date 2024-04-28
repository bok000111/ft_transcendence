from django.shortcuts import render
import websockets
import asyncio
from channels.generic.websocket import WebsocketConsumer

# Create your views here.
# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "pong/index.html")

def room(request, room_name):
    return render(request, "pong/room.html", {"room_name": room_name})
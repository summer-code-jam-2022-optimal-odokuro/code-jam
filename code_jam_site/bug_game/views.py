from django.shortcuts import render

from .mapgen import generate_map
from .models import MapModel

# Create your views here.


def home(request):
    return render(request, 'bug_game/home.html')


def ingame(request, game_id=None):
    if game_id is None:
        game_id = 0
        # change this to a random number or read from a database

    if MapModel.objects.filter(game_id=game_id).exists():
        game_map = MapModel.objects.filter(game_id=game_id)[0].map

    else:
        game_map = generate_map(game_id)
        MapModel.objects.create(map=game_map, game_id=game_id)

    return render(request, 'bug_game/ingame.html', {'game_map': game_map})


def lobby(request):
    return render(request, 'bug_game/lobby.html')

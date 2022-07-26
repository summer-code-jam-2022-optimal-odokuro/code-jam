import json

from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from .game_loop import initialize_game, GameWrapper

# Create your views here.


def home(request):
    return render(request, 'bug_game/home.html')


def ingame(request, game_id=None):
    if game_id is None:
        return HttpResponseRedirect(reverse(viewname='ingame', kwargs={'game_id': 0}))
        # change this to a random number or read from a database

    initialize_game(game_id=game_id)
    # not async oof

    return render(request, 'bug_game/ingame.html', {'game_id': game_id})


def lobby(request):
    return render(request, 'bug_game/lobby.html')

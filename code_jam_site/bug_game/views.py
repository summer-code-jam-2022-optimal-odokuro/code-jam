from django.shortcuts import render

# Create your views here.


def home(request):

    return render(request, 'bug_game/home.html')


def ingame(request, game_id=None):

    if game_id is None:
        game_id = 0
        # change this to a random number or read from a database

    return render(request, 'bug_game/ingame.html', {'game_id': game_id})


def lobby(request):

    return render(request, 'bug_game/lobby.html')

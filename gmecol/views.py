from django.shortcuts import render
from django.http import HttpResponseNotFound

from gmecol import forms, utils


def index(request):
    ''' Default landing page '''

    return render(request, 'gmecol/index.html', {})


def search(request):
    ''' Search for games '''

    form = forms.SearchGamesForm(request.GET if request.GET else None)
    games = None
    if form.is_valid():
        games = utils.giant_bomb_search(form.cleaned_data.get('name'))
    return render(request, 'gmecol/search.html', {
        'form': form,
        'games': games,
    })


def game_detail(request, remote_id):
    ''' Game detail view. Grabs the game from our database, otherwise snags it
    from Giant Bomb's API and saves it locally
    '''
    remote_id = int(remote_id)
    games = utils.giant_bomb_game_detail(remote_id)

    if not games:
        return HttpResponseNotFound()

    game_root = games[0]

    return render(request, 'gmecol/game_detail.html', {
        'games': games,
        'game_root': game_root,
    })

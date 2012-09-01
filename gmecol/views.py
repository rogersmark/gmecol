from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from gmecol import models, forms, utils


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


def game_platform_detail(request, game_id, platform_id):
    ''' Takes a remote_id for a game, along with a platform_id to find the
    exact copy of a game a user is requesting
    '''
    game = get_object_or_404(
        models.Game,
        remote_id=game_id,
        platform__remote_id=platform_id
    )

    return render(request, 'gmecol/game_platform_detail.html', {
        'game': game
    })


@login_required
def add_game_to_collection(request, game_id, platform_id):
    ''' Adds game to a user's collection '''
    game = get_object_or_404(
        models.Game,
        remote_id=game_id,
        platform__remote_id=platform_id
    )

    if game not in request.user.userprofile.games.all():
        models.UserGame.objects.get_or_create(
            game=game,
            user=request.user.userprofile
        )

    return redirect('game-platform-detail', game_id, platform_id)

import json
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from gmecol import models


@login_required
def add_game_to_collection(request, game_id, wish=False):
    ''' Adds game to a user's collection '''
    game = get_object_or_404(models.Game, pk=game_id)

    if game not in request.user.userprofile.games.all():
        models.UserGame.objects.get_or_create(
            game=game,
            user=request.user.userprofile,
            wish=wish
        )
    else:
        user_game = models.UserGame.objects.get(
            user=request.user.userprofile,
            game=game
        )
        user_game.wish = wish
        user_game.save()

    return redirect('game-platform-detail',
        game.remote_id,
        game.platform.remote_id)


@login_required
def rate_game(request, game_id):
    ''' View taking a game PK and score, and setting the player's rating. If
    0 is received, we null the score
    '''
    game = get_object_or_404(
        models.UserGame,
        game__pk=game_id,
        user=request.user.userprofile
    )
    score = Decimal(request.GET.get('score')) or None
    game.rating = score
    game.save()
    return HttpResponse(
        json.dumps({'status': 1}),
        content_type='application/json'
    )


@login_required
def toggle_trade_and_sale(request, game_id, trade=True):
    ''' Toggles the trade status of a game that exists in a user's collection
    '''
    game = get_object_or_404(
        models.UserGame,
        game__pk=game_id,
        user=request.user.userprofile
    )
    if trade:
        game.for_trade = False if game.for_trade else True
    else:
        game.for_sale = False if game.for_sale else True
    game.save()
    json_data = json.dumps({
        'status': True,
        'for_trade': game.for_trade,
        'for_sale': game.for_sale
    })
    return HttpResponse(
        json_data,
        content_type='application/json'
    )

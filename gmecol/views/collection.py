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
def view_collection(request, wish=False):
    ''' Views a users collection '''
    genres = models.Genre.objects.filter(
        pk__in=request.user.userprofile.usergame_set.filter(wish=wish).values_list(
            'game__genres__pk', flat=True)
    ).distinct()
    platforms = models.Platform.objects.filter(
        pk__in=request.user.userprofile.usergame_set.filter(wish=wish).values_list(
            'game__platform__pk', flat=True)
    ).distinct()

    return render(request, 'gmecol/user_collection.html', {
        'platforms': platforms,
        'genres': genres,
        'wish': wish,
    })


@login_required
def view_collection_by_genre(request, genre_id, wish=False):
    ''' View games in a collection by a genre '''
    genre = get_object_or_404(models.Genre, pk=genre_id)
    games = request.user.userprofile.usergame_set.filter(
        game__genres=genre,
        wish=wish
    )

    return render(request, 'gmecol/user_collection_by_genre.html', {
        'genre': genre,
        'games': games
    })


@login_required
def view_collection_by_platform(request, platform_id, wish=False):
    ''' View games in a collection by platform '''
    platform = get_object_or_404(models.Platform, pk=platform_id)
    games = request.user.userprofile.usergame_set.filter(
        game__platform=platform,
        wish=wish
    )

    return render(request, 'gmecol/user_collection_by_platform.html', {
        'platform': platform,
        'games': games
    })


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
        mimetype='application/json'
    )

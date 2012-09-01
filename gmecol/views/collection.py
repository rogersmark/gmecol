from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from gmecol import models


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


@login_required
def view_collection(request):
    ''' Views a users collection '''
    genres = models.Genre.objects.filter(
        pk__in=request.user.userprofile.games.all().values_list(
            'genres__pk', flat=True)
    ).distinct()
    platforms = models.Platform.objects.filter(
        pk__in=request.user.userprofile.games.all().values_list(
            'platform__pk', flat=True)
    ).distinct()

    return render(request, 'gmecol/user_collection.html', {
        'platforms': platforms,
        'genres': genres
    })


@login_required
def view_collection_by_genre(request, genre_id):
    ''' View games in a collection by a genre '''
    genre = get_object_or_404(models.Genre, pk=genre_id)
    games = request.user.userprofile.games.filter(genres=genre)

    return render(request, 'gmecol/user_collection_by_genre.html', {
        'genre': genre,
        'games': games
    })


@login_required
def view_collection_by_platform(request, platform_id):
    ''' View games in a collection by platform '''
    platform = get_object_or_404(models.Platform, pk=platform_id)
    games = request.user.userprofile.games.filter(platform=platform)

    return render(request, 'gmecol/user_collection_by_platform.html', {
        'platform': platform,
        'games': games
    })

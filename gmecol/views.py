from giantbomb import giantbomb

from django.shortcuts import render
from django.conf import settings
from django.template.defaultfilters import slugify
from django.http import HttpResponseNotFound

import forms, models


def index(request):
    ''' Default landing page '''

    return render(request, 'gmecol/index.html', {})


def search(request):
    ''' Search for games '''

    form = forms.SearchGamesForm(request.GET if request.GET else None)
    games = None
    if form.is_valid():
        gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
        games = gb.search(form.cleaned_data.get('name'))
    return render(request, 'gmecol/search.html', {
        'form': form,
        'games': games,
    })


def game_detail(request, remote_id):
    ''' Game detail view. Grabs the game from our database, otherwise snags it
    from Giant Bomb's API and saves it locally
    '''
    remote_id = int(remote_id)
    games = models.Game.objects.filter(remote_id=remote_id)
    if not games.exists():
        gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
        try:
            g = gb.getGame(remote_id)
        except giantbomb.GiantBombError:
            g = None

        if g is not None:
            game_platforms = models.Platform.objects.filter(
                remote_id__in=[x.id for x in g.platforms]
            )
            for platform in game_platforms:
                game, created = models.Game.objects.get_or_create(
                    platform=platform,
                    remote_id=g.id,
                    slug=slugify('%s-%s' % (g.name, platform.name)),
                    image_url=g.image.icon,
                    name=g.name
                )

        games = models.Game.objects.filter(remote_id=remote_id)

    if not games:
        return HttpResponseNotFound()

    return render(request, 'gmecol/game_detail.html', {
        'games': games
    })

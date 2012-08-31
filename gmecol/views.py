from giantbomb import giantbomb

from django.shortcuts import render
from django.conf import settings
from django.template.defaultfilters import slugify

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
    try:
        game = models.Game.objects.get(remote_id=remote_id)
    except models.Game.DoesNotExist:
        print "exception"
        gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
        g = gb.getGame(remote_id)
        # Cheap async safety with the get_or_create
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
    except models.Game.MultipleObjectsReturned:
        game = models.Game.objects.filter(remote_id=remote_id)[0]

    return render(request, 'gmecol/game_detail.html', {
        'game': game
    })

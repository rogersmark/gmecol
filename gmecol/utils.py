from giantbomb import giantbomb

from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.cache import cache

from gmecol import models


def load_platforms():
    ''' Calls to GiantBomb and loads all of the platforms into the database
    '''
    gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
    offset = 0
    platforms = gb.getPlatforms(offset=offset)
    needs_platforms = True if len(platforms) == 100 else False
    while needs_platforms:
        offset += 100
        platforms.extend(gb.getPlatforms(offset=offset))
        needs_platforms = True if len(platforms) == 100 + offset else False

    for platform in platforms:
        p_form = gb.getPlatform(platform['id'])
        models.Platform.objects.get_or_create(
            name=p_form.name,
            slug=slugify(p_form.name),
            image_url=p_form.image.icon,
            remote_id=p_form.id
        )


def giant_bomb_search(name):
    ''' Checks the cache for the search results from GiantBomb. If we don't
    find anything in the cache, we grab the results and cache it.
    '''
    cache_key = 'search_%s' % slugify(name)
    games = cache.get(cache_key)
    if not games:
        gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
        games = gb.search(name)
        cache.set(cache_key, games, settings.GAME_KEY_EXPIRATION)

    return games


def giant_bomb_game_detail(remote_id):
    ''' Checks the cache and database for the game requested. If we don't find
    what we need we'll go to GiantBomb and fetch it
    '''
    cache_key = 'game_detail_%s' % remote_id
    game = cache.get(cache_key)
    games_count = models.Game.objects.filter(remote_id=remote_id).count()
    if not game:
        gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
        try:
            game = gb.getGame(remote_id)
        except giantbomb.GiantBombError:
            game = None
        cache.set(cache_key, game, settings.GAME_KEY_EXPIRATION)

    if game and len(game.platforms) > games_count:
        game_platforms = models.Platform.objects.filter(
            remote_id__in=[x.id for x in game.platforms]
        )
        for platform in game_platforms:
            new_game, created = models.Game.objects.get_or_create(
                platform=platform,
                remote_id=game.id,
                slug=slugify('%s-%s' % (game.name, platform.name)),
                image_url=game.image.icon,
                name=game.name
            )

    return models.Game.objects.filter(remote_id=remote_id)

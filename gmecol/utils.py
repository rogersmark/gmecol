from datetime import datetime

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
        genres = []
        for genre in game.genres:
            new_genre, created = models.Genre.objects.get_or_create(
                name=genre.get('name'),
                slug=slugify(genre.get('name')),
                remote_id=genre.get('id'),
            )
            genres.append(new_genre)

        game_platforms = models.Platform.objects.filter(
            remote_id__in=[x.get('id') for x in game.platforms]
        )
        for platform in game_platforms:
            release_date = None
            if game.original_release_date:
                release_date = datetime.strptime(
                    game.original_release_date, '%Y-%m-%d %H:%M:%S'
                )
            new_game, created = models.Game.objects.get_or_create(
                deck=game.deck,
                platform=platform,
                remote_id=game.id,
                slug=slugify('%s-%s' % (game.name, platform.name)),
                icon_image_url=game.image.icon if game.image else '',
                med_image_url=game.image.medium if game.image else '',
                screen_image_url=game.image.screen if game.image else '',
                sm_image_url=game.image.small if game.image else '',
                super_image_url=game.image.super if game.image else '',
                thumb_image_url=game.image.thumb if game.image else '',
                tiny_image_url=game.image.tiny if game.image else '',
                name=game.name,
                release_date=release_date,
            )
            [new_game.genres.add(x) for x in genres]

    return models.Game.objects.filter(remote_id=remote_id)

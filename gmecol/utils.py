from giantbomb import giantbomb

from django.conf import settings
from django.template.defaultfilters import slugify

import models


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

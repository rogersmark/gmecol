from giantbomb import giantbomb

from django.shortcuts import render
from django.conf import settings

import forms


def search(request):

    form = forms.SearchGamesForm(request.GET)
    games = None
    if form.is_valid():
        gb = giantbomb.Api(settings.GIANT_BOMB_API_KEY)
        games = gb.search(form.cleaned_data.get('name'))
    return render(request, 'gmecol/search.html', {
        'form': form,
        'games': games,
    })

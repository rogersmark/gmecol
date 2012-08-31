from django import forms

import models


class SearchGamesForm(forms.Form):
    ''' Search the Giant Bomb Games Database for Games '''

    platform = forms.ModelChoiceField(queryset=models.Platform.objects.all())
    name = forms.CharField()

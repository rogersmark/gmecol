from django import forms


class SearchGamesForm(forms.Form):
    ''' Search the Giant Bomb Games Database for Games '''

    name = forms.CharField()

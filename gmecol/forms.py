from django import forms
from django.contrib.auth.models import User

from friends import models as friends

from gmecol import models


class SearchGamesForm(forms.Form):
    ''' Search the Giant Bomb Games Database for Games '''

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'search'}
    ))


class MessageForm(forms.ModelForm):
    ''' Form for sending messages between users '''

    class Meta:
        model = models.Message
        exclude = ('from_user', 'deleted', 'read', )

    def __init__(self, user=None, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['to_user'].queryset = friends.Friendship.objects.friends_of(
                user)


class FriendshipRequestForm(forms.Form):
    ''' Form for requesting friendship of other users '''

    from_user = forms.ModelChoiceField(queryset=User.objects.none())
    to_user = forms.ModelChoiceField(queryset=User.objects.all())
    message = forms.CharField(widget=forms.TextInput)


class CollectionFilterForm(forms.Form):

    genre = forms.ModelChoiceField(
        queryset=models.Genre.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    platform = forms.ModelChoiceField(
        queryset=models.Platform.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, user, wish=False, *args, **kwargs):
        super(CollectionFilterForm, self).__init__(*args, **kwargs)
        self.fields['genre'].queryset = models.Genre.objects.filter(
            pk__in=user.userprofile.usergame_set.filter(wish=wish).values_list(
                'game__genres__pk', flat=True
            )
        )
        self.fields['platform'].queryset = models.Platform.objects.filter(
            pk__in=user.userprofile.usergame_set.filter(wish=wish).values_list(
                'game__platform__pk', flat=True
            )
        )


class CollectionSortForm(forms.Form):

    CHOICES = (
        ('game__name', 'A-Z'),
        ('-game__name', 'Z-A'),
        ('rating', 'Rating')
    )

    sort_by = forms.ChoiceField(
        choices=CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

from django import forms
from django.contrib.auth.models import User

from friends import models as friends

from gmecol import models


class SearchGamesForm(forms.Form):
    ''' Search the Giant Bomb Games Database for Games '''

    name = forms.CharField()


class MessageForm(forms.ModelForm):
    ''' Form for sending messages between users '''

    class Meta:
        model = models.Message
        exclude = ('from_user', 'deleted', 'read', )

    def __init__(self, user, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['to_user'].queryset = friends.Friendship.objects.friends_of(
            user)


class FriendshipRequestForm(forms.Form):
    ''' Form for requesting friendship of other users '''

    from_user = forms.ModelChoiceField(queryset=User.objects.none())
    to_user = forms.ModelChoiceField(queryset=User.objects.all())
    message = forms.CharField(widget=forms.TextInput)

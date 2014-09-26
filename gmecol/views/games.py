from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from gmecol import forms


class GameListView(ListView):

    template_name = 'gmecol/user_collection.html'
    context_object_name = 'games'
    wish = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GameListView, self).dispatch(*args, **kwargs)

    def _populate_form_values(self):
        self.form = forms.CollectionFilterForm(
            user=self.request.user, wish=self.wish, data=self.request.GET
        )
        self.data = {'genre': None, 'platform': None}
        valid_form = self.form.is_valid()
        if valid_form:
            self.data = self.form.cleaned_data

        return valid_form

    def get_queryset(self):
        # Base queryset
        queryset = self.request.user.userprofile.usergame_set.filter(
            wish=self.wish
        )

        if self._populate_form_values():
            self.data = self.form.cleaned_data
            if self.data.get('genre'):
                queryset = queryset.filter(game__genres=self.data['genre'])

            if self.data.get('platform'):
                queryset = queryset.filter(game__platform=self.data['platform'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        self._populate_form_values()
        context.update({
            'form': self.form,
            'wish': self.wish,
            'genre': self.data['genre'],
            'platform': self.data['platform']
        })
        return context

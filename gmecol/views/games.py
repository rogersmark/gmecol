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
        self.filter_form = forms.CollectionFilterForm(
            user=self.request.user, wish=self.wish, data=self.request.GET
        )
        self.sort_form = forms.CollectionSortForm(self.request.GET)
        self.data = {'genre': None, 'platform': None, 'sort': None}
        valid_filter_form = self.filter_form.is_valid()
        valid_sort_form = self.sort_form.is_valid()
        if valid_filter_form:
            self.data = self.filter_form.cleaned_data

        if valid_sort_form:
            self.data.update(self.sort_form.cleaned_data)

        return valid_filter_form or valid_sort_form

    def get_queryset(self):
        # Base queryset
        queryset = self.request.user.userprofile.usergame_set.filter(
            wish=self.wish
        )

        if self._populate_form_values():
            if self.data.get('genre'):
                queryset = queryset.filter(game__genres=self.data['genre'])

            if self.data.get('platform'):
                queryset = queryset.filter(game__platform=self.data['platform'])

            if self.data.get('sort_by'):
                queryset = queryset.order_by(self.data.get('sort_by'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        self._populate_form_values()
        context.update({
            'filter_form': self.filter_form,
            'sort_form': self.sort_form,
            'wish': self.wish,
            'genre': self.data['genre'],
            'platform': self.data['platform']
        })
        return context

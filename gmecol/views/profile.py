import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from gmecol import forms, models


def profile(request, user_id):
    ''' Profile view for a user '''

    user = get_object_or_404(User, pk=user_id)
    games = user.userprofile.games.all()
    return render(request, 'accounts/profile.html', {
        'user': user,
        'platforms': models.Platform.objects.filter(game__in=games).distinct(),
        'games': games,
    })


@login_required
def update_email(request):
    ''' Update email address for user '''
    form = forms.EmailForm()
    response = {'status': 'failed'}
    if request.method == 'POST':
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.save()
            response['status'] = 'success'
            response['email'] = user.email
        else:
            response['errors'] = form.errors
            response['email'] = request.POST.get('id_email')

    return HttpResponse(json.dumps(response), content_type='application/json')

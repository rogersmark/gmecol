from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from friends import models as friends

from gmecol import models


def profile(request, user_id):
    ''' Profile view for a user '''

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'accounts/profile.html', {
        'user': user,
    })

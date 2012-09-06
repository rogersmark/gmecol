from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


def profile(request, user_id):
    ''' Profile view for a user '''

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'accounts/profile.html', {
        'user': user,
    })

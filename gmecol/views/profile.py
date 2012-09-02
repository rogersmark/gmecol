from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from gmecol import forms, models


def profile(request, user_id):
    ''' Profile view for a user '''

    user = get_object_or_404(User, pk=user_id)
    return render(request, 'accounts/profile.html', {
        'user': user,
    })


@login_required
def send_message(request):
    ''' View for sending messages between users '''

    instance = models.Message(from_user=request.user)
    form = forms.MessageForm(instance=instance, user=request.user)
    if request.method == 'POST':
        form = forms.MessageForm(user=request.user, data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # TODO: Redirect to user's inbox
            return redirect('profile', request.user.pk)

    return render(request, 'accounts/send_message.html', {
        'form': form
    })

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from friends.models import FriendshipRequest

from gmecol import forms, models


@login_required
def list_friends(request):
    ''' List all friendships for a user '''

    return render(request, 'gmecol/list_friends.html', {
    })


@login_required
def add_friend(request, friend_pk):
    ''' Makes a friendship request '''
    friend = get_object_or_404(User, pk=friend_pk)
    instance = models.Message(
        from_user=request.user,
        to_user=friend,
        subject='Friendship request from %s' % request.user.username,
        body='Please accept me as your friend!',
    )
    form = forms.MessageForm(instance=instance)
    if request.method == 'POST':
        form = forms.MessageForm(data=request.POST, instance=instance)
        if form.is_valid():
            try:
                existing_relationship = FriendshipRequest.objects.get(
                    to_user=friend
                )
            except FriendshipRequest.DoesNotExist:
                existing_relationship = None
            else:
                existing_relationship.accept()

            if not FriendshipRequest.objects.filter(
                    from_user=request.user, to_user=friend).exists():
                FriendshipRequest.objects.create(
                    from_user=request.user,
                    to_user=friend,
                    message='friends'
                )
                import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
                form.save()
                return redirect(reverse('list-friends'))

    return render(request, 'gmecol/add_friend.html', {
        'form': form,
        'friend': friend,
    })


@login_required
def remove_friend(request, friend_pk):
    ''' Ends a friendship for a user '''

    return render(request, 'gmecol/remove_friend.html', {
    })

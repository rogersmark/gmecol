from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from gmecol import forms, models


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

    return render(request, 'messages/send_message.html', {
        'form': form
    })


@login_required
def message_list(request):
    ''' View a user's inbox '''
    folder = request.GET.get('folder')
    if folder == 'sent':
        messages = models.Message.objects.get_sent(request.user.pk)
    elif folder == 'deleted':
        messages = models.Message.objects.get_deleted(request.user.pk)
    else:
        messages = models.Message.objects.get_messages(request.user.pk)

    return render(request, 'messages/inbox.html', {
        'messages': messages
    })


@login_required
def message_detail(request, message_id):
    ''' View a message '''
    message = get_object_or_404(models.Message,
        Q(from_user=request.user) | Q(to_user=request.user),
        pk=message_id,
    )

    return render(request, 'messages/message_detail.html', {
        'message': message
    })

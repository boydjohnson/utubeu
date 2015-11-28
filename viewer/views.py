from django.shortcuts import render, redirect
from django.template.context import RequestContext

from django.contrib.auth.views import logout as auth_logout

from viewer.models import Chatroom
from viewer.forms import Chatroom_with_InvitedChatroom


def login(request):
        user = request.user
        if user.is_authenticated():
            form = Chatroom_with_InvitedChatroom(request.POST or None) #Here is the form posting
            if form.is_valid():
                form.save(owner=request.user)
            chatrooms = Chatroom.objects.filter(users=user)
        else:
            chatrooms = []
        owned_chatrooms = []
        for c in chatrooms:
            if c.owner == user:
                owned_chatrooms.append(c)
                chatrooms.remove(c)
        context = RequestContext(request, {'user': user, 'owned_chatrooms': owned_chatrooms,
                                           'number_owned': len(owned_chatrooms), 'chatrooms': chatrooms})



        return render(request, 'login.html', context=context)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

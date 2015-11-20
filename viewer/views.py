from django.shortcuts import render, redirect
from django.template.context import RequestContext

from django.contrib.auth.views import logout as auth_logout

from viewer.models import ChatRoom

# Create your views here.


def login(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated():
            chatrooms = ChatRoom.objects.filter(users=user)
        else:
            chatrooms = []
        number_of_owned_chatrooms = 0
        for c in chatrooms:
            if c.owner == user:
                number_of_owned_chatrooms += 1
        context = RequestContext(request, {'user': user, 'number_owned': number_of_owned_chatrooms, 'chatrooms': chatrooms})
        return render(request, 'login.html', context=context)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


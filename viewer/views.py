from django.contrib.auth.views import logout as auth_logout
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

from json import loads, dumps

from viewer.models import Chatroom
from viewer.forms import Chatroom_with_InvitedChatroom

@ensure_csrf_cookie
def login(request):
        user = request.user
        if user.is_authenticated():

            form = Chatroom_with_InvitedChatroom(loads(request.POST[u'data'],'utf-8') if u'data' in request.POST.keys() else None or None) #Here is the form posting
            if form.is_valid():
                print "success"
                form.save(owner=request.user)
                return HttpResponse(dumps({"success": True}), content_type="application/json")
            chatrooms = Chatroom.objects.filter(users=user)
        else:
            chatrooms = []
        owned_chatrooms = []
        chatrooms = list(chatrooms)
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


def create_chatroom(request):
    user = request.user
    if user.is_authenticated():
        form = Chatroom_with_InvitedChatroom(loads(request.POST[u'data'],'utf-8'))
        if form.is_valid():
            chatroom = form.save(owner=request.user)
            return HttpResponse(dumps({"chatroom_id": chatroom.pk, "chatroom_name": chatroom.name}), content_type="application/json")
        else:
            raise ValidationError("Form was malformed.")
    else:
        raise PermissionDenied("User is not authenticated.")


def enter_chatroom(request, chatroom):
    if request.user.is_authenticated() and request.method=='GET':

from django.contrib.auth.views import logout as auth_logout
from django.core.exceptions import PermissionDenied, ValidationError
from django.forms.models import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

from json import loads, dumps

from viewer.models import Chatroom
from viewer.forms import ChatroomForm, EmailForm




def login(request):
        user = request.user
        if user.is_authenticated() and request.method=="GET":
            chatrooms = Chatroom.objects.filter(users=user)
            chatroomForm = ChatroomForm()
            emailFormSet = formset_factory(EmailForm, extra=19, max_num=19, validate_max=True)
            owned_chatrooms = []
            chatrooms = list(chatrooms)
            for c in chatrooms:
                if c.owner == user:
                    owned_chatrooms.append(c)
                    chatrooms.remove(c)

            return render(request, 'login.html', context={'user': user, 'owned_chatrooms': owned_chatrooms,
                                           'number_owned': len(owned_chatrooms), 'chatrooms': chatrooms,
                                                          'email_formset':emailFormSet, 'chatroom_form':chatroomForm})
        else:
            return render(request, 'login.html', context={'user':user})

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

@ensure_csrf_cookie
def create_chatroom(request):
    user = request.user
    if user.is_authenticated() and request.method=="POST":
        chatroomForm = ChatroomForm(request.POST)
        emailFormSet = formset_factory(EmailForm, extra=19, max_num=19, validate_max=True)
        emails = emailFormSet(request.POST)
        if chatroomForm.is_valid() and emails.is_valid():
            chatroom = chatroomForm.save(commit=False)
            chatroom.owner = user
            chatroom.save()
            chatroom.users.add(user)
            chatroom.save()
            for email in emails:
                email.chatroom.add(chatroom)
                email.loggedin = False
                email.save()
            return HttpResponse(dumps({"chatroom_id": chatroom.pk, "chatroom_name": chatroom.name }), content_type="application/json")
        else:
            return HttpResponse(dumps({'errors':[chatroomForm.errors,emailFormSet.errors]}),
                                content_type="application/json")
    else:
        raise PermissionDenied("User is not authenticated.")


def delete_chatroom(request):
    if request.user.is_authenticated() and request.method=="POST":
        chatroom_id = int(request.POST.get('chatroom_id'))
        try:
            cr = Chatroom.objects.filter(owner=request.user).get(pk=chatroom_id)
            cr.delete()
            return HttpResponse(dumps({'success': True}), content_type="application/json")
        except:
            raise PermissionDenied("User is not the owner of that chatroom.")

    else:
        raise PermissionDenied("User is not authenticated")


def enter_chatroom(request, chatroom):
    if request.user.is_authenticated() and request.method=='GET':
        try:
            cr = Chatroom.objects.filter(users=request.user).get(pk=chatroom)
        except:
            raise PermissionDenied("User is not a member of that chatroom.")
        return render(request, 'youtubeviewer.html', context={'chatroom': cr, 'email': request.user.email})

    else:
        raise PermissionDenied("User is not authenticated.")
from django.contrib.auth.views import logout as auth_logout
from django.core.exceptions import PermissionDenied, ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.forms.models import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from json import dumps

from viewer.models import Chatroom, InvitedEmails
from viewer.forms import ChatroomForm, EmailForm


def login(request):
        user = request.user
        if user.is_authenticated() and request.method == "GET":
            chatrooms = Chatroom.objects.filter(users=user)
            invites = InvitedEmails.objects.filter(user_email=user.email).filter(~Q(chatroom__users=user))
            chatroom_form = ChatroomForm()
            emailFormSet = formset_factory(EmailForm, extra=19, max_num=19)
            emailFormSet = emailFormSet()
            owned_chatrooms = chatrooms.filter(owner=user)
            non_owned_chatrooms = chatrooms.filter(~Q(owner=user))
            return render(request, 'login.html', context={'user': user, 'owned_chatrooms': owned_chatrooms,
                            'number_owned': len(owned_chatrooms), 'chatrooms': non_owned_chatrooms, 'invites': invites,
                                            'email_formset': emailFormSet, 'chatroom_form': chatroom_form})
        else:
            return render(request, 'login.html', context={'user': user})

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

@transaction.atomic
@ensure_csrf_cookie
def create_chatroom(request):
    user = request.user
    if user.is_authenticated() and request.method == "POST":
        chatroomForm = ChatroomForm(request.POST, owner=user)
        if chatroomForm.is_valid():
            chatroom = chatroomForm.save()
            chatroom_number = Chatroom.objects.filter(owner=user).count()
            emailFormSet = formset_factory(EmailForm, extra=5, max_num=19)
            emails = emailFormSet(request.POST)
            if emails and emails.is_valid():
                for email in emails:
                    email.save(chatroom=chatroom)
                return HttpResponse(dumps({"chatroom_id": chatroom.pk, "chatroom_name": chatroom.name, "no_more_chatrooms": chatroom_number >=2 }), content_type="application/json")
            else:
                return HttpResponse(dumps({'errors': emailFormSet.errors}),
                                content_type="application/json")
        else:
            return HttpResponse(dumps({'errors': chatroomForm.errors }), content_type="application/json")
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

def join_chatroom(request):
    user= request.user
    if user.is_authenticated() and request.method == "POST":
        try:
            chatroom_id = int(request.POST.get('chatroom_id'))
            chatroom = Chatroom.objects.filter(pk=chatroom_id).filter(emails_from_chatroom__user_email=user.email).get()
            chatroom.users.add(user)
            return HttpResponse(dumps({'chatroom_id': chatroom_id}))
        except KeyError:
            raise ValidationError("POST request wasn't configured correctly")
        except ObjectDoesNotExist:
            raise PermissionDenied("User has not been added to chatroom")

    else:
        raise PermissionDenied("User is not authenticated")


def enter_chatroom(request, chatroom):
    if request.user.is_authenticated() and request.method=='GET':
        try:
            cr = Chatroom.objects.filter(users=request.user).get(pk=chatroom)
        except:
            raise PermissionDenied("User is not a member of that chatroom.")
        return render(request, 'youtubeviewer.html', context={'chatroom': cr, 'user': request.user})

    else:
        raise PermissionDenied("User is not authenticated.")
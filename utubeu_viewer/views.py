from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect


from utubeu_viewer.models import Chatroom


def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.html')
    else:
        raise PermissionDenied("Method not supported.")


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


def enter_chatroom(request, chatroom):
    if request.user.is_authenticated() and request.method=='GET':
        try:
            cr = Chatroom.objects.get(identifier=chatroom)
            if not cr.is_active:
                return redirect(to='/')
            if request.user not in cr.joiners.all():
                cr.joiners.add(request.user)
        except ObjectDoesNotExist:
            raise PermissionDenied("User is not a member of that chatroom.")

        return render(request, 'youtubeviewer.html', context={'chatroom': cr, 'user': request.user})
    else:
        raise PermissionDenied("User is not authenticated.")
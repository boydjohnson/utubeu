from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse


from utubeu_viewer.models import Chatroom, UserSiteInfo

def main_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
             return redirect('viewer:dashboard')
        else:
            return render(request, 'main.html')
    else:
        raise PermissionDenied("Method not supported.")


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


def login_page(request):
    if request.method == 'GET':
        return render(request, "login_screen.html")
    elif request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            chatroom = request.POST.get('next')
            return redirect('viewer:enter_chatroom', chatroom=chatroom)
        else:
            print("USER is none!")
            raise PermissionDenied("User is not authenticated")

@login_required(login_url='viewer:login_page')
def enter_chatroom(request, chatroom):
    if request.user.is_authenticated() and request.method == 'GET':
        try:
            cr = Chatroom.objects.get(identifier=chatroom)

        except ObjectDoesNotExist:
            raise PermissionDenied("User is not a member of that chatroom.")
        if not cr.is_active:
            return redirect(to='/')
        if request.user not in cr.joiners.all():
            cr.joiners.add(request.user)
        if not hasattr(request.user, 'site_info') or \
                        (hasattr(request.user, 'site_info') and not request.user.site_info.has_logged_in):
            return redirect('viewer:splash', chatroom=chatroom)
        return render(request, 'chatroom.html', context={'chatroom': cr, 'user': request.user})
    else:
        raise PermissionDenied("User is not authenticated.")


def get_splash(request, chatroom):
    if request.user.is_authenticated() and request.method == 'GET':
        if not hasattr(request.user, 'site_info'):
            request.user.site_info = UserSiteInfo.objects.create(user=request.user, has_logged_in=True)
        elif hasattr(request.user, 'site_info') and not request.user.site_info.has_logged_in:
            request.user.site_info.has_logged_in = True
            request.user.site_info.save()
        return render(request, 'splash.html', context={'chatroom_id': chatroom})

    raise PermissionDenied("User is not authenticated.")
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from utubeu_viewer.models import Chatroom

@login_required(login_url='viewer:main_page')
def dashboard(request):
    if request.method == 'GET':
        user = request.user
        member_chatrooms = Chatroom.objects.filter(~Q(owner=user.pk), joiners=user.pk)[:8]
        owned_chatrooms = Chatroom.objects.filter(owner=user.pk)[:8]
        public_chatrooms = Chatroom.objects.filter(is_public=True)[:8]
        return render(request, 'utubeu-dash/dash.html', context={'user': user,
                                                                 'owned_chatrooms': owned_chatrooms,
                                                                 'member_chatrooms': member_chatrooms,
                                                                 'public_chatrooms': public_chatrooms})
    else:
        raise PermissionDenied("Method not supported.")
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import Application, AccessToken

from oauthlib.common import generate_token

from social.apps.django_app.utils import psa
from social.backends.google import GoogleOAuth2

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utubeuAPI.serializers import ChatroomSerializer, ChatroomDetailSerializer
from viewer.models import Chatroom, InvitedEmails

from datetime import datetime
from json import dumps
import sys

class OwnedChatroomListCreateView(ListCreateAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)


class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(users=user.pk).exclude(owner=user.pk)


class ChatroomDetailView(RetrieveUpdateAPIView):
    serializer_class = ChatroomDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(Q(owner=user.pk) | Q(users=user.pk))


class JoinableChatroomListView(ListAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return InvitedEmails.objects.get(user_email=user.email).exclude(chatroom__users=user.pk)

@psa('social:complete')
@api_view(['POST'])
def convert_token(request, backend):
    client_id = request.POST.get("client_id")
    client_secret = request.POST.get("client_secret")
    print client_id
    sys.stdout.flush()
    print client_secret
    sys.stdout.flush()
    my_app = get_object_or_404(Application, client_id=client_id, client_secret=client_secret)

    print dir(request)
    sys.stdout.flush()
    user = request.backend.do_auth(request.POST.get("token"))
    if user and user.is_authenticated and user.is_active:
        old_token = AccessToken.objects.filter(user = user)
        if len(old_token)>0:
            return Response(dumps({'access_token':old_token[0].token}), content_type="application/json")
        else:
            my_access_token = AccessToken.objects.create(user=user, token=generate_token(), application=my_app,
                                                         expires=datetime(2020,1,1), scope='create chatrooms')
            return Response(dumps({'access_token':my_access_token.token}), content_type="application/json")
    else:
        raise PermissionDenied("User is not authenticated.")




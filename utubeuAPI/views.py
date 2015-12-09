from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404

from oauth2_provider.models import Application, AccessToken

from oauthlib.common import generate_token

from social.apps.django_app.utils import psa

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utubeuAPI.serializers import ChatroomInSerializer, ChatroomDetailSerializer
from viewer.models import Chatroom, InvitedEmails

from datetime import datetime
from json import dumps

import requests

class OwnedChatroomListCreateView(ListCreateAPIView):

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatroomInSerializer
        else:
            return ChatroomDetailSerializer

class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(users=user.pk).exclude(owner=user.pk)


class ChatroomDetailView(RetrieveUpdateAPIView):
    serializer_class = ChatroomDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(Q(owner=user.pk) | Q(users=user.pk))


class JoinableChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return InvitedEmails.objects.get(user_email=user.email).exclude(chatroom__users=user.pk)

@psa('social:complete')
@api_view(['GET'])
def convert_token(request, backend):
    client_id = request.GET.get("client_id")
    client_secret = request.GET.get("client_secret")

    my_app = get_object_or_404(Application, client_id=client_id, client_secret=client_secret)

    params = dict(code=request.GET.get("token"),
                      client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                      client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                      redirect_uri=settings.SECRET_URI,
                      grant_type="authorization_code")
    response = requests.post("https://www.googleapis.com/oauth2/v3/token", data=params).json()
    user = request.backend.do_auth(response.get("access_token"))
    if user and user.is_authenticated and user.is_active:
        old_token = AccessToken.objects.filter(user = user)
        if len(old_token)>0:
            return Response(dumps({'access_token':old_token[0].token}), content_type="application/json")
        else:
            my_access_token = AccessToken.objects.create(user=user, token=generate_token(), application=my_app,
                                                         expires=datetime(2020,1,1), scope='create chatrooms')
            return Response(dumps({'access_token':my_access_token.token}).encode('utf-8'), content_type="application/json")
    else:
        raise PermissionDenied("User is not authenticated.")




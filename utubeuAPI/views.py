from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404

from oauth2_provider.models import Application, AccessToken
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

from oauthlib.common import generate_token

from social.apps.django_app.utils import psa

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utubeuAPI.serializers import ChatroomInSerializer, ChatroomDetailSerializer, InvitedEmailsSerializer
from viewer.models import Chatroom, InvitedEmails

from datetime import datetime

import requests

class OwnedChatroomListCreateView(ListCreateAPIView):
    """Can list the chatrooms a user owns and create new chatrooms"""
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)

    def get_serializer_class(self):
        return ChatroomInSerializer

class InvitesCreateUpdateView(GenericAPIView, CreateModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = InvitedEmailsSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return InvitedEmails.objects.filter(chatroom__owner=user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        # exclude owned chatrooms so we have a clean break between owned and member chatrooms
        return Chatroom.objects.filter(users=user.pk).exclude(owner=user.pk)


@psa('social:complete')
@api_view(['POST'])
def convert_token(request, backend):
    if request.method == 'POST':
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")

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
                return Response({'access_token':old_token[0].token})
            else:
                my_access_token = AccessToken.objects.create(user=user, token=generate_token(), application=my_app,
                                                             expires=datetime(2020,1,1), scope='create chatrooms')
                return Response({'access_token':my_access_token.token})
        else:
            raise PermissionDenied("User is not authenticated.")
    else:
        raise PermissionError("Method not available")



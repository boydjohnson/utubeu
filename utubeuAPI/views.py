from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from oauth2_provider.models import Application, AccessToken
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication

from oauthlib.common import generate_token



from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utubeuAPI.serializers import ChatroomInSerializer, ChatroomDetailSerializer
from viewer.models import Chatroom

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


class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    authentication_classes = (OAuth2Authentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        # exclude owned chatrooms so we have a clean break between owned and member chatrooms
        return Chatroom.objects.filter(users=user.pk).exclude(owner=user.pk)

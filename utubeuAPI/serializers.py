from rest_framework import serializers

from viewer.models import Chatroom, InvitedEmails

class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description')

class ChatroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description', 'users')


class InvitedEmails(serializers.ModelSerializer):
    class Meta:
        model = InvitedEmails
        fields = '__all__'



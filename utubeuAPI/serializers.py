from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework import exceptions
from viewer.models import Chatroom, InvitedEmails


class ChatroomInSerializer(serializers.ModelSerializer):
    """Tested to correctly make new chatrooms"""
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        owner = self.context.get('request').user
        c = Chatroom(owner=owner, name=validated_data.get('name'),
                        description=validated_data.get('description'))
        c.save()
        c.users.add(owner)
        c.save()
        return c

    def validate(self, attrs):
        owner = self.context.get('request').user
        try:
            Chatroom(owner=owner, **attrs).clean()
        except ValidationError:
            raise exceptions.ValidationError("Only 2 owned chatrooms per user.")
        return attrs


class ChatroomOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description')


class ChatroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description', 'users')

    def update(self, instance, validated_data):
        new_user = validated_data.get('users')
        instance.users.add(new_user)
        instance.save()
        return instance


class InvitedEmailsSerializer(serializers.ModelSerializer):
    """tested to create InvitedEmails for a chatroom"""
    class Meta:
        model = InvitedEmails
        fields = '__all__'


    def validate(self, attrs):
        try:
            InvitedEmails(**attrs).clean()
        except ValidationError:
            raise exceptions.ValidationError("Users can only invite 20 other people into the chatroom.")
        owner = self.context.get('request').user

        chatrooms = owner.owned_chatrooms.filter(id=attrs.get('chatroom').id)
        if len(chatrooms) == 0:
            raise exceptions.PermissionDenied("User must be the owner of chatroom to invite other people.")
        return attrs
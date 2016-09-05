from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework import exceptions
from viewer.models import Chatroom


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
        c.joiners.add(owner)
        c.save()
        return c


class ChatroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description', 'joiners')

    def update(self, instance, validated_data):
        new_users = validated_data.get('joiners', [])
        instance.joiners.add(*new_users)
        instance.save()
        return instance
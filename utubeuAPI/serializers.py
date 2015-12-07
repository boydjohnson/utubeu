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

    def update(self, instance, validated_data):
        new_user = validated_data.get('users')
        instance.users.add(new_user)
        instance.save()
        return instance


class InvitedEmailsSerializer(serializers.ModelSerializer):



    class Meta:
        model = InvitedEmails
        fields = '__all__'



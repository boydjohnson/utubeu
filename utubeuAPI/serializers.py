from rest_framework import serializers
from utubeu_viewer.models import Chatroom


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description', 'identifier')

        extra_kwargs = {
            'identifier': {
                'read_only': True,
            }
        }

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
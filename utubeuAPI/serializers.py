from rest_framework import serializers
from utubeu_viewer.models import Chatroom, UserSiteInfo


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'description', 'web_address', 'is_public', 'max_occupants', 'last_video_thumb',
                  'internal_identifier', 'number_of_joiners', 'facebook_share', 'twitter_share')

        extra_kwargs = {
            'web_address': {
                'read_only': True,
            },
            'internal_identifier': {
                'read_only': True,
            },
            'last_video_thumb': {
                'read_only': True,
            },
            'number_of_joiners': {
                'read_only': True,
            },
            'facebook_share': {
                'read_only': True,
            },
            'twitter_share': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        owner = self.context.get('request').user
        c = Chatroom(owner=owner, **validated_data)
        c.save()
        c.joiners.add(owner)
        c.save()
        return c


class ChatroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'identifier', 'max_occupants', 'description', 'number_of_joiners', 'last_video_thumb',
                  'internal_identifier', 'is_public')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSiteInfo
        fields = ('user', 'has_logged_in', 'madeup_username')
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'has_logged_in': {
                'read_only': True
            }
        }

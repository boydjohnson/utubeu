from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.exceptions import ValidationError

from utubeuAPI.serializers import ChatroomInSerializer


class TestChatroomInSerializerValidation(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')

        class Req:
            def __init__(self, u):
                self.user = u

        self.request = Req(self.user)

    def test_only_2_chatrooms_per_user(self):
        chatroom = ChatroomInSerializer(data={'name': 'test1', 'description': 'test test'},
                                        context={'request': self.request})
        chatroom.is_valid()
        chatroom.save()

        chatroom1 = ChatroomInSerializer(data={'name': 'test2', 'description': 'test test'},
                                         context={'request': self.request})
        chatroom1.is_valid()
        chatroom1.save()

        def too_many_chatrooms():
            chatroom1 = ChatroomInSerializer(data={'name': 'test3', 'description': 'test test'},
                                             context={'request': self.request})
            chatroom1.is_valid(raise_exception=True)

        self.assertRaises(ValidationError, too_many_chatrooms)
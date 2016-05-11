from django.test import TestCase

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utubeuAPI.serializers import ChatroomInSerializer
from viewer.models import Chatroom, InvitedEmails


# dummy class for request

class Req:
    def __init__(self, u):
        self.user = u


class TestChatroomValidation(TestCase):
    """The validation only happens when Forms or Serializers are doing the creating of Chatrooms"""


    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')
        self.request = Req(self.user)

    def test_validate_only_2_chatrooms_per_user(self):
        Chatroom.objects.create(name='testroom', description='test test', owner=self.user)
        Chatroom.objects.create(name='testroom2', description='test test', owner=self.user)


        def make_one_too_many_rooms():
            Chatroom(name='testroom3', description='test test', owner=self.user).clean()
        self.assertRaises(ValidationError, make_one_too_many_rooms)
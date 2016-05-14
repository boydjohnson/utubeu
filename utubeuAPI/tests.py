from django.test import TestCase
from django.contrib.auth.models import User


from rest_framework.exceptions import ValidationError, PermissionDenied

from utubeuAPI.serializers import ChatroomInSerializer, InvitedEmailsSerializer
from viewer.models import Chatroom, InvitedEmails

class TestChatroomInSerializerValidation(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')

        class Req:
            def __init__(self, u):
                self.user = u

        self.request = Req(self.user)

    def test_only_2_chatrooms_per_user(self):
        """
            Tests that only 2 chatrooms can be owned per user
        """
        chatroom1 = ChatroomInSerializer(data={'name': 'test1', 'description': 'test test'},
                                        context={'request': self.request})
        chatroom1.is_valid()
        chatroom1.save()

        chatroom2 = ChatroomInSerializer(data={'name': 'test2', 'description': 'test test'},
                                         context={'request': self.request})
        chatroom2.is_valid()
        chatroom2.save()

        def too_many_chatrooms():
            chatroom3 = ChatroomInSerializer(data={'name': 'test3', 'description': 'test test'},
                                             context={'request': self.request})
            chatroom3.is_valid(raise_exception=True)

        self.assertRaises(ValidationError, too_many_chatrooms)


class TestInvitedEmailsValidator(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')
        self.chatroom = Chatroom.objects.create(name='testroom', description='test test', owner=self.user)

        class Req:
            def __init__(self, u):
                self.user = u

        self.request = Req(self.user)

    def test_too_many_invites(self):
        """test that the user has only invited max 20 people"""

        the_emails = ['testemail'+str(x)+'@test.com' for x in range(20)]
        the_invites = [InvitedEmails.objects.create(user_email=email, loggedin=False,
                                                    chatroom=self.chatroom) for email in the_emails]

        def too_many_emails():
            ieserializer = InvitedEmailsSerializer(data={'user_email': 'test@test.com', 'loggedin': False,
                                                         'chatroom': self.chatroom.id},
                                                   context={'request': self.request})
            ieserializer.is_valid(raise_exception=True)

        self.assertRaises(ValidationError, too_many_emails)

    def test_not_owner_but_inviting(self):
        """test that the user doing the inviting is the owner of the chatroom... tested because it is part of the
        serializer validation logic"""
        other_user = User.objects.create(username='bilbo', password='password')
        other_chatroom = Chatroom.objects.create(name='other chatroom', description='description', owner=other_user)
        email = 'tester@test.com'

        def not_the_owner():
            ieserializer = InvitedEmailsSerializer(data={'user_email': email, 'loggedin': False,
                                                         'chatroom': other_chatroom.pk},
                                                   context={'request': self.request})
            ieserializer.is_valid(raise_exception=True)

        self.assertRaises(PermissionDenied, not_the_owner)
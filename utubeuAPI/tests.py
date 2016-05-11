from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.exceptions import ValidationError

from utubeuAPI.serializers import ChatroomInSerializer, InvitedEmailsSerializer
from viewer.models import Chatroom

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

class TestInvitedEmailsValidator(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')
        self.chatroom = Chatroom.objects.create(name='testroom', description='test test', owner=self.user)
        class Req:
            def __init__(self, u):
                self.user = u

        self.request = Req(self.user)


    def test_too_many_invites(self):
        the_emails = ['testemail'+str(x)+'@test.com' for x in range(20)]
        the_invites = [InvitedEmailsSerializer(data={'user_email':email, 'loggedin': False,
                                                     'chatroom': self.chatroom.id},
                                               context={'request': self.request}) for email in the_emails]
        map(lambda i: i.is_valid(), the_invites)
        map(lambda i: i.save(), the_invites)

        def too_many_emails():
            ieserializer = InvitedEmailsSerializer(data={'user_email': 'test@test.com', 'loggedin': False,
                                                         'chatroom': self.chatroom.id},
                                                   context={'request': self.request})
            ieserializer.is_valid(raise_exception=True)

        self.assertRaises(ValidationError, too_many_emails)


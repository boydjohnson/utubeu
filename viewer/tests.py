from django.test import TestCase

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from viewer.models import Chatroom, InvitedEmails


class TestChatroomValidation(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')

    def test_validate_only_2_chatrooms_per_user(self):
        Chatroom.objects.create(name='testroom', description='test test', owner=self.user)
        Chatroom.objects.create(name='testroom2', description='test test', owner=self.user)


        def make_one_too_many_rooms():
            Chatroom(name='testroom3', description='test test', owner=self.user).clean()
        self.assertRaises(ValidationError, make_one_too_many_rooms)

class TestInvitedEmailValidation(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')
        self.chatroom = Chatroom.objects.create(name='testroom', description='test test', owner=self.user)

    def test_validate_only_20_emails_per_chatroom(self):
        the_emails = ['testemail'+str(x)+'@test.com' for x in range(20)]
        the_invites = [InvitedEmails.objects.create(user_email=email, loggedin=False, chatroom=self.chatroom) for email in the_emails]
        def make_too_many_invites():
            InvitedEmails(user_email='test@test.com', loggedin=False, chatroom=self.chatroom).clean()

        self.assertRaises(ValidationError, make_too_many_invites)
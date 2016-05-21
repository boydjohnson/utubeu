from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.timezone import now

from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.test import APITestCase

from oauth2_provider.models import Application, AccessToken

from oauthlib.common import generate_token

from datetime import timedelta
import json

from utubeuAPI.serializers import ChatroomInSerializer, InvitedEmailsSerializer, ChatroomDetailSerializer
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

    def test_owner_is_initially_added(self):
        chatroom = ChatroomInSerializer(data={'name': 'test', 'description': 'test test'},
                                        context={'request': self.request})
        chatroom.is_valid()
        chatroom.save()
        self.assertIn(self.user, Chatroom.objects.get(id=1).users.all(),
                            "The owner is initially added to the Chatroom.users")

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

class TestChatroomDetailSerializer(TestCase):

    def setUp(self):
        self.a_whole_bunch_of_users = [u.pk for u in [User.objects.create(username='test'+str(i),
                                                           password='password') for i in range(10)]]

        self.user = User.objects.create(username='testtest', password='password')
        self.chatroom = Chatroom.objects.create(name='testroom', description='test test', owner=self.user)

    def test_that_update_of_chatroom_will_add_users(self):
        chat = ChatroomDetailSerializer(instance=self.chatroom, data={'name':'testroom','description': 'test test',
                                                                      'users': self.a_whole_bunch_of_users,
                                                                      'owner': self.user})
        chat.is_valid(raise_exception=True)
        chat.save()
        chatroom = Chatroom.objects.get(id=1)
        for someuser in self.a_whole_bunch_of_users:
            self.assertTrue(someuser in [u.pk for u in chatroom.users.all()], "{} is also in the Chatroom.users".format(someuser))


class TestOwnedChatroomsListCreateViewMobileApp(APITestCase):
    """Testing the view with Bearer Oauth2 spoofed local credentials -- the mobile Android App
        ... will seperately test the convert-token view that returns a local to UtubeU oauth token"""

    def setUp(self):
        self.user = User.objects.create(username='tester', password='password')

        self.application = Application.objects.create(user=self.user, name='testApp', client_id='284058dk30dk',
                                client_secret='20484kfk49kd', client_type=Application.CLIENT_CONFIDENTIAL,
                                  authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS)
        # the access token is what is given at the end of convert-token view
        self.access_token = AccessToken.objects.create(user=self.user, token=generate_token(),
                                                          application=self.application,
                                                          expires=now()+timedelta(weeks=52), scope='chatroom')

    def test_create_an_owned_chatroom(self):
        url = reverse('api:owned_chatrooms')
        resp = self.client.post(path=url, data='{"name": "TestChatroom", "description": "TestChatroom description"}',
                         content_type='application/json',
                                HTTP_AUTHORIZATION='BEARER {}'.format(self.access_token.token))
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(json.loads(resp.content.decode('utf-8')),
                         {"id":1, "name": "TestChatroom", "description": "TestChatroom description"})

    def test_list_owned_chatrooms(self):
        Chatroom.objects.create(owner=self.user, name='some chatroom', description='a chatroom')
        Chatroom.objects.create(owner=self.user, name='some other chatroom', description='a chatroom')

        url = reverse('api:owned_chatrooms')
        resp = self.client.get(path=url, HTTP_AUTHORIZATION='BEARER {}'.format(self.access_token.token))
        self.assertEqual(resp.status_code, 200, "Success on getting the list of chatrooms")
        self.assertEqual(len(json.loads(resp.content.decode('utf-8'))), 2, "There are two chatrooms in the list")


class TestInvitedCreateUpdateView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='tester', password='password')

        self.application = Application.objects.create(user=self.user, name='testApp', client_id='284058dk30dk',
                                client_secret='20484kfk49kd', client_type=Application.CLIENT_CONFIDENTIAL,
                                  authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS)
        # the access token is what is given at the end of convert-token view
        self.access_token = AccessToken.objects.create(user=self.user, token=generate_token(),
                                                          application=self.application,
                                                          expires=now()+timedelta(weeks=52), scope='chatroom')

    def test_all_the_right_options_are_available(self):
        url = reverse('api:invites')
        resp = self.client.options(path=url, HTTP_AUTHORIZATION='BEARER {}'.format(self.access_token.token))

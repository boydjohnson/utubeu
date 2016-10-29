from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from utubeu_viewer.models import Chatroom


class TestAuthFlow(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='test')
        self.user2 = User.objects.create_user(username='testuser2', password='test')


    def test_enter_as_invited_user(self):
        """
        This tests clicking on a link directly to a chatroom. If this is
        first time the user has been at the site they will be taken to a splash
        page to choose a username.

        """
        chatroom = Chatroom.objects.create(name='testroom', owner=self.user1)
        response = self.client.get(path=reverse('viewer:enter_chatroom',
                                                kwargs={'chatroom':chatroom.identifier}))
        self.client.login(**{'username': self.user2.username, 'password': self.user2.password})
        response2 = self.client.post(path=response.url,
                                     data={'username': self.user2.username,
                                           'password': self.user2.password})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.url, reverse('viewer:enter_chatroom',
                                                kwargs={'chatroom': chatroom.identifier}))

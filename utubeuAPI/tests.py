from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from utubeuAPI.serializers import ChatroomSerializer, ChatroomDetailSerializer
from utubeu_viewer.models import Chatroom

class TestSerializers(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testtest', password='password')
        self.a_whole_bunch_of_users = [u.pk for u in [User.objects.create(username='test'+str(i),
                                                           password='password') for i in range(10)]]
        self.chatroom = Chatroom.objects.create(name='testroom', description='test test', owner=self.user)
        # this class is a mock of the request context
        class Req:
            def __init__(self, u):
                self.user = u

        self.request = Req(self.user)


    def test_owner_is_initially_added(self):
        chatroom = ChatroomSerializer(data={'name': 'test', 'description': 'test test'},
                                      context={'request': self.request})
        chatroom.is_valid()
        c = chatroom.save()
        self.assertIn(self.user, Chatroom.objects.get(id=c.pk).joiners.all(),
                            "The owner is initially added to the Chatroom.joiners")

    def test_that_update_of_chatroom_will_add_users(self):
        chat = ChatroomDetailSerializer(instance=self.chatroom, data={'name':'testroom','description': 'test test',
                                                                      'joiners': self.a_whole_bunch_of_users,
                                                                      'owner': self.user})
        chat.is_valid(raise_exception=True)
        c = chat.save()
        chatroom = Chatroom.objects.get(id=c.pk)
        for someuser in self.a_whole_bunch_of_users:
            self.assertTrue(someuser in [u.pk for u in chatroom.joiners.all()], "{} is also in the Chatroom.users".format(someuser))

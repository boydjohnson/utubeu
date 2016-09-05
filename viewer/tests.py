from django.test import TestCase

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from viewer.models import Chatroom

from datetime import timedelta

class TestChatroomValidation(TestCase):

    def setUp(self):
        self.owner = User.objects.create(username='testtest', password='password')

    def testduration(self):
        """duration has granularity down to 1 second"""
        chatroom_ok = Chatroom(name="testtest", description="testtest",
                               owner=self.owner)

        with self.assertRaises(ValidationError):
            Chatroom(name="testtest", description="testtest",
                     owner=self.owner,
                     duration=timedelta(days=1).total_seconds() + timedelta(seconds=1).total_seconds())

        with self.assertRaises(ValidationError):
            Chatroom(name='testtest', description='testtest',
                     owner=self.owner,
                     duration=timedelta(minutes=10).total_seconds() - timedelta(seconds=1).total_seconds())
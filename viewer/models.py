from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import uuid


def only_two_chatrooms_per_user(obj):
    model = obj.__class__
    if model.objects.filter(owner=obj.owner) >= 2:
        raise ValidationError("Can only create 2 %s instances per user" % model.__name__)




class ChatRoom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    uuid = models.UUIDField(verbose_name='chatroom_uuid', null=False, default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(User, related_name='chatroom_from_owner', null=False)
    users = models.ManyToManyField(User, related_name='chatroom_from_users', null=False)



    def __unicode__(self):
        return self.name + " " + self.owner.username


    def clean(self):
        only_two_chatrooms_per_user(self)
        super(self, ChatRoom).clean()
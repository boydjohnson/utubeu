from django.db import models

from django.contrib.auth.models import User

import uuid


class ChatRoom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    uuid = models.UUIDField(verbose_name='chatroom_uuid', null=False, default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(User, related_name='chatroom_from_owner', null=False)
    users = models.ManyToManyField(User, related_name='chatroom_from_users', null=False)
    type = models.IntegerField(editable=False, null=False)


    def __unicode__(self):
        return self.name + " " + self.owner.username


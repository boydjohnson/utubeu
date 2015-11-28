from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import F


def only_two_chatrooms_per_user(obj):
    model = obj.__class__
    if model.objects.filter(owner=obj.owner) >= 2:
        raise ValidationError("Can only create 2 %s instances per user" % model.__name__)


class Chatroom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(to=User, related_name='chatroom_from_owner', null=False)

    users = models.ManyToManyField(to=User, related_name='chatroom_from_users', null=False)
    user_emails = models.ManyToManyField(to='InvitedChatroom', related_name='chatroom_from_emails')

    room_number = models.IntegerField(default=0)


    class Meta:
        unique_together = ('owner', 'room_number')

    def __unicode__(self):
        return self.name + " " + self.owner.username

    def clean(self):
        only_two_chatrooms_per_user(self)
        super(self, Chatroom).clean()


class InvitedChatroom(models.Model):
    chatroom = models.OneToOneField(to='Chatroom', related_name='invited_room')
    user_email = models.EmailField()
    number_in = models.IntegerField(default=0)
    loggedin = models.BooleanField(default=False, null=False)


    def __unicode__(self):
        return self.chatroom.name + " " + self.user_email

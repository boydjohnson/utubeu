from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



def only_two_chatrooms_per_user(obj):
    model = obj.__class__
    if model.objects.filter(owner=obj.owner) >= 2:
        raise ValidationError("Can only create 2 %s instances per user" % model.__name__)


def only_20_emails_per_chatroom(obj):
    model = obj.__class__
    if model.objects.filter(chatroom=obj.chatroom)>=20:
        raise ValidationError("Can only have 20 %s instances per chatroom" % model.__name__)


class Chatroom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(to=User, related_name='chatroom_from_owner', null=False)

    users = models.ManyToManyField(to=User, related_name='chatroom_from_users', null=False)


    def __unicode__(self):
        return self.name + " " + self.owner.username

    def clean(self):
        only_two_chatrooms_per_user(self)
        super(Chatroom, self).clean()


class InvitedEmails(models.Model):
    user_email = models.EmailField()
    loggedin = models.BooleanField(default=False, null=False)
    chatroom = models.ForeignKey('Chatroom', related_name='emails_from_chatroom')

    def __unicode__(self):
        return self.user_email + self.chatroom.name

    def clean(self):
        only_20_emails_per_chatroom(self)
        super(InvitedEmails, self).clean()
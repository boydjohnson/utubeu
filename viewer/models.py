from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Chatroom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(to=User, related_name='chatrooms', null=False)

    users = models.ManyToManyField(to=User, related_name='chatrooms')

    def only_two_chatrooms_per_user(self):
        model = self.__class__
        if model.objects.filter(owner=self.owner) >= 2:
            raise ValidationError("Can only create 2 %s instances per user" % model.__name__)


    def __unicode__(self):
        return self.name + " " + self.owner.username

    def clean(self):
        self.only_two_chatrooms_per_user()
        super(Chatroom, self).clean()


class InvitedEmails(models.Model):
    user_email = models.EmailField()
    loggedin = models.BooleanField(default=False, null=False)
    chatroom = models.ForeignKey('Chatroom', related_name='invited_emails')

    def __unicode__(self):
        return self.user_email + self.chatroom.name

    def only_20_emails_per_chatroom(self):
        model = self.__class__
        if model.objects.filter(chatroom=self.chatroom)>=20:
            raise ValidationError("Can only have 20 %s instances per chatroom" % model.__name__)

    def clean(self):
        self.only_20_emails_per_chatroom()
        super().clean()
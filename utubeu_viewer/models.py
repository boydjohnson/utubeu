from django.db import models


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

import random
import string
from datetime import timedelta


def generate_id_string():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    num_chars = random.randint(34, 38)
    return get_random_string(length=num_chars,
                             allowed_chars=chars
                             )


def validate_duration(dur):
        if timedelta(seconds=dur) < timedelta(minutes=10):
            raise ValidationError("Chatroom duration must be greater than 10 minutes")
        elif timedelta(seconds=dur) > timedelta(days=3):
            raise ValidationError("Chatroom duration must be less than 1 day")


class Chatroom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    identifier = models.CharField(max_length=38, default=generate_id_string)

    owner = models.ForeignKey(to=User, related_name='owned_chatrooms', null=False)
    joiners = models.ManyToManyField(to=User, related_name='joined_chatrooms')

    is_public = models.BooleanField(default=False)
    max_occupants = models.IntegerField(default=20, verbose_name="The maximum number of joiners")
    duration = models.BigIntegerField(default=45*60)
    is_active = models.BooleanField(default=True)
    start = models.DateTimeField(auto_now=True, verbose_name="When the user added the chatroom")

    def __str__(self):
        return self.name + ":" + self.owner.username + ":Active:" + str(self.is_active)


class UserSiteInfo(models.Model):
    user = models.OneToOneField(to=User, related_name='site_info', null=False)
    has_logged_in = models.BooleanField(default=False)

    def __str__(self):
        if self.has_logged_in:
            return "{} has logged in".format(str(self.user))
        return "{} has not logged in".format(str(self.user))

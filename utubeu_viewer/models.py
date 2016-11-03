from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from datetime import timedelta


def string_is_integer(value):
    """only evaluates to true when the value is a str that contains only numbers"""
    if isinstance(value, str):
        try:
            int(value)
            return True
        except ValueError:
            return False
    return False


def validate_duration(dur):
        if timedelta(seconds=dur) < timedelta(minutes=10):
            raise ValidationError("Chatroom duration must be greater than 10 minutes")
        elif timedelta(seconds=dur) > timedelta(days=3):
            raise ValidationError("Chatroom duration must be less than 1 day")


class Chatroom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True)
    identifier = models.CharField(max_length=38, blank=True, null=False)

    owner = models.ForeignKey(to=User, related_name='owned_chatrooms', null=False)
    joiners = models.ManyToManyField(to=User, related_name='joined_chatrooms')

    is_public = models.BooleanField(default=False)
    max_occupants = models.IntegerField(default=20, verbose_name="The maximum number of joiners")
    duration = models.BigIntegerField(default=45*60)
    is_active = models.BooleanField(default=True)
    start = models.DateTimeField(auto_now=True, verbose_name="When the user added the chatroom")

    def __str__(self):
        return self.name + ":" + self.owner.username + ":Active:" + str(self.is_active)

    def number_of_joiners(self):
        return self.joiners.count()

    def save(self, *args, **kwargs):
        urlified_name = self.name.replace(" ", "-")

        other_chatrooms = Chatroom.objects.filter(identifier__contains=urlified_name).values_list('identifier')

        if self.pk is None:
            other_identifiers = map(lambda x: x[0], other_chatrooms)
            other_identifiers = list(filter(lambda x: string_is_integer(x.split('-')[-1]), other_identifiers))
            if len(other_identifiers) > 0:
                largest_value = max(other_identifiers, key=lambda x: x.split('-')[-1]).split('-')[-1]
                others_number = int(largest_value)
                urlified_name += "-" + str(others_number + 1)
            elif len(other_chatrooms) > 0:
                urlified_name += "-" + str(1)
            print(urlified_name)
            self.identifier = urlified_name
        super(Chatroom, self).save(*args, **kwargs)


class UserSiteInfo(models.Model):
    user = models.OneToOneField(to=User, related_name='site_info', null=False)
    has_logged_in = models.BooleanField(default=False)
    madeup_username = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        if self.has_logged_in:
            return "{} has logged in".format(str(self.user))
        return "{} has not logged in".format(str(self.user))

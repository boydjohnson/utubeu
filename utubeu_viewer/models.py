from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.http import urlquote_plus

import re
import random
import string

from socialConfig import facebook_app_id
from socialConfig import utubeu_web_address


def string_is_integer(value):
    """only evaluates to true when the value is a str that contains only numbers"""
    if isinstance(value, str):
        try:
            int(value)
            return True
        except ValueError:
            return False
    return False


def generate_id_string():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    num_chars = random.randint(34, 38)
    return get_random_string(length=num_chars,
                             allowed_chars=chars
)

class Chatroom(models.Model):
    name = models.TextField(verbose_name='Chatroom Name', max_length=50, blank=False, null=False)
    description = models.TextField(blank=True, null=True, max_length=50)

    identifier = models.TextField(blank=True, null=False)
    internal_identifier = models.CharField(max_length=38, default=generate_id_string)

    owner = models.ForeignKey(to=User, related_name='owned_chatrooms', null=False)
    joiners = models.ManyToManyField(to=User, related_name='joined_chatrooms')

    is_public = models.BooleanField(default=False)
    max_occupants = models.IntegerField(default=20, verbose_name="The maximum number of joiners")
    duration = models.BigIntegerField(default=45*60)
    is_active = models.BooleanField(default=True)
    start = models.DateTimeField(auto_now=True, verbose_name="When the user added the chatroom")

    last_video_thumb = models.TextField(verbose_name="The thumbnail url of the last video played.",
                                        blank=True, null=True)

    def web_address(self):
        return "{base}/chatroom/{identifier}".format(base=utubeu_web_address,
                                                            identifier=self.identifier)

    def facebook_share(self):
        web_address = self.web_address()
        return_address = "{base}/dashboard".format(base=utubeu_web_address)
        return "https://www.facebook.com/dialog/share?app_id={app_id}" \
               "&display=page&href={url}&redirect_uri={redirect_url}".format(app_id=facebook_app_id,
                                                                             url=urlquote_plus(web_address),
                                                                             redirect_url=urlquote_plus(return_address))

    def twitter_share(self):
        return "https://twitter.com/intent/tweet?url={url}" \
               "&text={title}".format(url=urlquote_plus(self.web_address()), title=urlquote_plus(self.name))

    def __str__(self):
        return self.name + ":" + self.owner.username + ":Active:" + str(self.is_active)

    def number_of_joiners(self):
        return self.joiners.count()

    def save(self, *args, **kwargs):
        urlified_name = self.name.lower().replace(" ", "-")

        other_chatrooms = Chatroom.objects.filter(identifier__contains=urlified_name).values_list('identifier')

        if self.pk is None:
            other_identifiers = map(lambda x: x[0], other_chatrooms)
            if urlified_name in other_identifiers:
                regex = re.compile(urlified_name + '-[0-9]{0,}$')
                other_ending_numbers = set()
                for other in other_identifiers:
                    if regex.match(other) is not None:
                        if string_is_integer(other.split('-')[-1]):
                            other_ending_numbers.add(int(other.split('-')[-1]))
                maximum = max(other_ending_numbers) if len(other_ending_numbers) != 0 else 2
                nums_not_in_set = set(range(1, maximum)) - other_ending_numbers
                if len(nums_not_in_set) == 0:
                    self.identifier = urlified_name + "-{}".format(maximum + 1)
                else:
                    self.identifier = urlified_name + "-{}".format(min(nums_not_in_set))
            else:
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

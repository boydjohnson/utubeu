from django import forms
from django.db import transaction

from viewer.models import Chatroom, InvitedChatroom

import sys

class EmailMultiField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.EmailField() for f in kwargs.pop('emailsFromForm'))
        super(EmailMultiField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        return data_list


class Chatroom_with_InvitedChatroom(forms.Form):
    """This Form is used when a user first makes a Chatroom
    and there will be at least one InvitedChatroom user_email from the owner"""
    chatroom_name=forms.CharField()
    chatroom_description = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(Chatroom_with_InvitedChatroom, self).__init__(*args, **kwargs)
        emails = args[0].pop('user_emails') if 'user_emails' in args[0].keys() else []
        self.fields['user_emails'] = EmailMultiField(emailsFromForm=emails)



    @transaction.atomic
    def save(self, owner):
        cr_name = self.cleaned_data.get('chatroom_name')
        cr_description = self.cleaned_data.get('chatroom_description')

        cr = Chatroom(name=cr_name, description=cr_description, owner=owner)
        cr.save()
        cr.users.add(owner)

        ivcr = InvitedChatroom(chatroom=cr, user_email=owner.email, number_in=0, loggedin=True)
        ivcr.save()

        emails = set(self.cleaned_data.get('user_emails', []))

        if len(emails)>19:
            emails = emails[:19]
        invited_chatrooms = []
        for i,email in enumerate(emails):
            invited_chatrooms.append(InvitedChatroom(chatroom=cr, user_email=email, number_in=i+1, loggedin=False))
        InvitedChatroom.objects.bulk_create(invited_chatrooms)
        return cr

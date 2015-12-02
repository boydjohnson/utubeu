from django import forms

from viewer.models import Chatroom, InvitedEmails




class ChatroomForm(forms.ModelForm):
    """This is a model form for creating the chatroom"""
    name = forms.CharField()

    class Meta:
        model= Chatroom
        fields = ['name', 'description']

class EmailForm(forms.ModelForm):
    """This is the modelform to be used with formset_factory to make all of the email forms"""
    class Meta:
        model=InvitedEmails
        fields = ['user_email']



from django import forms

from utubeu_viewer.models import Chatroom, InvitedEmails




class ChatroomForm(forms.ModelForm):
    """This is a model form for creating the chatroom"""
    name = forms.CharField()

    class Meta:
        model= Chatroom
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super(ChatroomForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        chatroom = super(ChatroomForm, self).save(commit=False)
        chatroom.owner = self.owner
        chatroom.save(commit)
        chatroom.users.add(self.owner)
        return chatroom

class EmailForm(forms.ModelForm):
    """This is the modelform to be used with formset_factory to make all of the email forms"""
    class Meta:
        model=InvitedEmails
        fields = ['user_email']

    def save(self, commit=True, *args, **kwargs):
        chatroom = kwargs.get('chatroom')
        email = super(EmailForm, self).save(commit=False)
        email.chatroom = chatroom
        email.loggedin = False
        email.save(commit)
        return email

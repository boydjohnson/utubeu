from django import forms

from viewer.models import Chatroom, InvitedEmails




class ChatroomForm(forms.ModelForm):
    """This is a model form for creating the chatroom"""
    name = forms.CharField()

    class Meta:
        model= Chatroom
        fields = ['name', 'description']

    def save(self, commit=True, *args,**kwargs):
        instance = super(ChatroomForm, self).save(commit=False)
        owner = kwargs.pop('owner')
        instance.owner= owner
        instance.users.add(owner)
        instance.save(commit=commit)
        return instance

class EmailForm(forms.ModelForm):
    """This is the modelform to be used with formset_factory to make all of the email forms"""
    class Meta:
        model=InvitedEmails
        fields = ['user_email']

    def save(self, commit=True, *args, **kwargs):
        instance = super(EmailForm, self).save(commit=False)
        chatroom = kwargs.pop('chatroom')
        instance.chatroom = chatroom
        if self.user_email==chatroom.owner.email:
            instance.loggedin=True
        else:
            instance.loggedin=False
        instance.save(commit=commit)
        return instance

from django.db.models import ObjectDoesNotExist

from channels.generic.websockets import JsonWebsocketConsumer
from channels.channel import Channel, Group

from utubeu_viewer.models import Chatroom

import json


class ChatroomConsumer(JsonWebsocketConsumer):

    action_map = {
        'ChatMess': 'ChatMess',
        'Sugg': 'Sugg',
        'VoteSugg': 'VoteSugg',
        'VoteCurrent': 'VoteCurrent'
    }

    http_user = True

    def connect(self, message, **kwargs):
        if 'chatroom' not in kwargs:
            return
        try:
            cr = Chatroom.objects.get(internal_identifier=kwargs['chatroom'])
            if self.message.user not in cr.joiners.all():
                return
        except ObjectDoesNotExist:
            return
        Group(kwargs['chatroom']).add(self.message.reply_channel)

    def receive(self, content, **kwargs):
        if 'chatroom' not in kwargs:
            return
        if 'chatroom' not in content:
            return
        if kwargs['chatroom'] != content['chatroom']:
            return
        if 'action' not in content:
            return
        if content['action'] not in self.action_map:
            return
        results = {k:v for k,v in content.items()}
        Channel(self.action_map[content['action']]).send(results)

    def disconnect(self, message, **kwargs):
        if 'chatroom' in kwargs:
            Group(kwargs['chatroom']).discard(self.message.reply_channel)


def chat_message_consumer(message):
    if 'user' not in message.content:
        return
    chatroom = message.content['chatroom']
    del message.content['chatroom']
    Group(chatroom[0:10]).send({'text': json.dumps(message.content)})


def suggestion_consumer(message):

    chatroom = message.content['chatroom']
    del message.content['chatroom']
    Group(chatroom[0:10]).send({'text': json.dumps(message.content)})


def vote_sugg_consumer(message):
   chatroom = message.content['chatroom']
   del message.content['chatroom']
   del message.content['direction']
   m = {'start': 1, 'action': 'Start', 'youtube_value': message.content['youtube_value']}
   Group(chatroom[0:10]).send({'text': json.dumps(m)})

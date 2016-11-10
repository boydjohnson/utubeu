from django.db.models import ObjectDoesNotExist

from channels.generic.websockets import JsonWebsocketConsumer
from channels.channel import Channel, Group

from utubeu_viewer.models import Chatroom

import json

import redis


class ChatroomConsumer(JsonWebsocketConsumer):

    action_map = {
        'ChatMess': 'ChatMess',
        'Sugg': 'Sugg',
        'VoteSugg': 'VoteSugg',
        'VoteCurrent': 'VoteCurrent'
    }

    http_user = True
    strict_ordering = True

    def connect(self, message, **kwargs):
        try:
            cr = Chatroom.objects.get(internal_identifier=kwargs['chatroom'])
            if self.message.user not in cr.joiners.all():
                return
        except ObjectDoesNotExist:
            return
        Group(kwargs['chatroom']).add(self.message.reply_channel)
        r = redis.StrictRedis(host='localhost', port=6379)
        if r.exists(kwargs['chatroom'] + ":lastten"):
            last_ten_messages = [m.decode('UTF-8') for m in r.lrange(kwargs['chatroom'] + ":lastten", 0, 10)]
            self.message.reply_channel.send({"text": json.dumps(last_ten_messages)})



    def receive(self, content, **kwargs):
        if 'chatroom' not in kwargs:
            return
        if 'action' not in content:
            return
        if content['action'] not in self.action_map:
            return
        results = {k:v for k,v in content.items()}
        results['chatroom'] = kwargs['chatroom']
        results['user'] = self.message.user.site_info.madeup_username
        Channel(self.action_map[content['action']]).send(results)

    def disconnect(self, message, **kwargs):
        if 'chatroom' in kwargs:
            Group(kwargs['chatroom']).discard(self.message.reply_channel)


def chat_message_consumer(message):
    chatroom = message.content['chatroom']
    if 'text' not in message.content:
        return
    msg = {
        'user': message.content['user'],
        'text': message.content['text']
    }
    Group(chatroom).send({'text': json.dumps(msg)})
    r = redis.StrictRedis(host='localhost', port=6379)
    redis_pipeline = r.pipeline()
    redis_pipeline.lpush(chatroom + ":lastten", {'user': message.content['user'],
                                                            'text': message.content['text']})
    redis_pipeline.ltrim(chatroom + ":lastten", 0, 10)
    redis_pipeline.execute()


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

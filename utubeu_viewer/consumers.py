from channels.generic.websockets import JsonWebsocketConsumer
from channels.channel import Channel, Group

import json


class ChatroomConsumer(JsonWebsocketConsumer):

    action_map = {
        'ChatMess': 'ChatMess',
        'Sugg': 'Sugg',
        'VoteSugg': 'VoteSugg',
        'VotePlaylist': 'VotePlaylist',
        'VoteCurrent': 'VoteCurrent'
    }

    def connect(self, message, **kwargs):
        if 'chatroom' not in kwargs:
            return
        Group(kwargs['chatroom'][0:10]).add(self.message.reply_channel)

    def receive(self, content, **kwargs):
        if 'chatroom' not in kwargs:
            return
            # print(self.message.reply_channel)
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

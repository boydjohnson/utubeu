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
        msg = {}
        if r.exists(kwargs['chatroom'] + ":lastten"):
            last_ten_messages = [json.loads(m.decode('UTF-8')) for m in r.lrange(kwargs['chatroom'] + ":lastten", 0, 10)]
            msg['last_ten'] = last_ten_messages

        all_suggestions_key = kwargs['chatroom'] + ":all:suggestions"
        if r.exists(all_suggestions_key):
            videos =[json.loads(v.decode('UTF-8')) for v in r.lrange(all_suggestions_key, 0, r.llen(all_suggestions_key))]
            msg['suggestions'] = videos
        r.lpush(kwargs['chatroom'] + ":users", self.message.user.site_info.madeup_username or 'AnonymousUser')
        msg['users'] = [u.decode('UTF-8') for u in r.lrange(kwargs['chatroom'] + ":users", 0, -1)]
        self.message.reply_channel.send({'text': json.dumps(msg)})

    def receive(self, content, **kwargs):
        if 'chatroom' not in kwargs:
            return
        if 'action' not in content:
            return
        if content['action'] not in self.action_map:
            return
        results = {k:v for k,v in content.items()}
        results['chatroom'] = kwargs['chatroom']
        results['user'] = self.message.user.site_info.madeup_username or 'AnonymousUser'
        Channel(self.action_map[content['action']]).send(results)

    def disconnect(self, message, **kwargs):
        if 'chatroom' in kwargs:
            Group(kwargs['chatroom']).discard(self.message.reply_channel)
        r = redis.StrictRedis(host='localhost', port=6379)
        r.lrem(kwargs['chatroom'] + ":users", 1, self.message.user.site_info.madeup_username or 'AnonymousUser')


def chat_message_consumer(message):
    """
    Stores the :lastten messages, and sends the ChatMess out to the chatroom
    """
    chatroom = message.content['chatroom']
    if 'text' not in message.content:
        return
    msg = {
        'user': message.content['user'],
        'text': message.content['text'],
        'action': 'ChatMess'
    }
    Group(chatroom).send({'text': json.dumps(msg)})
    r = redis.StrictRedis(host='localhost', port=6379)
    redis_pipeline = r.pipeline()
    redis_pipeline.lpush(chatroom + ":lastten", json.dumps({'user': message.content['user'],
                                                 'text': message.content['text']}))
    redis_pipeline.ltrim(chatroom + ":lastten", 0, 10)
    redis_pipeline.execute()


def suggestion_consumer(message):
    """
    Sugset enforces that a video can only be add once,
    :all:suggestions keeps the video information
    """
    if 'video_id' not in message.content:
        return
    if 'imageurl' not in message.content:
        return
    if 'title' not in message.content:
        return
    if 'description' not in message.content:
        return
    video_id = message.content['video_id']
    chatroom = message.content['chatroom']
    imageurl = message.content['imageurl']
    r = redis.StrictRedis(host='localhost', port=6379)
    if not r.sismember(chatroom + ":sugset", message.content['video_id']):
        r.sadd(chatroom + ":sugset", video_id)
    else:
        return
    # used for on_connect sending out the suggestions
    video_info = {"video_id": video_id, "imageurl": imageurl,
                  "title": message.content['title'],
                  "description": message.content['description']}
    r.lpush(chatroom + ":all:suggestions", json.dumps(video_info))
    r.hmset(chatroom + ":" + video_id, video_info)
    msg = {
        'video_id': video_id,
        'title': message.content['title'],
        'description': message.content['description'],
        'imageurl': imageurl,
        'action': 'Sugg'
    }
    Group(chatroom).send({'text': json.dumps(msg)})


def vote_sugg_consumer(message):
    chatroom = message.content['chatroom']
    if 'video_id' not in message.content:
        return
    video_id = message.content['video_id']
    if 'vote_up' not in message.content:
        return
    vote_up = bool(message.content['vote_up'])
    r = redis.StrictRedis(host='localhost', port=6379)
    video_votes_key = chatroom + ":" + video_id + ":" + "votes"
    if vote_up is True:
        r.hsetnx(video_votes_key, 'up', 1)
        r.hincrby(video_votes_key, 'up', 1)
    elif vote_up is not True:
        r.hsetnx(video_votes_key, 'down', 1)
        r.hincrby(video_votes_key, 'down', 1)
    v = r.hgetall(video_votes_key)
    votes = {str(k, 'UTF-8'): int(str(v, 'UTF-8')) for k,v in r.hgetall(video_votes_key).items() }
    num_users = r.llen(chatroom + ":users")
    num_up = votes['up'] if 'up' in votes else 0
    num_down = votes['down'] if 'down' in votes else 0
    if float(num_up) / float(num_users) > 0.4:
        start_msg = {str(k, 'UTF-8'): str(v, 'UTF-8') for k, v in r.hgetall(chatroom + ":" + video_id).items() }
        start_msg['action'] = 'start'
        Group(chatroom).send({'text': json.dumps(start_msg)})

    elif float(num_down) / float(num_users) > 0.4:
        down_msg = {str(k, 'UTF-8'): str(v, 'UTF-8') for k, v in r.hgetall(chatroom + ":" + video_id).items() }
        pipeline = r.pipeline(transaction=False)
        pipeline.delete(chatroom + ":" + video_id).srem(chatroom + ":sugset", video_id)
        pipeline.execute()
        down_msg['action'] = 'down'
        Group(chatroom).send({'text': json.dumps(down_msg)})
    else:
        msg = {
            'video_id': video_id,
            'action': 'VoteSugg',
            'up': num_up,
            'down': num_down
        }
        Group(chatroom).send({'text': json.dumps(msg)})

from channels.generic.websockets import JsonWebsocketConsumer


class ChatroomConsumer(JsonWebsocketConsumer):

    def receive(self, content, **kwargs):
        if 'chatroom' not in kwargs:
            return
        if kwargs['chatroom'] != content['chatroom']:
            return
        print(content)
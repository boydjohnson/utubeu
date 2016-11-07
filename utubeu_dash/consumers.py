from channels.generic.websockets import JsonWebsocketConsumer
from channels.channel import Group

from utubeu_viewer.models import Chatroom


class DashboardConsumer(JsonWebsocketConsumer):

    http_user = True

    def connect(self, message, **kwargs):
        chatrooms = Chatroom.objects.filter(joiners=self.message.user).values_list('internal_identifier')
        for identifier in chatrooms:
            Group(identifier[0] + ":listeners").add(self.message.reply_channel)

    def disconnect(self, message, **kwargs):
        chatrooms = Chatroom.objects.filter(joiners=self.message.user).values_list('internal_identifier')
        for identifier in chatrooms:
            Group(identifier[0] + ':listeners').discard(self.message.reply_channel)
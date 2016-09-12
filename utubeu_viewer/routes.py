from channels.routing import route_class

from utubeu_viewer.consumers import ChatroomConsumer

channel_route = [
    route_class(ChatroomConsumer, path=r'^/chat/(?P<chatroom>[A-Za-z0-9]{30,40})$')
]
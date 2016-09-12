from channels.generic.websockets import WebsocketDemultiplexer


class ChatroomConsumer(WebsocketDemultiplexer):

    mapping = {
        'message': message_consumer,
    }


def message_consumer(message):
    print(message)
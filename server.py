from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utubeu.settings")

from whitenoise.django import DjangoWhiteNoise


from django.core.wsgi import get_wsgi_application
from json import dumps


class ChatroomUser:
    def __init__(self, youtubewebsocketsuser, useremail, chatroom_id):
        self.user = youtubewebsocketsuser
        self.email = useremail
        self.chatroom_id = chatroom_id




class YouTubeWebSockets(WebSocketServerProtocol):

    def onConnect(self, request):
        self.factory.users.append(self)

    def onMessage(self, payload, isBinary):
        JSON = {'screen':{'count':len(self.factory.users)}}
        if not isBinary:
            JSON['msg'] = payload.decode('utf-8')
            for s in self.factory.users:
                s.sendMessage(dumps(JSON).encode('utf-8'))



class SeparateServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug=False, debugCodePaths=False):
        super(SeparateServerFactory, self).__init__(url, debug, debugCodePaths)
        self.users = []




if __name__ == '__main__':

    factory = SeparateServerFactory("ws://utubeu.herokuapp.com/receiver", debug=False)
    factory.protocol = YouTubeWebSockets

    wsResource = WebSocketResource(factory)


    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)

    djangoResource = WSGIResource(reactor, reactor.getThreadPool(), application)

    rootResource = WSGIRootResource(djangoResource, {'ws': wsResource})

    site = Site(rootResource)

    reactor.listenTCP(int(os.environ.get("PORT")), site)
    reactor.run()


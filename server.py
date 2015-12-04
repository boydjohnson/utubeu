from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utubeu.settings")

from whitenoise.django import DjangoWhiteNoise


from django.core.wsgi import get_wsgi_application
from json import dumps, loads


class ChatroomUser:
    def __init__(self, youtubewebsocketsuser, username, chatroom_id):
        self.user = youtubewebsocketsuser
        self.username = username
        self.chatroom_id = chatroom_id

    def __unicode__(self):
        return self.username

class YouTubeWebSockets(WebSocketServerProtocol):
    """
    Messages that are coming in/out are text-messages, picture-messages, suggestions, votes, and possibly binary streaming video
    IN text-message = { chatroom_id: 1, message: text, username: somebody}
    OUT text-message = {message: text, //depending username: somebody //withRedis id: 5768}

    IN picture-message = {chatroom_id: 75, picture: binary, username: somebody}
    OUT //[if not sender] picture-message = {picture: binary, username: somebody}

    The next two will work better with Redis

    IN suggestion = {chatroom_id: 58, youtube_value: '3Mehdi895Ddi', username: somebody}
    OUT suggestion = {youtube_value: '...', //depending username: somebody}

    IN vote = {chatroom_id: 58, youtube_value: '4859DidEing48d', username: somebody}
    OUT vote = {youtube_value: '...', vote_total: percentage}

    strictly OUT

    userlist = { usernames = [somebody, somebodyelse, ...]}

    """


    def onConnect(self, request):
        """the client sends in parameters of chatroom-id and user-name
            to either add a ChatroomUser object to the list of ChatroomUsers that
            is the value in the self.factory.users dict with chatroom_id being the key
        """
        params = request.params
        chatroom_id = int(params.get(u"chatroom-id")[0])
        new_user = ChatroomUser(self, params.get(u"user-name")[0], chatroom_id)
        if chatroom_id in self.factory.users:
            chatroomUsers = self.factory.users.get(chatroom_id)
            chatroomUsers.append(new_user)
            output = {'usernames': [cru.username for cru in chatroomUsers]}
            for cru in chatroomUsers:
                cru.user.sendMessage(dumps(output).encode('utf-8'), isBinary=False)
        else:
            self.factory.users[chatroom_id]= [new_user]

    def onMessage(self, payload, isBinary):
        if not isBinary:
            server_input = loads(payload, encoding='utf-8')
            chatroom_id = int(server_input.pop("chatroom_id"))
            chatroomUsers = self.factory.users.get(chatroom_id)
            server_input['usernames'] = [cru.username for cru in chatroomUsers]
            if "message" in server_input:
                user_name = server_input.get("username")
                for cru in chatroomUsers:
                    individual_output = dict(server_input)
                    if cru.username==user_name:
                        individual_output.pop('username')
                    cru.user.sendMessage(dumps(individual_output).encode('utf-8'), isBinary=False)


    def onClose(self, wasClean, code, reason):
        """The reason will be just the primary key of the chatroom---This seems like a hack"""
        chatroom_id = int(reason)
        chatroomUsers = self.factory.users.get(chatroom_id)
        chatroomUsers = [ cru for cru in chatroomUsers if self != cru.user]
        self.factory.users[chatroom_id] = chatroomUsers
        output = {'usernames':[cru.username for cru in chatroomUsers]}
        for c in chatroomUsers:
            c.user.sendMessage(dumps(output).encode('utf-8'), isBinary=False)

class SeparateServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug=False, debugCodePaths=False):
        super(SeparateServerFactory, self).__init__(url, debug, debugCodePaths)
        self.users = {}




if __name__ == '__main__':


    #This is needed for development vs heroku environment
    try:
        port=int(os.environ.get("PORT"))
        websockets_url = "ws://utubeu.herokuapp.com/ws"
    except:
        port=8000
        websockets_url="ws://127.0.0.1:8000/ws"


    factory = SeparateServerFactory(websockets_url, debug=False)
    factory.protocol = YouTubeWebSockets

    wsResource = WebSocketResource(factory)


    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)

    djangoResource = WSGIResource(reactor, reactor.getThreadPool(), application)

    rootResource = WSGIRootResource(djangoResource, {'ws': wsResource})

    site = Site(rootResource)

    reactor.listenTCP(port, site)
    reactor.run()


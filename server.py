from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from redis import from_url

#some key values to be used with redis
def CHATROOM_MESSAGES_KEY(chatroom_id):
    return "CHATROOM_MESS" + str(chatroom_id)

def getChatroomId_From_key(chatroom_key):
    return chatroom_key.replace("CHATROOM_MESS", "")



from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "utubeu.settings")

from whitenoise.django import DjangoWhiteNoise


from django.core.wsgi import get_wsgi_application
from json import dumps, loads


cache = from_url(os.environ["REDIS_URL"])


class ChatroomUser:
    def __init__(self, youtubewebsocketsuser, username, chatroom_id):
        self.user = youtubewebsocketsuser
        self.username = username
        self.chatroom_id = chatroom_id

    def __repr__(self):
        return self.username

class YouTubeWebSockets(WebSocketServerProtocol):
    """
    Messages that are coming in/out are text-messages, picture-messages, suggestions, votes, and possibly binary streaming video
    IN text-message = { chatroom_id: 1, message: text, username: somebody}
    OUT text-message = {message: text, //depending username: somebody //withRedis id: 5768}

    IN picture-message = {chatroom_id: 75, picture: binary, username: somebody}
    OUT //[if not sender] picture-message = {picture: binary, username: somebody}

    The next two will work better with Redis

    IN suggestion = {chatroom_id: 58, youtube_value: '3Mehdi895Ddi', title: 'Uptown Funk...', description: 'stuff about ...',
                        image_url:'https:.....', username: somebody}
    OUT suggestion = {youtube_value: '...', title: '...', description: '...',
                       image_url: 'https:...', //depending username: somebody}

    IN vote = {chatroom_id: 58, youtube_value: '4859DidEing48d', username: somebody}
    OUT vote = {youtube_value: '...', vote_total: percentage}

    strictly OUT

    userlist = { usernames = [somebody, somebodyelse, ...]}

    """
    def doPing(self):
        if self.run:
            self.sendPing()
            reactor.callLater(10, self.doPing)

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
        else:
            self.factory.users[chatroom_id]= [new_user]

    def onOpen(self):
        """On open can be terribly inefficient because it only is called when a user enters the chatroom
        """
        self.run=True
        for id, user_room in self.factory.users.iteritems():
            for chatroom_user in user_room:
                if chatroom_user.user == self:
                    chatroom_id = id
        if cache.exists(CHATROOM_MESSAGES_KEY(chatroom_id)):
            user_message_dict= cache.lrange(CHATROOM_MESSAGES_KEY(chatroom_id),0, -1)
            self.sendMessage(dumps({'last_ten': user_message_dict}).encode('utf-8'), isBinary=False)
        try:
            users = self.factory.users.get(chatroom_id)
            message = {'usernames':[cru.username for cru in users]}
            for u in users:
                u.user.sendMessage(dumps(message).encode('utf-8'), isBinary=False)
        except KeyError:
            print "no chatroom"

    def onMessage(self, payload, isBinary):
        if not isBinary:
            server_input = loads(payload, encoding='utf-8')
            chatroom_id = int(server_input.pop("chatroom_id"))
            chatroom_mess_key = CHATROOM_MESSAGES_KEY(chatroom_id)
            chatroomUsers = self.factory.users.get(chatroom_id)
            if "message" in server_input:
                user_name = server_input.get("username")
                cache.rpush(chatroom_mess_key, dumps({'username': user_name,'msg': server_input.get('message')},encoding='utf-8'))
                length_of_message_list = cache.llen(chatroom_mess_key)
                if length_of_message_list>10:
                    cache.lpop(chatroom_mess_key)
                for cru in chatroomUsers:
                    individual_output = dict(server_input)
                    if cru.username==user_name:
                        individual_output.pop('username')
                    cru.user.sendMessage(dumps(individual_output).encode('utf-8'), isBinary=False)
            elif "youtube_value" in server_input:
                user_name = server_input.get("username")
                for cru in chatroomUsers:
                    individual_output = dict(server_input)
                    if cru.username == user_name:
                        individual_output.pop("username")
                    cru.user.sendMessage(dumps(individual_output).encode('utf-8'), isBinary=False)

    def onClose(self, wasClean, code, reason):
        """The reason will be just the primary key of the chatroom---This seems like a hack"""
        self.run=False
        try:
            chatroom_id = int(reason)
            chatroomUsers = self.factory.users.get(chatroom_id)
            chatroomUsers = [ cru for cru in chatroomUsers if self != cru.user]
            self.factory.users[chatroom_id] = chatroomUsers
            output = {'usernames':[cru.username for cru in chatroomUsers]}
            for c in chatroomUsers:
                c.user.sendMessage(dumps(output).encode('utf-8'), isBinary=False)
        except ValueError:
            pass

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


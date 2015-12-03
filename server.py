from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

from twisted.internet import reactor
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

    factory = SeparateServerFactory("ws://127.0.0.1:9000", debug=False)
    factory.protocol = YouTubeWebSockets

    reactor.listenTCP(9000, factory)
    reactor.run()
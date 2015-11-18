from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

from twisted.internet import reactor
from json import dumps


SCREENS = ['Firefox', 'Chrome']
PHONES = ['Android']



def determineUser(text):
    if "Firefox" in text:
        return 'Firefox'
    elif "Chrome" in text:
        return "Chrome"
    else:
        return "Other"



class YouTubeWebSockets(WebSocketServerProtocol):

    def onConnect(self, request):
        device = determineUser(request.headers[u'user-agent'])
        if device in PHONES:
            self.factory.phones.append(self)
        elif device in SCREENS:
            self.factory.screens.append(self)
            for s in self.factory.screens:
                s.sendMessage(dumps({'screen': {'count':len(self.factory.screens)}}).encode('utf-8'))
        else:
            self.factory.other.append(self)

    def onClose(self, wasClean, code, reason):
        device = determineUser(self.http_headers[u'user-agent'])
        if device in PHONES:
            self.factory.phones.remove(self)
        elif device in SCREENS:
            self.factory.screens.remove(self)
            for s in self.factory.screens:
                s.sendMessage(dumps({'screen': {'count':len(self.factory.screens)}}).encode('utf-8'))
        else:
            self.factory.other.remove(self)

    def onMessage(self, payload, isBinary):
        JSON = {'screen':{'count':len(self.factory.screens)}}
        print len(self.factory.screens)
        if not isBinary:
            JSON['msg'] = payload.decode('utf-8')
            for s in self.factory.screens:
                s.sendMessage(dumps(JSON).encode('utf-8'))



class SeparateServerFactory(WebSocketServerFactory):

    def __init__(self, url, debug=False, debugCodePaths=False):
        super(SeparateServerFactory, self).__init__(url, debug, debugCodePaths)
        self.phones = []
        self.screens = []
        self.other = []




if __name__ == '__main__':

    factory = SeparateServerFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = YouTubeWebSockets



    reactor.listenTCP(9000, factory)
    reactor.run()
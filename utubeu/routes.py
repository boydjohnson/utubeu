from channels.routing import route, include

from utubeu_dash.routes import channel_routing as dash_routing

channel_routing = [
    include(dash_routing, path=r'^/ws/$')
]
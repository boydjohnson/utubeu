from channels.routing import route, include

from utubeu_dash.routes import channel_routing as dash_routing
from utubeu_viewer.routes import channel_route as viewer_routing
from utubeu_viewer import consumers as con


channel_routing = [
    include(dash_routing, path=r'^/ws'),
    include(viewer_routing, path=r'^/c'),
    route('ChatMess', con.chat_message_consumer)
]
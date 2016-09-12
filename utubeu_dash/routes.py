from channels.routing import route_class

from utubeu_dash.consumers import DashboardConsumer

channel_routing = [
    route_class(DashboardConsumer, path=r'^/dash/$')
]
from channels.routing import ChannelNameRouter, ProtocolTypeRouter


application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({}),
})

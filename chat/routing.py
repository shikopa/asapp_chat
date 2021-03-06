from channels.staticfiles import StaticFilesConsumer
from consumers import ws_connect, ws_receive, ws_disconnect

channel_routing = {
    'websocket.connect': ws_connect,
    'websocket.receive': ws_receive,
    'websocket.disconnect': ws_disconnect,
    'http.request': StaticFilesConsumer(),
}
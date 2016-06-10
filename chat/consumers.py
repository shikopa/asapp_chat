import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from models import ChatRoom

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    """
    Connect to the websocket
    routing.channel_routing['websocket.connect']
    Obtain the room name from the path
    Path format = '/chat/[username_1]_[username_2]'
    """

    room_uuid = ''
    try:
        prefix, room_uuid = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'chat':
            print 'ws_connect: Invalid Path: {0}'.format(message['path'])
            return

        room = ChatRoom.objects.get(room_uuid=room_uuid)

    except ValueError:
        print 'ws_connect: Invalid Path: {0}'.format(message['path'])
        return
    except ChatRoom.DoesNotExist:
        print 'ws_connect: The room, {0} does not exist in the database'.format(room_uuid)
        return

    print 'ws_connect: A client at, {0}:{1}, has connected to the ChatRoom: {2}'.format(
        message['client'][0], message['client'][1], room.room_uuid)

    # Add the Chat room to the session
    message.channel_session['room'] = room.room_uuid
    # Broadcast the message to all listening sockets
    print 'channel layer..... : ', message.channel_layer
    Group('chat-' + room_uuid, channel_layer=message.channel_layer).add(message.reply_channel)

@channel_session
def ws_receive(message):
    """
    Websocket receives a message
    routing.channel_routing['websocket.receive']
    Obtain the ChatRoom from the message, if valid, obtain the Chat Message, store it in the DB and broadcast the message
    """

    room_uuid = ''
    try:
        room_uuid = message.channel_session['room']
        room = ChatRoom.objects.get(room_uuid=room_uuid)
    except KeyError:
        print 'ws_receive: Channel Session does not have a room.'
        return
    except ChatRoom.DoesNotExist:
        print 'ws_receive: The room, {0} does not exist in the database'.format(room_uuid)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        print 'ws_receive: The message text is not in JSON format: {0}'.format(message['text'])
        return


    if data:
        print 'ws_receive: The room: {0}, has received the message, {1}, from: {2}'.format(room.room_uuid, data['message'],
                                                                                           data['sender'])
        data['sender'] = get_object_or_404(User, username=data['sender'])
        chat_message = room.messages.create(**data)

        # Broadcast the message to all listening sockets
        Group('chat-'+room_uuid, channel_layer=message.channel_layer).send({'text': json.dumps(chat_message.as_dict())})

@channel_session
def ws_disconnect(message):
    """
    Disconnect the Websocket
    routing.channel_routing['websocket.disconnect']
    """

    room_uuid = ''
    try:
        room_uuid = message.channel_session['room']
        ChatRoom.objects.get(room_uuid=room_uuid)
        Group('chat-'+room_uuid, channel_layer=message.channel_layer).discard(message.reply_channel)
    except KeyError:
        print 'ws_disconnect: Channel Session does not have a room.'
        return
    except ChatRoom.DoesNotExist:
        print 'ws_disconnect: The room, {0} does not exist in the database'.format(room_uuid)
        return

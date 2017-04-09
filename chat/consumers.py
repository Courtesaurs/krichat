import json

from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http 
from channels.channel import Group

from .models import User, Message, Room

http_user = True

@channel_session_user_from_http  
def kri_connect(message):
    Group('chat').add(message.reply_channel)
    message.reply_channel.send({"accept": True})


@channel_session_user
def kri_message(message):
    data = json.loads(message.content['text'])

    user = message.user
    room = Room.objects.get(pk=data['room_id'])

    msg = Message(
        sender=user,
        room=room,
        text=data['text'],
        is_loud=False
    )
    msg.save()

    if message.content['text'].isupper():
        screaming = True
    else:
        screaming = False

    Group('chat').send({'text': json.dumps({'message': message.content['text'],
    										'sender': message.user.username,
    										'screaming': screaming})})


@channel_session_user
def kri_disconnect(message):
    Group('chat').discard(message.reply_channel)




from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ChatRoom(models.Model):
    room_uuid = models.SlugField(unique=True)
    owner = models.ForeignKey(User, related_name='chat_rooms')
    guest = models.ForeignKey(User)

    def __unicode__(self):
        return self.room_uuid

    class Meta:
        unique_together = (('owner', 'guest'),)

    @classmethod
    def create_rooms(cls, user):
        """
        Creates Chat Rooms for the given user and all other users
        """

        users = User.objects.all().exclude(username=user.username)

        # Check if a Chat Room has been created for each User, create one if none exist
        for u in users:
            if not cls.objects.filter(models.Q(owner=user, guest=u) |  models.Q(owner=u, guest=user)).exists():
                cls.objects.create(
                    room_uuid=user.username + '_' + u.username,
                    owner=user, guest=u
                )

    @classmethod
    def get_room(cls, user1, user2):
        """
        Given two users, return a Chat Room
        """
        if not cls.objects.filter(models.Q(owner=user1, guest=user2) | models.Q(owner=user2, guest=user1)).exists():
            cls.objects.create(
                room_uuid=user1.username + '_' + user2.username,
                owner=user1, guest=user2
            )
        else:
            return cls.objects.get(models.Q(owner=user1, guest=user2) |  models.Q(owner=user2, guest=user1))

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages')
    sender = models.ForeignKey(User)
    message = models.TextField()
    created_dt = models.DateTimeField(default=timezone.now, db_index=True, )

    def __unicode__(self):
        return '[{created_dt}] {sender}: {message}'.format(**self.as_dict())

    @property
    def formatted_created_dt(self):
        return self.created_dt.strftime("%B %-d, %Y, %-I:%M %p %Z").replace('PM', 'p.m.').replace('AM', 'a.m.')
    
    def as_dict(self):
        return {'created_dt': self.formatted_created_dt, 'message': self.message, 'sender': self.sender.username }
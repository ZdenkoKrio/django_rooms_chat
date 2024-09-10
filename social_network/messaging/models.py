from django.contrib.auth.models import User
from django.db import models


class Chatroom(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='chatrooms')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(User, related_name='private_messages', on_delete=models.CASCADE, null=True,
                                  blank=True)

    def is_private(self):
        return self.recipient is not None

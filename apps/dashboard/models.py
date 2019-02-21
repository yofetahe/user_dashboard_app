from django.db import models
from apps.login_registration.models import User

DEFAULT_MSG_ID = 1

class Message(models.Model):
    msg_content = models.TextField()
    user = models.ForeignKey(User, related_name="messages", default=DEFAULT_MSG_ID)
    created_at = models.DateTimeField(auto_now_add=True)
    udpated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    reply_content = models.TextField()
    message = models.ForeignKey(Message, related_name="replies", default=DEFAULT_MSG_ID)
    user = models.ForeignKey(User, related_name="comments", default=DEFAULT_MSG_ID)
    created_at = models.DateTimeField(auto_now_add=True)
    udpated_at = models.DateTimeField(auto_now=True)


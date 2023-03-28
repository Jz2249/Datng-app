from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatMessage(models.Model):
    username = models.TextField()
    room_name = models.CharField(max_length=255, null=True)
    content = models.TextField()
    
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    def most_recent_msg(self): # most 20 recent msg will be loaded
        return ChatMessage.objects.order_by('-timestamp').all()[:20]
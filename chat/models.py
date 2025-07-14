from django.db import models
import uuid
from django.conf import settings


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions', null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def messages(self):
        return self.messages.all()

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=(('human', 'Human'), ('ai', 'AI')))
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150, blank=True, null=True)  # New field for human username

    def __str__(self):
        preview = (self.text[:30] + '...') if len(self.text) > 30 else self.text
        return f"{self.sender.capitalize()} @ {self.created.strftime('%Y-%m-%d %H:%M:%S')}:{preview}"
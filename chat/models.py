from django.db import models
from accounts.models import CustomUser
from marketplace.models import Listing


class Message(models.Model):
    listing   = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages')
    sender    = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.email} → {self.receiver.email}: {self.content[:40]}'

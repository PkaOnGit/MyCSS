from django.db import models
from User.models import User  # Import the User model from the users app

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    email_subject = models.CharField(max_length=255, blank=True, null=True)
    email_content = models.TextField(blank=True, null=True)
    sms_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user.name} at {self.created_at}"
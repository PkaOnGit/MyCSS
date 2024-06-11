from django.db import models
from django.conf import settings

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=1021)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1021)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
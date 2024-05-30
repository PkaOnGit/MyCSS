from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Notification'


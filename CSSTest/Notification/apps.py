from django.apps import AppConfig
from . import signals

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Notification'

    # def ready(self):
    #     import Notification.signals

from .models import Notification

def send_confirmation_message(user, message):
    Notification.objects.create(user=user, message=message)
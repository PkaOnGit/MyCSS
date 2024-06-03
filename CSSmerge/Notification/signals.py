from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification
from Login.models import User
from Ticket.models import Ticket

@receiver(post_save, sender=User)
def notify_user_profile_update(sender, instance, created, **kwargs):
    if created:
        message = f'Your profile has been created, {instance.user.username}!'
    else:
        message = f'Your profile has been updated, {instance.user.username}!'
    Notification.objects.create(user=instance.user, message=message)

@receiver(post_save, sender=Ticket)
def notify_ticket_creation(sender, instance, created, **kwargs):
    if created:
        message = f'A new ticket "{instance.title}" has been created.'
        Notification.objects.create(user=instance.user, message=message)
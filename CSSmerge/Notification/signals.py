# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from .models import Notification
# from Login.models import User
# from Ticket.models import Ticket

# @receiver(post_save, sender=User)
# def notify_user_profile_update(sender, instance, created, **kwargs):
#     if created:
#         message = f'Your profile has been created, {instance.user.username}!'
#         subject = 'Profile Created'
#     else:
#         message = f'Your profile has been updated, {instance.user.username}!'
#         subject = 'Profile Updated'
    
#     Notification.objects.create(user=instance.user, message=message)
    
#     # Send email notification
#     send_mail(
#         subject,
#         message,
#         'from@example.com',  # Replace with your "from" email address
#         [instance.user.email],
#         fail_silently=False,
#     )

# @receiver(post_save, sender=Ticket)
# def notify_ticket_creation(sender, instance, created, **kwargs):
#     if created:
#         message = f'A new ticket "{instance.title}" has been created.'
#         subject = 'New Ticket Created'
#         Notification.objects.create(user=instance.user, message=message)
        
#         # Send email notification
#         send_mail(
#             subject,
#             message,
#             'from@example.com',  # Replace with your "from" email address
#             [instance.user.email],
#             fail_silently=False,
#         )

#comment this until got the E-mail
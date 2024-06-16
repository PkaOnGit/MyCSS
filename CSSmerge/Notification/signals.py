# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.conf import settings
# from django.core.mail import send_mail
# from .models import Notification
# from Login.models import UserRegister
# from Ticket.models import Ticket

# @receiver(post_save, sender=UserRegister)
# def send_user_registration_notification(sender, instance, created, **kwargs):
#     if created:
#         # Notify user
#         Notification.objects.create(
#             user=instance,
#             message='Welcome to our service! Your account has been created.'
#         )
#         # Send email
#         send_mail(
#             'Account Created',
#             'Welcome to our service! Your account has been created.',
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.email],
#             fail_silently=False,
#         )

# @receiver(post_save, sender=Ticket)
# def send_ticket_creation_notification(sender, instance, created, **kwargs):
#     if created:
#         # Notify admin
#         admin_user = UserRegister.objects.filter(is_staff=True).first()
#         if admin_user:
#             Notification.objects.create(
#                 user=admin_user,
#                 message=f"A new ticket has been created by {instance.user.username}: {instance.title}"
#             )
#             # Send email to admin
#             send_mail(
#                 'New Ticket Created',
#                 f"A new ticket has been created by {instance.user.username}: {instance.title}",
#                 settings.DEFAULT_FROM_EMAIL,
#                 [admin_user.email],
#                 fail_silently=False,
#             )

# @receiver(pre_save, sender=UserRegister)
# def send_profile_update_notification(sender, instance, **kwargs):
#     if instance.pk:
#         old_instance = UserRegister.objects.get(pk=instance.pk)
#         if old_instance.roles != instance.roles:
#             # Notify user
#             Notification.objects.create(
#                 user=instance,
#                 message='Your profile has been updated by an admin.'
#             )
#             # Send email
#             send_mail(
#                 'Profile Updated',
#                 'Your profile has been updated by an admin.',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [instance.email],
#                 fail_silently=False,
#             )

# comment this until got the E-mail
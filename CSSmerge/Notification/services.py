import os
import urllib.parse
import urllib.request
from django.core.mail import send_mail
from django.conf import settings

# Ensure you have these settings in your settings.py
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.your-email-provider.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'

def send_email_notification(to_email, user, subject, content):
    send_mail(
        user,
        subject,
        content,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )
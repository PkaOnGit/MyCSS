# Generated by Django 5.0.6 on 2024-06-14 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0006_notification_read_alter_notification_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='read',
        ),
    ]

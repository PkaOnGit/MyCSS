# Generated by Django 5.0.6 on 2024-06-10 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0009_customtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregister',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userregister',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='userregister',
            name='user_permissions',
        ),
    ]
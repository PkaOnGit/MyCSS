# Generated by Django 5.0.6 on 2024-06-16 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0014_userprofile_roles'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomToken',
        ),
    ]
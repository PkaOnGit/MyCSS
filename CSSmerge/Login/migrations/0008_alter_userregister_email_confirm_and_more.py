# Generated by Django 5.0.6 on 2024-06-10 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0007_userregister_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='email_confirm',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userregister',
            name='phone_confirm',
            field=models.BooleanField(default=False),
        ),
    ]
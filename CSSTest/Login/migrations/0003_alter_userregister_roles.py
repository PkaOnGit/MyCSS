# Generated by Django 5.0.6 on 2024-06-18 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_delete_userlogin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='roles',
            field=models.ManyToManyField(default=3, related_name='users', to='Login.role'),
        ),
    ]
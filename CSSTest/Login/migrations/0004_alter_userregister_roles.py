# Generated by Django 5.0.6 on 2024-06-18 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_alter_userregister_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='roles',
            field=models.ManyToManyField(related_name='users', to='Login.role'),
        ),
    ]

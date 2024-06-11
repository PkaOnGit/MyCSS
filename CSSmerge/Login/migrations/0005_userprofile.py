# Generated by Django 5.0.6 on 2024-06-10 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0004_userlogin_rename_user_userregister'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(null=True)),
                ('notes', models.CharField(max_length=5000, null=True)),
            ],
        ),
    ]

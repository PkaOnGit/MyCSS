from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserRegister(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=1024,null=True)
    email = models.CharField(max_length=100, null = True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(null=True)
    status = models.CharField(max_length=1,null=True)
    email_confirm = models.BooleanField(null=True)
    phone_confirm = models.BooleanField(null=True)
    create_at = models.DateTimeField(null=True)
    create_by = models.CharField(max_length= 150, null=True)
    update_at = models.DateTimeField(null=True)
    update_by = models.CharField(max_length= 150,null=True)
    notes = models.CharField(max_length=5000, null=True)

class UserLogin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager

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

class UserRegisterManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
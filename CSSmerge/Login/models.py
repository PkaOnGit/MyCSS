from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserRegisterManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserRegister(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=1024, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=1, null=True)
    roles = models.ManyToManyField(Role, related_name='users')
    email_confirm = models.BooleanField(default=False)
    phone_confirm = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.CharField(max_length=150, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.CharField(max_length=150, null=True)
    notes = models.CharField(max_length=5000, null=True)
    is_staff = models.BooleanField(default=False)

    objects = UserRegisterManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class UserLogin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

class Userprofile(models.Model):
    name = models.CharField(max_length=1024,null=True)
    roles = models.ManyToManyField(Role, related_name='users')
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(null=True)
    notes = models.CharField(max_length=5000, null=True)

class CustomToken(Token):
    user_token = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

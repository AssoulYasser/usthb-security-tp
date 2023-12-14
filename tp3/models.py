from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import managers

def user_directory_path(instance, filename):
    return f'tp3/personal_images/user_{instance.email}/{filename}'

def hacker_directory_path(instance, filename):
    return f'tp3/hackers_images/user_{instance.user}/{filename}'

class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    personal_image = models.ImageField(upload_to=user_directory_path)
    android_id = models.CharField(max_length=16, unique=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    
    objects = managers.MyUserManage()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

class UnauthorizedAccessHistory(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=16)
    password = models.BooleanField(default=False)
    email_2fa = models.BooleanField(default=False)
    face_id = models.BooleanField(default=False)
    android_id = models.BooleanField(default=False)
    last_photo = models.ImageField(upload_to=hacker_directory_path, null=True, blank=True)
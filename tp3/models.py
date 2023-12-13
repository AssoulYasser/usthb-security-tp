from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import managers

def user_directory_path(instance, filename):
    return f'tp3/personal_images/user_{instance.email}/{filename}'

class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    personal_image = models.ImageField(upload_to=user_directory_path)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    
    objects = managers.MyUserManage()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
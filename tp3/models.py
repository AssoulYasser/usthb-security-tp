from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
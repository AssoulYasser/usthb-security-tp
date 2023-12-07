from django.contrib.auth.base_user import BaseUserManager
import re

class MyUserManage(BaseUserManager):
    def user_condition_satisfied(self, **extra_fields):
        from . import models
        for field in models.MyUser.REQUIRED_FIELDS:
            if field not in extra_fields:
                raise Exception('FIELD ARE NOT SATISFIED')    
        
    def validate_mac_address(self, mac):
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(pattern, mac):
            print('not match')
            raise Exception('MAC ADDRESS IS UNCORRECT')
    
    def create_user(self, **extra_fields):
        try:
            self.user_condition_satisfied(**extra_fields)

            email = self.normalize_email(extra_fields['email'])
            mac_address = extra_fields['mac_address']
            password = extra_fields['password']

            self.validate_mac_address(mac_address)

            extra_fields.pop('email')
            extra_fields.pop('password')
            
            user = self.model(email=email, **extra_fields)
            user.set_password(password)

            user.save()
            return user

        except Exception as E:
            raise E

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(**extra_fields)


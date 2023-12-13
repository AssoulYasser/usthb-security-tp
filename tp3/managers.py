from django.contrib.auth.base_user import BaseUserManager
import re
from . import rsa

class MyUserManage(BaseUserManager):
    def user_condition_satisfied(self, **extra_fields):
        from . import models
        for field in models.MyUser.REQUIRED_FIELDS:
            if field not in extra_fields:
                raise Exception('FIELD ARE NOT SATISFIED')    

    def validate_password(self, password):
        pattern = r'^(?=.*[A-Z])(?=.*[\W_]).{7,}$'

        if not re.match(pattern, password):
            raise Exception(f"Password error: WE WILL EXPLAIN IT LATER")    

    def create_user(self, **extra_fields):
        try:
            self.user_condition_satisfied(**extra_fields)

            email = self.normalize_email(extra_fields['email'])
            password = extra_fields['password']

            self.validate_password(password)
            
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


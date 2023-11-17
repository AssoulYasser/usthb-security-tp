from django.contrib.auth.base_user import BaseUserManager
from . import models

class MyUserManage(BaseUserManager):
    def user_condition_satisfied(**extra_fields):
        if models.MyUser.REQUIRED_FIELDS not in extra_fields:
            return Exception('FIELD ARE NOT SATISFIED')    
        return None
    
    def create_user(self, **extra_fields):
        try:
            self.user_condition_satisfied(extra_fields)

            email = self.normalize_email(extra_fields['email'])
            password = extra_fields['password']

            extra_fields.pop('email')
            extra_fields.pop('password')
            
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            
            user.save()
            return user

        except Exception as E:
            raise E

    def create_superuser():
        pass
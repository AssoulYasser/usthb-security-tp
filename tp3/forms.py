from django import forms
from .models import *

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'add-user-form-input'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'add-user-form-input'
            })
        }
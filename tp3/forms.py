from django import forms
from .models import MyUser

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'mac_address', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'add-user-form-input'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'add-user-form-input'
            }),
            'mac_address': forms.TextInput(attrs={
                'calss': 'add-user-form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'add-user-form-input'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'add-user-form-input'
            })
        }
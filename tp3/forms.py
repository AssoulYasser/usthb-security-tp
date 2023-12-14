from django import forms
from .models import MyUser

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'android_id', 'email', 'password', 'personal_image']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'add-user-form-input'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'add-user-form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'add-user-form-input'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'add-user-form-input'
            })
        }
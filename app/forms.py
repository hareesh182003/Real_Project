from django import forms
from app.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']
        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Username'
            }) ,
            'password' : forms.PasswordInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the password'
            }),
            'email' : forms.TextInput(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Email'
            })

        }
        help_texts = {
            'username':""
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','profile_pic']
        widgets = {
            'address' : forms.Textarea(attrs={
                'class' : 'form-control text-center',
                'placeholder' : 'Enter the Address'
            }),
            'username' : forms.FileInput(attrs= {
                'class' : 'form-control-file',
            })
        }


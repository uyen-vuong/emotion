import email
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from utils.helpers import check_validate_email  

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    def cleaned_data(self, str_data):
        return str_data.replace(" ", "")

class CustomUserCreationForm(UserCreationForm):  
    
    fullname = forms.CharField(label = "Fullname")
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

    class Meta:
        model = User
        fields = ('fullname', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            fullname=self.cleaned_data['fullname'],
            is_active=True
        )
        return user
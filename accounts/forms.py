from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.contrib import messages

class SignUpForm(forms.Form):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'id': 'user_email',
                'class': 'form-control'
            }
        )
    )
    password = forms.Field(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    verify_password = forms.Field(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_email(self):
        new_email = self.cleaned_data.get("username")
        emails = User.objects.filter(email=new_email)
        if emails.exists():
            raise forms.ValidationError("Email is taken")
        return new_email

    def clean(self):
        data = self.cleaned_data
        if data.get('password') != data.get('verify_password'):
            raise forms.ValidationError('Your passwords must match.')
        return data


class LoginForm(forms.Form):
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'id': 'user_email',
                'class': 'form-control'
            }
        )
    )
    password = forms.Field(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        emails = User.objects.filter(email=new_email)
        if not emails.exists():
            raise forms.ValidationError("Password or email does not match.")
        return new_email

    def clean(self):
        data = self.cleaned_data
        # if data.get('password') != data.get('verify_password'):
        #     raise forms.ValidationError('Your passwords must match.')
        # username2 = data.get('email')
        # password2 = data.get('password')
        # user = authenticate(username=username2, password=password2)
        # if user is None:
        #     raise forms.ValidationError('Your username/email or password is wrong. Try again')
        return super().clean()




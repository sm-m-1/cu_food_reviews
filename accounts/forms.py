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
    password2 = forms.Field(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_username(self):
        new_email = self.cleaned_data.get("username")
        emails = User.objects.filter(email=new_email)
        if emails.exists():
            raise forms.ValidationError("Email is taken")
        return new_email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        return password



    def clean(self):
        error_messages = [
            'Your passwords must match.',
            'Your password must have 8 characters at least',
            "Your password can't have all numbers"
        ]
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        password_valid = password == password2 and len(password) > 7 and (not str(password).isdigit())
        if not password_valid:
            raise forms.ValidationError(error_messages)
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
        return super().clean()



class ContactForm(forms.Form):
    fullname = forms.CharField(
        label="Your name:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "Placeholder": "Your full name"}
        )
    )
    email = forms.EmailField(
        label="Your email:",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "Placeholder": "Your Email"}
        )
    )
    subject = forms.CharField(
        label="Message subject:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "Placeholder": "Your subject"}
        )
    )
    content = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "Placeholder": "Your message"}
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if not "gmail.com" in email:
        #     raise forms.ValidationError("Email has to be gmail.")
        return email
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class Signup(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm your password'}))
    zip_code = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder':'Enter your ZIP code'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exist.')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return password

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if len(zip_code) != 5:
            raise forms.ValidationError('ZIP code needs to be 5 numeric (0-9) characters in length.')
        if zip_code.isnumeric() == False:
            raise forms.ValidationError('ZIP code can only contain 5 numeric (0-9) characters.')
        return zip_code

class Login(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))

class ResetPassword(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your new password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm your new password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists() == False:
            raise forms.ValidationError('Username does not exist.')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return confirm_password

class Settings(forms.Form):
    username = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'placeholder':'Update your username'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder':'Update your new password'}))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder':'Confirm your new password'}))
    zip_code = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'placeholder':'Update your ZIP code'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == "":
            return username
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exist.')
        return username
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password == "" or confirm_password == "":
            return confirm_password
        elif password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return confirm_password

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if zip_code == "":
            return zip_code
        if len(zip_code) != 5:
            raise forms.ValidationError('ZIP code needs to be 5 numeric (0-9) characters in length.')
        if zip_code.isnumeric() == False:
            raise forms.ValidationError('ZIP code can only contain 5 numeric (0-9) characters.')
        return zip_code
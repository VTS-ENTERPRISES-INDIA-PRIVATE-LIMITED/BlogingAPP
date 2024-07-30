from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter email address"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter username"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm password"}))
   
    class Meta:
        model = CustomUser
        fields =[ "email", "username", "password1", "password2"]



class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter FirstName"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter LastName"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter address"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter bio"}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone"}))
    role = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter role"}))
    
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "profile_pic", "address", "bio", "phone_no", "role"]


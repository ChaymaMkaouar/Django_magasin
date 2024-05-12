from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contact
from django.contrib.auth.forms import UserChangeForm


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')
    email = forms.EmailField(label='Adresse e-mail')

class Meta(UserCreationForm.Meta):
    model = User
    fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')

class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.HiddenInput())

class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        fields ="__all__"
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", 'bio',
                  'image', "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already taken. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.bio = self.cleaned_data['bio']
        user.image = self.cleaned_data['image']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class blog_form(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = blog_model
        fields = ('theme', 'header', 'image', 'content', 'link')


class MessengerForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Messenger
        fields = ['message']
        READ_ONLY_FIELDS = ['from_user', 'to_user']

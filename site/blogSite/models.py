
from django.contrib.auth.models import User
from django.db import models


class user_account(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    bio = models.TextField(max_length=255)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.username


class Messenger(models.Model):
    from_user = models.CharField(max_length=100)
    to_user = models.CharField(max_length=100)
    message = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class blog_model(models.Model):
    theme = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/', blank=False, null=True)
    time = models.DateField(auto_now_add=True)
    header = models.CharField(max_length=25)
    content = models.TextField(max_length=1000)
    link = models.CharField(max_length=2000, unique=True)

    def __str__(self) -> str:
        return self.author


from django.contrib.auth.models import User
from django.db import models


class user_account(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    bio = models.TextField(max_length=255)
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.username


class theme_model(models.Model):
    theme = models.CharField(max_length=25)


class blog_model(models.Model):
    theme = models.CharField(max_length=25)
    # author = models.OneToOneRel(user_account,on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    time = models.DateField(auto_now_add=True)
    header = models.CharField(max_length=25)
    content = models.TextField(max_length=1000)
    link = models.CharField(max_length=2000,unique=True)
    def __str__(self) -> str:
        return self.author

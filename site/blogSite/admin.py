from django.contrib import admin
from .models import *

reg = admin.site.register

reg(user_account)
reg(theme_model)
reg(blog_model)
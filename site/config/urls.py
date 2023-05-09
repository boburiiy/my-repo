"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.views import *
def hehe(request):
    return HttpResponse('O`xshamadi')
urlpatterns = [
    path('admin/',hehe),
    path('i_need_to/how/admin', admin.site.urls),
    path('', include('blogSite.urls')), 
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="auth/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]

from django.contrib.auth import login, logout, authenticate, forms
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import MessengerForm
from django.conf import settings
from .models import blog_model
from django.views import View
from .forms import *
from .models import *
import requests


def users(request):
    if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
        img = user_account.objects.get(username=request.user).image.url
    else:
        img = None
    context = {
        'users': User.objects.all(),
        'image': img
    }
    return render(request, 'users.html', context)


def user_detect(request, name):
    if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
        image = user_account.objects.get(username=request.user).image.url
    else:
        image = None
    context = {
        'user': user_account.objects.filter(username=name).first(),
        'image': image
    }
    return render(request, 'user.html', context)


def index(request):
    username = request.user.username
    if request.user.is_authenticated and not request.user.is_superuser:
        image = user_account.objects.get(username=username).image.url
    else:
        image = None
    return render(request, 'main/index.html', {"usering": request, "image": image})


def about(request):
    username = request.user.username
    if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
        image = user_account.objects.get(username=username).image.url
    else:
        image = None
    return render(request, 'main/about.html', {"usering": request, "image": image})


def news(reqeuest, typen):
    context = {
        'data': requests.get(
            f'http://boburiyapi.pythonanywhere.com/{typen}').json(),
        'typen': typen
    }
    return render(reqeuest, 'news/index.html', context)


@login_required()
def my_profile(request):
    user = request.user
    if not user.is_superuser:
        user_p = user_account.objects.get(username=user)
        context = {
            'name': user_p.username,
            'email': user_p.email,
            'bio': user_p.bio,
            'image': user_p.image.url,
            'smsgs': sended_messages,
            'getted': getted
        }
    else:
        context = {'none':None}
        user_p = 'admin'
    sended_messages = Messenger.objects.filter(from_user=user)
    getted = Messenger.objects.filter(to_user=user)
    return render(request, 'main/account.html', context)


@login_required()
def logout_user(request):
    logout(request)
    messages.error(request, 'log outed')
    return redirect(index)


def blog(request, theme):
    cards = blog_model.objects.filter(theme=theme)
    username = request.user.username
    if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
        image = user_account.objects.get(username=username).image.url
    else:
        image = None
    context = {
        "image": image,
        'cards': cards,
        'themes': False,
        'hide': True
    }
    return render(request, 'blog/index.html', context=context)


def blog_detail(request, blog_id):
    card = blog_model.objects.filter(id=blog_id).first()
    username = request.user.username
    if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
        image = user_account.objects.get(username=username).image.url
    print(card.theme)
    return render(request, 'blog/big_card.html', {'card': card, 'image': image})


def blog_search(request, header):
    if request.method == 'POST':
        cards = blog_model.objects.filter(header=header)
        context = {
            'cards': cards,
            'themes': False
        }
        return render(request, 'blog/index.html', context=context)
    else:
        return redirect('blogs')


def blogs(request):
    username = request.user.username
    if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
        image = user_account.objects.get(username=username).image.url
    else:
        image = None
    blogs = blog_model.objects.all().order_by('-id')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    themes = []
    for i in blog_model.objects.all():
        themes.append(i.theme)
    context = {
        'cards': page_obj,
        'themes': themes,
        'image': image
    }
    if request.method == 'POST':
        print('*******************')
        header = request.POST.get('header')
        cards = blog_model.objects.filter(header=header)
        context = {
            'cards': cards,
            'themes': False,
        }
    return render(request, 'blog/index.html', context=context)


def delete_blog(request, blog):
    blog_model.objects.get(id=blog).delete()
    messages.info(request, 'O`chirish muvaffaqiyatli yakunlandi.')
    return redirect('blogs')


class MessengerView(View):
    def get(self, request, to_user):
        form = MessengerForm
        return render(request, 'messenger.html', {'form': form, 'to_user': to_user})

    def post(self, request, to_user):
        form = MessengerForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.to_user = to_user
            message.save()
        return redirect('index')


class add_blog(View):
    def get(self, request):
        username = request.user.username
        if request.user.is_authenticated and request.user.is_authenticated and not request.user.is_superuser:
            image = user_account.objects.get(username=username).image.url
            form = blog_form
            return render(request, 'blog/add.html', {'form': form, 'image': image})
        else:
            form = NewUserForm
            messages.warning(request, 'oldin tizimga kiring')
            return redirect('login')

    def post(self, request):
        form = blog_form(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.username
            blog.save()
            return redirect('blogs')
        else:
            messages.error(request, form.errors)
            form = blog_form()
        return render(request, 'blog/add.html', {'form': form})


class register(View):
    def get(self, request):
        form = NewUserForm
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = NewUserForm(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                bio = form.cleaned_data.get('bio')
                image = form.cleaned_data.get('image')
                user1 = user_account.objects.create(
                    username=username, email=email, bio=bio, image=image)
                user = form.save()
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, message='succesfull')
                return redirect('index')
            else:
                print(form.errors)
                messages.error(request, "Xatolik yuzaga keldi.")
        return render(request, "auth/register.html", {"form": form})


class user_login(View):
    def get(self, request):
        form = AuthenticationForm
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'you are logged as {username}')
                return redirect('index')
            else:
                messages.error(request, f"Invalid username or password")
        else:
            messages.error(request, f"Invalid {form.errors.as_text()}")
            form = AuthenticationForm
        return render(request, "auth/login.html", {"form": form})


class passwd_reset(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'auth/password_reset.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            if user:
                subject = "akkauntni qaytarish"
                email_template_name = "auth/password_reset_email.txt"
                data = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                message = render_to_string(email_template_name, data)
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [
                              user.email], False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                else:
                    return redirect("password_reset_done")
        else:
            messages.error(request, 'error in complete form')
            return redirect('password_reset')

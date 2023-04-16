from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login, logout, authenticate, forms
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import blog_model

def users(request):
    return render(request,'users.html',{'users':User.objects.all()})

def index(request):
    username = request.user.username
    if request.user.is_authenticated:
        image = user_account.objects.get(username=username).image.url
    else:image = None
    return render(request, 'main/index.html', {"usering": request,"image":image})
def about(request):
    username = request.user.username
    if request.user.is_authenticated:
        image = user_account.objects.get(username=username).image.url
    else:image=None
    return render(request, 'main/about.html', {"usering": request,"image":image})


def my_profile(request):
    user_p = user_account.objects.get(username=request.user)
    print(user_p)
    context = {
        'name': user_p.username,
        'email': user_p.email,
        'bio': user_p.bio,
        'image': user_p.image.url
    }
    return render(request, 'main/account.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'logged')
    return redirect(index)


def blog(request, theme):
    cards = blog_model.objects.filter(theme=theme)
    username = request.user.username
    if request.user.is_authenticated:
        image = user_account.objects.get(username=username).image.url
    else:image=None
    context = {
        "image":image,
        'cards': cards,
        'themes': False
    }
    return render(request, 'blog/index.html', context=context)


def blog_detail(request, blog_id):
    card = blog_model.objects.filter(id=blog_id).first()
    username = request.user.username
    if request.user.is_authenticated:
        image = user_account.objects.get(username=username).image.url
    print(card.theme)
    return render(request, 'blog/big_card.html', {'card': card,'image':image})


def blog_search(request, header):
    if request.method == 'POST':
        header = request.POST.get('header', '')
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
    if request.user.is_authenticated:
        image = user_account.objects.get(username=username).image.url
    else:image=None
    blogs = blog_model.objects.all().order_by('-id')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    themes = theme_model.objects.all()
    context = {
        'cards': page_obj,
        'themes': themes,
        'image':image
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


class add_blog(View):
    def get(self, request):
        username = request.user.username
        if request.user.is_authenticated:
            image = user_account.objects.get(username=username).image.url
            form = blog_form
            return render(request, 'blog/add.html', {'form': form,'image':image})
        else:
            form = NewUserForm
            messages.success(request, 'oldin tizimga kiring')
            return redirect('login')

    def post(self, request):
        form = blog_form(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.username
            blog.save()
            theme_model.objects.create(theme=form.cleaned_data.get('theme'))
            return redirect('blogs')
        else:
            messages.error(request,form.errors)
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
                login(request, user)
                messages.success(request, message='succesfull')
                return redirect('index')
            else:
                print(form.errors)
                messages.error(request, "Xatolik yuzaga keldi.")
        return render(request, "auth/register.html", {"form": form})


class user_login(View):
    def get(self, request):
        form = forms.AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'you are logged as {username}')
                return redirect('index')
            else:
                messages.error(request, f"Invalid username or password")
        else:
            messages.error(request, f"Invalid {form.errors}")
            form = forms.AuthenticationForm()
        return render(request, "auth/login.html", {"form": form})

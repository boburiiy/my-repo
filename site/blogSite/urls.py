from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.urls import path, include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('blog_detail/<blog_id>', blog_detail, name='blogdtl'),
    path('blogsearch/<str:header>', blog_search, name='blogss'),
    path('user/<str:name>', user_detect, name='user_f'),
    path('logout/', logout_user, name='logout'),
    path('blog/<str:theme>', blog, name='blogd'),
    path('me/', my_profile, name='profile'),
    path('about/', about, name='about'),
    path('users/', users, name='users'),
    path('blogs/', blogs, name='blogs'),
    path('', index, name='index'),
    path('news/<typen>', news, name='news'),

    path('messenger/<to_user>/', MessengerView.as_view(), name='messenger'),
    path('blogs/delete/<int:blog>', delete_blog, name='blog_d'),
    path('register/', register.as_view(), name='register'),
    path('blogs/add', add_blog.as_view(), name='blogadd'),
    path('login/', user_login.as_view(), name='login'),
    path("password_reset", passwd_reset.as_view(), name="password_reset"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

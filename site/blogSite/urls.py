from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('users/', users, name='users'),
    path('me/', my_profile, name='profile'),
    path('blogs/', blogs, name='blogs'),
    path('blog/<theme>', blog, name='blogd'),
    path('blog/<header>', blog_search, name='blogss'),
    path('blog_detail/<blog_id>', blog_detail, name='blogdtl'),
    path('blogs/add', add_blog.as_view(), name='blogadd'),
    path('logout/', logout_user, name='logout'),
    path('login/', user_login.as_view(), name='login'),
    path('register/', register.as_view(), name='register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

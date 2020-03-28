from django.contrib import admin
from django.urls import path
from craigslist import settings
from django.conf.urls.static import static
from . import views
from .views import PostListView
urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('search', views.search, name="search"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name="update_profile"),
    path('login', views.login, name='login'),
    path('posts', views.home, name='posts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

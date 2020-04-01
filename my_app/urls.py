from django.contrib import admin
from django.urls import path
from craigslist import settings
from django.conf.urls.static import static
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
urlpatterns = [
    path('', views.home, name="home"),
    path('home_login', PostListView.as_view(), name="home_login"),
    path('search', views.search, name="search"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name='profile'),
    path('like/<int:pk>', views.like, name='like'),
    path('update_profile', views.update_profile, name="update_profile"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('posts', views.home, name='posts'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name="post_detail" ),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name="post_update"),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name="post_delete"),
    path('create', PostCreateView.as_view(), name="create"),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

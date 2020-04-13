from django.contrib import admin
from django.urls import path
from craigslist import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostLikeToggle
urlpatterns = [
    path('', views.home, name="home"),
    path('home_login', views.PostListView.as_view(), name="home_login"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name='profile'),
    path('like/<int:pk>', views.like, name='like'),
    path('api/like/<int:pk>', PostLikeToggle.as_view(), name='like-api'),
    path('update_profile', views.update_profile, name="update_profile"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('posts', views.home, name='posts'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name="post_detail" ),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name="post_update"),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name="post_delete"),
    path('password_reset/',       
                        auth_views.PasswordResetView.as_view(template_name="my_app/password_reset.html"), 
                        name="password_reset"),
    path('password_reset/done/',  
                        auth_views.PasswordResetDoneView.as_view(template_name="my_app/password_reset_done.html"), 
                        name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', 
                        auth_views.PasswordResetConfirmView.as_view(template_name="my_app/password_reset_confirm.html"), 
                        name="password_reset_confirm" ),
    path('reset_password/', 
                        auth_views.PasswordResetCompleteView.as_view(template_name="my_app/password_reset_confirm.html"), 
                        name="password_reset_complete" ),
    path('create', PostCreateView.as_view(), name="create"),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

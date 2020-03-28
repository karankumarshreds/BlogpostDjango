from django.shortcuts import render, redirect
from django.contrib.auth.forms import  UserCreationForm as uc
from django.contrib.auth.forms import AuthenticationForm as af
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import UserUpdate, ProfileUpdate
from django.contrib import messages

URL = "https://oslo.craigslist.org/search/hhh?query=bike"

def home(request):
    return render(request, 'home.html', {})

def search(request):
    serch = request.POST.get('search')
    context = {
        'serch': serch,
        'data': data
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = uc(data=request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)
            return redirect('/')
    else:
        form = uc()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = af(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            return redirect('/profile')
    else:
        form = af()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

#my long way for profile + update
# @login_required(login_url='/login')
# def profile(request):
#     status=''
#     user_id = request.user.id
#     instance_user = User.objects.filter(id=user_id).first()
#     if request.method == 'POST':
#         status = request.POST['status']
#         u = Profile.objects.filter(user=request.user.id).get()
#         u.status = status
#         u.save()
#     context = {
#         'user': instance_user.profile.user,
#         'image': instance_user.profile.image.url,
#         'status': status,
#     }
#     return render(request, 'profile.html', context)

@login_required(login_url='/login')
def profile(request):
    user_id = request.user.id
    instance_user = User.objects.filter(id=user_id).first()
    context = {
        'user': instance_user.profile.user,
        'image': instance_user.profile.image.url,
    }
    return render(request, 'profile.html', context)

#copied source code for profile update
@login_required(login_url='/login')
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdate(request.POST, request.FILES, instance=user)
        p_form = ProfileUpdate(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'The profile has been updated.')
            return redirect('/profile')
    else:
        #instance: to get pre-filled data of user
        u_form = UserUpdate(instance=user)
        p_form = ProfileUpdate(instance=user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'update_profile.html', context)


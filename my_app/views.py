from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import  UserCreationForm as uc
from django.contrib.auth.forms import AuthenticationForm as af
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.models import User
from .models import Profile, Post, Likes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin as lrm 
from django.contrib.auth.mixins import UserPassesTestMixin as uptm
from .forms import UserUpdate, ProfileUpdate
from django.contrib import messages
from django.views.generic import (ListView, 
                                DetailView, 
                                CreateView, 
                                UpdateView,
                                DeleteView)


def home(request):
    post = Post.objects.all()
    return render(request, 'home.html', {'post': post})


# class PostListView(ListView):
#     model = Post
#     #generic format : <app>/<model>_<viewtype>.html
#     template_name = 'home_login.html'
#     context_object_name = 'post'
#     ordering = ['-date']


def posts(request):
    post = Post.objects.all()
    likes = Likes.objects.all()
    context = {
        'post': post,
        'likes': likes,
    }
    return render(request, 'home_login.html', context )


#using generic format this time
class PostDetailView(lrm, DetailView): 
    login_url = '/login'
    model = Post 


class PostCreateView(lrm, CreateView):
    login_url = '/login'
    model = Post 
    fields = ['title', 'content']
    #generic name : <model>_form

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

## uptm: because we want users to only update
## their own posts and not others'
class PostUpdateView(lrm, uptm, UpdateView):

    login_url = '/login'
    model = Post
    fields = ['title', 'content']
    
    #Post.objects.filter(user=1).first().user
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
    

class PostDeleteView(lrm, uptm, DeleteView):
    login_url = '/login'
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user :
            return True
        return False


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = uc(data=request.POST)
        if form.is_valid():
            user = form.save(*args, **kwargs)
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
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect('/profile')
    else:
        form = af()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def logout(request):
    dj_logout(request)
    return redirect ('/')

# def like(request, pk):
#     if request.method == 'POST':
#         uid = request.user.id
#         # print(Likes.objects.filter(user=uid).filter(liked_posts=pk).get())
#         likes = Likes.objects.filter(user=uid).filter(liked_posts=pk).first()
#         count = len(Likes.objects.filter(liked_posts=pk))
#         if likes:
#             print('count ------> already--->: ' + str(count))
#             return redirect('home_login')
#         else:
#             # cnt = int(Likes.objects.filter(user=uid).filter(liked_posts=pk).first().count)
#             print('count ------>: ' + str(count))
#             l = Likes(count=count+1, liked_posts=pk)
#             l.save()
#             l.user.add(request.user)
#             l.save()
#             return redirect('home_login')

def like(request, pk):
    uid = request.user.id 
    instance = Post.objects.filter(id=pk).get()
    if request.user in instance.likes.all():
        instance.likes.remove(uid)
        return redirect('home_login')
    else:    
        instance.likes.add(uid)
        instance.save()
        return redirect('home_login')


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




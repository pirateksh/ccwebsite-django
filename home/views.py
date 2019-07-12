from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from home.forms import UserSignupForm
from post.models import Post, Tags
from post.forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_profile.models import UserProfile


NUMBER_OF_POSTS_PER_PAGE = 2
User = get_user_model()
# A function to paginate posts and return them


def page_maker(request, native_user=None):
    if native_user is None:
        post_list = Post.objects.all().order_by('-published')
    else:
        post_list = Post.objects.filter(author=native_user).order_by('-published')
    paginator = Paginator(post_list, NUMBER_OF_POSTS_PER_PAGE)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    form = UserSignupForm()
    addpostform = PostForm()
    posts = page_maker(request)
    user_profiles = UserProfile.objects.all()
    tags = Tags.objects.all()
    context = {
        'form': form,
        'addpostform': addpostform,
        'posts': posts,
        'tags': tags,
        'user_profiles': user_profiles,
    }
    return render(request, 'home/index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Login Success")
            to = '/home/'
            return redirect(to)
        else:
            messages.error(request, f"Login Failed")
            return redirect('/home/')
    else:
        return redirect('/home/')


def logout_view(request):
    logout(request)
    messages.success(request, f"Logout Success")
    return redirect('/home/')


def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            choice = form.cleaned_data.get('choice')
            user = authenticate(username=username, password=raw_password)
            if choice == 'teacher':
                my_group = Group.objects.get(name='Teacher')
                my_group.user_set.add(user)
                my_group.save()
            elif choice == 'student':
                my_group = Group.objects.get(name='Student')
                my_group.user_set.add(user)
                my_group.save()
            login(request, user)

            # Creating profile
            profile = UserProfile(user=user)
            profile.save()

            messages.success(request, f"Signup Success")
            return redirect('/home/')
    else:
        form = UserSignupForm()
    posts = page_maker(request)
    tags = Tags.objects.all()
    addpostform = PostForm()
    context = {
        'form': form,
        'addpostform': addpostform,
        'posts': posts,
        'tags': tags,
    }
    return render(request, 'home/index.html', context)

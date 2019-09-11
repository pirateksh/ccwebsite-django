from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash  # authenticate
from django.contrib.auth.decorators import login_required
from post.views import page_maker

# Imported Models
from django.contrib.auth.models import User
from .models import UserProfile
from comments.models import Comment
from post.models import Post, Tags
# from post.models import Post, Tags

# Imported Forms
from django.contrib.auth.forms import PasswordChangeForm
from .forms import AvatarUploadForm
from home.forms import UserSignupForm
from post.forms import PostForm
from comments.forms import CommentForm

# Create your views here.


def user_profile(request, username, tag_name=None):
    native_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=native_user)
    native_posts = page_maker(request, Post, native_user, tag_filter=tag_name)
    avatar_form = AvatarUploadForm()
    form = UserSignupForm()
    addpostform = PostForm()
    user_profiles = UserProfile.objects.all()
    comments = Comment.objects.all()
    comment_form = CommentForm()
    tags = Tags.objects.all()
    password_change_form = PasswordChangeForm(user=native_user)
    pending_posts = Post.objects.filter(verify_status=-1)
    native_pending_posts = pending_posts.filter(author=native_user)
    read_notif = None
    unread_notif = None
    if request.user.is_authenticated:
        read_notif = request.user.notifications.read()
        unread_notif = request.user.notifications.unread()
    context = {
        'profile': profile,
        'avatar_form': avatar_form,
        'form': form,
        'native_user': native_user,
        'native_posts': native_posts,
        'addpostform': addpostform,
        'password_change_form': password_change_form,
        'comments': comments,
        'comment_form': comment_form,
        'user_profiles': user_profiles,
        'tags': tags,
        'pending_posts': pending_posts,
        'native_pending_posts': native_pending_posts,
        'read_notif': read_notif,
        'unread_notif': unread_notif,
    }
    return render(request, 'user_profile/user_profile.html', context)


@login_required
def edit_profile(request, username):
    native_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=native_user)
    avatar_form = AvatarUploadForm()
    form = UserSignupForm()
    password_change_form = PasswordChangeForm(user=native_user)
    context = {
        'form': form,
        'profile': profile,
        'avatar_form': avatar_form,
        'native_user': native_user,
        'password_change_form': password_change_form,
    }
    return render(request, 'user_profile/edit_profile.html', context)


def change_password(request, username):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important! To keep User Logged in.
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
        else:
            messages.error(request, f'Something went wrong, try again!')
            return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    else:
        password_change_form = PasswordChangeForm(request.user)
    avatar_form = AvatarUploadForm()
    form = UserSignupForm()
    addpostform = PostForm()
    comments = Comment.objects.all()
    comment_form = CommentForm()
    user_profiles = UserProfile.objects.all()
    context = {
        'password_change_form': password_change_form,
        'addpostform': addpostform,
        'avatar_form': avatar_form,
        'form': form,
        'comments': comments,
        'comment_form': comment_form,
        'user_profiles': user_profiles,
    }
    return render(request, 'user_profile/edit_profile.html', context)


def avatar_upload(request, username):
    if request.method == 'POST':
        avatar_form = AvatarUploadForm(request.POST, request.FILES)
        if avatar_form.is_valid():
            user = User.objects.get(username=username)
            user_prof = UserProfile.objects.get(user=user)
            img = avatar_form.cleaned_data['avatar']
            user_prof.avatar = img
            user_prof.save()
            messages.success(request, f"Avatar uploaded successfully!")
            return HttpResponseRedirect(reverse("edit_profile", kwargs={'username': username}))
    else:
        avatar_form = AvatarUploadForm()
    form = UserSignupForm()
    password_change_form = PasswordChangeForm(request.user)
    addpostform = PostForm()
    comments = Comment.objects.all()
    comment_form = CommentForm()
    user_profiles = UserProfile.objects.all()
    context = {
        'password_change_form': password_change_form,
        'addpostform': addpostform,
        'avatar_form': avatar_form,
        'form': form,
        'comments': comments,
        'comment_form': comment_form,
        'user_profiles': user_profiles,
    }
    return render(request, 'user_profile/edit_profile.html', context)


def show_drafts(request, username):
    # native_user = get_object_or_404(User, username=username)
    # profile = get_object_or_404(UserProfile, user=native_user)
    # draft_list = page_maker(request, native_user=native_user, draft=True)
    # avatar_form = AvatarUploadForm()
    # form = UserSignupForm()
    # addpostform = PostForm()
    # password_change_form = PasswordChangeForm(user=native_user)
    # context = {
    #     'profile': profile,
    #     'avatar_form': avatar_form,
    #     'form': form,
    #     'native_user': native_user,
    #     'draft_list': draft_list,
    #     'addpostform': addpostform,
    #     'password_change_form': password_change_form,
    # }
    # return render(request, 'user_profile/user_profile.html', context)
    return HttpResponse('You will see drafts here soon')




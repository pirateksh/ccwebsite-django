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
    """
        This functions renders User Profile Page
    """
    # User whose profile is open
    native_user = get_object_or_404(User, username=username)

    # Profile, posts and avatar of that user
    profile = get_object_or_404(UserProfile, user=native_user)
    native_posts = page_maker(request, Post, native_user, tag_filter=tag_name)
    avatar_form = AvatarUploadForm()

    # Fetching all User profiles, comments, tags, pending posts and
    # pending posts of native user
    user_profiles = UserProfile.objects.all()
    comments = Comment.objects.all()
    tags = Tags.objects.all()
    pending_posts = Post.objects.filter(verify_status=-1)
    native_pending_posts = pending_posts.filter(author=native_user)

    # Comment form, user signup form, post adding form and password change form
    comment_form = CommentForm()
    form = UserSignupForm()
    addpostform = PostForm()
    password_change_form = PasswordChangeForm(user=native_user)

    read_notif = None
    unread_notif = None
    if request.user.is_authenticated:

        # Read notifications
        read_notif = request.user.notifications.read()

        # Unread notifications
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
    """
        This function renders Edit Profile Page.
    """
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


# Personal Information Edit Section Started

@login_required
def change_name(request, username):
    """
        This function changes/add First Name OR Last Name OR Both of a user.
    """
    user = request.user
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, f"Name changed successfully!")
        return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    messages.error(request, f"Something went wrong. Try again!")
    return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))


@login_required
def change_email(request, username):
    """
        This function adds/changes Email of a user.
    """
    user = request.user
    if request.method == "POST":
        email = request.POST['email']
        user.email = email
        user.save()
        messages.success(request, f"Email changed successfully!")
        return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    messages.error(request, f"Something went wrong. Try again!")
    return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))


@login_required
def avatar_upload(request, username):
    """
        This function uploads/re-uploads profile picture of a user.
    """
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

# Personal Information Edit Section Ended

# Notification settings Started


@login_required
def unsubscribe(request, username):
    """
        This function Un-subscribes user from receiving Email Notifications
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    profile.is_subscribed = False
    profile.save()
    messages.success(request, f"Unsubscribed from Email Notifications.")
    return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))


@login_required
def subscribe(request, username):
    """
        This function Subscribes user to receive Email Notifications
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    profile.is_subscribed = True
    profile.save()
    messages.success(request, f"Subscribed to Email Notifications.")
    return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))


def change_password(request, username):
    """
        This function changes password of a user . It ask for current(old) password.
        It also keeps user logged in after successful password change.
    """
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


def show_drafts(request, username):
    """
        This function shows drafts. Currently not in use.
    """
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




from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth import get_user_model
from post.views import page_maker
# from django.contrib.contenttypes.models import ContentType

# Importng models
from comments.models import Comment
from django.contrib.auth.models import Group
from post.models import Tags, Post
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from home.models import EmailBackend

# Importing Forms
from home.forms import UserSignupForm
from post.forms import PostForm
from comments.forms import CommentForm

# A function to paginate posts and return them

HOME = '/'


def index(request):
    form = UserSignupForm()
    addpostform = PostForm()
    posts = page_maker(request)
    user_profiles = UserProfile.objects.all()
    tags = Tags.objects.all()

    # Using Model Manager all().
    comments = Comment.objects.all()
    comment_form = CommentForm()
    # if comment_form.is_valid():
    #     print(comment_form.cleaned_data)
    context = {
        'form': form,
        'addpostform': addpostform,
        'posts': posts,
        'tags': tags,
        'user_profiles': user_profiles,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'home/index.html', context)


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Login Success")
#             return redirect(HOME)
#         else:
#             messages.error(request, f"Login Failed")
#             return redirect(HOME)
#     else:
#         return redirect(HOME)


def ajax_login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        '''
            Response Codes(Acronyms):
            LS: Login success.
            LF: Login failed.
        '''
        if user is not None:
            login(request, user)
            return HttpResponse('LS')
        else:
            return HttpResponse('LF')
    # else:
    #     return redirect(HOME)


def logout_view(request):
    logout(request)
    messages.success(request, f"Logout Success")
    return redirect(HOME)


# def signup_view(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             choice = form.cleaned_data.get('choice')
#             user = authenticate(username=username, password=raw_password)
#             if choice == 'teacher':
#                 my_group = Group.objects.get(name='Teacher')
#                 my_group.user_set.add(user)
#                 my_group.save()
#             elif choice == 'student':
#                 my_group = Group.objects.get(name='Student')
#                 my_group.user_set.add(user)
#                 my_group.save()
#             login(request, user)
#
#             # Creating profile
#             profile = UserProfile(user=user)
#             profile.save()
#
#             messages.success(request, f"Signup Success")
#             return redirect(HOME)
#     else:
#         form = UserSignupForm()
#     posts = page_maker(request)
#     tags = Tags.objects.all()
#     addpostform = PostForm()
#     context = {
#         'form': form,
#         'addpostform': addpostform,
#         'posts': posts,
#         'tags': tags,
#     }
#     return render(request, 'home/index.html', context)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def ajax_signup_view(request):
    if request.method == 'POST':
        username_ = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_ = request.POST['email']
        choice = request.POST['choice']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        users = User.objects.all()

        username_list = []
        email_list = []
        for user in users:
            username_list.append(user.username)
            email_list.append(user.email)

        '''
            Response Codes(Acronyms):
            UAR: User with that Username already registered.
            EAR: User with that Email already registered.
            NA: Not Available.
            PNM: Passwords did'nt match.
            PTS: Password too short.
            PVS: Password very similar to personal information.
            PTC: Password too common.
            PEN: Password entirely numeric.
            SS: Signup Success.
            ERR: Error.
        '''

        # Checking for Username uniqueness
        if username_ in username_list:
            return HttpResponse('UAR')

        # Checking for Email uniqueness
        if email_ in email_list:
            return HttpResponse('EAR')

        # Checking passwords.
        if password1 != password2:
            return HttpResponse('PNM')
        else:
            if len(password1) < 8:
                return HttpResponse('PTS')

            username_lower = username_.lower()
            pass_lower = password1.lower()
            fname_lower = first_name.lower()
            lname_lower = last_name.lower()

            if is_number(pass_lower):
                return HttpResponse('PEN')
            if (pass_lower in username_lower) or (username_lower in pass_lower):
                return HttpResponse('PVS')
            if (fname_lower in pass_lower) or (pass_lower in fname_lower):
                return HttpResponse('PVS')
            if (lname_lower in pass_lower) or (pass_lower in lname_lower):
                return HttpResponse('PVS')
            if 'qwerty' in pass_lower:
                return HttpResponse('PTC')
            if '123' in pass_lower:
                return HttpResponse('PTC')

        # All checks done, user entries valid for signup.
        user_ = User.objects.create_user(
            username=username_,
            email=email_,
            password=password1,
        )
        user_.first_name = first_name
        user_.last_name = last_name
        user_.save()

        if choice == 'teacher':
            my_group = Group.objects.get(name='Teacher')
            my_group.user_set.add(user_)
            my_group.save()
        elif choice == 'student':
            my_group = Group.objects.get(name='Student')
            my_group.user_set.add(user_)
            my_group.save()

        user_ = authenticate(username=username_, password=password1)
        if user_ is not None:
            login(request, user_)
        else:
            # Deleting user in case it has been added in database.
            user_qs = User.objects.filter(username=username_)
            if user_qs:
                user = user_qs.first()
                user.delete()
            return HttpResponse('ERR')

        # Creating profile
        profile = UserProfile(user=user_)
        profile.save()
        return HttpResponse('SS')


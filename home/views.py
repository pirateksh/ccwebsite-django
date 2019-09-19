from django.shortcuts import render, HttpResponseRedirect, HttpResponse, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from post.views import page_maker
from django.http import JsonResponse
# from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType

# Imports for email
from django.template.loader import render_to_string
from django.core import mail
from django.utils.html import strip_tags

# Importing models
from comments.models import Comment
from django.contrib.auth.models import Group
from post.models import Tags, Post
from user_profile.models import UserProfile
from django.contrib.auth.models import User

# Importing Forms
from home.forms import UserSignupForm
from post.forms import PostForm
from comments.forms import CommentForm


def set_profile(request, user):
    """
        This function checks whether all necessary information about user is filled or not
        and sets profile.
        If profile is set successfully it returns True, otherwise False.
    """
    profile_qs = UserProfile.objects.filter(user=user)
    if profile_qs:
        profile = profile_qs.first()

        # Saving Group of user as Student by Default
        my_group = Group.objects.get(name='Student')
        my_group.user_set.add(request.user)
        my_group.save()

        if profile.is_password_set:
            if profile.is_email_verified:
                if len(str(user.email)) > 0:
                    if len(str(user.first_name)) > 0:
                        profile.is_profile_set = True
                        profile.save()
                        return True
                    else:
                        messages.info(request, f"Name is not set.")
                else:
                    messages.info(request, f"Email is not set.")
            else:
                messages.info(request, f"Email not verified")
        else:
            messages.info(request, f"Password is not set.")
        profile.is_profile_set = False
        profile.save()
        return False
    messages.error(request, f"User not found.")
    return False


def index(request, tag_filter=None, username=None, liked=None, older=None):
    """
        This function renders Home Page.
        If tag_filter = None, All posts are fetched
        otherwise posts from specific tags are fetched.
    """
    check_profile = None
    flag = False
    if request.user.is_authenticated:
        flag = set_profile(request, request.user)
        check_profile = UserProfile.objects.get(user=request.user)

    # User signup form, comment form, Post adding form
    form = UserSignupForm()
    comment_form = CommentForm()
    addpostform = PostForm()

    # Fetching posts as pages, all User Profiles, tags and comments
    posts = page_maker(request, Post, tag_filter=tag_filter, username=username, liked=liked, older=older)
    user_profiles = UserProfile.objects.all()
    tags = Tags.objects.all()
    comments = Comment.objects.all()  # Using overridden Model Manager all().

    # Context to be sent to template
    context = {
        'form': form,
        'addpostform': addpostform,
        'posts': posts,
        'tags': tags,
        'user_profiles': user_profiles,
        'comments': comments,
        'comment_form': comment_form,
    }
    if check_profile is not None:
        if not check_profile.is_profile_set:
            # messages.info(request, f"Set your profile first.")
            return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': request.user.username}))

    if username is not None:
        messages.info(request, f"You are viewing Personalised Feed.")
    else:
        messages.info(request, f"You are viewing Public Feed.")

    return render(request, 'home/index.html', context)

    # Tried earlier:
    # if comment_form.is_valid():
    #     print(comment_form.cleaned_data)


# def personalised_index(request, username, tag_filter=None):
#     """
#         This function renders Personalised Home Page.
#         i.e. this page will contain post of only followed user.
#         If tag_filter = None, All posts are fetched
#         otherwise posts from specific tags are fetched.
#     """
#     check_profile = None
#     flag = False
#     user = User.objects.get(username=username)
#     if request.user == user:
#         if request.user.is_authenticated:
#             flag = set_profile(request, request.user)
#             check_profile = UserProfile.objects.get(user=request.user)
#
#         # User signup form, comment form, Post adding form
#         form = UserSignupForm()
#         comment_form = CommentForm()
#         addpostform = PostForm()
#
#         # Fetching posts as pages, all User Profiles, tags and comments
#         posts = page_maker(request, Post, tag_filter=tag_filter)
#         user_profiles = UserProfile.objects.all()
#         tags = Tags.objects.all()
#         comments = Comment.objects.all()  # Using overridden Model Manager all().
#
#         # Context to be sent to template
#         context = {
#             'form': form,
#             'addpostform': addpostform,
#             'posts': posts,
#             'tags': tags,
#             'user_profiles': user_profiles,
#             'comments': comments,
#             'comment_form': comment_form,
#         }
#         if check_profile is not None:
#             if not check_profile.is_profile_set:
#                 # messages.info(request, f"Set your profile first.")
#                 return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': request.user.username}))
#
#         return render(request, 'home/post_display_personalised.html', context)
#     messages.info(request, f"You are unauthorized to view this page.")
#     return HttpResponseRedirect(reverse('Index'))


def ajax_login_view(request):
    """
        Function to login using AJAX.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        '''
            Response Codes(Acronyms):
            LS: Login success.
            LF: Login failed.
        '''       
        if user is not None:
            login(request, user)
            response = HttpResponse('LS')
            if remember_me is None:
                # Executed when remember_me is None i.e. not checked.
                if 'cook_user' and 'cook_pass' in request.COOKIES:
                    # Enters when either of the cookie is present.
                    # response = render(request,'blogapp/newhome.html',context)
                    response.delete_cookie('cook_user')
                    response.delete_cookie('cook_pass')
                    return response
                else:
                    # Enters when both of the cookie is not present i.e. deleted .
                    return response
            else:
                if 'cook_user' and 'cook_pass' not in request.COOKIES:
                    response.set_cookie('cook_user', username, max_age=86400, path='/')
                    response.set_cookie('cook_pass', password, max_age=86400, path='/')
                    return response
                else:
                    if username==request.COOKIES.get('cook_user') and password==request.COOKIES.get('cook_password'):                        
                        return response
                    elif username!=request.COOKIES.get('cook_user') or password!=request.COOKIES.get('password'):
                        response.set_cookie('cook_user', username, max_age=86400, path='/')
                        response.set_cookie('cook_pass', password, max_age=86400, path='/')
                        return response
        else:
            return JsonResponse('LF')
    # else:
    #     return redirect(HOME)


def logout_view(request):
    """
        A simple function to log out.
    """
    logout(request)

    # Success message
    messages.success(request, f"Logout Success")

    return HttpResponseRedirect(reverse('Index'))


def is_number(s):
    """
        Function to check whether 's' is a number or NOT.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def ajax_signup_view(request):
    """
        A function to Sign Up using AJAX.
    """
    if request.method == 'POST':

        # Intuitive variable names
        username_ = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_ = request.POST['email']
        # choice = request.POST['choice']
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

            # Changing to Lower Case
            username_lower = username_.lower()
            pass_lower = password1.lower()
            fname_lower = first_name.lower()
            lname_lower = last_name.lower()

            # Checks for password.
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

        # Saving group of user
        # if choice == 'teacher':
        #     my_group = Group.objects.get(name='Teacher')
        #     my_group.user_set.add(user_)
        #     my_group.save()
        # elif choice == 'student':
        my_group = Group.objects.get(name='Student')
        my_group.user_set.add(user_)
        my_group.save()

        # Authenticating user
        user_ = authenticate(username=username_, password=password1)
        if user_ is not None:
            # If user is present, Log In
            login(request, user_)
            # Password is set hence true.
            profile = UserProfile.objects.get(user=user_)
            profile.is_password_set = True
            profile.save()
        else:
            # Some error occurred.
            # Deleting user in case it has been added in database.
            user_qs = User.objects.filter(username=username_)
            if user_qs:
                user = user_qs.first()
                user.delete()
            return HttpResponse('ERR')

        return HttpResponse('SS')

        # Tried earlier:
        # Creating profile
        # profile = UserProfile(user=user_)
        # profile.save()


def AddToCalendar(request, pk):
    post = Post.objects.all().filter(id=pk).first()
    event_url = "https://www.google.com/calendar/render?action=TEMPLATE&text="+str(post.title)+"&details="+str(post.post_content)
    return redirect(event_url)


# Functions not in use currently

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
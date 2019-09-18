from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash  # authenticate
from django.contrib.auth.hashers import make_password  # check_password
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.utils.timesince import timesince
from django.utils import timezone

# from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Importing token
from .tokens import account_activation_token

# Import for sending mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Self made functions import
from home.views import set_profile, is_number
from post.views import page_maker

# Imported Models
from django.contrib.auth.models import User
from .models import UserProfile
from comments.models import Comment
from post.models import Post, Tags
from quizapp.models import UserQuizResult

# Imported Forms
from django.contrib.auth.forms import PasswordChangeForm
from .forms import AvatarUploadForm
from home.forms import UserSignupForm
from post.forms import PostForm, TagForm
from comments.forms import CommentForm

# Importing Stuff for Google Calendar API
from .cal_setup import get_calendar_service
import os.path

# 3rd Party imports
from notifications.signals import notify


def user_profile(request, username, tag_name=None):
    """
        This functions renders User Profile Page
    """
    service = get_calendar_service(request)
    # Call the Calendar API
    # print('Getting list of calendars')
    timeZone = None
    calendar_id = None
    if service:
        cal_service_found = True     
        calendars_result = service.calendarList().list().execute()

        calendars = calendars_result.get('items', [])

        if not calendars:
            print('No calendars found.')
        for calendar in calendars:
            # print(calendar.get('primary'))# prints True only for the primary Calendar of User
            if calendar.get('primary'):
                summary = calendar['summary']
                calendar_id = calendar['id']
                timeZone = calendar['timeZone']
                primary = "Primary" if calendar.get('primary') else ""
                  # print(timeZone) # prints Asia/Kolkata
                print("%s\t%s\t%s" % (summary, calendar_id, primary))
        # User whose profile is open
    native_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=native_user)

    check_profile = None
    flag = False

    if request.user.is_authenticated:
        check_profile = get_object_or_404(UserProfile, user=request.user)
        if profile is check_profile:
            flag = set_profile(request, native_user)
            check_profile = get_object_or_404(UserProfile, user=request.user)

    # Users current user is following
    followed_users = check_profile.followed_users.all()
    # Users who are following current user
    followers = check_profile.followers.all()

    # Posts and avatar of that user
    native_posts = page_maker(request, Post, native_user, tag_filter=tag_name)

    # drafts = page_maker(request, Post, native_user, draft=True)
    # This also contains scheduled but NOT yet approved event related post
    drafts = Post.objects.filter(author=native_user).filter(draft=True)

    # Scheduled event related post which have not been given permission yet.
    scheduled_posts = Post.objects.filter(author=native_user).filter(draft=True).filter(is_scheduled=True)

    # Fetching all User profiles, comments, tags, pending posts and
    # pending posts of native user
    user_profiles = UserProfile.objects.all()
    comments = Comment.objects.all()
    tags = Tags.objects.all()

    # Filtering All pending posts and pending post of native user which are NOT drafts.
    pending_posts = Post.objects.filter(verify_status=-1).filter(draft=False)
    native_pending_posts = pending_posts.filter(author=native_user).filter(draft=False)

    # Comment form, user signup form, post adding form and password change form
    comment_form = CommentForm()
    form = UserSignupForm()
    addpostform = PostForm()
    password_change_form = PasswordChangeForm(user=native_user)
    avatar_form = AvatarUploadForm()

    read_notif = None
    unread_notif = None
    if request.user.is_authenticated:

        # Read notifications
        read_notif = request.user.notifications.read()

        # Unread notifications
        unread_notif = request.user.notifications.unread()
    quiz_results = UserQuizResult.objects.all().filter(user=request.user)

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
        'drafts': drafts,
        'quiz_results': quiz_results,
        'scheduled_posts': scheduled_posts,
        'followed_users': followed_users,
        'followers': followers,
    }

    if check_profile is not None:
        if not profile.is_profile_set:
            messages.info(request, f"User profile not set")
            return HttpResponseRedirect(reverse('Index'))

    if 'cal_service_found' in locals():
        new_to_context = {'cal_service_found': 1, 'calendar_id': calendar_id, 'timeZone': timeZone}
        context.update(new_to_context)
    return render(request, 'user_profile/user_profile.html', context)


@login_required
def follow_user(request, username, username2):
    """
        This function adds desired user to following list of logged in user.
    """
    follower = User.objects.get(username=username)
    follower_profile = UserProfile.objects.get(user=follower)
    if request.user == follower:
        followed = User.objects.get(username=username2)
        followed_profile = UserProfile.objects.get(user=followed)

        # Checking if logged in user already followed the user.
        if followed in follower_profile.followed_users.all():
            result = "AF"
            response = {
                'result': result,
            }
            return JsonResponse(response)

        # Adding desired user to logged in user's followed list
        follower_profile.followed_users.add(followed)
        follower_profile.save()

        # Adding logged in user to followed user's followers list
        followed_profile.followers.add(follower)
        followed_profile.save()

        # A very bad idea to attach this notification with a specific post by hard - coding to avoid errors.
        # post = Post.objects.get(title='Follow Users')
        # post_url = reverse('post_detail', kwargs={'slug': post.slug})

        notify.send(
            # Sending notification to person being followed.
            follower_profile,
            recipient=followed,
            verb='followed you',
            # target=post,
            dp_url=follower_profile.avatar.url,
            prof_url=reverse("User Profile", kwargs={'username': follower.username}),
            # post_url=post_url,
            actor_name=follower_profile.user.first_name,
            timestamp_=timesince(timezone.now()),
        )

        result = "SS"
        response = {
            'result': result,
            'nativePK': followed.pk,
        }
        return JsonResponse(response)
    result = "ERR"
    response = {
        'result': result,
    }
    return JsonResponse(response)


@login_required
def unfollow_user(request, username, username2):
    """
        This function removes desired user from following list of logged in user.
    """
    unfollower = User.objects.get(username=username)
    unfollower_profile = UserProfile.objects.get(user=unfollower)

    if request.user == unfollower:
        unfollowed = User.objects.get(username=username2)
        unfollowed_profile = UserProfile.objects.get(user=unfollowed)

        # Checking if logged in user already unfollowed the user.
        if unfollowed not in unfollower_profile.followed_users.all():
            result = "AUF"
            response = {
                'result': result,
            }
            return JsonResponse(response)

        # Removing desired user from logged in user's followed list
        unfollower_profile.followed_users.remove(unfollowed)
        unfollower_profile.save()

        # Removing logged in user from followed user's followers list
        unfollowed_profile.followers.remove(unfollower)
        unfollowed_profile.save()

        # No notification sent in case of un-following.

        result = "SS"
        response = {
            'result': result,
            'nativePK': unfollowed.pk,
        }
        return JsonResponse(response)
    result = "ERR"
    response = {
        'result': result,
    }
    return JsonResponse(response)


@login_required
def edit_profile(request, username):
    """
        This function renders Edit Profile Page.
    """
    native_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=native_user)

    # All tags and subscribed tags
    tags = Tags.objects.all()
    tags_subscribed = profile.subscribed_tags.all()

    # Forms
    avatar_form = AvatarUploadForm()
    form = UserSignupForm()
    password_change_form = PasswordChangeForm(user=native_user)
    tag_form = TagForm()
    context = {
        'form': form,
        'profile': profile,
        'avatar_form': avatar_form,
        'native_user': native_user,
        'password_change_form': password_change_form,
        'tag_form': tag_form,
        'tags': tags,
        'tags_subscribed': tags_subscribed,
    }

    # A check so that other users cannot visit edit page of native user.
    if request.user == native_user:
        return render(request, 'user_profile/edit_profile.html', context)
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


# Personal Information Edit Section Started

@login_required
def change_name(request, username):
    """
        This function changes/add First Name OR Last Name OR Both of a user.
    """
    native_user = get_object_or_404(User, username=username)
    user = request.user
    if request.user == native_user:
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
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


@login_required
def change_email(request, username):
    """
        This function adds/changes Email of a user.
    """
    native_user = get_object_or_404(User, username=username)
    user = request.user
    if request.user == native_user:
        if request.method == "POST":
            email = request.POST['email']
            old_email = user.email

            if old_email != email:
                user.email = email
                user.save()
                profile = UserProfile.objects.get(user=user)
                # Setting is email verified to be false when email is changed
                profile.is_email_verified = False
                profile.save()
                messages.success(request, f"Email changed successfully!")
            else:
                messages.info(request, f"You have entered same email as saved in you profile.")
            return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
        messages.error(request, f"Something went wrong. Try again!")
        return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


@login_required
def verify_email(request, username):
    """
        This function sends a verification link to your email.
    """
    native_user = get_object_or_404(User, username=username)
    user = request.user
    if user == native_user:
        email = native_user.email
        # Verifying Email

        subject = 'Activate your blog account.'
        # current_site = get_current_site(request)
        domain = Site.objects.filter()
        email_context = {
            'user': user,
            'domain': domain.first(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # .decode(),
            'token': account_activation_token.make_token(user),
        }
        html_message = render_to_string('user_profile/mail_template_email_verification.html', context=email_context)
        plain_message = strip_tags(html_message)

        from_email = "noreply@ccwebsite"
        to = str(user.email)
        try:
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except mail.BadHeaderError:
            messages.info(request, f"Invalid Header found, mail not sent!")

        # message = render_to_string('acc_active_email.html', {
        #     'user': user,
        # })
        #
        # to_email = form.cleaned_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        return HttpResponse('Please confirm your email address to complete the registration')
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


def activate(request, uidb64, token):
    """
        A function that verifies email through activation link.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.user == user:
            if user.is_authenticated:
                profile = UserProfile.objects.get(user=user)

                profile.is_email_verified = True
                profile.save()

                messages.success(request, f"Your email has been verified.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': user.username}))
            messages.success(request, f"Login to verify email.")
            return HttpResponseRedirect(reverse('Index'))
    return HttpResponse('Activation link is invalid!')


@login_required
def avatar_upload(request, username):
    """
        This function uploads/re-uploads profile picture of a user.
    """
    native_user = get_object_or_404(User, username=username)
    if request.user == native_user:
        if request.method == 'POST':
            avatar_form = AvatarUploadForm(request.POST, request.FILES)
            if avatar_form.is_valid():
                user_prof = UserProfile.objects.get(user=native_user)
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
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))

# Personal Information Edit Section Ended


# Subscription settings started

@login_required
def subscribe_to_tag_toggle(request, username, tag):
    """
        A function to subscribe/unsubscribe to tags.
    """
    if request.method == "GET":
        user = User.objects.get(username=username)
        if request.user == user:
            tag_name = request.GET['tag']
            tag_name = str(tag_name)
            tag = Tags.objects.get(name=tag_name)
            profile = UserProfile.objects.get(user=user)
            """
                Acronyms:
                SU - Succesfully Unsubscribed
                SS - Successfully Subscribed
                UA - Unauthorised
                ERR - Error
            """
            # Check if tag is already subscribed
            if tag in profile.subscribed_tags.all():
                # Unsubscribe
                profile.subscribed_tags.remove(tag)
                tag.subscribed_by.remove(user)
                result = "SU"
            else:
                # Subscribe
                profile.subscribed_tags.add(tag)
                tag.subscribed_by.add(user)
                result = "SS"
            profile.save()
            tag.save()
        else:
            result = "UA"
    else:
        result = "ERR"
    response = {
        'result': result
    }
    return JsonResponse(response)

# Notification settings Started


@login_required
def subscription_toggle(request, username):
    """
        This function toggles user's subscription of receiving Email Notifications
    """
    native_user = get_object_or_404(User, username=username)
    if request.user == native_user:
        profile = get_object_or_404(UserProfile, user=native_user)
        if profile.is_subscribed:
            profile.is_subscribed = False
            messages.success(request, f"Unsubscribed from Email Notifications.")
        else:
            profile.is_subscribed = True
            messages.success(request, f"Subscribed to Email Notifications.")
        profile.save()
        return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))

#
# @login_required
# def subscribe(request, username):
#     """
#         This function Subscribes user to receive Email Notifications
#     """
#     user = request.user
#     profile = get_object_or_404(UserProfile, user=user)
#     profile.is_subscribed = True
#     profile.save()
#     messages.success(request, f"Subscribed to Email Notifications.")
#     return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))


@login_required
def sound_notification_toggle(request, username):
    """
        This function toggles Sound Notification option.
    """
    native_user = get_object_or_404(User, username=username)
    if request.user == native_user:
        profile = get_object_or_404(UserProfile, user=native_user)
        if profile.is_sound_on:
            profile.is_sound_on = False
            messages.success(request, f"Sound notification turned Off.")
        else:
            profile.is_sound_on = True
            messages.success(request, f"Sound notification turned On.")
        profile.save()
        return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


# Security Section Started


def set_password(request, username):
    """
        This functions sets Password of user who have logged in through Social Account.
    """
    native_user = get_object_or_404(User, username=username)
    if request.user == native_user:
        if request.method == "POST":
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Changing to Lower Case
            username_lower = username.lower()
            pass_lower = password1.lower()
            fname_lower = request.user.first_name.lower()
            lname_lower = request.user.last_name.lower()

            # Checks for password.
            if password1 != password2:
                messages.error(request, f"Passwords did not match. Try Again!")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            if is_number(pass_lower):
                messages.error(request, f"Passwords can't ne entirely numeric.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            if (pass_lower in username_lower) or (username_lower in pass_lower):
                messages.error(request, f"Password can't be too similar to personal information.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            if (fname_lower in pass_lower) or (pass_lower in fname_lower):
                messages.error(request, f"Password can't be too similar to personal information.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            if (lname_lower in pass_lower) or (pass_lower in lname_lower):
                messages.error(request, f"Password can't be too similar to personal information.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            if 'qwerty' in pass_lower:
                messages.error(request, f"Passwords can't be too common.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            if '123' in pass_lower:
                messages.error(request, f"Passwords can't be too common.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))

            request.user.password = make_password(password=password1)
            request.user.save()
            profile = UserProfile.objects.get(user=native_user)
            profile.is_password_set = True
            profile.save()
            messages.success(request, f"Password has been set successfully.")
            return HttpResponseRedirect(reverse('Index'))
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


def change_password(request, username):
    """
        This function changes password of a user . It ask for current(old) password.
        It also keeps user logged in after successful password change.
    """
    native_user = get_object_or_404(User, username=username)
    if request.user == native_user:
        if request.method == 'POST':
            password_change_form = PasswordChangeForm(native_user, request.POST)
            if password_change_form.is_valid():
                user = password_change_form.save()
                update_session_auth_hash(request, user)  # Important! To keep User Logged in.
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
            else:
                messages.error(request, f'Something went wrong, try again!')
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
        else:
            password_change_form = PasswordChangeForm(native_user)
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
    messages.info(request, f"You are not authorised to visit this page.")
    return HttpResponseRedirect(reverse('User Profile', kwargs={'username': request.user}))


@login_required
def approve_event(request, username, slug):
    if request.method == "POST":
        approve_comment = request.POST['approve_comment']
        approve_comment = str(approve_comment)

        # Native user and profile
        native_user = User.objects.get(username=username)
        native_profile = UserProfile.objects.get(user=native_user)

        post = Post.objects.get(slug=slug)
        post_url = reverse('post_detail', kwargs={'slug': slug})

        # Event's post's author and author's profile
        author = post.author
        author_profile = UserProfile.objects.get(user=author)

        if author_profile.is_subscribed:
            subject = "Request for conducting event approved."
            domain = Site.objects.filter()
            email_context = {
                    'teacher': native_user,
                    'post': post,
                    'domain': domain.first(),
                    'status': 'accepted',
                    'remark': approve_comment,
            }
            html_message = render_to_string('user_profile/mail_template_reply.html', context=email_context)
            plain_message = strip_tags(html_message)
            from_email = "noreply@ccwebsite"
            to = str(author.email)
            try:
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            except mail.BadHeaderError:
                messages.info(request, f"Invalid Header found, mail not sent!")

        # Sending notification to event's post's author.
        notify.send(
            native_profile,
            recipient=author,
            verb='granted permission for event.',
            target=post,
            dp_url=native_profile.avatar.url,
            prof_url=reverse("User Profile", kwargs={'username': native_user.username}),
            post_url=post_url,
            actor_name=native_profile.user.first_name,
            timestamp_=timesince(timezone.now()),
        )

        tags = post.tags.all()
        notify_users = []
        email_users = []
        for tag in tags:
            subs = tag.subscribed_by.all()
            for sub in subs:
                if sub not in notify_users:
                    notify_users.append(sub)
                sub_profile = UserProfile.objects.get(user=sub)
                if sub_profile.is_subscribed:
                    if sub not in email_users:
                        email_users.append(sub)

        # Sending notification to all users who have subscribed to tag in tags.
        """
            This is giving error. Check why!
        """

        # notify.send(
        #     author,
        #     recipient=notify_users,
        #     verb='is hosting an event.',
        #     target=post,
        #     dp_url=author_profile.avatar.url,
        #     prof_url=reverse("User Profile", kwargs={'username': author.username}),
        #     post_url=post_url,
        #     actor_name=author.first_name,
        #     timestamp_=timesince(timezone.now()),
        # )

        # Sending mail to subscribed users
        subject = 'Event of your interest'

        # Domain of link
        domain = Site.objects.filter()
        email_context = {
            'post': post,
            'domain': domain.first(),
        }
        html_message = render_to_string('user_profile/mail_template_event_notification.html', context=email_context)
        plain_message = strip_tags(html_message)
        from_email = "noreply@ccwebsite"

        try:
            mail.send_mail(subject, plain_message, from_email, email_users, html_message=html_message)
        except mail.BadHeaderError:
            messages.info(request, f"Invalid Header found, mail not sent!")

        post.verify_status = 1
        post.draft = False
        post.save()
    messages.info(request, f"You have approved an event.")
    return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))


@login_required
def reject_event(request, username, slug):
    if request.method == "POST":
        reject_comment = request.POST['reject_comment']
        reject_comment = str(reject_comment)
        # Native user and profile
        native_user = User.objects.get(username=username)
        native_profile = UserProfile.objects.get(user=native_user)

        post = Post.objects.get(slug=slug)
        post_url = reverse('post_detail', kwargs={'slug': slug})

        # Event's post's author and author's profile
        author = post.author
        author_profile = UserProfile.objects.get(user=author)
        if author_profile.is_subscribed:
            # Sending Email if post author has subscribed to Email notification.
            subject = "Request for conducting event rejected."
            # Domain of link
            domain = Site.objects.filter()
            email_context = {
                'teacher': native_user,
                'post': post,
                'domain': domain.first(),
                'status': 'rejected',
                'remark': reject_comment,
            }
            html_message = render_to_string('user_profile/mail_template_reply.html', context=email_context)
            plain_message = strip_tags(html_message)
            from_email = "noreply@ccwebsite"
            to = str(author.email)
            try:
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            except mail.BadHeaderError:
                messages.info(request, f"Invalid Header found, mail not sent!")
        notify.send(
            # Sending notification to event's post's author.
            native_profile,
            recipient=author,
            verb='rejected permission for event.',
            target=post,
            dp_url=native_profile.avatar.url,
            prof_url=reverse("User Profile", kwargs={'username': native_user.username}),
            post_url=post_url,
            actor_name=native_profile.user.first_name,
            timestamp_=timesince(timezone.now()),
        )
        post.verify_status = -1
        post.draft = False
        post.save()
    messages.info(request, f"You have rejected an event.")
    return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))


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




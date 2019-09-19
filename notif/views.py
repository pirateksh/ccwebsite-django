from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

# Imported models
from user_profile.models import UserProfile
from post.models import Tags

# Self made function imports
from home.views import set_profile
User = get_user_model()


@login_required
def notification_view(request):
    """
        This function will render notification detail view.
    """
    user = request.user
    check_profile = None
    flag = None
    if user.is_authenticated:
        flag = set_profile(request, user)
        check_profile = UserProfile.objects.get(user=user)

    # Read notifications of current user
    read_notif = user.notifications.read().filter()

    # Unread notifications of current user
    unread_notif = user.notifications.unread()

    # All user profiles
    user_profile_qs = UserProfile.objects.all()

    context = {
        'read_notif': read_notif,
        'unread_notif': unread_notif,
        'user_profile_qs': user_profile_qs,
    }

    if check_profile is not None:
        if not check_profile.is_profile_set:
            # messages.info(request, f"Set your profile first.")
            return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': request.user.username}))

    return render(request, 'notif/notifications_detail.html', context)


def mark_as_read(request, pk):
    """
        This function will mark a particular unread notification as read.
    """

    # Notification having primary key = pk (of current user).
    notification = request.user.notifications.get(pk=pk)

    notification.unread = False
    notification.save()
    return HttpResponseRedirect(reverse('all_notifications'))


def mark_all_as_read(request):
    """
        This function will mark all unread notifications as read.
    """
    # All unread notifications of current user
    notification_qs = request.user.notifications.unread()
    if notification_qs:
        notification_qs.mark_all_as_read()
        messages.success(request, f"All notifications marked as read.")
    else:
        messages.info(request, f"You do not have any notification.")
    return HttpResponseRedirect(reverse('all_notifications'))


def clear_notification(request, pk):
    """
        This function clears/deletes a particular read notification as read.
    """
    notification = request.user.notifications.get(pk=pk)
    notification.delete()
    return HttpResponseRedirect(reverse('all_notifications'))


def clear_all_notification(request):
    """
        This function clears/deletes all read notification as read.
    """
    # All unread notifications of current user
    notification_qs = request.user.notifications.read()
    if notification_qs:
        for notification in notification_qs:
            notification.delete()
        # notification_qs.mark_all_as_deleted()
        messages.success(request, f"All notifications cleared.")
    else:
        messages.info(request, f"You do not have any notification.")
    return HttpResponseRedirect(reverse('all_notifications'))

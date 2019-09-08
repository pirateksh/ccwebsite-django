from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

# Imported models
from user_profile.models import UserProfile

User = get_user_model()


@login_required
def notification_view(request):
    """
        This function will render notification detail view.
    """
    user = request.user
    read_notif = user.notifications.read()
    unread_notif = user.notifications.unread()
    user_profile_qs = UserProfile.objects.all()
    context = {
        'read_notif': read_notif,
        'unread_notif': unread_notif,
        'user_profile_qs': user_profile_qs,
    }
    return render(request, 'notif/notifications_detail.html', context)


def mark_as_read(request, pk):
    """
        This function will mark a particular unread notification as read.
    """
    notification = request.user.notifications.get(pk=pk)
    notification.unread = False
    notification.save()
    return HttpResponseRedirect(reverse('all_notifications'))


def mark_all_as_read(request):
    """
        This function will mark all unread notifications as read.
    """
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
    notification.delete = True
    notification.save()
    return HttpResponseRedirect(reverse('all_notifications'))


def clear_all_notification(request):
    """
        This function clears/deletes all read notification as read.
    """
    notification_qs = request.user.notifications.read()
    if notification_qs:
        notification_qs.mark_all_as_deleted()
        messages.success(request, f"All notifications cleared.")
    else:
        messages.info(request, f"You do not have any notification.")
    return HttpResponseRedirect(reverse('all_notifications'))

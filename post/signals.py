from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Post
from notifications.models import Notification


@receiver(pre_delete)
def delete_notification(sender, instance, using, **kwargs):
    if sender == Post:
        title = instance.title
        notifications = Notification.objects.all()
        # Deleting notification related to post before deleting post
        for notification in notifications:
            if str(notification.target) == str(title):
                print("target is same as title")
                notification.delete()
    else:
        print("Sender error")

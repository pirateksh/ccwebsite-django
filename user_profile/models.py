from django.db import models
from django.contrib.auth.models import User

# 3rd party imports
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Imported models
from post.models import Tags


def user_directory_path(instance, filename):
    """
        A function to return path where image will be stored after uploading.
    """
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_avatar/' + 'user_{0}/{1}'.format(instance.user.username, filename)


class UserProfile(models.Model):

    # User whose profile is to be created.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile picture of user
    avatar = ProcessedImageField(
        default='default.png',
        upload_to=user_directory_path,
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
    )

    # Whether Email has been verified or not
    is_email_verified = models.BooleanField(default=False)

    # Whether user is subscribed to email notifications
    is_subscribed = models.BooleanField(default=True)

    # Whether sound notification is on or not.
    is_sound_on = models.BooleanField(default=True)

    # Whether password is set or not
    is_password_set = models.BooleanField(default=False)

    # Whether user profile is set or not
    is_profile_set = models.BooleanField(default=False)

    # Subscribed tags(topics)
    subscribed_tags = models.ManyToManyField(Tags, related_name='subscribed_tags', verbose_name='Subscribed Tags', default=None, blank=True)

    # Followed users
    followed_users = models.ManyToManyField(User, related_name='followed_user', verbose_name='Followed users', default=None, blank=True)

    # Followers
    followers = models.ManyToManyField(User, related_name='followers', verbose_name='Followers', default=None, blank=True)

    def __str__(self):
        return self.user.username

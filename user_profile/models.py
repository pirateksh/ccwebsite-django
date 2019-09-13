from django.db import models
from django.contrib.auth.models import User

# 3rd party imports
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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

    # Whether user is subscribed to email notifications
    is_subscribed = models.BooleanField(default=True)

    # Whether user profile is set or not
    is_profile_set = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_avatar/' + 'user_{0}/{1}'.format(instance.user.username, filename)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = ProcessedImageField(
        upload_to=user_directory_path,
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
    )
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


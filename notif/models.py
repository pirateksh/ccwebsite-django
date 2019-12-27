from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Importing models
from post.models import Post


User = get_user_model()


class Notification(models.Model):
	"""
		This models stores notificaitons.
	"""

	# User to which notification is sent
	recipient = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="Recipient",)

	# User whose action triggers notification
	sender = models.ForeignKey(
		User,
		blank=False,
		on_delete=models.CASCADE,
		related_name="Sender"
	)

	# Post (If notification is attached to some post)
	post = models.ForeignKey(
		Post,
		blank=True,
		default=None,
		on_delete=models.CASCADE,
		related_name="Post",
	)

	# Summary of notification
	verb = models.CharField(max_length=255)

	# Description of notification
	description = models.TextField(blank=True, null=True)

	# Serialize and store in data. Deserialize to get JSON.
	# Any extra data {in JSON(stored in serialized manner) format)}
	data = models.TextField(blank=True, null=True)

	# Time of creation of notification
	timestamp = models.DateTimeField(default=timezone.now)

	# Whether notification is unread or not
	unread = models.BooleanField(default=True, blank=False, db_index=True)

	def __str__(self):
		return self.verb

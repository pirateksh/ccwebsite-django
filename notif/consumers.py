import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from django.utils import timezone

# Importing models
from django.contrib.auth.models import User
from notif.models import Notification
from post.models import Post


"""
	@database_sync_to_async use this decorator above the method which will interact with database.
	So if we want to save the notification to database we will do kind of following - 

	@database_sync_to_async
	def create_notif(user, notif_msg, timestamp):
		return model.objects.create(user=user, notif_msg=notif_msg, timestamp=timestamp)

	# Calling above function
	await create_notif(user, msg, time)

"""




# class NoseyConsumer(AsyncJsonWebsocketConsumer):
# 	# This will 'listen' to the messages sent by django signals when user is created.

# 	async def connect(self):
# 		await self.accept()

# 		# Retrieving the channel layer.
# 		# Every channel has a unique name available as slef.channel_name.
# 		# We added our channel to 'gossip' group.
# 		await self.channel_layer.group_add("gossip", self.channel_name)

# 		print(f"Added {self.channel_name} channel to gossip")


# 	async def disconnect(self, *args, **kwargs):

# 		# We will remove ourselves from the group/broadcast channel.
# 		await self.channel_layer.group_discard("gossip", self.channel_name)

# 		print(f"Removed {self.channel_name} channel from gossip")


# 	# user.gossip type event defined in signals.py is automatically translated to user_gossip event.
# 	async def user_gossip(self, event):
# 		# As soon as we receive the gossip that new user has been added, we're to broadcast this event
# 		# to everybody else.
# 		await self.send_json(event)
# 		print(f"Got message {event} at {self.channel_name}")
# User = get_user_model()


class LikeNotificationConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		
		print("connect", event)

		await self.channel_layer.group_add("like_notif", self.channel_name)

		await self.send({
			"type": "websocket.accept",
		})

	async def websocket_receive(self, event):
		print("receive", event)

		# dict_string = event.get('text', None)
		# if dict_string is not None:
		# 	dict_ = json.loads(dict_string)
		# 	print("Message: ", dict_.get('message'))
		# 	print("Like Count: ", dict_.get('likeCount'))
		#
		# 	await self.send({
		# 		"type": "websocket.send",
		# 		"text": json.dumps(dict_)
		# 	})

	async def websocket_disconnect(self, event):
		print("disconnect", event)
		await self.channel_layer.group_discard("like_notif", self.channel_name)
		# raise StopConsumer

	async def notif_like(self, event):
		print("like_notif_send", event)

		await self.send({
			"type": "websocket.send",
			"text": event.get('text')
		})

		json_dict = json.loads(event.get('text'))

		recipient_username = json_dict.get('recipient_username')
		recipient = await self.get_user(recipient_username)
		# recipient = User.objects.get(username=recipient_username)

		sender_username = json_dict.get('sender_username')
		sender = await self.get_user(sender_username)
		# sender = User.objects.get(username=sender_username)

		post_pk = json_dict.get('post_pk', None)
		post = await self.get_post(post_pk)
		# post = Post.objects.get(pk=post_pk)

		verb = json_dict.get('verb')
		description = json_dict.get('description', None)
		data_dict = json_dict.get('data', None)
		data = json.dumps(data_dict)

		await self.create_notif(recipient, sender, verb, post, description, data)

	@database_sync_to_async
	def get_user(self, username_):
		return User.objects.get(username=username_)

	@database_sync_to_async
	def get_post(self, pk_):
		return Post.objects.get(pk=pk_)

	@database_sync_to_async
	def create_notif(self, recipient, sender, verb, post=None, description=None, data=None, *args, **kwargs):
		return Notification.objects.create(recipient=recipient,	sender=sender,	post=post, verb=verb, description=description,	data=data)


class NoseyConsumer(AsyncConsumer):

	# Whenever a Consumer is called, the event type(event['type']) is matched with method name
	# by replacing '.' with '_', and accordingly that method is called for that event.

	async def websocket_connect(self, event):
		print("connected", event)

		# Below code accepts the socket.
		await self.send({
			"type": "websocket.accept" 
		})

		# To get current user's name
		# me = self.scope['user']

		# To get some information from routing URL (eg: if URL was "user_profile/<userName>")
		# username = self.scope['url_route']['kwargs']['userName']
		# print(me)

		# await asyncio.sleep(10)

		await self.send({
			"type": "websocket.send",
			"text": "Hello World sent from NoseyConsumer"
		})

	async def websocket_receive(self, event):
		# Receives data form frontend. For eg: On form submission, data can be directed here.
		print("receive", event)

		text_data = event.get('text', None)

		if text_data is not None:
			# json.loads is same as JSON.parse() in JavaScript
			loaded_dict_data = json.loads(text_data)
			msg = loaded_dict_data.get('message')
			# print(msg)

			user = self.scope.get('user')
			username = "default"
			if user.is_authenticated:
				username = user.username

			my_response = {
				'message': msg,
				'username': username,
			}

			await self.send({
				"type": "websocket.send",
				# json.dumps() is like JSON.stringify of JavaScript
				"text": json.dumps(my_response),
			})

			# json.loads() loads the JSON.stringify string back to JSON format (Probably)

		"""
			'event' contains following data - 
			{'type': 'websocket.receive', 'text': '{"messgage":"Hello World from scripts.html"}'}
			Here 'type' maps with the name of function when a Consumer is called on any event.
			i.e. 'websocket.receive' maps with 'websocket_receive'.
			which means if we change name of function to 'websocket_receive2', then it will not work.
		"""

	async def websocket_disconnect(self, event):
		print("disconnected", event)

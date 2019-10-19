import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


"""
	@database_sync_to_async use this decorator above method which will interact with database.
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

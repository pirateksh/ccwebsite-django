from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, AllowedHostsOriginValidator

# AllowedHostOriginValidator - Only ALLOWED_HOSTS in settings.py can connect
# OriginValidator - We can have specific origin for just channels using this.

from notif.consumers import NoseyConsumer

application = ProtocolTypeRouter({
	"websocket": AllowedHostsOriginValidator(
			AuthMiddlewareStack(
				URLRouter(
					# Inside below list - similar to standard urls.py
					[
						# Consumer is similar to views in Django.
						path("notifications/", NoseyConsumer),
					]
				),
			)
	)
}) 
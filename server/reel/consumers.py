import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


logger = logging.getLogger(__name__)


class TwinedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "twined_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send the most recent message
        for changes in cache.get(self.room_name, default=list()):
            await self.send(text_data=changes)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket, broadcast to room group
    async def receive(self, text_data=None, bytes_data=None):

        # Append changes to the cache for this room, allowing us to flush all changes through to new connection
        # TODO Race condition exists here. Either rewrite automerge for python and keep a master record, or use
        #  a locking strategy enabling us to ensure all changes are recorded or use a synchronous websocketconsumer
        #  to properly persist the change history
        #  https://pypi.org/project/python-redis-lock/
        #  https://github.com/joanvila/aioredlock
        changes = cache.get(self.room_name, default=list())
        changes.append(text_data)
        cache.set(self.room_name, changes)
        data = {
            "type": "twined_message",
            "message_text": text_data,
            "message_bytes": bytes_data,
        }
        await self.channel_layer.group_send(self.room_group_name, data)

    # Receive message from room group, send to WebSocket
    async def twined_message(self, event):
        text_data = event["message_text"]
        await self.send(text_data=text_data)

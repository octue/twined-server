import json
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


logger = logging.getLogger(__name__)

MESSAGE_FIELDS = (
    "action",
    "reference",
    "value",
    "data",
    "status",
    "hints",
    "input_values",
    "twine",
    "configuration_values",
    "input_manifest",
    "configuration_manifest",
    "credentials",
    "children",
    "output_values",
    "output_manifest",
)


class ReelMessage:
    """ Class to manage incoming and outgoing messages
    """

    def __init__(self, src=None, **kwargs):
        """ Constructor for ServiceMessage
        """
        if src is not None:
            # Inbound from a src - overwrites any extras you give it
            kwargs = json.loads(src)
            # TODO schema based validation with no extra fields allowed

        if "action" not in kwargs.keys():
            raise Exception("No action specified")

        kwargs["status"] = kwargs.pop("status", "success")

        self.__dict__ = dict((k, kwargs.get(k, None)) for k in MESSAGE_FIELDS)

    def serialise(self):
        """ Serialise self to a string
        """
        to_serialise = dict((k, getattr(self, k)) for k in MESSAGE_FIELDS if getattr(self, k) is not None)
        return json.dumps(to_serialise)

    def send(self, obj):
        """ Send this message to an individual channel name
        """
        serialised = self.serialise()
        logger.debug("Sending ReelMessage to channel '%s': %s", obj, serialised)
        obj.send(serialised)

    def group_send(self, group_name, message_type="reel_message"):
        """ Send this message to a group over channels
        """
        serialised = self.serialise()
        logger.debug("Group sending ReelMessage: %s", serialised)
        async_to_sync(channel_layer.group_send)(group_name, {"type": message_type, "message": serialised})

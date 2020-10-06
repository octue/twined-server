import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from reel.messages import ReelMessage


logger = logging.getLogger(__name__)


class ServiceConsumer(WebsocketConsumer):
    """ A high-level consumer allowing subscription to service messages and the current twine

    ~~ When in danger or in doubt, run in circles, scream and shout ~~

    """

    def connect(self):
        """ Accept connection to the service, and send twine to the client as acknowledgement
        """

        # Add this channel to the service group
        async_to_sync(self.channel_layer.group_add)("service", self.channel_name)

        # Accept the connection
        self.accept()

        # Send the twine for this service to the connected client
        self._send_twine()

    def disconnect(self, code):
        """ Accept a disconnection from the service gracefully
        """
        async_to_sync(self.channel_layer.group_discard)("service", self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        """ Receive service instructions from WebSocket
        """

        # Get the incoming message data
        try:
            message = ReelMessage(src=text_data)
        except Exception as e:
            self.send(text_data=ReelMessage(status="error", hints="Unable to understand your message").serialise())
            raise e

        # Attempt to respond
        try:
            if message.action == "ping":
                # Play ping pong with anybody who wants to know the service is live
                ReelMessage(
                    action="pong", status="success", hints="U wanna play? I can pong your ping all day..."
                ).send(self)
                return

        except Exception as e:
            logger.error(e.args[0])
            ReelMessage(action=message.action, status="error",).send(self)
            return

    def service_message(self, event):
        """ Handle sending of service messages to all clients
        """
        text_data = event["message_text"]
        self.send(text_data=text_data)

    def _send_twine(self):
        """ Refresh the client with everything it needs to know about the twine and the analyses it has going on
        """

        # TODO replace with real one for current service
        fake_twine = """{
            "configuration_values_schema": {
                "$schema": "http://json-schema.org/2019-09/schema#",
                "title": "The example configuration form",
                "description": "The configuration strand of an example twine",
                "type": "object",
                "properties": {
                    "n_iterations": {
                        "description": "An example of an integer configuration variable, called 'n_iterations'.",
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5
                    }
                }
            },
            "input_values_schema": {
                "$schema": "http://json-schema.org/2019-09/schema#",
                "title": "Input Values",
                "description": "The input values strand of an example twine, with a required height value",
                "type": "object",
                "properties": {
                    "height": {
                        "description": "An example of an integer value called 'height'",
                        "type": "integer",
                        "minimum": 2
                    }
                },
                "required": ["height"]
            },
            "output_values_schema": {
                "title": "Output Values",
                "description": "The output values strand of an example twine",
                "type": "object",
                "properties": {
                    "width": {
                        "description": "An example of an integer value called 'result'",
                        "type": "integer",
                        "minimum": 2
                    }
                }
            }
        }
        """
        ReelMessage(action="connect", twine=fake_twine).send(self)

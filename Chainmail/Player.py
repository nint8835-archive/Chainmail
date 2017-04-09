from .MessageBuilder import MessageBuilder
from . import Wrapper


class Player(object):

    def __init__(self, name: str, uuid: str, wrapper: "Wrapper.Wrapper"):
        """
        Initializes a new player
        :param name: The username of the player
        :param uuid: The uuid of the player
        :param wrapper: The wrapper the player belongs to
        """
        self.username = name
        self.uuid = uuid
        self.wrapper = wrapper
        self.connected = False
        self.is_op = False

    def send_message(self, builder: MessageBuilder):
        """
        Sends a message to this player
        :param builder: The message to send
        """
        self.wrapper.write_line(builder.generate_command(self))

    def op(self):
        """
        Ops this player
        """
        self.wrapper.write_line(f"op {self.username}")

    def deop(self):
        """
        Deops this player
        """
        self.wrapper.write_line(f"deop {self.username}")

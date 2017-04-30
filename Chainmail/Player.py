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

    def teleport_to(self, player: "Player"):
        """
        Teleports this player to another player
        :param player: The player to teleport this player to
        """
        self.wrapper.write_line(f"tp {self.username} {player.username}")

    def kick(self, reason: str=""):
        """
        Kicks this player from the server
        :param reason: The optional reason for this kick
        """
        if reason == "":
            self.wrapper.write_line(f"kick {self.username}")
        else:
            self.wrapper.write_line(f"kick {self.username} {reason}")

    def ban(self, reason: str=""):
        """
        Bans this player from the server
        :param reason: The optional reason for this ban
        """
        if reason == "":
            self.wrapper.write_line(f"ban {self.username}")
        else:
            self.wrapper.write_line(f"ban {self.username} {reason}")

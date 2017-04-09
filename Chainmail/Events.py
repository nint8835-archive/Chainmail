from enum import Enum, auto

from typing import Match, List

from .Player import Player


class Events(Enum):
    CONSOLE_OUTPUT = auto()
    VERSION_DISCOVERED = auto()
    SERVER_STOPPED = auto()
    SERVER_STARTED = auto()
    SERVER_READY = auto()
    UUID_DISCOVERED = auto()
    PLAYER_CONNECTED = auto()
    PLAYER_DISCONNECTED = auto()
    MESSAGE_SENT = auto()
    USER_OPPED = auto()
    USER_DEOPPED = auto()
    COMMAND_SENT = auto()


class Event(object):
    pass


class ConsoleOutputEvent(Event):

    def __init__(self, level: int, output: str):
        """
        Initializes a new ConsoleOutputEvent
        :param level: The log level of the output
        :param output: The text of the output
        """
        self.level = level
        self.output = output


class VersionDiscoveredEvent(Event):

    def __init__(self, version: str):
        """
        Initializes a new VersionDiscoveredEvent
        :param version: The version of the server
        """
        self.version = version


class ServerStoppedEvent(Event):
    pass


class ServerStartedEvent(Event):
    pass


class ServerReadyEvent(Event):
    pass


class UUIDDiscoveredEvent(Event):

    def __init__(self, username: str, uuid: str):
        """
        Initializes a new UUIDDiscoveredEvent
        :param username: The username that the uuid was discovered for
        :param uuid: The user's uuid
        """
        self.username = username
        self.uuid = uuid


class PlayerConnectedEvent(Event):

    def __init__(self, username: str, player: Player):
        """
        Initializes a new PlayerConnectedEvent
        :param username: The username of the player that connected
        :param player: The player that connected
        """
        self.username = username
        self.player = player


class PlayerDisconnectedEvent(Event):

    def __init__(self, username: str, player: Player):
        """
        Initializes a new PlayerDisconnectedEvent
        :param username: The username of the player that disconnected
        :param player: The player that disconnected
        """
        self.username = username
        self.player = player


class MessageSentEvent(Event):

    def __init__(self, username: str, message: str, player: Player):
        """
        Initializes a new MessageSentEvent
        :param username: The username of the player that sent the message
        :param message: The message that was sent
        :param player: The player that sent the message
        """
        self.username = username
        self.message = message
        self.player = player


class CommandSentEvent(MessageSentEvent):

    def __init__(self, username: str, message: str, player: Player, args: List[Match[str]]):
        """
        Initializes a new CommandSentEvent
        :param username: The username of the player that sent the command
        :param message: The message containing the command
        :param player: The player that sent the command
        :param args: The args for the command
        """
        super().__init__(username, message, player)
        self.args = args


class UserOppedEvent(Event):

    def __init__(self, username: str, player: Player):
        """
        Initializes a new UserOppedEvent
        :param username: The username of the player that got opped
        :param player: The player that got opped
        """
        self.username = username
        self.player = player


class UserDeoppedEvent(Event):

    def __init__(self, username: str, player: Player):
        """
        Initializes a new UserDeoppedEvent
        :param username: The username of the player that got deopped
        :param player: The player that got deopped
        """
        self.username = username
        self.player = player

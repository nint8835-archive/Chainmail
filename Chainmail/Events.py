from enum import Enum, auto

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


class Event(object):
    pass


class ConsoleOutputEvent(Event):

    def __init__(self, level: int, output: str):
        self.level = level
        self.output = output


class VersionDiscoveredEvent(Event):

    def __init__(self, version: str):
        self.version = version


class ServerStoppedEvent(Event):
    pass


class ServerStartedEvent(Event):
    pass


class ServerReadyEvent(Event):
    pass


class UUIDDiscoveredEvent(Event):

    def __init__(self, username: str, uuid: str):
        self.username = username
        self.uuid = uuid


class PlayerConnectedEvent(Event):

    def __init__(self, username: str, player: Player):
        self.username = username
        self.player = player


class PlayerDisconnectedEvent(Event):

    def __init__(self, username: str, player: Player):
        self.username = username
        self.player = player


class MessageSentEvent(Event):

    def __init__(self, username: str, message: str, player: Player):
        self.username = username
        self.message = message
        self.player = player


class UserOppedEvent(Event):

    def __init__(self, username: str, player: Player):
        self.username = username
        self.player = player


class UserDeoppedEvent(Event):

    def __init__(self, username: str, player: Player):
        self.username = username
        self.player = player

from typing import Dict, Optional

from .Player import Player
from . import Wrapper


class PlayerManager(object):

    def __init__(self, wrapper: "Wrapper.Wrapper"):
        """
        Initializes a new player manager
        :param wrapper: The wrapper this player manager belongs to
        """
        self._wrapper = wrapper
        self._uuids = {}  # type: Dict[str, str]
        self._players = []  # type: List[Player]

    def set_uuid(self, username: str, uuid: str):
        """
        Sets the uuid assigned to a username
        :param username: The username the uuid belongs to
        :param uuid: The uuid
        """
        self._uuids[username] = uuid

    def get_uuid(self, username: str) -> Optional[str]:
        """
        Gets the uuid belonging to a username
        :param username: The username to get the uuid for
        :return: The uuid belonging to the username
        """
        if username in self._uuids:
            return self._uuids[username]
        return None

    def get_player(self, username: str) -> Optional[Player]:
        """
        Gets a player from a username
        :param username: The player's username
        :return: The player
        """
        for player in self._players:
            if player.username == username:
                return player
        return None

    def add_player(self, username: str):
        """
        Initializes and registers a new player
        :param username: The player's username
        """
        if self.get_player(username) is None:
            self._players.append(Player(username, self.get_uuid(username), self._wrapper))
            for op in self._wrapper.ops:
                if op == self.get_uuid(username):
                    self.get_player(username).is_op = True

    def set_player_disconnected(self, username: str):
        """
        Marks a player as disconnected and removes them from the internal player list
        :param username: The player's username
        """
        user = self.get_player(username)
        user.connected = False

        self._players.remove(user)

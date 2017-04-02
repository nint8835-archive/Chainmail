from typing import Dict

from .Player import Player


class PlayerManager(object):

    def __init__(self):
        self._uuids = {}  # type: Dict[str, str]
        self._players = []  # type: List[Player]

    def set_uuid(self, username: str, uuid: str):
        self._uuids[username] = uuid

    def get_uuid(self, username: str) -> str:
        if username in self._uuids:
            return self._uuids[username]
        return None

    def get_player(self, username: str) -> Player:
        for player in self._players:
            if player.name == username:
                return player
        return None

    def add_player(self, username: str):
        if self.get_player(username) is None:
            self._players.append(Player(username, self.get_uuid(username)))

    def set_player_disconnected(self, username: str):
        user = self.get_player(username)
        user.connected = False

        self._players.remove(user)
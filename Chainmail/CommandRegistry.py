import re
import threading

from typing import List

from .Events import MessageSentEvent, CommandSentEvent
from .Player import Player


class Command(object):

    def __init__(self, name: str, regex: str, description: str, handler: classmethod, requires_op: bool):
        self.name = name
        self.regex = re.compile(regex)
        self.description = description
        self.handler = handler
        self.requires_op = requires_op

    def can_run_command(self, player: Player) -> bool:
        return not self.requires_op or (player.is_op and self.requires_op)

    def matches(self, event: MessageSentEvent) -> bool:
        return self.regex.match(event.message)

    def __call__(self, event: MessageSentEvent):
        threading.Thread(target=self.handler, args=(CommandSentEvent(event.player.username, event.message, event.player, self.regex.findall(event.message)), )).start()


class CommandRegistry(object):
    def __init__(self):
        self._commands = []  # type: List[Command]

    def get_accessible_commands(self, player: Player) -> List[Command]:
        return [i for i in self._commands if i.can_run_command(player)]

    def register_command(self, name: str, regex: str, description: str, handler: classmethod, requires_op: bool = False) -> Command:
        command = Command(name, regex, description, handler, requires_op)
        self._commands.append(command)
        return command

    def process_command(self, event: MessageSentEvent):
        for command in self._commands:
            if command.matches(event) and command.can_run_command(event.player):
                command(event)

    def clear_commands(self):
        self._commands = []


import re
import threading

from typing import List

from .Events import MessageSentEvent, CommandSentEvent
from .Player import Player


class Command(object):

    def __init__(self, name: str, regex: str, description: str, handler: classmethod, requires_op: bool) -> None:
        """
        Initializes this command
        :param name: The name for this command. Typically used for command lists
        :param regex: The regex for detecting this command
        :param description: The description for this command
        :param handler: The handler for this command
        :param requires_op: Whether or not this command requires op
        """
        self.name = name
        self.regex = re.compile(regex)
        self.description = description
        self.handler = handler
        self.requires_op = requires_op

    def can_run_command(self, player: Player) -> bool:
        """
        Returns whether or not a player can run this command
        :param player: The player to check for
        :return: Whether the player can run the command
        """
        return not self.requires_op or (player.is_op and self.requires_op)

    def matches(self, event: MessageSentEvent) -> bool:
        """
        Returns whether or not the message contained within an event matches the regex belonging to this command
        :param event: The event to get the message from
        :return: Whether the message matches
        """
        return self.regex.match(event.message)

    def __call__(self, event: MessageSentEvent) -> None:
        """
        Runs this command
        :param event: The event that triggered this command
        """
        threading.Thread(target=self.handler, args=(CommandSentEvent(event.player.username, event.message, event.player, self.regex.findall(event.message)), )).start()


class CommandRegistry(object):

    def __init__(self) -> None:
        """
        Initializes the command registry
        """
        self._commands = []  # type: List[Command]

    def get_accessible_commands(self, player: Player) -> List[Command]:
        """
        Returns all commands that the player has access to
        :param player: The player to check for
        :return: The commands the player can access
        """
        return [i for i in self._commands if i.can_run_command(player)]

    def register_command(self, name: str, regex: str, description: str, handler: classmethod, requires_op: bool = False) -> Command:
        """
        Initializes and registers a new command
        :param name: The name for the command. Typically used for command lists
        :param regex: The regex for detecting the command
        :param description: The description for the command
        :param handler: The handler for the command
        :param requires_op: Whether or not the command requires op
        :return: The command object
        """
        command = Command(name, regex, description, handler, requires_op)
        self._commands.append(command)
        return command

    def process_command(self, event: MessageSentEvent):
        """
        Takes a MessageSentEvent and runs all commands matching the message content
        :param event: The event to check
        """
        for command in self._commands:
            if command.matches(event) and command.can_run_command(event.player):
                command(event)

    def clear_commands(self) -> None:
        """
        Clears the command list
        """
        self._commands = []


import difflib
import json
import logging
import os
import re
from typing import Dict, Pattern

from . import Wrapper
from .Events import *

RegexMatches = List[Match[str]]


class TextProcessor(object):

    def __init__(self, wrapper: "Wrapper.Wrapper"):
        """
        Initializes a new text processor
        :param wrapper: The wrapper that this text processor belongs to
        """
        self._wrapper = wrapper
        self.regexes = []  # type: List[Dict[str, Pattern[str]]]
        self.loaded_files = []
        self._logger = logging.getLogger("TextProcessor")
        self.server_log = logging.getLogger("MinecraftServer")

        self._regex_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regex")

        self.load_version("generic")

    @staticmethod
    def get_json_files(path: str):
        """
        Returns a generator giving all json files for a given path
        :param path: The path
        """
        for file in os.listdir(path):
            if file.endswith(".json"):
                yield os.path.join(path, file)

    def load_version(self, version: str) -> None:
        """
        Loads the regex json files for a version
        :param version: The version to load the files for
        """
        self._logger.debug(f"Loading regexes for version {version}...")
        directory = os.path.join(self._regex_path, version)
        if os.path.isdir(directory):
            for file in self.get_json_files(directory):
                self.process_file(file)
        else:
            self._logger.warning(f"Version {version} not found.")
            close = difflib.get_close_matches(version, os.listdir(self._regex_path))
            if len(close) != 0:
                self._logger.warning(f"Using closest variation: {close[0]}. This may cause compatibility issues.")
                self.load_version(close[0])
            else:
                self._logger.error("No close variation found. Not attempting to load.")
                return
        self._logger.debug("Regexes loaded.")

    def process_file(self, path: str) -> None:
        if path in self.loaded_files:
            return
        with open(path) as f:
            data = json.load(f)

            for item in data:
                if "import" in item:
                    self.process_file(os.path.join(self._regex_path, item["import"]))
                else:
                    self.regexes.append({
                        "type": item["type"],
                        "regex": re.compile(item["regex"])
                    })

                    self._logger.debug(f"Loaded new regex for {item['type']}")
            self.loaded_files.append(path)

    def unspecified_handler(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a regex with no handler
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._logger.warning(f"No handler specified for {event_type} (Matches: {', '.join(matches)}")

    def console_output(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a console_output regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self.server_log.log(getattr(logging, matches[0][0]), matches[0][1])
        self._wrapper.EventManager.dispatch_event(Events.CONSOLE_OUTPUT, ConsoleOutputEvent(matches[0][0],
                                                                                            matches[0][1]))

    def version_discovered(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a version_discovered regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._logger.debug(f"Version detected: {matches[0]}")
        self._wrapper.version = matches[0]
        self.load_version(matches[0])
        self._wrapper.EventManager.dispatch_event(Events.VERSION_DISCOVERED, VersionDiscoveredEvent(matches[0]))

    def server_ready(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a server_ready regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._wrapper.EventManager.dispatch_event(Events.SERVER_READY, ServerReadyEvent())

    def uuid_found(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a uuid_found regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._wrapper.PlayerManager.set_uuid(matches[0][0], matches[0][1])
        self._wrapper.EventManager.dispatch_event(Events.UUID_DISCOVERED, UUIDDiscoveredEvent(matches[0][0], matches[0][1]))

    def player_connected(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a player_connected regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._wrapper.PlayerManager.add_player(matches[0])
        self._wrapper.EventManager.dispatch_event(Events.PLAYER_CONNECTED, PlayerConnectedEvent(matches[0], self._wrapper.PlayerManager.get_player(matches[0])))

    def player_disconnected(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a player_disconnected regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._wrapper.PlayerManager.set_player_disconnected(matches[0])
        self._wrapper.EventManager.dispatch_event(Events.PLAYER_DISCONNECTED, PlayerDisconnectedEvent(matches[0], self._wrapper.PlayerManager.get_player(matches[0])))

    def message_sent(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a message_sent regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        event = MessageSentEvent(matches[0][0], matches[0][1], self._wrapper.PlayerManager.get_player(matches[0][0]))
        self._wrapper.EventManager.dispatch_event(Events.MESSAGE_SENT, event)
        self._wrapper.CommandRegistry.process_command(event)

    def user_opped(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a user_opped regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._wrapper.PlayerManager.get_player(matches[0]).is_op = True
        self._wrapper.ops.append(self._wrapper.PlayerManager.get_uuid(matches[0]))
        self._wrapper.EventManager.dispatch_event(Events.USER_OPPED, UserOppedEvent(matches[0], self._wrapper.PlayerManager.get_player(matches[0])))

    def user_deopped(self, event_type: str, matches: RegexMatches):
        """
        Processes the data returned by a user_deopped regex
        :param event_type: The type of event
        :param matches: The regex matches
        """
        self._wrapper.PlayerManager.get_player(matches[0]).is_op = False
        self._wrapper.ops.remove(self._wrapper.PlayerManager.get_uuid(matches[0]))
        self._wrapper.EventManager.dispatch_event(Events.USER_DEOPPED, UserDeoppedEvent(matches[0], self._wrapper.PlayerManager.get_player(matches[0])))

    def process_line(self, line: str):
        """
        Processes a line of server output
        :param line: The server output
        """
        line = line.replace("\r\n", "\n").rstrip("\n")
        print(line)
        for regex in self.regexes:
            if regex["regex"].match(line):
                getattr(self, regex["type"], self.unspecified_handler)(regex["type"], regex["regex"].findall(line))

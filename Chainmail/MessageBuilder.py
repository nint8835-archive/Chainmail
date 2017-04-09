import json
from enum import Enum
from typing import List

from . import Wrapper, Player


class Colours(Enum):
    black = "black"
    dark_blue = "dark_blue"
    dark_green = "dark_green"
    dark_aqua = "dark_aqua"
    dark_red = "dark_red"
    dark_purple = "dark_purple"
    gold = "gold"
    gray = "gray"
    dark_gray = "dark_gray"
    blue = "blue"
    green = "green"
    aqua = "aqua"
    red = "red"
    light_purple = "light_purple"
    yellow = "yellow"
    white = "white"


class HoverEvent(object):

    # noinspection PyMethodMayBeStatic
    def to_dict(self) -> dict:
        """
        Returns a dict for this HoverEvent
        :return: The dict
        """
        return {}


class MessageBuilder(object):

    def __init__(self):
        """
        Initializes a new message builder
        """
        self.fields = []

    def add_field(self, text: str, colour: Colours=Colours.white, bold: bool=False, italic: bool=False, underlined: bool=False, strikethrough: bool=False, obfuscated: bool=False, hover_event: HoverEvent=HoverEvent(), insertion: str="",  **kwargs):
        """
        Adds a new field to the message builder
        :param text: The text of the field
        :param colour: The colour of the field
        :param bold: Whether or not this field is bold
        :param italic: Whether or not this field is italic
        :param underlined: Whether or not this field is underlined
        :param strikethrough: Whether or not this field has a strikethrough
        :param obfuscated: Whether or not this field is obfuscated
        :param hover_event: The hover event for this field
        :param insertion: What will be inserted when you shift-click this field
        :param kwargs: Any additional arguments
        """
        self.fields.append({
            "text": text,
            "color": colour.value,
            "bold": bold,
            "italic": italic,
            "underlined": underlined,
            "strikethrough": strikethrough,
            "obfuscated": obfuscated,
            "hoverEvent": hover_event.to_dict(),
            "insertion": insertion,
            **kwargs
        })

    def send(self, destination: "Player.Player"):
        """
        Sends this message to a player
        :param destination: The player to sent this message to
        """
        destination.send_message(self)

    def generate_command(self, player: "Player.Player") -> str:
        """
        Generates the command to be used to send this message
        :param player: The player to send the message to
        :return: The command
        """
        return f"tellraw {player.username} {json.dumps(self.fields)}"

    def send_to_group(self, group: List["Player.Player"]):
        """
        Sends this message to a group of people
        :param group: The people to send this to
        """
        for player in group:
            player.send_message(self)


class TextHoverEvent(HoverEvent):

    def __init__(self):
        """
        Initializes a new TextHoverEvent
        """
        self.builder = MessageBuilder()

    def add_field(self, text: str, colour: Colours=Colours.white, bold: bool=False, italic: bool=False, underlined: bool=False, strikethrough: bool=False, obfuscated: bool=False):
        """
        Adds a new field to the message builder
        :param text: The text of the field
        :param colour: The colour of the field
        :param bold: Whether or not this field is bold
        :param italic: Whether or not this field is italic
        :param underlined: Whether or not this field is underlined
        :param strikethrough: Whether or not this field has a strikethrough
        :param obfuscated: Whether or not this field is obfuscated
        """
        self.builder.add_field(text=text,
                               colour=colour,
                               bold=bold,
                               italic=italic,
                               underlined=underlined,
                               strikethrough=strikethrough,
                               obfuscated=obfuscated)

    def to_dict(self) -> dict:
        """
        Returns a dict for this HoverEvent
        :return: The dict
        """
        return {
            "action": "show_text",
            "value": {"text": "",
                      "extra": [self.builder.fields]}
        }

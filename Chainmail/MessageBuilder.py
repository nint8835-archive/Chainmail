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
        return {}


class MessageBuilder(object):

    def __init__(self):
        self.fields = []

    def add_field(self, text: str, colour: Colours=Colours.white, bold: bool=False, italic: bool=False, underlined: bool=False, strikethrough: bool=False, obfuscated: bool=False, hover_event: HoverEvent=HoverEvent(), insertion: str="",  **kwargs):
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
        destination.send_message(self)

    def generate_command(self, player: "Player.Player") -> str:
        return f"tellraw {player.username} {json.dumps(self.fields)}"

    def send_to_group(self, group: List["Player.Player"]):
        for player in group:
            player.send_message(self)


class TextHoverEvent(HoverEvent):

    def __init__(self):
        self.builder = MessageBuilder()

    def add_field(self, text: str, colour: Colours=Colours.white, bold: bool=False, italic: bool=False, underlined: bool=False, strikethrough: bool=False, obfuscated: bool=False):
        self.builder.add_field(text=text,
                               colour=colour,
                               bold=bold,
                               italic=italic,
                               underlined=underlined,
                               strikethrough=strikethrough,
                               obfuscated=obfuscated)

    def to_dict(self) -> dict:
        return {
            "action": "show_text",
            "value": {"text": "",
                      "extra": [self.builder.fields]}
        }

import json
from enum import Enum

from . import Wrapper


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


class MessageBuilder(object):

    def __init__(self, wrapper: "Wrapper.Wrapper"):
        self.wrapper = wrapper
        self.fields = []

    def add_field(self, text: str, colour: Colours=Colours.white, bold: bool=False, italic: bool=False, underlined: bool=False, strikethrough: bool=False, obfuscated: bool = False):
        self.fields.append({
            "text": text,
            "color": colour.value,
            "bold": bold,
            "italic": italic,
            "underlined": underlined,
            "strikethrough": strikethrough,
            "obfuscated": obfuscated
        })

    def send(self, destination: str):
        self.wrapper.write_line(f"tellraw {destination} {json.dumps(self.fields)}")

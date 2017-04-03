from .MessageBuilder import MessageBuilder
from . import Wrapper


class Player(object):

    def __init__(self, name: str, uuid: str, wrapper: "Wrapper.Wrapper"):
        self.username = name
        self.uuid = uuid
        self.wrapper = wrapper
        self.connected = False
        self.is_op = False

    def send_message(self, builder: MessageBuilder):
        builder.send(self.username)

    def op(self):
        self.wrapper.write_line(f"op {self.username}")

    def deop(self):
        self.wrapper.write_line(f"deop {self.username}")

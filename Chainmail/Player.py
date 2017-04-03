from .MessageBuilder import MessageBuilder


class Player(object):

    def __init__(self, name: str, uuid: str):
        self.name = name
        self.uuid = uuid
        self.connected = False
        self.is_op = False

    def send_message(self, builder: MessageBuilder):
        builder.send(self.name)

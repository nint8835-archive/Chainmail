from Chainmail.Events import Events, PlayerConnectedEvent
from Chainmail.MessageBuilder import MessageBuilder, Colours
from Chainmail.Plugin import ChainmailPlugin


class AutoOP(ChainmailPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest, wrapper)

        self.wrapper.EventManager.register_handler(Events.PLAYER_CONNECTED, self.handle_player_connected)

    def handle_player_connected(self, event: PlayerConnectedEvent):
        if len(self.wrapper.ops) == 0:
            self.logger.info(f"Server has no ops registered. Opping {event.username}.")
            event.player.op()
            message = MessageBuilder(self.wrapper)
            message.add_field("You have been granted op status for being the first player.", Colours.gold)
            event.player.send_message(message)

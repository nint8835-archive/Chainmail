from Chainmail import Wrapper
from Chainmail.Events import Events, PlayerConnectedEvent
from Chainmail.MessageBuilder import MessageBuilder, Colours, TextHoverEvent
from Chainmail.Plugin import ChainmailPlugin


class AutoOP(ChainmailPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest, wrapper)

        self.wrapper.EventManager.register_handler(Events.PLAYER_CONNECTED, self.handle_player_connected)
        hover = TextHoverEvent()
        hover.add_field("Since Chainmail does not have a method to interact with the console at the moment, the server will auto-op the first player that joins.")
        self.opped_message = MessageBuilder()
        self.opped_message.add_field("You have been granted op status.", Colours.gold)
        self.opped_message.add_field(" [INFO]", Colours.blue, bold=True, hover_event=hover)

    def handle_player_connected(self, event: PlayerConnectedEvent):
        if len(self.wrapper.ops) == 0:
            self.logger.info(f"Server has no ops registered. Opping {event.username}.")
            event.player.op()
            event.player.send_message(self.opped_message)

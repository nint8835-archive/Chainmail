import traceback

from Chainmail.Events import MessageSentEvent, Events
from Chainmail.Plugin import ChainmailPlugin


class TestPlugin(ChainmailPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest, wrapper)

        self.wrapper.EventManager.register_handler(Events.MESSAGE_SENT, self.handle_message)

    def handle_message(self, event: MessageSentEvent):
        if event.message == "!op":
            self.wrapper.write_line(f"op {event.username}")
            self.logger.info(f"Gave op status to {event.username}!")
        elif event.message == "!deop":
            self.wrapper.write_line(f"deop {event.username}")
            self.logger.info(f"Took away op status from {event.username}")

        elif event.message.startswith("!eval"):
            args = event.message.split(" ")
            if len(args) == 1:
                self.wrapper.write_line("say Usage: !exec <code>")
            else:
                code = " ".join(args[1:])

                try:
                    result = eval(code)
                except:
                    result = traceback.format_exc(1)

                self.wrapper.write_line(f"say Result: {result}")


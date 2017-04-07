import traceback

from Chainmail.Events import CommandSentEvent
from Chainmail.MessageBuilder import MessageBuilder, Colours
from Chainmail.Plugin import ChainmailPlugin


class TestPlugin(ChainmailPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest, wrapper)

        self.eval_usage_message = MessageBuilder(self.wrapper)
        self.eval_usage_message.add_field("Usage: ", colour=Colours.red, bold=True)
        self.eval_usage_message.add_field("!exec <code>", colour=Colours.gold)

        self.eval = self.wrapper.CommandRegistry.register_command("!eval", "^!eval (.+)$", "Evaluates Python expressions.", self.command_eval, True)
        self.eval_usage = self.wrapper.CommandRegistry.register_command("!eval", "^!eval$", "Displays the usage message.", self.command_eval_usage, True)

    def command_eval(self, event: CommandSentEvent):
        code = event.args[0]
        try:
            result = str(eval(code))
            error = False
        except:
            result = traceback.format_exc(1)
            error = True

        builder = MessageBuilder(self.wrapper)
        colour = Colours.green if not error else Colours.red
        builder.add_field("Result: ", colour=Colours.gold)
        builder.add_field(result, colour=colour)
        event.player.send_message(builder)

    def command_eval_usage(self, event: CommandSentEvent):
        event.player.send_message(self.eval_usage_message)

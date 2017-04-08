from Chainmail.Events import CommandSentEvent
from Chainmail.MessageBuilder import MessageBuilder, Colours
from Chainmail.Plugin import ChainmailPlugin


class ChainmailEssentials(ChainmailPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest, wrapper)

        self.commands_no_args = self.wrapper.CommandRegistry.register_command("!commands", "^!commands$", "Lists commands accessible to a user.", self.command_commands)

    def command_commands(self, event: CommandSentEvent):
        commands = self.wrapper.CommandRegistry.get_accessible_commands(event.player)
        builder = MessageBuilder(self.wrapper)
        seen_commands = []
        for command in commands:
            if command.name not in seen_commands:
                seen_commands.append(command.name)
                builder.add_field(f"{command.name}: ", Colours.red)
                suffix = "\n" if command != commands[-1] and command.name != commands[-1].name else ""
                builder.add_field(f"{command.description}{suffix}", Colours.gold)
        event.player.send_message(builder)

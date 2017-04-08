from Chainmail.Events import CommandSentEvent
from Chainmail.MessageBuilder import MessageBuilder, Colours
from Chainmail.Plugin import ChainmailPlugin


class ChainmailEssentials(ChainmailPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest, wrapper)

        self.commands = self.wrapper.CommandRegistry.register_command("!commands", "^!commands$", "Lists commands accessible to a user.", self.command_commands)
        self.plugins = self.wrapper.CommandRegistry.register_command("!plugins", "^!plugins$", "Lists all loaded plugins.", self.command_plugins)

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

    def command_plugins(self, event: CommandSentEvent):
        plugins = self.wrapper.plugin_manager.get_all_plugins()
        builder = MessageBuilder(self.wrapper)

        for plugin in plugins:
            if self.wrapper.plugin_manager.get_plugin_loaded(plugin["manifest"]["name"]):
                builder.add_field(f"{plugin['manifest']['name']}\n", Colours.blue)
                builder.add_field("    Developer: ", Colours.red)
                builder.add_field(f"{plugin['manifest']['developer']}\n", Colours.blue)
                suffix = "\n" if plugin != plugins[-1] else ""
                builder.add_field("    Version: ", Colours.red)
                builder.add_field(f"{plugin['manifest']['version']}{suffix}", Colours.blue)

        event.player.send_message(builder)

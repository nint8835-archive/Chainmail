import json
import logging
import os
import shlex
import subprocess
import sys
import threading

import jigsaw

from .CommandRegistry import CommandRegistry
from .Events import ServerStartedEvent, Events, ServerStoppedEvent
from .EventManager import EventManager
from .PlayerManager import PlayerManager
from .Plugin import ChainmailPlugin
from .TextProcessor import TextProcessor


class Wrapper(threading.Thread):

    def __init__(self, jar="minecraft_server.jar", max_ram="2G", min_ram="256M", log_level=logging.INFO):
        """
        Initializes the wrapper
        :param jar: The name of the minecraft server jar file
        :param max_ram: The maximum ram for the java vm
        :param min_ram: The minimum ram for the java vm
        :param log_level: The log lever for all internal loggers
        """
        super().__init__()
        logging.basicConfig(format="{%(asctime)s} (%(name)s) [%(levelname)s]: %(message)s",
                            datefmt="%x, %X",
                            level=log_level)
        self._logger = logging.getLogger("Chainmail")

        self.TextProcessor = TextProcessor(self)
        self.EventManager = EventManager()
        self.CommandRegistry = CommandRegistry()
        self.PlayerManager = PlayerManager(self)

        self.wrapper_running = True

        self.server_data_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, "server"))
        if not os.path.isdir(self.server_data_path):
            self._logger.error("Server data path does not exist, creating now.")
            os.mkdir(self.server_data_path)
            self._logger.info("Server data path created. Please place the minecraft jar in this folder.")
            sys.exit(1)

        os.chdir(self.server_data_path)
        self._command = shlex.split(f"java -Xmx{max_ram} -Xms{min_ram} -jar {jar} nogui")

        if not os.path.isfile(os.path.join(self.server_data_path, jar)):
            self._logger.error(f"The specified jar file, {jar}, could not be found in the server directory.")
            sys.exit(1)

        self._logger.debug("Loading OPs...")
        self.ops = []
        if os.path.isfile(os.path.join(self.server_data_path, "ops.json")):
            with open(os.path.join(self.server_data_path, "ops.json")) as f:
                ops = json.load(f)
                for op in ops:
                    self.ops.append(op["uuid"])
        self._logger.debug("OPs loaded")

        self.plugin_manager = jigsaw.PluginLoader(
            (os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, "plugins")),),
            log_level,
            ChainmailPlugin
        )

        self._logger.debug("Loading manifests...")
        self.plugin_manager.load_manifests()
        self._logger.debug("Manifests loaded.")

        self._logger.debug("Loading plugins...")
        self.plugin_manager.load_plugins(self)
        self._logger.debug("Plugins loaded.")

        self._server_process = None  # type: subprocess.Popen
        self.version = "UNKNOWN"

        self._logger.debug("Wrapper initialized.")

    def start_server(self):
        """
        Starts the server
        """
        self._logger.info("Starting server...")
        self._server_process = subprocess.Popen(self._command,
                                                stdout=subprocess.PIPE,
                                                stdin=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
        self.EventManager.dispatch_event(Events.SERVER_STARTED, ServerStartedEvent())
        self._logger.info("Server started.")

    def write_line(self, line: str):
        """
        Writes a line to the server's console input
        :param line: 
        """
        self._server_process.stdin.write(f"{line}\n".encode(sys.stdin.encoding))
        self._server_process.stdin.flush()

    def run(self) -> None:
        """
        Handles the running of the server
        """

        self.start_server()

        while self.wrapper_running:
            return_code = self._server_process.poll()
            if return_code is not None:
                self._logger.info("Server no longer running.")
                self.EventManager.dispatch_event(Events.SERVER_STOPPED, ServerStoppedEvent())
                self.wrapper_running = False
                return

            out = self._server_process.stdout.readline().decode("utf-8")
            self.TextProcessor.process_line(out)

    def reload(self):
        """
        Reloads all plugins
        """
        self.CommandRegistry.clear_commands()
        self.EventManager.clear_handlers()
        self.plugin_manager.reload_all_manifests()
        self.plugin_manager.reload_all_plugins(self)

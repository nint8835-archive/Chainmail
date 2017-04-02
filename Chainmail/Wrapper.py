import logging
import os
import shlex
import subprocess
import sys
import threading

import jigsaw

from .Events import ServerStartedEvent, Events, ServerStoppedEvent
from .EventManager import EventManager
from .PlayerManager import PlayerManager
from .Plugin import ChainmailPlugin
from .TextProcessor import TextProcessor


class Wrapper(threading.Thread):

    def __init__(self, jar="minecraft_server.jar", max_ram="2G", min_ram="256M", log_level=logging.INFO):
        super().__init__()
        logging.basicConfig(format="{%(asctime)s} (%(name)s) [%(levelname)s]: %(message)s",
                            datefmt="%x, %X",
                            level=log_level)
        self._logger = logging.getLogger("Chainmail")

        self.TextProcessor = TextProcessor(self)
        self.EventManager = EventManager()
        self.PlayerManager = PlayerManager()

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

        self.plugin_manager = jigsaw.PluginLoader(
            (os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, "plugins")),),
            log_level,
            ChainmailPlugin
        )

        self._server_process = None  # type: subprocess.Popen
        self.wrapper_running = False
        self.version = "UNKNOWN"

        self._logger.debug("Wrapper initialized.")

    def start_server(self):
        self._logger.info("Starting server...")
        self._server_process = subprocess.Popen(self._command,
                                                stdout=subprocess.PIPE,
                                                stdin=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
        self.EventManager.dispatch_event(Events.SERVER_STARTED, ServerStartedEvent())
        self._logger.info("Server started.")

    def run(self):
        self.wrapper_running = True

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

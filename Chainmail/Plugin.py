import logging
from jigsaw import JigsawPlugin

from . import Wrapper


class ChainmailPlugin(JigsawPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        """
        Initializes a new plugin
        :param manifest: The plugin manifest
        :param wrapper: The wrapper that loaded this plugin
        """
        super().__init__(manifest)
        self.wrapper = wrapper
        self._logger = None

    @property
    def logger(self) -> logging.Logger:
        """
        Gets the logger belonging to this plugin
        :return: The logger
        """
        if self._logger is None:
            self._logger = logging.getLogger(self.manifest.get("name"))
        return self._logger

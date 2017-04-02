import logging
from jigsaw import JigsawPlugin

from . import Wrapper


class ChainmailPlugin(JigsawPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest)
        self.wrapper = wrapper
        self._logger = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = logging.getLogger(self.manifest.get("name"))
        return self._logger

import logging
from typing import Optional

import requests
from jigsaw import JigsawPlugin

from .Util import get_item_from_list
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
        self.enabled = False
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

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    @property
    def new_version_available(self) -> Optional[bool]:
        """
        Checks the remote manifest to see if a new version is available
        :return: Whether or not there is a new version available
        """
        if self.manifest.get("remote_manifest", "") == "":
            return
        self.logger.info("Checking for update...")
        try:
            manifest = requests.get(self.manifest.get("remote_manifest", "")).json()
            version_remote = manifest["version"].split(".")
            version_local = self.manifest["version"].split(".")
            for i in range(len(version_local)):
                if int(version_local[i]) < int(get_item_from_list(version_remote, i, "0")):
                    self.logger.info(f"An update is available. Current version is v{self.manifest['version']}, updated version is v{manifest['version']}.")
                    return True
            self.logger.info("No update required.")
            return False
        except requests.HTTPError:
            self.logger.warning("Failed to check for update.")

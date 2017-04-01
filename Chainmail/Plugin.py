from jigsaw import JigsawPlugin

from . import Wrapper


class ChainmailPlugin(JigsawPlugin):
    def __init__(self, manifest: dict, wrapper: "Wrapper.Wrapper") -> None:
        super().__init__(manifest)
        self.wrapper = wrapper

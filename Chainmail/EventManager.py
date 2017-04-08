import threading

import logging

from .Events import Events, Event


class EventManager(object):

    def __init__(self):

        self._handlers = []
        self._logger = logging.getLogger("EventManager")

    def register_handler(self, event_type: Events, handler: classmethod):
        self._handlers.append({
            "type": event_type,
            "handler": handler
        })

    def dispatch_event(self, event_type: Events, args: Event):
        self._logger.debug(f"Event thrown: {event_type.name}")
        for handler in self._handlers:
            if handler["type"] == event_type:
                threading.Thread(target=handler["handler"], args=(args,)).start()

    def clear_handlers(self):
        self._handlers = []

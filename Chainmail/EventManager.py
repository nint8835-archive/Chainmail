import threading

from .Events import Events, Event


class EventManager(object):

    def __init__(self):

        self._handlers = []

    def register_handler(self, event_type: Events, handler: classmethod):
        self._handlers.append({
            "type": event_type,
            "handler": handler
        })

    def throw_event(self, event_type: Events, args: Event):
        for handler in self._handlers:
            if handler["type"] == event_type:
                threading.Thread(target=handler["handler"], args=(args,)).start()

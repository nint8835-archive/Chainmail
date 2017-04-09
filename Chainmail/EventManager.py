import threading

import logging

from .Events import Events, Event


class EventManager(object):

    def __init__(self) -> None:

        """
        Initializes the event manager
        """
        self._handlers = []
        self._logger = logging.getLogger("EventManager")

    def register_handler(self, event_type: Events, handler: classmethod) -> None:
        """
        Registers a new event handler
        :param event_type: The type of event this handler should handle
        :param handler: The handler
        """
        self._handlers.append({
            "type": event_type,
            "handler": handler
        })

    def dispatch_event(self, event_type: Events, args: Event) -> None:
        """
        Dispatches an event to all registered event handlers of matching type
        :param event_type: The type of event
        :param args: The event args
        """
        self._logger.debug(f"Event thrown: {event_type.name}")
        for handler in self._handlers:
            if handler["type"] == event_type:
                threading.Thread(target=handler["handler"], args=(args,)).start()

    def clear_handlers(self) -> None:
        """
        Clears the event handler list
        """
        self._handlers = []

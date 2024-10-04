from typing import Any, Callable

from Messaging.Events import Event


class Broker:
    __subscribers: dict[type[Event], list[Callable[[Event], Any]]] = {}

    @classmethod
    def subscribe(cls, event: type[Event], function: Callable[[Event], Any]):
        if event not in cls.__subscribers:
            cls.__subscribers[event] = []
        cls.__subscribers[event].append(function)

    @classmethod
    def notify(cls, event: Event):
        for evt in type(event).mro():
            if evt in cls.__subscribers and issubclass(evt, Event):
                for subscriber in cls.__subscribers[evt]:
                    subscriber(event)

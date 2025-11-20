from typing import Callable

from util.event_type_enum import EventEnum


class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: EventEnum):
        def decorator(func: Callable):
            subscriptions = getattr(func, "_subscriptions", [])

            if not subscriptions:
                setattr(func, "_subscriptions", subscriptions)

            subscriptions.append(event_type)
            return func

        return decorator

    def register(self, instance):
        for attr_name in dir(instance):
            attr: Callable = getattr(instance, attr_name)

            subscriptions = getattr(attr, "_subscriptions", [])
            for event_type in subscriptions:
                self._subscribers.setdefault(event_type, []).append(attr)

    def publish(self, event_type: EventEnum, *args, **kwargs):
        for subscriber in self._subscribers.get(event_type, []):
            subscriber(*args, **kwargs)

from typing import List, Type
from .events import BaseTelemetryEvent
from .sinks import BaseSink

class EventBus:
    """
    Routes typed telemetry events from Collectors to registered Sinks.
    """
    def __init__(self):
        self.routes: dict[Type[BaseTelemetryEvent], List[BaseSink]] = {}

    def subscribe(self, event_type: Type[BaseTelemetryEvent], sink: BaseSink) -> None:
        """
        Subscribes a specific sink to an event type.
        """
        if event_type not in self.routes:
            self.routes[event_type] = []
        self.routes[event_type].append(sink)

    async def publish(self, event: BaseTelemetryEvent) -> None:
        """
        Publishes an event to all subscribed sinks asynchronously.
        """
        event_type = type(event)
        if event_type in self.routes:
            for sink in self.routes[event_type]:
                await sink.push(event)

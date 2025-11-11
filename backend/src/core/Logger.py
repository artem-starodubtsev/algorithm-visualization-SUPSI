from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    step: int
    type: dict


class Logger:
    def __init__(self):
        self._current_step: int = 0
        self._events: list[Event] = []

    def log(self, action: dict):
        self._current_step += 1
        self._events.append(
            Event(self._current_step, action)
        )

    def export(self):
        return [
            {
                'step': event.step,
                'action': event.type
            } for event in self._events
        ]

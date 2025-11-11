from dataclasses import dataclass
from enum import Enum
from typing import Any


## TODO add Actions class
class Operation(Enum):
    ASSIGN = 1
    COMPARE = 2
    HIGHLIGHT = 3

@dataclass
class Event:
    step: int
    type: str
    description: Any


class Logger:
    def __init__(self):
        self._current_step: int = 0
        self._events: list[Event] = []

    def log(self, kind, **data):
        self._current_step += 1
        self._events.append(

        )

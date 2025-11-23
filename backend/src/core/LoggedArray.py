from .Logger import Logger
from .LoggedStructureInterface import LoggedStructureInterface
from .ElementRef import ElementRef


class LoggedArray[T](LoggedStructureInterface[T]):
    def __init__(self, name: str, logger: Logger, capacity: int | None = None, data: list[T] | None = None) -> None:
        self._name: str = name
        if data is None:
            if capacity is None:
                raise TypeError('capacity cannot be None')
            self._capacity: int = capacity
            self._data: list[T] = [None] * capacity
        else:
            self._data = data[:]
            self._capacity = len(data)

        self._logger: Logger = logger
        self._logger.register_structure(self.to_dict())

    def name(self) -> str:
        return self._name

    def to_dict(self) -> dict:
        return {
            'name': self._name,
            'type': 'Array',
            'capacity': self._capacity
        }

    def get_value(self, idx: ElementRef | int) -> T:
        idx = ElementRef.unwrap(idx)
        return self._data[idx]

    def set_value(self, idx: ElementRef | int, value: T) -> None:
        idx = ElementRef.unwrap(idx)
        self._data[idx] = value

    def __str__(self):
        return str(self._data)

    def __len__(self) -> int:
        return self._capacity

    def __getitem__(self, idx: ElementRef | int) -> ElementRef[T]:
        idx = ElementRef.unwrap(idx)
        return ElementRef(self, idx, self._logger)

    def __setitem__(self, idx: ElementRef | int, value: ElementRef[T] | T) -> None:
        idx = ElementRef.unwrap(idx)
        v = ElementRef.unwrap(value)
        self._logger.log(
            {
                'type': 'write',
                'el': self[idx].to_dict(),
                'val': v
            }
        )
        self._data[idx] = v

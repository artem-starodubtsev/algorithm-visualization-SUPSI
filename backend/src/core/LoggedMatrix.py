from .Logger import Logger
from .LoggedStructureInterface import LoggedStructureInterface
from .ElementRef import ElementRef
from copy import deepcopy

class LoggedMatrix[T](LoggedStructureInterface[T]):
    def __init__(self, name: str, logger: Logger, shape: tuple[int, int] | None = None, data: list[list[T]] | None = None) -> None:
        self._name: str = name
        if data is None:
            if shape is None:
                raise TypeError('shape cannot be None')
            self._shape: tuple[int, int] = shape
            self._data: list[list[T]] = [[None] * self._shape[1] for _ in range(self._shape[0])]
        else:
            self._data = deepcopy(data)
            self._shape: tuple[int, int] = (len(self._data), len(self._data[0]))

        self._logger: Logger = logger
        self._logger.register_structure(self.to_dict())

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape

    def name(self) -> str:
        return self._name

    def to_dict(self) -> dict:
        return {
            'name': self._name,
            'type': 'Matrix',
            'rows': self._shape[0],
            'cols': self._shape[1],
            'data': deepcopy(self._data)
        }

    def get_value(self, idx: tuple) -> T:
        y = ElementRef.unwrap(idx[0])
        x = ElementRef.unwrap(idx[1])
        return self._data[y][x]

    def set_value(self, idx: tuple, value: T) -> None:
        y = ElementRef.unwrap(idx[0])
        x = ElementRef.unwrap(idx[1])
        self._data[y][x] = value

    def __str__(self):
        return str(self._data)

    def __len__(self) -> int:
        return self._shape[0]

    def __getitem__(self, idx: tuple) -> ElementRef[T]:
        y = ElementRef.unwrap(idx[0])
        x = ElementRef.unwrap(idx[1])
        return ElementRef(self, (y, x), self._logger)

    def __setitem__(self, idx: tuple, value: ElementRef[T] | T) -> None:
        y = ElementRef.unwrap(idx[0])
        x = ElementRef.unwrap(idx[1])
        v = ElementRef.unwrap(value)
        self._logger.log(
            {
                'type': 'write',
                'el': self[idx].to_dict(),
                'val': v
            }
        )
        self._data[y][x] = v

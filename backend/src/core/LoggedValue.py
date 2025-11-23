from .Logger import Logger
from .LoggedArray import LoggedArray
from .ElementRef import ElementRef


class LoggedValue[T](LoggedArray[T]):
    def __init__(self, name: str, logger: Logger, value: T | None = None) -> None:
        super().__init__(name, logger, 1)
        if value is not None:
            self._data[0] = value

    def name(self) -> str:
        return self._name

    def to_dict(self) -> dict:
        return {
            'name': self._name,
            'type': 'Value'
        }

    def get_value(self, idx: ElementRef | int) -> T:
        idx = ElementRef.unwrap(idx)
        if idx != 0:
            raise IndexError()
        return self._data[0]

    def set_value(self, idx: ElementRef | int, value: T) -> None:
        idx = ElementRef.unwrap(idx)
        if idx != 0:
            raise IndexError()
        self._data[idx] = value

    def __getitem__(self, idx: ElementRef | int) -> ElementRef[T]:
        idx = ElementRef.unwrap(idx)
        if idx != 0:
            raise IndexError()
        return ElementRef(self, 0, self._logger)

    def __setitem__(self, idx: ElementRef | int, value: ElementRef[T] | T) -> None:
        idx = ElementRef.unwrap(idx)
        if idx != 0:
            raise IndexError()
        v = ElementRef.unwrap(value)
        self._logger.log(
            {
                'type': 'write',
                'el': self[idx].to_dict(),
                'val': v
            }
        )
        self._data[idx] = v




from core.Logger import Logger
from LoggedArray import LoggedArray
from ElementRef import ElementRef

class LoggedValue[T](LoggedArray[T]):
    def __init__(self, name: str, logger: Logger, value: T | None = None) -> None:
        super().__init__(name, logger, 1)
        if value:
            self._data[0] = value

    def to_dict(self) -> dict:
        return {
            'name': self._name,
            'type': 'Value'
        }

    def get_value(self, idx: int) -> T:
        if idx != 0:
            raise IndexError()
        return self._data[0]

    def set_value(self, idx: int, value: T) -> None:
        if idx != 0:
            raise IndexError()
        self._data[idx] = value

    def __getitem__(self, idx: int) -> ElementRef[T]:
        if idx != 0:
            raise IndexError()
        return ElementRef(self, 0, self._logger)

    def __setitem__(self, idx: int, value: ElementRef[T] | T) -> None:
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

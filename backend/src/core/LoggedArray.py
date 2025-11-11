from Logger import Logger

## TODO add comparator
class ElementRef[T]:
    def __init__(self, array_ref: 'LoggedArray[T]', idx: int, logger: Logger) -> None:
        self._ref: 'LoggedArray[T]' = array_ref
        self._idx: int = idx
        self._logger: Logger = logger

    @property
    def value(self) -> T:
        return self._ref.get_value(self._idx)




class LoggedArray[T]:
    def __init__(self, name: str, capacity: int, logger: Logger):
        self._name: str = name
        self._capacity: int = capacity
        self._data: list[T] = [0 for _ in range(capacity)]
        self._logger: Logger = logger

    def get_value(self, idx: int) -> T:
        return self._data[idx]

    def __getitem__(self, idx):
        return ElementRef(self, idx, self._logger)

    def __setitem__(self, idx: int, value: T | ElementRef[T]):
        if isinstance(value, ElementRef):
            v = value.value
        else:
            v = value

        self._logger.log()


        self._data[idx] = v
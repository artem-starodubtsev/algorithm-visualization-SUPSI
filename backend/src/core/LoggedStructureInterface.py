from abc import ABC, abstractmethod

class LoggedStructureInterface[T](ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_value(self, idx: int) -> T:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, idx: int, value: T) -> None:
        raise NotImplementedError
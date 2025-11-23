from abc import ABC, abstractmethod


class AlgorithmInterface[TInstance, TSolution](ABC):

    @abstractmethod
    def input_scheme(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def solve(self, instance: TInstance) -> TSolution:
        raise NotImplementedError

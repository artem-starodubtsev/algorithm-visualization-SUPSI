from abc import ABC, abstractmethod


class AlgorithmInterface[TInstance, TSolution](ABC):
    @abstractmethod
    def solve(self, instance: TInstance) -> TSolution:
        raise NotImplementedError

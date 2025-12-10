from core.AlgorithmInterface import AlgorithmInterface
from pydantic import BaseModel, field_validator, model_validator
from core.LoggedArray import LoggedArray
from core.LoggedMatrix import LoggedMatrix
from core.LoggedValue import LoggedValue
from core.Logger import Logger


class IndependentSetInstance(BaseModel):
    graph: list[list[bool]]
    independent_set: list[int]

    @field_validator('graph')
    @classmethod
    def validate_graph(cls, graph: list[list[bool]]):
        n = len(graph)

        for i in range(n):
            if len(graph[i]) != n:
                raise ValueError('Graph must have rows the same length as cols')

        for i in range(n):
            if not graph[i][i]:
                raise ValueError('Graph must have True diagonal (edge to itself)')

        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] != graph[j][i]:
                    raise ValueError('Graph must be not directional')

        return graph

    @model_validator(mode='after')
    def validate_set(self):
        independent_set = set(self.independent_set)

        if len(independent_set) != len(self.independent_set):
            raise ValueError('Independent set has duplicates')

        for i in self.independent_set:
            if not 0 <= i < len(self.graph):
                raise ValueError('Node index out of range')

        return self


class IndependentSetSolution(BaseModel):
    answer: bool
    logs: dict


class IndependentSetAlgorithm(AlgorithmInterface[IndependentSetInstance, IndependentSetSolution]):
    def input_scheme(self) -> dict:
        return IndependentSetInstance.model_json_schema()

    def solve(self, instance: IndependentSetInstance) -> IndependentSetSolution:
        logger = Logger()

        matrix = LoggedMatrix[bool]('Graph', logger, data=instance.graph)
        independent_set = LoggedArray[int]('Independent Set', logger, data=instance.independent_set)

        answer = LoggedValue[bool]('Verdict', logger, True)

        n = len(independent_set)

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[independent_set[i], independent_set[j]] == True:
                    answer[0] = False
                    break
            else:
                continue
            break

        return IndependentSetSolution(logs=logger.export(), answer=answer[0].value)

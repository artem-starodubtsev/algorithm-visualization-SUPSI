from core.AlgorithmInterface import AlgorithmInterface
from pydantic import BaseModel, field_validator, model_validator, conlist
from core.LoggedArray import LoggedArray
from core.LoggedMatrix import LoggedMatrix
from core.LoggedValue import LoggedValue
from core.Logger import Logger

Pair = conlist(int, min_length=2, max_length=2)


class BipartiteMatchingInstance(BaseModel):
    graph: list[list[bool]]
    matching: list[Pair]

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
    def validate_matching(self):
        for i, j in self.matching:
            if not 0 <= i < len(self.graph) or not 0 <= j < len(self.graph):
                raise ValueError('Node index out of range')

        return self


class BipartiteMatchingSolution(BaseModel):
    answer: bool
    logs: dict


class BipartiteMatchingAlgorithm(AlgorithmInterface[BipartiteMatchingInstance, BipartiteMatchingSolution]):
    def input_scheme(self) -> dict:
        return BipartiteMatchingInstance.model_json_schema()

    def solve(self, instance: BipartiteMatchingInstance) -> BipartiteMatchingSolution:
        logger = Logger()

        matrix = LoggedMatrix[bool]('Graph', logger, data=instance.graph)
        matching = LoggedMatrix[int]('Matching', logger, data=instance.matching)

        answer = LoggedValue[bool]('Verdict', logger, True)

        n = len(matching)

        for i in range(n):
            if matrix[matching[i, 0], matching[i, 1]] == False:
                answer[0] = False
                break

        if answer[0].value:
            for i in range(n):
                for j in range(i+1, n):
                    if matching[i, 0] == matching[j, 0] or matching[i, 1] == matching[j, 1]:
                        answer[0] = False
                        break
                else:
                    continue
                break


        return BipartiteMatchingSolution(logs=logger.export(), answer=answer[0].value)

from pprint import pprint

from core.AlgorithmInterface import AlgorithmInterface
from pydantic import BaseModel, field_validator, model_validator, conlist
from core.LoggedArray import LoggedArray
from core.LoggedMatrix import LoggedMatrix
from core.LoggedValue import LoggedValue
from core.Logger import Logger


class BinarySearchInstance(BaseModel):
    sorted_array: list[int]
    value: int

    @field_validator('sorted_array')
    @classmethod
    def validate_array(cls, sorted_array: list[int]):
        n = len(sorted_array)

        for i in range(n - 1):
            if sorted_array[i] > sorted_array[i + 1]:
                raise ValueError('Array must be sorted (ASC)')

        return sorted_array


class BinarySearchSolution(BaseModel):
    answer: bool
    logs: dict


class BinarySearchAlgorithm(AlgorithmInterface[BinarySearchInstance, BinarySearchSolution]):
    def input_scheme(self) -> dict:
        return BinarySearchInstance.model_json_schema()

    def solve(self, instance: BinarySearchInstance) -> BinarySearchSolution:
        logger = Logger()

        array = LoggedArray[int]('Array', logger, data=instance.sorted_array)
        value = LoggedValue[int]('Value', logger, value=instance.value)

        l = LoggedValue[int]('Left pointer', logger, value=0)
        r = LoggedValue[int]('Right pointer', logger, value=len(instance.sorted_array) - 1)
        m = LoggedValue[int]('Middle pointer', logger)

        answer = LoggedValue[bool]('Verdict', logger, False)

        while l != r:
            m[0] = (l + r) // 2
            if array[m[0]] == value:
                answer[0] = True
                break
            elif array[m[0]] > value:
                r[0] = m[0]
            else:
                l[0] = m + 1

        return BinarySearchSolution(logs=logger.export(), answer=answer[0].value)

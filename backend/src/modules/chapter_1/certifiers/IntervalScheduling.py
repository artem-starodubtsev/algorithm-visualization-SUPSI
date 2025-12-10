from core.AlgorithmInterface import AlgorithmInterface
from pydantic import BaseModel, field_validator, model_validator, conlist
from core.LoggedArray import LoggedArray
from core.LoggedMatrix import LoggedMatrix
from core.LoggedValue import LoggedValue
from core.Logger import Logger

Interval = conlist(int, min_length=2, max_length=2)


class IntervalSchedulingInstance(BaseModel):
    intervals: list[Interval]
    intervals_set: list[int]

    @field_validator('intervals')
    @classmethod
    def validate_intervals(cls, intervals: list[Interval]):
        for s, e in intervals:
            if s > e:
                raise ValueError("Each interval must satisfy start <= end")

        e_prev = intervals[0][1]
        for _, e in intervals[1:]:
            if e_prev > e:
                raise ValueError("Plese sort intervals by end")
            e_prev = e

        return intervals

    @model_validator(mode='after')
    def validate_intervals_set(self):
        intervals_set = set(self.intervals_set)

        if len(intervals_set) != len(self.intervals_set):
            raise ValueError('Interval duplicate')

        for i in self.intervals_set:
            if not 0 <= i < len(self.intervals):
                raise ValueError('Interval index out of range')

        return self


class IntervalSchedulingSolution(BaseModel):
    answer: bool
    logs: dict


class IntervalSchedulingAlgorithm(AlgorithmInterface[IntervalSchedulingInstance, IntervalSchedulingSolution]):
    def input_scheme(self) -> dict:
        return IntervalSchedulingInstance.model_json_schema()

    def solve(self, instance: IntervalSchedulingInstance) -> IntervalSchedulingSolution:
        logger = Logger()

        matrix = LoggedMatrix[int]('Intervals', logger, data=instance.intervals)
        intervals_set = LoggedArray[int]('Interval Set', logger, data=instance.intervals_set)

        answer = LoggedValue[bool]('Verdict', logger, True)

        n = len(intervals_set)

        for i in range(n):
            for j in range(i + 1, n):
                if matrix[intervals_set[i], 0] < matrix[intervals_set[j], 1] and matrix[intervals_set[j], 0] < matrix[
                    intervals_set[i], 1]:
                    answer[0] = False
                    break
            else:
                continue
            break

        return IntervalSchedulingSolution(logs=logger.export(), answer=answer[0].value)

from core.AlgorithmInterface import AlgorithmInterface
from pydantic import BaseModel, field_validator, model_validator
from pprint import pprint


class GaleShapleyInstance(BaseModel):
    male_profile: list[list[int]]
    female_profile: list[list[int]]

    @field_validator('male_profile', 'female_profile')
    @classmethod
    def validate_profile(cls, profile: list[list[int]]):
        l = len(profile[0])
        ids = frozenset(range(l))
        for row in profile:
            if len(row) != l:
                raise ValueError(f"Row should have equal width {l}.")
            if frozenset(row) != ids:
                raise ValueError(f"Row should have {l} different ids.")
        return profile

    @model_validator(mode='after')
    def check_sizes(self):
        if len(self.male_profile) != len(self.female_profile[0]) or len(self.female_profile) != len(
                self.male_profile[0]):
            raise ValueError(f"Male and female profiles doesn't match.")
        return self


class GaleShapleySolution(BaseModel):
    answer: list[tuple[int, int]]
    log: list[dict]


class GaleShapleyAlgorithm(AlgorithmInterface[GaleShapleyInstance, GaleShapleySolution]):

    def solve(self, instance: GaleShapleyInstance) -> GaleShapleySolution:
        answer = [(-1, -1) for _ in range(min(len(instance.male_profile), len(instance.female_profile)))]

        return GaleShapleySolution(answer=answer, log=[])


if __name__ == '__main__':
    print('!')

from core.AlgorithmInterface import AlgorithmInterface
from pydantic import BaseModel, field_validator, model_validator
from pprint import pprint

from core.LoggedArray import LoggedArray
from core.LoggedMatrix import LoggedMatrix
from core.LoggedValue import LoggedValue
from core.Logger import Logger


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
    logs: dict


class GaleShapleyAlgorithm(AlgorithmInterface[GaleShapleyInstance, GaleShapleySolution]):

    def solve(self, instance: GaleShapleyInstance) -> GaleShapleySolution:
        logger = Logger()

        men_prefs = LoggedMatrix[int](name="MEN PREFERENCES", logger=logger, data=instance.male_profile)
        women_prefs = LoggedMatrix[int](name="WOMEN PREFERENCES", logger=logger, data=instance.female_profile)

        n = len(men_prefs)

        next_choice = LoggedArray[int](name="MEN NEXT PROPOSE", logger=logger, data=[0] * n)
        women_match = LoggedArray[int](name="WOMAN MATCH", logger=logger, data=[-1] * n)
        free_men = LoggedArray[bool](name="IS MAN FREE?", logger=logger, data=[True] * n)

        m = LoggedValue[int](name="men iterator", logger=logger, value=0)

        target_m = LoggedValue[int](name="TARGET MAN", logger=logger)
        target_w = LoggedValue[int](name="TARGET WOMAN", logger=logger)

        def better_man(w_id, m_new_id) -> bool:
            for i in range(n):
                if women_prefs[w_id, i] == m_new_id:
                    return True
                if women_prefs[w_id, i] == women_match[w_id]:
                    break
            return False

        while True:
            for i in range(m[0].value, m[0].value + n):
                if free_men[i % n] == True:
                    target_m[0] = i % n
                    m[0] = (m[0] + 1) % n
                    break
            else:
                break

            target_w[0] = men_prefs[target_m[0], next_choice[target_m[0]]]
            next_choice[target_m[0]] = next_choice[target_m[0]] + 1

            if women_match[target_w[0]] == -1:
                women_match[target_w[0]] = target_m[0]
                free_men[target_m[0]] = False
            elif better_man(target_w[0], target_m[0]):
                free_men[women_match[target_w[0]]] = True
                women_match[target_w[0]] = target_m[0]
                free_men[target_m[0]] = False

        return GaleShapleySolution(logs=logger.export(), answer=[(w, women_match[w].value) for w in range(n)])


if __name__ == '__main__':
    ins = GaleShapleyInstance(
        male_profile=[
            [1, 0, 3, 4, 2],  # Victor:  Bertha, Amy,   Diane, Erika, Clare
            [3, 1, 0, 2, 4],  # Wyatt:   Diane,  Bertha, Amy,   Clare, Erika
            [1, 4, 2, 3, 0],  # Xavier:  Bertha, Erika, Clare, Diane, Amy
            [0, 3, 2, 1, 4],  # Yancey:  Amy,   Diane,  Clare, Bertha,Erika
            [1, 3, 0, 4, 2],  # Zeus:    Bertha, Diane, Amy,   Erika, Clare
        ],
        female_profile=[
            [4, 0, 1, 3, 2],  # Amy:   Zeus,  Victor, Wyatt,  Yancey, Xavier
            [2, 1, 3, 0, 4],  # Bertha:Xavier,Wyatt,  Yancey, Victor, Zeus
            [1, 2, 3, 4, 0],  # Clare: Wyatt, Xavier, Yancey, Zeus,   Victor
            [0, 4, 3, 2, 1],  # Diane: Victor,Zeus,   Yancey, Xavier, Wyatt
            [3, 1, 4, 2, 0],  # Erika: Yancey,Wyatt,  Zeus,   Xavier, Victor
        ]
    )
    pprint(GaleShapleyAlgorithm().solve(ins))

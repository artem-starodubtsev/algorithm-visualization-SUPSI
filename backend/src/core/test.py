from Logger import Logger
from LoggedArray import LoggedArray
from LoggedValue import LoggedValue
from pprint import pprint


def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j].swap(a[j + 1])


def gale_shapley(men_prefs: list[list[int]], women_prefs: list[list[int]], logger: Logger):
    n = len(men_prefs)

    next_choice = LoggedArray[int](name="MEN NEXT PROPOSE", logger=logger, data=[0] * n)
    women_match = LoggedArray[int](name="WOMAN MATCH", logger=logger, data=[-1] * n)
    free_men = LoggedArray[bool](name="IS MAN FREE?", logger=logger, data=[True] * n)

    m = LoggedValue[int](name="men iterator", logger=logger, value=0)

    target_m = LoggedValue[int](name="TARGET MAN", logger=logger)
    target_w = LoggedValue[int](name="TARGET WOMAN", logger=logger)

    def better_man(w_id, m_new_id) -> bool:
        for i in range(n):
            if women_prefs[w_id][i] == m_new_id:
                return True
            if women_prefs[w_id][i] == women_match[w_id].value:
                break
        return False

    while True:
        for i in range(m[0].value, m[0].value + n):
            if free_men[i % n] == True:
                target_m[0] = i % n
                m[0] = (m[0].value + 1) % n
                break
        else:
            break

        target_w[0] = men_prefs[target_m[0].value][next_choice[target_m[0].value].value]
        next_choice[target_m[0].value] = next_choice[target_m[0].value].value + 1

        if women_match[target_w[0].value] == -1:
            women_match[target_w[0].value] = target_m[0].value
            free_men[target_m[0].value] = False
        elif better_man(target_w[0].value, target_m[0].value):
            free_men[women_match[target_w[0].value].value] = True
            women_match[target_w[0].value] = target_m[0].value
            free_men[target_m[0].value] = False

    return [(w, women_match[w].value) for w in range(n)]


if __name__ == '__main__':
    logger = Logger()
    # data = [4, -1, 2, 9, 3, 1]
    # array = LoggedArray[int](name='A1', logger=logger, data=data)
    #
    # bubble_sort(array)
    #
    # pprint(logger.export())
    # print(array)

    # 0..4: men = [Victor, Wyatt, Xavier, Yancey, Zeus]
    # 0..4: women = [Amy, Bertha, Clare, Diane, Erika]

    men_prefs = [
        [1, 0, 3, 4, 2],  # Victor:  Bertha, Amy,   Diane, Erika, Clare
        [3, 1, 0, 2, 4],  # Wyatt:   Diane,  Bertha, Amy,   Clare, Erika
        [1, 4, 2, 3, 0],  # Xavier:  Bertha, Erika, Clare, Diane, Amy
        [0, 3, 2, 1, 4],  # Yancey:  Amy,   Diane,  Clare, Bertha,Erika
        [1, 3, 0, 4, 2],  # Zeus:    Bertha, Diane, Amy,   Erika, Clare
    ]

    women_prefs = [
        [4, 0, 1, 3, 2],  # Amy:   Zeus,  Victor, Wyatt,  Yancey, Xavier
        [2, 1, 3, 0, 4],  # Bertha:Xavier,Wyatt,  Yancey, Victor, Zeus
        [1, 2, 3, 4, 0],  # Clare: Wyatt, Xavier, Yancey, Zeus,   Victor
        [0, 4, 3, 2, 1],  # Diane: Victor,Zeus,   Yancey, Xavier, Wyatt
        [3, 1, 4, 2, 0],  # Erika: Yancey,Wyatt,  Zeus,   Xavier, Victor
    ]

    matches = gale_shapley(men_prefs, women_prefs, logger)
    # matches[w] = man matched to woman w

    men = ['Victor', 'Wyatt', 'Xavier', 'Yancey', 'Zeus']
    women = ['Amy', 'Bertha', 'Clare', 'Diane', 'Erika']

    pprint(logger.export())

    for m, w in matches:
        print(f'pair:\t{men[m]} - {women[w]}')

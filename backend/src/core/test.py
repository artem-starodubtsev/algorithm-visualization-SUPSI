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


if __name__ == '__main__':
    logger = Logger()
    data = [4, -1, 2, 9, 3, 1]
    array = LoggedArray[int](name='A1', logger=logger, data=data)

    bubble_sort(array)

    pprint(logger.export())
    print(array)


from textdata.util import partition


def test_partition():

    def odd(x):
        return x % 2

    evens, odds = partition(odd, range(10))
    assert evens == [0, 2, 4, 6, 8]
    assert odds == [1, 3, 5, 7, 9]

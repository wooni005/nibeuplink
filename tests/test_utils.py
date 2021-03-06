from nibeuplink.utils import cyclic_tuple
import pytest

def test_cyclic_filled():
    data = [
        (1, 'a'),
        (1, 'b'),
        (1, 'c'),
        (1, 'd'),
    ]

    cyclic = cyclic_tuple(data, 3)
    next(cyclic)
    assert next(cyclic) == (1, {'a', 'b', 'c'})
    assert next(cyclic) == (1, {'d', 'a', 'b'})
    assert next(cyclic) == (1, {'c', 'd', 'a'})
    assert next(cyclic) == (1, {'b', 'c', 'd'})
    assert next(cyclic) == (1, {'a', 'b', 'c'})

def test_cyclic_tuple():
    data = [
        (1, 'a'),
        (1, 'b'),
        (2, 'a'),
        (1, 'c'),
        (2, 'b'),
        (1, 'd'),
    ]

    cyclic = cyclic_tuple(data, 3)
    next(cyclic)
    assert next(cyclic) == (1, {'a', 'b', 'c'})
    assert next(cyclic) == (2, {'a', 'b'})
    assert next(cyclic) == (1, {'d', 'a', 'b'})
    assert next(cyclic) == (2, {'a', 'b'})


def test_cyclic_all_aligned():
    data = [
        (1, 'a'),
        (1, 'b'),
        (1, 'c'),
    ]

    cyclic = cyclic_tuple(data, 3)
    next(cyclic)
    assert next(cyclic) == (1, {'a', 'b', 'c'})
    assert next(cyclic) == (1, {'a', 'b', 'c'})

def test_cyclic_empty():
    data = []
    cyclic = cyclic_tuple(data, 3)
    next(cyclic)
    assert next(cyclic) == (None, {None})
    assert next(cyclic) == (None, {None})


def test_cyclic_postponed():
    data = [
        (1, 'a'),
        (1, 'b'),
        (1, 'c'),
        (1, 'd'),
    ]

    cyclic = cyclic_tuple(data, 2)
    next(cyclic)
    cyclic.send((1, 'a'))
    assert next(cyclic) == (1, {'b', 'c'})
    assert next(cyclic) == (1, {'d', 'a'})

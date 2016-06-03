"""
Additional dict functions.

This module contains functions, witch operate on dict or create new one
but do not modify already existed values.
"""

import functools
import collections
import operator

__author__ = 'Leszek Trzemecki'


def two_way(dictionary):
    """
    Create new dict contains two way associated (values to keys and keys to values)
    items from given dict, for example:
    >>> two_way({'A': 1, 'B': 2})
    {'A': 1, 1: 'A', 2: 'B', 'B': 2}

    :param dict dictionary: one way association dict
    :return: two way association dict
    """

    return merge(swap(dictionary), dictionary)


def swap(dictionary):
    """
    Create new dict with given dictionary keys as values and values as keys.

    :param dict dictionary: dict to swap
    :return: new swapped dict
    """

    return {value: key for key, value in dictionary.items()}


def by(key, elements):
    """
    Create dict contained elements, which could be accessed by
    extracted key, as given as parameter.

    :param elements: list or tuple of elements
    :param key: attribute, by which element could be accessed or lambda function
    :return: dict with elements, assigned to extracted key
    """
    if not callable(key):
        key = operator.attrgetter(key)

    return {key(element): element for element in elements}


def group_by(key, elements):
    """
    Create dict contained elements, grouped by given key.
    Return dict of list of values, with the same extracted key assigned to this key.

    :param elements: list or tuple of elements
    :param key: attribute, by which element could be accessed or lambda function
    :return: dict with list of elements, assigned to extracted key
    """

    if not callable(key):
        key = operator.attrgetter(key)

    result = collections.defaultdict(list)

    for each in elements:
        result[key(each)].append(each)

    return dict(result)


def extract(source, *values):
    """
    Create dict with attributes name and associated value extracted from object,
    by keys given as parameter.

    :param source: object to extract
    :param values: values which should be extracted
    :return: dict with extracted values
    """

    return {value: getattr(source, value) for value in values}


def merge(*dicts):
    """
    Merge dicts into single dict. If keys are duplicated, value is taken from last dict,
    which contains this key.

    :param dicts: dicts to merge
    :return: dict contained all element from given dicts
    """

    def update(result, item):
        result.update(item)
        return result

    return functools.reduce(update, dicts, dict())


def split(elements, *conditions, **kwargs):
    """
    Split elements to other sets of elements according to given conditions, for example:
    >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%2 == 0))
    [{0: 'A', 2: 'C', 4: 'E'}, {1: 'B', 3: 'D'}]

    When the elements which are not follow any given condition should be omitted set rest attribute to False:
    >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%2 == 0), rest=False)
    [{0: 'A', 2: 'C', 4: 'E'}]

    When more than one condition is given element was included in first dictionary, which for condition
    was fulfilled
    >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0, lambda i: i%2 == 0))
    [{0: 'A', 3: 'D'}, {2: 'C', 4: 'E'}, {1: 'B'}]

    :param elements: elements to split into other sets of elements
    :param conditions: lambdas (key -> bool) to decide to include or not element in current result
    :param rest: True if should append at end elements which not fulfilled any condition, False otherwise
    :return: generator for element split according to given condition
    """

    rest = kwargs.get('rest', True)

    for condition in conditions:
        yield sift(elements, condition)
        elements = sift(elements, condition, opposite=True)
    if rest:
        yield elements


def sift(elements, condition, opposite=False):
    """
    Select elements from dictionary, which fulfilled given condition

    :param elements: set of elements for select subset
    :param condition: lambda (key -> bool or key, value -> bool) to select remain elements
    :param opposite: if True replace "condition" by "not condition" (default False)
    :return: subset of elements which fulfilled given condition
    """

    def select(key, value):
        try:
            return bool(opposite) != bool(condition(key, value))  # != <=> xor
        except TypeError:
            return bool(opposite) != bool(condition(key))

    return {key: value for key, value in elements.items() if select(key, value)}


def contains(sub, super):
    """
    Non-recursive.
    Check if sub dict is included in super dict (both keys and values are equal).

    :param dict sub: the dict, which should be included in super dict
    :param dict super: the dict, which should include all elements from sub dict
    :return: true if super contains sub, otherwise false.
    """

    return all(
        key in super and sub[key] == super[key] for key, value in sub.items()
    )

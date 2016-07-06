import collections
import functools
import operator
import inspect


def two_way(dictionary):
    """
    Create new dict contains two way associated (values to keys and keys to values)
    items from given dict, for example::

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


def select(source, *values):
    """
    Select from mapping given values and put into new created dict.

    :param source: mapping, from which values are selected
    :param values: values which should be selected
    :return: dict with selected values
    """
    return extract(source, *values, key=operator.getitem)


def extract(source, *values, **kwargs):
    """
    Create dict with attributes name and associated value extracted from object,
    by keys given as parameter.

    :param source: object to extract
    :param values: values which should be extracted
    :param key: two arguments function, which extract required argument (default getattr)
    :return: dict with extracted values
    """

    extractor = kwargs.get('key', getattr)

    return {value: extractor(source, value) for value in values}


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
    Split elements to other sets of elements according to given conditions, for example::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%2 == 0))
        [{0: 'A', 2: 'C', 4: 'E'}, {1: 'B', 3: 'D'}]

    When the elements which are not follow any given condition should be omitted set rest attribute to False::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%2 == 0), rest=False)
        [{0: 'A', 2: 'C', 4: 'E'}]

    When more than one condition is given element was included in first dictionary, which for condition
    was fulfilled::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0, lambda i: i%2 == 0))
        [{0: 'A', 3: 'D'}, {2: 'C', 4: 'E'}, {1: 'B'}]

    :param elements: elements to split into other sets of elements
    :param conditions: functions (name matters): key -> bool or  value -> bool or key, value -> bool)
        which decide that element in current result should be included or not
    :param rest: True if should append at end elements which not fulfilled any condition, False otherwise
    :return: generator for element split according to given condition
    """

    rest = kwargs.get('rest', True)

    for condition in conditions:
        selected, elements = _split_two(elements, condition)
        yield selected
    if rest:
        yield elements


def _split_two(elements, condition):
    selector = _selector(condition)

    yes, no = {}, {}

    for key, value in elements.items():
        if selector(key, value):
            yes[key] = value
        else:
            no[key] = value

    return yes, no


def sift(elements, condition, opposite=False):
    """
    Select elements from dictionary, which fulfilled given condition

    :param elements: set of elements for select subset
    :param condition: function (name matters): key -> bool or  value -> bool or key, value -> bool)
        selected remain elements
    :param opposite: if True replace "condition" by "not condition" (default False)
    :return: subset of elements which fulfilled given condition
    """

    selector = _selector(condition)

    return {key: value for key, value in elements.items() if bool(opposite) != bool(selector(key, value))}


def _selector(condition):
    spec = inspect.getargspec(condition)
    ismethod = inspect.ismethod(condition)

    if spec.varargs or len(spec.args) - ismethod == 2:
        return lambda key, value: condition(key, value)
    elif spec.args[ismethod] in ['v', 'val', 'value']:
        return lambda key, value: condition(value)
    else:
        return lambda key, value: condition(key)


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


def map_values(function, dictionary):
    """
    Map each value using given function, and return new dict with changed values.

    :param function: keys map function
    :param dictionary: dictionary to mapping
    :return: dict with changed values
    """
    return {key: function(value) for key, value in dictionary.items()}


def map_keys(function, dictionary):
    """
    Map each key using given function, and return new dict with changed keys.

    :param function: values map function
    :param dictionary: dictionary to mapping
    :return: dict with changed (mapped) keys
    """
    return {function(key): value for key, value in dictionary.items()}
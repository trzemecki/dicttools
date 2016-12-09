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
    Create new dict with given dictionary keys as values and values as keys::

        >>> swap({0: 'A', 1: 'B', 2: 'C'})
        {'A': 0, 'C': 2, 'B': 1}

    :param dict dictionary: dict to swap
    :return: new swapped dict
    """

    return {value: key for key, value in dictionary.items()}


def by(key, *elements):
    """
    Create dict contained elements, which could be accessed by
    extracted key, as given as parameter::

        >>> by('real', (1+2j), (2-3j),(-5+0j))
        {1.0: (1+2j), 2.0: (2-3j), -5.0: (-5+0j)}

        >>> by('imag', [(1+2j), (2-3j),(-5+0j)])
        {0.0: (-5+0j), 2.0: (1+2j), -3.0: (2-3j)}


    :param elements: iterable of elements or elements as varargs
    :param key: attribute, by which element could be accessed or lambda function
    :return: dict with elements, assigned to extracted key
    """

    if not callable(key):
        key = operator.attrgetter(key)

    return {key(element): element for element in _iter_all_or_first(elements)}


def group_by(key, *elements):
    """
    Create dict contained elements, grouped by given key.
    Return dict of list of values, with the same extracted key assigned to this key::

        >>> group_by('real', 2j, -3j, (-5+0j), (-3+2j), (-5+15j))
        {0.0: [2j, -3j], -5.0: [(-5+0j), (-5+15j)], -3.0: [(-3+2j)]}

    :param elements: list or tuple of elements
    :param key: attribute, by which element could be accessed or lambda function
    :return: dict with list of elements, assigned to extracted key
    """

    if not callable(key):
        key = operator.attrgetter(key)

    result = collections.defaultdict(list)

    for each in _iter_all_or_first(elements):
        result[key(each)].append(each)

    return dict(result)


def select(source, *elements):
    """
    Select from mapping given values and put into new created dict::

        >>> select({'a': 1, 'b': 2, 'c':4}, 'a', 'c')
        {'a': 1, 'c': 4}

    :param source: mapping, from which values are selected
    :param elements: values which should be selected
    :return: dict with selected values
    """

    return extract(source, *elements, key=operator.getitem)


def extract(source, *elements, **kwargs):
    """
    Create dict with attributes name and associated value extracted from object,
    by keys given as parameter.

    :param source: object to extract
    :param elements: values which should be extracted
    :param key: two arguments function, which extract required argument (default getattr)
    :return: dict with extracted values
    """

    extractor = kwargs.get('key', getattr)

    return {value: extractor(source, value) for value in _iter_all_or_first(elements)}


def _iter_all_or_first(elements):
    if len(elements) > 1:
        return iter(elements)
    elif isinstance(elements[0], collections.Iterable):
        return iter(elements[0])
    else:
        return iter([elements[0]])


def merge(*dicts):
    """
    Merge dicts into single dict. If keys are duplicated, value is taken from last dict,
    which contains this key::

        >>> merge({'A': 1}, {'B': 2}, {'C': 3})
        {'A': 1, 'C': 3, 'B': 2}

    :param dicts: dicts to merge
    :return: dict contained all element from given dicts
    """

    def update(result, item):
        result.update(item)
        return result

    return functools.reduce(update, dicts, dict())


def split(dictionary, *conditions, **kwargs):
    """
    Split elements to other sets of elements according to given conditions, for example::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%2 == 0))
        [{0: 'A', 2: 'C', 4: 'E'}, {1: 'B', 3: 'D'}]

    When the elements which are not follow any given condition should be omitted set rest attribute to False::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%2 == 0, rest=False))
        [{0: 'A', 2: 'C', 4: 'E'}]

    When more than one condition is given element was included in first dictionary, which for condition
    was fulfilled::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0, lambda i: i%2 == 0))
        [{0: 'A', 3: 'D'}, {2: 'C', 4: 'E'}, {1: 'B'}]

    :param dictionary: elements to split into other sets of elements
    :param conditions: functions (name matters): key -> bool or  value -> bool or key, value -> bool)
        which decide that element in current result should be included or not
    :param rest: True if should append at end elements which not fulfilled any condition, False otherwise
    :return: generator for element split according to given condition
    """

    rest = kwargs.get('rest', True)

    for condition in conditions:
        selected, dictionary = _split_two(dictionary, condition)
        yield selected
    if rest:
        yield dictionary


def _split_two(dictionary, condition):
    selector = _selector(condition)

    yes, no = {}, {}

    for key, value in dictionary.items():
        if selector(key, value):
            yes[key] = value
        else:
            no[key] = value

    return yes, no


def sift(dictionary, condition, opposite=False):
    """
    Select elements from dictionary, which fulfilled given condition

    :param dictionary: set of elements to select subset
    :param condition: function (name matters): key -> bool or  value -> bool or key, value -> bool)
        selected remain elements
    :param opposite: if True replace "condition" by "not condition" (default False)
    :return: subset of elements which fulfilled given condition
    """

    selector = _selector(condition)

    return {key: value for key, value in dictionary.items() if bool(opposite) != bool(selector(key, value))}


def sift_update(dictionary, condition, opposite=False):
    """
    Works like sift_, but modify given dict in place.

    :param dictionary: set of elements to select subset
    :param condition: function (name matters): key -> bool or  value -> bool or key, value -> bool)
        selected remain elements
    :param opposite: if True replace "condition" by "not condition" (default False)
    """

    selector = _selector(condition)

    for each in list(dictionary):
        if bool(opposite) == bool(selector(each, dictionary[each])):
            del dictionary[each]


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


def find_key(value, dictionary, default=None):
    """
    Function find key in dict for given value. If not found return default value (None or given).
    If many elements can be found return one of it (first founded)::

        >>> find_key('d', {'a': 'b', 'c': 'd'})
        'c'

        >>> find_key('c', {'a': 'b', 'c': 'd'}, default=-1)
        -1

    :param value: value in dictionary, which for is searching a key
    :param dictionary: dictionary to search in
    :param default: value returned if value is not in dictionary (default None)
    :return: key which value in dictionary is assigned to
    """

    for key, item_value in dictionary.items():
        if value == item_value:
            return key

    return default

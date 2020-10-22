import collections
import functools
import operator
import inspect

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

def two_way(dictionary):
    """
    Create a new dict containing two-way associations (values to keys and keys to values)
    from the given dictionary::

        >>> two_way({'A': 1, 'B': 2})
        {'A': 1, 1: 'A', 2: 'B', 'B': 2}

    :param dict dictionary: one way association dict
    :return: two way association dict
    """
    return merge(swap(dictionary), dictionary)


def swap(dictionary):
    """
    Create a new dict with the given dictionary keys as values and values as keys::

        >>> stringify(swap({0: 'A', 1: 'B', 2: 'C'}))
        '{A:0, B:1, C:2}'

    :param dict dictionary: dict to swap
    :return: new swapped dict
    """

    return {value: key for key, value in dictionary.items()}


def by(key, *elements):
    """
    Create a new dict with the given elements as values,
    and the keys determined by the given parameter function::

        >>> by('real', (1+2j), (2-3j),(-5+0j))
        {1.0: (1+2j), 2.0: (2-3j), -5.0: (-5+0j)}

        >>> by('imag', [(1+2j), (2-3j),(-5+0j)])
        {0.0: (-5+0j), 2.0: (1+2j), -3.0: (2-3j)}

        >>> by(lambda x:int(x), "123", "456")
        {456: '456', 123: '123'}


    :param elements: iterable of elements or elements as varargs
    :param key: attribute, by which element could be accessed or lambda function
    :return: dict with elements, assigned to extracted key
    """

    if not callable(key):
        key = operator.attrgetter(key)

    return {key(element): element for element in _iter_all_or_first(elements)}


def group_by(key, *elements):
    """
    Create a new dict containing elements grouped by the given key.
    Returns a dict of list of values, with the same extracted key assigned to this key::

        >>> group_by('real', 2j, 0-3j, (-5+0j), (-3+2j), (-5+15j))
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


def select(source, *keys):
    """
    Create a new dict containing only the selected keys from the source dictionary.

        >>> stringify(select({'a': 1, 'b': 2, 'c':4}, 'a', 'c'))
        '{a:1, c:4}'

    :param source: mapping, from which values are selected
    :param keys: keys which should be selected
    :return: dict with selected values
    """

    return extract(source, *keys, key=operator.getitem)


def extract(source, *elements, **kwargs):
    """
    Create a new dict with attributes name and associated value extracted from object,
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
    elif isinstance(elements[0], Iterable):
        return iter(elements[0])
    else:
        return iter([elements[0]])


def merge(*dicts):
    """
    Merge the given dicts into a single new dict::

        >>> d = merge({'A': 1}, {'B': 2}, {'C': 3})
        >>> stringify(d)
        '{A:1, B:2, C:3}'

    If the same key is found in two or more dicts, the value is taken from last dict
    containing this key::

        >>> d = merge({'A': 1}, {'B': 2}, {'A': 3})
        >>> stringify(d)
        '{A:3, B:2}'


    If the first argument is a function, it is used to merge duplicate values::

        >>> d = merge(lambda x,y:x+y, {'A': 1}, {'B': 2}, {'A': 3})
        >>> stringify(d)
        '{A:4, B:2}'

    The returned type is of the same type as the first non-None dict in the list::

        >>> d = merge({'A': 1}, {'B': 2}, {'C': 3})
        >>> type(d)
        <class 'dict'>
        >>> from collections import OrderedDict
        >>> od = OrderedDict()
        >>> od["A"] = 1
        >>> d = merge(od, {'B': 2}, {'A': 3})
        >>> type(d)
        <class 'collections.OrderedDict'>
        >>> d = merge(None, od, {'B': 2}, {'A': 3})
        >>> type(d)
        <class 'collections.OrderedDict'>


    :param dicts: dicts to merge
    :return: dict containing all element from given dicts
    """
    if len(dicts) == 0:
        return {}

    if callable(dicts[0]):
        mergefunc = dicts[0]
        dicts = dicts[1:]

        def update(result, item):
            for k, v in item.items():
                result[k] = mergefunc(result[k], v) if k in result else v

            return result
    else:
        def update(result, item):
            result.update(item)
            return result

    dicts = [d for d in dicts if d is not None]

    if len(dicts) == 0:
        return {}

    TypeToReturn = type(dicts[0])
    return functools.reduce(update, dicts, TypeToReturn())


def split(dictionary, *conditions, **kwargs):
    """
    Split the dictionary to sub-dictionaries based on conditions operated on the keys::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0, lambda i: i%3 == 1))
        [{0: 'A', 3: 'D'}, {1: 'B', 4: 'E'}, {2: 'C'}]

    When the elements which do not follow any given condition should be omitted, set rest attribute to False::

        >>> list(split({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0, lambda i: i%3 == 1, rest=False))
        [{0: 'A', 3: 'D'}, {1: 'B', 4: 'E'}]

    When more than one condition is given, each element is included in the first dictionary for which the condition
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
    Select from dictionary only the keys for which the condition is True.

        >>> sift({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0)
        {0: 'A', 3: 'D'}

        >>> sift({0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}, lambda i: i%3 == 0, opposite=True)
        {1: 'B', 2: 'C', 4: 'E'}

    :param dictionary: set of elements to select subset
    :param condition: function (name matters): key -> bool or  value -> bool or key, value -> bool)
        selected remain elements
    :param opposite: if True replace "condition" by "not condition" (default False)
    :return: subset of elements which fulfilled given condition.
    """

    selector = _selector(condition)

    return {key: value for key, value in dictionary.items() if bool(opposite) != bool(selector(key, value))}


def sift_update(dictionary, condition, opposite=False):
    """
    Works like sift, but modifies the given dictionary in place.

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
    Check if sub dict is included in super dict (both keys and values are equal)::

        >>> contains({0: 'A', 1: 'B'}, {0: 'A', 1: 'B', 2: 'C'})
        True

        >>> contains({0: 'A', 1: 'B', 2: 'C'}, {0: 'A', 1: 'B'})
        False

    :param dict sub: the dict, which should be included in super dict
    :param dict super: the dict, which should include all elements from sub dict
    :return: true if super contains sub, otherwise false.
    """

    return all(
        key in super and sub[key] == super[key] for key, value in sub.items()
    )


def map_values(function, dictionary):
    """
    Transform each value using the given function. Return a new dict with transformed values.

    :param function: keys map function
    :param dictionary: dictionary to mapping
    :return: dict with changed values
    """

    return {key: function(value) for key, value in dictionary.items()}


def map_keys(function, dictionary):
    """
    Transform each key using the given function. Return a new dict with transformed keys.

    :param function: values map function
    :param dictionary: dictionary to mapping
    :return: dict with changed (mapped) keys
    """

    return {function(key): value for key, value in dictionary.items()}


def find_key(value, dictionary, default=None):
    """
    Find the given value in the given dictionary and returns its key.
    If value is not found - return default value (None or given).
    If many elements can be found - return one of them arbitrarily (the first one found)::

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


def fill_value(keys, value):
    """
    Return a dict with the given value assigned to each given key.

        >>> fill_value([1, 2, 3], 'a')
        {1: 'a', 2: 'a', 3: 'a'}

    :param keys: keys, which returned dict should contains
    :param value: value, which should be assigned to each key
    :return: dict with value assigned do each given key
    """
    return {key: value for key in keys}


def stringify(d):
    """
    Returns a canonical string representation of the given dict,
    by sorting its items recursively.
    This is especially useful in doctests::

        >>> stringify({"a":1,"b":2,"c":{"d":3,"e":4}})
        '{a:1, b:2, c:{d:3, e:4}}'
    """
    d2 = {}

    for k, v in d.items():
        d2[k] = stringify(v) if isinstance(v, dict) else v

    return "{" + ", ".join(["{}:{}".format(k, v) for k, v in sorted(d2.items())]) + "}"


def list_of_values(dictionary, list_of_keys, default=None):
    """
    Converts a dict to a list of its values,
    with the default value inserted for each missing key::

        >>> list_of_values({"a":1, "b":2, "d":4}, ["d","c","b","a"])
        [4, None, 2, 1]

        >>> list_of_values({"a":1, "b":2, "d":4}, ["d","c","b","a"], default=0)
        [4, 0, 2, 1]

    """
    result = []

    for key in list_of_keys:
        result.append(dictionary.get(key, default))

    return result


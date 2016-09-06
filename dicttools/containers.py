import bisect
import collections
import itertools


class FrozenDict(collections.Mapping):
    """
    Object represents pairs key-value, and works like dict, but cannot be
    modified. Also is hashable  in contrast to builtin dict.
    """

    def __init__(self, *args, **kwargs):
        """
        Init is analogical as dict:

        To create empty frozen dictionary::

            >>> FrozenDict()
            ${}

        To create frozen dict from mapping::

            >>> FrozenDict({'x': 4.5, 'y': 3})
            ${'x': 4.5, 'y': 3}

        To create frozen dict from iterable (of 2-tuple pairs of key and value)::

            >>> FrozenDict((('x', 4.5), ('y', 3)))
            ${'x': 4.5, 'y': 3}

        Using kwargs::

            >>> FrozenDict(x=4.5, y=3)
            ${'x': 4.5, 'y': 3}

        Using kwargs with other method::

            >>> FrozenDict({'x': 4.5}, y=3)
            ${'x': 4.5, 'y': 3}
        """

        if not kwargs and len(args) == 1 and isinstance(args[0], collections.Mapping):
            content = args[0]
        else:
            content = dict(*args, **kwargs)

        self._keys = tuple(sorted(content))
        self._values = tuple(content[key] for key in self._keys)

    def has_key(self, key):
        """
        Search key in contained keys and return True if founded, otherwise Fasle.

        :param key: key which is looked for
        :return: True if key is contained, otherwise False
        """
        return key in self

    def __getitem__(self, item):
        index = bisect.bisect_left(self._keys, item)

        if 0 <= index < len(self._keys) and self._keys[index] == item:
            return self._values[index]
        else:
            raise KeyError(item)

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def __hash__(self):
        return 13 * hash(self._values) + hash(self._keys)

    def __str__(self):
        return "${%s}" % self._str_content()

    def __repr__(self):
        return "FrozenDict({%s})" % self._str_content()

    def _str_content(self):
        return ', '.join('%r: %r' % each for each in self.items())

    def copy(self):
        return FrozenDict(self)


class ChainMap(collections.MutableMapping):
    """
    Object for multiple dicts aggregation for iterate, getting, setting and deleting
    as single dict.

    When key is many dict then item is consider as the fist founded::

        >>> chain = ChainMap([{'a': 1}, {'b': 2}, {'a': 4}])
        >>> chain['a']
        1

    In the same way works deletion and setting::

        >>> chain = ChainMap([{'a': 1}, {'b': 2}, {'a': 4}])
        >>> chain['a'] = 9
        >>> chain
        ChainMap([{'a': 9}, {'b': 2}, {'a': 4}])
        >>> del chain['a']
        >>> chain
        ChainMap([{}, {'b': 2}, {'a': 4}])

    When key is not in any of dicts (maps) KeyException is raised::

        >>> chain = ChainMap([{'a': 1}, {'b': 2}, {'a': 4}])
        >>> chain['x'] = 9
        Traceback (most recent call last):
        ...
        KeyError: 'x'

    """

    def __init__(self, maps):
        """
        Create view of iterable of dict tool set. Given argument is handle by reference,
        hence each change affected this chain. Given maps are encapsulated and cannot be
        accessed via ChainMap, so keep it separately.

        :param maps: iterable of dicts **(but not iterator)**
        """
        self._maps = maps

    def __iter__(self):
        return itertools.chain(*self._maps)

    def __getitem__(self, key):
        for item in self._maps:
            if key in item:
                return item[key]

        raise KeyError(key)

    def __setitem__(self, key, value):
        for item in self._maps:
            if key in item:
                item[key] = value
                return

        raise KeyError(key)

    def __delitem__(self, key):
        for item in self._maps:
            if key in item:
                del item[key]
                return

        raise KeyError(key)

    def __len__(self):
        return sum(map(len, self._maps))

    def __str__(self):
        return str(tuple(self._maps))

    def __repr__(self):
        return 'ChainMap(' + repr(list(self._maps)) + ')'
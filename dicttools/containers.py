import bisect
import collections


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

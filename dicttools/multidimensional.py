import six.moves
from .functions import map_values


class MultiDict(object):
    @classmethod
    def from_flat(cls, data, **kwargs):
        result = cls(**kwargs)
        for key, value in data.items():
            result[key] = value

        return result

    def __init__(self, data=None, headers=None):
        self._headers = None if headers is None else list(map(list, headers))

        self._items = {}

        if isinstance(data, (tuple, list)):
            self._items = dict(self._roll_array(data))
        elif isinstance(data, dict):
            self._items = data.copy()

        if self._items:
            self._init_headers(max(self._items))

    def _roll_array(self, data, index=()):
        for i, value in enumerate(data):
            value_index = index + (i,)
            if isinstance(value, list):
                for each in self._roll_array(value, value_index):
                    yield each
            else:
                yield value_index, value

    @property
    def shape(self):
        return tuple(map(len, self._headers or []))

    @property
    def size(self):
        return len(self._headers or [])

    def items(self):
        return tuple(
            (tuple(headers[token] for token, headers in zip(key, self._headers)), value)
            for key, value in self._items.items()
        )

    def __len__(self):
        return len(self._items)

    def __contains__(self, key):
        if not isinstance(key, tuple):
            key = (key,)

        try:
            return self.key_index(key) in self._items
        except KeyError:
            return False

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)

        if len(key) < self.size:
            key += (slice(None),) * (self.size - len(key))

        if not any(isinstance(token, (slice, list)) for token in key):
            return self._items[self.key_index(key)]
        else:
            return _MultiDictView(self, key)

    def reduce(self, index):
        index = self.key_index(index)
        return MultiDict(dict(self._reduce_keys(index)), list(self._reduce_headers(index)))

    def _reduce_keys(self, request_index):
        for source_index, source_value in self._items.items():
            result = []
            for request_token, source_token in zip(request_index, source_index):
                if isinstance(request_token, list):
                    if source_token not in request_token:
                        break

                    result.append(source_token)
                elif source_token != request_token:
                    break
            else:
                yield tuple(result), source_value

    def _reduce_headers(self, index):
        for token, header in zip(index, self._headers):
            if isinstance(token, list):
                yield header

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = (key,)

        self._init_headers(len(key))
        index = self.key_index(key, insert=True)

        self._items[index] = value

    def _init_headers(self, shape):
        if isinstance(shape, tuple):
            count = len(shape)
        else:
            count = shape
            shape = [0] * count

        if self._headers is None:
            self._headers = [list(six.moves.range(size + 1)) for size in shape]
        elif len(self._headers) != count:
            raise KeyError('Wrong size %d, expected %d' % (count, len(self._headers)))

    def key_index(self, key, insert=False):
        return tuple(
            self.token_index(token, axis, insert) for axis, token in enumerate(key)
        )

    def token_index(self, token, axis, insert=False):
        headers = self._headers[axis]

        if isinstance(token, slice):
            start = 0 if token.start is None else headers.index(token.start)
            stop = len(headers) if token.stop is None else headers.index(token.stop)
            step = 1 if token.step is None else token.step

            return list(six.moves.range(start, stop, step))
        elif isinstance(token, list):
            return [self._single_token_index(each, headers, insert) for each in token]
        else:
            return self._single_token_index(token, headers, insert)

    @staticmethod
    def _single_token_index(token, headers, insert):
        try:
            return headers.index(token)
        except ValueError:
            if not insert:
                raise KeyError(token)

        new_index = len(headers)
        headers.append(token)
        return new_index

    def merge(self, other):
        result = self.copy()

        for key, value in other.items():
            result[key] = value

        return result

    def copy(self):
        return MultiDict(self._items, self._headers)

    def map_values(self, function):
        return MultiDict(map_values(function, self._items), self._headers)

    def to_nested(self):
        def add(dictionary, key, value):
            if len(key) == 1:
                dictionary[key[0]] = value
            else:
                nested = dictionary.setdefault(key[0], {})
                add(nested, key[1:], value)

        result = {}

        for k, v in self.items():
            add(result, k, v)

        return result

    def __repr__(self):
        return repr(self._items)

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            other = MultiDict(other)

        if isinstance(other, MultiDict):
            return self._items == other._items

        return False

    def __ne__(self, other):
        return not self == other


class _DictView(object):
    def reduce(self, key=None):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            other = MultiDict(other)

        if isinstance(other, MultiDict):
            return self.reduce() == other

        return False

    def __len__(self):
        return len(self.reduce())

    def __repr__(self):
        return repr(self.reduce())

    def __ne__(self, other):
        return not self == other


class _MultiDictView(_DictView):
    def __init__(self, source, key):
        self._source = source
        self._key = key

    def __getitem__(self, key):
        return self._source[self._merge_key_with(key)]

    def __setitem__(self, key, value):
        self._source[self._merge_key_with(key)] = value

    def reduce(self, key=None):
        return self._source.reduce(
            self._key if key is None else self._merge_key_with(key)
        )

    def _merge_key_with(self, other_key):
        if not isinstance(other_key, tuple):
            other_key = (other_key,)

        result = []

        iter_keys = iter(other_key)
        for axis, item in enumerate(self._key):
            if isinstance(item, (slice, list)):
                try:
                    reduced_item = next(iter_keys)
                    self._check_contains(axis, item, other_key, reduced_item)
                    result.append(reduced_item)
                    continue
                except StopIteration:
                    pass

            result.append(item)

        return tuple(result)

    def _check_contains(self, axis, item, other_key, reduced_item):
        indices = self._source.token_index(item, axis)
        if isinstance(reduced_item, slice):
            reduced_indices = set(self._source.token_index(reduced_item, axis))

            if set(indices) | reduced_indices != reduced_indices:
                raise KeyError(other_key)

        elif self._source.token_index(reduced_item, axis) not in indices:
            raise KeyError(other_key)


class _NamedMixin(object):
    _names = ()

    def __getitem__(self, item):
        raise NotImplementedError

    def get(self, **kwargs):
        key = self._keywords_to_key(kwargs)
        result = self[key]

        if isinstance(result, _DictView):
            return _NamedMultiDictViewDecorator(result, self._reduce_names(key))

        return result

    def _keywords_to_key(self, kwargs):
        key = []

        for name in self._names:
            key.append(kwargs.pop(name, slice(None)))

        return tuple(key)

    def _reduce_names(self, key):
        result = []

        for name, token in zip(self._names, key):
            if isinstance(token, (slice, list)):
                result.append(name)

        return tuple(result)


class NamedMultiDict(MultiDict, _NamedMixin):
    def __init__(self, data=None, headers=None, names=None):
        super(NamedMultiDict, self).__init__(data, headers)
        self._names = names

    def map_values(self, function):
        return NamedMultiDict(map_values(function, self._items), self._headers, self._names)

    def copy(self):
        return NamedMultiDict(self._items, self._headers, self._names)


class _NamedMultiDictViewDecorator(_DictView, _NamedMixin):
    def __init__(self, view, names):
        self._view = view
        self._names = names

    def __getitem__(self, item):
        return self._view[item]

    def __setitem__(self, key, value):
        self._view[key] = value

    def items(self):
        return self.reduce().items()

    def reduce(self, key=None):
        result = self._view.reduce(key)
        return NamedMultiDict(result._items, result._headers, self._names)

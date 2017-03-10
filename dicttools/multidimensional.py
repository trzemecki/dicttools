import six.moves


class MultiDict(object):
    def __init__(self, data=None, headers=None):
        self._headers = None if headers is None else [list(each) for each in headers]

        self._items = {}

        if isinstance(data, (tuple, list)):
            self._items = dict(self._roll_array(data))
        elif isinstance(data, dict):
            self._items = data.copy()

        if self._items:
            self._init_headers(max(self._items))

    def _roll_array(self, data, index=()):
        for i, item in enumerate(data):
            item_index = index + (i,)
            if isinstance(item, list):
                for each in self._roll_array(item, item_index):
                    yield each
            else:
                yield item_index, item

    @property
    def shape(self):
        return tuple(map(len, self._headers or []))

    @property
    def size(self):
        return len(self._headers or [])

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)

        if len(key) < self.size:
            key += (slice(None),) * (self.size - len(key))

        if not any(isinstance(k, slice) for k in key):
            return self._items[self._map_key(key)]
        else:
            return _MultiDictView(self, key)

    def reduce(self, key):
        key = self._map_key(key)
        return MultiDict(dict(self._reduce_keys(key)), headers=list(self._reduce_headers(key)))

    def _reduce_keys(self, request_key):
        for source_key, source_value in self._items.items():
            result = []
            for request_index, source_index in zip(request_key, source_key):
                if isinstance(request_index, list):
                    if source_index not in request_index:
                        break

                    result.append(source_index)
                elif source_index != request_index:
                    break
            else:
                yield tuple(result), source_value

    def _reduce_headers(self, request_key):
        for request_index, header in zip(request_key, self._headers):
            if isinstance(request_index, list):
                yield header

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = (key,)

        self._init_headers(len(key))
        key = self._map_key(key, insert=True)

        self._items[key] = value

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

    def _map_key(self, request_key, insert=False):
        return tuple(
            self._map_index(request_index, headers, insert)
            for request_index, headers in zip(request_key, self._headers)
        )

    def item_to_index(self, item, column):
        return self._map_index(item, self._headers[column])

    def _map_index(self, item, headers, insert=False):
        if isinstance(item, slice):
            start = 0 if item.start is None else headers.index(item.start)
            stop = len(headers) if item.stop is None else headers.index(item.stop)
            step = 1 if item.step is None else item.step

            return list(six.moves.range(start, stop, step))

        try:
            return headers.index(item)
        except ValueError:
            if not insert:
                raise

        new_item = len(headers)
        headers.append(item)
        return new_item

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


class _MultiDictView(object):
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
        for col, item in enumerate(self._key):
            if isinstance(item, slice):
                try:
                    reduced_item = next(iter_keys)
                    self._check_contains(col, item, other_key, reduced_item)
                    result.append(reduced_item)
                    continue
                except StopIteration:
                    pass

            result.append(item)

        return tuple(result)

    def _check_contains(self, col, item, other_key, reduced_item):
        indices = self._source.item_to_index(item, col)
        if isinstance(reduced_item, slice):
            reduced_indices = set(self._source.item_to_index(reduced_item, col))

            if set(reduced_item) | reduced_indices != reduced_indices:
                raise KeyError(other_key)

        elif self._source.item_to_index(reduced_item, col) not in indices:
            raise KeyError(other_key)

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            other = MultiDict(other)

        if isinstance(other, MultiDict):
            return self.reduce() == other

        return False

    def __repr__(self):
        return repr(self.reduce())

    def __ne__(self, other):
        return not self == other

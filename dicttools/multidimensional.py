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
        return list(map(len, self._headers))

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)

        key = self._map_key(key)

        if not any(isinstance(k, list) for k in key):
            return self._items[key]
        else:
            return MultiDict(dict(self._reduce_keys(key)))

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
            self._headers = [list(six.moves.range(size)) for size in shape]
        elif len(self._headers) != count:
            raise KeyError('Wrong size %d, expected %d' % (count, len(self._headers)))

    def _map_key(self, key, insert=False):
        result = []

        for each, headers in zip(key, self._headers):
            if isinstance(each, slice):
                start = 0 if each.start is None else headers.index(each.start)
                stop = len(headers) if each.stop is None else headers.index(each.stop)
                step = 1 if each.step is None else each.step

                indices = list(six.moves.range(start, stop, step))
                result.append(indices)
            else:
                try:
                    index = headers.index(each)
                except ValueError:
                    if not insert:
                        raise

                    index = len(headers)
                    headers.append(each)

                result.append(index)

        return tuple(result)

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



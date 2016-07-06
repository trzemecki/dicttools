===============
Getting started
===============

First import module::

    >>> import dicttools

Now you can use dicttools functions. For example if you want to merge dict type::

    >>> dicttools.merge({'a': 1}, {'b': 2}, {'c': 3})
    {'a': 1, 'c': 3, 'b': 2}

To select items from dict::

    >>> dicttools.select({'a': 1, 'c': 3, 'b': 2}, 'a', 'b')
    {'a': 1, 'b': 2}

Also you can create FrozenDict::

    >>> frozen = dicttools.FrozenDict(a=1, b=2)
    >>> frozen
    FrozenDict({'a': 1, 'b': 2})

The FrozenDict is immutable, so it cannot be changed::

    >>> frozen['c'] = 3
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
    TypeError: 'FrozenDict' object does not support item assignment

But work just like dict::

    >>> frozen['a']
    1
    >>> list(frozen.items())
    [('a', 1), ('b', 2)]

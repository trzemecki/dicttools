=====================================
Welcome to Dicttools's documentation!
=====================================
.. |copy|   unicode:: U+000A9 .. COPYRIGHT SIGN

Version 1.1

Copyright |copy| 2016 by Leszek Trzemecki

Dicttools is open-source, Apache 2 licenced library with additional dict functions and classes.

Installation
------------

1. If you have not git yet, install it from https://git-scm.com/downloads
2. Install dicttools library using pip (https://pypi.python.org/pypi/pip)

    $ pip install git+git://github.com/trzemecki/dicttools.git

It it also possible to install it by cloning repository with zip on desktop, unpack it and then run setup.py,
but is more complicated than the way by using pip, so it will not be described.

Contents
--------

.. toctree::
    :maxdepth: 1

    functions
    classes
    license
    contact

Getting started
---------------

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


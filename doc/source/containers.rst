=================
Custom Containers
=================

FrozenDict
----------

``FrozenDict`` is unmodifiable ``dict``-like object (like ``tuple``) and therefore can be easy share between object or functions
without making copy. State of object (it's contents) is set in init and then cannot be changed (so called "frozen").
All functions works fine in both Python 2 and 3 thanks to ``collections.Mapping`` class, which encapsulate all differences
between Python versions (like viewitems in Python 2 renamed to items in Python 3).

It can be created like ``dict`` objects (it simply use dict object in ``__init__``) and have same functions like dict, without
methods to mutate state like ``__setitem__``. Also unlike dict, the FrozenDict has ``__hash__`` implementation, so that it can
be use in hash required places (like ``dict`` keys).

.. autoclass:: dicttools.FrozenDict
    :members: __init__


ChainMap
--------

The ``ChainMap`` is similar to ``collections.ChainMap``, but cannot be used as replacement. There are a few important
differences. This ``ChainMap`` is designed as view for iterable (``list``, ``tuple``, ``MappingView``, etc.) of maps (``dict`` or
other ``Mapping``). ``ChainMap`` allow to get, set, or delete items in dicts. When value cannot be founded, ``KeyException`` is raised.
Given maps is encapsulated inside ``ChainMap`` and cannot be called directly. For chaining maps directly keep object separately.
Each modification in maps automatically affect the chain, because maps is contained as reference (not as copy).

.. autoclass:: dicttools.ChainMap
    :members: __init__


TwoWayDict
----------

``TwoWayDict`` is container for storing pairs key-value with additional reversed access.
It means, when you assign value to key, the key can be also accessible by value.
Is important to handle both keys and variables as hashable.

.. autoclass:: dicttools.TwoWayDict
    :members: __init__
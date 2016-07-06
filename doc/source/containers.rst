=================
Custom Containers
=================

FrozenDict
----------

FrozenDict is unmodifiable dict-like object (like tuple) and therefore can be easy share between object or functions
without making copy. State of object (it's contents) is set in init and then cannot be changed (so called "frozen").
All functions works fine in both Python 2 and 3 thanks to collections.Mapping class, which encapsulate all differences
between Python versions (like viewitems in Python 2 renamed to items in Python 3).

It can be created like dict objects (it simply use dict object in init) and have same functions like dict, without
methods to mutate state like __setitem__. Also unlike dict, the FrozenDict has __hash__ implementation, so that it can
be use in hash required places (like dict keys).

.. autoclass:: dicttools.FrozenDict
    :members: __init__
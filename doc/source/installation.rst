============
Installation
============

Using pip (recommended)
-----------------------

1. If you have not git yet, install it from https://git-scm.com/downloads
2. Install dicttools library using pip (https://pypi.python.org/pypi/pip)

.. code-block:: bash

    $ pip install git+git://github.com/trzemecki/dicttools.git

3. If you have already installed previous version, upgrade it by:

.. code-block:: bash

    $ pip install git+git://github.com/trzemecki/dicttools.git --upgrade

By downloading
--------------

1. Clone repository on desktop (git required: https://git-scm.com/downloads)

.. code-block:: bash

    $ git clone https://github.com/trzemecki/dicttools.git

2. If you cannot clone, download zip (https://github.com/trzemecki/dicttools/archive/master.zip) and unpack

3. Go to directory containing `setup.py` file

4. Run tests (optional)

.. code-block:: bash

    $ python setup.py test

5. If all tests passed, install

.. code-block:: bash

    $ python setup.py install
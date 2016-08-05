.. _installation:

knittingpattern Installation Instructions
=========================================

Package installation from Pypi
------------------------------

The knittingpattern library requires `Python 3 <https://www.python.org/>`__.
It can be installed form the `Python Package Index
<https://pypi.python.org/pypi/knittingpattern>`__.

Windows
~~~~~~~

Install it with a specific python version under windows:

.. code:: bash

    py -3 -m pip --no-cache-dir install --upgrade knittingpattern

Test the installed version:

.. code:: bash

    py -3 -m pytest --pyargs knittingpattern

Linux
~~~~~ 

To install the version from the python package index, you can use your terminal and execute this under Linux:

.. code:: shell
  
  sudo python3 -m pip --no-cache-dir install --upgrade knittingpattern

test the installed version:

.. code:: shell
  
  python3 -m pytest --pyargs knittingpattern

.. _installation-repository:

Installation from Repository
----------------------------

You can setup the development version under Windows and Linux.

.. _installation-repository-linux:

Linux
~~~~~

If you wish to get latest source version running, you can check out the repository and install it manually.

.. code:: bash

  git clone https://github.com/fossasia/knittingpattern.git
  cd knittingpattern
  sudo python3 -m pip install --upgrade pip
  sudo python3 -m pip install -r requirements.txt
  sudo python3 -m pip install -r test-requirements.txt
  py.test

To also make it importable for other libraries, you can link it into the site-packages folder this way:

.. code:: bash

  sudo python3 setup.py link

.. _installation-repository-windows:

Windows
~~~~~~~

Same as under :ref:`installation-repository-linux` but you need to replace
``sudo python3`` with ``py -3``. This also counts for the following
documentation.

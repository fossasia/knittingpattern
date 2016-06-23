knittingpattern
===============

.. image:: https://travis-ci.org/AllYarnsAreBeautiful/knittingpattern.svg
   :target: https://travis-ci.org/AllYarnsAreBeautiful/knittingpattern
   :alt: Build Status

.. image:: https://codeclimate.com/github/AllYarnsAreBeautiful/knittingpattern/badges/gpa.svg
   :target: https://codeclimate.com/github/AllYarnsAreBeautiful/knittingpattern
   :alt: Code Climate

.. image:: https://codeclimate.com/github/AllYarnsAreBeautiful/knittingpattern/badges/coverage.svg
   :target: https://codeclimate.com/github/AllYarnsAreBeautiful/knittingpattern/coverage
   :alt: Test Coverage

.. image:: https://codeclimate.com/github/AllYarnsAreBeautiful/knittingpattern/badges/issue_count.svg
   :target: https://codeclimate.com/github/AllYarnsAreBeautiful/knittingpattern
   :alt: Issue Count

.. image:: https://badge.fury.io/py/knittingpattern.svg
   :target: https://pypi.python.org/pypi/knittingpattern
   :alt: Issue Count
   
.. image:: https://img.shields.io/pypi/dm/knittingpattern.svg
   :target: https://pypi.python.org/pypi/knittingpattern#downloads
   :alt: Downloads from pypi   

.. image:: https://readthedocs.org/projects/knittingpattern/badge/?version=latest
   :target: https://knittingpattern.readthedocs.org
   :alt: Read the Documentation

   
Installation
============ 

To install the version from the python package index, you can use your command line and execute this under Linux:

.. code:: shell
  
  python3 -m pip install knittingpattern

Under Windows you can use


.. code:: shell
  
  py -3 -m pip install knittingpattern

Installation from Repository (Linux)
------------------------------------

If you wish to get latest source version running, you can check out the repository and install it manually.

Note: Under Windows you can replace `python3` with `py -3` and remove `sudo`

.. code:: shell

  git clone https://github.com/AllYarnsAreBeautiful/knittingpattern.git
  cd knittingpattern
  sudo python3 -m pip install --upgrade pip
  sudo python3 -m pip install -r requirements.txt
  sudo python3 -m pip install -r test-requirements.txt
  py.test

To also make it importable for other libraries, you can link it into the site-packages folder this way:

.. code:: shell

  sudo python3 setup.py link


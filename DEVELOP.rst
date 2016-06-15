Version
-------


1. Create a new branch for the version.

.. code:: bash

 git checkout -b <new_version>

2. Increase the ``__version__`` in `__init__.py
<knittingpattern/__init__.py>`_
  - no letter at the end means release
  - ``b`` in the end means Beta
  - ``a`` in the end means Alpha

3. Commit and upload this version.
  
.. code:: bash
  
  git push origin <new_version>
    
4. Create a pull-request.
5. Wait for `travis-ci
<https://travis-ci.org/AllYarnsAreBeautiful/knittingpattern>`_
  to pass the tests.
6. Merge the pull-request.
7. Upload_
  

Upload
------

.. Upload:

First ensure all tests are running:

.. code:: bash

    setup.py pep8


From `docs.python.org
<https://docs.python.org/3.1/distutils/uploading.html>`_:

.. code:: bash

    setup.py sdist bdist_wininst upload register

Install
-------

Install it with a specific python verison under windows:

.. code:: cmd

    py -3.5 -m pip --no-cache-dir install --upgrade knittingpattern

Test the installed version. You might have forgotten some includes:

.. code:: cmd

    cd C:\Python35-32\Lib\site-packages
    py -3.5 -m pytest knittingpattern

Classifiers
-----------

You can find all Pypi classifiers `here
<http://pypi.python.org/pypi?%3Aaction=list_classifiers>`_.

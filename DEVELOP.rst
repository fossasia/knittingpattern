Version
-------

Throughout this chapter, ``<new_version>`` refers to a a string of the form ``[0-9]+\.[0-9]+\.[0-9]+[ab]?`` or ``<MAYOR>.<MINOR>.<STEP>[<MATURITY>]`` where ``<MAYOR>``, ``<MINOR>`` and, ``<STEP>`` represent numbers and ``<MATURITY>`` can be a letter to indicate how mature the release is.

1. Create a new branch for the version.

.. code:: bash

  git checkout -b <new_version>

2. Increase the ``__version__`` in `__init__.py <knittingpattern/__init__.py#L3>`_

   - no letter at the end means release
   - ``b`` in the end means Beta
   - ``a`` in the end means Alpha

3. Commit and upload this version.

.. code:: bash
  
  git add knittingpattern/__init__.py
  git commit -m "version <new_version>"
  git push origin <new_version>

4. Create a pull-request.

5. Wait for `travis-ci <https://travis-ci.org/AllYarnsAreBeautiful/knittingpattern>`_ to pass the tests.

6. Merge the pull-request.
7. Tag the version at the master branch with a ``v`` in the beginning and push it to github

.. code:: bash

  git checkout master
  git pull
  git tag v<new_version>
  git push origin v<new_version>

8. Upload_ the code to Pypi.
  

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

Install it with a specific python version under windows:

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

Version Pinning
===============

We use version pinning, described in `this blog post (outdated)
<http://nvie.com/posts/pin-your-packages/>`__.
Also read the `current version
<https://github.com/nvie/pip-tools>`__ for how to set up.

After installation you can run

    pip-sync requirements.txt dev-requirements.txt test-requirements.txt
    pip-compile --output-file requirements.txt requirements.in
    pip-compile --output-file test-requirements.txt test-requirements.in
    pip-compile --output-file dev-requirements.txt dev-requirements.in
    pip install --upgrade -r requirements.txt -r test-requirements.txt -r dev-requirements.txt

This uninstalls every package you do not need and 
writes the fix package versions to the requirements files.

Continuous Integration to Pypi
==============================

Before you put something on Pypi, ensure the following:

1. The version in in the master branch on github.
2. The tests run by travis-ci run successfully.

Pypi is automatically deployed by travis. `See here
<https://docs.travis-ci.com/user/deployment/pypi>`__.
To upload new versions, tag them with git and push them.

.. code:: bash

  setup.py tag_and_deploy

The tag shows up as a `travis build
<https://travis-ci.org/AllYarnsAreBeautiful/knittingpattern/builds>`__.
If the build succeeds, it is automatically deployed to `Pypi
<https://pypi.python.org/pypi/knittingpattern>`__.

Manual Upload to the Python Package Index
=========================================


However, here you can see how to upload this package manually.

Version
-------

Throughout this chapter, ``<new_version>`` refers to a a string of the form ``[0-9]+\.[0-9]+\.[0-9]+[ab]?`` or ``<MAYOR>.<MINOR>.<STEP>[<MATURITY>]`` where ``<MAYOR>``, ``<MINOR>`` and, ``<STEP>`` represent numbers and ``<MATURITY>`` can be a letter to indicate how mature the release is.

1. Create a new branch for the version.

.. code:: bash

  git checkout -b <new_version>

2. Increase the ``__version__`` in `__init__.py <knittingpattern/__init__.py#L3>`__

   - no letter at the end means release
   - ``b`` in the end means Beta
   - ``a`` in the end means Alpha

3. Commit and upload this version.

.. _commit:

.. code:: bash
  
  git add knittingpattern/__init__.py
  git commit -m "version <new_version>"
  git push origin <new_version>

4. Create a pull-request.

5. Wait for `travis-ci <https://travis-ci.org/AllYarnsAreBeautiful/knittingpattern>`__ to pass the tests.

6. Merge the pull-request.
7. Checkout the master branch and pull the changes from the commit_.

.. code:: bash

  git checkout master
  git pull

8. Tag the version at the master branch with a ``v`` in the beginning and push it to github.

.. code:: bash

  git tag v<new_version>
  git push origin v<new_version>

9. Upload_ the code to Pypi.
  

Upload
------

.. Upload:

First ensure all tests are running:

.. code:: bash

    setup.py pep8


From `docs.python.org
<https://docs.python.org/3.1/distutils/uploading.html>`__:

.. code:: bash

    setup.py sdist bdist_wininst upload register
    
Classifiers
-----------

You can find all Pypi classifiers `here
<http://pypi.python.org/pypi?%3Aaction=list_classifiers>`_.

Package installation from Pypi
==============================

Install it with a specific python version under windows:

.. code:: cmd

    py -3.5 -m pip --no-cache-dir install --upgrade knittingpattern

Test the installed version. You might have forgotten some includes:

.. code:: cmd

    cd C:\Python35-32\Lib\site-packages
    py -3.5 -m pytest knittingpattern


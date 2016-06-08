#!/usr/bin/python3
import os
import sys
from setuptools.command.test import test as TestCommandBase

PACKAGE_NAME = "knittingpattern"
PACKAGE_NAMES = [
        "knittingpattern",
        "knittingpattern.convert", "knittingpattern.convert.test"
    ]

__doc__ = '''
The setup and build script for the {} library.
'''.format(PACKAGE_NAME)
__version__ = __import__(PACKAGE_NAME).__version__
__author__ = 'Nicco Kunzmann'

HERE = os.path.dirname(__file__)


def read_file_named(file_name):
    file_path = os.path.join(HERE, file_name)
    with open(file_path) as f:
        return f.read()


def read_filled_lines_from_file_named(file_name):
    content = read_file_named("requirements-test.txt")
    lines = content.splitlines()
    return [line for line in lines if line]


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name=PACKAGE_NAME,
    version=__version__,
    packages=PACKAGE_NAMES,
    author=__author__,
    author_email='niccokunzmann@rambler.ru',
    description='Python library for knitting machines.',
    license='MIT',
    url='https://github.com/AllYarnsAreBeautiful/' + PACKAGE_NAME,
    keywords='knitting ayab fashion',
)

# Run tests in setup


class TestCommand(TestCommandBase):

    TEST_ARGS = []

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = self.TEST_ARGS

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class CoverageTestCommand(TestCommand):
    TEST_ARGS = ["--cov=" + PACKAGE_NAME]


class PEP8TestCommand(TestCommand):
    TEST_ARGS = ["--pep8"]


class FlakesTestCommand(TestCommand):
    TEST_ARGS = ["--flakes"]


class CoveragePEP8TestCommand(TestCommand):
    TEST_ARGS = ["--cov=" + PACKAGE_NAME, "--pep8"]


class LintCommand(TestCommandBase):

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = [PACKAGE_NAME]

    def run_tests(self):
        from pylint.lint import Run
        Run(self.test_args)

# Extra package metadata to be used only if setuptools is installed
required_packages = \
    read_filled_lines_from_file_named("requirements.txt")
required_test_packages = \
    read_filled_lines_from_file_named("requirements-test.txt")

SETUPTOOLS_METADATA = dict(
    install_requires=required_packages,
    tests_require=required_test_packages,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    package_data=dict(
        # If any package contains of these files, include them:
        knitting=['*.json'],
    ),
    zip_safe=False,
    cmdclass={
        "test": TestCommand,
        "coverage": CoverageTestCommand,
        "coverage_test": CoverageTestCommand,
        "pep8": PEP8TestCommand,
        "pep8_test": PEP8TestCommand,
        "flakes": FlakesTestCommand,
        "fakes_test": FlakesTestCommand,
        "coverage_pep8_test": CoveragePEP8TestCommand,
        "lint": LintCommand,
        },
)


def main():
    # Build the long_description from the README and CHANGES
    METADATA['long_description'] = read_file_named("README.rst")

    # Use setuptools if available, otherwise fallback and use distutils
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)

if __name__ == '__main__':
    main()

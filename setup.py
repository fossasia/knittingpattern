#!/usr/bin/python3
"""The setup and build script for the library named "PACKAGE_NAME"."""
import os
import sys
from setuptools.command.test import test as TestCommandBase
from distutils.core import Command
import subprocess

PACKAGE_NAME = "knittingpattern"
PACKAGE_NAMES = [
        "knittingpattern",
        "knittingpattern.convert", "knittingpattern.convert.test"
    ]

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, HERE)  # for package import

__version__ = __import__(PACKAGE_NAME).__version__
__author__ = 'Nicco Kunzmann'


def read_file_named(file_name):
    file_path = os.path.join(HERE, file_name)
    with open(file_path) as file:
        return file.read()


def read_requirements_file(file_name):
    content = read_file_named(file_name)
    lines = []
    for line in content.splitlines():
        comment_index = line.find("#")
        if comment_index >= 0:
            line = line[:comment_index]
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return lines


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name=PACKAGE_NAME,
    version=__version__,
    packages=PACKAGE_NAMES,
    author=__author__,
    author_email='niccokunzmann@rambler.ru',
    description='Python library for knitting machines.',
    license='LGPL',
    url='https://github.com/AllYarnsAreBeautiful/' + PACKAGE_NAME,
    keywords='knitting ayab fashion',
)

# Run tests in setup


class TestCommand(TestCommandBase):

    TEST_ARGS = [PACKAGE_NAME]

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = self.TEST_ARGS

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class CoverageTestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--cov=" + PACKAGE_NAME]


class PEP8TestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--pep8"]


class FlakesTestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--flakes"]


class CoveragePEP8TestCommand(TestCommand):
    TEST_ARGS = [PACKAGE_NAME, "--cov=" + PACKAGE_NAME, "--pep8"]


class LintCommand(TestCommandBase):

    def finalize_options(self):
        TestCommandBase.finalize_options(self)
        self.test_suite = True
        self.test_args = [PACKAGE_NAME]

    def run_tests(self):
        from pylint.lint import Run
        Run(self.test_args)


# command for linking


class LinkIntoSitePackagesCommand(Command):

    description = "link this module into the site-packages so the latest "\
        "version can always be used without installation."
    user_options = []
    library_path = os.path.join(HERE, PACKAGE_NAME)
    site_packages = [p for p in sys.path if "site-packages" in p]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        assert self.site_packages, "We need a folder to install to."
        print("link: {} -> {}".format(
                  os.path.join(self.site_packages[0], PACKAGE_NAME),
                  self.library_path
              ))
        try:
            if "win" in sys.platform:
                self.run_windows_link()
            elif "linux" == sys.platform:
                self.run_linux_link()
            else:
                self.run_other_link()
        except:
            print("failed:")
            raise
        else:
            print("linked")

    def run_linux_link(self):
        subprocess.check_call(["sudo", "ln", "-f", "-s", "-t",
                               self.site_packages[0], self.library_path])

    run_other_link = run_linux_link

    def run_windows_link(self):
        path = os.path.join(self.site_packages[0], PACKAGE_NAME)
        if os.path.exists(path):
            os.remove(path)
        command = ["mklink", "/J", path, self.library_path]
        subprocess.check_call(command, shell=True)

# Extra package metadata to be used only if setuptools is installed

required_packages = read_requirements_file("requirements.txt")
required_test_packages = read_requirements_file("test-requirements.txt")

# print requirements


class PrintRequiredPackagesCommand(Command):

    description = "Print the packages to install. "\
                  "Use pip install `setup.py requirements`"
    user_options = []
    name = "requirements"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        packages = list(set(required_packages + required_test_packages))
        packages.sort(key=lambda s: s.lower())
        for package in packages:
            print(package)

# set development status from __version__

DEVELOPMENT_STATES = {
        "p": "Development Status :: 1 - Planning",
        "pa": "Development Status :: 2 - Pre-Alpha",
        "a": "Development Status :: 3 - Alpha",
        "b": "Development Status :: 4 - Beta",
        "": "Development Status :: 5 - Production/Stable",
        "m": "Development Status :: 6 - Mature",
        "i": "Development Status :: 7 - Inactive"
    }
development_state = DEVELOPMENT_STATES[""]
for ending in DEVELOPMENT_STATES:
    if ending and __version__.endswith(ending):
        development_state = DEVELOPMENT_STATES[ending]

if not __version__[-1:].isdigit():
    METADATA["version"] += "0"

# tag and upload to github to autodeploy with travis


class TagAndDeployCommand(Command):

    description = "Create a git tag for this version and push it to origin."\
                  "To trigger a travis-ci build and and deploy."
    user_options = []
    name = "tag_and_deploy"
    remote = "origin"
    branch = "master"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if subprocess.call(["git", "--version"]) != 0:
            print("ERROR:\n\tPlease install git.")
            exit(1)
        status_lines = subprocess.check_output(["git", "status"]).splitlines()
        current_branch = status_lines[0].strip().split()[-1].decode()
        print("On branch {}.".format(current_branch))
        if current_branch != self.branch:
            print("ERROR:\n\tNew tags can only be made from branch \"{}\"."
                  "".format(self.branch))
            print("\tYou can use \"git checkout {}\" to switch the branch."
                  "".format(self.branch))
            exit(1)
        tags_output = subprocess.check_output(["git", "tag"])
        tags = [tag.strip().decode() for tag in tags_output.splitlines()]
        tag = "v" + __version__
        if tag in tags:
            print("Warning: \n\tTag {} already exists.".format(tag))
            print("\tEdit the version information in {}".format(
                    os.path.join(HERE, PACKAGE_NAME, "__init__.py")
                ))
        else:
            print("Creating tag \"{}\".".format(tag))
            subprocess.check_call(["git", "tag", tag])
        print("Pushing tag \"{}\" to remote \"{}\".".format(tag, self.remote))
        subprocess.check_call(["git", "push", self.remote, tag])


SETUPTOOLS_METADATA = dict(
    install_requires=required_packages,
    tests_require=required_test_packages,
    include_package_data=True,
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License'
        ' v3 (LGPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Artistic Software',
        'Topic :: Home Automation',
        'Topic :: Utilities',
        'Intended Audience :: Manufacturing',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        development_state
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
        "link": LinkIntoSitePackagesCommand,
        PrintRequiredPackagesCommand.name: PrintRequiredPackagesCommand,
        TagAndDeployCommand.name: TagAndDeployCommand
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
    if len(sys.argv) == 2 and sys.argv[1] == PrintRequiredPackagesCommand.name:
        PrintRequiredPackagesCommand.run()
    else:
        main()

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='comics_downloader',
    version='0.1',
    author='Arnold Krille',
    author_email='arnold@arnoldarts.de',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'comics_downloader = comic_downloader.informationextractor:run'
        ]
    },
    tests_require=['pytest', 'pytest-xdist'],
    cmdclass={'test': PyTest},
)

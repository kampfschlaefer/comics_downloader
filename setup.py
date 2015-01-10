from setuptools import setup, find_packages

setup(
    name='comics_downloader',
    version='0.1',
    author='Arnold Krille',
    author_email='arnold@arnoldarts.de',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['comics_downloader = comic_downloader.informationextractor:run']
    },
)
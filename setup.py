import codecs
import os.path
import re

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='deepl-cli',
    version=find_version('deeplcli', '__init__.py'),
    description='Universal Command Line Environment for DeepL APIs.',
    py_modules=['deeplcli'],
    entry_points={
        'console_scripts': [
            'deepl = deeplcli.deepl:main',
        ]
    },
    install_requires=[],
)

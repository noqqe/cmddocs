# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
import sys

# file read helper
def read_from_file(path):
    if os.path.exists(path):
        with open(path,"rb","utf-8") as input:
            return input.read()

version = "1.0.3"

setup(
    name='cmddocs',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='An interactive commandline interface for your personal docs using python, Cmd, git and markdown',
    long_description=read_from_file('README.rst'),

    # The project's main homepage.
    url='https://github.com/noqqe/cmddocs',

    # Author details
    author='Florian Baumann',
    author_email='flo@noqqe.de',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='markdown wiki commandline git',
    packages=find_packages(),
    zip_safe=True,
    install_requires=['future', 'gitpython', 'configparser', 'mistune'],

    entry_points={
        'console_scripts': [
            'cmddocs=cmddocs:main',
        ],
    },
)

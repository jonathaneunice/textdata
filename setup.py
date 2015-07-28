#!/usr/bin/env python

from setuptools import setup

setup(
    name='textdata',
    version='1.1.1',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description='Get clean data easily direct from Python source',
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/jeunice/textdata',
    py_modules=['textdata'],
    install_requires=[],
    tests_require=['six', 'tox', 'pytest'],
    zip_safe=False,  # it really is, but this will prevent weirdness
    keywords='text data lines dedent words qw',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

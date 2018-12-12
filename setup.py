#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='ALIAS',
    description='ALIAS',
    author='Marcin Szczot, Roberto La Greca',
    license='GNU',
    url='https://github.com/alias-org/alias.git',
    author_email='mszczot@gmail.com, roberto@robertolagreca.com',
    version='0.2',
    classifiers=[
        'Development Status :: 3 - Alpha'
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['tables', 'ortools', 'parameterized', 'matplotlib', 'scipy', 'numpy', 'pycosat', 'flask', 'pyparsing', 'networkx', 'slqalchemy', 'py2neo'],
    packages=find_packages(exclude=['docs', 'tests*'])
    },
    tests_require=['nose'],
)

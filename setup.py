#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from sys import version_info

assert version_info >= (2,7)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
setup(
    name='molly',
    version='2.0dev',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='http://mollyproject.org/',
    author='The Molly Project',
    license='Apache License 2.0',
    setup_requires=['setuptools'],
    tests_require=['unittest2', 'mock'],
    test_suite='unittest2.collector',
    install_requires=[
        'celery==3.0.24',
        'Flask',
        'Flask-Babel',
        'Flask-Cache',
        'Flask-PyMongo',
        'Flask-Script',
        'geojson',
        'gunicorn',
        'imposm.parser',
        'phonenumbers==5.7b2',
        'pyelasticsearch',
        'python-dateutil',
        'python-memcached',
        'requests',
        'Shapely'
    ],
    entry_points={
        'console_scripts': [
            'molly = molly.command:main'
        ]
    }
)

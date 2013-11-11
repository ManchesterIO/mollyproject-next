#!/usr/bin/env python

from setuptools import setup, find_packages
from sys import version_info

assert version_info >= (2,7)

setup(
    name='molly',
    version='2.0dev',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='http://mollyproject.org/',
    author='The Molly Project',
    setup_requires=['setuptools'],
    tests_require=['unittest2', 'mock'],
    test_suite='unittest2.collector',
    install_requires=[
        'celery==3.0.24',
        'cssmin',
        'Flask',
        'Flask-Assets',
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
            'mollyui = molly.command:ui_main',
            'mollyrest = molly.command:rest_main'
        ]
    }
)

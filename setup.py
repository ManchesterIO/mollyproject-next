from setuptools import setup, find_packages
from sys import version_info

assert version_info >= (2,7)

setup(
    name='molly',
    version='2.0dev',
    packages=find_packages(exclude=['tests']),
    url='http://mollyproject.org/',
    author='The Molly Project',
    setup_requires=['setuptools'],
    tests_require=['unittest2', 'mock'],
    test_suite='unittest2.collector',
    install_requires=[
        'celery',
        'cssmin',
        'Flask',
        'Flask-Assets',
        'Flask-Babel',
        'Flask-Cache',
        'Flask-PyMongo',
        'Flask-Script',
        'Flask-StatsD',
        'geojson',
        'gunicorn',
        'imposm.parser',
        'phonenumbers==5.7b2',
        'python-dateutil',
        'python-memcached',
        'raven',
        'requests',
        'Shapely',
        'supervisor'
    ],
    entry_points={
        'console_scripts': [
            'mollyui = molly.command:ui_main',
            'mollyrest = molly.command:rest_main',
            'mollyd = molly.command:mollyd',
            'mollydebugd = molly.command:mollydebugd',
            'mollyctl = molly.command:mollyctl',
            'mollydebugctl = molly.command:mollydebugctl'
        ]
    }
)

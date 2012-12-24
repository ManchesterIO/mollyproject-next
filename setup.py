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
    entry_points={
        'console_scripts': [
            'mollyui = molly.ui.html5.command:main',
            'mollyrest = molly.command:main'
        ]
    }
)

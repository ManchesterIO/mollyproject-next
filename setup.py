from setuptools import setup, find_packages

setup(
    name='molly-ui-html5',
    version='2.0dev',
    packages=find_packages(exclude=['tests']),
    url='http://mollyproject.org/',
    author='The Molly Project',
    setup_requires=['setuptools'],
    tests_require=['unittest2', 'mock'],
    test_suite='unittest2.collector'
)

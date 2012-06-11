from setuptools import setup, find_packages

setup(
    name='tch',
    version='1.0dev',
    packages=find_packages(exclude=['tests']),
    url='http://github.com/cnorthwood/tch',
    license='GNU General Public License (version 3)',
    author='Chris Northwood',
    author_email='chris@pling.org.uk',
    description='The Transport Clearing House is a library for dealing with ' \
                'different forms of transport data in a unified manner',
    setup_requires=['setuptools'],
    tests_require=['unittest2', 'mock'],
    test_suite='unittest2.collector',
    install_requires=['pymongo', 'shapely', 'geojson'],
)

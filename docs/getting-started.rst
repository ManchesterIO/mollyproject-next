Getting Started with Transport Clearing House
=============================================

.. info:: You may wish to use `virtualenv <http://www.virtualenv.org/>`_ to manage your installation of Transport
          Clearing House.

geos
----

As the Transport Clearing House does lots of geographical calculations, it depends on the system library
`geos <http://trac.osgeo.org/geos/>`_ to be installed. Most


Installing Transport Clearing House
-----------------------------------

.. code-block:: none

    git clone https://github.com/cnorthwood/tch.git
    cd tch
    python setup.py install

This will install the latest (possibly broken and unstable) version of Transport Clearing House. When installing using
this form, you can also run the unit test suite and behaviour suite.

Unit Test Suite
~~~~~~~~~~~~~~~

.. code-block:: none

    python setup.py test

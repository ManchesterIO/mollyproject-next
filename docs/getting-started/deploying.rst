Deploying Molly
===============

.. note:: If you are using Chef, the cookbook will have done all this for you already, using supervisor to manage the
          processes.

Once Molly is installed (this guide assumes into ``/opt/molly``) and a config file created, then you need to start Molly.
Different components of Molly's run time exist, and can be scaled to different servers depending on how you see fit.

.. todo: Document how to put UI/REST services on different servers.

These components are:

* UI
* API
* Task worker
* Task beat (triggers running scheduled tasks)

.. warning:: Unlike the other servers, Task beat must be a singleton, otherwise multiple instances of the same job may
             be put on to the queue. Additionally, state about the schedule is stored on disk

.. todo:: Refactor taskbeat to not store state on disk.

These commands rely on an environment variable named ``MOLLY_CONFIG`` to point to the absolute URL of your previously
defined config file. Additionally, the UI server requires an environment variable named ``MOLLY_UI_SETTINGS`` to
point to the UI config file.

To start the servers, you can run the following commands:

* ``mollyrest start`` to start the API server
* ``mollyui start`` to start the UI server
* ``mollyrest taskworker`` to start the task worker
* ``mollyrest taskbeat`` to start the task beat

Additionally, the ``mollyrest`` and ``mollyui`` commands expose other potentially useful commands. For example,
``start_debug`` instead of just ``start`` will start the server in debug mode. Running either ``mollyrest`` or
``mollyui`` without arguments will list all the commands available to you. This can be useful to force a particular
importer to run, for example.

It is recommended that these commands are daemonized using a tool like `supervisor <http://supervisord.org/>`_.

Reverse proxies
---------------

It is not recommended to directly expose the Molly servers to the outside world, neither is it recommended to run the
applications as root so that they can listen on port 80. The recommended configuration is to use a tool like Apache httpd
or nginx

Static file serving
-------------------

The Molly UI server is not optimised for serving static files. It is recommended that you configure your webserver to
serve the folder defined in the ``ASSET_DIR`` setting under the ``/static`` URL.

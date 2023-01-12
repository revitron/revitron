Model Analytics
===============

Revitron ships with a small CLI wrapper that uses the *pyRevit CLI* in the background in order to
automatically collect model analytics using a task scheduler such as the *Windows Task Scheduler*.
The CLI analyzer is configured using a **JSON** file that is passed as argument. The configuration includes 
the *model path*, *storage configuration*, the *Revit version* and the *data providers*.

.. code-block::

    revitron analyze "path\to\config.json"

Introduction
------------

Conceptually the ``revitron analyze config.json`` command reads a *JSON* file, opens the configured Revit version, 
opens the given model, creates data provider instances as configured and sends the extracted data to a storage driver.

.. container:: .image-mockup

    .. image:: https://github.com/revitron/revitron-charts/raw/master/images/charts.png

*Data providers* are basically not more than a class that filters elements and aggregates a certain property or counts 
certain items in a model. *Storage drivers* are interfaces to data storage formats such as *JSON*, *SQLite* or a *RESTful API*. 
However, for the time being, only `Directus <https://directus.io/>`_ is supported as RESTful API.

Setup
-----

In order to be able to run the `revitron <cli.html>`_ command from anywhere it has to be added 
to your *path* environment variable. 
You can do that manually or by running the following commands once:

.. code-block::

    cd path\to\revitron.lib
    cli\setup

Configuration
-------------

As mentioned before, analytics jobs are configured using a *JSON* file. No coding is required at all. 
A basic configuration consits of four top fields:

============= ======================================================================================
Field         Description
============= ======================================================================================
``model``     the Revit :ref:`model path<model-path>` information
``revit``     the Revit version to be used to run the analytics
``storage``   the :ref:`storage configuration<storage-drivers>` for the extracted data snapshots
``providers`` the actual :ref:`configuartion for the data<data-providers>` the has to be tracked
============= ======================================================================================

.. note:: You can find a set of example configuration in the official `Github repository <https://github.com/revitron/revitron/tree/develop/docs/examples/analyze>`_. 
    Feel free to uses those configuration as template for your own projects.

A typical `JSON file <https://github.com/revitron/revitron/tree/develop/docs/examples/analyze>`_ that can be used to create snapshots of a model's accumulated room area looks as follows:

.. code-block:: json

    {
        "model": {
            "type": "cloud",
            "projectGUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "modelGUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "region": "EMEA"
        },
        "storage": {
            "driver": "Directus",
            "config": {
                "token": "YOUR_DIRECTUS_API_KEY",
                "host": "http://domain.com/",
                "collection": "Project Name"
            }
        },
        "revit": "2022",
        "providers": [
           {
                "name": "Room Area",
                "class": "ElementAreaProvider",
                "config": {
                    "filters": [
                        {
                            "rule": "byCategory",
                            "args": ["Rooms"]
                        },
                        {
                            "rule": "byStringContains",
                            "args": ["Name", "Room"]
                        }
                    ]
                }
            }
        ]
    }


.. _model-path:

Model Path
~~~~~~~~~~

The model path field contains information about where the source model is loaded from — *local* or *cloud*.
Local models can be loaded by just providing a local file system path as demonstrated in the snippet below. 

.. code-block:: json

    {
        "model": {
            "type": "local",
            "path": "C:\\path\\to\\model.rvt"
        }
    }

Models that are stored in the *BIM360* cloud require a bit more information, such as the *project GUID*, 
the *model GUID* and the *region*. You can use the **Cloud → Cloud Model Info** button in the *Revitron UI* 
in order to get the required GUIDs and the region information for the currently opened model. 

.. code-block:: json

    {
        "model": {
            "type": "cloud",
            "projectGUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "modelGUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "region": "EMEA"
        }
    }

.. _storage-drivers:

Storage Drivers
~~~~~~~~~~~~~~~

The storage driver can be configured using the ``storage`` field. 
It field takes a single configuration object that provides the required data for *Revitron* to write or connect.
There are currently multiple options for storing the actual analytics snapshots — *SQLite*, *JSON* and *Directus*

JSON
""""

In order to quickly get up and running and for testing the analytics configuration, the
extracted snapshot data can be dumped into a *JSON* file.

.. code-block:: json 

    {
        "storage": {
            "driver": "JSON",
            "config": {
                "file": "C:\\path\\to\\snapshots.json"
            }
        }
    }

SQLite
""""""

Alternatively to *JSON* files it is also possible to use *SQLite* databases as 
local storage.

.. code-block:: json 

    {
        "storage": {
            "driver": "SQLite",
            "config": {
                "file": "C:\\path\\to\\snapshots.sqlite"
            }
        }
    }

.. _directus-storage:

Directus
""""""""

The **recommended** but by far more complex solution is to send the snapshots data to 
a `Directus <https://directus.io/>`_ instance. Directus is data platform that can be used 
in `the cloud <https://docs.directus.io/cloud/overview/>`_ or `self-hosted <https://docs.directus.io/self-hosted/quickstart/>`_, installed on a local server. The cloud version even provides
a `free plan <https://directus.io/pricing/>`_. After creating your Directus instance, you will have to create an *API key* in order to 
give **Revitron** write access.

.. note:: Using Directus for snapshots storage also enables you to make use of automatically :ref:`generated analytics dashboards<viz>`.

.. code-block:: json 

    {
        "storage": {
            "driver": "Directus",
            "config": {
                "token": "YOUR_DIRECTUS_API_KEY",
                "host": "http://domain.com/url/to/directus",
                "collection": "Project Name"
            }
        }
    }

.. note:: Storing the token in plain text in your configuration might not be the best solution. Alternatively it is therefore possible to reference any environment variable instead: 

.. code-block:: json
    :emphasize-lines: 5

    {
        "storage": {
            "driver": "Directus",
            "config": {
                "token": "{{ ENV_VARIABLE }}",
                "host": "http://domain.com/url/to/directus",
                "collection": "Project Name"
            }
        }
    }

.. _data-providers:

Data Providers
~~~~~~~~~~~~~~

So far we have configured where the data is taken from and where the snapshots are stored. 
Now we can define what kind of analytics we want to extract from the model. The data extraction 
is handled by *Data Providers* that define how and what data is aggregated and what set 
of elements is used for the calculation. Therefore a provider configuration consits of the following
fields:

.. code-block:: json
    :emphasize-lines: 5, 7

    {
        "providers": [
           {
                "name": "Room Area",
                "class": "ElementAreaProvider",
                "config": {
                    "filters": [
                        {
                            "rule": "byCategory",
                            "args": ["Rooms"]
                        },
                        {
                            "rule": "byStringContains",
                            "args": ["Name", "Room"]
                        }
                    ]
                }
            }
        ]
    }

Aside from the ``name`` field, that has to be unique, the ``class`` field and the ``config.filters`` field are important here.

Classes
"""""""

The classes field defines what provider type is used to calculate the extracted value. There are currently five 
different `types of providers <revitron.analyze.providers.html>`_ available.

Filters
"""""""

The ``filters`` field contains a list of filter objects that have two properties:

================ ===============================================================================
Name             Description 
================ ===============================================================================
``rule``         The `filter method <revitron.filter.html#revitron.filter.Filter>`_ that is used to filter a collection of elements.
``args``         A list of arguments that is passed to the filter method. Take a look at the documentation for these methods in order get all available parameters.
================ ===============================================================================

.. code-block:: json
    :emphasize-lines: 3, 4

    "filters": [
        {
            "rule": "byCategory",
            "args": ["Rooms"]
        },
        {
            "rule": "byStringContains",
            "args": ["Name", "Room"]
        }
    ]

Automation
----------

Since we want the snapshots to be taken periodically, like on a daily basis, 
we can configure the *Windows Task Scheduler*
to run the ``revitron`` command, or a ``.bat`` file containing multiple calls.

.. code-block::

    revitron analyze "C:\\path\\to\\config.json"

.. _viz:

Visualization
-------------

Analytics snapshots that are stored in :ref:`Directus<directus-storage>` can automatically visualized in 
a web based dashboard using `Revitron Charts <https://github.com/revitron/revitron-charts>`_.

.. container:: .image-mockup

    .. image:: https://github.com/revitron/revitron-charts/raw/master/images/dashboard.png

The charts app can easily be deployed on a local webserver using Docker. A working Dockerfile is included
in the repository. An installation guide can be found `here <https://github.com/revitron/revitron-charts#readme>`_.
After a successfull deployment, there is no further setup needed. All analytically tracked projects are 
automatically added to the dashboard.

.. container:: .buttons-small

   `More about charts   ⟶ <https://github.com/revitron/revitron-charts>`_
   

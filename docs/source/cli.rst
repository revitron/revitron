Command Line
============

Revitron ships its own little wrapper for the *pyRevit* CLI that includes some additional features such as the
ability to handle cloud models and to pass configuration files. 

.. code-block::

    revitron [command] "path\to\config.json"

Setup
-----

In order to be able to run the ``revitron`` command from anywhere it has to be added 
to your *path* environment variable. 
You can do that manually or by running the following commands once:

.. code-block::

    cd path\to\revitron.lib
    cli\setup

Standard Commands
-----------------

Revitron ships with two default commands.

=============== =====================================================================================
Command         Description
=============== =====================================================================================
``analyze``     Creates analytical snapshots from models. More `here <analyze.html>`_.
``compact``     Compacts a model. The configuration JSON file only has to include `model` and `revit`
                fields.
=============== =====================================================================================

Compact Example 
~~~~~~~~~~~~~~~

The configuration for the ``compact`` command operating on cloud models looks as follows:

.. code-block:: json

    {
        "model": {
            "type": "cloud",
            "projectGUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "modelGUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "region": "EMEA"
        },
        "revit": "2022"
    }

Alternatively local models have a slightly different configuration:

.. code-block:: json

    {
        "model": {
            "type": "local",
            "path": "C:\\path\\to\\model.rvt"
        },
        "revit": "2022"
    }

The compacting can be started with the following command. Manually or as a command used in a task scheduler.

.. code-block::

    revitron compact "path\to\config.json"

Custom Commands
---------------

Revitron supports custom commands as well to be used with the CLI. In order to be used as a command, 
a command has to meet the following requirements for its location and its content.

Location
~~~~~~~~

In order to be picked up as a valid command, a custom command file must have the ``.cli.py`` extension
and be located somewhere subdirectory tree of the main extension directory of pyRevit. It is strongly recommended
to ship commands as Revitron packages that will be installed automatically in the correct location by the Revitron
package manager.

Anatomy
~~~~~~~

You can use one of the following example commands below in order to quickly get a custom command up and running:

.. code-block:: python

    import revitron
    from cli import App, Config, getLogFromEnv

    # Get the config dictionary from the JSON file.
    config = Config().get()

    # Get a log handle to use for logging.
    log = getLogFromEnv().write
    log('Hello')

    # Open the model that is configured in the JSON file.
    # Use App.open(True) in order to open and detach the file.
    revitron.DOC = App.open(True)

    # Implement your functionality here.
    # Use the config dict in order to access your configuration stored 
    # in the JSON file that is passed as CLI argument.

    revitron.DOC.Close(False)

In order to sync changes that have been applied by your command, you can use the following boiler plate
that includes synching as well.

.. code-block:: python

    import revitron
    from cli import App, Config, getLogFromEnv

    config = Config().get()
    log = getLogFromEnv().write
    revitron.DOC = App.open(False)

    # Implement your functionality here before synching ...

    if revitron.Document().synchronize(compact=True, comment='Some comment'):
        log('Synching finished successfully')
    else:
        log('Synching failed')

    revitron.DOC.Close(False)

You can take a look at the included `commands <https://github.com/revitron/revitron/tree/develop/cli/commands>`_ as simple but fully working examples for command files.
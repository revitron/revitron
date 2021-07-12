Getting Started
===============

Revitron is a `Revit API <https://www.revitapidocs.com/>`_ wrapper written in Python that can help you 
to develop clean and powerful `pyRevit <https://www.notion.so/pyRevit-bd907d6292ed4ce997c46e84b6ef67a0>`_ extensions. 
Check out the `developer guide <revitron.html>`_ for more information or 
use the `cheat sheet <cheat-sheet.html>`_ to get started quickly.

Installation
------------

There are three options for installing **Revitron** and the `Revitron UI <https://revitron-ui.readthedocs.io/>`_ --- 
using the `pyRevit UI <#using-the-pyrevit-ui>`_, using the `pyRevit CLI <#using-the-pyrevit-cli>`_ or 
installing the `full bundle <#bundled-version>`_.

.. important:: Note that in order to use the Revitron package manager or the bundle installer, 
    `Git <https://git-scm.com/>`_ must be installed on your computer.

Using the pyRevit UI
~~~~~~~~~~~~~~~~~~~~

To use the Revit UI to install this extensions, open the *pyRevit* tab, 
click on *pyRevit* > *Extensions* to open the extensions manager and 
follow `these <https://www.notion.so/Install-Extensions-0753ab78c0ce46149f962acc50892491>`_ instructions.

Using the pyRevit CLI
~~~~~~~~~~~~~~~~~~~~~

In case you want to use the command line to install **Revitron** and 
the `Revitron UI <https://revitron-ui.readthedocs.io/>`_, use the following command::

    pyrevit extend lib revitron https://github.com/revitron/revitron.git
    pyrevit extend ui revitron https://github.com/revitron/revitron-ui.git


Bundled Version
~~~~~~~~~~~~~~~

There is also a bundle installer available that will install *pyRevit* 
including the *Revitron* and the *Revitron UI* packages.

1. Right-click `here <https://raw.githubusercontent.com/revitron/installer/master/install.bat>`_ 
   to download the **Revitron** installer. Make sure it keeps the ``.bat`` extension.
2. Move the ``install.bat`` to the directory, where you want to install **pyRevit**.
3. Double-click the ``install.bat`` file to start the installation and wait until it has finished.
4. Start **Revit**.


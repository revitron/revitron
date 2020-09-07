Install
=======

The Revitron library can be installed as a single Python package for pyRevit or bundled with a custom 
fork of pyRevit including the package manager `RPM <https://github.com/revitron/rpm>`_ and 
the `Revitron UI <https://revitron-ui.readthedocs.io/en/latest/>`_. In case you want to setup a new Revit project and you are new to pyRevit, 
it is recommendend to install the bundled version as described below.

Installing Only the Library
---------------------------

The single library package can be installed using the pyRevit CLI as follows::

    pyrevit extend lib revitron https://github.com/revitron/revitron.git

Alternatively the package can also just be cloned as follows::

    cd C:[\path\to\pyrevit]\extensions
    git clone https://github.com/revitron/revitron.git revitron.lib

Installing the Full Bundle
--------------------------

To install the full bundle including pyRevit, RPM and the Revitron UI, follow the instructions below:

1. Right-click `here <https://raw.githubusercontent.com/revitron/installer/master/install.bat>`_ to download the installer.
2. Move the `install.bat` to the directory, where you want to install pyRevit.
3. Double-click the installer.
4. Start Revit and close it again.
5. Start Revit a second time.
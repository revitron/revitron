Install
=======

The Revitron library can be installed as a single Python package for pyRevit or bundled with a custom 
`fork <https://github.com/revitron/pyRevit>`_ of pyRevit including the project based package manager 
`RPM <https://github.com/revitron/rpm-ui/blob/master/README.md>`_ and the `Revitron UI <https://revitron-ui.readthedocs.io/>`_. 
In case you want to setup a new Revit project and you are new to pyRevit, 
it is recommendend to install the bundled version as described below.

.. important:: The bundle installer as well as the Revitron package manager are using `Git <https://git-scm.com/>`_ to manage dependencies.
   Please make sure that Git is installed properly on your system before installing Revitron.

Bundle Installer 
----------------

To install the full bundle including pyRevit, RPM and the Revitron UI, follow the instructions below:

1. Right-click `here <https://raw.githubusercontent.com/revitron/installer/master/install.bat>`_ to download the installer.
2. Move the ``install.bat`` to the directory, where you want to install pyRevit.
3. Double-click the ``install.bat`` file.
4. Start Revit after the installer script has finished and close it again.
5. Start Revit a second time.

Manual Installation
-------------------

The single library and UI packages can be installed using the pyRevit CLI as follows::

    pyrevit extend lib revitron https://github.com/revitron/revitron.git
    pyrevit extend ui revitron https://github.com/revitron/revitron-ui.git

Alternatively the package can also just be cloned with Git as follows::

    cd C:[\path\to\pyrevit]\extensions
    git clone https://github.com/revitron/revitron.git revitron.lib
    git clone https://github.com/revitron/revitron-ui.git revitron-ui.extension
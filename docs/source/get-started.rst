Getting Started
===============

The Revitron library can be installed as a single Python package for **pyRevit** or bundled with a custom 
`fork <https://github.com/revitron/pyRevit>`_ of pyRevit including the project based package manager 
`RPM <https://github.com/revitron/rpm-ui/blob/master/README.md>`_ and the `Revitron UI <https://revitron-ui.readthedocs.io/>`_. 
In case you want to setup a new **Revit** project and you are new to pyRevit, 
it is recommendend to install the bundled version as described below.

.. attention:: The bundle installer as well as the Revitron package manager are using **Git** to manage dependencies.
   Please make sure that `Git <https://git-scm.com/>`_ is installed properly on your system before installing Revitron.

Bundle Installer 
----------------

To install the full bundle including **pyRevit**, **RPM** and the **Revitron UI**, follow the instructions below:

1. In case **Git** is not already installed --- `download <https://git-scm.com/download/win>`_ and install Git.
2. Right-click `here <https://raw.githubusercontent.com/revitron/installer/master/install.bat>`_ to download the **Revitron** installer. 
   Make sure it keeps the ``.bat`` extension.
3. Move the ``install.bat`` to the directory, where you want to install **pyRevit**.
4. Double-click the ``install.bat`` file to start the installation and wait until the **CMD** window closes.
5. Start **Revit** and choose to always load the extension.
6. Close and start **Revit** a second time to finish the installation.

Manual Installation
-------------------

The single library and UI packages can be installed using the **pyRevit CLI** as follows::

    pyrevit extend lib revitron https://github.com/revitron/revitron.git
    pyrevit extend ui revitron https://github.com/revitron/revitron-ui.git

Alternatively the package can also just be cloned with **Git** as follows::

    cd C:[\path\to\pyrevit]\extensions
    git clone https://github.com/revitron/revitron.git revitron.lib
    git clone https://github.com/revitron/revitron-ui.git revitron-ui.extension
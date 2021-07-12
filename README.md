![](https://raw.githubusercontent.com/revitron/revitron/master/svg/revitron-readme.svg)

# Revitron

Revitron is a [Revit API](https://www.revitapidocs.com/) wrapper written in Python. It helps you to develop clean and powerful Revit plugins for [pyRevit](https://github.com/eirannejad/pyRevit). 

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/revitron/revitron?label=version&color=222222)
![GitHub](https://img.shields.io/github/license/revitron/revitron?color=222222)
![GitHub top language](https://img.shields.io/github/languages/top/revitron/revitron?color=222222)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/revitron/revitron?color=222222)
![Read the Docs](https://img.shields.io/readthedocs/revitron?color=222222)
![](https://img.shields.io/badge/Revit-2017--2022-222222)

- [Installation](#installation)
	- [Using the pyRevit UI](#using-the-pyrevit-ui)
	- [Using the pyRevit CLI](#using-the-pyrevit-cli)
	- [Bundled Version](#bundled-version)
- [Documentation](#documentation)

## Installation

There are three options for installing Revitron and the [Revitron UI](https://revitron-ui.readthedocs.io/) &mdash; using the [pyRevit UI](#using-the-pyrevit-ui), using the [pyRevit CLI](#using-the-pyrevit-cli) or installing the [full bundle](#bundled-version).

> ☝ Note that in order to use the Revitron package manager or the bundle installer, [Git](https://git-scm.com/) must be installed on your computer.

### Using the pyRevit UI

To use the *Revit UI* to install this extensions, open the *pyRevit* tab, click on *pyRevit > Extensions* to open the extensions manager and follow [these](https://www.notion.so/Install-Extensions-0753ab78c0ce46149f962acc50892491) instructions.

### Using the pyRevit CLI

In case you want to use the command line to install *Revitron* and the *Revitron UI*, use the following command:

	pyrevit extend lib revitron https://github.com/revitron/revitron.git
	pyrevit extend ui revitron https://github.com/revitron/revitron-ui.git

### Bundled Version

There is also a bundle installer available that will install *pyRevit* including the *Revitron* and the *Revitron UI* packages.

1. Right-click [here](https://raw.githubusercontent.com/revitron/installer/master/install.bat) to download the installer. Make sure it keeps the `.bat` extension.
2. Move the `install.bat` to the directory, where you want to install *pyRevit*.
3. Double-click the `install.bat` file.
4. Start *Revit*.

## Documentation

The full documentation and API reference as well as some cheat sheets can be found [here](https://revitron.readthedocs.io/).

---

&copy; 2020-2021 [Marc Anton Dahmen](https://marcdahmen.de) &mdash; MIT license
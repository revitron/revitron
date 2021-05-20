![](https://raw.githubusercontent.com/revitron/revitron/master/svg/revitron-readme.svg)

# Revitron

Revitron is a [Revit API](https://www.revitapidocs.com/) wrapper written in Python. It helps you to develop clean and powerful Revit plugins for [pyRevit](https://github.com/eirannejad/pyRevit). 

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/revitron/revitron?label=version)
![GitHub](https://img.shields.io/github/license/revitron/revitron?color=222222)
![GitHub top language](https://img.shields.io/github/languages/top/revitron/revitron?color=222222)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/revitron/revitron?color=222222)
![Read the Docs](https://img.shields.io/readthedocs/revitron?color=222222)
![](https://img.shields.io/badge/Revit-2017--2021-222222)

## Docs

An installation guide, the API reference and the UI docs can be found [here](https://revitron.readthedocs.io).     

## Unit Tests

> :point_up: Note that this extension is only tested on Revit `2017`, `2019.1`, `2020.2` and `2021.1`, but may as well work on other versions.

Revitron unit tests need their own pyRevit UI to run. Since they are only needed to develop the library extension and would only bother normal users, all unit tests are located in a [separate repository](https://github.com/revitron/revitron-tests) and can be installed as an independent UI extension if required.

&copy; 2020-2021 [Marc Anton Dahmen](https://marcdahmen.de) &mdash; MIT license
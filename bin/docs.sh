#!/bin/sh

dir=`dirname $0`
cd "$dir/../docs"

sphinx-apidoc --separate --ext-autodoc --ext-viewcode --templatedir source/_templates/ -TMf -o source/ ../revitron

make html
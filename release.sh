#!/bin/sh

read -p "Tag: " tag 

sed -i "s|REVITRON_VERSION.*|REVITRON_VERSION = '$tag'|g" "./revitron/__init__.py"
sed -i "s|Version.*|Version $tag|g" "./docs/source/index.rst"
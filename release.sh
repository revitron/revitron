#!/bin/sh

read -p "Tag: " tag 

sed -i "s|REVITRON_VERSION.*|REVITRON_VERSION = '$tag'|g" "./revitron/__init__.py"
sed -i "s|Version.*|Version $tag|g" "./docs/source/index.rst"

git add -A && git commit -m "Prepared release $tag"
git checkout master
git merge develop --no-ff -m "Merged branch develop (release $tag)"
git tag -a -m "Release $tag" $tag
git checkout develop
git log -n 2 --graph --all
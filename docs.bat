set cwd=%~dp0
cd %cwd%
cd docs
sphinx-apidoc --private --ext-viewcode --ext-githubpages -e -T -M --implicit-namespaces -f -o source/ ../revitron
call make html
cd %cwd%
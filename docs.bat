set cwd=%~dp0
cd %cwd%
cd docs
sphinx-apidoc --separate --ext-autodoc --ext-viewcode --templatedir source/_templates/ -Tf -o source/ ../revitron
call make html
cd %cwd%
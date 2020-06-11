set cwd=%~dp0
cd %cwd%
cd docs
sphinx-apidoc --ext-viewcode --templatedir source/_templates/ -TMf -o source/ ../revitron
call make html
cd %cwd%
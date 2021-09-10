@echo off

set cliPath=%~dp0
set newPath=%PATH%;%cliPath%
set newPath=%newPath:;;=;%

echo %newPath% > temp.txt
for %%? in (temp.txt) do ( set /A pathLength=%%~z? - 2 )
del temp.txt

if %pathLength% leq 1020 setx path "%newPath%"

exit
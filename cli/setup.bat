@echo off

set key="HKCU\Environment"
for /F "usebackq tokens=2*" %%A in (`REG QUERY %key% /v PATH`) do set userPath=%%B

set cliPath=%~dp0
set newPath=%userPath%;%cliPath%;
set newPath=%newPath:;;=;%

echo %newPath% > temp.txt
for %%? in (temp.txt) do ( set /A pathLength=%%~z? - 2 )
del temp.txt

if %pathLength% leq 1022 (
	setx path "%newPath%"
) else (
	echo Path is too long!
)

pause
exit
@echo off

if not exist "%~dp0\target.rvt" (
	Powershell -executionpolicy remotesigned -File %~dp0\target.ps1
)

set run=%~dp0\run.py
set command=%~dp0\commands\%1.py
set args=%*

if "%~1" == "" (
	echo No command specified!
) else (
	if exist %command% (
		python %run% %args%
	) else (
		echo Command "%1" not found!
	)
)
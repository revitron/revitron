@echo off

set command=%~dp0\commands\%1.py
set args=%*

if "%~1" == "" (
	echo No command specified!
) else (
	if exist %command% (
		python %command% %args%
	) else (
		echo Command "%1" not found!
	)
)
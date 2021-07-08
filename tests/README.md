# Revitron Unit Tests

Use the following command in a Bash shell such as Git-Bash to run all unit tests at once in Revit 2022:

	bash bin/tests.sh

Currently, the `pyrevit run` command requires a target file. The file itself is not used for the tests and is just required to actually make the pyRevit CLI work. Therefore it is required to place a Revit file with a version lower or equal to the test environment and the name `tests.rvt` in the `tests/temp` directory.

## Options

The following options are available to change the selection of tests as well as the Revit version in use:

	-r	The Revit version such as 2019 or 2020
	-g	The glob pattern for selecting the test modules

## Example

In order to run all filter tests in Revit 2019 you can use:

	bash bin/tests.sh -r 2019 -g test_filter*
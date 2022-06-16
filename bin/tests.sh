#!/bin/sh

revitVersion=2022
glob="test_*.py"

cd "`dirname $0`/.."
revitronDir=`pwd`
testsPy="$revitronDir/tests/run.py"
testsTemp="$revitronDir/tests/temp"
testsRvt="$testsTemp/target.rvt"
testsLog="$testsTemp/tests.log"
testsConfig="$testsTemp/config.json"
targetFile="https://github.com/revitron/cli-target/raw/master/cli-target-2019.rvt"

mkdir -p $testsTemp

if [ ! -f "$testsRvt" ]; then
	Powershell -executionpolicy remotesigned wget "$targetFile" -Outfile "$testsRvt"	
fi

while getopts 'g:r:' opt; do
	case $opt in
		g)
			glob=$OPTARG
			;;
		r)
			revitVersion=$OPTARG
			;;
		\?)
			echo "$opt is not a valid option"
			exit 0
	esac
done

echo "{ \"glob\": \"$glob\" }" > $testsConfig

cd "$revitronDir/../.."

bin/pyrevit run $testsPy $testsRvt --revit=$revitVersion --purge

clear 

echo
echo "Revitron Unit Tests"
echo "======================================================================"
echo "Test pattern:   $glob"
echo "Revit version:  $revitVersion"
echo "----------------------------------------------------------------------"
echo

cat $testsLog

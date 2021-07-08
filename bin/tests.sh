#!/bin/sh

revitVersion=2022
glob="test_*.py"

cd "`dirname $0`/.."
revitronDir=`pwd`
testsPy="$revitronDir/tests/run.py"
testsTemp="$revitronDir/tests/temp"
testsRvt="$testsTemp/tests.rvt"
testsLog="$testsTemp/tests.log"
testsConfig="$testsTemp/config.json"

mkdir -p $testsTemp

cd "$revitronDir/../.."
pyrevitDir=`pwd`

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

bin/pyrevit run $testsPy $testsRvt --revit=$revitVersion --purge

echo
echo "Unit Tests"
echo "=========="
echo

cat $testsLog

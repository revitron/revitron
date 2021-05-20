#!/bin/sh

# Check if working directory is clean.
if [[ $(git status -s) ]]
then
	echo "Working directory is not clean!"
	git status -s
	echo
fi

# Get latest tag.
latestTag=$(git describe --tags $(git rev-list --tags --max-count=1))

# Choose type of release.
echo "Current version is: $latestTag"
echo 

IFS='.' read -ra elem <<< "$latestTag"

major=${elem[0]}
minor=${elem[1]}
patch=${elem[2]}

newMajorTag=$((major + 1)).0.0
newMinorTag=$major.$((minor + 1)).0
newPatchTag=$major.$minor.$((patch + 1))

echo "Choose type of release:"
echo
echo "  1) Patch $newPatchTag (default)"
echo "  2) Minor $newMinorTag"
echo "  3) Major $newMajorTag"
echo
read -n 1 -p "Please select a number or press Enter for a patch: " option
echo

case $option in 
	1) tag=$newPatchTag;;
	2) tag=$newMinorTag;;
	3) tag=$newMajorTag;;
	*) tag=$newPatchTag;;
esac

# Wait for confirmation.
while true
do
	read -p "Create release \"$tag\"? (y/n) " continue
	case $continue in
		[Yy]* ) 
			break
			;;
		[Nn]* ) 
			exit 0
			;;
		* ) 
			echo "Please only enter \"y\" or \"n\"."
			;;
	esac
done
echo

# Updating version numbers.
sed -i "s|REVITRON_VERSION.*|REVITRON_VERSION = '$tag'|g" "./revitron/__init__.py"

# Commit, merge and tag.
git add -A && git commit -m "build(release): prepared release $tag"
git checkout master
git merge develop --no-ff -m "build(release): merged branch develop (release $tag)"
git tag -a -m "Release $tag" $tag
git checkout develop
git log -n 2 --graph --all
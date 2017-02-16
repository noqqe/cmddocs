#!/usr/bin/env bash
set -e

# conf
VERFILE=setup.py

if [[ $1 != "major" ]] && [[ $1 != "minor" ]] && [[ $1 != "patch" ]]; then
  echo wrong usage. use major/minor/patch as first argument
  exit 1
fi

function get_cur_vers {
  grep '^version = "' $VERFILE | awk -F\" '{print $2}'
}

echo bump version
bumpversion --current-version $(get_cur_vers) $1 $VERFILE

v=$(get_cur_vers)

echo adding local file
git add $VERFILE

echo commit
git commit -m "Release: $v"

echo tagging..
git tag v${v}

echo creating history.rst
gitchangelog > HISTORY.rst
git add HISTORY.rst

echo committing history
git commit -m "Changelog: $v"

echo pushing..
git push --tags origin master

echo release on pypi
python setup.py sdist upload -r pypi


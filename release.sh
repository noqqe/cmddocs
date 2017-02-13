#!/usr/bin/env bash
set -e

if [[ $1 != "major" ]] && [[ $1 != "minor" ]] && [[ $1 != "patch" ]]; then
  echo wrong usage. use major/minor/patch as first argument
  exit 1
fi

echo bump version
bumpversion --current-version $(cat VERSION) $1 VERSION

v=$(cat VERSION)

echo adding local file
git add VERSION

echo commit
git commit -m "Release: $v"

echo tagging..
git tag ${v}

echo creating history.rst
gitchangelog > HISTORY.rst
git add HISTORY.rst

echo committing history
git commit -m "Changelog: $v"

echo pushing..
git push --tags origin master

echo release on pypi
python setup.py sdist upload -r pypi


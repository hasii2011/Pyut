#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

rm -rf dist build
rm -rf Pyut.dist Pyut.build

find . -type d -name '*'.egg-info -delete
find . -type f -name pyutHistory"*" -delete
find . -type f -name "*.log"        -delete
find . -type f -name UnitTest.gml   -delete

rm -rf src/UNKNOWN.egg-info

cd src/tests/resources/testdata > /dev/null 2>&1

find . -type f -name "*.png" -delete

cd - > /dev/null 2>&1
find . -type f -name "translationGraph.gml" -delete

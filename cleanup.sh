#!/bin/bash

find . -type f -name pyutHistory"*" -delete
find . -type f -name "*.log" -delete

cd src/tests/testdata > /dev/null 2>&1

find . -type f -name "*.png" -delete

cd - > /dev/null 2>&1

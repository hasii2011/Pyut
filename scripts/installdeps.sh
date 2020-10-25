#!/usr/local/bin/bash

#
# Assumes python 3 is on PATH
# Assumes you are in a virtual environment
#

clear
pip3 list > /dev/null 2>&1
STATUS=$?

if [[ ${STATUS} -eq 0 ]] ; then
    echo "in virtual environment"
    pip3 install --upgrade pip
    pip3 install wheel
    pip3 install setuptools
    pip3 install wxPython
    pip3 install xmlschema
    pip3 install pygmlparser
    pip3 install pyumldiagrams
    pip3 install orthogonal
    pip3 install html-testRunner
    pip3 install py2app
    pip3 install antlr4-python3-runtime
    pip3 install py2app
    pip3 install networkx
    pip3 install fpdf2
else
    echo "You are not in a virtual environment"

fi

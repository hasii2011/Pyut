#!/usr/bin/env bash

#
#  assumes xcode is installed
#  assumes I added an entry APP_PASSWORD to my keychain
#
clear

xcrun notarytool history -p "APP_PASSWORD"

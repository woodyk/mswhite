#!/usr/bin/env bash
#
# File: update.sh
# Author: Wadih Khairallah
# Description: 
# Created: 2025-04-29 20:41:35

zip=`ls -t ./Archive | head -1`

unzip -o ${zip}
git add .
git commit -m "${zip}"
git push

#!/usr/bin/env bash
#
# File: update.sh
# Author: Wadih Khairallah
# Description: 
# Created: 2025-04-29 20:41:35
# Modified: 2025-04-29 20:46:17

zip=`ls -t ./Archive | head -1`

unzip -o ./Archive/${zip}
git add .
git commit -m "${zip}"
git push

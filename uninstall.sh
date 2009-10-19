#!/bin/sh
## Installation Script for gtweetbar
 
# ======================================================================
# Copyright (C) 2009 Abhishek Mishra <ideamonk@gmail.com>
# Time-stamp: Sun Oct 04 12:11:57 IST 2009
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

# i don't know no packaging yet

echo 'GTweetBar 1.0 Uninstaller'
echo ' *** you must be a super user to be able to remove *** '
echo ' '

echo "Removing gTweetBar..."

rm  /usr/local/bin/gtweetbar.py
rm -Rf /usr/share/gtweetbar
rm /usr/lib/bonobo/servers/gtweetbar.server

echo "Done!"

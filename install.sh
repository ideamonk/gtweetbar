#!/bin/sh
## Installation Script for gtweetbar
 
# ======================================================================
# Copyright (C) 2009 Abhishek Mishra <ideamonk@gmail.com>
# Time-stamp: Sun Oct 04 12:11:57 IST 2009
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

echo 'GTweetBar 1.0 Installer'
echo ' *** you must be a super user to be able to install *** '
echo ' '

echo 'installing simplejson...'
apt-get install python-setuptools
easy_install simplejson

echo 'Creating /usr/share/gtweetbar'
mkdir -p /usr/share/gtweetbar

echo 'Copying needed resource files'
cp -R ./python_twitter /usr/share/gtweetbar/
cp -R ./ui /usr/share/gtweetbar/
cp README /usr/share/gtweetbar/

echo 'Copying main script into /usr/local/bin'
cp gtweetbar.py /usr/local/bin/

echo 'Setting up permissions'
chmod u+x /usr/local/bin/gtweetbar.py
chmod g+x /usr/local/bin/gtweetbar.py
chmod a+x /usr/local/bin/gtweetbar.py
cp gtweetbar.server /usr/lib/bonobo/servers/

echo "Done!"
echo "Do a right click on desired panel, and add Gnome TweetBar to it"


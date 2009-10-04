#!/bin/sh

mkdir -p /usr/share/gtweetbar
cp -R ./python_twitter /usr/share/gtweetbar/
cp README /usr/share/gtweetbar/

cp tweetbar.py /usr/local/bin/
chmod u+x /usr/local/bin/tweetbar.py
chmod g+x /usr/local/bin/tweetbar.py
chmod a+x /usr/local/bin/tweetbar.py
cp tweetbar.server /usr/lib/bonobo/servers/

echo "Done!"


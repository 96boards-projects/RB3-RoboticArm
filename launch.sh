#!/bin/bash

memcached &;

xterm python3 shape.py &

if [ $1 == "gui" ]; then
    echo "Launching in gui mode."
    xterm python3 main-gui.py &
elif [ $1 == "voice" ]; then
    echo "Launching in voice mode."
    xterm python3 main-voice.py &
else
    echo "Usage: sudo bash launch.sh <gui or voice>"
fi
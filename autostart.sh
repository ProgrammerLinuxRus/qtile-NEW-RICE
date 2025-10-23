#!/bin/bash
xrandr --newmode "1920x1080_100.00"  302.50  1920 2072 2280 2640  1080 1083 1088 1147 -hsync +vsync 
xrandr --addmode HDMI-A-0 1920x1080_100.00 
xrandr --output HDMI-A-0 --mode 1920x1080_100.00 
picom &
nitrogen --restore &

#conky &

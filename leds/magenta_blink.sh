#!/bin/sh
#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# Simple magenta blink for RGB LED in limited loop
# Allwinner SoC led controller driver has to be loaded
#

LED_CONTROLLER=/sys/devices/platform/soc/2008000.led-controller

if [ ! -d "$LED_CONTROLLER" ]; then
    exit 1
fi

LED_STATUS=$LED_CONTROLLER/leds/rgb:status

R_VAL=255
G_VAL=0
B_VAL=255

# Be gentle, limit brightness
echo 150 > $LED_STATUS/brightness

for k in 1 2 3
do
   echo $R_VAL $G_VAL $B_VAL > $LED_STATUS/multi_intensity
   sleep 0.5
   echo 0 0 0 > $LED_STATUS/multi_intensity
   sleep 0.5
done

echo 0 > $LED_STATUS/brightness


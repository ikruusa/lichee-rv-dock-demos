#!/bin/sh
#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# Sipeed's Lichee RV module itself is having an user LED, connected to the port PC1
# This LED is defined in device tree as gpio led device
# This script is constantly switching this LED on and off
#

LED_BRIGHTNESS=/sys/class/leds/green:status/brightness

# Be nice and switch lights off when exiting
function ctrl_c(){
        echo ""
        echo "Setting green LED off"
        echo 0 > $LED_BRIGHTNESS
        echo "Bye"
        exit 0
}

# Catch the CTRL+C
trap ctrl_c INT

echo "One small green LED is located on the Lichee RV module itself."
echo "Switching it on and off"
echo "Press CTRL+C to quit..."

while true; do
        echo 1 > $LED_BRIGHTNESS
        sleep 0.5
        echo 0 > $LED_BRIGHTNESS
        sleep 0.5
done

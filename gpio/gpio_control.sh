#!/bin/sh
#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# This script is constantly changing GPIO pin value on and off
# Make sure the pinctrl driver is loaded and kernel is built
# with libgpiod
# Tested on Sipeed's Lichee RV module
#

#
# How to map pin names like PG14 to pinctrl's line numbers (run gpioinfo)
# Original source: https://linux-sunxi.org/GPIO
# To calculate the correct number you have to calculate it from the pin name (like PG14):
# (position of the letter in alphabet - 1) * 32 + pin number
# E.g for PG14 this would be ( 7 - 1) * 32 + 14 = 192 + 14 = 206 (since 'g' is the 7th letter)
#

PIN_NAME=PG14
# One day the number of the pin will be calculated automatically from PIN_NAME
# Set it manually now
PIN_NO=206

# Set pin to low when exiting (assumed that low is inactive state)
function ctrl_c(){
        echo ""
        echo "Setting GPIO pin" $PIN_NAME "off"
        gpioset gpiochip0 $PIN_NO=0
        echo "Bye"
        exit 0
}

# Catch the CTRL+C
trap ctrl_c INT

echo "Switching GPIO pin" $PIN_NAME "on and off"
echo "Press CTRL+C to quit..."

while true; do
        gpioset gpiochip0 $PIN_NO=1
        sleep 0.5
        gpioset gpiochip0 $PIN_NO=0
        sleep 0.5
done


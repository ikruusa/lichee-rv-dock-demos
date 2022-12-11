#!/bin/sh
#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# Torch - press the KEY button and RGB LED will lit @ max. brightness
# Allwinner SoC led controller driver has to be loaded
#

trap ctrl_c INT

LED_CONTROLLER=/sys/devices/platform/soc/2008000.led-controller

if [ ! -d "$LED_CONTROLLER" ]; then
    echo "Allwinner SOC LED driver LEDS_SUN50I_A100 is not activated!"
    echo "Terminating..."
    exit 1
else
    echo "Found the Allwinner SOC LED controller, modalias:"
    cat $LED_CONTROLLER/modalias
fi

LED_STATUS=$LED_CONTROLLER/leds/rgb:status

# Be nice and switch lights off when exiting
function ctrl_c(){
    echo 0 0 0 > $LED_STATUS/multi_intensity
    echo 0 > $LED_STATUS/brightness
    echo
    echo "Bye"
    exit 0
}

# Define matching string for the event line
pressed='*code 352 (KEY_OK), value 1'
released='*code 352 (KEY_OK), value 0'

# Set even intensity to get white light
echo 255 255 255 > $LED_STATUS/multi_intensity
echo "Press the white button on Lichee RV dock labeled KEY (and not RESET!!)"
echo "Press CTRL+C to quit..."

evtest /dev/input/event0 | while read line; do
    case $line in
        ($pressed) echo 255 > $LED_STATUS/brightness ;;
        ($released) echo 0 > $LED_STATUS/brightness ;;
    esac
done

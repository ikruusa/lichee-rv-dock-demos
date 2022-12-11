#!/bin/sh
#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# This script is changing RGB LED's colors on Lichee RV dock 
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
    echo "Switching LED off"
    echo "Bye"
    exit 0
}

R_VAL=50
R_INC=1
R_DIR=-1
G_VAL=200
G_INC=1
G_DIR=-1
B_VAL=120
B_INC=1

SLP=6500
RANDOM=$$

# Be gentle, limit brightness
echo 120 > $LED_STATUS/brightness
echo "Limiting brightness a bit"
echo "Will change the RGB LED colors"
echo "Press CTRL+C to quit..."

while true; do
    echo $R_VAL $G_VAL $B_VAL > $LED_STATUS/multi_intensity
    # Randomize red's and green's increment when at minimum
    if [ $R_VAL -lt 10 ]; then
        R_DIR=$((-R_DIR))
        R_INC=$((RANDOM/SLP + 1))
        R_VAL=10
    fi
    if [ $R_VAL -gt 245 ]; then
        R_DIR=$((-R_DIR))
        R_VAL=245
        sleep 1
    fi
    if [ $G_VAL -lt 10 ]; then
        G_DIR=$((-G_DIR))
        G_INC=$((RANDOM/SLP + 1))
        G_VAL=10
    fi
    if [ $G_VAL -gt 245 ]; then
        G_DIR=$((-G_DIR))
        G_VAL=245
        sleep 1
    fi
    if [ $B_VAL -eq 254 ] || [ $B_VAL -eq 0 ]; then
        B_INC=$((-B_INC))
        sleep 1
    fi
    R_VAL=$((R_VAL + R_INC * R_DIR))
    G_VAL=$((G_VAL + G_INC * G_DIR))
    B_VAL=$((B_VAL + B_INC))
    sleep 0.01
done

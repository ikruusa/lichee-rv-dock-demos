import gpiod
import time
import sys
import signal

#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# This script is constantly changing GPIO pin value on and off
# Make sure the pinctrl driver is loaded and kernel is built
# with libgpiod and libgpiod is installed (it includes the module for the python also)
# Tested on Sipeed's Lichee RV module
#

def ctrl_c_handler(signum, frame):
    print("")
    print("Bye")
    lines.set_values([0])
    print("")
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

#
# How to map pin names like PG14 to pinctrl's line numbers (run gpioinfo)
# Original source: https://linux-sunxi.org/GPIO
# To calculate the correct number you have to calculate it from the pin name (like PG14):
# (position of the letter in alphabet - 1) * 32 + pin number
# E.g for PG14 this would be ( 7 - 1) * 32 + 14 = 192 + 14 = 206 (since 'g' is the 7th letter)
#

pin_name = "PG14"
pin_no = 206

print("Switching GPIO pin " + pin_name + " on and off")
print("Press CTRL+C to quit...")

chip = gpiod.Chip('gpiochip0')
lines = chip.get_lines([pin_no])
lines.request(consumer='none', type=gpiod.LINE_REQ_DIR_OUT)

while True:
    lines.set_values([1])
    time.sleep(0.5)
    lines.set_values([0])
    time.sleep(0.5)


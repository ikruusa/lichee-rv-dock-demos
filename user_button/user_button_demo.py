import libevdev
import sys
import signal

#
# Copyright (C) 2022 Indrek Kruusa <indrek.kruusa@gmail.com>
#
# This program monitors the user button called KEY on Lichee RV dock.
#

def ctrl_c_handler(signum, frame):
    print("")
    print("Bye")
    print("")
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

fd = open('/dev/input/event0', 'rb')
d = libevdev.Device(fd)

print("Press the white button on Lichee RV dock labeled KEY (and not RESET!!)")
print("Press CTRL+C to quit...")

# Processing events in endless loop
while True:
    for e in d.events():
        if e.matches(libevdev.EV_KEY.KEY_OK):
            if e.value == 1:
                print('Key pressed')
            else:
                print('Key released')


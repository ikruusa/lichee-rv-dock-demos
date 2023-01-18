# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Modified
# Copyright (C) 2023 Indrek Kruusa <indrek.kruusa@gmail.com>
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import smbus

#
# This program controls I2C connected OLED display on Lichee RV dock
#
# Requirements:
# - SSD1306 OLED must be connected to the header pins PB0 (SCL) and PB1 (SDA)
# - in my system only /dev/i2c-0 was presented (its related to the HDMI) so
#   kernel's devictree missed the needed i2c device
# - i2c2 device has to be enabled in linux kernel devicetree (I ended up compiling new u-boot)
# - at the end i2c2 device was presented as /dev/i2c-1, hence the i2c_bus=1:
#     disp = SSD1306_128_64(i2c_bus=1)
#
# Demo displays HI! on the OLED display.
# run the demo: python3 ssd1306-demo.py

# Constants
SSD1306_I2C_ADDRESS = 0x3C
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

# Scrolling constants
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A


class SSD1306Base(object):
    def __init__(self, width, height, i2c_bus=None):
        self.width = width
        self.height = height
        self._pages = height//8
        self._buffer = [0]*(width*self._pages)
        self._i2c = smbus.SMBus(i2c_bus)

    def _initialize(self):
        raise NotImplementedError

    def command(self, c):
        control = 0x00
        self._i2c.write_byte_data(SSD1306_I2C_ADDRESS, control, c)

    def data(self, c):
        control = 0x40
        self._i2c.write_byte_data(SSD1306_I2C_ADDRESS, control, c)

    def begin(self, vccstate=SSD1306_SWITCHCAPVCC):
        """Initialize display."""
        # Save vcc state.
        self._vccstate = vccstate
        self._initialize()
        # Turn on the display.
        self.command(SSD1306_DISPLAYON)

    def say_hi(self):
        hi = [0xFF,0xFF,0x18,0x18,0x18,0xFF,0xFF,0x00,0x00,0xFF,0xFF,0x00,0x00,0xCF,0xCF]
        self._buffer = hi
        self.display()

    def display(self):
        """Write display buffer to physical display."""
        self.command(SSD1306_COLUMNADDR)
        self.command(0)              # Column start address. (0 = reset)
        self.command(self.width-1)   # Column end address.
        self.command(SSD1306_PAGEADDR)
        self.command(0)              # Page start address. (0 = reset)
        self.command(self._pages-1)  # Page end address.

        for i in range(0, len(self._buffer), 16):
                control = 0x40   # Co = 0, DC = 0
                self._i2c.write_i2c_block_data(SSD1306_I2C_ADDRESS, control, self._buffer[i:i+16])

    def clear(self):
        """Clear contents of image buffer."""
        self._buffer = [0]*(self.width*self._pages)

    def set_contrast(self, contrast):
        """Sets the contrast of the display.  Contrast should be a value between
        0 and 255."""
        if contrast < 0 or contrast > 255:
            raise ValueError('Contrast must be a value from 0 to 255 (inclusive).')
        self.command(SSD1306_SETCONTRAST)
        self.command(contrast)

    def dim(self, dim):
        """Adjusts contrast to dim the display if dim is True, otherwise sets the
        contrast to normal brightness if dim is False.
        """
        # Assume dim display.
        contrast = 0
        # Adjust contrast based on VCC if not dimming.
        if not dim:
            if self._vccstate == SSD1306_EXTERNALVCC:
                contrast = 0x9F
            else:
                contrast = 0xCF
            self.set_contrast(contrast)

class SSD1306_128_64(SSD1306Base):
    def __init__(self, i2c_bus=None):
        # Call base class constructor.
        super(SSD1306_128_64, self).__init__(128, 64, i2c_bus)

    def _initialize(self):
        # 128x64 pixel specific initialization.
        self.command(SSD1306_DISPLAYOFF)                    # 0xAE
        self.command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        self.command(0x80)                                  # the suggested ratio 0x80
        self.command(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.command(0x3F)
        self.command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.command(0x0)                                   # no offset
        self.command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.command(SSD1306_CHARGEPUMP)                    # 0x8D
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x10)
        else:
            self.command(0x14)
        self.command(SSD1306_MEMORYMODE)                    # 0x20
        self.command(0x00)                                  # 0x0 act like ks0108
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)                    # 0xDA
        self.command(0x12)
        self.command(SSD1306_SETCONTRAST)                   # 0x81
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x9F)
        else:
            self.command(0xCF)
        self.command(SSD1306_SETPRECHARGE)                  # 0xd9
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x22)
        else:
            self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.command(SSD1306_NORMALDISPLAY)                 # 0xA6


disp = SSD1306_128_64(i2c_bus=1)
disp.begin()
disp.clear()
disp.display()
disp.say_hi()

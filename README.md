# lichee-rv-dock-demos
Demos about how to use onboard resources on Lichee RV dock.

If you are in hurry: go and grab tiny image (download size is less than 30MB!) from https://github.com/ikruusa/lichee_dock_images and boot up your board. You will find those demos in `/root/demos`

To interact with or use certain resource you have to consider:
* how the circuit is wired up
* what linux kernel drivers are available
  *  device tree for the board

As of december 2022 (kernel version 6.1) there is no full official support for Allwinner D1 SOC which is in use by Lichee RV SOM.

Luckily the "official" work-in-progress linux kernel development is accessible via Samuel Holland's linux repo at https://github.com/smaeul/linux

It seems that it will take many more kernel release cycles before we gonna get full support for D1 SOC and Lichee dock. Maybe kernel versions after 6.3 will bring some good news.

As of WIP `kernel version 6.1-rc3` the Lichee dock is supported as following
* video
  * driver sun20i-d1-video-engine
  * driver sun4i-drm
* audio
  * driver sun20i-codec (ALSA driver)
* green LED on Lichee RV module
  * driver gpio-leds (GPIO led driver)
* RGB led on dock
  * driver sun50i-a100-ledc (led controller driver)
* white button labeled KEY on dock
  * driver sun50i-r329-lradc (input driver, decodes ADC voltages to KEY codes)
* GPIO
  * driver sun20i-d1-pinctrl

The driver for the WiFi is also not yet mainlined. The driver rtl8723ds usually comes built in with boot images.

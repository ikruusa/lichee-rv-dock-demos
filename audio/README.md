Lichee RV dock has on-board electret microphone circuit and 3W audio amplifier (with connector for a speaker).


Quick hint: unmute Headphones and set volume to non-zero:
`amixer -c 0 set Headphone playback 75% unmute`


Amplifier circuit in use is NS4150 by ShenZhen Nsiway Technology Co., Ltd. This is a filterless 3W@4 Ohm mono class D audio amplifier.

Audio output from D1 SoC is taken from headphone amplifier.
D1's headphone amplifier output is connected to the SoC's line input.

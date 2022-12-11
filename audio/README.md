Lichee dock has on-board electret microphone circuit and 3W mono audio amplifier (with connector for a speaker).
Audio amplifier circuit in use is NS4150 by ShenZhen Nsiway Technology Co., Ltd. This is a filterless 3W@4 Ohm mono class D audio amplifier.
Audio output from D1 SoC is taken from headphone amplifier.

Run `alsamixer` and check that channel named Headphone is unmuted and volume is reasonable.
To just set everything in place run `amixer -c 0 set Headphone playback 75% unmute`. After that you can play WAV files with `aplay` command.

